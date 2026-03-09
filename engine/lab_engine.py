import os
import csv
import multiprocessing as mp
import numpy as np

from data_utils import get_recent_data
from workers.lab_worker import lab_worker
from utils.reporting import plot_strategy_landscape


def run_strategy_lab(args):

    print("\nRunning Strategy Lab\n")

    tickers = ["TSLA", "NVDA", "AAPL", "MSFT", "AMD"]

    data_cache = {t: get_recent_data(t, args.window) for t in tickers}

    results = []

    short_windows = range(3, 120)
    long_windows = range(10, 400)

    jobs = []

    for s in short_windows:
        for l in long_windows:

            if s >= l:
                continue

            jobs.append((s, l, tickers, data_cache))

    print("Testing", len(jobs), "strategies across CPU cores\n")

    pool = mp.Pool(mp.cpu_count())

    results = pool.map(lab_worker, jobs, chunksize=50)

    pool.close()
    pool.join()

    results.sort(key=lambda x: x[3], reverse=True)

    print("\nTop Strategies Found\n")

    for r in results[:20]:
        print(f"{r[0]} {r[1]}/{r[2]} Sharpe {r[3]:.2f}")

    print("\nStrategy Scoreboard\n")

    print("Top Sharpe Strategies")
    for r in results[:10]:
        print(f"MA {r[1]}/{r[2]}  Sharpe {r[3]:.2f}")

    print("\nWorst Strategies")
    for r in results[-10:]:
        print(f"MA {r[1]}/{r[2]}  Sharpe {r[3]:.2f}")

    sharpes = [r[3] for r in results]

    mean_sharpe = np.mean(sharpes)
    std_sharpe = np.std(sharpes)

    print("\nSharpe Distribution")
    print("Average Sharpe:", round(mean_sharpe, 2))
    print("Sharpe Std Dev:", round(std_sharpe, 2))

    plot_strategy_landscape(results)

    existing = []

    if os.path.exists("strategies.csv"):

        with open("strategies.csv") as f:
            reader = csv.DictReader(f)

            for row in reader:
                existing.append((
                    "MA",
                    int(row["Short"]),
                    int(row["Long"]),
                    float(row["Sharpe"])
                ))

    combined = existing + results

    combined.sort(key=lambda x: x[3], reverse=True)

    survivors = []

    min_gap = 10

    for strat in combined:

        _, short, long, sharpe = strat

        too_close = False

        for s in survivors:
            if abs(short - s[1]) < min_gap and abs(long - s[2]) < min_gap:
                too_close = True
                break

        if not too_close:
            survivors.append(strat)

        if len(survivors) >= 100:
            break

    with open("strategies.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow(["Strategy", "Short", "Long", "Sharpe"])

        for r in survivors:
            writer.writerow(r)

    print(f"\nStrategy League Updated: {len(survivors)} survivors")
    print("\nSaved strategies to strategies.csv")
