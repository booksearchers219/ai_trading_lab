import numpy as np

from strategies import analyze_market
from backtest_utils import run_backtest, calculate_sharpe


def lab_worker(args):

    s, l, tickers, data_cache = args

    def ma_strategy(d, short=s, long=l):
        return analyze_market(d, short, long)

    sharpes = []

    for t in tickers:

        data = data_cache[t]

        equity, final_value, _, _, _ = run_backtest(data, ma_strategy)

        sharpe = calculate_sharpe(equity)

        if np.isnan(sharpe):
            sharpe = 0

        sharpes.append(sharpe)

    avg_sharpe = np.mean(sharpes)
    std_sharpe = np.std(sharpes)

    stability_score = avg_sharpe / (1 + std_sharpe)

    return ("MA", s, l, stability_score)
