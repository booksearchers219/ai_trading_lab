import yfinance as yf
from data_utils import get_recent_data


def find_momentum_leaders(data_cache, top_n=5):

    results = []

    for ticker, data in data_cache.items():

        if data is None or len(data) < 2:
            continue

        close = data["Close"]

        prev = close.iloc[-2]
        curr = close.iloc[-1]

        if prev == 0:
            continue

        pct = float((curr - prev) / prev)

        results.append((ticker, pct))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]



def print_momentum_leaders(leaders):

    print("\nMARKET LEADERS")
    print("--------------")

    for t, pct in leaders:
        print(f"{t:<6} {pct*100:+.2f}%")
