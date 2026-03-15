import numpy as np
from backtest_utils import run_backtest, calculate_sharpe


def walkforward_test(data, strategy_func, train_ratio=0.7):

    split = int(len(data) * train_ratio)

    train_data = data.iloc[:split]
    test_data = data.iloc[split:]

    # train performance
    train_equity, train_final, *_ = run_backtest(train_data, strategy_func)
    train_sharpe = calculate_sharpe(train_equity)

    # test performance
    test_equity, test_final, *_ = run_backtest(test_data, strategy_func)
    test_sharpe = calculate_sharpe(test_equity)

    return {
        "train_sharpe": train_sharpe,
        "test_sharpe": test_sharpe,
        "train_final": train_final,
        "test_final": test_final
    }
