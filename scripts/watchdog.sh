#!/bin/bash

cd ~/ai_trading_lab

echo "AI Trading Lab Watchdog Started"

while true
do
    RUNNING=$(pgrep -f "bots.market_agent")

    if [ -z "$RUNNING" ]; then
        echo "$(date) Bot not running. Restarting..."

        nohup python -m bots.market_agent --daemon --log >> watchdog.log 2>&1 &
    fi

    sleep 60
done
