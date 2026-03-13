import csv
import os
from datetime import datetime



BOT_NAME = os.getenv("BOT_NAME", "default_bot")

filename = f"trade_log_{BOT_NAME}.csv"


def log_trade(strategy, ticker, action, price, shares):

    file_exists = os.path.exists(TRADE_LOG)

    with open(TRADE_LOG, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "strategy",
                "ticker",
                "action",
                "price",
                "shares"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            strategy,
            ticker,
            action,
            price,
            shares
        ])
