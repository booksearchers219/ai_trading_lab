import os
import csv
import multiprocessing as mp
import numpy as np
from visualization.backtest_report import generate_backtest_report
from data_utils import get_recent_data
from workers.lab_worker import lab_worker
from utils.reporting import plot_strategy_landscape
from core.strategy_registry import STRATEGY_REGISTRY
import random


def run_strategy_lab(args):
    print("\nRunning Strategy Lab\n")

    candidate_universe = [
        "NVDA", "SMCI", "TSLA", "AMD", "PLTR", "COIN", "META", "AMZN", "NFLX", "MSFT",
        "AAPL", "SHOP", "ROKU", "PANW", "SNOW", "UBER", "CRM", "GOOGL", "AVGO", "DKNG",
        "INTC", "MU", "BABA", "RIVN", "LCID", "SOFI", "AFRM", "DDOG", "NET"
    ]

    vol_scores = []

    for t in candidate_universe:
        try:
            d = get_recent_data(t, args.window)
            vol = d["Close"].pct_change().std()
            vol_scores.append((t, vol))
        except:
            continue

    vol_scores.sort(key=lambda x: x[1], reverse=True)

    base_universe = [t for t, _ in vol_scores[:20]]

    random.shuffle(base_universe)

    random.shuffle(base_universe)

    if args.ticker:
        tickers = [args.ticker] + [t for t in base_universe if t != args.ticker]
    else:
        tickers = base_universe
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

    # --------------------------------------------------
    # Generate backtest report chart
    # --------------------------------------------------

    try:

        ticker = tickers[0]
        data = data_cache[ticker]

        # Run a basic backtest so we have chart data
        from core.strategies import analyze_market, mean_reversion_strategy, adaptive_strategy
        from backtest_utils import run_backtest

        ma_equity, _, ma_buys, ma_sells, ma_profits = run_backtest(data, analyze_market)
        mr_equity, _, mr_buys, mr_sells, mr_profits = run_backtest(data, mean_reversion_strategy)
        adaptive_equity, _, ad_buys, ad_sells, ad_profits = run_backtest(data, adaptive_strategy)

        # simple placeholders for comparison curves
        bh_equity = ma_equity
        vote_equity = ma_equity
        council_equity = ma_equity

        if tickers[0] == args.ticker:
            generate_backtest_report(
                ticker,
                "lab",
                data,
                ma_equity,
                mr_equity,
                adaptive_equity,
                bh_equity,
                vote_equity,
                council_equity,
                ma_buys,
                ma_sells,
                mr_buys,
                mr_sells,
                ad_buys,
                ad_sells,
                ma_profits,
                mr_profits,
                ad_profits
            )

    except Exception as e:
        print("Chart generation failed:", e)
