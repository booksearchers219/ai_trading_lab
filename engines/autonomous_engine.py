import argparse

from scanners.momentum_scanner import find_momentum_leaders
from engines.lab_engine import run_strategy_lab
from core.strategy_league import load_league, update_scores, save_league


DISCOVERY_UNIVERSE = [
    "NVDA","AMD","AVGO","TSLA","META","AAPL","MSFT",
    "GOOGL","AMZN","NFLX","SMCI","ARM","INTC",
    "MU","QCOM","ADBE","CRM","ORCL","NOW","SHOP"
]


def run_autonomous_cycle():

    print("\nAUTONOMOUS AI RESEARCH LOOP")
    print("---------------------------")

    leaders = find_momentum_leaders(DISCOVERY_UNIVERSE, top_n=5)

    print("\nMomentum Leaders")
    print("----------------")

    for ticker, pct in leaders:
        print(f"{ticker:<6} {pct*100:+.2f}%")

    print("\nRunning strategy labs...\n")

    for ticker, pct in leaders:

        print(f"Testing {ticker}")

        args = argparse.Namespace(
            ticker=ticker,
            window=6,
            top=10,
            report=False
        )

        run_strategy_lab(args)

    print("\nUpdating Strategy League")

    league = load_league()

    league = update_scores(league)

    save_league(league)

    print("\nTOP AI STRATEGIES")
    print("-----------------")

    for s in league[:10]:

        short = s["short"]
        long = s["long"]

        if long:
            params = f"{short}/{long}"
        else:
            params = f"{short}"

        print(
            f"{s['strategy']} {params} "
            f"Sharpe:{s['sharpe']:.2f} "
            f"Score:{s['score']:.2f}"
        )

    print("\nAutonomous cycle complete.")
