def trend_symbol(short_ma, long_ma):

    diff = (short_ma - long_ma) / long_ma

    if diff > 0.01:
        return "↑↑"
    elif diff > 0:
        return "↑"
    elif abs(diff) < 0.005:
        return "→"
    else:
        return "↓"


def calculate_trend(data, short_window=5, long_window=20):

    closes = data["Close"]

    if len(closes) < long_window:
        return "?"

    short_ma = closes.tail(short_window).mean()
    long_ma = closes.tail(long_window).mean()

    return trend_symbol(short_ma, long_ma)


def print_trend_panel(symbol_data):

    print("\nTREND STRENGTH")
    print("--------------")

    for symbol, data in symbol_data.items():

        trend = calculate_trend(data)

        if trend in ["↑", "↑↑"]:
            color = "🟢"
        elif trend == "→":
            color = "🟡"
        else:
            color = "🔴"

        print(f"{symbol:<6} {color} {trend}")

def print_market_breadth(symbol_data):

    bullish = 0
    neutral = 0
    bearish = 0

    for symbol, data in symbol_data.items():

        trend = calculate_trend(data)

        if trend in ["↑", "↑↑"]:
            bullish += 1
        elif trend == "→":
            neutral += 1
        else:
            bearish += 1

    print("\nBREADTH")
    print("-------")
    print(f"Bullish: {bullish}")
    print(f"Neutral: {neutral}")
    print(f"Bearish: {bearish}")
