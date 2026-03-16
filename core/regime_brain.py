def decide_strategy_mode(market_regime, volatility_regime):

    if volatility_regime == "HIGH":
        return "DEFENSIVE"

    if market_regime == "TRENDING":
        return "TREND"

    if market_regime == "SIDEWAYS":
        return "MEAN_REVERSION"

    return "NEUTRAL"
