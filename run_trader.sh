#!/bin/bash

while true
do
    echo "Starting AI Trading Lab..."

    python3 generate_watchlist.py
    python3 market_agent.py --live

    echo "Bot stopped. Restarting in 5 seconds..."
    sleep 5
done
