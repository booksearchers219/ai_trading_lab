import random

STRATEGY_TYPES = [
    "MA",
    "MR",
    "VOL",
    "RSI",
    "MOM"
]


def random_gene():

    strat = random.choice(STRATEGY_TYPES)

    if strat == "MA":
        short = random.randint(5, 40)
        long = random.randint(50, 200)
        return (strat, short, long)

    if strat == "MR":
        threshold = random.randint(5, 20)
        return (strat, threshold, None)

    if strat == "VOL":
        window = random.randint(10, 40)
        return (strat, window, None)

    if strat == "RSI":
        lower = random.randint(20, 40)
        upper = random.randint(60, 80)
        return (strat, lower, upper)

    if strat == "MOM":
        window = random.randint(5, 30)
        return (strat, window, None)


def mutate_gene(gene):

    strat, p1, p2 = gene

    if strat == "MA":
        p1 += random.randint(-5,5)
        p2 += random.randint(-10,10)

        p1 = max(3,p1)
        p2 = max(p1+10,p2)

    if strat == "MR":
        p1 += random.randint(-2,2)
        p1 = max(1,p1)

    if strat == "VOL":
        p1 += random.randint(-3,3)
        p1 = max(5,p1)

        if strat == "RSI":
            p1 += random.randint(-3, 3)
            p2 += random.randint(-3, 3)

            p1 = max(10, p1)
            p2 = max(p1 + 10, p2)

        if strat == "MOM":
            p1 += random.randint(-3, 3)
            p1 = max(3, p1)

    return (strat,p1,p2)


def crossover(gene1,gene2):

    strat1,p1a,p2a = gene1
    strat2,p1b,p2b = gene2

    if strat1 != strat2:
        return gene1

    if strat1 in ["MA", "RSI"]:
        return (strat1, (p1a + p1b) // 2, (p2a + p2b) // 2)

    return (strat1, (p1a + p1b) // 2, None)

    return (strat1,(p1a+p1b)//2,None)


def evolve_population(population):

    new_population = []

    population = sorted(population,key=lambda x:x[1],reverse=True)

    survivors = population[:10]

    for g,score in survivors:
        new_population.append(g)

    while len(new_population) < 30:

        parent = random.choice(survivors)[0]

        if random.random() < 0.5:
            child = mutate_gene(parent)
        else:
            other = random.choice(survivors)[0]
            child = crossover(parent,other)

        new_population.append(child)

    return new_population
