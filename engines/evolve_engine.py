import random
from data_utils import get_recent_data
from core.strategies import analyze_market
from backtest_utils import run_backtest, calculate_sharpe


def run_evolution_search(args):

    print("\nRunning Evolutionary Strategy Discovery\n")

    tickers = ["TSLA", "NVDA", "AAPL", "MSFT", "AMD"]

    population_size = 20
    generations = 10

    population = []

    for _ in range(population_size):
        short = random.randint(3, 30)
        long = random.randint(short + 5, 120)
        population.append((short, long))

    for g in range(generations):

        results = []

        for short, long in population:

            def ma_strategy(d, s=short, l=long):
                return analyze_market(d, s, l)

            sharpes = []

            for t in tickers:

                data = get_recent_data(t, args.window)

                equity, final_value, _, _, _ = run_backtest(data, ma_strategy)

                sharpe = calculate_sharpe(equity)

                sharpes.append(sharpe)

            avg_sharpe = sum(sharpes) / len(sharpes)

            results.append((short, long, avg_sharpe))

        results.sort(key=lambda x: x[2], reverse=True)

        best = results[:5]

        print(f"\nGeneration {g + 1} best strategies")

        for s, l, sh in best:
            print(f"MA {s}/{l} Sharpe {sh:.2f}")

        population = []

        for s, l, _ in best:

            population.append((s, l))

            for _ in range(3):

                new_s = max(3, s + random.randint(-3, 3))
                new_l = max(new_s + 5, l + random.randint(-10, 10))

                population.append((new_s, new_l))

    best = results[0]

    print("\nFinal Best Strategy")

    print(f"MA {best[0]}/{best[1]} Sharpe {best[2]:.2f}")
