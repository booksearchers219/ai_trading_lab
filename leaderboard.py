def print_leaderboard(strategy_equity):

    print("\nSTRATEGY LEADERBOARD")
    print("--------------------")

    ranked = sorted(
        strategy_equity.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for name, value in ranked:
        print(f"{name:<4} ${value:,.2f}")
