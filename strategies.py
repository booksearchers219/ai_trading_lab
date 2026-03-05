import numpy as np


def analyze_market(data, short_window=5, long_window=20):

    closes = data["Close"]

    if len(closes) < 20:
        return "HOLD"

    short_ma = closes.rolling(window=short_window).mean().iloc[-1]
    long_ma = closes.rolling(window=long_window).mean().iloc[-1]

    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    else:
        return "HOLD"


def mean_reversion_strategy(data):

    closes = data["Close"]

    if len(closes) < 6:
        return "HOLD"

    five_day_return = (closes.iloc[-1] - closes.iloc[-6]) / closes.iloc[-6]

    if five_day_return < -0.03:
        return "BUY"

    return "HOLD"


def detect_regime(data):

    closes = data["Close"]

    if len(closes) < 50:
        return "SIDEWAYS"

    ma20 = closes.rolling(window=20).mean().iloc[-1]
    ma50 = closes.rolling(window=50).mean().iloc[-1]

    returns = closes.pct_change()
    recent_vol = returns.rolling(window=20).std().iloc[-1]

    vol_threshold = 0.02

    if ma20 > ma50 and recent_vol > vol_threshold:
        return "TRENDING"

    return "SIDEWAYS"


def regime_history(data):

    regimes = []

    for i in range(len(data)):

        if i < 50:
            regimes.append("SIDEWAYS")

        else:
            subset = data.iloc[:i]
            regimes.append(detect_regime(subset))

    return regimes


def adaptive_strategy(data, state):

    regime = detect_regime(data)

    if "current_regime" not in state:

        state["current_regime"] = regime
        state["regime_count"] = 1

    else:

        if regime == state["current_regime"]:
            state["regime_count"] += 1

        else:
            state["regime_count"] = 1

        if state["regime_count"] >= 5:
            state["current_regime"] = regime

    if state["current_regime"] == "TRENDING":
        return analyze_market(data)

    return mean_reversion_strategy(data)
