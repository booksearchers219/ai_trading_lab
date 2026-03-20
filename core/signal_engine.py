from core.strategies import analyze_market, mean_reversion_strategy, adaptive_strategy
from core.strategies import regime_history


def generate_signals(prices, data_cache, adaptive_state):

    signal_list = []

    for ticker in prices:

        if ticker == "SPY":
            continue

        data = data_cache.get(ticker)

        # ----- TREND FILTER -----

        if len(data) >= 200:

            ma200 = data["Close"].rolling(200).mean()

            if data["Close"].iloc[-1] < ma200.iloc[-1]:
                downtrend = True
            else:
                downtrend = False

        else:
            downtrend = False

        if data is None:
            continue

        regimes = regime_history(data)

        if not regimes:
            continue

        regime = regimes[-1]

        signals = {}

        if regime == "TRENDING":
            signals["MA"] = analyze_market(data)
            signals["AD"] = adaptive_strategy(data, adaptive_state)

        elif regime == "SIDEWAYS":
            signals["MR"] = mean_reversion_strategy(data)
            signals["AD"] = adaptive_strategy(data, adaptive_state)

        else:
            signals["AD"] = adaptive_strategy(data, adaptive_state)

        votes = list(signals.values())

        buy_votes = votes.count("BUY")
        sell_votes = votes.count("SELL")

        vote_strength = buy_votes + sell_votes

        if buy_votes >= 2 and not downtrend:
            signal_list.append(("COUNCIL", "BUY", ticker, vote_strength))

        elif sell_votes >= 2:
            signal_list.append(("COUNCIL", "SELL", ticker, vote_strength))

    # Rank strongest signals first
    signal_list = sorted(signal_list, key=lambda x: x[3], reverse=True)

    if not signal_list:
        return signal_list

    return signal_list
