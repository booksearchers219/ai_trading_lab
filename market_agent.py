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

def run_backtest(data, strategy_function):
    cash = 10000
    shares = 0
    equity_curve = []
    hold_days = 0

    for i in range(20, len(data)):
        recent_data = data.iloc[:i]
        decision = strategy_function(recent_data)
        current_price = data["Close"].iloc[i]

        # Record portfolio value
        portfolio_value = cash + (shares * current_price)
        equity_curve.append(portfolio_value)

        # BUY
        if decision == "BUY" and shares == 0:
            investment_amount = cash * 0.5
            shares = int(investment_amount / current_price)

            if shares > 0:
                cash -= shares * current_price
                hold_days = 5

        # SELL from strategy signal
        elif decision == "SELL" and shares > 0:
            cash += shares * current_price
            shares = 0
            hold_days = 0

        # Timed exit (for mean reversion)
        elif shares > 0 and hold_days == 0:
            cash += shares * current_price
            shares = 0

        # Decrement holding timer
        if shares > 0:
            hold_days -= 1

    final_price = data["Close"].iloc[-1]
    final_value = cash + (shares * final_price)

    return equity_curve, final_value
if __name__ == "__main__":
    ticker = "SPY"
    data = get_recent_data(ticker)

    print(f"\nRunning Strategy Comparison on {ticker}\n")

    # Strategy 1: Moving Average
    ma_equity, ma_final = run_backtest(data, analyze_market)
    mr_equity, mr_final = run_backtest(data, mean_reversion_strategy)


    # Strategy 2: Buy & Hold
    first_price = data["Close"].iloc[0]
    last_price = data["Close"].iloc[-1]
    bh_shares = 10000 / first_price
    bh_final = bh_shares * last_price

    # Build Buy & Hold Equity Curve
    bh_equity = []
    for price in data["Close"].iloc[20:]:
        bh_equity.append(bh_shares * price)

    print("Moving Average Final Value:", round(ma_final, 2))
    print("Mean Reversion Final Value:", round(mr_final, 2))
    print("Buy & Hold Final Value:", round(bh_final, 2))

    plt.figure()
    plt.plot(ma_equity, label="Moving Average")
    plt.plot(mr_equity, label="Mean Reversion")
    plt.plot(bh_equity, label="Buy & Hold")
    plt.axhline(y=10000, linestyle="--", label="Starting Value")
    plt.title("Strategy Comparison")
    plt.xlabel("Days")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.show()

   
   
   
