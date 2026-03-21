#!/bin/bash

SESSION="trading_lab"

# kill previous session if it exists
tmux kill-session -t $SESSION 2>/dev/null

# Start new detached tmux session
tmux new-session -d -s $SESSION

# Split into 3 vertical panes
tmux split-window -h -t $SESSION
tmux split-window -h -t $SESSION:0.0

# Resize panes evenly
tmux select-layout -t $SESSION even-horizontal

# Pane 0 (left) - start immediately
tmux send-keys -t $SESSION:0.0 "cd ~/ai_trading_lab && python3 -m bots.market_agent --research-daemon" C-m

# Pane 1 (middle) - wait 5 minutes
tmux send-keys -t $SESSION:0.1 "sleep 300 && cd ~/ai_trading_lab && python3 -m bots.market_agent --daemon --log --autotrade --report --live" C-m

# Pane 2 (right) - wait 10 minutes
tmux send-keys -t $SESSION:0.2 "sleep 600 && cd ~/ai_trading_lab && python3 -m bots.market_agent --crypto --daemon --log --autotrade --live" C-m

# Attach to session
tmux attach -t $SESSION
