import time
import os
import yfinance as yf

from portfolio import Portfolio
from strategies import analyze_market, mean_reversion_strategy, adaptive_strategy
from portfolio_state import save_state, load_state
from data_utils import get_recent_data
from trade_logger import log_trade
from trade_charts import generate_trade_chart
from equity_logger import log_equity
from equity_chart import generate_equity_chart



MAX_POSITIONS = 6
MAX_RISK_PER_TRADE = 0.05

SCAN_UNIVERSE = [
    "NVDA", "AMD", "TSLA", "META", "AAPL",
    "MSFT", "GOOGL", "AMZN", "AVGO", "NFLX"
]


def run_live_simulation():
    state = load_state()

    if state:
        print("Resuming previous session...")
        portfolio = Portfolio(state["cash"])
        portfolio.positions = state["positions"]

    else:
        print("Starting new session...")
        portfolio = Portfolio(30000)

    adaptive_state = {}

    while True:

        prices = {}
        data_cache = {}

        tickers = " ".join(SCAN_UNIVERSE)

        try:
            live_data = yf.download(
                tickers,
                period="1d",
                interval="1m",
                group_by="ticker",
                progress=False
            )
        except Exception:
            live_data = None

        if live_data is not None:

            for ticker in SCAN_UNIVERSE:

                try:
                    price = live_data[ticker]["Close"].iloc[-1]
                    prices[ticker] = float(price)
                except Exception:
                    continue

                data_cache[ticker] = get_recent_data(ticker, 1)
        print("\nScanning market...")

        for t in SCAN_UNIVERSE:
            if t in prices:
                print(f"{t:<6} {round(prices[t], 2)}")

        signal_list = []


        for ticker in prices:

            data = data_cache.get(ticker)
            if data is None:
                continue

            signals = {
                "MA": analyze_market(data),
                "MR": mean_reversion_strategy(data),
                "AD": adaptive_strategy(data, adaptive_state)
            }

            votes = list(signals.values())

            buy_votes = votes.count("BUY")
            sell_votes = votes.count("SELL")

            combined_signal = "HOLD"
            vote_strength = 0

            if buy_votes >= 2:
                combined_signal = "BUY"
                vote_strength = buy_votes

            elif sell_votes >= 2:
                combined_signal = "SELL"
                vote_strength = sell_votes

            if combined_signal in ("BUY", "SELL"):
                signal_list.append(("COUNCIL", combined_signal, ticker, vote_strength))



        print("\nSignals detected")
        print("----------------")

        if not signal_list:
            print("None")
        else:
            for strat, signal, ticker, vote_strength in signal_list:
                print(f"{strat:<3} {signal:<4} {ticker}")

        # ---- INSERT STEP 3 RIGHT HERE ----

        for strat, signal, ticker, vote_strength in signal_list:

            price = prices.get(ticker)

            if price is None:
                continue

            portfolio_value = portfolio.total_value(prices)

            confidence = vote_strength / 3
            risk_amount = portfolio_value * MAX_RISK_PER_TRADE * confidence

            shares = int(risk_amount / price)

            open_positions = len(portfolio.positions)

            held = portfolio.positions.get(ticker, 0)

            if signal == "BUY" and shares > 0 and held == 0 and open_positions < MAX_POSITIONS:
                print(f"{strat} BUY {shares} {ticker} @ {round(price, 2)}")
                portfolio.buy(ticker, price, shares)
                log_trade("COUNCIL", ticker, "BUY", price, shares)
                generate_trade_chart(ticker)


            elif signal == "SELL" and held > 0:
                print(f"{strat} SELL {held} {ticker} @ {round(price, 2)}")
                portfolio.sell(ticker, price, held)
                log_trade("COUNCIL", ticker, "SELL", price, held)

        time.sleep(2)

        value = portfolio.total_value(prices)

        print(f"\nPortfolio Value: ${value:,.2f}")

        shares = sum(portfolio.positions.values())

        if shares > 0:
            status = "LONG"
        elif shares < 0:
            status = "SHORT"
        else:
            status = "CASH"

        print(f"Status: {status}")

        if portfolio.positions:
            print("Holdings:")
            total_pnl = 0

            for ticker, qty in portfolio.positions.items():
                entry_price = portfolio.entry_prices.get(ticker, 0)
                current_price = prices.get(ticker, 0)

                pnl = (current_price - entry_price) * qty
                total_pnl += pnl

                pnl_str = f"+${pnl:,.2f}" if pnl >= 0 else f"-${abs(pnl):,.2f}"

                print(f"   {ticker:<5} {qty:>4}  entry:{entry_price:.2f}  now:{current_price:.2f}  P/L:{pnl_str}")

            print(f"\nUnrealized P/L: ${total_pnl:,.2f}")

        else:
            print("No open positions")

        log_equity({"MA": value, "MR": value, "AD": value})
        generate_equity_chart()



        # Save portfolio state


        save_state({
            "cash": portfolio.cash,
            "positions": portfolio.positions
        })



        time.sleep(60)


if __name__ == "__main__":
    run_live_simulation()
