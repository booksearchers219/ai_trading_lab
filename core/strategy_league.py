import csv
import os


LEAGUE_FILE = "strategies.csv"


def load_league():

    strategies = []

    if not os.path.exists(LEAGUE_FILE):
        return strategies

    with open(LEAGUE_FILE) as f:
        reader = csv.DictReader(f)

        for row in reader:
            strategies.append({
                "strategy": row["Strategy"],
                "short": int(row["Short"]) if row["Short"] else None,
                "long": int(row["Long"]) if row["Long"] else None,
                "sharpe": float(row["Sharpe"]),
                "wins": int(row.get("Wins", 0)),
                "losses": int(row.get("Losses", 0)),
                "score": float(row.get("Score", 0))
            })

    return strategies


def update_scores(strategies):

    for s in strategies:

        winrate = 0
        total = s["wins"] + s["losses"]

        if total > 0:
            winrate = s["wins"] / total

        s["score"] = (s["sharpe"] * 0.6) + (winrate * 0.4)

    strategies.sort(key=lambda x: x["score"], reverse=True)

    return strategies


def save_league(strategies):

    with open(LEAGUE_FILE, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow(["Strategy", "Short", "Long", "Sharpe", "Wins", "Losses", "Score"])

        for s in strategies:

            writer.writerow([
                s["strategy"],
                s["short"],
                s["long"],
                s["sharpe"],
                s["wins"],
                s["losses"],
                s["score"]
            ])
