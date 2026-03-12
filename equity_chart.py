import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker as mtick

import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_equity_chart():
    print("DEBUG: generating equity chart...")

    if not os.path.exists("equity_log.csv"):
        return

    df = pd.read_csv("equity_log.csv")

    # convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # sort and remove duplicates
    df = df.sort_values("timestamp")
    df = df.drop_duplicates(subset="timestamp")

    # keep only last 500 rows so chart stays clean
    df = df.tail(500)

    # compute drawdown
    df["MA"] = pd.to_numeric(df["MA"], errors="coerce")

    df["peak"] = df["MA"].cummax()
    df["drawdown"] = (df["MA"] - df["peak"]) / df["peak"]
    df["drawdown"] = df["drawdown"].fillna(0)

    plt.clf()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))

    # -----------------------
    # Equity Curve
    # -----------------------
    ax1.plot(df["timestamp"], df["MA"], label="Portfolio Equity", linewidth=2)

    ax1.axhline(30000, linestyle="--", color="black")

    ax1.set_title("Portfolio Equity")
    ax1.set_ylabel("Value ($)")
    ax1.grid(True)
    ax1.legend()

    # -----------------------
    # Drawdown
    # -----------------------
    ax2.fill_between(df["timestamp"], df["drawdown"], 0)

    ax2.set_title("Drawdown")
    ax2.set_ylabel("Drawdown %")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax2.grid(True)

    # -----------------------
    # Strategy Comparison
    # -----------------------
    ax3.plot(df["timestamp"], df["MA"], label="MA")
    ax3.plot(df["timestamp"], df["MR"], label="MR")
    ax3.plot(df["timestamp"], df["AD"], label="AD")

    ax3.set_title("Strategy Performance")
    ax3.set_ylabel("Equity")
    ax3.grid(True)
    ax3.legend()

    plt.tight_layout()

    output_dir = "reports/live_performance"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(output_dir, f"equity_{timestamp}.png")

    plt.savefig(filename)

    # latest snapshot
    plt.savefig("chart.png")

    plt.close()

