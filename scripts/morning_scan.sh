#!/bin/bash

cd ~/ai_trading_lab

echo "=== MORNING SCAN ==="

python -m bots.market_agent --cycle --log
