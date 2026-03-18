import numpy as np

from core.strategies import analyze_market
from backtest_utils import run_backtest, calculate_sharpe


def lab_worker(args):

    strategy_type, p1, p2, tickers, data_cache = args

    # ----- Build strategy function -----

    if strategy_type == "MA":

        def strategy(d, short=p1, long=p2):
            return analyze_market(d, short, long)

    elif strategy_type == "MR":

        from core.strategies import mean_reversion_strategy

        def strategy(d, lb=p1):
            return mean_reversion_strategy(d, lb)

    elif strategy_type == "VOL":

        from core.strategies import volatility_breakout_strategy

        def strategy(d):
            return volatility_breakout_strategy(d)

    else:

        def strategy(d):
            return "HOLD"

    # ----- Run backtests -----

    sharpes = []

    for t in tickers:

        data = data_cache[t]

        # skip bad datasets
        if data is None:
            continue

        equity, final_value, _, _, _ = run_backtest(data, strategy)

        sharpe = calculate_sharpe(equity)

        if np.isnan(sharpe):
            sharpe = 0

        sharpes.append(sharpe)

    if not sharpes:
        return (strategy_type, p1, p2, -999)

    avg_sharpe = np.mean(sharpes)
    std_sharpe = np.std(sharpes)

    # stability-adjusted score
    stability_score = avg_sharpe - (std_sharpe * 0.5)

    return (strategy_type, p1, p2, stability_score)