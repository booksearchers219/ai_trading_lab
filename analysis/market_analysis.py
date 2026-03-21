from core.volatility_regime import detect_volatility_regime
from backtest_utils import regime_history


def print_market_regime(data):
    regimes = regime_history(data)

    if not regimes:
        return

    current = regimes[-1]

    vol_regime = detect_volatility_regime(data)

    print("\nVOLATILITY REGIME")
    print("-----------------")
    print(vol_regime)

    print("\nMARKET REGIME")
    print("-------------")

    if current == "TRENDING":
        print("TRENDING 📈")
    else:
        print("SIDEWAYS 🔄")

def print_market_sentiment(symbol_data):

    score = 0

    for symbol, df in symbol_data.items():

        if len(df) < 2:
            continue

        close = df["Close"]

        pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

        if pct > 0.01:
            score += 1
        elif pct < -0.01:
            score -= 1

    print("\nMARKET SENTIMENT")
    print("----------------")

    if score >= 3:
        print("BULLISH 🔥🔥🔥")

    elif score >= 1:
        print("BULLISH 🔥")

    elif score == 0:
        print("NEUTRAL ⚖️")

    elif score <= -3:
        print("BEARISH ❄️❄️❄️")

    else:
        print("BEARISH ❄️")


def print_watchlist_momentum(data):

    changes = []

    for symbol, df in data.items():

        if len(df) < 2:
            continue

        close = df["Close"]

        pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

        changes.append((symbol, pct))

    changes.sort(key=lambda x: x[1], reverse=True)

    print("\nMOMENTUM LEADERS")
    print("----------------")

    for sym, pct in changes:
        print(f"{sym:<6} {pct * 100:+.2f}%")


def print_strategy_confidence(symbol_data):

    buy_votes = 0
    sell_votes = 0
    hold_votes = 0

    from core.strategies import analyze_market, mean_reversion_strategy, adaptive_strategy

    for symbol, df in symbol_data.items():

        if len(df) < 20:
            continue

        vote_ma = analyze_market(df)
        vote_mr = mean_reversion_strategy(df)
        vote_ad = adaptive_strategy(df, {})

        votes = [vote_ma, vote_mr, vote_ad]

        for v in votes:
            if v == "BUY":
                buy_votes += 1
            elif v == "SELL":
                sell_votes += 1
            else:
                hold_votes += 1

    total = buy_votes + sell_votes + hold_votes

    if total == 0:
        return

    buy_pct = buy_votes / total
    sell_pct = sell_votes / total

    print("\nSTRATEGY CONSENSUS")
    print("------------------")

    bar = int(buy_pct * 10)

    print(f"BUY confidence  {'█' * bar}{'░' * (10 - bar)} {buy_pct * 100:.0f}%")
    print(f"SELL pressure   {sell_pct * 100:.0f}%")

def print_strategy_agreement(symbol_data):

    buy_votes = 0
    sell_votes = 0
    hold_votes = 0

    from core.strategies import analyze_market, mean_reversion_strategy, adaptive_strategy

    for symbol, df in symbol_data.items():

        if len(df) < 20:
            continue

        votes = [
            analyze_market(df),
            mean_reversion_strategy(df),
            adaptive_strategy(df, {})
        ]

        for v in votes:
            if v == "BUY":
                buy_votes += 1
            elif v == "SELL":
                sell_votes += 1
            else:
                hold_votes += 1

    total = buy_votes + sell_votes + hold_votes

    if total == 0:
        return

    strongest = max(buy_votes, sell_votes, hold_votes) / total

    print("\nSTRATEGY AGREEMENT")
    print("------------------")

    if strongest > 0.70:
        print("HIGH AGREEMENT ⚡")
    elif strongest > 0.50:
        print("MODERATE AGREEMENT")
    else:
        print("LOW AGREEMENT ⚠️")


def compute_sector_strength(data):

    sectors = {
        "AI": ["NVDA", "AMD"],
        "TECH": ["AAPL", "MSFT"],
        "MEDIA": ["META", "GOOGL"]
    }

    sector_scores = {}

    for sector, symbols in sectors.items():

        changes = []

        for s in symbols:

            if s in data and len(data[s]) >= 2:

                close = data[s]["Close"]

                pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

                changes.append(pct)

        if not changes:
            sector_scores[sector] = ("UNKNOWN", 0)
            continue

        avg = sum(changes) / len(changes)

        if avg > 0.01:
            label = "🟢 STRONG"
        elif avg < -0.01:
            label = "🔴 WEAK"
        else:
            label = "🟡 MIXED"

        sector_scores[sector] = (label, avg)

    return sector_scores
