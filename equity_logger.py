import os
import csv
from datetime import datetime


def log_equity(data, BOT_NAME="default_bot"):

    EQUITY_FILE = f"equity_log_{BOT_NAME}.csv"

    file_exists = os.path.exists(EQUITY_FILE)

    with open(EQUITY_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "MA", "MR", "AD"])

        writer.writerow([
            datetime.now().isoformat(),
            data.get("MA", 0),
            data.get("MR", 0),
            data.get("AD", 0),
        ])