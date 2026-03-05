import math


def run_backtest(data, strategy_function):

    cash = 10000
    shares = 0
    entry_price = None

    equity_curve = []
    buy_points = []
    sell_points = []
    trade_profits = []

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

        if decision == "BUY" and shares == 0:

            investment_amount = cash * 0.5
            shares = int(investment_amount / current_price)

            if shares > 0:

                trade_value = shares * current_price
                cost = trade_value * 0.001

                cash -= trade_value + cost
                entry_price = current_price

                hold_days = 5
                buy_points.append(len(equity_curve))

        elif decision == "SELL" and shares > 0:

            trade_value = shares * current_price
            cost = trade_value * 0.001

            profit = (current_price - entry_price) * shares
            trade_profits.append(profit)

            cash += trade_value - cost
            shares = 0
            hold_days = 0

            sell_points.append(len(equity_curve))

        elif shares > 0 and hold_days == 0:

            trade_value = shares * current_price
            cost = trade_value * 0.001

            profit = (current_price - entry_price) * shares
            trade_profits.append(profit)

            cash += trade_value - cost
            shares = 0

        if shares > 0 and hold_days > 0:
            hold_days -= 1

    final_price = data["Close"].iloc[-1]
    final_value = cash + (shares * final_price)

    return equity_curve, final_value, buy_points, sell_points, trade_profits


def calculate_drawdown(equity_curve):

    drawdowns = []
    peak = equity_curve[0]

    for value in equity_curve:

        if value > peak:
            peak = value

        drawdown = (value - peak) / peak
        drawdowns.append(drawdown)

    return drawdowns


def max_drawdown(drawdowns):
    return min(drawdowns)


def safe_points(points, series):

    valid = [i for i in points if i < len(series)]
    values = [series[i] for i in valid]

    return valid, values


def calculate_sharpe(equity_curve):

    returns = []

    for i in range(1, len(equity_curve)):
        daily_return = (equity_curve[i] - equity_curve[i - 1]) / equity_curve[i - 1]
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


def trade_statistics(profits):

    if len(profits) == 0:
        return 0, 0, 0, 0

    wins = sum(1 for p in profits if p > 0)
    losses = sum(1 for p in profits if p <= 0)

    win_rate = wins / len(profits)
    avg_profit = sum(profits) / len(profits)

    return wins, losses, win_rate, avg_profit


def profit_factor(profits):

    gross_profit = sum(p for p in profits if p > 0)
    gross_loss = abs(sum(p for p in profits if p < 0))

    if gross_loss == 0:
        return 0

    return gross_profit / gross_loss
