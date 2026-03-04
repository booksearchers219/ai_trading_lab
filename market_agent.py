import yfinance as yf
import matplotlib.pyplot as plt

def get_recent_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="6mo")
    return data

def analyze_market(data):
    closes = data["Close"]

    if len(closes) < 20:
        return "HOLD"

    short_ma = closes.rolling(window=5).mean().iloc[-1]
    long_ma = closes.rolling(window=20).mean().iloc[-1]

    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    else:
        return "HOLD"
    last_three = closes[-3:]

def mean_reversion_strategy(data):
    closes = data["Close"]

    if len(closes) < 6:
        return "HOLD"

    # Calculate percent change over last 5 days
    five_day_return = (closes.iloc[-1] - closes.iloc[-6]) / closes.iloc[-6]

    # If price dropped more than 3% in 5 days, BUY
    if five_day_return < -0.03:
        return "BUY"
    else:
        return "HOLD"



def execute_trade(decision, price, cash, shares):
    print(f"Current Price: {price:.2f}")

    if decision == "BUY" and cash >= price:
        shares += 1
        cash -= price
        print("Executed: BUY 1 share")

    elif decision == "SELL" and shares > 0:
        shares -= 1
        cash += price
        print("Executed: SELL 1 share")

    else:
        print("Executed: HOLD")

    portfolio_value = cash + (shares * price)

    return cash, shares, portfolio_value


def detect_regime(data):
    closes = data["Close"]

    if len(closes) < 50:
        return "SIDEWAYS"

    ma20 = closes.rolling(window=20).mean().iloc[-1]
    ma50 = closes.rolling(window=50).mean().iloc[-1]

    returns = closes.pct_change()
    recent_vol = returns.rolling(window=20).std().iloc[-1]

    # Threshold for meaningful volatility (tweakable)
    vol_threshold = 0.02  # 2% daily std

    if ma20 > ma50 and recent_vol > vol_threshold:
        return "TRENDING"
    else:
        return "SIDEWAYS"


def adaptive_strategy(data, state):
    regime = detect_regime(data)

    # Initialize state if first call
    if "current_regime" not in state:
        state["current_regime"] = regime
        state["regime_count"] = 1
    else:
        if regime == state["current_regime"]:
            state["regime_count"] += 1
        else:
            state["regime_count"] = 1

        # Only switch if regime stable for 5 days
        if state["regime_count"] >= 5:
            state["current_regime"] = regime

    if state["current_regime"] == "TRENDING":
        return analyze_market(data)
    else:
        return mean_reversion_strategy(data)

def run_backtest(data, strategy_function):
    cash = 10000
    shares = 0
    equity_curve = []
    hold_days = 0
    state = {}

    for i in range(50, len(data)):
        recent_data = data.iloc[:i]
        if strategy_function.__name__ == "adaptive_strategy":
            decision = strategy_function(recent_data, state)
        else:
            decision = strategy_function(recent_data)
        current_price = data["Close"].iloc[i]

        portfolio_value = cash + (shares * current_price)
        equity_curve.append(portfolio_value)

        # BUY
        if decision == "BUY" and shares == 0:
            investment_amount = cash * 0.5
            shares = int(investment_amount / current_price)

            if shares > 0:
                trade_value = shares * current_price
                cost = trade_value * 0.001
                cash -= trade_value + cost
                hold_days = 5

        # SELL from signal
        elif decision == "SELL" and shares > 0:
            trade_value = shares * current_price
            cost = trade_value * 0.001
            cash += trade_value - cost
            shares = 0
            hold_days = 0

        # Timed exit
        elif shares > 0 and hold_days == 0:
            trade_value = shares * current_price
            cost = trade_value * 0.001
            cash += trade_value - cost
            shares = 0

        # Decrement timer safely
        if shares > 0 and hold_days > 0:
            hold_days -= 1

    final_price = data["Close"].iloc[-1]
    final_value = cash + (shares * final_price)

    return equity_curve, final_value

import math


def calculate_drawdown(equity_curve):
    drawdowns = []
    peak = equity_curve[0]

    for value in equity_curve:
        if value > peak:
            peak = value

        drawdown = (value - peak) / peak
        drawdowns.append(drawdown)

    return drawdowns





def calculate_sharpe(equity_curve):
    returns = []

    for i in range(1, len(equity_curve)):
        daily_return = (equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1]
        returns.append(daily_return)

    if len(returns) == 0:
        return 0

    mean_return = sum(returns) / len(returns)

    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return 0

    sharpe = (mean_return / std_dev) * math.sqrt(252)

    return sharpe








if __name__ == "__main__":
    ticker = "SPY"
    data = get_recent_data(ticker)

    print(f"\nRunning Strategy Comparison on {ticker}\n")

    # Run Strategies
    ma_equity, ma_final = run_backtest(data, analyze_market)
    ma_sharpe = calculate_sharpe(ma_equity)

    mr_equity, mr_final = run_backtest(data, mean_reversion_strategy)
    mr_sharpe = calculate_sharpe(mr_equity)

    adaptive_equity, adaptive_final = run_backtest(data, adaptive_strategy)
    adaptive_sharpe = calculate_sharpe(adaptive_equity)



    # Buy & Hold
    first_price = data["Close"].iloc[0]
    last_price = data["Close"].iloc[-1]
    bh_shares = 10000 / first_price
    bh_final = bh_shares * last_price

    bh_equity = []
    for i in range(20, len(data)):
        price = data["Close"].iloc[i]
        bh_equity.append(bh_shares * price)

        ma_drawdown = calculate_drawdown(ma_equity)
        mr_drawdown = calculate_drawdown(mr_equity)
        adaptive_drawdown = calculate_drawdown(adaptive_equity)
        bh_drawdown = calculate_drawdown(bh_equity)

    bh_sharpe = calculate_sharpe(bh_equity)

    # Print Results
    print("Moving Average Final Value:", round(ma_final, 2))
    print("Moving Average Sharpe:", round(ma_sharpe, 2))
    print()

    print("Mean Reversion Final Value:", round(mr_final, 2))
    print("Mean Reversion Sharpe:", round(mr_sharpe, 2))
    print()

    print("Adaptive Strategy Final Value:", round(adaptive_final, 2))
    print("Adaptive Strategy Sharpe:", round(adaptive_sharpe, 2))
    print()

    print("Buy & Hold Final Value:", round(bh_final, 2))
    print("Buy & Hold Sharpe:", round(bh_sharpe, 2))

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # --- Equity Curves ---
    ax1.plot(ma_equity, label="Moving Average", linewidth=3, color="blue")
    ax1.plot(mr_equity, label="Mean Reversion", linewidth=3, color="red", linestyle="--")
    ax1.plot(adaptive_equity, label="Adaptive Strategy", linewidth=3, color="purple")
    ax1.plot(bh_equity, label="Buy & Hold", linewidth=3, color="green")

    ax1.axhline(y=10000, linestyle="--", linewidth=2, color="black", alpha=0.6)

    ax1.set_title("Equity Curve")
    ax1.set_ylabel("Portfolio Value")
    ax1.legend()
    ax1.grid(True)

    # --- Drawdown Curves ---
    ax2.plot(ma_drawdown, label="MA Drawdown", linewidth=2, color="blue")
    ax2.plot(mr_drawdown, label="MR Drawdown", linewidth=2, color="red", linestyle="--")
    ax2.plot(adaptive_drawdown, label="Adaptive Drawdown", linewidth=2, color="purple")
    ax2.plot(bh_drawdown, label="Buy & Hold Drawdown", linewidth=2, color="green")

    ax2.set_title("Drawdown")
    ax2.set_ylabel("Drawdown %")
    ax2.set_xlabel("Days")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()