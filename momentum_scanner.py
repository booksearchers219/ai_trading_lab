import yfinance as yf
from data_utils import get_recent_data


def find_momentum_leaders(universe, top_n=5):

    results = []

    for ticker in universe:

        data = get_recent_data(ticker, 1)

        if data is None or len(data) < 2:
            continue

        close = data["Close"]

        pct = float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2])

        results.append((ticker, pct))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]



def print_momentum_leaders(leaders):

    print("\nMARKET LEADERS")
    print("--------------")

    for t, pct in leaders:
        print(f"{t:<6} {pct*100:+.2f}%")
