import yfinance as yf

def find_momentum_leaders(tickers, top_n=5):

    results = []

    data = yf.download(
        tickers,
        period="1mo",
        group_by="ticker",
        auto_adjust=True,
        threads=True
    )

    for ticker in tickers:

        try:
            close = data[ticker]["Close"]

            if len(close) < 2:
                continue

            prev = close.iloc[-2]
            curr = close.iloc[-1]

            if prev == 0:
                continue

            pct = float((curr - prev) / prev)

            results.append((ticker, pct))

        except Exception:
            continue

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]

def print_momentum_leaders(leaders):

    print("\nMARKET LEADERS")
    print("--------------")

    for t, pct in leaders:
        print(f"{t:<6} {pct*100:+.2f}%")