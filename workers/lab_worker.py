import numpy as np

from core.strategies import analyze_market
from backtest_utils import run_backtest, calculate_sharpe


def lab_worker(args):

    strategy_type, p1, p2, tickers, data_cache = args

    def strategy(d):

        if strategy_type == "MA":

            if p1 is None or p2 is None:
                return "HOLD"

            return analyze_market(d, p1, p2)

        elif strategy_type == "MR":

            if p1 is None:
                return "HOLD"

            from core.strategies import mean_reversion_strategy
            return mean_reversion_strategy(d, p1)

        elif strategy_type == "VOL":

            from core.strategies import volatility_breakout_strategy
            return volatility_breakout_strategy(d)

        else:
            return "HOLD"

    sharpes = []

    for t in tickers:

        data = data_cache[t]

        equity, final_value, _, _, _ = run_backtest(data, strategy)

        sharpe = calculate_sharpe(equity)

        if np.isnan(sharpe):
            sharpe = 0

        sharpes.append(sharpe)

    avg_sharpe = np.mean(sharpes)
    std_sharpe = np.std(sharpes)

    stability_score = avg_sharpe / (1 + std_sharpe)

    return (strategy_type, p1, p2, stability_score)