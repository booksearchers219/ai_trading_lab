import sys
import os
from datetime import datetime, timedelta
from engines.walkforward_engine import walkforward_test
import argparse
import traceback
from analysis.performance_report import print_strategy_performance
import time
from analysis.market_analysis import (
    print_market_regime,
    print_market_sentiment,
    print_watchlist_momentum,
    print_strategy_confidence,
    print_strategy_agreement,
    compute_sector_strength
)
from backtest_utils import *
from data_utils import *
from core.portfolio_allocator import allocate_by_sharpe
from engines.evolve_engine import run_evolution_search
from engines.lab_engine import run_strategy_lab
from engines.scan_engine import run_scan_and_report
from core.volatility_regime import detect_volatility_regime
from bots.live_trading import run_live_simulation
from core.strategy_league import load_league, update_scores, save_league
from core.strategies import (
    analyze_market,
    mean_reversion_strategy,
    adaptive_strategy,
    volatility_breakout_strategy,
    voting_strategy,
    council_strategy,
)

from core.signal_engine import generate_signals

from core.strategy_stats import record_trade, print_strategy_stats
from engines.autonomous_engine import run_autonomous_cycle
from utils.reporting import max_drawdown, rolling_sharpe
from utils.strategy_loader import load_best_strategies
import json
from visualization.backtest_report_bak_simple import generate_backtest_report
import time
import random
from trend_panel import print_trend_panel, print_market_breadth
from trade_logger import log_trade
from scanners.momentum_scanner import find_momentum_leaders, print_momentum_leaders
from core.regime_brain import decide_strategy_mode
from analysis.signal_analysis import (
    print_opportunity_heatmap,
    rank_opportunities,
    print_signal_radar,
    print_top_opportunities,

)
from evolution.genome_engine import evolve_population
from evolution.dna_engine import evolve_population as evolve_dna, random_gene
from evolution.darwin_engine import run_strategy_darwinism

STRATEGY = "adaptive"

MAX_DAILY_LOSS = -0.05  # stop trading at -5% daily loss

# --------------------------------------------------
# DISCOVERY UNIVERSE
# --------------------------------------------------
# These stocks are used by the momentum scanner to
# decide which markets deserve research attention.
# Expanding this list gives the AI more opportunities.
# --------------------------------------------------

DISCOVERY_UNIVERSE = [
    "NVDA", "AMD", "AVGO", "TSLA", "META", "AAPL", "MSFT", "GOOGL", "AMZN", "NFLX",

    "SMCI", "ARM", "INTC", "MU", "QCOM", "ADBE", "CRM", "ORCL", "NOW", "SHOP",

    "PLTR", "COIN", "MSTR", "SNOW", "PANW", "NET", "DDOG", "ZS",

    "UBER", "LYFT", "PYPL", "ROKU",

    "COST", "WMT", "HD", "LOW", "TGT"
]

EVOLUTION_TEST_UNIVERSE = [
    "SPY",
    "QQQ",
    "NVDA",
    "BTC-USD",
    "ETH-USD"
]

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


# --------------------------------------------------
# AI Ticker Selection
# --------------------------------------------------
# This function chooses the most interesting tickers
# for strategy research.
#
# It prioritizes stocks with:
# - high volatility
# - large recent moves
#
# This prevents the research daemon from wasting time
# on slow or inactive stocks.
# --------------------------------------------------


def select_research_tickers(results, limit=50):
    ranked = []

    for r in results:
        ticker = r.get("ticker")

        # use absolute move as a proxy for volatility
        move = abs(r.get("pct_move", 0))

        ranked.append((move, ticker))

    # sort by biggest moves
    ranked.sort(reverse=True)

    # take the top candidates
    top = [t for _, t in ranked[:limit]]

    # if something goes wrong fallback to random selection
    if len(top) < limit:
        pool = [r.get("ticker") for r in results]

        random.shuffle(pool)

        top = pool[:limit]

    return top


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


def print_market_pulse(data, symbol_data, leaders, BOT_NAME):
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


def run_research_pipeline(BOT_NAME, crypto_universe=None):
    print("\nRunning research pipeline")

    # --------------------------------------------------
    # SMART RESEARCH SCAN
    # --------------------------------------------------
    # Scan a larger pool of S&P stocks so we are not
    # stuck with alphabetical tickers.
    # The scan engine will then rank opportunities
    # and keep the best ones.
    # --------------------------------------------------

    # --------------------------------------------------
    # VOLATILITY RADAR RESEARCH MODE
    # --------------------------------------------------
    # Instead of scanning alphabetical S&P stocks,
    # we first find the most active stocks in the market.
    #
    # These are the best candidates for discovering
    # profitable trading strategies.
    # --------------------------------------------------

    print("\nScanning market for momentum leaders...")

    # Find the 100 most active stocks from the discovery universe
    if args.crypto:
        if crypto_universe is None:
            crypto_universe = load_crypto_watchlist() or ["BTC-USD", "ETH-USD"]
        leaders = find_momentum_leaders(crypto_universe, top_n=15)
    else:
        leaders = find_momentum_leaders(DISCOVERY_UNIVERSE, top_n=15)

    selected_tickers = []

    for sym, pct in leaders:

        # Skip tickers with missing or bad data
        if pct != pct:
            print(f"Skipping {sym} (no data)")
            continue

        print(f"Research candidate: {sym} {pct * 100:+.2f}%")
        selected_tickers.append(sym)

    # --------------------------------------------------
    # Run research scan for each momentum ticker
    # --------------------------------------------------

    for sym in selected_tickers:
        print(f"\nRunning scan for {sym}")

        scan_args = argparse.Namespace(
            scan=None,
            ticker=sym,
            window=6,
            crypto=False,
            parallel=False,
            report=False,
            top=10
        )

        run_scan_and_report(scan_args)

    if args.crypto:
        base_symbol = "BTC-USD"
    else:
        base_symbol = "SPY"

    evo_args = argparse.Namespace(ticker=base_symbol, window=12)
    run_evolution_search(evo_args)

    lab_args = argparse.Namespace(
        ticker=base_symbol,
        window=12,
        top=10,
        report=False,
        crypto=args.crypto
    )

    run_strategy_lab(lab_args, BOT_NAME)

    # --------------------------------------------------
    # Export best strategies for trading bots
    # --------------------------------------------------

    try:

        league = load_league()

        top_strategies = [s for s in league if s["sharpe"] > 0][:10]

        export_data = []

        for s in top_strategies:
            export_data.append({
                "strategy": s["strategy"],
                "short": s.get("short"),
                "long": s.get("long"),
                "sharpe": s.get("sharpe")
            })

        with open(f"best_strategies_{BOT_NAME}.json", "w") as f:
            json.dump(export_data, f, indent=2)

        print("Exported best_strategies.json")

    except Exception as e:
        print("Strategy export failed:", e)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="AI Trading Lab")

    parser.add_argument("--research", action="store_true", help="Run full strategy research pipeline")

    parser.add_argument("--bot", default="default_bot")

    parser.add_argument("--strategy_name", default="adaptive")

    parser.add_argument("--ticker", type=str, default=None,
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
        "--research-daemon",
        action="store_true",
        help="Run continuous strategy discovery loop"
    )

    parser.add_argument(
        "--crypto",
        action="store_true",
        help="Run crypto market scan"
    )
    args = parser.parse_args()

    crypto_mode = args.crypto

    if args.crypto and not args.ticker:
        args.ticker = "BTC-USD"

    BOT_NAME = "crypto_bot" if crypto_mode else "equity_bot"

    print(f"DEBUG BOT INIT: {BOT_NAME} | crypto_mode={crypto_mode}")

    # --------------------------------------------------
    # Research mode
    # --------------------------------------------------
    if args.research:
        print("\n==============================")
        print("AUTONOMOUS RESEARCH MODE")
        print("==============================")

        run_research_pipeline(BOT_NAME)
        sys.exit()

    print("\n==============================")
    print("AI TRADING LAB STARTING")
    print("==============================")
    print("Bot:", BOT_NAME)
    print("Crypto Mode:", args.crypto)
    print("Daemon Mode:", args.daemon)
    print("Live Mode:", args.live)
    print("==============================\n")

    # --------------------------------------------------
    # Reset live trading state
    # --------------------------------------------------
    if args.reset:

        state_file = f"portfolio_state_{BOT_NAME}.json"

        print("\nRESET FLAG DETECTED")
        print("-------------------")

        if os.path.exists(state_file):
            os.remove(state_file)
            print(f"Deleted saved state: {state_file}")
        else:
            print("No saved state found.")

        print("Live trading state reset.\n")

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
                # "ARB-USD"
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

    # --------------------------------------------------
    # Bot name override
    # --------------------------------------------------
    if args.crypto:
        BOT_NAME = "crypto_bot"
    else:
        BOT_NAME = "equity_bot"

    # DO NOT persist to environment (this was causing bleed-over)

    # --------------------------------------------------
    # Logging setup
    # --------------------------------------------------
    if args.log:

        os.makedirs("logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        ticker = args.ticker if args.ticker else ("BTC-USD" if args.crypto else "SPY")

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

    # --------------------------------------------------
    # Daemon mode
    # --------------------------------------------------

    # --------------------------------------------------
    # Research Daemon Mode
    # --------------------------------------------------
    if args.research_daemon:

        print("\n==============================")
        print("AI RESEARCH DAEMON ACTIVE")
        print("==============================")

        cycle = 0

        while True:

            cycle += 1

            print(f"\nRESEARCH CYCLE {cycle}")
            print("---------------------")

            try:
                run_research_pipeline(BOT_NAME, crypto_universe if args.crypto else None)




            except Exception as e:

                print("\n⚠ RESEARCH CYCLE ERROR")

                traceback.print_exc()

            if args.crypto:
                sleep_seconds = 600
            else:
                sleep_seconds = 900

            next_run = datetime.now() + timedelta(seconds=sleep_seconds)

            print(f"\nCycle {cycle} complete.")
            print(f"Next cycle at {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Sleeping {sleep_seconds // 60} minutes...\n")

            time.sleep(sleep_seconds)

            if args.daemon:



                print("\nDaemon mode active")
                print("Crypto mode:", args.crypto)
                print("Bot:", BOT_NAME)

                cycle = 0

            while True:

                cycle += 1

                try:

                    print("\n==============================")
                    print(f"AI TRADING CYCLE {cycle}")
                    print("==============================")

                    if args.crypto:

                        crypto_universe = load_crypto_watchlist()

                        if not crypto_universe:
                            crypto_universe = [
                                "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD",
                                "ADA-USD", "DOGE-USD", "AVAX-USD", "LINK-USD", "DOT-USD",
                                "LTC-USD", "ATOM-USD", "NEAR-USD", "FIL-USD", "ETC-USD",
                                "XLM-USD",
                            ]

                        run_live_simulation([], crypto_universe, BOT_NAME)

                    else:

                        universe = load_watchlist()
                        run_live_simulation(universe, [], BOT_NAME)

                except Exception as e:

                    print("\n⚠ DAEMON ERROR")
                    print(e)

                if args.crypto:
                    sleep_seconds = 600  # 10 minutes for crypto
                else:
                    sleep_seconds = 900  # 15 minutes for equities

                next_run = datetime.now() + timedelta(seconds=sleep_seconds)

                print(f"\nCycle {cycle} complete.")
                print(f"Next cycle at {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Sleeping {sleep_seconds // 60} minutes...\n")
                time.sleep(sleep_seconds)

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

    run_live_simulation(universe, crypto_universe, BOT_NAME)
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

    for sym in crypto_universe:

        try:
            df = get_recent_data(sym, months)

            if df is not None and len(df) > 0:
                symbol_data[sym] = df

        except Exception as e:
            print(f"Data error for {sym}: {e}")

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
        run_strategy_lab(
            argparse.Namespace(
                ticker=sym,
                window=6,
                top=10,
                report=False,
                crypto=args.crypto
            )
        )

    except Exception as e:
        print(f"Lab failed for {sym}: {e}")

data = get_recent_data(ticker, months)

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

if args.crypto:
    top_trades = rank_opportunities(signals)

    # FORCE minimum trade count for testing
    if len(top_trades) < 20:
        print("DEBUG: Not enough signals, expanding to full universe")
        top_trades = [(t, 1.0) for t in crypto_universe[:20]]

else:
    top_trades = rank_opportunities(signals)[:5]

print("\nAI PORTFOLIO MANAGER")
print("--------------------")

seen = set()

for t, score in top_trades:

    if t in seen:
        continue

    seen.add(t)

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

            sharpe_scores = []

            for symbol in EVOLUTION_TEST_UNIVERSE:

                try:

                    test_data = get_recent_data(symbol, 12)

                    if strat == "MA":
                        equity, final, *_ = run_backtest(
                            test_data,
                            lambda d: analyze_market(d, p1, p2)
                        )

                    elif strat == "MR":
                        equity, final, *_ = run_backtest(
                            test_data,
                            lambda d: mean_reversion_strategy(d, -p1 / 100)
                        )

                    elif strat == "VOL":
                        equity, final, *_ = run_backtest(
                            test_data,
                            volatility_breakout_strategy
                        )

                    sharpe_scores.append(calculate_sharpe(equity))

                except Exception:
                    continue

            if sharpe_scores:
                sharpe = sum(sharpe_scores) / len(sharpe_scores)
            else:
                sharpe = -999

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

league = run_strategy_darwinism(league)

# Keep only the best 500 strategies
league = sorted(league, key=lambda x: x["score"], reverse=True)[:500]

save_league(league)

# --------------------------------------------------
# Export best strategies for live trading bots
# --------------------------------------------------

try:

    top_strategies = [s for s in league if s["sharpe"] > 0][:10]

    export_data = []

    for s in top_strategies:
        export_data.append({
            "strategy": s["strategy"],
            "short": s.get("short"),
            "long": s.get("long"),
            "sharpe": s.get("sharpe")
        })

    bot_name = globals().get("BOT_NAME", "default_bot")

    with open(f"best_strategies_{bot_name}.json", "w") as f:

        json.dump(export_data, f, indent=2)

    print("\nExported best strategies to best_strategies.json")

except Exception as e:
    print("Strategy export failed:", e)

# Strategy Darwinism
# SURVIVAL_THRESHOLD = 0.1

# league = [s for s in league if s["score"] > SURVIVAL_THRESHOLD]

print("\nSTRATEGY EVOLUTION")
print("------------------")
print("Strategies surviving:", len(league))

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

if args.crypto:
    best_strategies = load_best_strategies("crypto_bot", 50) or []
else:
    best_strategies = load_best_strategies("equity_bot", 10) or []

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

print_strategy_performance(
    ma_equity, mr_equity, adaptive_equity,
    ma_final, mr_final, adaptive_final,
    ma_sharpe, mr_sharpe, adaptive_sharpe,
    ma_max_dd, mr_max_dd, adaptive_max_dd,
    ma_profits, mr_profits, ad_profits,
    vote_final, vote_sharpe,
    council_final, council_sharpe,
    bh_final, bh_sharpe, bh_max_dd,
    ticker,
    record_trade,
    log_trade,
    print_strategy_stats
)

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

generate_backtest_report(
    ticker,
    BOT_NAME,
    data,
    ma_equity,
    mr_equity,
    adaptive_equity,
    bh_equity,
    vote_equity,
    council_equity,
    ma_buys,
    ma_sells,
    mr_buys,
    mr_sells,
    ad_buys,
    ad_sells,
    ma_profits,
    mr_profits,
    ad_profits
)

# print("Displaying chart window...")

# plt.show()
