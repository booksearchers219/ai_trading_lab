import os
import csv
import multiprocessing as mp
import numpy as np

from data_utils import get_recent_data
from workers.lab_worker import lab_worker
from utils.reporting import plot_strategy_landscape
from core.strategy_registry import STRATEGY_REGISTRY

def run_strategy_lab(args):

    print("\nRunning Strategy Lab\n")

    tickers = ["TSLA", "NVDA", "AAPL", "MSFT", "AMD"]

    data_cache = {t: get_recent_data(t, args.window) for t in tickers}

    results = []


    jobs = []

    for name, strat in STRATEGY_REGISTRY.items():

        params = strat["params"]

        if name == "MA":

            for s in params["short"]:
                for l in params["long"]:

                    if s >= l:
                        continue

                    jobs.append((name, s, l, tickers, data_cache))

        elif name == "MR":

            for lb in params["lookback"]:
                jobs.append((name, lb, None, tickers, data_cache))

        elif name == "VOL":

            for w in params["window"]:
                jobs.append((name, w, None, tickers, data_cache))
    print("Testing", len(jobs), "strategies across CPU cores\n")

    pool = mp.Pool(mp.cpu_count())

    results = pool.map(lab_worker, jobs, chunksize=50)

    pool.close()
    pool.join()

    results.sort(key=lambda x: x[3], reverse=True)

    print("\nTop Strategies Found\n")

    for r in results[:20]:
        name, p1, p2, sharpe = r

        if p2 is not None:
            param_str = f"{p1}/{p2}"
        else:
            param_str = f"{p1}"

        print(f"{name} {param_str} Sharpe {sharpe:.4f}")

    print("\nStrategy Scoreboard\n")

    print("Top Sharpe Strategies")

    for r in results[:10]:

        name, p1, p2, sharpe = r

        if p2 is not None:
            param_str = f"{p1}/{p2}"
        else:
            param_str = f"{p1}"

        print(f"{name} {param_str}  Sharpe {sharpe:.2f}")

    print("\nWorst Strategies")

    for r in results[-10:]:

        name, p1, p2, sharpe = r

        if p2 is not None:
            param_str = f"{p1}/{p2}"
        else:
            param_str = f"{p1}"

        print(f"{name} {param_str}  Sharpe {sharpe:.2f}")

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
                short_val = int(row["Short"]) if row["Short"] else None
                long_val = int(row["Long"]) if row["Long"] else None

                existing.append((
                    row["Strategy"],
                    short_val,
                    long_val,
                    float(row["Sharpe"])
                ))

    combined = existing + results

    combined.sort(key=lambda x: x[3], reverse=True)

    survivors = []

    min_gap = 10

    for strat in combined:

        name, p1, p2, sharpe = strat

        too_close = False

        for s in survivors:

            s_name, s_p1, s_p2, _ = s

            # Skip strategies that don't have two parameters
            if p2 is None or s_p2 is None:
                continue

            if abs(p1 - s_p1) < min_gap and abs(p2 - s_p2) < min_gap:
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
