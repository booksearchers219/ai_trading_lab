def print_leaderboard(strategy_results):

    print("\nSTRATEGY LEADERBOARD")
    print("------------------------------")
    print(f"{'Strategy':<10} {'Final':>10} {'Sharpe':>10}")
    print("------------------------------")

    ranked = sorted(
        strategy_results.items(),
        key=lambda x: x[1]["sharpe"],
        reverse=True
    )

    for name, stats in ranked:
        final_value = stats["final"]
        sharpe = stats["sharpe"]

        print(f"{name:<10} ${final_value:>9,.2f} {sharpe:>9.2f}")