import csv
import os
from datetime import datetime

EQUITY_LOG = "equity_log.csv"


def log_equity(values):

    file_exists = os.path.exists(EQUITY_LOG)

    with open(EQUITY_LOG, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "MA", "MR", "AD"])

        writer.writerow([
            datetime.now().isoformat(),
            values.get("MA", 0),
            values.get("MR", 0),
            values.get("AD", 0)
        ])
