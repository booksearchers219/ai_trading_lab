# Scott's Unified AI Trading Lab Cheat Sheet

This document merges all your cheat sheets into one organized reference.

------------------------------------------------------------------------

# Table of Contents

- [ELI5 Trading Concepts](#eli5-trading-concepts)
  - [The 3 Strategies Your Bot Tests](#the-3-strategies-your-bot-tests)
  - [Signals vs Trades](#signals-vs-trades-important-concept)
  - [Graph 1 — Price Chart](#-graph-1-----price-chart)
  - [Graph 2 — Strategy Comparison](#-graph-2-----strategy-comparison-very-important)
  - [Graph 3 — Drawdown](#-graph-3-----drawdown)
  - [Graph 4 — Trade Profit Distribution](#-graph-4-----trade-profit-distribution)
  - [Graph 5 — Win / Loss Count](#-graph-5-----win--loss-count)
  - [Graph 6 — Rolling Sharpe Ratio](#-graph-6-----rolling-sharpe-ratio)
  - [Terminal Statistics Cheat Sheet](#-terminal-statistics-cheat-sheet)
  - [Heatmap](#-heatmap)
  - [Strategy Dominance Chart](#-strategy-dominance-chart)
  - [Market Regime Detection](#-market-regime-detection)
  - [Market Scanner](#-market-scanner)
  - [Live Simulation Mode](#-live-simulation-mode)
  - [The 5 Most Important Things To Look At](#-the-5-most-important-things-to-look-at)
  - [The Big Idea of Your Program](#-the-big-idea-of-your-program)
  - [Important Truth About Trading](#-important-truth-about-trading)
  - [The Real Power of Your System](#-the-real-power-of-your-system)

- [Live Output Reference](#live-output-reference)
  - [Trend Panel](#1️⃣-trend-panel)
  - [Market Breadth](#2️⃣-market-breadth)
  - [Sector Flow](#3️⃣-sector-flow)
  - [Strategy Comparison Chart](#4️⃣-strategy-comparison-chart)
  - [Drawdown Chart](#5️⃣-drawdown-chart)
  - [Trade Profit Distribution](#6️⃣-trade-profit-distribution)
  - [Win/Loss Trade Count](#7️⃣-winloss-trade-count)
  - [Rolling Sharpe Ratio](#8️⃣-rolling-sharpe-ratio)
  - [Strategy Correlation Matrix](#9️⃣-strategy-correlation-matrix)
  - [Overall Goal of the System](#-overall-goal-of-the-system)

- [Market Agent Commands](#market-agent-commands)
  - [Basic Usage](#basic-usage)
  - [Analyze a Specific Stock](#analyze-a-specific-stock)
  - [Change Backtest Window](#change-backtest-window)
  - [Strategy Selection](#strategy-selection)
  - [Multi-Ticker Market Scan](#multi-ticker-market-scan)
  - [Parallel Scanning](#parallel-scanning-faster)
  - [Save Scan Reports](#save-scan-reports)
  - [Strategy Research Lab](#strategy-research-lab)
  - [Evolutionary Strategy Discovery](#evolutionary-strategy-discovery)
  - [Strategy Parameter Sweep](#strategy-parameter-sweep)
  - [Strategy Leaderboard](#strategy-leaderboard)
  - [Live Trading Simulation](#live-trading-simulation)

- [Quick Live Reference](#quick-live-reference)

- [TMUX](#tmux)
  - [Install tmux](#1-install-tmux-one-time)
  - [Start a New Session](#2-start-a-new-tmux-session)
  - [Detach From Session](#3-detach-from-tmux-leave-it-running)
  - [Reconnect to Session](#4-reconnect-to-the-running-session)
  - [Stop Program](#5-stop-the-program-inside-tmux)
  - [Update Code](#6-update-your-trading-lab-code-on-computer-2)
  - [List Sessions](#7-see-all-running-tmux-sessions)
  - [Kill Session](#8-kill-a-tmux-session-stop-everything)

- [Trading Lab Project Overview](#trading-lab-project-overview)
  - [System Overview](#system-overview)
  - [Core Engine](#core-engine)
  - [Data Utilities](#data-utilities)
  - [Market Scanning](#market-scanning)
  - [Trading Strategies](#trading-strategies)
  - [Portfolio System](#portfolio-system)
  - [Risk Management](#risk-management)
  - [Signal System](#signal-system)
  - [Logging](#logging)
  - [Graph and Chart Generators](#graph-and-chart-generators)
  - [Strategy Intelligence](#strategy-intelligence)
  - [Research Engines](#research-engines)
  - [Automatically Generated Data Files](#automatically-generated-data-files)
  - [Quick Mental Model](#quick-mental-model)

- [Git Moltbook Workflow](#git-moltbook-workflow)

- [GitHub Workflow](#github-workflow)

- [VI / VIM](#vi--vim)



# ELI5 Trading Concepts

# 🧠 ELI5 Cheat Sheet for Your Trading Program (Updated)

Your program basically answers one big question:

> **"If I started with \$10,000, which strategy would make the most
> money with the least risk?"**

Your system downloads market data, runs strategies, simulates trades,
and compares results.

# 🧠 The 3 Strategies Your Bot Tests

  -------------- ------------------ ------------------------------------
  **MA**         Follow the trend   Buy when price starts trending up
  **MR**         Buy dips           Buy when price drops below average
  **Adaptive**   Smart switcher     Uses MA or MR depending on market
  -------------- ------------------ ------------------------------------

These are defined in:

<div>

strategies.py

</div>

# 🧠 Signals vs Trades (Important Concept)

Your strategies generate **signals**, not trades.

Signal = opinion\
Trade = action

Example:

<div>

[]{#anchor}MA strategy → BUY signal

Portfolio → executes BUY trade

</div>

Your **portfolio engine** decides:

<div>

[]{#anchor-1}cash

shares

position

</div>

This logic lives in:

<div>

[]{#anchor-2}portfolio.py

</div>

# 📈 GRAPH 1 --- Price Chart

What you see:

Price line with arrows.

### What it means

Black line = stock price over time\
Colored arrows = where the bot traded

  --- ------
  ▲   BUY
  ▼   SELL
  --- ------

### Colors

  -------- ----------------
  Green    Moving Average
  Orange   Mean Reversion
  Purple   Adaptive
  -------- ----------------

Example:

<div>

[]{#anchor-3}▲ green → ▼ green

</div>

Means:

Moving Average bought there and sold there.

# 📊 GRAPH 2 --- Strategy Comparison (Very Important)

Lines you'll see:

<div>

[]{#anchor-4}Moving Average

Mean Reversion

Adaptive

Buy & Hold

</div>

This graph answers:

> **If each strategy started with \$10,000, how much would it grow?**

Example:

<div>

[]{#anchor-5}MA \$11,500

MR \$10,900

AD \$12,200

BuyHold \$11,000

</div>

Winner:

<div>

[]{#anchor-6}Adaptive

</div>

The code calculates portfolio value every day:

<div>

[]{#anchor-7}backtest_utils.py

portfolio_value = cash + (shares \* current_price)

</div>

# 📉 GRAPH 3 --- Drawdown

This shows **how painful the ride was**.

Drawdown = how far the account falls from its peak.

Example:

<div>

[]{#anchor-8}Start: \$10,000

Peak: \$12,000

Drop: \$9,000

</div>

Drawdown:

<div>

[]{#anchor-9}(9000 - 12000) / 12000 = -25%

</div>

Meaning:

<div>

[]{#anchor-10}-25% drawdown

</div>

Calculated here:

<div>

[]{#anchor-11}backtest_utils.py

</div>

# 📊 GRAPH 4 --- Trade Profit Distribution

This histogram shows **how big wins and losses are**.

Example:

<div>

[]{#anchor-12}Profit

\^

\| █

\| █ █ █

\| █ █

\|\_\_\_\_\_\_\_\_\_\_→

\$

</div>

Questions it answers:

• Do trades usually win?\
• Are losses large?\
• Are wins large?

# 📊 GRAPH 5 --- Win / Loss Count

Bar chart showing:

<div>

[]{#anchor-13}MA Wins

MA Losses

MR Wins

MR Losses

AD Wins

AD Losses

</div>

Example:

<div>

[]{#anchor-14}MA Wins: 8

MA Loss: 5

</div>

Win rate:

<div>

[]{#anchor-15}8 / 13 = 61%

</div>

Your program also prints this in the terminal.

# 📈 GRAPH 6 --- Rolling Sharpe Ratio

Sharpe Ratio measures:

> **Reward ÷ Risk**

  ----- -----------
  \<0   Losing
  0.5   OK
  1     Good
  2     Excellent
  ----- -----------

Calculated in:

<div>

[]{#anchor-16}backtest_utils.py

</div>

# 🧾 Terminal Statistics Cheat Sheet

Example terminal output:

<div>

[]{#anchor-17}Moving Average

Trades: 7

Win Rate: 28.6 %

Avg Trade: -88.17

Profit Factor: 0.34

</div>

### Trades

Number of BUY→SELL pairs.

<div>

[]{#anchor-18}BUY → SELL = 1 trade

</div>

### Win Rate

<div>

[]{#anchor-19}wins / total trades

</div>

Example:

<div>

[]{#anchor-20}7 trades

2 wins

= 28%

</div>

### Avg Trade

Average profit or loss per trade.

Example:

<div>

[]{#anchor-21}+50

-30

+70

-20

</div>

Average:

<div>

[]{#anchor-22}(50 - 30 + 70 - 20) / 4 = +17.5

</div>

### Profit Factor (Very Important)

Formula:

<div>

[]{#anchor-23}total profits / total losses

</div>

Example:

<div>

[]{#anchor-24}wins = \$1000

loss = \$500

profit factor = 2

</div>

Meaning:

You make **\$2 for every \$1 you lose**.

Calculated here:

<div>

[]{#anchor-25}backtest_utils.py

</div>

# 📊 Heatmap

This chart answers:

> **Which strategy wins on each stock?**

Example:

  ------ --- --- ---
  NVDA   0   1   0
  TSLA   0   0   1
  ------ --- --- ---

Color indicates the winner.

Generated in:

<div>

[]{#anchor-26}charts.py

</div>

# 📊 Strategy Dominance Chart

Bar chart:

<div>

[]{#anchor-27}MA wins: 7

MR wins: 12

AD wins: 18

</div>

This tells you:

> Which strategy wins **across many stocks**.

# 📊 Market Regime Detection

Your program detects if the market is:

  ---------- -------------------------
  TRENDING   Strong up/down movement
  SIDEWAYS   Bouncing around
  ---------- -------------------------

Code:

<div>

[]{#anchor-28}strategies.py

</div>

The **Adaptive strategy uses this**.

<div>

[]{#anchor-29}TRENDING → MA

SIDEWAYS → MR

</div>

# 📊 Market Scanner

When you run:

<div>

[]{#anchor-30}python3 -m bots.market_agent --scan sp500 --top 10

</div>

Your bot:

1️⃣ Loads many stocks\
2️⃣ Runs all strategies\
3️⃣ Compares results\
4️⃣ Picks winners

Output example:

<div>

[]{#anchor-31}MO \| SIDEWAYS \| MA: 9773 MR: 10598 AD: 10598 \| Winner:
MR

</div>

Meaning:

<div>

[]{#anchor-32}MR performed best on MO

</div>

# 🟢 Live Simulation Mode

When you run:

<div>

[]{#anchor-33}python3 market_agent.py --live

</div>

The bot:

1️⃣ Downloads live prices\
2️⃣ Runs strategies\
3️⃣ Generates signals\
4️⃣ Simulates trades in real time

No real money involved --- it\'s **paper trading**.

# 🧠 The 5 Most Important Things To Look At

If you only check a few things:

### 1️⃣ Final Portfolio Value

Which strategy made the most money.

### 2️⃣ Sharpe Ratio

Best **risk-adjusted** return.

### 3️⃣ Drawdown

How painful the losses were.

### 4️⃣ Win Rate

How often trades win.

### 5️⃣ Profit Factor

Are wins **bigger than losses**?

# 🧠 The Big Idea of Your Program

Your system basically does:

<div>

[]{#anchor-34}1. Download stock data

2\. Run strategies

3\. Generate signals

4\. Simulate trades

5\. Measure performance

6\. Compare strategies

</div>

Main engine:

<div>

[]{#anchor-35}backtest_utils.py

</div>

# ⚡ Important Truth About Trading

A strategy can:

<div>

[]{#anchor-36}lose often

but still make money

</div>

Example:

<div>

[]{#anchor-37}Win Rate = 40%

Profit Factor = 2.5

</div>

This can still be **very profitable**.

# 🧠 The Real Power of Your System

Your program already includes:

✔ backtesting\
✔ multi-strategy comparison\
✔ market regime detection\
✔ portfolio simulation\
✔ strategy scanning\
✔ heatmap analytics\
✔ Sharpe & drawdown risk metrics\
✔ live market simulation

That's essentially a **mini quantitative trading research lab**.

Which is pretty wild considering you built it piece-by-piece over the
last few days. 🚀

------------------------------------------------------------------------

# Live Output Reference

# 🧠 AI Trading Lab --- Live Output Cheat Sheet

## 1️⃣ Trend Panel

<div>

TREND PANEL

\-\-\-\-\-\-\-\-\---

SPY 🟢

NVDA 🟢

AMD 🟡

TSLA 🔴

META 🟢

</div>

**What it means**

This shows the **current trend direction** for key market leaders.

  ---- ----------------------------
  🟢   Uptrend / bullish momentum
  🟡   Sideways / neutral
  🔴   Downtrend / bearish
  ---- ----------------------------

**How to interpret**

If many are 🟢 → bullish market environment\
If many are 🔴 → risk-off market

SPY is the **overall market indicator**.

# 2️⃣ Market Breadth

<div>

[]{#anchor}MARKET BREADTH

\-\-\-\-\-\-\-\-\-\-\-\---

Bullish: 3

Neutral: 1

Bearish: 1

</div>

**What it means**

Counts how many stocks are:

-   Bullish
-   Neutral
-   Bearish

**Interpretation**

  -------------------- -----------------
  Bullish \> Bearish   Market strength
  Bearish \> Bullish   Market weakness
  Mostly Neutral       Sideways chop
  -------------------- -----------------

Breadth often **matters more than SPY alone**.

# 3️⃣ Sector Flow

<div>

[]{#anchor-1}SECTOR FLOW

\-\-\-\-\-\-\-\-\---

AI 🟢 STRONG

TECH 🟡 MIXED

MEDIA 🔴 WEAK

</div>

**What it means**

Groups stocks by sector and measures **average price change**.

  ------- -------------
  AI      NVDA, AMD
  TECH    AAPL, MSFT
  MEDIA   META, GOOGL
  ------- -------------

**Interpretation**

  ----------- -------------------------
  🟢 STRONG   Sector money flowing in
  🟡 MIXED    No clear direction
  🔴 WEAK     Sector selling pressure
  ----------- -------------------------

This helps detect **sector rotation**.

Example:

<div>

[]{#anchor-2}AI strong

TECH weak

</div>

→ capital moving **into semiconductors**

# 4️⃣ Strategy Comparison Chart

Graph shows equity curves for:

  ------------------ -------------------------------
  Moving Average     Trend following
  Mean Reversion     Buy dips
  Adaptive           Switch based on market regime
  Voting             Strategies vote
  Strategy Council   Ensemble of best strategies
  Buy & Hold         Benchmark
  ------------------ -------------------------------

**Goal**

Beat **Buy & Hold** with lower drawdown.

# 5️⃣ Drawdown Chart

Shows **how far each strategy falls during losses**.

  -------------- -----------------------
  Drawdown       \% drop from peak
  Max Drawdown   worst historical loss
  -------------- -----------------------

Lower drawdown = **safer strategy**.

# 6️⃣ Trade Profit Distribution

Histogram of trade results.

Interpretation:

  ----------------- -------------------------
  Tall center       small consistent trades
  Long right tail   occasional big winners
  Long left tail    dangerous losses
  ----------------- -------------------------

# 7️⃣ Win/Loss Trade Count

<div>

[]{#anchor-3}MA Wins / Losses

MR Wins / Losses

AD Wins / Losses

</div>

Shows **strategy reliability**.

  --------------- ---------------------------
  Win Rate        \% profitable trades
  Avg Trade       average profit per trade
  Profit Factor   gross profit ÷ gross loss
  --------------- ---------------------------

# 8️⃣ Rolling Sharpe Ratio

Measures **risk-adjusted performance over time**.

Rule of thumb:

> 2 \| Excellent\
> 1--2 \| Good\
> 0--1 \| Weak\
> \<0 \| Losing strategy

Rolling view shows **when strategies stop working**.

# 9️⃣ Strategy Correlation Matrix

Example:

<div>

[]{#anchor-4} MA MR AD

1.00 0.22 0.61

0.22 1.00 0.35

0.61 0.35 1.00

</div>

Measures **how similar strategies behave**.

  ---------- --------------------
  0.8+       very similar
  0.3--0.7   moderately related
  \<0.3      independent
  ---------- --------------------

Lower correlation → **better diversification**.

# 🔟 Overall Goal of the System

The system tries to answer:

> "Which strategies make the most money with the least risk?"

It tests strategies on historical data and compares them using:

-   Final equity
-   Sharpe ratio
-   Drawdown
-   Trade statistics

# 🚀 What Your System Is Becoming

Right now your program is evolving into:

<div>

[]{#anchor-5}Market Dashboard

\+

Strategy Research Lab

\+

AI Strategy Ensemble

</div>

In other words...

**a mini quant trading platform.**

Pretty awesome progress. 😄

------------------------------------------------------------------------

# Market Agent Commands

# AI Trading Lab --- Command Cheat Sheet

Assuming your main file is something like:

*python market_agent.py*

# Basic Usage

### Default run (quick analysis)

*python market_agent.py*

Defaults:

*Ticker: TSLA*

*Window: 6 months*

Shows:

-   market pulse
-   trend panel
-   momentum leaders
-   strategy comparison
-   leaderboard
-   charts

# Analyze a Specific Stock

*python market_agent.py --ticker NVDA*

Example:

*python market_agent.py --ticker AAPL*

# Change Backtest Window

*python market_agent.py --ticker NVDA --window 12*

Meaning:

*12 months of data*

# Strategy Selection

Run a specific strategy:

*python market_agent.py --strategy ma*

Options:

*ma Moving Average*

*mr Mean Reversion*

*adaptive Adaptive strategy*

Example:

*python market_agent.py --ticker TSLA --strategy adaptive*

# Multi-Ticker Market Scan

Scan a universe like S&P500.

*python market_agent.py --scan sp500*

Limit scan size:

*python market_agent.py --scan sp500 --limit 50*

# Parallel Scanning (faster)

*python market_agent.py --scan sp500 --parallel*

# Save Scan Reports

*python market_agent.py --scan sp500 --report*

Creates:

*reports/*

-   charts\*

-   scan_results\*

# Strategy Research Lab

Runs your **full research environment**.

*python market_agent.py --lab*

This typically runs:

*strategy testing*

*ranking*

*performance reports*

# Evolutionary Strategy Discovery

Runs genetic search for strategies.

*python market_agent.py --evolve*

This tries to **discover new trading strategies automatically**.

# Strategy Parameter Sweep

Search moving-average combinations.

*python market_agent.py --sweep*

Tests:

*Short MA: 5--30*

*Long MA: 20--200*

Outputs best Sharpe strategies.

# Strategy Leaderboard

Show top N strategies.

*python market_agent.py --top 10*

# Debug Strategy Votes

Shows strategy voting behavior.

*python market_agent.py --debug-votes*

Useful for debugging:

*voting_strategy*

*council_strategy*

# Live Trading Simulation

Runs portfolio simulation.

*python market_agent.py --live*

Uses:

*watchlist.txt*

*crypto_watchlist.txt*

# Use Top-10 Universe Instead of Watchlist

*python market_agent.py --live --top10*

Universe:

*AAPL*

*MSFT*

*NVDA*

*GOOGL*

*AMZN*

*META*

*TSLA*

*AVGO*

*AMD*

*NFLX*

# Strategy Autotrading Mode

Runs discovered strategies automatically.

*python market_agent.py --autotrade*

# Example Power Commands

### Quick NVDA analysis

*python market_agent.py --ticker NVDA*

### Deep NVDA research

*python market_agent.py --ticker NVDA --window 24 --sweep*

### Scan large market

*python market_agent.py --scan sp500 --parallel --limit 100*

### Strategy discovery

*python market_agent.py --evolve*

### Full research lab

*python market_agent.py --lab*

### Live portfolio simulation

*python market_agent.py --live*

# Files Used

### watchlist.txt

Example:

*NVDA*

*AMD*

*AAPL*

*MSFT*

*META*

*TSLA*

*AVGO*

*NFLX*

### crypto_watchlist.txt

Example:

*BTC-USD*

*ETH-USD*

*SOL-USD*

# Output Produced

Your script generates:

*chart.png*

*strategy leaderboard*

*trade stats*

*drawdowns*

*rolling Sharpe*

*signal radar*

*opportunity heatmap*

# Pro Tip (Highly Recommended)

Since your lab is getting big, add a **help shortcut**:

*python market_agent.py --help*

This will automatically show all flags from argparse.

If you want, I can also show you something **extremely cool for this
system**:

**A single command called**

*--research*

that automatically runs:

*scan*

*evolve*

*lab*

*parameter sweep*

*strategy ranking*

Basically turning your script into a **full autonomous quant research
engine**.

And honestly... your trading lab is already **90% of the way there.** 🚀

------------------------------------------------------------------------

# Quick Live Reference

TREND PANEL

SPY = overall market direction

🟢 bullish \| 🟡 neutral \| 🔴 bearish

MARKET BREADTH

More bullish than bearish = strong market

More bearish than bullish = weak market

SECTOR FLOW

AI = NVDA AMD

TECH = AAPL MSFT

MEDIA = META GOOGL

🟢 STRONG = money flowing into sector

🟡 MIXED = no clear trend

🔴 WEAK = sector selling

STRATEGIES

MA = trend following

MR = buy dips

Adaptive = switches by regime

Voting = strategies vote

Council = ensemble of best strategies

KEY METRICS

Final Value = ending portfolio value

Sharpe = risk-adjusted performance

Drawdown = worst loss from peak

SHARPE GUIDE

\>2 excellent

1--2 good

0--1 weak

\<0 losing

GOAL

Beat Buy & Hold with lower drawdown.

------------------------------------------------------------------------

# TMUX

# TMUX CHEAT SHEET (for your AI Trading Lab server)

## What tmux does

tmux lets programs keep running even if you close the terminal or
disconnect.\
Perfect for letting your trading simulation run 24/7.

# 1. Install tmux (one time)

sudo apt install tmux

# 2. Start a new tmux session

tmux new -s tradinglab

You are now inside a persistent session called **tradinglab**.

Start your program normally:

python3 market_agent.py --live

# 3. Detach from tmux (leave it running)

Press:

Ctrl + B\
then press\
D

Your program keeps running in the background.

# 4. Reconnect to the running session

tmux attach -t tradinglab

You will see the program exactly where it left off.

# 5. Stop the program inside tmux

Press:

Ctrl + C

# 6. Update your trading lab code on computer #2

Inside the repo:

git pull\
git fetch --tags

Restart the program:

python3 market_agent.py --live

# 7. See all running tmux sessions

tmux ls

Example output:

tradinglab: 1 windows

# 8. Kill a tmux session (stop everything)

tmux kill-session -t tradinglab

# Typical workflow for your setup

Computer #1 (development machine)\
edit code\
git commit\
git push

Computer #2 (simulation server)

tmux attach -t tradinglab\
Ctrl + C\
git pull\
git fetch --tags\
python3 market_agent.py --live\
Ctrl + B then D

Simulation keeps running 24/7.

------------------------------------------------------------------------

# Trading Lab Project Overview

# 📈 AI Trading Lab --- Command Cheat Sheet (Updated)

## Basic Syntax

<div>

python3 market_agent.py \[OPTIONS\]

</div>

# 🧪 Single Stock Analysis

Run default analysis (TSLA, 6 months)

<div>

[]{#anchor}python3 market_agent.py

</div>

Analyze a specific stock

<div>

[]{#anchor-1}python3 market_agent.py --ticker NVDA

</div>

Change backtest window

<div>

[]{#anchor-2}python3 market_agent.py --ticker AAPL --window 12

</div>

Example:

<div>

[]{#anchor-3}python3 market_agent.py --ticker TSLA --window 24

</div>

# 🔴 Live Strategy Competition (NEW)

Runs **real-time strategy trading simulation** using current market
data.

<div>

[]{#anchor-4}python3 market_agent.py --ticker NVDA --live

</div>

This launches the **Live Strategy Leaderboard** where strategies
compete:

<div>

[]{#anchor-5}LIVE STRATEGY LEADERBOARD

NVDA: 183.41

MA \$10,021

MR \$10,118

AD \$10,044

Leader: MR

</div>

Features:

• real-time market price\
• independent portfolios per strategy\
• automatic trade execution\
• live strategy leaderboard

Runs continuously until stopped.

Stop with:

<div>

[]{#anchor-6}CTRL + C

</div>

# 🔍 Strategy Optimization

Run moving average parameter sweep

<div>

[]{#anchor-7}python3 market_agent.py --ticker TSLA --sweep

</div>

Tests multiple MA combinations.

# 📊 Multi-Stock Scanning

Scan S&P500

<div>

[]{#anchor-8}python3 market_agent.py --scan sp500

</div>

Limit number of stocks

<div>

[]{#anchor-9}python3 market_agent.py --scan sp500 --limit 20

</div>

Good for testing.

# ⚡ Parallel Processing

Uses all CPU cores.

<div>

[]{#anchor-10}python3 market_agent.py --scan sp500 --parallel

</div>

Example:

<div>

[]{#anchor-11}python3 market_agent.py --scan sp500 --limit 50
--parallel

</div>

# 📁 Save Reports

Outputs charts and CSV files to:

<div>

[]{#anchor-12}reports/

</div>

Run with:

<div>

[]{#anchor-13}python3 market_agent.py --scan sp500 --report

</div>

Files generated:

<div>

[]{#anchor-14}heatmap.png

portfolio.png

strategy_dominance.png

sharpe_leaderboard.png

market_regimes.png

trade_opportunities.csv

scan_results.csv

</div>

# 🏆 Limit Leaderboard Results

Show fewer top strategies.

<div>

[]{#anchor-15}python3 market_agent.py --scan sp500 --top 10

</div>

Default is 20.

# 🚀 Recommended Commands

Quick test

<div>

[]{#anchor-16}python3 market_agent.py --scan sp500 --limit 10

</div>

Normal research run

<div>

[]{#anchor-17}python3 market_agent.py --scan sp500 --limit 50
--parallel

</div>

Full report run

<div>

[]{#anchor-18}python3 market_agent.py --scan sp500 --limit 100
--parallel --report

</div>

Deep strategy tuning

<div>

[]{#anchor-19}python3 market_agent.py --ticker NVDA --sweep

</div>

Live strategy competition

<div>

[]{#anchor-20}python3 market_agent.py --ticker NVDA --live

</div>

# 🧠 What Each Option Does

  --------------- -----------------------------------
  *--ticker*     analyze a single stock
  *--window*     backtest period in months
  *--scan*       run multi-ticker scan
  *--limit*      limit number of tickers
  *--parallel*   use all CPU cores
  *--sweep*      optimize MA parameters
  *--top*        limit leaderboard size
  *--report*     save charts & CSV output
  *--live*       run real-time strategy tournament
  --------------- -----------------------------------

# 📊 Best Daily Command

If running this every morning:

<div>

[]{#anchor-21}python3 market_agent.py --scan sp500 --limit 100
--parallel --report

</div>

This gives:

• strategy winners\
• market regime detection\
• Sharpe leaderboard\
• trade opportunities\
• charts

💡 **Tip**

Once you start using this a lot, you can create a shortcut command like:

<div>

[]{#anchor-22}scan

</div>

or

<div>

[]{#anchor-23}live

</div>

instead of typing the full Python command.

------------------------------------------------------------------------

# Trading Lab Commands (Updated)

\# AI Trading Lab -- Project Cheat Sheet

This file explains what each major Python file in the project does and

how the system flows together. It is meant to be a quick reference when

navigating the growing codebase.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# System Overview

Typical runtime flow when running:

python3 market_agent.py --live

Pipeline:

market_agent.py

↓

live_trading.py

↓

data_utils.py → fetch market data

↓

strategies.py → generate signals

↓

signal_engine.py → combine votes

↓

risk_manager.py → determine position size

↓

portfolio.py → execute buy/sell

↓

equity_logger.py → write equity log

↓

equity_chart.py → generate charts

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Core Engine

\## market_agent.py

Main command center.

Runs things like:

python3 market_agent.py --live

python3 market_agent.py --scan

python3 market_agent.py --lab

Responsibilities:

\- CLI argument handling

\- launching live trading

\- running backtests

\- running research tools

\- generating strategy comparison charts

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\## live_trading.py

The real-time trading engine.

Main responsibilities:

\- fetch live prices

\- compute strategy signals

\- vote on signals

\- risk management

\- place trades

\- update portfolio

\- log equity

\- generate charts

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Data Utilities

\## data_utils.py

Fetches market data.

Main function:

get_recent_data()

Used throughout the system for retrieving price history.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Market Scanning

\## momentum_scanner.py

Finds strongest stocks based on short-term momentum.

Typical output:

NVDA +2.1%

AMD +1.5%

META +0.9%

Used for discovery and market analysis.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Trading Strategies

\## strategies.py

Contains the core trading logic:

\- analyze_market()

\- mean_reversion_strategy()

\- adaptive_strategy()

\- volatility_breakout_strategy()

Each strategy returns:

BUY

SELL

HOLD

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Portfolio System

\## portfolio.py

Tracks the account state.

Handles:

\- cash

\- open positions

\- entry prices

\- trade history

Main methods:

buy()

sell()

total_value()

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\## portfolio_state.py

Saves and loads bot state so the system can resume after restart.

Creates file:

live_state.json

Stores:

\- cash

\- positions

\- entry prices

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Risk Management

\## risk_manager.py

Controls risk rules such as:

\- max risk per trade

\- portfolio exposure

\- position sizing

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Signal System

\## signal_engine.py

Combines strategy signals into final decisions.

Implements the voting system used by the trading bot.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Logging

\## equity_logger.py

Logs account performance to CSV files.

Example files created:

equity_log_default_bot.csv

equity_log_adaptive_bot.csv

equity_log_momentum_bot.csv

Each row contains:

\- timestamp

\- strategy equity values

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\## trade_logger.py

Logs each executed trade.

Example:

BUY NVDA 10 @ 920

SELL TSLA 5 @ 170

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Graph and Chart Generators

These Python files \*\*create graphs or visual charts\*\* in the system.

\## equity_chart.py

Generates portfolio performance charts.

Creates:

chart.png

reports/live_performance/equity\_\*.png

Displays:

\- equity curve

\- drawdown

\- strategy comparison

This chart is generated automatically during live trading.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\## trade_charts.py

Creates charts for individual trades.

Used when a new position is opened.

These charts show:

\- entry price

\- price movement

\- exit point

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\## visualization.py

Used primarily for \*\*backtest visualization\*\*.

Creates charts such as:

\- strategy equity curves

\- price overlays

\- trade markers

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\## (Optional / Experimental) Dashboard Scripts

If created during development, you may also have:

\### trading_dashboard.py

Live dashboard that shows:

\- equity curve

\- drawdown

\- portfolio stats

\### live_dashboard.py

Simple real-time chart viewer for equity logs.

These are monitoring tools and are not required for trading.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Strategy Intelligence

\## strategy_stats.py

Tracks strategy performance:

\- win rate

\- average trade

\- profit factor

Used to analyze which strategies perform best.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\## strategy_memory.json

Stores learning data for adaptive strategy weighting.

Tracks:

\- total P/L per strategy

\- number of trades

Used to adjust strategy weights over time.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Research Engines

Inside the \`engine/\` directory:

\### evolve_engine.py

Genetic search for new strategies.

\### lab_engine.py

Strategy experimentation and research.

\### scan_engine.py

Multi-ticker scanning engine.

These tools are used for \*\*strategy development and testing\*\*.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Automatically Generated Data Files

These appear during runtime:

equity_log\_\*.csv

chart.png

live_state.json

strategy_memory.json

reports/live_performance/

These files contain runtime logs, performance data, and charts.

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Quick Mental Model

Think of the system in layers:

Market Data

↓

Strategies

↓

Signal Voting

↓

Risk Manager

↓

Portfolio Execution

↓

Logging

↓

Charts & Visualization

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\---

\# Tip

As the project grows, keep this file updated so it always reflects the

architecture of the system.

market_agent.py ← main program

live_trading.py ← trading engine

equity_logger.py ← logs performance

equity_chart.py ← saves PNG charts

trading_dashboard.py ← live monitoring window

**updated graphs**

python3 trading_dashboard.py \---better info

python3 live_dashboard.py \---ok to delete

both showing same data

python chart_viewer.py

4way graph, doesn't update

tail equity_log_adaptive_bot.csv

log file w/data points

\*.png = (graphs)

python3 -m bots.market_agent --cycle

python3 -m dashboard.trading_dashboard.py

python3 -m bots.market_agent --auto

# 6️⃣ How you'll run the system

Terminal 1 (bot):

<div>

python3 market_agent.py --live

\*\*\*

python3 -m bots.market_agent --live

</div>

Terminal 2 (dashboard):

<div>

[]{#anchor}python3 trading_dashboard.py

</div>

Now you get \*\*\*\*live charts while the bot trades\*\*\*\*.

python3 -m dashboard.trading_dashboard

\*\*\* python3 -m bots.market_agent --daemon --log

------------------------------------------------------------------------

# Git Moltbook Workflow

(Unable to auto‑extract text from this file.)

------------------------------------------------------------------------

# GitHub Workflow

(Unable to auto‑extract text from this file.)

------------------------------------------------------------------------

# VI / VIM

(Unable to auto‑extract text from this file.)
