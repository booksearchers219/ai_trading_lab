#!/bin/bash

SESSION="trading_lab"

# kill old session if it exists
tmux kill-session -t $SESSION 2>/dev/null

# start new detached session
tmux new-session -d -s $SESSION -c ~/ai_trading_lab

# split into 3 vertical panes
tmux split-window -h -t $SESSION
tmux select-pane -t 1
tmux split-window -h -t $SESSION

# evenly size panes
tmux select-layout -t $SESSION even-horizontal

# start bots
tmux send-keys -t $SESSION:0.0 'export BOT_NAME=momentum_bot; python market_agent.py --live --strategy_name momentum' C-m
tmux send-keys -t $SESSION:0.1 'export BOT_NAME=meanrev_bot; python market_agent.py --live --strategy_name meanrev' C-m
tmux send-keys -t $SESSION:0.2 'export BOT_NAME=adaptive_bot; python market_agent.py --live --strategy_name adaptive' C-m


# attach to session
tmux attach -t $SESSION

