import os
import multiprocessing as mp
import numpy as np
import csv
from datetime import datetime
import random

from data_utils import get_recent_data, get_sp500_tickers
from workers.ticker_worker import process_ticker
from utils.reporting import cleanup_reports
from charts import (
    save_heatmap,
    save_portfolio_chart,
    save_strategy_dominance,
    save_sharpe_leaderboard,
    save_regime_distribution,
    save_trade_opportunities,
    save_regime_strategy_chart
)


def run_scan(args):

    ticker_list = []

    if args.scan == "sp500":
        all_tickers = get_sp500_tickers()

        if args.limit:
            ticker_list = all_tickers[:args.limit]
        else:
            ticker_list = all_tickers

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)

    if args.report:
        os.makedirs("reports", exist_ok=True)
        report_dir = f"reports/{timestamp}"
        os.makedirs(report_dir, exist_ok=True)

    cleanup_reports()

    results = []

    if args.parallel:

        print("\nRunning parallel scan...\n")

        pool = mp.Pool(mp.cpu_count())

        data_cache = {}

        months = args.window

        for ticker in ticker_list:
            try:
                data_cache[ticker] = get_recent_data(ticker, months)
            except:
                pass

        job_args = [(ticker, data_cache[ticker]) for ticker in data_cache]

        random.shuffle(job_args)

        results = pool.map(process_ticker, job_args)
        results = [r for r in results if r is not None]

        pool.close()
        pool.join()

    else:

        months = args.window

        for i, ticker in enumerate(ticker_list, 1):

            print(f"\nTesting {ticker} ({i}/{len(ticker_list)})")

            data = get_recent_data(ticker, months)

            r = process_ticker((ticker, data))

            if r:
                results.append(r)

    print("\nScan complete.")
    print("Tickers tested:", len(results))

    return results



import csv


def analyze_scan_results(results, args):

    print("\nStrategy Results Summary\n")

    results.sort(key=lambda x: max(x[5], x[6], x[7]), reverse=True)

    top_n = args.top if args.top else 20
    top_results = results[:top_n]

    ma_wins = 0
    mr_wins = 0
    ad_wins = 0

    for r in top_results:

        best_value = max(r[2], r[3], r[4])

        if best_value == r[2]:
            winner = "MA"
            ma_wins += 1
        elif best_value == r[3]:
            winner = "MR"
            mr_wins += 1
        else:
            winner = "AD"
            ad_wins += 1

        print(
            f"{r[0]:<5} | "
            f"{r[1]:<8} | "
            f"MA: {'$' + format(r[2], ',.2f'):>12} "
            f"MR: {'$' + format(r[3], ',.2f'):>12} "
            f"AD: {'$' + format(r[4], ',.2f'):>12} "
            f"| Winner: {winner}"
        )

    print("\nStrategy Leaderboard\n")

    print(f"{'Moving Average':<18}: {ma_wins}")
    print(f"{'Mean Reversion':<18}: {mr_wins}")
    print(f"{'Adaptive':<18}: {ad_wins}")



def run_scan_and_report(args):

    results = run_scan(args)

    analyze_scan_results(results, args)


