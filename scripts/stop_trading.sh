#!/bin/bash

echo "Stopping AI Trading Lab..."

echo "Stopping watchdog..."
pkill -f watchdog.sh

sleep 2

echo "Stopping trading bots..."
pkill -f bots.market_agent
pkill -f start_trading.sh
pkill -f ai_trading_lab

sleep 2

echo "Remaining trading processes:"
ps aux | grep ai_trading_lab | grep -v grep

echo "Shutdown complete."
