#!/bin/bash

cd ~/ai_trading_lab

echo "=== EVENING RESEARCH ==="

python -m bots.market_agent --lab --log
python -m bots.market_agent --evolve --log
