import random
import numpy as np

from backtest_utils import run_backtest, calculate_sharpe
from core.strategies import analyze_market, mean_reversion_strategy


STRATEGY_TYPES = [
    "MA",
    "MR"
]


def random_genome():

    strat = random.choice(STRATEGY_TYPES)

    if strat == "MA":

        short = random.randint(5, 40)
        long = random.randint(50, 200)

        if short >= long:
            short = 5

        return ("MA", short, long)

    if strat == "MR":

        lookback = random.randint(5, 30)

        return ("MR", lookback, None)


def genome_to_strategy(genome):

    strat, p1, p2 = genome

    if strat == "MA":

        def s(d):
            return analyze_market(d, p1, p2)

        return s

    if strat == "MR":

        def s(d):
            return mean_reversion_strategy(d, p1)

        return s


def evolve_population(data, population=30):

    genomes = []

    for _ in range(population):
        genomes.append(random_genome())

    results = []

    for g in genomes:

        strategy = genome_to_strategy(g)

        equity, final_value, *_ = run_backtest(data, strategy)

        sharpe = calculate_sharpe(equity)

        if np.isnan(sharpe):
            sharpe = 0

        results.append((g, sharpe))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:10]
