MAX_RISK_PER_TRADE = 0.05
MAX_TICKER_ALLOCATION = 0.20


def calculate_position_size(portfolio, price, vote_strength, market_regime):

    portfolio_value = portfolio.total_value({})

    confidence = vote_strength / 3

    if market_regime == "SIDEWAYS":
        risk_multiplier = 0.7
    elif market_regime == "TRENDING":
        risk_multiplier = 1.0
    else:
        risk_multiplier = 0.5

    risk_amount = portfolio_value * MAX_RISK_PER_TRADE * confidence * risk_multiplier

    shares = int(risk_amount / price)

    return shares
