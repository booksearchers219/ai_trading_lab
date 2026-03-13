import time
import os
import pandas as pd
import matplotlib.pyplot as plt

LOGFILE = "equity_log_default_bot.csv"
REFRESH_SECONDS = 5


def load_data():
    if not os.path.exists(LOGFILE):
        return None

    df = pd.read_csv(LOGFILE)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8))

while True:

    df = load_data()

    if df is not None and len(df) > 0:

        ax1.clear()
        ax2.clear()

        ax1.plot(df["timestamp"], df["MA"], label="Equity", linewidth=2)

        ax1.axhline(30000, linestyle="--")

        ax1.set_title("Portfolio Equity")
        ax1.grid(True)
        ax1.legend()

        df["peak"] = df["MA"].cummax()
        df["drawdown"] = (df["MA"] - df["peak"]) / df["peak"]

        ax2.fill_between(df["timestamp"], df["drawdown"], 0)

        ax2.set_title("Drawdown")
        ax2.grid(True)

        fig.autofmt_xdate()

        plt.pause(0.01)

    time.sleep(REFRESH_SECONDS)
