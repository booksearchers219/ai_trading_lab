import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_sp500_tickers():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    try:

        tables = pd.read_html(url)

        df = tables[0]

        tickers = df["Symbol"].tolist()

        # save cache
        with open("sp500_cache.txt", "w") as f:
            for t in tickers:
                f.write(t + "\n")

        return tickers

    except Exception as e:

        print("⚠ Failed to download S&P500 list")
        print("Reason:", e)

        # fallback to cached list
        try:
            with open("sp500_cache.txt") as f:
                tickers = [x.strip() for x in f.readlines()]

            print("Using cached S&P500 list")

            return tickers

        except Exception:

            print("No cache found — using fallback universe")

            return [
                "AAPL","MSFT","NVDA","GOOGL","AMZN",
                "META","TSLA","AMD","AVGO","NFLX",
                "ADBE","CRM","ORCL","INTC","QCOM",
                "MU","SHOP","SMCI","ARM"
            ]


def get_recent_data(ticker, months):

    stock = yf.Ticker(ticker)

    end_date = datetime.today()
    start_date = end_date - timedelta(days=months * 30)

    data = stock.history(start=start_date, end=end_date)

    # --- CLEAN DATA ---
    data = data.dropna()

    if data.empty or len(data) < 60:
        return None

    data = data[["Open", "High", "Low", "Close", "Volume"]]

    return data
