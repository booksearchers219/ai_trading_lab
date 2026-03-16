import csv
import os
from datetime import datetime

TRADE_FILE = "trade_history.csv"

def log_trade(symbol, action, shares, price, strategy, cash_after, equity_after):

    file_exists = os.path.exists(TRADE_FILE)

    with open(TRADE_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "symbol",
                "action",
                "shares",
                "price",
                "strategy",
                "cash_after",
                "equity_after"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            symbol,
            action,
            shares,
            price,
            strategy,
            cash_after,
            equity_after
        ])