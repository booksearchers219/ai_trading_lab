strategy_stats = {
    "MA": {"trades": 0, "wins": 0, "losses": 0, "total_return": 0},
    "MR": {"trades": 0, "wins": 0, "losses": 0, "total_return": 0},
    "AD": {"trades": 0, "wins": 0, "losses": 0, "total_return": 0},
}

def record_trade(strategy, pnl):
    s = strategy_stats[strategy]

    s["trades"] += 1
    s["total_return"] += pnl

    if pnl > 0:
        s["wins"] += 1
    else:
        s["losses"] += 1


def print_strategy_stats():
    print("\nSTRATEGY INTELLIGENCE")
    print("---------------------")

    for name, s in strategy_stats.items():

        trades = s["trades"]

        if trades == 0:
            winrate = 0
            avg = 0
        else:
            winrate = (s["wins"] / trades) * 100
            avg = s["total_return"] / trades

        print(
            f"{name}  trades:{trades}  winrate:{winrate:.1f}%  avg:{avg:.2f}%"
        )
