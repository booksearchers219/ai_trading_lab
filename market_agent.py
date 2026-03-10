import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import yfinance as yf

from backtest_utils import *
from data_utils import *
from engine.evolve_engine import run_evolution_search
from engine.lab_engine import run_strategy_lab
from engine.scan_engine import run_scan_and_report
from live_trading import run_live_simulation
from strategies import *
from utils.reporting import max_drawdown, rolling_sharpe
from utils.strategy_loader import load_best_strategies
from visualization import *
from portfolio_state import save_state, load_state
from signal_engine import generate_signals
from risk_manager import calculate_position_size
from dashboard import print_market, print_signals
from trend_panel import print_trend_panel, print_market_breadth


def get_live_price(ticker):
    data = yf.Ticker(ticker)

    price = data.history(period="1d", interval="1m")["Close"].iloc[-1]

    return float(price)

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
            adaptive_strategy(df)
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


def print_strategy_confidence(symbol_data):

    buy_votes = 0
    sell_votes = 0
    hold_votes = 0

    for symbol, df in symbol_data.items():

        if len(df) < 20:
            continue

        vote_ma = analyze_market(df)
        vote_mr = mean_reversion_strategy(df)
        vote_ad = adaptive_strategy(df)

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

    print(f"BUY confidence  {'█'*bar}{'░'*(10-bar)} {buy_pct*100:.0f}%")
    print(f"SELL pressure   {sell_pct*100:.0f}%")




def print_momentum_leaders(data):

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

        print(f"{sym:<6} {pct*100:+.2f}%")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="AI Trading Lab")

    parser.add_argument("--ticker", type=str, default="TSLA",
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

    # parser.add_argument("--discover", action="store_true",
    #                   help="Run automatic strategy discovery")

    parser.add_argument("--evolve", action="store_true",
                        help="Run evolutionary strategy search")

    parser.add_argument("--lab", action="store_true",
                        help="Run full strategy research lab")

    parser.add_argument("--autotrade", action="store_true",
                        help="Run top discovered strategies")

    parser.add_argument("--debug-votes", action="store_true",
                        help="Print strategy votes during backtest")

    args = parser.parse_args()

    if args.live:
        run_live_simulation()
        exit()

    ticker = args.ticker.upper()
    months = args.window

    if args.scan:
        run_scan_and_report(args)
        exit()

    if args.lab:
        run_strategy_lab(args)
        exit()

    if args.evolve:
        run_evolution_search(args)
        exit()

    data = get_recent_data(ticker, months)

    # Trend panel data
    spy_data = get_recent_data("SPY", 1)
    nvda_data = get_recent_data("NVDA", 1)
    amd_data = get_recent_data("AMD", 1)
    tsla_data = get_recent_data("TSLA", 1)
    meta_data = get_recent_data("META", 1)

    symbol_data = {
        "SPY": spy_data,
        "NVDA": nvda_data,
        "AMD": amd_data,
        "TSLA": tsla_data,
        "META": meta_data
    }

    print(f"\nRunning Strategy Comparison on {ticker}\n")
    print("=" * 70)

    print_trend_panel(symbol_data)
    print_market_breadth(symbol_data)
    print_market_regime(data)
    print_market_sentiment(symbol_data)
    print_momentum_leaders(symbol_data)
    print_strategy_confidence(symbol_data)
    print_strategy_agreement(symbol_data)

    sectors = compute_sector_strength(symbol_data)

    print("-" * 70)
    print("\nSECTOR FLOW")
    print("-----------")

    for sector, (label, pct) in sorted(sectors.items()):
        pct_str = f"{pct * 100:+.2f}%"

        print(f"{sector:<7} {label:<10} {pct_str}")


    # Run strategies
    ma_equity, ma_final, ma_buys, ma_sells, ma_profits = run_backtest(data, analyze_market)
    mr_equity, mr_final, mr_buys, mr_sells, mr_profits = run_backtest(data, mean_reversion_strategy)
    adaptive_equity, adaptive_final, ad_buys, ad_sells, ad_profits = run_backtest(data, adaptive_strategy)

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

    council_equity, council_final, council_buys, council_sells, council_profits = run_backtest(
        data,
        lambda d: council_strategy(d, council_state)
    )

    council_sharpe = calculate_sharpe(council_equity)

    ma_sharpe = calculate_sharpe(ma_equity)
    mr_sharpe = calculate_sharpe(mr_equity)
    adaptive_sharpe = calculate_sharpe(adaptive_equity)
    vote_sharpe = calculate_sharpe(vote_equity)

    # Buy & Hold
    first_price = data["Close"].iloc[0]
    last_price = data["Close"].iloc[-1]

    bh_shares = 10000 / first_price
    bh_final = bh_shares * last_price

    bh_equity = []
    for i in range(50, len(data)):
        price = data["Close"].iloc[i]
        bh_equity.append(bh_shares * price)

    bh_sharpe = calculate_sharpe(bh_equity)

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
    bh_max_dd = max_drawdown(bh_drawdown)

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
    for i in range(len(regimes) - 1):

        if regimes[i] == "TRENDING":
            ax0.axvspan(i, i + 1, color="green", alpha=0.08)

        else:
            ax0.axvspan(i, i + 1, color="yellow", alpha=0.08)

    # Moving Average trades
    x, y = safe_points(ma_buys, price_series)
    ax0.scatter(x, y, marker="^", color="green", s=80)

    x, y = safe_points(ma_sells, price_series)
    ax0.scatter(x, y, marker="v", color="red", s=80)

    # Mean Reversion trades
    x, y = safe_points(mr_buys, price_series)
    ax0.scatter(x, y, marker="^", color="orange", s=80)

    x, y = safe_points(mr_sells, price_series)
    ax0.scatter(x, y, marker="v", color="darkorange", s=80)

    # Adaptive trades
    x, y = safe_points(ad_buys, price_series)
    ax0.scatter(x, y, marker="^", color="purple", s=80)

    x, y = safe_points(ad_sells, price_series)
    ax0.scatter(x, y, marker="v", color="magenta", s=80)

    ax0.set_title(f"{ticker} Price", fontsize=15, fontweight="bold", loc="left")
    ax0.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax0.grid(True)

    ax1.plot(ma_equity, label="Moving Average", linewidth=3)
    ax1.plot(mr_equity, label="Mean Reversion", linewidth=3, linestyle="--")
    ax1.plot(adaptive_equity, label="Adaptive", linewidth=3)
    ax1.plot(bh_equity, label="Buy & Hold", linewidth=3)
    ax1.plot(vote_equity, label="Voting Strategy", linewidth=3)
    ax1.plot(council_equity, label="Strategy Council", linewidth=3)

    ax1.axhline(y=10000, linestyle="--", color="black")

    # Moving Average trades
    x, y = safe_points(ma_buys, ma_equity)
    ax1.scatter(x, y, marker="^", color="green", s=80)

    x, y = safe_points(ma_sells, ma_equity)
    ax1.scatter(x, y, marker="v", color="red", s=80)

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

    ax1.set_title(f"{ticker} Strategy Comparison", fontsize=16, fontweight="bold", loc="left")
    ax1.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax1.grid(True)
    ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    ax2.plot(ma_drawdown, label="MA Drawdown", linewidth=3, color="blue")
    ax2.plot(mr_drawdown, label="MR Drawdown", linewidth=3, color="red", linestyle="--")
    ax2.plot(adaptive_drawdown, label="Adaptive Drawdown", linewidth=3, color="purple")
    ax2.plot(bh_drawdown, label="Buy & Hold Drawdown", linewidth=3, color="green")

    ax2.axhline(y=0, color="black", linewidth=2, linestyle="--", alpha=0.5)

    ax2.set_title("Drawdown", fontsize=15, fontweight="bold", loc="left")
    ax2.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax2.grid(True)

    # Trade Profit Distribution
    ax3.hist(ma_profits, bins=20, alpha=0.6, label="MA")
    ax3.hist(mr_profits, bins=20, alpha=0.6, label="MR")
    ax3.hist(ad_profits, bins=20, alpha=0.6, label="Adaptive")

    ax3.set_title("Trade Profit Distribution", fontsize=15, fontweight="bold", loc="left")
    ax3.set_xlabel("Profit per Trade")
    ax3.set_ylabel("Number of Trades")

    ax3.legend(loc="upper left", bbox_to_anchor=(1, 1))
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

    ax5.legend(loc="upper left", bbox_to_anchor=(1, 1))
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

    plt.tight_layout()
    plt.show()
