import os
import csv
from datetime import datetime

BOT_NAME = os.getenv("BOT_NAME", "default_bot")

EQUITY_LOG = f"equity_log_{BOT_NAME}.csv"


def log_equity(strategy_values):

    file_exists = os.path.exists(EQUITY_LOG)

    with open(EQUITY_LOG, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "MA", "MR", "AD"])

        writer.writerow([
            datetime.now().isoformat(),
            strategy_values.get("MA", 0),
            strategy_values.get("MR", 0),
            strategy_values.get("AD", 0),
        ])

