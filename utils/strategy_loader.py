import csv






def load_best_strategies(limit=5):

    strategies = []

    try:
        with open("strategies.csv") as f:

            reader = csv.DictReader(f)

            for row in reader:

                strategies.append((
                    int(row["Short"]),
                    int(row["Long"]),
                    float(row["Sharpe"])
                ))

    except:
        return []

    strategies.sort(key=lambda x: x[2], reverse=True)

    return strategies[:limit]
