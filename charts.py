import matplotlib.pyplot as plt

def save_heatmap(heatmap_array, heatmap_labels, args, timestamp, report_dir):

    plt.figure(figsize=(8,10))
    plt.imshow(heatmap_array, cmap="coolwarm", aspect="auto")

    plt.yticks(range(len(heatmap_labels)), heatmap_labels)
    plt.xticks([0,1,2], ["MA","MR","AD"])

    plt.title("Strategy Winners Heatmap", fontsize=16, fontweight="bold")
    plt.xlabel("Strategy")
    plt.ylabel("Ticker")

    plt.colorbar(label="Winner")
    plt.tight_layout()

    if args.report:
        plt.savefig(f"{report_dir}/heatmap.png", dpi=300)
    else:
        plt.show()

    plt.close()


def save_portfolio_chart(ma_curve, mr_curve, ad_curve, args, timestamp, report_dir):

    plt.figure(figsize=(10,6))

    if ma_curve:
        plt.plot(ma_curve, label="MA Portfolio", linewidth=3)

    if mr_curve:
        plt.plot(mr_curve, label="MR Portfolio", linewidth=3)

    if ad_curve:
        plt.plot(ad_curve, label="Adaptive Portfolio", linewidth=3)

    plt.title("Strategy Portfolio Performance (All Tickers)", fontsize=16, fontweight="bold")
    plt.xlabel("Backtest Day")
    plt.ylabel("Portfolio Value")

    if plt.gca().lines:
        plt.legend()

    plt.grid(True)

    if args.report:
        plt.savefig(f"{report_dir}/portfolio.png", dpi=300)
    else:
        plt.show()

    plt.close()

def save_strategy_dominance(ma_wins, mr_wins, ad_wins, args, timestamp, report_dir):

    labels = ["Moving Average", "Mean Reversion", "Adaptive"]
    values = [ma_wins, mr_wins, ad_wins]
    colors = ["blue", "orange", "purple"]

    plt.figure(figsize=(8,5))

    plt.bar(labels, values, color=colors)

    plt.title("Strategy Wins Across Market Scan", fontsize=15, fontweight="bold")
    plt.ylabel("Number of Tickers")
    plt.grid(axis="y", alpha=0.3)

    if args.report:
        plt.savefig(f"{report_dir}/strategy_dominance.png", dpi=300)
    else:
        plt.show()

    plt.close()

def save_strategy_dominance(ma_wins, mr_wins, ad_wins, args, timestamp, report_dir):

    labels = ["Moving Average", "Mean Reversion", "Adaptive"]
    values = [ma_wins, mr_wins, ad_wins]
    colors = ["blue", "orange", "purple"]

    plt.figure(figsize=(8,5))

    plt.bar(labels, values, color=colors)

    plt.title("Strategy Wins Across Market Scan", fontsize=15, fontweight="bold")
    plt.ylabel("Number of Tickers")
    plt.grid(axis="y", alpha=0.3)

    if args.report:
        plt.savefig(f"{report_dir}/strategy_dominance.png", dpi=300)
    else:
        plt.show()

    plt.close()




def save_sharpe_leaderboard(results, args, timestamp, report_dir, top_n=20):

    import matplotlib.pyplot as plt

    # Sort by best Sharpe across strategies
    results_sorted = sorted(results, key=lambda x: max(x[5], x[6], x[7]), reverse=True)

    top = results_sorted[:top_n]

    labels = [r[0] for r in top]
    sharpes = [max(r[5], r[6], r[7]) for r in top]

    plt.figure(figsize=(10,6))

    plt.barh(labels, sharpes)

    plt.title("Top Strategy Sharpe Ratios", fontsize=16, fontweight="bold")
    plt.xlabel("Sharpe Ratio")
    plt.ylabel("Ticker")

    plt.gca().invert_yaxis()
    plt.grid(axis="x", alpha=0.3)

    if args.report:
        plt.savefig(f"{report_dir}/sharpe_leaderboard.png", dpi=300)
    else:
        plt.show()

    plt.close()

def save_regime_distribution(trend_count, side_count, args, timestamp, report_dir):

    import matplotlib.pyplot as plt

    labels = ["Trending", "Sideways"]
    values = [trend_count, side_count]
    colors = ["green", "gold"]

    plt.figure(figsize=(6,5))

    plt.bar(labels, values, color=colors)

    plt.title("Market Regime Distribution", fontsize=15, fontweight="bold")
    plt.ylabel("Number of Tickers")

    plt.grid(axis="y", alpha=0.3)

    if args.report:
        plt.savefig(f"{report_dir}/market_regimes.png", dpi=300)
    else:
        plt.show()

    plt.close()

def save_trade_opportunities(results, args, timestamp, report_dir, top_n=10):

    import csv

    # determine best strategy per ticker
    ranked = []

    for r in results:

        ticker = r[0]
        ma_sharpe = r[5]
        mr_sharpe = r[6]
        ad_sharpe = r[7]

        best_sharpe = max(ma_sharpe, mr_sharpe, ad_sharpe)

        if best_sharpe == ma_sharpe:
            strategy = "MA"
        elif best_sharpe == mr_sharpe:
            strategy = "MR"
        else:
            strategy = "Adaptive"

        ranked.append((ticker, strategy, best_sharpe))

    ranked.sort(key=lambda x: x[2], reverse=True)

    top = ranked[:top_n]

    print("\nTop Trade Opportunities\n")

    for t in top:
        print(f"{t[0]:<6} | {t[1]:<8} | Sharpe {t[2]:.2f}")

    if args.report:

        file = f"{report_dir}/trade_opportunities.csv"

        with open(file, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["Ticker", "Strategy", "Sharpe"])

            for row in top:
                writer.writerow(row)