import time
import os
import pandas as pd
import matplotlib.pyplot as plt

LOGFILE = "equity_log_default_bot.csv"
REFRESH_SECONDS = 5
START_CAPITAL = 30000


def load_data():
    if not os.path.exists(LOGFILE):
        return None

    df = pd.read_csv(LOGFILE)

    if len(df) == 0:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["MA"] = pd.to_numeric(df["MA"], errors="coerce")

    return df


plt.ion()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14,10))

while True:

    df = load_data()

    if df is not None:

        ax1.clear()
        ax2.clear()
        ax3.clear()

        # -----------------
        # Equity curve
        # -----------------

        ax1.plot(df["timestamp"], df["MA"], linewidth=2, label="Portfolio")

        ax1.axhline(START_CAPITAL, linestyle="--")

        ax1.set_title("Equity Curve")
        ax1.set_ylabel("Account Value")
        ax1.grid(True)
        ax1.legend()

        # -----------------
        # Drawdown
        # -----------------

        df["peak"] = df["MA"].cummax()
        df["drawdown"] = (df["MA"] - df["peak"]) / df["peak"]

        ax2.fill_between(df["timestamp"], df["drawdown"], 0)

        ax2.set_title("Drawdown")
        ax2.set_ylabel("Drawdown %")
        ax2.grid(True)

        # -----------------
        # Performance stats
        # -----------------

        current = df["MA"].iloc[-1]
        pnl = current - START_CAPITAL
        pnl_pct = (pnl / START_CAPITAL) * 100

        stats = [
            f"Equity: ${current:,.2f}",
            f"P/L: ${pnl:,.2f}",
            f"Return: {pnl_pct:.2f}%"
        ]

        ax3.axis("off")

        y = 0.7

        for s in stats:
            ax3.text(0.05, y, s, fontsize=16)
            y -= 0.2

        ax3.set_title("Portfolio Stats")

        fig.autofmt_xdate()

        plt.pause(0.01)

    time.sleep(REFRESH_SECONDS)
