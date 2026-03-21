portfolio_tickers = []




def print_opportunity_heatmap(signals):
    print("\nOPPORTUNITY HEATMAP")
    print("-------------------")

    if not signals:
        print("None")
        return

    counts = {}

    for s in signals:
        ticker = s[2]  # FIXED (ticker is index 2)

        counts[ticker] = counts.get(ticker, 0) + 1

    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    for ticker, score in ranked[:10]:
        bar = "█" * score

        print(f"{ticker:<6} {bar:<10} {score}")


def rank_opportunities(signals):

    ranked = []

    for strat, action, ticker, votes in signals:

        for strat, action, ticker, votes in signals:

            score = votes * 2

            if action == "BUY":
                ranked.append((ticker, score))

            elif action == "SELL":
                ranked.append((ticker, -score))

        score = votes * 2

        ranked.append((ticker, score))

    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked

def print_signal_radar(signals):
    print("\nSIGNAL RADAR")
    print("------------")

    if not signals:
        print("None")
        return

    counts = {}

    for s in signals:
        ticker = s[2]  # FIXED
        action = s[1]

        key = (ticker, action)

        counts[key] = counts.get(key, 0) + 1

    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    for (ticker, action), score in ranked[:10]:
        print(f"{ticker:<6} {action:<4} strength {score}")


def print_top_opportunities(signals):
    global portfolio_tickers

    top_trades = rank_opportunities(signals)[:5]

    portfolio_tickers = [t[0] for t in top_trades]

    print("\nAI PORTFOLIO MANAGER")
    print("--------------------")

    for t, score in top_trades:
        print(f"{t:<6} score:{score}")

        capital = 10000
        weight = capital / len(portfolio_tickers)

        portfolio_weights = {t: weight for t in portfolio_tickers}

        print("\nPORTFOLIO ALLOCATION")
        print("--------------------")

        for t, w in portfolio_weights.items():
            print(f"{t:<6} ${w:.0f}")

    ranked = rank_opportunities(signals)

    print("\nTOP OPPORTUNITIES")
    print("-----------------")

    if not ranked:
        print("None")
        return

    for ticker, score in ranked:
        print(f"{ticker:<6} score:{score}")

def print_risk_monitor(portfolio, prices):
    value = portfolio.total_value(prices)

    positions_value = value - portfolio.cash

    exposure = (positions_value / value) * 100 if value > 0 else 0

    largest = None
    largest_pct = 0

    for ticker, shares in portfolio.positions.items():

        price = prices.get(ticker, 0)

        pos_value = shares * price

        pct = (pos_value / value) * 100 if value > 0 else 0

        if pct > largest_pct:
            largest_pct = pct
            largest = ticker

    print("\nRISK MONITOR")
    print("------------")

    print(f"Exposure: {exposure:.1f}%")

    if largest:
        print(f"Largest Position: {largest} {largest_pct:.1f}%")

    if exposure > 80:
        print("⚠ WARNING: Portfolio exposure high")

    if largest_pct > 25:
        print("⚠ WARNING: Position concentration risk")

