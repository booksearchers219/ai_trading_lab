import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os


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

    fig, ax = plt.subplots(figsize=(12,6))

    ax.plot(ma_equity, label="MA")
    ax.plot(mr_equity, label="MR")
    ax.plot(adaptive_equity, label="Adaptive")
    ax.plot(bh_equity, label="BuyHold")
    ax.plot(vote_equity, label="Vote")
    ax.plot(council_equity, label="Council")

    ax.legend()
    ax.grid(True)

    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    filename = f"chart_{ticker}_{BOT_NAME}.png"

    plt.tight_layout()
    plt.savefig(filename)

    print("\nReport saved:")
    print(" ", os.path.abspath(filename))
