import subprocess
import os
import time

bots = [
    ("momentum_bot", "momentum"),
    ("meanrev_bot", "meanrev"),
    ("adaptive_bot", "adaptive")
]

processes = []

for bot, strat in bots:

    env = os.environ.copy()
    env["BOT_NAME"] = bot

    print(f"Launching {bot}")

    p = subprocess.Popen(
        [
            "python",
            "market_agent.py",
            "--live",
            "--strategy_name",
            strat
        ],
        env=env
    )

    processes.append(p)

    time.sleep(2)

for p in processes:
    p.wait()
