import os
import glob
import numpy as np
import matplotlib.pyplot as plt


def cleanup_reports(max_files=50):

    files = sorted(glob.glob("reports/*"), key=os.path.getmtime)

    if len(files) > max_files:
        for f in files[:-max_files]:
            os.remove(f)


def max_drawdown(drawdowns):
    return min(drawdowns)


def rolling_sharpe(equity_curve, window=20):

    sharpes = []

    for i in range(len(equity_curve)):

        if i < window:
            sharpes.append(0)
            continue

        segment = equity_curve[i-window:i]

        returns = np.diff(segment) / segment[:-1]

        mean = np.mean(returns)
        std = np.std(returns)

        if std == 0:
            sharpes.append(0)
        else:
            sharpes.append((mean / std) * np.sqrt(252))

    return sharpes


def plot_strategy_landscape(results):

    shorts = sorted(set(r[1] for r in results))
    longs = sorted(set(r[2] for r in results))

    heatmap = np.zeros((len(shorts), len(longs)))

    for strat, s, l, sharpe in results:

        i = shorts.index(s)
        j = longs.index(l)

        heatmap[i][j] = sharpe

    plt.figure(figsize=(10,6))

    plt.imshow(
        heatmap,
        aspect="auto",
        origin="lower",
        cmap="viridis"
    )

    plt.colorbar(label="Sharpe Ratio")

    plt.xticks(range(len(longs)), longs, rotation=90)
    plt.yticks(range(len(shorts)), shorts)

    plt.xlabel("Long MA")
    plt.ylabel("Short MA")
    plt.title("Moving Average Strategy Landscape")

    plt.tight_layout()
    plt.show()
