import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_sp500_tickers():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    tables = pd.read_html(
        url,
        storage_options={"User-Agent": "Mozilla/5.0"}
    )

    df = tables[0]

    tickers = df["Symbol"].tolist()

    tickers = [t.replace(".", "-") for t in tickers]

    return tickers


def get_recent_data(ticker, months):

    stock = yf.Ticker(ticker)

    end_date = datetime.today()
    start_date = end_date - timedelta(days=months * 30)

    data = stock.history(start=start_date, end=end_date)

    print("\nBacktest Window")
    print(start_date.strftime("%Y-%m-%d"), "→", end_date.strftime("%Y-%m-%d"))

    return data
