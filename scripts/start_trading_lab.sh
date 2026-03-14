#!/bin/bash

SESSION="trading"

# If session already exists just attach
tmux has-session -t $SESSION 2>/dev/null
if [ $? -eq 0 ]; then
    tmux attach -t $SESSION
    exit
fi

# Start new session
tmux new-session -d -s $SESSION -n bot

# Pane 1 (top left) – trading bot
tmux send-keys -t $SESSION "cd ~/ai_trading_lab && python3 market_agent.py --live" C-m

# Pane 2 (top right) – trade log
tmux split-window -h -t $SESSION
tmux send-keys -t $SESSION "cd ~/ai_trading_lab && tail -f trade_log.txt" C-m

# Pane 3 (bottom) – system monitor
tmux split-window -v -t $SESSION:0.0
tmux send-keys -t $SESSION "htop" C-m

# Adjust layout
tmux select-layout -t $SESSION tiled

# Attach
tmux attach -t $SESSION

