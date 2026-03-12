import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_equity_chart():
    print("DEBUG: generating equity chart...")


    if not os.path.exists("equity_log.csv"):
        return

    df = pd.read_csv("equity_log.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    plt.clf()
    plt.figure(figsize=(12, 6))

    plt.plot(df["timestamp"], df["MA"], label="MA")
    plt.plot(df["timestamp"], df["MR"], label="MR")
    plt.plot(df["timestamp"], df["AD"], label="AD")

    plt.axhline(30000, linestyle="--", color="black")

    plt.title("Live Strategy Equity Curves")
    plt.legend()
    plt.grid(True)

    output_dir = "reports/live_performance"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(output_dir, f"equity_{timestamp}.png")

    plt.tight_layout()
    plt.savefig(filename)

    # latest snapshot
    plt.savefig("chart.png")

    plt.close()





