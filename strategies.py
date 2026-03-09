import numpy as np


def analyze_market(data, short_window=3, long_window=10):

    closes = data["Close"]

    if len(closes) < long_window:
        return "HOLD"

    short_ma = closes.rolling(window=short_window).mean().iloc[-1]
    long_ma = closes.rolling(window=long_window).mean().iloc[-1]

    if short_ma > long_ma:
        return "BUY"
    else:
        return "HOLD"

def mean_reversion_strategy(data, threshold=-0.01):

    closes = data["Close"]

    if len(closes) < 6:
        return "HOLD"

    five_day_return = (closes.iloc[-1] - closes.iloc[-6]) / closes.iloc[-6]
    # print("5-day return:", five_day_return)

    if five_day_return < threshold:
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


def strategy_vote(signals):

    buy_votes = signals.count("BUY")
    sell_votes = signals.count("SELL")

    if buy_votes > sell_votes and buy_votes >= max(2, len(signals)//2 + 1):
        return "BUY"

    if sell_votes > buy_votes and sell_votes >= max(2, len(signals)//2 + 1):
        return "SELL"

    return "HOLD"

def voting_strategy(data, state):
    ma_signal = analyze_market(data)
    mr_signal = mean_reversion_strategy(data)
    ad_signal = adaptive_strategy(data, state)

    signals = [ma_signal, mr_signal, ad_signal]

    decision = strategy_vote(signals)

    if state.get("debug"):
        print(
            f"MA:{ma_signal:<5} "
            f"MR:{mr_signal:<5} "
            f"AD:{ad_signal:<5} "
            f"→ VOTE:{decision}"
        )

    return decision

def council_strategy(data, state):

    regime = detect_regime(data)

    if regime == "TRENDING":
        strategies = state.get("trend_strategies", [])
    else:
        strategies = state.get("sideways_strategies", [])

    if not strategies:

        ma_signal = analyze_market(data)
        mr_signal = mean_reversion_strategy(data)
        ad_signal = adaptive_strategy(data, state)

        signals = [ma_signal, mr_signal, ad_signal]

        decision = strategy_vote(signals)

        if state.get("debug"):
            print("Council fallback vote:", signals, "→", decision)

        return decision

    buy_weight = 0
    sell_weight = 0

    signals = []

    for short, long, sharpe in strategies:

        signal = analyze_market(data, short, long)

        signals.append(signal)

        if signal == "BUY":
            buy_weight += sharpe

        if signal == "SELL":
            sell_weight += sharpe

    if buy_weight > sell_weight and buy_weight > 0:
        decision = "BUY"

    elif sell_weight > buy_weight and sell_weight > 0:
        decision = "SELL"

    else:
        decision = "HOLD"

    if state.get("debug"):
        print(f"{regime} council votes:", signals, "→", decision)

    return decision
