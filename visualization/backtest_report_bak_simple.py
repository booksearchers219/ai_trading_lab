import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

    fig, ax = plt.subplots(figsize=(12, 6))

    # Align all arrays safely
    min_len = min(
        len(ma_equity),
        len(mr_equity),
        len(adaptive_equity),
        len(bh_equity),
        len(vote_equity),
        len(council_equity),
        len(data)
    )

    x_axis = data.index[-min_len:]
    price_series = data["Close"].iloc[-min_len:]

    ma_equity = ma_equity[-min_len:]
    mr_equity = mr_equity[-min_len:]
    adaptive_equity = adaptive_equity[-min_len:]
    bh_equity = bh_equity[-min_len:]
    vote_equity = vote_equity[-min_len:]
    council_equity = council_equity[-min_len:]


    ax.plot(x_axis, price_series, color="black", alpha=0.3, label="Price")

    # Strategy equity curves
    ax.plot(x_axis, ma_equity, label="MA")
    ax.plot(x_axis, mr_equity, label="MR")
    ax.plot(x_axis, adaptive_equity, label="Adaptive")
    ax.plot(x_axis, bh_equity, label="BuyHold")
    ax.plot(x_axis, vote_equity, label="Vote")
    ax.plot(x_axis, council_equity, label="Council")

    # BUY markers
    buy_x = [data.index[i] for i in ma_buys if i < len(data)]
    buy_y = [ma_equity[i-30] for i in ma_buys if i >= 30 and (i-30) < len(ma_equity)]

    ax.scatter(buy_x, buy_y, marker="^", color="green", s=60, label="MA BUY")

    # SELL markers
    sell_x = [data.index[i] for i in ma_sells if i < len(data)]
    sell_y = [ma_equity[i-30] for i in ma_sells if i >= 30 and (i-30) < len(ma_equity)]

    ax.scatter(sell_x, sell_y, marker="v", color="red", s=60, label="MA SELL")

    ax.legend()
    ax.grid(True)

    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    filename = f"chart_{ticker}_{BOT_NAME}.png"

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)

    print("\nReport saved:")
    print(" ", os.path.abspath(filename))