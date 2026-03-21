from evolution.dna_engine import random_gene

def run_strategy_darwinism(league):

    SURVIVAL_THRESHOLD = 0.05
    MIN_POPULATION = 30
    MUTATION_COUNT = 20

    print("\nSTRATEGY DARWINISM")
    print("------------------")

    original_count = len(league)

    # Kill weak strategies
    league = [s for s in league if s["score"] > SURVIVAL_THRESHOLD]

    killed = original_count - len(league)

    print(f"Strategies killed: {killed}")
    print(f"Strategies surviving: {len(league)}")

    if len(league) < MIN_POPULATION:

        print("\nRepopulating strategy pool...")

        for _ in range(MUTATION_COUNT):

            strat, p1, p2 = random_gene()

            league.append({
                "strategy": strat,
                "short": p1,
                "long": p2,
                "sharpe": 0,
                "wins": 0,
                "losses": 0,
                "score": 0
            })

        print(f"New strategies spawned: {MUTATION_COUNT}")

    print("Total strategies now:", len(league))

    return league
