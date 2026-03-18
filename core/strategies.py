import numpy as np

MA_CACHE = {}

def analyze_market(data, short_window=10, long_window=50):

    if short_window is None or long_window is None:
        return "HOLD"

    closes = data["Close"]

    if len(closes) < long_window:
        return "HOLD"

    key_short = (len(data), short_window)
    key_long = (len(data), long_window)

    if key_short not in MA_CACHE:
        MA_CACHE[key_short] = closes.rolling(window=short_window).mean()

    if key_long not in MA_CACHE:
        MA_CACHE[key_long] = closes.rolling(window=long_window).mean()

    short_series = MA_CACHE[key_short]
    long_series = MA_CACHE[key_long]

    if len(short_series) < 2 or len(long_series) < 2:
        return "HOLD"

    prev_short = short_series.iloc[-2]
    prev_long = long_series.iloc[-2]

    curr_short = short_series.iloc[-1]
    curr_long = long_series.iloc[-1]

    # prevent NaN comparisons
    if np.isnan(prev_short) or np.isnan(prev_long) or np.isnan(curr_short) or np.isnan(curr_long):
        return "HOLD"

    if prev_short <= prev_long and curr_short > curr_long:
        return "BUY"

    elif prev_short >= prev_long and curr_short < curr_long:
        return "SELL"

    return "HOLD"

def mean_reversion_strategy(data, threshold=-0.01):

    closes = data["Close"]

    if len(closes) < 24:
        return "HOLD"

    # lookback ~5 hours on 5m candles
    change = (closes.iloc[-1] - closes.iloc[-60]) / closes.iloc[-24]

    if change < threshold:
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


def volatility_breakout_strategy(data):

    closes = data["Close"]
    highs = data["High"]
    lows = data["Low"]

    if len(closes) < 20:
        return "HOLD"

    today_range = highs.iloc[-1] - lows.iloc[-1]

    avg_range_series = (highs - lows).rolling(window=10).mean()

    avg_range = avg_range_series.iloc[-2]

    if np.isnan(avg_range):
        return "HOLD"

    if today_range > avg_range * 1.5:
        return "BUY"

    return "HOLD"



def council_strategy(data, state):

    votes = []

    vote_ma = analyze_market(data)
    vote_mr = mean_reversion_strategy(data)
    vote_ad = adaptive_strategy(data, state.setdefault("adaptive_state", {}))
    vote_vol = volatility_breakout_strategy(data)

    votes = [vote_ma, vote_mr, vote_ad, vote_vol]

    buy_votes = votes.count("BUY")
    sell_votes = votes.count("SELL")

    if buy_votes >= 3:
        decision = "BUY"
    elif sell_votes >= 3:
        decision = "SELL"
    else:
        decision = "HOLD"

    if state.get("debug"):

        print("\nSTRATEGY COUNCIL")
        print("----------------")

        names = ["MA","MR","AD","VOL"]

        for name,v in zip(names,votes):
            print(f"{name:<5} {v}")

        confidence = max(buy_votes, sell_votes) / len(votes)

        print(f"\nFINAL DECISION: {decision} ({confidence*100:.0f}% confidence)")

    return decision


def crash_radar(data):

    closes = data["Close"]

    if len(closes) < 30:
        return False

    returns = closes.pct_change()

    # last candle move
    last_move = returns.iloc[-1]

    # short-term drop
    short_drop = (closes.iloc[-1] - closes.iloc[-12]) / closes.iloc[-12]

    # volatility spike
    vol = returns.rolling(20).std().iloc[-1]

    # panic selling conditions
    if short_drop < -0.03 and vol > 0.01 and last_move > -0.01:
        return True

    return False