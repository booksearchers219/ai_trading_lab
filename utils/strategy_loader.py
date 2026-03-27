import csv

def load_best_strategies(bot_name=None, limit=5):
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

    except Exception as e:
        print("DEBUG load failed:", e)
        return []

    strategies.sort(key=lambda x: x[2], reverse=True)

    return strategies[:limit]