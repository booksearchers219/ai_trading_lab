def allocate_by_sharpe(strategy_sharpes):

    # remove negative sharpes
    filtered = {k: max(v, 0) for k, v in strategy_sharpes.items()}

    total = sum(filtered.values())

    if total == 0:
        # fallback equal allocation
        n = len(filtered)
        return {k: 1/n for k in filtered}

    weights = {}

    for strat, sharpe in filtered.items():
        weights[strat] = sharpe / total

    return weights
