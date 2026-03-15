#!/bin/bash

cd ~/ai_trading_lab

echo "=== STARTING TRADING BOT ==="

nohup python -m bots.market_agent --daemon --log > daemon.log 2>&1 &
