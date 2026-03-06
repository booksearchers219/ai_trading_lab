import time
import os
import yfinance as yf

from portfolio import Portfolio
from strategies import analyze_market, mean_reversion_strategy, adaptive_strategy
from data_utils import get_recent_data

SCAN_UNIVERSE = [
    "NVDA","AMD","TSLA","META","AAPL",
    "MSFT","GOOGL","AMZN","AVGO","NFLX"
]


def run_live_simulation():
    portfolios = {
        "MA": Portfolio(10000),
        "MR": Portfolio(10000),
        "AD": Portfolio(10000)
    }

    adaptive_state = {}

    while True:



        prices = {}
        data_cache = {}

        for ticker in SCAN_UNIVERSE:
            ticker_obj = yf.Ticker(ticker)

            live_data = ticker_obj.history(period="1d", interval="1m")

            price = live_data["Close"].iloc[-1]

            prices[ticker] = price

            data_cache[ticker] = get_recent_data(ticker, 1)

        print("\nScanning market...")

        for t in SCAN_UNIVERSE:
            if t in prices:
                print(f"{t:<6} {round(prices[t], 2)}")

        signal_list = []

        best_score = 0
        best_signal = None
        best_ticker = None
        best_strategy = None

        for ticker in SCAN_UNIVERSE:
            data = data_cache[ticker]
            signals = {
                "MA": analyze_market(data),
                "MR": mean_reversion_strategy(data),
                "AD": adaptive_strategy(data, adaptive_state)
            }

            for strat, signal in signals.items():

                if signal == "BUY":

                    signal_list.append((strat, ticker))

                    # basic scoring system
                    score = 1

                    # mean reversion gets bonus
                    if strat == "MR":
                        score += 1

                    if score > best_score:
                        best_score = score
                        best_signal = signal
                        best_ticker = ticker
                        best_strategy = strat

        print("\nSignals detected")
        print("----------------")

        if not signal_list:
            print("None")
        else:
            for strat, ticker in signal_list:
                print(f"{strat:<3} {ticker}")

        if best_signal:

            portfolio = portfolios[best_strategy]

            price = prices[best_ticker]

            portfolio_value = portfolio.total_value(prices)

            risk_amount = portfolio_value * 0.10

            shares = int(risk_amount / price)

            open_positions = len(portfolio.positions)

            held = portfolio.positions.get(best_ticker, 0)

            # BUY if we don't own it
            if best_signal == "BUY" and shares > 0 and held == 0 and open_positions < 3:
                print(f"{best_strategy} BUY {shares} {best_ticker} @ {round(price, 2)}")
                portfolio.buy(best_ticker, price, shares)

            # SELL if we already own it
            elif best_signal == "SELL" and held > 0:
                print(f"{best_strategy} SELL {held} {best_ticker} @ {round(price, 2)}")
                portfolio.sell(best_ticker, price, held)

        time.sleep(2)
        # os.system("clear")

        values = {}

        for name, portfolio in portfolios.items():

            values[name] = portfolio.total_value(prices)

            shares = sum(portfolio.positions.values())

            if shares > 0:
                status = "LONG"
            elif shares < 0:
                status = "SHORT"
            else:
                status = "CASH"

            print(f"{name:<3}  {status:<5}  shares:{shares:<4}  value:${values[name]:,.2f}")

        print("\nLIVE STRATEGY LEADERBOARD\n")

        if best_ticker:
            print(f"{best_ticker}: {round(prices[best_ticker], 2)}")

        print("-" * 40)

        leader = max(values, key=values.get)

        print(f"\nLeader: {leader}")

        time.sleep(60)

if __name__ == "__main__":
    run_live_simulation()