import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math
import matplotlib.ticker as mtick
import csv
import pandas as pd
import numpy as np

def get_sp500_tickers():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    tables = pd.read_html(
        url,
        storage_options={
            "User-Agent": "Mozilla/5.0"
        }
    )

    df = tables[0]

    tickers = df["Symbol"].tolist()

    # Fix tickers like BRK.B -> BRK-B for Yahoo Finance
    tickers = [t.replace(".", "-") for t in tickers]

    return tickers

plt.style.use("ggplot")

def get_recent_data(ticker, months):
    stock = yf.Ticker(ticker)

    end_date = datetime.today()
    start_date = end_date - timedelta(days=months * 30)

    data = stock.history(start=start_date, end=end_date)

    print("\nBacktest Window")
    print(start_date.strftime("%Y-%m-%d"), "→", end_date.strftime("%Y-%m-%d"))

    return data


def analyze_market(data, short_window=5, long_window=20):
    closes = data["Close"]

    if len(closes) < 20:
        return "HOLD"

    short_ma = closes.rolling(window=short_window).mean().iloc[-1]
    long_ma = closes.rolling(window=long_window).mean().iloc[-1]

    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    else:
        return "HOLD"


def mean_reversion_strategy(data):
    closes = data["Close"]

    if len(closes) < 6:
        return "HOLD"

    five_day_return = (closes.iloc[-1] - closes.iloc[-6]) / closes.iloc[-6]

    if five_day_return < -0.03:
        return "BUY"
    else:
        return "HOLD"


def detect_regime(data):
    closes = data["Close"]

    if len(closes) < 50:
        return "SIDEWAYS"

    ma20 = closes.rolling(window=20).mean().iloc[-1]
    ma50 = closes.rolling(window=50).mean().iloc[-1]

    returns = closes.pct_change()
    recent_vol = returns.rolling(window=20).std().iloc[-1]

    vol_threshold = 0.02

    if ma20 > ma50 and recent_vol > vol_threshold:
        return "TRENDING"
    else:
        return "SIDEWAYS"


def adaptive_strategy(data, state):
    regime = detect_regime(data)

    if "current_regime" not in state:
        state["current_regime"] = regime
        state["regime_count"] = 1
    else:
        if regime == state["current_regime"]:
            state["regime_count"] += 1
        else:
            state["regime_count"] = 1

        if state["regime_count"] >= 5:
            state["current_regime"] = regime

    if state["current_regime"] == "TRENDING":
        return analyze_market(data)
    else:
        return mean_reversion_strategy(data)


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

        # BUY
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

        # SELL from signal
        elif decision == "SELL" and shares > 0:

            trade_value = shares * current_price
            cost = trade_value * 0.001

            profit = (current_price - entry_price) * shares
            trade_profits.append(profit)

            cash += trade_value - cost
            shares = 0
            hold_days = 0

            sell_points.append(len(equity_curve))

        # Timed exit
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


if __name__ == "__main__":

    default_ticker = "TSLA"
    all_tickers = get_sp500_tickers()

    TEST_LIMIT = 100  # change to 20 or None for full list

    if TEST_LIMIT:
        ticker_list = all_tickers[:TEST_LIMIT]
    else:
        ticker_list = all_tickers

    user_input = input(f'Current stock is "{default_ticker}". Press Enter to keep it, or type a new ticker: ')

    print("\nSelect backtest window:")
    print("1) 6 months")
    print("2) 1 year")
    print("3) 2 years")

    choice = input("Enter choice (default = 1): ").strip()

    if choice == "2":
        months = 12
    elif choice == "3":
        months = 24
    else:
        months = 6

    if user_input.strip() == "":
        ticker = default_ticker
    else:
        ticker = user_input.strip().upper()

    print("\nRun multi-ticker test? (y/n)")
    batch_mode = input("> ").lower()

    if batch_mode == "y":

        results = []
        heatmap_data = []
        heatmap_labels = []

        # Leaderboard counters
        ma_wins = 0
        mr_wins = 0
        ad_wins = 0

        for i, ticker in enumerate(ticker_list, 1):
            print(f"\nTesting {ticker} ({i}/{len(ticker_list)})")

            data = get_recent_data(ticker, months)

            ma_equity, ma_final, _, _, ma_profits = run_backtest(data, analyze_market)
            mr_equity, mr_final, _, _, mr_profits = run_backtest(data, mean_reversion_strategy)
            ad_equity, ad_final, _, _, ad_profits = run_backtest(data, adaptive_strategy)

            ma_sharpe = calculate_sharpe(ma_equity)
            mr_sharpe = calculate_sharpe(mr_equity)
            ad_sharpe = calculate_sharpe(ad_equity)

            results.append((ticker, ma_final, mr_final, ad_final, ma_sharpe, mr_sharpe, ad_sharpe))

        # Save results to CSV
        with open("strategy_results.csv", "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Ticker",
                "MA_Final",
                "MR_Final",
                "AD_Final",
                "MA_Sharpe",
                "MR_Sharpe",
                "AD_Sharpe"
            ])

            for row in results:
                writer.writerow(row)

        print("\nResults saved to strategy_results.csv\n")

        # Sort results by best Sharpe ratio
        results.sort(key=lambda x: max(x[4], x[5], x[6]), reverse=True)

        top_results = results[:20]

        print("\nStrategy Results Summary\n")

        for r in top_results:

            best_value = max(r[1], r[2], r[3])

            if best_value == r[1]:
                winner = "MA"
                ma_wins += 1
            elif best_value == r[2]:
                winner = "MR"
                mr_wins += 1
            else:
                winner = "AD"
                ad_wins += 1

            row = [0, 0, 0]

            if winner == "MA":
                row[0] = 1
            elif winner == "MR":
                row[1] = 1
            else:
                row[2] = 1

            heatmap_data.append(row)
            heatmap_labels.append(r[0])

            print(
                f"{r[0]:<5} | "
                f"MA: {'$' + format(r[1], ',.2f'):>12} "
                f"MR: {'$' + format(r[2], ',.2f'):>12} "
                f"AD: {'$' + format(r[3], ',.2f'):>12} "
                f"| Winner: {winner}"
            )

        print("\nStrategy Leaderboard\n")

        print(f"{'Moving Average':<18}: {ma_wins}")
        print(f"{'Mean Reversion':<18}: {mr_wins}")
        print(f"{'Adaptive':<18}: {ad_wins}")

        top_n = 20

        heatmap_array = np.array(heatmap_data[:top_n])
        heatmap_labels = heatmap_labels[:top_n]

        plt.figure(figsize=(8, 10))
        plt.imshow(heatmap_array, cmap="coolwarm", aspect="auto")

        plt.yticks(range(len(heatmap_labels)), heatmap_labels)
        plt.xticks([0, 1, 2], ["MA", "MR", "AD"])

        plt.title("Strategy Winners Heatmap", fontsize=16, fontweight="bold")
        plt.xlabel("Strategy")
        plt.ylabel("Ticker")

        plt.colorbar(label="Winner")

        plt.tight_layout()
        plt.show()

        exit()


    if user_input.strip() == "":
        ticker = default_ticker
    else:
        ticker = user_input.strip().upper()

    data = get_recent_data(ticker, months)

    print(f"\nRunning Strategy Comparison on {ticker}\n")

    # Run strategies
    ma_equity, ma_final, ma_buys, ma_sells, ma_profits = run_backtest(data, analyze_market)
    mr_equity, mr_final, mr_buys, mr_sells, mr_profits = run_backtest(data, mean_reversion_strategy)
    adaptive_equity, adaptive_final, ad_buys, ad_sells, ad_profits = run_backtest(data, adaptive_strategy)

    ma_sharpe = calculate_sharpe(ma_equity)
    mr_sharpe = calculate_sharpe(mr_equity)
    adaptive_sharpe = calculate_sharpe(adaptive_equity)

    # Buy & Hold
    first_price = data["Close"].iloc[0]
    last_price = data["Close"].iloc[-1]

    bh_shares = 10000 / first_price
    bh_final = bh_shares * last_price

    bh_equity = []
    for i in range(50, len(data)):
        price = data["Close"].iloc[i]
        bh_equity.append(bh_shares * price)

    bh_sharpe = calculate_sharpe(bh_equity)

    print("\nRun Moving Average parameter sweep? (y/n)")
    sweep = input("> ").lower()

    if sweep == "y":

        short_windows = range(5, 31, 5)
        long_windows = range(20, 201, 20)

        results = []
        top_results = []

        for s in short_windows:
            for l in long_windows:

                if s >= l:
                    continue


                def ma_strategy(data, short=s, long=l):
                    return analyze_market(data, short, long)


                equity, final_value, _, _, _ = run_backtest(data, ma_strategy)
                sharpe = calculate_sharpe(equity)

                results.append((s, l, final_value, sharpe))
                top_results.append((s, l, final_value, sharpe))



        print("\nMA Parameter Sweep Results\n")

        results.sort(key=lambda x: x[3], reverse=True)
        top_results.sort(key=lambda x: x[3], reverse=True)

        for r in results:
            short_ma = r[0]
            long_ma = r[1]
            final_val = r[2]
            sharpe = r[3]

            print(
                f"MA {short_ma}/{long_ma} | "
                f"Final: {round(final_val, 2):>10} | "
                f"Sharpe: {round(sharpe, 2):>6}"
            )

            print("\nTop 10 Moving Average Strategies\n")

            for r in top_results[:10]:
                print(
                    f"MA {r[0]}/{r[1]} | "
                    f"Final: ${r[2]:,.2f} | "
                    f"Sharpe: {r[3]:.2f}"
                )

    # Drawdowns
    ma_drawdown = calculate_drawdown(ma_equity)
    mr_drawdown = calculate_drawdown(mr_equity)
    adaptive_drawdown = calculate_drawdown(adaptive_equity)
    bh_drawdown = calculate_drawdown(bh_equity)
    ma_max_dd = max_drawdown(ma_drawdown)
    mr_max_dd = max_drawdown(mr_drawdown)
    adaptive_max_dd = max_drawdown(adaptive_drawdown)
    bh_max_dd = max_drawdown(bh_drawdown)

    # Trade stats
    ma_wins, ma_losses, ma_wr, ma_avg = trade_statistics(ma_profits)
    mr_wins, mr_losses, mr_wr, mr_avg = trade_statistics(mr_profits)
    ad_wins, ad_losses, ad_wr, ad_avg = trade_statistics(ad_profits)
    ma_pf = profit_factor(ma_profits)
    mr_pf = profit_factor(mr_profits)
    ad_pf = profit_factor(ad_profits)

    print("\nMoving Average")
    print("Trades:", len(ma_profits))
    print("Win Rate:", round(ma_wr * 100, 1), "%")
    print("Avg Trade:", round(ma_avg, 2))
    print("Profit Factor:", round(ma_pf, 2))

    print("\nMean Reversion")
    print("Trades:", len(mr_profits))
    print("Win Rate:", round(mr_wr * 100, 1), "%")
    print("Avg Trade:", round(mr_avg, 2))
    print("Profit Factor:", round(mr_pf, 2))

    print("\nAdaptive")
    print("Trades:", len(ad_profits))
    print("Win Rate:", round(ad_wr * 100, 1), "%")
    print("Avg Trade:", round(ad_avg, 2))
    print("Profit Factor:", round(ad_pf, 2))

    print("\nBuy & Hold Final Value:", round(bh_final, 2))
    print("Buy & Hold Sharpe:", round(bh_sharpe, 2))
    print("Buy & Hold Max Drawdown:", round(bh_max_dd * 100, 2), "%")

   # print("\nTrade Statistics")

    print("\nMoving Average")
    print("Trades:", len(ma_profits))
    print("Win Rate:", round(ma_wr * 100, 1), "%")
    print("Avg Trade:", round(ma_avg, 2))

    print("\nMean Reversion")
    print("Trades:", len(mr_profits))
    print("Win Rate:", round(mr_wr * 100, 1), "%")
    print("Avg Trade:", round(mr_avg, 2))

    print("\nAdaptive")
    print("Trades:", len(ad_profits))
    print("Win Rate:", round(ad_wr * 100, 1), "%")
    print("Avg Trade:", round(ad_avg, 2))

    # Plot
    fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    price_series = data["Close"].iloc[50:].reset_index(drop=True)

    ax0.plot(price_series, color="black", linewidth=2, label="Price")

    # Moving Average trades on price
    ax0.scatter(ma_buys, [price_series[i] for i in ma_buys], marker="^", color="green", s=80)
    ax0.scatter(ma_sells, [price_series[i] for i in ma_sells], marker="v", color="red", s=80)

    # Mean Reversion trades
    ax0.scatter(mr_buys, [price_series[i] for i in mr_buys], marker="^", color="orange", s=80)
    ax0.scatter(mr_sells, [price_series[i] for i in mr_sells], marker="v", color="darkorange", s=80)

    # Adaptive trades
    ax0.scatter(ad_buys, [price_series[i] for i in ad_buys], marker="^", color="purple", s=80)
    ax0.scatter(ad_sells, [price_series[i] for i in ad_sells], marker="v", color="magenta", s=80)
    ax0.set_title(f"{ticker} Price", fontsize=15, fontweight="bold")
    ax0.legend(fontsize=12)
    ax0.grid(True)

    ax1.plot(ma_equity, label="Moving Average", linewidth=3)
    ax1.plot(mr_equity, label="Mean Reversion", linewidth=3, linestyle="--")
    ax1.plot(adaptive_equity, label="Adaptive", linewidth=3)
    ax1.plot(bh_equity, label="Buy & Hold", linewidth=3)

    ax1.axhline(y=10000, linestyle="--", color="black")

    # Moving Average trades
    ax1.scatter(ma_buys, [ma_equity[i] for i in ma_buys], marker="^", color="green", s=80)
    ax1.scatter(ma_sells, [ma_equity[i] for i in ma_sells], marker="v", color="red", s=80)

    # Mean Reversion trades
    ax1.scatter(mr_buys, [mr_equity[i] for i in mr_buys], marker="^", color="orange", s=80)
    ax1.scatter(mr_sells, [mr_equity[i] for i in mr_sells], marker="v", color="darkorange", s=80)

    # Adaptive trades
    ax1.scatter(ad_buys, [adaptive_equity[i] for i in ad_buys], marker="^", color="purple", s=80)
    ax1.scatter(ad_sells, [adaptive_equity[i] for i in ad_sells], marker="v", color="magenta", s=80)

    ax1.set_title(f"{ticker} Strategy Comparison", fontsize=16, fontweight="bold")
    ax1.legend(fontsize=12)
    ax1.grid(True)
    ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    ax2.plot(ma_drawdown, label="MA Drawdown", linewidth=3, color="blue")
    ax2.plot(mr_drawdown, label="MR Drawdown", linewidth=3, color="red", linestyle="--")
    ax2.plot(adaptive_drawdown, label="Adaptive Drawdown", linewidth=3, color="purple")
    ax2.plot(bh_drawdown, label="Buy & Hold Drawdown", linewidth=3, color="green")

    ax2.axhline(y=0, color="black", linewidth=2, linestyle="--", alpha=0.5)

    ax2.set_title("Drawdown", fontsize=15, fontweight="bold")
    ax2.legend(fontsize=12)
    ax2.grid(True)

    fig.suptitle(f"{ticker} Strategy Backtest", fontsize=18, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()