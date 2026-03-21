


def generate_backtest_report(
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
):
    # paste plotting code here
















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

    ma_final_val = ma_equity[-1] if ma_equity else 0
    mr_final_val = mr_equity[-1] if mr_equity else 0
    ad_final_val = adaptive_equity[-1] if adaptive_equity else 0
    vote_final_val = vote_equity[-1] if vote_equity else 0
    council_final_val = council_equity[-1] if council_equity else 0
    bh_final_val = bh_equity[-1] if bh_equity else 0

    ax1.set_title(
        f"{ticker} Equity Curves | "
        f"MA ${ma_final_val:,.0f}  "
        f"MR ${mr_final_val:,.0f}  "
        f"AD ${ad_final_val:,.0f}  "
        f"Vote ${vote_final_val:,.0f}  "
        f"Council ${council_final_val:,.0f}  "
        f"BH ${bh_final_val:,.0f}",
        fontsize=16,
        fontweight="bold",
        loc="left"
    )

    ax1.legend(loc="upper left")
    ax1.grid(True)
    ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    ax1.set_ylabel("Portfolio Value ($)")

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

    filename = f"chart_{ticker}_{BOT_NAME}.png"

    plt.savefig(filename)

