from core.strategies import (
    analyze_market,
    mean_reversion_strategy,
    volatility_breakout_strategy,
)

STRATEGY_REGISTRY = {
    "MA": {
        "func": analyze_market,
        "params": {
            "short": range(5, 50, 5),
            "long": range(20, 200, 10),
        },
    },

    "MR": {
        "func": mean_reversion_strategy,
        "params": {
            "lookback": range(5, 30, 5),
        },
    },

    "VOL": {
        "func": volatility_breakout_strategy,
        "params": {
            "window": range(10, 60, 10),
        },
    },
}
