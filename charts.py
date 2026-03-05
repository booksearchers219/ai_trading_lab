import matplotlib.pyplot as plt

def save_heatmap(heatmap_array, heatmap_labels, args, timestamp):

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
        plt.savefig(f"reports/{timestamp}_heatmap.png", dpi=300)
    else:
        plt.show()

    plt.close()


def save_portfolio_chart(ma_portfolio, mr_portfolio, ad_portfolio, args, timestamp):

    plt.figure(figsize=(10,6))

    if len(ma_portfolio) > 0:
        plt.plot(ma_portfolio, label="MA Final Values", linewidth=3)

    if len(mr_portfolio) > 0:
        plt.plot(mr_portfolio, label="MR Final Values", linewidth=3)

    if len(ad_portfolio) > 0:
        plt.plot(ad_portfolio, label="Adaptive Final Values", linewidth=3)

    plt.title("Strategy Portfolio Performance (All Tickers)", fontsize=16, fontweight="bold")
    plt.xlabel("Ticker Number")
    plt.ylabel("Portfolio Value")

    plt.legend()
    plt.grid(True)

    if args.report:
        plt.savefig(f"reports/{timestamp}_portfolio.png", dpi=300)
    else:
        plt.show()

    plt.close()

    def save_strategy_dominance(ma_wins, mr_wins, ad_wins, args, timestamp):

        import matplotlib.pyplot as plt

        labels = ["Moving Average", "Mean Reversion", "Adaptive"]
        values = [ma_wins, mr_wins, ad_wins]
        colors = ["blue", "orange", "purple"]

        plt.figure(figsize=(8, 5))

        plt.bar(labels, values, color=colors)

        plt.title("Strategy Wins Across Market Scan", fontsize=15, fontweight="bold")
        plt.ylabel("Number of Tickers")
        plt.grid(axis="y", alpha=0.3)

        if args.report:
            plt.savefig(f"reports/{timestamp}_strategy_dominance.png", dpi=300)
        else:
            plt.show()

        plt.close()

def save_strategy_dominance(ma_wins, mr_wins, ad_wins, args, timestamp):

    import matplotlib.pyplot as plt

    labels = ["Moving Average", "Mean Reversion", "Adaptive"]
    values = [ma_wins, mr_wins, ad_wins]
    colors = ["blue", "orange", "purple"]

    plt.figure(figsize=(8,5))

    plt.bar(labels, values, color=colors)

    plt.title("Strategy Wins Across Market Scan", fontsize=15, fontweight="bold")
    plt.ylabel("Number of Tickers")
    plt.grid(axis="y", alpha=0.3)

    if args.report:
        plt.savefig(f"reports/{timestamp}_strategy_dominance.png", dpi=300)
    else:
        plt.show()

    plt.close()
