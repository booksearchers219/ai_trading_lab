import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from analysis.market_analysis import regime_history

def safe_points(points, series):
    x = []
    y = []
    for p in points:
        if 0 <= p < len(series):
            x.append(p)
            y.append(series[p])
    return x, y


def compute_drawdown(equity):
    equity = np.array(equity)
    peak = np.maximum.accumulate(equity)
    return (equity - peak) / peak


def rolling_sharpe(equity, window=30):
    equity = np.array(equity)

    if len(equity) < 2:
        return [0]

    returns = np.diff(equity) / equity[:-1]
    sharpe = []

    for i in range(len(returns)):
        r = returns[max(0, i - window): i + 1]

        if len(r) < 2 or np.std(r) == 0:
            sharpe.append(0)
        else:
            sharpe.append(np.mean(r) / np.std(r) * np.sqrt(252))

    return sharpe


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

    print(f"\nGenerating chart for: {ticker}")

    # --- Compute metrics ---
    ma_drawdown = compute_drawdown(ma_equity)
    mr_drawdown = compute_drawdown(mr_equity)
    adaptive_drawdown = compute_drawdown(adaptive_equity)
    bh_drawdown = compute_drawdown(bh_equity)

    ma_roll = rolling_sharpe(ma_equity)
    mr_roll = rolling_sharpe(mr_equity)
    ad_roll = rolling_sharpe(adaptive_equity)

    price_series = data["Close"].reset_index(drop=True)

    # --- Create 6 chart panels ---
    fig, (ax0, ax1, ax2, ax3, ax4, ax5) = plt.subplots(
        6, 1, figsize=(16, 20), sharex=False
    )

    # --------------------------------------------------
    # 1️⃣ Price + Trades
    # --------------------------------------------------
    ax0.plot(price_series, color="black", linewidth=2, label="Price")

    # --- Market regime shading ---
    regimes = regime_history(data)

    limit = min(len(price_series) - 1, len(regimes))

    for i in range(limit):

        if regimes[i] == "TRENDING":
            ax0.axvspan(i, i + 1, color="green", alpha=0.08)
        else:
            ax0.axvspan(i, i + 1, color="yellow", alpha=0.08)

    x, y = safe_points(ma_buys, price_series)

    for i, (bx, by) in enumerate(zip(x, y), start=1):
        ax0.scatter(bx, by, marker="^", color="lime", s=140)

        ax0.text(
            bx,
            by + 1,
            str(i),
            fontsize=11,
            fontweight="bold",
            ha="center"
        )

    x, y = safe_points(ma_sells, price_series)

    for i, (sx, sy) in enumerate(zip(x, y), start=1):

        if i - 1 < len(ma_profits) and ma_profits[i - 1] > 0:
            color = "lime"
        else:
            color = "red"

        ax0.scatter(sx, sy, marker="v", color=color, s=140)

        ax0.text(
            sx,
            sy - 1,
            str(i),
            fontsize=11,
            fontweight="bold",
            ha="center"
        )

    x, y = safe_points(mr_buys, price_series)
    ax0.scatter(x, y, marker="^", color="orange", s=80)

    x, y = safe_points(mr_sells, price_series)
    ax0.scatter(x, y, marker="v", color="darkorange", s=80)

    x, y = safe_points(ad_buys, price_series)
    ax0.scatter(x, y, marker="^", color="purple", s=80)

    x, y = safe_points(ad_sells, price_series)
    ax0.scatter(x, y, marker="v", color="magenta", s=80)

    ax0.set_title(f"{ticker} Price", fontsize=15, fontweight="bold", loc="left")

    ax0.text(
        0.01,
        0.95,
        "BUY confidence: green=strong  yellow=medium  blue=weak",
        transform=ax0.transAxes,
        fontsize=9
    )

    ax0.grid(True)
    ax0.legend(loc="upper left")

    # --------------------------------------------------
    # 2️⃣ Equity Curves
    # --------------------------------------------------
    regimes = regime_history(data)

    limit = min(len(ma_equity) - 1, len(regimes))

    for i in range(limit):

        if regimes[i] == "TRENDING":
            color = "green"
        else:
            color = "gold"

        if i == 0:
            ax1.plot(
                [i, i + 1],
                [ma_equity[i], ma_equity[i + 1]],
                color=color,
                linewidth=3,
                label="MA"
            )
        else:
            ax1.plot(
                [i, i + 1],
                [ma_equity[i], ma_equity[i + 1]],
                color=color,
                linewidth=3
            )
    ax1.plot(ma_equity, color="black", linewidth=1, alpha=0.3)
    ax1.plot(mr_equity, label="MR", linewidth=2)
    ax1.plot(adaptive_equity, label="Adaptive", linewidth=2)
    ax1.plot(bh_equity, label="Buy & Hold", linewidth=2)
    ax1.plot(vote_equity, label="Voting", linewidth=2)
    ax1.plot(council_equity, label="Council", linewidth=2)

    ax1.axhline(y=10000, linestyle="--", color="black")

    ma_final = ma_equity[-1] if len(ma_equity) else 0
    mr_final = mr_equity[-1] if len(mr_equity) else 0
    ad_final = adaptive_equity[-1] if len(adaptive_equity) else 0
    bh_final = bh_equity[-1] if len(bh_equity) else 0

    ax1.set_title(
        f"{ticker} Strategy Equity | "
        f"MA ${ma_final:,.0f}  "
        f"MR ${mr_final:,.0f}  "
        f"AD ${ad_final:,.0f}  "
        f"BH ${bh_final:,.0f}",
        fontsize=16,
        fontweight="bold",
        loc="left"
    )
    ax1.legend()
    ax1.grid(True)
    ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    # --------------------------------------------------
    # 3️⃣ Drawdown
    # --------------------------------------------------
    ax2.plot(ma_drawdown, label="MA")
    ax2.plot(mr_drawdown, label="MR")
    ax2.plot(adaptive_drawdown, label="Adaptive")
    ax2.plot(bh_drawdown, label="Buy & Hold")

    ax2.axhline(0, linestyle="--", color="black")

    ax2.set_title("Drawdown", fontsize=15, fontweight="bold", loc="left")
    ax2.legend()
    ax2.grid(True)

    # --------------------------------------------------
    # 4️⃣ Trade Profit Distribution
    # --------------------------------------------------
    ax3.hist(ma_profits, bins=20, alpha=0.6, label="MA")
    ax3.hist(mr_profits, bins=20, alpha=0.6, label="MR")
    ax3.hist(ad_profits, bins=20, alpha=0.6, label="Adaptive")

    ax3.set_title("Trade Profit Distribution", fontsize=15, fontweight="bold", loc="left")
    ax3.legend()
    ax3.grid(True)

    # --------------------------------------------------
    # 5️⃣ Win / Loss Count
    # --------------------------------------------------
    ma_wins = sum(p > 0 for p in ma_profits)
    ma_losses = sum(p <= 0 for p in ma_profits)

    mr_wins = sum(p > 0 for p in mr_profits)
    mr_losses = sum(p <= 0 for p in mr_profits)

    ad_wins = sum(p > 0 for p in ad_profits)
    ad_losses = sum(p <= 0 for p in ad_profits)

    labels = ["MA W", "MA L", "MR W", "MR L", "AD W", "AD L"]
    values = [ma_wins, ma_losses, mr_wins, mr_losses, ad_wins, ad_losses]

    ax4.bar(labels, values)

    ax4.set_title("Win / Loss Trade Count", fontsize=15, fontweight="bold", loc="left")
    ax4.grid(True)

    # --------------------------------------------------
    # 6️⃣ Rolling Sharpe
    # --------------------------------------------------
    ax5.plot(ma_roll, label="MA")
    ax5.plot(mr_roll, label="MR")
    ax5.plot(ad_roll, label="Adaptive")

    ax5.axhline(0, linestyle="--", color="black")

    ax5.set_title("Rolling Sharpe Ratio", fontsize=15, fontweight="bold", loc="left")
    ax5.legend()
    ax5.grid(True)

    # --------------------------------------------------
    # Save chart
    # --------------------------------------------------
    plt.tight_layout()

    filename = f"chart_{ticker}_{BOT_NAME}.png"

    plt.savefig(filename)

    print("Saved:", filename)