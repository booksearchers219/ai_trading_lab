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
from strategies import regime_history



MAX_POSITIONS = 6
MAX_RISK_PER_TRADE = 0.05
MAX_TICKER_ALLOCATION = 0.20
STOP_LOSS_PCT = 0.05
TRAILING_STOP_PCT = 0.05
SIGNAL_CONFIRM_CYCLES = 3

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

    cooldowns = {}
    COOLDOWN_SECONDS = 600  # 10 minutes

    high_prices = {}
    signal_history = {}

    data_refresh_time = 0
    DATA_REFRESH_SECONDS = 300

    data_cache = {}

    while True:

        os.system("clear")

        print("========== AI TRADING LAB ==========\n")
        print("Scanning market...\n")

        prices = {}


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

                    if price == price:  # ignore NaN
                        prices[ticker] = float(price)

                except Exception:
                    continue

        # refresh strategy data only every few minutes
        current_time = time.time()

        if current_time - data_refresh_time > DATA_REFRESH_SECONDS:

            for ticker in SCAN_UNIVERSE:

                try:
                    data_cache[ticker] = get_recent_data(ticker, 1)
                except Exception:
                    continue

            data_refresh_time = current_time

        print("MARKET")
        print("------")

        for t in SCAN_UNIVERSE:
            p = prices.get(t)

            if p is None or p != p:
                print(f"{t:<6} data")
            else:
                print(f"{t:<6} {p:8.2f}")

        print()



        signal_list = []


        for ticker in prices:

            data = data_cache.get(ticker)
            if data is None:
                continue

            regime = regime_history(data)[-1]

            print(f"{ticker} regime: {regime}")

            signals = {}

            if regime == "TRENDING":
                signals["MA"] = analyze_market(data)
                signals["AD"] = adaptive_strategy(data, adaptive_state)

            elif regime == "SIDEWAYS":
                signals["MR"] = mean_reversion_strategy(data)
                signals["AD"] = adaptive_strategy(data, adaptive_state)

            else:
                signals["AD"] = adaptive_strategy(data, adaptive_state)

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

        print("SIGNALS")
        print("-------")

        if not signal_list:
            print("None")
        else:
            for strat, signal, ticker, vote_strength in signal_list:
                count = signal_history.get((ticker, signal), 0)

                print(f"{ticker:<6} {signal:<4} votes:{vote_strength} confirm:{count}")

        # --- signal confirmation tracking ---

        active_keys = {(ticker, signal) for _, signal, ticker, _ in signal_list}

        # remove stale signals
        for key in list(signal_history.keys()):
            if key not in active_keys:
                signal_history.pop(key)

        confirmed_signals = []

        for strat, signal, ticker, vote_strength in signal_list:

            key = (ticker, signal)

            signal_history[key] = signal_history.get(key, 0) + 1

            if signal_history[key] >= SIGNAL_CONFIRM_CYCLES:
                confirmed_signals.append((strat, signal, ticker, vote_strength))

        for strat, signal, ticker, vote_strength in confirmed_signals:

            now = time.time()

            if ticker in cooldowns:
                if now - cooldowns[ticker] < COOLDOWN_SECONDS:
                    continue

            price = prices.get(ticker)

            if price is None or price != price:  # skip NaN
                continue

            held = portfolio.positions.get(ticker, 0)

            # update high watermark
            if ticker in portfolio.positions:
                prev_high = high_prices.get(ticker, price)
                high_prices[ticker] = max(prev_high, price)

            # trailing stop check


            if held > 0:

                high_price = high_prices.get(ticker, price)
                trailing_stop = high_price * (1 - TRAILING_STOP_PCT)

                if price <= trailing_stop:
                    print(f"TRAILING STOP triggered for {ticker} @ {round(price, 2)}")
                    portfolio.sell(ticker, price, held)
                    log_trade("TRAIL", ticker, "SELL", price, held)
                    cooldowns[ticker] = time.time()
                    high_prices.pop(ticker, None)
                    continue


            # stop-loss check

            if held > 0:
                entry_price = portfolio.entry_prices.get(ticker, 0)
                stop_price = entry_price * (1 - STOP_LOSS_PCT)

                if price <= stop_price:
                    print(f"STOP LOSS triggered for {ticker} @ {round(price, 2)}")
                    portfolio.sell(ticker, price, held)
                    log_trade("STOP", ticker, "SELL", price, held)
                    cooldowns[ticker] = time.time()
                    high_prices.pop(ticker, None)
                    continue

            portfolio_value = portfolio.total_value(prices)

            current_position = portfolio.positions.get(ticker, 0)
            current_value = current_position * price

            max_allowed = portfolio_value * MAX_TICKER_ALLOCATION

            confidence = vote_strength / 3
            risk_amount = portfolio_value * MAX_RISK_PER_TRADE * confidence

            shares = int(risk_amount / price)

            open_positions = len(portfolio.positions)



            if (
                    signal == "BUY"
                    and shares > 0
                    and held == 0
                    and open_positions < MAX_POSITIONS
                    and current_value < max_allowed
            ):

                print(f"{strat} BUY {shares} {ticker} @ {round(price, 2)}")
                portfolio.buy(ticker, price, shares)
                high_prices[ticker] = price
                log_trade("COUNCIL", ticker, "BUY", price, shares)
                generate_trade_chart(ticker)
                cooldowns[ticker] = time.time()



            elif signal == "SELL" and held > 0:
                print(f"{strat} SELL {held} {ticker} @ {round(price, 2)}")
                portfolio.sell(ticker, price, held)
                log_trade("COUNCIL", ticker, "SELL", price, held)
                cooldowns[ticker] = time.time()
                high_prices.pop(ticker, None)

        time.sleep(2)

        if not prices:
            print("\nNo market data this cycle.")
            time.sleep(60)
            continue

        value = portfolio.total_value(prices)

        print("\nPORTFOLIO")
        print("---------")
        print(f"Value: ${value:,.2f}")

        shares = sum(portfolio.positions.values())

        if shares > 0:
            status = "LONG"
        elif shares < 0:
            status = "SHORT"
        else:
            status = "CASH"

        print(f"Status: {status}")

        if portfolio.positions:
            print("\nPOSITIONS")
            print("---------")
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
