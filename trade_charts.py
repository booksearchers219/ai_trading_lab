import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import os


def generate_trade_chart(ticker):

    if not os.path.exists("trade_log.csv"):
        return

    df = pd.read_csv("trade_log.csv")

    df = df[df["ticker"] == ticker]

    if df.empty:
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start = df["timestamp"].min().strftime("%Y-%m-%d")

    price_data = yf.download(ticker, period="5d", interval="5m", progress=False)

    if price_data.empty:
        return

    buys = df[df["action"] == "BUY"]
    sells = df[df["action"] == "SELL"]

    plt.figure(figsize=(12,6))

    plt.plot(price_data["Close"], label="Price")

    plt.scatter(
        buys["timestamp"],
        buys["price"],
        marker="^",
        color="green",
        s=100,
        label="BUY"
    )

    plt.scatter(
        sells["timestamp"],
        sells["price"],
        marker="v",
        color="red",
        s=100,
        label="SELL"
    )

    plt.title(f"{ticker} Trade History")
    plt.legend()
    plt.grid(True)

    os.makedirs("reports/live_trades", exist_ok=True)

    path = f"reports/live_trades/{ticker}_trades.png"

    plt.savefig(path)
    plt.close()
