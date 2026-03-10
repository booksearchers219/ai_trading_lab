from strategies import analyze_market, mean_reversion_strategy, adaptive_strategy
from strategies import regime_history


def generate_signals(prices, data_cache, adaptive_state):

    signal_list = []

    for ticker in prices:

        if ticker == "SPY":
            continue

        data = data_cache.get(ticker)

        if data is None:
            continue

        regime = regime_history(data)[-1]

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

        if buy_votes >= 2:
            signal_list.append(("COUNCIL", "BUY", ticker, buy_votes))

        elif sell_votes >= 2:
            signal_list.append(("COUNCIL", "SELL", ticker, sell_votes))

    return signal_list
