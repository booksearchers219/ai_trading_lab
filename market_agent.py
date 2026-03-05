import matplotlib.ticker as mtick
import csv
from data_utils import *
from strategies import *
from backtest_utils import *
from visualization import *
import argparse
import multiprocessing as mp
import os
from charts import save_heatmap, save_portfolio_chart, save_strategy_dominance, save_sharpe_leaderboard, save_regime_distribution, save_trade_opportunities
from datetime import datetime



plt.style.use("ggplot")

def max_drawdown(drawdowns):
    return min(drawdowns)

def rolling_sharpe(equity_curve, window=20):

    sharpes = []

    for i in range(len(equity_curve)):

        if i < window:
            sharpes.append(0)
            continue

        segment = equity_curve[i-window:i]

        returns = [
            (segment[j] - segment[j-1]) / segment[j-1]
            for j in range(1, len(segment))
        ]

        mean = np.mean(returns)
        std = np.std(returns)

        if std == 0:
            sharpes.append(0)
        else:
            sharpes.append((mean/std) * np.sqrt(252))

    return sharpes

def process_ticker(args):

    ticker, months = args

    data = get_recent_data(ticker, months)

    regime = detect_regime(data)



    ma_equity, ma_final, _, _, _ = run_backtest(data, analyze_market)
    mr_equity, mr_final, _, _, _ = run_backtest(data, mean_reversion_strategy)
    ad_equity, ad_final, _, _, _ = run_backtest(data, adaptive_strategy)

    ma_sharpe = calculate_sharpe(ma_equity)
    mr_sharpe = calculate_sharpe(mr_equity)
    ad_sharpe = calculate_sharpe(ad_equity)

    return (
        ticker,
        regime,
        ma_final,
        mr_final,
        ad_final,
        ma_sharpe,
        mr_sharpe,
        ad_sharpe,
        ma_equity,
        mr_equity,
        ad_equity
    )


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

    parser.add_argument("--top", type=int, help="Show top N strategies by Sharpe")

    parser.add_argument("--parallel", action="store_true",
                        help="Run multi-ticker scan in parallel")
    parser.add_argument("--sweep", action="store_true",
                        help="Run moving average parameter sweep")
    parser.add_argument("--report", action="store_true",
                        help="Save scan results and charts to reports folder")

    args = parser.parse_args()

    if args.scan == "sp500":

        all_tickers = get_sp500_tickers()

        if args.limit:
            ticker_list = all_tickers[:args.limit]
        else:
            ticker_list = all_tickers

    ticker = args.ticker.upper()

    months = args.window

    ticker = args.ticker.upper()

    batch_mode = "y" if args.scan else "n"

    if batch_mode == "y":

        if args.report:
            os.makedirs("reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        results = []
        heatmap_data = []
        heatmap_labels = []

        ma_portfolio = []
        mr_portfolio = []
        ad_portfolio = []

        ma_portfolio_curve = None
        mr_portfolio_curve = None
        ad_portfolio_curve = None

        # Leaderboard counters
        ma_wins = 0
        mr_wins = 0
        ad_wins = 0

        trend_counts = {"MA": 0, "MR": 0, "AD": 0}
        side_counts = {"MA": 0, "MR": 0, "AD": 0}

        trend_total = 0
        side_total = 0

        if args.parallel:

            print("\nRunning parallel scan...\n")

            pool = mp.Pool(mp.cpu_count())

            job_args = [(ticker, months) for ticker in ticker_list]

            results = pool.map(process_ticker, job_args)

            for r in results:

                regime = r[1]

                if regime == "TRENDING":
                    trend_total += 1
                else:
                    side_total += 1

                ma_portfolio.append(r[2])
                mr_portfolio.append(r[3])
                ad_portfolio.append(r[4])

                ma_equity = r[8]
                mr_equity = r[9]
                ad_equity = r[10]

                if ma_portfolio_curve is None:
                    ma_portfolio_curve = ma_equity
                    mr_portfolio_curve = mr_equity
                    ad_portfolio_curve = ad_equity
                else:
                    ma_portfolio_curve = [a + b for a, b in zip(ma_portfolio_curve, ma_equity)]
                    mr_portfolio_curve = [a + b for a, b in zip(mr_portfolio_curve, mr_equity)]
                    ad_portfolio_curve = [a + b for a, b in zip(ad_portfolio_curve, ad_equity)]

            pool.close()
            pool.join()

        else:

            for i, ticker in enumerate(ticker_list, 1):
                print(f"\nTesting {ticker} ({i}/{len(ticker_list)})")

                data = get_recent_data(ticker, months)

                regime = detect_regime(data)

                if regime == "TRENDING":
                    trend_total += 1
                else:
                    side_total += 1

                ma_equity, ma_final, _, _, _ = run_backtest(data, analyze_market)
                mr_equity, mr_final, _, _, _ = run_backtest(data, mean_reversion_strategy)
                ad_equity, ad_final, _, _, _ = run_backtest(data, adaptive_strategy)

                ma_sharpe = calculate_sharpe(ma_equity)
                mr_sharpe = calculate_sharpe(mr_equity)
                ad_sharpe = calculate_sharpe(ad_equity)

                results.append((ticker, regime, ma_final, mr_final, ad_final, ma_sharpe, mr_sharpe, ad_sharpe))

                if regime == "TRENDING":
                    trend_total += 1
                else:
                    side_total += 1

                if ma_portfolio_curve is None:
                    ma_portfolio_curve = ma_equity
                    mr_portfolio_curve = mr_equity
                    ad_portfolio_curve = ad_equity
                else:
                    ma_portfolio_curve = [a + b for a, b in zip(ma_portfolio_curve, ma_equity)]
                    mr_portfolio_curve = [a + b for a, b in zip(mr_portfolio_curve, mr_equity)]
                    ad_portfolio_curve = [a + b for a, b in zip(ad_portfolio_curve, ad_equity)]

                ma_portfolio.append(ma_final)
                mr_portfolio.append(mr_final)
                ad_portfolio.append(ad_final)

        # Save results to CSV
        csv_file = "strategy_results.csv"

        if args.report:
            csv_file = f"reports/{timestamp}_scan_results.csv"

        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Ticker",
                "MA_Final",
                "MR_Final",
                "AD_Final",
                "MA_Sharpe",
                "MR_Sharpe",
                "AD_Sharpe"
            ])

            for row in results:
                writer.writerow(row)

        print("\nResults saved to strategy_results.csv\n")

        # Sort results by best Sharpe ratio
        results.sort(key=lambda x: max(x[5], x[6], x[7]), reverse=True)

        top_n = args.top if args.top else 20
        top_results = results[:top_n]

        print("\nStrategy Results Summary\n")

        for r in top_results:

            best_value = max(r[2], r[3], r[4])

            if best_value == r[2]:
                winner = "MA"
                ma_wins += 1
            elif best_value == r[3]:
                winner = "MR"
                mr_wins += 1
            else:
                winner = "AD"
                ad_wins += 1

            regime = r[1]

            if regime == "TRENDING":
                trend_counts[winner] += 1
            else:
                side_counts[winner] += 1

            row = [0, 0, 0]

            if winner == "MA":
                row[0] = 1
            elif winner == "MR":
                row[1] = 1
            else:
                row[2] = 1

            heatmap_data.append(row)
            heatmap_labels.append(r[0])

            print(
                f"{r[0]:<5} | "
                f"{r[1]:<8} | "
                f"MA: {'$' + format(r[2], ',.2f'):>12} "
                f"MR: {'$' + format(r[3], ',.2f'):>12} "
                f"AD: {'$' + format(r[4], ',.2f'):>12} "
                f"| Winner: {winner}"
            )

        print("\nStrategy Leaderboard\n")

        print(f"{'Moving Average':<18}: {ma_wins}")
        print(f"{'Mean Reversion':<18}: {mr_wins}")
        print(f"{'Adaptive':<18}: {ad_wins}")

        save_strategy_dominance(ma_wins, mr_wins, ad_wins, args, timestamp)

        print("\nRegime Performance\n")

        print("TRENDING markets")
        print("MA wins:", trend_counts["MA"])
        print("MR wins:", trend_counts["MR"])
        print("AD wins:", trend_counts["AD"])

        print("\nSIDEWAYS markets")
        print("MA wins:", side_counts["MA"])
        print("MR wins:", side_counts["MR"])
        print("AD wins:", side_counts["AD"])

        print("\nTop Moving Average Strategies\n")

        print("\nPortfolio Performance Across All Tickers\n")

        print("MA total :", f"${sum(ma_portfolio):,.2f}")
        print("MR total :", f"${sum(mr_portfolio):,.2f}")
        print("AD total :", f"${sum(ad_portfolio):,.2f}")

        ma_rank = sorted(results, key=lambda x: x[5], reverse=True)[:10]

        for r in ma_rank:
            print(f"{r[0]:<6} Sharpe: {r[5]:>5.2f}")

        print("\nTop Mean Reversion Strategies\n")

        mr_rank = sorted(results, key=lambda x: x[6], reverse=True)[:10]

        for r in mr_rank:
            print(f"{r[0]:<6} Sharpe: {r[6]:>5.2f}")

        print("\nTop Adaptive Strategies\n")

        ad_rank = sorted(results, key=lambda x: x[7], reverse=True)[:10]

        for r in ad_rank:
            print(f"{r[0]:<6} Sharpe: {r[7]:>5.2f}")

        print("\nStrategy Stability Score\n")

        ma_sharpes = [r[5] for r in results]
        mr_sharpes = [r[6] for r in results]
        ad_sharpes = [r[7] for r in results]

        ma_mean = np.mean(ma_sharpes)
        mr_mean = np.mean(mr_sharpes)
        ad_mean = np.mean(ad_sharpes)

        ma_std = np.std(ma_sharpes)
        mr_std = np.std(mr_sharpes)
        ad_std = np.std(ad_sharpes)

        print(f"MA stability : {(ma_mean / ma_std) if ma_std else 0:.2f}")
        print(f"MR stability : {(mr_mean / mr_std) if mr_std else 0:.2f}")
        print(f"AD stability : {(ad_mean / ad_std) if ad_std else 0:.2f}")

        top_n = args.top if args.top else 20

        print("TRENDING markets")
        print("MA wins:", trend_counts["MA"])
        print("MR wins:", trend_counts["MR"])
        print("AD wins:", trend_counts["AD"])

        print("\nSIDEWAYS markets")
        print("MA wins:", side_counts["MA"])
        print("MR wins:", side_counts["MR"])
        print("AD wins:", side_counts["AD"])

        heatmap_array = np.array(heatmap_data[:top_n])
        heatmap_labels = heatmap_labels[:top_n]

        print("Curve lengths:",
              len(ma_portfolio_curve) if ma_portfolio_curve else 0,
              len(mr_portfolio_curve) if mr_portfolio_curve else 0,
              len(ad_portfolio_curve) if ad_portfolio_curve else 0)

        print("Regime totals:", trend_total, side_total)

        save_heatmap(heatmap_array, heatmap_labels, args, timestamp)

        save_strategy_dominance(ma_wins, mr_wins, ad_wins, args, timestamp)

        save_sharpe_leaderboard(results, args, timestamp)

        save_regime_distribution(trend_total, side_total, args, timestamp)

        save_trade_opportunities(results, args, timestamp)


    ticker = args.ticker.upper()

    data = get_recent_data(ticker, months)

    print(f"\nRunning Strategy Comparison on {ticker}\n")

    # Run strategies
    ma_equity, ma_final, ma_buys, ma_sells, ma_profits = run_backtest(data, analyze_market)
    mr_equity, mr_final, mr_buys, mr_sells, mr_profits = run_backtest(data, mean_reversion_strategy)
    adaptive_equity, adaptive_final, ad_buys, ad_sells, ad_profits = run_backtest(data, adaptive_strategy)

    ma_sharpe = calculate_sharpe(ma_equity)
    mr_sharpe = calculate_sharpe(mr_equity)
    adaptive_sharpe = calculate_sharpe(adaptive_equity)

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

            regime = r[1]

            if regime == "TRENDING":
                trend_total += 1
            else:
                side_total += 1

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

    print("\nMean Reversion")
    print("Trades:", len(mr_profits))
    print("Win Rate:", round(mr_wr * 100, 1), "%")
    print("Avg Trade:", round(mr_avg, 2))
    print("Profit Factor:", round(mr_pf, 2))

    print("\nAdaptive")
    print("Trades:", len(ad_profits))
    print("Win Rate:", round(ad_wr * 100, 1), "%")
    print("Avg Trade:", round(ad_avg, 2))
    print("Profit Factor:", round(ad_pf, 2))

    print("\nBuy & Hold Final Value:", round(bh_final, 2))
    print("Buy & Hold Sharpe:", round(bh_sharpe, 2))
    print("Buy & Hold Max Drawdown:", round(bh_max_dd * 100, 2), "%")

   # print("\nTrade Statistics")

    print("\nMoving Average")
    print("Trades:", len(ma_profits))
    print("Win Rate:", round(ma_wr * 100, 1), "%")
    print("Avg Trade:", round(ma_avg, 2))

    print("\nMean Reversion")
    print("Trades:", len(mr_profits))
    print("Win Rate:", round(mr_wr * 100, 1), "%")
    print("Avg Trade:", round(mr_avg, 2))

    print("\nAdaptive")
    print("Trades:", len(ad_profits))
    print("Win Rate:", round(ad_wr * 100, 1), "%")
    print("Avg Trade:", round(ad_avg, 2))

    # Plot
    fig, (ax0, ax1, ax2, ax3, ax4, ax5) = plt.subplots(6, 1, figsize=(10, 16), sharex=False)

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

    ax0.set_title(f"{ticker} Price", fontsize=15, fontweight="bold")
    ax0.legend(fontsize=12)
    ax0.grid(True)

    ax1.plot(ma_equity, label="Moving Average", linewidth=3)
    ax1.plot(mr_equity, label="Mean Reversion", linewidth=3, linestyle="--")
    ax1.plot(adaptive_equity, label="Adaptive", linewidth=3)
    ax1.plot(bh_equity, label="Buy & Hold", linewidth=3)

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

    ax1.set_title(f"{ticker} Strategy Comparison", fontsize=16, fontweight="bold")
    ax1.legend(fontsize=12)
    ax1.grid(True)
    ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    ax2.plot(ma_drawdown, label="MA Drawdown", linewidth=3, color="blue")
    ax2.plot(mr_drawdown, label="MR Drawdown", linewidth=3, color="red", linestyle="--")
    ax2.plot(adaptive_drawdown, label="Adaptive Drawdown", linewidth=3, color="purple")
    ax2.plot(bh_drawdown, label="Buy & Hold Drawdown", linewidth=3, color="green")

    ax2.axhline(y=0, color="black", linewidth=2, linestyle="--", alpha=0.5)

    ax2.set_title("Drawdown", fontsize=15, fontweight="bold")
    ax2.legend(fontsize=12)
    ax2.grid(True)

    # Trade Profit Distribution
    ax3.hist(ma_profits, bins=20, alpha=0.6, label="MA")
    ax3.hist(mr_profits, bins=20, alpha=0.6, label="MR")
    ax3.hist(ad_profits, bins=20, alpha=0.6, label="Adaptive")

    ax3.set_title("Trade Profit Distribution", fontsize=15, fontweight="bold")
    ax3.set_xlabel("Profit per Trade")
    ax3.set_ylabel("Number of Trades")

    ax3.legend(fontsize=12)
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

    ax4.set_title("Win/Loss Trade Count", fontsize=15, fontweight="bold")
    ax4.set_ylabel("Number of Trades")
    ax4.grid(True)

    # Rolling Sharpe Ratio
    ax5.plot(ma_roll, label="MA Sharpe", linewidth=2)
    ax5.plot(mr_roll, label="MR Sharpe", linewidth=2)
    ax5.plot(ad_roll, label="Adaptive Sharpe", linewidth=2)

    ax5.axhline(y=0, color="black", linestyle="--", linewidth=1)

    ax5.set_title("Rolling Sharpe Ratio", fontsize=15, fontweight="bold")
    ax5.set_ylabel("Sharpe")
    ax5.set_xlabel("Backtest Days")

    ax5.legend(fontsize=11)
    ax5.grid(True)

    # Strategy returns for correlation
    ma_returns = np.diff(ma_equity) / ma_equity[:-1]
    mr_returns = np.diff(mr_equity) / mr_equity[:-1]
    ad_returns = np.diff(adaptive_equity) / adaptive_equity[:-1]

    corr_matrix = np.corrcoef([
        ma_returns,
        mr_returns,
        ad_returns
    ])

    save_heatmap(heatmap_array, heatmap_labels, args, timestamp)

    save_portfolio_chart(ma_portfolio_curve, mr_portfolio_curve, ad_portfolio_curve, args, timestamp)