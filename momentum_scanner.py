import yfinance as yf


def find_momentum_leaders(tickers, top_n=10):

    results = []

    for t in tickers:

        try:

            data = yf.download(t, period="5d", interval="1d", progress=False)

            if len(data) < 2:
                continue

            close = data["Close"]

            pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

            results.append((t, pct))

        except:
            continue

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]


def print_momentum_leaders(leaders):

    print("\nMARKET LEADERS")
    print("--------------")

    for t, pct in leaders:
        print(f"{t:<6} {pct*100:+.2f}%")
