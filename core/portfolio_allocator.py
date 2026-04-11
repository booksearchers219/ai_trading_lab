def allocate_by_sharpe(strategy_sharpes):

    # ensure every strategy gets at least a small weight
    MIN_WEIGHT = 0.05
    filtered = {
        k: max(v, MIN_WEIGHT)
        for k, v in strategy_sharpes.items()
    }

    total = sum(filtered.values())

    if total == 0:
        # fallback equal allocation
        n = len(filtered)
        return {k: 1/n for k in filtered}

    weights = {}

    for strat, sharpe in filtered.items():
        weights[strat] = sharpe / total

    # 🔥 OPTIONAL BOOST (aggressive mode)
    BOOST_FACTOR = 1.2

    weights = {
        k: min(v * BOOST_FACTOR, 1.0)
        for k, v in weights.items()
    }

    # renormalize after boost
    total = sum(weights.values())
    weights = {k: v / total for k, v in weights.items()}

    return weights
