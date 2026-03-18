def print_ai_dashboard(
    regime,
    vol_regime,
    council_votes,
    decision,
    confidence,
    opportunities,
    crypto=False
):

    if crypto:
        print("\nAI CRYPTO TRADING DASHBOARD")
    else:
        print("\nAI TRADING DASHBOARD")

    print("--------------------")

    print(f"\nMarket Regime:      {regime}")
    print(f"Volatility Regime:  {vol_regime}")

    print("\nStrategy Council")
    print("----------------")

    names = ["MA", "MR", "AD", "VOL"]

    for name, vote in zip(names, council_votes):
        print(f"{name:<6} {vote}")

    print(f"\nFinal Decision: {decision} ({confidence*100:.0f}%)")

    print("\nTop Opportunities")
    print("-----------------")

    if not opportunities:
        print("None")

    for ticker, score in opportunities[:5]:
        print(f"{ticker:<6} score:{score}")