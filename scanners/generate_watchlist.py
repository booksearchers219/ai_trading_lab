import yfinance as yf
from datetime import datetime

print("\nWatchlist update:", datetime.now())

UNIVERSE = [
    "AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA","AMD","AVGO","NFLX",
    "QCOM","INTC","CRM","ADBE","ORCL","NOW","SNOW","UBER","SHOP","COIN",
    "PLTR","PYPL","JPM","GS","BAC","XOM","CVX","LLY","UNH","CAT",
    "BA","GE","DIS","ROKU","DKNG","MRNA","PANW"
]

TOP_N = 20

print("Downloading market data...")

data = yf.download(
    " ".join(UNIVERSE),
    period="3mo",
    group_by="ticker",
    progress=False
)

scores = []

for ticker in UNIVERSE:

    try:

        if ticker not in data:
            continue

        closes = data[ticker]["Close"]

        if len(closes) < 20:
            continue

        start = closes.iloc[-20]
        end = closes.iloc[-1]

        momentum = (end - start) / start

        scores.append((ticker, momentum))

    except Exception:
        continue

scores.sort(key=lambda x: x[1], reverse=True)

leaders = [t for t, _ in scores[:TOP_N]]

with open("watchlist.txt", "w") as f:
    for t in leaders:
        f.write(t + "\n")

print("\nNew watchlist generated:\n")
for t in leaders:
    print(t)
