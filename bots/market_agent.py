import sys
import os
import logging
from datetime import datetime
import os
from engines.walkforward_engine import walkforward_test
import argparse
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import yfinance as yf
from engines.genome_engine import evolve_population
from backtest_utils import *
from data_utils import *
from core.portfolio_allocator import allocate_by_sharpe
from engines.evolve_engine import run_evolution_search
from engines.lab_engine import run_strategy_lab
from engines.scan_engine import run_scan_and_report
from core.volatility_regime import detect_volatility_regime
from bots.live_trading import run_live_simulation
from core.strategy_league import load_league, update_scores, save_league
from core.strategies import *
from core.portfolio_state import save_state, load_state
from core.signal_engine import generate_signals
from core.risk_manager import calculate_position_size
from core.strategy_stats import record_trade, print_strategy_stats
from engines.autonomous_engine import run_autonomous_cycle
from utils.reporting import max_drawdown, rolling_sharpe
from utils.strategy_loader import load_best_strategies
from engines.dna_engine import evolve_population as evolve_dna, random_gene
from visualization import *
from dashboard.ai_dashboard import print_ai_dashboard
from dashboard.dashboard import print_market, print_signals
from trend_panel import print_trend_panel, print_market_breadth
from trade_logger import log_trade
from scanners.momentum_scanner import find_momentum_leaders, print_momentum_leaders
from core.regime_brain import decide_strategy_mode


BOT_NAME = os.getenv("BOT_NAME", "default_bot")
STRATEGY = "adaptive"

MAX_DAILY_LOSS = -0.05   # stop trading at -5% daily loss

portfolio_tickers = []

def print_opportunity_heatmap(signals):

    print("\nOPPORTUNITY HEATMAP")
    print("-------------------")

    if not signals:
        print("None")
        return

    counts = {}

    for s in signals:
        ticker = s[2]   # FIXED (ticker is index 2)

        counts[ticker] = counts.get(ticker, 0) + 1

    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    for ticker, score in ranked[:10]:

        bar = "█" * score

        print(f"{ticker:<6} {bar:<10} {score}")


def rank_opportunities(signals):

    ranked = []

    for strat, action, ticker, votes in signals:

        if action != "BUY":
            continue

        score = votes * 2

        ranked.append((ticker, score))

    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked[:10]


def print_signal_radar(signals):

    print("\nSIGNAL RADAR")
    print("------------")

    if not signals:
        print("None")
        return

    counts = {}

    for s in signals:

        ticker = s[2]   # FIXED
        action = s[1]

        key = (ticker, action)

        counts[key] = counts.get(key, 0) + 1

    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    for (ticker, action), score in ranked[:10]:

        print(f"{ticker:<6} {action:<4} strength {score}")

def print_top_opportunities(signals):

    global portfolio_tickers

    top_trades = rank_opportunities(signals)[:5]

    portfolio_tickers = [t[0] for t in top_trades]

    print("\nAI PORTFOLIO MANAGER")
    print("--------------------")

    for t, score in top_trades:
        print(f"{t:<6} score:{score}")

        capital = 10000
        weight = capital / len(portfolio_tickers)

        portfolio_weights = {t: weight for t in portfolio_tickers}

        print("\nPORTFOLIO ALLOCATION")
        print("--------------------")

        for t, w in portfolio_weights.items():
            print(f"{t:<6} ${w:.0f}")

    ranked = rank_opportunities(signals)

    print("\nTOP OPPORTUNITIES")
    print("-----------------")

    if not ranked:
        print("None")
        return

    for ticker, score in ranked:
        print(f"{ticker:<6} score:{score}")




def print_risk_monitor(portfolio, prices):

    value = portfolio.total_value(prices)

    positions_value = value - portfolio.cash

    exposure = (positions_value / value) * 100 if value > 0 else 0

    largest = None
    largest_pct = 0

    for ticker, shares in portfolio.positions.items():

        price = prices.get(ticker, 0)

        pos_value = shares * price

        pct = (pos_value / value) * 100 if value > 0 else 0

        if pct > largest_pct:
            largest_pct = pct
            largest = ticker

    print("\nRISK MONITOR")
    print("------------")

    print(f"Exposure: {exposure:.1f}%")

    if largest:
        print(f"Largest Position: {largest} {largest_pct:.1f}%")

    if exposure > 80:
        print("⚠ WARNING: Portfolio exposure high")

    if largest_pct > 25:
        print("⚠ WARNING: Position concentration risk")


def load_watchlist(filename="watchlist.txt"):
    tickers = []

    try:
        with open(filename, "r") as f:
            for line in f:
                t = line.strip().upper()
                if t:
                    tickers.append(t)
    except FileNotFoundError:
        print("watchlist.txt not found")
        return []

    return tickers


TOP10 = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "META",
    "TSLA",
    "AVGO",
    "AMD",
    "NFLX"
]

DISCOVERY_UNIVERSE = [
    "NVDA", "AMD", "AVGO", "TSLA", "META", "AAPL", "MSFT",
    "GOOGL", "AMZN", "NFLX", "SMCI", "ARM", "INTC",
    "MU", "QCOM", "ADBE", "CRM", "ORCL", "NOW", "SHOP"
]


def load_crypto_watchlist(filename="crypto_watchlist.txt"):
    tickers = []

    try:
        with open(filename, "r") as f:
            for line in f:
                t = line.strip().upper()
                if t:
                    tickers.append(t)

    except FileNotFoundError:
        print("crypto_watchlist.txt not found")
        return []

    return tickers


def get_live_price(ticker):
    try:
        data = yf.Ticker(ticker)

        hist = data.history(period="5d", interval="5m")

        if hist.empty:
            return None

        price = hist["Close"].iloc[-1]

        if price <= 0:
            return None

        return float(price)

    except Exception:
        return None


def compute_sector_strength(data):
    sectors = {
        "AI": ["NVDA", "AMD"],
        "TECH": ["AAPL", "MSFT"],
        "MEDIA": ["META", "GOOGL"]
    }

    sector_scores = {}

    for sector, symbols in sectors.items():

        changes = []

        for s in symbols:
            if s in data and len(data[s]) >= 2:
                close = data[s]["Close"]
                pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

                changes.append(pct)

        if not changes:
            sector_scores[sector] = ("UNKNOWN", 0)
            continue

        avg = sum(changes) / len(changes)

        if avg > 0.01:
            label = "🟢 STRONG"
        elif avg < -0.01:
            label = "🔴 WEAK"
        else:
            label = "🟡 MIXED"

        sector_scores[sector] = (label, avg)

    return sector_scores


def print_market_regime(data):


    regimes = regime_history(data)

    if not regimes:
        return

    current = regimes[-1]

    vol_regime = detect_volatility_regime(data)

    print("\nVOLATILITY REGIME")
    print("-----------------")
    print(vol_regime)

    print("\nMARKET REGIME")
    print("-------------")

    if current == "TRENDING":
        print("TRENDING 📈")

    else:
        print("SIDEWAYS 🔄")


def print_strategy_agreement(symbol_data):
    buy_votes = 0
    sell_votes = 0
    hold_votes = 0

    for symbol, df in symbol_data.items():

        if len(df) < 20:
            continue

        votes = [
            analyze_market(df),
            mean_reversion_strategy(df),
            adaptive_strategy(df, {})
        ]

        for v in votes:
            if v == "BUY":
                buy_votes += 1
            elif v == "SELL":
                sell_votes += 1
            else:
                hold_votes += 1

    total = buy_votes + sell_votes + hold_votes

    if total == 0:
        return

    strongest = max(buy_votes, sell_votes, hold_votes) / total

    print("\nSTRATEGY AGREEMENT")
    print("------------------")

    if strongest > 0.70:
        print("HIGH AGREEMENT ⚡")
    elif strongest > 0.50:
        print("MODERATE AGREEMENT")
    else:
        print("LOW AGREEMENT ⚠️")


def compute_strategy_allocation(ma_sharpe, mr_sharpe, ad_sharpe):
    scores = {
        "MA": max(ma_sharpe, 0),
        "MR": max(mr_sharpe, 0),
        "AD": max(ad_sharpe, 0)
    }

    total = sum(scores.values())

    if total == 0:
        return {"MA": 0.33, "MR": 0.33, "AD": 0.33}

    weights = {k: v / total for k, v in scores.items()}

    return weights


def print_market_sentiment(symbol_data):
    score = 0

    for symbol, df in symbol_data.items():

        if len(df) < 2:
            continue

        close = df["Close"]

        pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

        if pct > 0.01:
            score += 1
        elif pct < -0.01:
            score -= 1

    print("\nMARKET SENTIMENT")
    print("----------------")

    if score >= 3:
        print("BULLISH 🔥🔥🔥")

    elif score >= 1:
        print("BULLISH 🔥")

    elif score == 0:
        print("NEUTRAL ⚖️")

    elif score <= -3:
        print("BEARISH ❄️❄️❄️")

    else:
        print("BEARISH ❄️")


def print_market_pulse(data, symbol_data, leaders):
    if args.crypto:
        print("\nAI CRYPTO TRADING LAB")
    else:
        print("\nAI TRADING LAB")
    print("--------------")

    print(f"BOT: {BOT_NAME}")

    # Market regime
    regimes = regime_history(data)
    regime = regimes[-1] if regimes else "UNKNOWN"

    if regime == "TRENDING":
        regime_label = "TRENDING 📈"
    else:
        regime_label = "SIDEWAYS 🔄"

    # Market sentiment
    score = 0
    for symbol, df in symbol_data.items():
        if len(df) < 2:
            continue

        close = df["Close"]
        pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

        if pct > 0.01:
            score += 1
        elif pct < -0.01:
            score -= 1

    if score >= 3:
        sentiment = "BULLISH 🔥🔥🔥"
    elif score >= 1:
        sentiment = "BULLISH 🔥"
    elif score == 0:
        sentiment = "NEUTRAL ⚖️"
    elif score <= -3:
        sentiment = "BEARISH ❄️❄️❄️"
    else:
        sentiment = "BEARISH ❄️"

    # Top stock
    if leaders:
        top_stock, pct = leaders[0]
        top_stock_label = f"{top_stock} {pct * 100:+.2f}%"
    else:
        top_stock_label = "None"

    print(f"REGIME        {regime_label}")
    print(f"SENTIMENT     {sentiment}")
    print(f"TOP STOCK     {top_stock_label}")


def print_strategy_confidence(symbol_data):
    buy_votes = 0
    sell_votes = 0
    hold_votes = 0

    for symbol, df in symbol_data.items():

        if len(df) < 20:
            continue

        vote_ma = analyze_market(df)
        vote_mr = mean_reversion_strategy(df)
        vote_ad = adaptive_strategy(df, {})

        votes = [vote_ma, vote_mr, vote_ad]

        for v in votes:
            if v == "BUY":
                buy_votes += 1
            elif v == "SELL":
                sell_votes += 1
            else:
                hold_votes += 1

    total = buy_votes + sell_votes + hold_votes

    if total == 0:
        return

    buy_pct = buy_votes / total
    sell_pct = sell_votes / total

    print("\nSTRATEGY CONSENSUS")
    print("------------------")

    bar = int(buy_pct * 10)

    print(f"BUY confidence  {'█' * bar}{'░' * (10 - bar)} {buy_pct * 100:.0f}%")
    print(f"SELL pressure   {sell_pct * 100:.0f}%")


def print_watchlist_momentum(data):
    changes = []

    for symbol, df in data.items():

        if len(df) < 2:
            continue

        close = df["Close"]

        pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

        changes.append((symbol, pct))

    changes.sort(key=lambda x: x[1], reverse=True)

    print("\nMOMENTUM LEADERS")
    print("----------------")

    for sym, pct in changes:
        print(f"{sym:<6} {pct * 100:+.2f}%")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="AI Trading Lab")

    parser.add_argument("--bot", default="default_bot")

    parser.add_argument("--strategy_name", default="adaptive")

    parser.add_argument("--ticker", type=str, default="SPY",
                        help="Stock ticker to analyze")

    parser.add_argument("--window", type=int, default=6,
                        help="Backtest window in months")

    parser.add_argument("--scan", type=str,
                        help="Run multi-ticker scan (example: sp500)")

    parser.add_argument("--limit", type=int, default=30,
                        help="Limit number of tickers during scan")

    parser.add_argument("--strategy", type=str,
                        help="Run single strategy: ma, mr, adaptive")

    parser.add_argument("--top", type=int,
                        help="Show top N strategies by Sharpe")

    parser.add_argument("--parallel", action="store_true",
                        help="Run multi-ticker scan in parallel")

    parser.add_argument("--sweep", action="store_true",
                        help="Run moving average parameter sweep")

    parser.add_argument("--report", action="store_true",
                        help="Save scan results and charts to reports folder")

    parser.add_argument("--live", action="store_true",
                        help="Run live portfolio simulation")

    parser.add_argument("--log", action="store_true", help="log output to file")

    # parser.add_argument("--discover", action="store_true",
    #                   help="Run automatic strategy discovery")

    parser.add_argument("--evolve", action="store_true",
                        help="Run evolutionary strategy search")

    parser.add_argument("--lab", action="store_true",
                        help="Run full strategy research lab")

    parser.add_argument("--debug-votes", action="store_true",
                        help="Print strategy votes during backtest")

    parser.add_argument("--reset", action="store_true",
                        help="Reset live trading state and start fresh")

    parser.add_argument(
        "--top10",
        action="store_true",
        help="Use top 10 stock universe instead of watchlist"
    )

    parser.add_argument("--autotrade", action="store_true",
                        help="Run top discovered strategies")

    parser.add_argument(
        "--cycle",
        action="store_true",
        help="Run autonomous scan → lab → trade cycle"
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run autonomous AI research cycle"
    )

    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run continuous AI trading loop"
    )
    parser.add_argument(
        "--crypto",
        action="store_true",
        help="Run crypto market scan"
    )

    args = parser.parse_args()

    if args.crypto:
        os.environ["BOT_NAME"] = "crypto_bot"

    if args.crypto:
        print("\nCRYPTO MODE ENABLED")
        print("-------------------")

        crypto_universe = []

        if not crypto_universe:
            crypto_universe = [
                "BTC-USD",
                "ETH-USD",
                "SOL-USD",
                "BNB-USD",
                "XRP-USD",
                "ADA-USD",
                "DOGE-USD",
                "AVAX-USD",
                "LINK-USD",
                "DOT-USD",
                "LTC-USD",
                "ATOM-USD",
                "NEAR-USD",
                "FIL-USD",
                "ETC-USD",
                "XLM-USD",
                "ARB-USD"
            ]

        args.scan = "crypto"
        args.limit = len(crypto_universe)

        print("Crypto Universe:")
        for c in crypto_universe:
            print(c)



    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
    AI TRADING LAB COMMANDS
    =======================

    Live Trading Simulation
    -----------------------
    python market_agent.py --live

    Reset Live Trading
    ------------------
    python market_agent.py --live --reset

    Run Strategy Lab
    ----------------
    python market_agent.py --lab --ticker NVDA

    Scan Market
    -----------
    python market_agent.py --scan sp500 --limit 50

    Evolutionary Strategy Search
    ----------------------------
    python market_agent.py --evolve --ticker NVDA

    Autonomous Research Cycle
    -------------------------
    python market_agent.py --cycle

    Continuous Trading Daemon
    -------------------------
    python market_agent.py --daemon

    Parameter Sweep
    ---------------
    python market_agent.py --sweep --ticker NVDA
    """)

        sys.exit()

    if args.crypto:
        if args.crypto:
            market_status = "CRYPTO MARKET (24/7)"
            print("\nMarket: CRYPTO (24/7)")

    if args.log:

        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        ticker = "market"
        if hasattr(args, "ticker"):
            ticker = args.ticker

        logfile = f"logs/{BOT_NAME}_{ticker}_{timestamp}.log"


        class Tee:
            def __init__(self, *files):
                self.files = files

            def write(self, obj):
                for f in self.files:
                    f.write(obj)
                    f.flush()

            def flush(self):
                for f in self.files:
                    f.flush()


        log_file = open(logfile, "a")

        sys.stdout = Tee(sys.stdout, log_file)
        sys.stderr = Tee(sys.stderr, log_file)

        print(f"Logging to {logfile}")

        if args.daemon:

            import time

            print("\nDaemon mode active")

            while True:

                try:
                    print("\nAI TRADING CYCLE START")

                    run_autonomous_cycle()

                except Exception as e:
                    print("Daemon error:", e)

                print("Sleeping 15 minutes...\n")

                time.sleep(900)



    if args.bot:
        BOT_NAME = args.bot

    STRATEGY = args.strategy_name

    if args.live:

        if args.crypto:
            universe = []
            crypto_universe = load_crypto_watchlist()

        elif args.top10:
            universe = TOP10
            crypto_universe = []

        else:
            universe = load_watchlist()
            crypto_universe = []

        print("\nTrading Universe")
        print("----------------")

        for t in universe:
            print(t)

        if crypto_universe:
            for c in crypto_universe:
                print(c)

        run_live_simulation(universe, crypto_universe)
        exit()

    ticker = args.ticker.upper()
    months = args.window

    if args.scan:

        if args.crypto:
            args.tickers = crypto_universe

        run_scan_and_report(args)
        exit()

    if args.lab:
        run_strategy_lab(args)
        exit()

    if args.auto:
        run_autonomous_cycle()
        exit()

    if args.cycle:

        print("\nAUTONOMOUS TRADING CYCLE")
        print("------------------------")

        leaders = find_momentum_leaders(DISCOVERY_UNIVERSE, top_n=3)

        print("\nMomentum Leaders")
        print("----------------")

        for sym, pct in leaders:
            print(f"{sym:<6} {pct * 100:+.2f}%")

        print("\nRunning strategy labs...\n")

        for sym, pct in leaders:

            try:
                print(f"Testing {sym}")

                lab_args = argparse.Namespace(
                    ticker=sym,
                    window=12,
                    top=5,
                    report=False
                )

                run_strategy_lab(lab_args)

            except Exception as e:
                print(f"Lab failed for {sym}: {e}")



        print("\nCycle complete.")

        exit()

    if args.evolve:
        run_evolution_search(args)
        exit()

    if args.crypto:

        symbol_data = {}

        import time

        for sym in crypto_universe:
            price = get_live_price(sym)
            time.sleep(0.2)

    else:

        spy_data = get_recent_data("SPY", 6)
        nvda_data = get_recent_data("NVDA", 6)
        amd_data = get_recent_data("AMD", 6)
        tsla_data = get_recent_data("TSLA", 6)
        meta_data = get_recent_data("META", 6)

        symbol_data = {
            "SPY": spy_data,
            "NVDA": nvda_data,
            "AMD": amd_data,
            "TSLA": tsla_data,
            "META": meta_data
        }

    print(f"\nRunning Strategy Comparison on {ticker}\n")
    print("=" * 70)

    if args.crypto:
        leaders = find_momentum_leaders(crypto_universe, top_n=5)
    else:
        leaders = find_momentum_leaders(DISCOVERY_UNIVERSE, top_n=5)

    print("\nAUTO STRATEGY DISCOVERY")
    print("-----------------------")

    for sym, pct in leaders:

        print(f"\nRunning strategy lab for {sym} ({pct * 100:+.2f}%)")

        try:
            result = run_strategy_lab(
                argparse.Namespace(
                    ticker=sym,
                    window=6,
                    top=10,
                    report=False
                )
            )

        except Exception as e:
            print(f"Lab failed for {sym}: {e}")

    if args.crypto:
        data = list(symbol_data.values())[0]
    else:
        data = symbol_data["SPY"]

    print_trend_panel(symbol_data)
    print_market_breadth(symbol_data)
    print_market_regime(data)
    print_market_sentiment(symbol_data)
    print_watchlist_momentum(symbol_data)
    print_strategy_confidence(symbol_data)
    print_strategy_agreement(symbol_data)

    print_momentum_leaders(leaders)

    data_cache = symbol_data
    adaptive_state = {}

    portfolio_tickers = []

    # --- DATA SAFETY CHECK ---
    bad_symbols = []

    for symbol, df in symbol_data.items():
        if df is None or len(df) == 0 or df["Close"].isna().any():
            bad_symbols.append(symbol)

    if bad_symbols:
        print("\n⚠ DATA ERROR - Skipping cycle")
        print("Missing data for:", ", ".join(bad_symbols))
        signals = []
    else:
        signals = generate_signals(symbol_data, data_cache, adaptive_state)

        # --- DAILY LOSS SAFETY ---
        if hasattr(adaptive_state, "start_equity"):

            current_equity = adaptive_state.get("equity", 0)
            start_equity = adaptive_state.get("start_equity", current_equity)

            if start_equity > 0:

                daily_return = (current_equity - start_equity) / start_equity

                if daily_return <= MAX_DAILY_LOSS:
                    print("\n⚠ DAILY LOSS LIMIT HIT")
                    print(f"Return: {daily_return * 100:.2f}%")

                    print("Trading halted for safety.")

                    sys.exit()
        # -------------------------
    # -------------------------

    print_opportunity_heatmap(signals)
    print_signal_radar(signals)
    print_top_opportunities(signals)

    portfolio_results = {}

    regimes = regime_history(data)
    market_regime = regimes[-1] if regimes else "UNKNOWN"

    volatility_regime = detect_volatility_regime(data)

    mode = decide_strategy_mode(market_regime, volatility_regime)

    print("\nAI MARKET MODE")
    print("--------------")
    print(mode)

    print("\nRUNNING PORTFOLIO BACKTEST")
    print("--------------------------")

    for sym in portfolio_tickers:
        print(f"\nRunning strategies for {sym}")

        data = get_recent_data(sym, months)

        equity, final, *_ = run_backtest(data, analyze_market)

        portfolio_results[sym] = final

        print("\nPORTFOLIO RESULTS")
        print("-----------------")

        for sym, val in portfolio_results.items():
            print(f"{sym:<6} ${val:,.2f}")



    # Build portfolio from signals
    portfolio_tickers = []

    top_trades = rank_opportunities(signals)[:5]

    print("\nAI PORTFOLIO MANAGER")
    print("--------------------")

    for t, score in top_trades:
        print(f"{t:<6} score:{score}")
        portfolio_tickers.append(t)

    # ----- Strategy Council Snapshot -----

    votes = []

    if mode in ["TREND", "NEUTRAL"]:
        votes.append(analyze_market(data))

    if mode in ["MEAN_REVERSION", "NEUTRAL"]:
        votes.append(mean_reversion_strategy(data))

    if mode != "DEFENSIVE":
        votes.append(adaptive_strategy(data, {}))

    votes.append(volatility_breakout_strategy(data))

    council_votes = votes

    buy_votes = council_votes.count("BUY")
    sell_votes = council_votes.count("SELL")

    decision = "HOLD"

    if buy_votes >= 3:
        decision = "BUY"
    elif sell_votes >= 3:
        decision = "SELL"

    confidence = max(buy_votes, sell_votes) / len(council_votes)

    sectors = compute_sector_strength(symbol_data)

    print("\nDNA STRATEGY EVOLUTION")
    print("----------------------")

    population = [random_gene() for _ in range(40)]

    generations = 5

    for g in range(generations):

        print(f"\nGeneration {g + 1}")

        population_scores = []

        for gene in population:

            strat, p1, p2 = gene

            try:

                if strat == "MA":
                    equity, final, *_ = run_backtest(
                        data,
                        lambda d: analyze_market(d, p1, p2)
                    )

                elif strat == "MR":
                    equity, final, *_ = run_backtest(
                        data,
                        lambda d: mean_reversion_strategy(d, -p1 / 100)
                    )

                elif strat == "VOL":
                    equity, final, *_ = run_backtest(
                        data,
                        volatility_breakout_strategy
                    )

                sharpe = calculate_sharpe(equity)

            except Exception:
                sharpe = -999

            population_scores.append((gene, sharpe))

        population = evolve_dna(population_scores)

    print(f"Next generation created: {len(population)} strategies")

    print("\nGENOME STRATEGY DISCOVERY")
    print("-------------------------")

    genomes = evolve_population(data)

    league = load_league()  # load once

    for g, sharpe in genomes:

        strat, p1, p2 = g

        if p2:
            params = f"{p1}/{p2}"
        else:
            params = f"{p1}"

        print(f"{strat} {params} Sharpe {sharpe:.2f}")

        league.append({
            "strategy": strat,
            "short": p1,
            "long": p2,
            "sharpe": sharpe,
            "wins": 0,
            "losses": 0,
            "score": sharpe
        })

    league = update_scores(league)

    save_league(league)

    print("\nSTRATEGY LEAGUE TOP 10")
    print("----------------------")

    for s in league[:10]:

        short = s["short"]
        long = s["long"]

        if long:
            params = f"{short}/{long}"
        else:
            params = f"{short}"

        print(
            f"{s['strategy']} {params} "
            f"Sharpe:{s['sharpe']:.2f} "
            f"Score:{s['score']:.2f}"
        )


    print("-" * 70)
    print("\nSECTOR FLOW")
    print("-----------")

    for sector, (label, pct) in sorted(sectors.items()):
        pct_str = f"{pct * 100:+.2f}%"

        print(f"{sector:<7} {label:<10} {pct_str}")

    # Run strategies
    ma_equity, ma_final, ma_buys, ma_sells, ma_profits = run_backtest(data, analyze_market)

    wf = walkforward_test(data, analyze_market)

    print("\nWALK FORWARD TEST")
    print("-----------------")
    print(f"Train Sharpe: {wf['train_sharpe']:.2f}")
    print(f"Test Sharpe:  {wf['test_sharpe']:.2f}")

    mr_equity, mr_final, mr_buys, mr_sells, mr_profits = run_backtest(data, mean_reversion_strategy)
    adaptive_equity, adaptive_final, ad_buys, ad_sells, ad_profits = run_backtest(data, adaptive_strategy)

    vol_equity, vol_final, vol_buys, vol_sells, vol_profits = run_backtest(
        data, volatility_breakout_strategy
    )

    vote_state = {"debug": args.debug_votes}

    vote_equity, vote_final, vote_buys, vote_sells, vote_profits = run_backtest(
        data,
        lambda d: voting_strategy(d, vote_state)
    )

    best_strategies = load_best_strategies(10)

    trend_strategies = best_strategies[:5]
    sideways_strategies = best_strategies[5:10]

    council_state = {
        "trend_strategies": trend_strategies,
        "sideways_strategies": sideways_strategies,
        "debug": args.debug_votes
    }

    vote_ma = analyze_market(data)
    vote_mr = mean_reversion_strategy(data)
    vote_ad = adaptive_strategy(data, {})
    vote_vol = volatility_breakout_strategy(data)

    council_votes = [vote_ma, vote_mr, vote_ad, vote_vol]

    buy_votes = council_votes.count("BUY")
    sell_votes = council_votes.count("SELL")

    decision = "HOLD"

    if buy_votes >= 3:
        decision = "BUY"
    elif sell_votes >= 3:
        decision = "SELL"

    confidence = max(buy_votes, sell_votes) / len(council_votes)

    council_equity, council_final, council_buys, council_sells, council_profits = run_backtest(
        data,
        lambda d: council_strategy(d, council_state)
    )

    ma_sharpe = calculate_sharpe(ma_equity)
    mr_sharpe = calculate_sharpe(mr_equity)
    adaptive_sharpe = calculate_sharpe(adaptive_equity)
    vol_sharpe = calculate_sharpe(vol_equity)

    strategy_sharpes = {
        "MA": ma_sharpe,
        "MR": mr_sharpe,
        "AD": adaptive_sharpe,
        "VOL": vol_sharpe
    }

    print("\nSTRATEGY SURVIVAL ENGINE")
    print("------------------------")

    for name, sharpe in strategy_sharpes.items():

        if sharpe < -0.5:
            print(f"{name:<5} ❌ KILLED (Sharpe {sharpe:.2f})")
            strategy_sharpes[name] = 0

        elif sharpe < 0:
            print(f"{name:<5} ⚠ WEAK (Sharpe {sharpe:.2f})")

        else:
            print(f"{name:<5} 🟢 SURVIVES (Sharpe {sharpe:.2f})")

    weights = allocate_by_sharpe(strategy_sharpes)

    capital = 10000

    print("\nAI CAPITAL ALLOCATION")
    print("---------------------")

    for strat, weight in weights.items():
        allocation = capital * weight

        print(f"{strat:<5} ${allocation:,.0f} ({weight * 100:.1f}%)")



        if mode == "DEFENSIVE":
            print("\nDEFENSIVE MODE ACTIVATED")
            print("------------------------")

            capital *= 0.5

            print(f"Capital reduced to ${capital:,.0f}")

    print("\nSTRATEGY HEALTH MONITOR")
    print("-----------------------")

    for name, sharpe in strategy_sharpes.items():

        if sharpe < -0.5:
            print(f"{name:<6} ❌ DISABLED (Sharpe {sharpe:.2f})")
            strategy_sharpes[name] = 0

        elif sharpe < 0:
            print(f"{name:<6} ⚠ WEAK (Sharpe {sharpe:.2f})")

        else:
            print(f"{name:<6} ✔ HEALTHY (Sharpe {sharpe:.2f})")


    print("\nSTRATEGY ALLOCATION")
    print("-------------------")

    for k, v in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        print(f"{k:<3} {v * 100:5.1f}%")

    vote_sharpe = calculate_sharpe(vote_equity)
    council_sharpe = calculate_sharpe(council_equity)

    # Buy & Hold
    first_price = data["Close"].iloc[0]
    last_price = data["Close"].iloc[-1]

    bh_shares = 10000 / first_price
    bh_final = bh_shares * last_price

    bh_equity = []
    for i in range(30, len(data)):
        price = data["Close"].iloc[i]
        bh_equity.append(bh_shares * price)

    bh_sharpe = calculate_sharpe(bh_equity)

    strategy_results = {
        "MA": {"final": ma_final, "sharpe": ma_sharpe},
        "MR": {"final": mr_final, "sharpe": mr_sharpe},
        "Adaptive": {"final": adaptive_final, "sharpe": adaptive_sharpe},
        "Vote": {"final": vote_final, "sharpe": vote_sharpe},
        "Council": {"final": council_final, "sharpe": council_sharpe},
        "BuyHold": {"final": bh_final, "sharpe": bh_sharpe},
        "Volatility": {"final": vol_final, "sharpe": vol_sharpe},
    }

    from leaderboard import print_leaderboard

    print_leaderboard(strategy_results)

    if args.sweep:

        short_windows = range(5, 31, 5)
        long_windows = range(20, 201, 20)

        results = []
        top_results = []

        for s in short_windows:
            for l in long_windows:

                if s >= l:
                    continue


                def ma_strategy(data, short=s, long=l):
                    return analyze_market(data, short, long)


                equity, final_value, _, _, _ = run_backtest(data, ma_strategy)
                sharpe = calculate_sharpe(equity)

                results.append((s, l, final_value, sharpe))
                top_results.append((s, l, final_value, sharpe))

        print("\nMA Parameter Sweep Results\n")

        results.sort(key=lambda x: x[3], reverse=True)
        top_results.sort(key=lambda x: x[3], reverse=True)

        for r in results:
            short_ma = r[0]
            long_ma = r[1]
            final_val = r[2]
            sharpe = r[3]

            print(
                f"MA {short_ma}/{long_ma} | "
                f"Final: {round(final_val, 2):>10} | "
                f"Sharpe: {round(sharpe, 2):>6}"
            )

        print("\nTop 10 Moving Average Strategies\n")

        for r in top_results[:10]:
            print(
                f"MA {r[0]}/{r[1]} | "
                f"Final: ${r[2]:,.2f} | "
                f"Sharpe: {r[3]:.2f}"
            )

    # Drawdowns
    ma_drawdown = calculate_drawdown(ma_equity)
    mr_drawdown = calculate_drawdown(mr_equity)
    adaptive_drawdown = calculate_drawdown(adaptive_equity)
    bh_drawdown = calculate_drawdown(bh_equity)
    ma_max_dd = max_drawdown(ma_drawdown)
    mr_max_dd = max_drawdown(mr_drawdown)
    adaptive_max_dd = max_drawdown(adaptive_drawdown)

    MAX_DRAWDOWN_LIMIT = 0.25

    if ma_max_dd > MAX_DRAWDOWN_LIMIT:
        print("⚠ MA strategy halted due to drawdown")

    if mr_max_dd > MAX_DRAWDOWN_LIMIT:
        print("⚠ MR strategy halted due to drawdown")

    if adaptive_max_dd > MAX_DRAWDOWN_LIMIT:
        print("⚠ Adaptive strategy halted due to drawdown")
    bh_max_dd = max_drawdown(bh_drawdown)

    MAX_DRAWDOWN_LIMIT = 0.25

    if ma_max_dd > MAX_DRAWDOWN_LIMIT:
        print("⚠ MA strategy halted due to drawdown")

    if mr_max_dd > MAX_DRAWDOWN_LIMIT:
        print("⚠ MR strategy halted due to drawdown")

    if adaptive_max_dd > MAX_DRAWDOWN_LIMIT:
        print("⚠ Adaptive strategy halted due to drawdown")

    ma_roll = rolling_sharpe(ma_equity)
    mr_roll = rolling_sharpe(mr_equity)
    ad_roll = rolling_sharpe(adaptive_equity)

    # Trade stats
    ma_wins, ma_losses, ma_wr, ma_avg = trade_statistics(ma_profits)
    mr_wins, mr_losses, mr_wr, mr_avg = trade_statistics(mr_profits)
    ad_wins, ad_losses, ad_wr, ad_avg = trade_statistics(ad_profits)
    ma_pf = profit_factor(ma_profits)
    mr_pf = profit_factor(mr_profits)
    ad_pf = profit_factor(ad_profits)

    print("\nSTRATEGY PERFORMANCE")
    print("--------------------------------------------")

    strategy_table = [
        ("MA", ma_final, ma_sharpe, ma_max_dd),
        ("MR", mr_final, mr_sharpe, mr_max_dd),
        ("Adaptive", adaptive_final, adaptive_sharpe, adaptive_max_dd),
        ("Vote", vote_final, vote_sharpe, 0),
        ("Council", council_final, council_sharpe, 0),
        ("BuyHold", bh_final, bh_sharpe, bh_max_dd),
    ]

    strategy_table.sort(key=lambda x: x[2], reverse=True)

    print(f"{'Strategy':<12}{'Final':>12}{'Sharpe':>10}{'MaxDD':>10}")

    for name, final, sharpe, dd in strategy_table:
        print(f"{name:<12}{final:>12.2f}{sharpe:>10.2f}{dd * 100:>9.2f}%")

        # Profit attribution
        print("\nPROFIT ATTRIBUTION")
        print("------------------")

        starting_capital = 10000

        attribution = {
            "MA": ma_final - starting_capital,
            "MR": mr_final - starting_capital,
            "Adaptive": adaptive_final - starting_capital,
            "Vote": vote_final - starting_capital,
            "Council": council_final - starting_capital,
            "BuyHold": bh_final - starting_capital,
        }

        # sort best → worst
        sorted_attr = sorted(attribution.items(), key=lambda x: x[1], reverse=True)

        for name, profit in sorted_attr:

            if profit > 0:
                icon = "🟢"
            elif profit < 0:
                icon = "🔴"
            else:
                icon = "⚪"

            print(f"{name:<10} {icon} ${profit:,.2f}")

    # Record trades for strategy intelligence

    for p in ma_profits:
        record_trade("MA", p)

        log_trade(
            ticker,
            "TRADE",
            1,
            p,
            "MA",
            0,
            ma_final
        )

    for p in ad_profits:
        record_trade("AD", p)

        log_trade(
            ticker,
            "TRADE",
            1,
            p,
            "AD",
            0,
            adaptive_final
        )

    for p in mr_profits:
        record_trade("MR", p)

        log_trade(
            ticker,
            "TRADE",
            1,
            p,
            "MR",
            0,
            mr_final
        )
    print_strategy_stats()

    print("\nMoving Average")
    print("Trades:", len(ma_profits))
    print("Win Rate:", round(ma_wr * 100, 1), "%")
    print("Avg Trade:", round(ma_avg, 2))
    print("Profit Factor:", round(ma_pf, 2))

    print("\nAdaptive")
    print("Trades:", len(ad_profits))
    print("Win Rate:", round(ad_wr * 100, 1), "%")
    print("Avg Trade:", round(ad_avg, 2))
    print("Profit Factor:", round(ad_pf, 2))

    print("\nBuy & Hold Final Value:", round(bh_final, 2))
    print("Buy & Hold Sharpe:", round(bh_sharpe, 2))
    print("Buy & Hold Max Drawdown:", round(bh_max_dd * 100, 2), "%")

    # print("\nTrade Statistics")

    print("\nMean Reversion")
    print("Trades:", len(mr_profits))
    print("Win Rate:", round(mr_wr * 100, 1), "%")
    print("Avg Trade:", round(mr_avg, 2))

    print("\nVoting Strategy")
    print("Trades:", len(vote_profits))

    vote_wins = sum(1 for p in vote_profits if p > 0)
    vote_losses = sum(1 for p in vote_profits if p <= 0)

    vote_wr = vote_wins / len(vote_profits) if vote_profits else 0
    vote_avg = sum(vote_profits) / len(vote_profits) if vote_profits else 0

    print("Win Rate:", round(vote_wr * 100, 1), "%")
    print("Avg Trade:", round(vote_avg, 2))
    print("Sharpe:", round(vote_sharpe, 2))

    print("\nStrategy Council")
    print("Trades:", len(council_profits))

    council_wins = sum(1 for p in council_profits if p > 0)
    council_wr = council_wins / len(council_profits) if council_profits else 0
    council_avg = sum(council_profits) / len(council_profits) if council_profits else 0

    print("Win Rate:", round(council_wr * 100, 1), "%")
    print("Avg Trade:", round(council_avg, 2))
    print("Sharpe:", round(council_sharpe, 2))

    # Plot
    fig, (ax0, ax1, ax2, ax3, ax4, ax5) = plt.subplots(6, 1, figsize=(14, 12), sharex=False)

    price_series = data["Close"].iloc[50:].reset_index(drop=True)

    regimes = regime_history(data)[50:]

    ax0.plot(price_series, color="black", linewidth=2, label="Price")

    # Regime shading
    limit = min(len(price_series) - 1, len(regimes))

    for i in range(limit):

        if regimes[i] == "TRENDING":
            ax0.axvspan(i, i + 1, color="green", alpha=0.08)

        else:
            ax0.axvspan(i, i + 1, color="yellow", alpha=0.08)

    # Moving Average trades
    x, y = safe_points(ma_buys, price_series)

    for i, (bx, by) in enumerate(zip(x, y), start=1):

        if confidence >= 0.75:
            color = "lime"
        elif confidence >= 0.5:
            color = "yellow"
        else:
            color = "dodgerblue"

        ax0.scatter(bx, by, marker="^", color=color, s=160)

        ax0.text(
            bx,
            by + 2,
            str(i),
            fontsize=12,
            fontweight="bold",
            ha="center"
        )



    x, y = safe_points(ma_sells, price_series)
    ax0.scatter(x, y, marker="v", color="red", s=80)

    for i, (sx, sy) in enumerate(zip(x, y), start=1):
        ax0.text(sx, sy - 1, f"{i}", fontsize=12, ha="center", va="top", color="black")

    # Mean Reversion trades
    x, y = safe_points(mr_buys, price_series)
    ax0.scatter(x, y, marker="^", color="orange", s=80)

    x, y = safe_points(mr_sells, price_series)
    ax0.scatter(x, y, marker="v", color="darkorange", s=80)

    # Adaptive trades
    x, y = safe_points(ad_buys, price_series)
    ax0.scatter(x, y, marker="^", color="purple", s=80)

    x, y = safe_points(ad_sells, price_series)
    ax0.scatter(x, y, marker="v", color="magenta", s=160)


    ax0.set_title(f"{ticker} Price", fontsize=15, fontweight="bold", loc="left")

    ax0.text(
        0.01,
        0.95,
        "BUY confidence: green=strong  yellow=medium  blue=weak",
        transform=ax0.transAxes,
        fontsize=9
    )

    ax0.legend(loc="upper left")
    ax0.grid(True)

    equity = ma_equity
    regimes = regime_history(data)[50:]

    equity = ma_equity
    regimes = regime_history(data)[50:]

    limit = min(len(equity) - 1, len(regimes))

    for i in range(limit):

        if regimes[i] == "TRENDING":
            color = "green"
        else:
            color = "gold"

        ax1.plot(
            [i, i + 1],
            [equity[i], equity[i + 1]],
            color=color,
            linewidth=3
        )

    ax1.plot(mr_equity, label="Mean Reversion", linewidth=3, linestyle="--")
    ax1.plot(adaptive_equity, label="Adaptive", linewidth=3)
    ax1.plot(bh_equity, label="Buy & Hold", linewidth=3)
    ax1.plot(vote_equity, label="Voting Strategy", linewidth=3)
    ax1.plot(council_equity, label="Strategy Council", linewidth=3)

    # Moving Average trades
    x, y = safe_points(ma_buys, ma_equity)
    ax1.scatter(x, y, marker="^", color="green", s=80)

    for i, (bx, by) in enumerate(zip(x, y), start=1):
        ax1.text(bx, by + 50, f"{i}", fontsize=12, ha="center")

    x, y = safe_points(ma_sells, ma_equity)

    for i, (sx, sy) in enumerate(zip(x, y), start=1):

        if i - 1 < len(ma_profits) and ma_profits[i - 1] > 0:
            color = "lime"
        else:
            color = "red"

        ax1.scatter(sx, sy, marker="v", color=color, s=160)

        ax1.text(
            sx,
            sy - 80,
            str(i),
            fontsize=13,
            fontweight="bold",
            ha="center"
        )


    # Mean Reversion trades
    x, y = safe_points(mr_buys, mr_equity)
    ax1.scatter(x, y, marker="^", color="orange", s=80)

    x, y = safe_points(mr_sells, mr_equity)
    ax1.scatter(x, y, marker="v", color="darkorange", s=80)

    # Adaptive trades
    x, y = safe_points(ad_buys, adaptive_equity)
    ax1.scatter(x, y, marker="^", color="purple", s=80)

    x, y = safe_points(ad_sells, adaptive_equity)
    ax1.scatter(x, y, marker="v", color="magenta", s=80)

    ax1.axhline(y=10000, linestyle="--", color="black")

    ax1.set_title(f"{ticker} Strategy Comparison", fontsize=16, fontweight="bold", loc="left")
    ax1.legend(loc="upper left")
    ax1.grid(True)
    ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    ax2.plot(ma_drawdown, label="MA Drawdown", linewidth=3, color="blue")
    ax2.plot(mr_drawdown, label="MR Drawdown", linewidth=3, color="red", linestyle="--")
    ax2.plot(adaptive_drawdown, label="Adaptive Drawdown", linewidth=3, color="purple")
    ax2.plot(bh_drawdown, label="Buy & Hold Drawdown", linewidth=3, color="green")

    ax2.axhline(y=0, color="black", linewidth=2, linestyle="--", alpha=0.5)

    ax2.set_title("Drawdown", fontsize=15, fontweight="bold", loc="left")
    ax2.legend(loc="upper left")
    ax2.grid(True)

    # Trade Profit Distribution
    ax3.hist(ma_profits, bins=20, alpha=0.6, label="MA")
    ax3.hist(mr_profits, bins=20, alpha=0.6, label="MR")
    ax3.hist(ad_profits, bins=20, alpha=0.6, label="Adaptive")

    ax3.set_title("Trade Profit Distribution", fontsize=15, fontweight="bold", loc="left")
    ax3.set_xlabel("Profit per Trade")
    ax3.set_ylabel("Number of Trades")

    ax3.legend(loc="upper left")
    ax3.grid(True)

    # Win/Loss Distribution
    ma_wins = sum(1 for p in ma_profits if p > 0)
    ma_losses = sum(1 for p in ma_profits if p <= 0)

    mr_wins = sum(1 for p in mr_profits if p > 0)
    mr_losses = sum(1 for p in mr_profits if p <= 0)

    ad_wins = sum(1 for p in ad_profits if p > 0)
    ad_losses = sum(1 for p in ad_profits if p <= 0)

    labels = ["MA Wins", "MA Losses", "MR Wins", "MR Losses", "AD Wins", "AD Losses"]
    values = [ma_wins, ma_losses, mr_wins, mr_losses, ad_wins, ad_losses]

    colors = ["green", "red", "orange", "darkorange", "purple", "magenta"]

    ax4.bar(labels, values, color=colors)

    ax4.set_title("Win/Loss Trade Count", fontsize=15, fontweight="bold", loc="left")
    ax4.set_ylabel("Number of Trades")
    ax4.grid(True)

    # Rolling Sharpe Ratio
    ax5.plot(ma_roll, label="MA Sharpe", linewidth=2)
    ax5.plot(mr_roll, label="MR Sharpe", linewidth=2)
    ax5.plot(ad_roll, label="Adaptive Sharpe", linewidth=2)

    ax5.axhline(y=0, color="black", linestyle="--", linewidth=1)

    ax5.set_title("Rolling Sharpe Ratio", fontsize=15, fontweight="bold", loc="left")
    ax5.set_ylabel("Sharpe")
    ax5.set_xlabel("Backtest Days")

    ax5.legend(loc="upper left")
    ax5.grid(True)

    # Calculate strategy returns
    ma_returns = np.diff(ma_equity) / ma_equity[:-1]
    mr_returns = np.diff(mr_equity) / mr_equity[:-1]
    ad_returns = np.diff(adaptive_equity) / adaptive_equity[:-1]

    # Strategy returns for correlation
    min_len = min(len(ma_returns), len(mr_returns), len(ad_returns))

    ma_returns = ma_returns[:min_len]
    mr_returns = mr_returns[:min_len]
    ad_returns = ad_returns[:min_len]

    # Prevent numpy warnings if strategies never traded
    if (
            len(ma_returns) == 0
            or len(mr_returns) == 0
            or len(ad_returns) == 0
            or np.std(ma_returns) == 0
            or np.std(mr_returns) == 0
            or np.std(ad_returns) == 0
    ):
        corr_matrix = None
    else:
        corr_matrix = np.corrcoef([
            ma_returns,
            mr_returns,
            ad_returns
        ])
    if corr_matrix is not None:
        print("\nStrategy Correlation Matrix")
        print(" MA   MR   AD")
        for row in corr_matrix:
            print(" ".join(f"{v:5.2f}" for v in row))

    print(f"\nGenerating chart for: {ticker}")

    plt.tight_layout()

    # save chart
    plt.savefig(f"chart_{ticker}_{BOT_NAME}.png")

    # print("Displaying chart window...")

    # plt.show()
