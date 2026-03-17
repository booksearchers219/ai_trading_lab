#!/bin/bash

cd ~/ai_trading_lab

echo "Starting nightly strategy research..."

nice -n 15 taskset -c 0-3 python -m engines.evolve_engine --window 365

echo "Strategy research complete"
