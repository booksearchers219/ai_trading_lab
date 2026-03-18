import random
from data_utils import get_recent_data
from core.strategies import analyze_market
from backtest_utils import run_backtest, calculate_sharpe
from multiprocessing import Pool, cpu_count
import math



def evaluate_strategy(params):

    short, long, threshold, tickers, data_cache = params

    def ma_strategy(d, s=short, l=long):
        return analyze_market(d, s, l)

    sharpes = []

    for t in tickers:

        data = data_cache[t]

        equity, final_value, _, _, _ = run_backtest(data, ma_strategy)

        sharpe = calculate_sharpe(equity)

        sharpes.append(sharpe)

    valid = [s for s in sharpes if not math.isnan(s)]

    if not valid:
        return (short, long, threshold, float("nan"))

    avg_sharpe = sum(valid) / len(valid)

    return (short, long, threshold, avg_sharpe)


def run_evolution_search(args):

    print("\nRunning Evolutionary Strategy Discovery\n")

    tickers = ["TSLA", "NVDA", "AAPL", "MSFT", "AMD"]

    data_cache = {}

    for t in tickers:

        data_cache[t] = get_recent_data(t, args.window)

    population_size = 20
    generations = 10

    population = []

    for _ in range(population_size):
        short = random.randint(3, 30)
        long = random.randint(short + 5, 120)
        threshold = random.uniform(0.0, 0.02)

        population.append((short, long, threshold))

    for g in range(generations):

        tasks = [(s, l, t, tickers, data_cache) for s, l, t in population]

        with Pool(cpu_count()) as pool:
            results = pool.map(evaluate_strategy, tasks)

        for r in results:
            print("RESULT:", r, "LEN:", len(r))


        results = [r for r in results if not math.isnan(r[2])]
        results.sort(key=lambda x: x[2], reverse=True)

        best = results[:5]

        print(f"\nGeneration {g + 1} best strategies")

        for s, l, t, sh in best:
            print(f"MA {s}/{l} thr:{t:.3f} Sharpe {sh:.2f}")

        population = []

        for s, l, t, _ in best:

            population.append((s, l, t))

            for _ in range(3):
                new_s = max(3, s + random.randint(-3, 3))
                new_l = max(new_s + 5, l + random.randint(-10, 10))
                new_t = max(0, min(0.03, t + random.uniform(-0.003, 0.003)))

                population.append((new_s, new_l, new_t))

    if not results:
        print("No valid strategies found.")
        return

    best = results[0]
    print("Best strategy:", best)

    print(f"MA {best[0]}/{best[1]} Sharpe {best[2]:.2f}")

    with open("data/best_strategy.txt", "w") as f:
        f.write(f"{best[0]},{best[1]}")

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", type=int, default=365)

    args = parser.parse_args()

    run_evolution_search(args)
