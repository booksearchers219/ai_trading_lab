import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_equity_chart():

    if not os.path.exists("equity_log.csv"):
        return

    df = pd.read_csv("equity_log.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    plt.figure(figsize=(12,6))

    plt.plot(df["timestamp"], df["MA"], label="MA")
    plt.plot(df["timestamp"], df["MR"], label="MR")
    plt.plot(df["timestamp"], df["AD"], label="AD")

    plt.axhline(10000, linestyle="--", color="black")

    plt.title("Live Strategy Equity Curves")
    plt.legend()
    plt.grid(True)

    os.makedirs("reports/live_performance", exist_ok=True)

    plt.savefig("reports/live_performance/equity_curves.png")

    plt.close()

