import os
import time
import yfinance as yf

from data_utils import get_recent_data
from equity_chart import generate_equity_chart
from equity_logger import log_equity
from portfolio import Portfolio
from portfolio_state import save_state, load_state
from strategies import analyze_market, mean_reversion_strategy, adaptive_strategy
from strategies import regime_history
from trade_charts import generate_trade_chart
from trade_logger import log_trade
from leaderboard import print_leaderboard
import math
from datetime import datetime, timedelta
import pytz


MAX_POSITIONS = 6
MAX_RISK_PER_TRADE = 0.05
MAX_TICKER_ALLOCATION = 0.20
STOP_LOSS_PCT = 0.05
TRAILING_STOP_PCT = 0.05
SIGNAL_CONFIRM_CYCLES = 3


SCAN_UNIVERSE = [
    "SPY",
    "NVDA","AMD","TSLA","META","AAPL",
    "MSFT","GOOGL","AMZN","AVGO","NFLX"
]


def run_live_simulation():

    strategy_equity = {
        "MA": 30000,
        "MR": 30000,
        "AD": 30000
    }

    state = load_state()

    if state:
        print("Resuming previous session...")
        portfolio = Portfolio(state["cash"])
        portfolio.positions = state["positions"]
        portfolio.entry_prices = state.get("entry_prices", {})
    else:
        print("Starting new session...")
        portfolio = Portfolio(30000)

    adaptive_state = {}

    cooldowns = {}
    COOLDOWN_SECONDS = 600

    high_prices = {}
    signal_history = {}

    data_refresh_time = 0
    DATA_REFRESH_SECONDS = 300

    data_cache = {}

    while True:

        os.system("clear")

        print("========== AI TRADING LAB ==========")

        eastern = pytz.timezone("US/Eastern")
        now = datetime.now(eastern)

        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

        if market_open <= now <= market_close:
            market_status = "OPEN"
            remaining = market_close - now
        else:
            market_status = "CLOSED"
            if now < market_open:
                remaining = market_open - now
            else:
                tomorrow = now + timedelta(days=1)
                market_open = tomorrow.replace(hour=9, minute=30, second=0, microsecond=0)
                remaining = market_open - now

        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60

        print("Time:", now.strftime("%H:%M:%S"), "ET")
        print(f"Market: {market_status}  ({hours}h {minutes}m remaining)")
        print()

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

                    # Try structure: live_data[ticker]["Close"]
                    if ticker in live_data:
                        price = live_data[ticker]["Close"].iloc[-1]

                    # Try structure: live_data["Close"][ticker]
                    else:
                        price = live_data["Close"][ticker].iloc[-1]

                    if not math.isnan(price):
                        prices[ticker] = float(price)

                except Exception:
                    continue


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

        row = ""

        for t in SCAN_UNIVERSE:

            p = prices.get(t)

            if p is None or p != p:
                cell = f"{t}:data"
            else:
                cell = f"{t}:{p:.2f}"

            row += f"{cell:<15}"

        print(row)

        print()


        signal_list = []
        pending_signals = []
        confirmed_signals = []


        market_regime = "UNKNOWN"

        spy_data = data_cache.get("SPY")

        if spy_data is not None:
            try:
                market_regime = regime_history(spy_data)[-1]
            except Exception:
                market_regime = "UNKNOWN"


        risk_mode = {
            "TRENDING":"AGGRESSIVE",
            "SIDEWAYS":"NORMAL",
            "UNKNOWN":"DEFENSIVE"
        }.get(market_regime,"DEFENSIVE")

        print(f"\nMARKET REGIME: {market_regime}")
        print(f"RISK MODE: {risk_mode}\n")

        regime_row = ""

        for ticker in prices:

            if ticker == "SPY":
                continue

            data = data_cache.get(ticker)
            if data is None:
                continue

            regime = regime_history(data)[-1]
            regime_row += f"{ticker}:{regime:<10}"

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


            if combined_signal in ("BUY","SELL"):
                signal_list.append(("COUNCIL",combined_signal,ticker,vote_strength))



        active_keys = {(ticker,signal) for _,signal,ticker,_ in signal_list}

        for key in list(signal_history.keys()):
            if key not in active_keys:
                signal_history.pop(key)

        print(regime_row)

        for strat,signal,ticker,vote_strength in signal_list:

            key = (ticker,signal)

            signal_history[key] = signal_history.get(key,0)+1

            if signal_history[key] >= SIGNAL_CONFIRM_CYCLES:
                confirmed_signals.append((strat,signal,ticker,vote_strength))
            else:
                pending_signals.append((strat,signal,ticker,vote_strength))


        print("\nPENDING SIGNALS")
        print("----------------")

        if not pending_signals:
            print("None")

        for strat,signal,ticker,vote_strength in pending_signals:
            count = signal_history.get((ticker,signal),0)
            print(f"{ticker:<6} {signal:<4} votes:{vote_strength} confirm:{count}/{SIGNAL_CONFIRM_CYCLES}")


        print("\nCONFIRMED SIGNALS")
        print("-----------------")

        if not confirmed_signals:
            print("None")

        for strat,signal,ticker,vote_strength in confirmed_signals:
            print(f"{ticker:<6} {signal:<4} votes:{vote_strength}")


        print("\nCOOLDOWN")
        print("--------")

        cooling = False

        for ticker,ts in cooldowns.items():

            remaining = int(COOLDOWN_SECONDS-(time.time()-ts))

            if remaining > 0:
                cooling = True
                print(f"{ticker:<6} {remaining}s")

        if not cooling:
            print("None")


        for strat,signal,ticker,vote_strength in confirmed_signals:

            now = time.time()

            if ticker in cooldowns:
                if now-cooldowns[ticker] < COOLDOWN_SECONDS:
                    continue

            price = prices.get(ticker)

            if price is None or price != price:
                continue

            held = portfolio.positions.get(ticker,0)


            if ticker in portfolio.positions:
                prev_high = high_prices.get(ticker,price)
                high_prices[ticker] = max(prev_high,price)


            if held > 0:

                high_price = high_prices.get(ticker,price)
                trailing_stop = high_price*(1-TRAILING_STOP_PCT)

                if price <= trailing_stop:
                    print(f"TRAILING STOP triggered for {ticker}")
                    portfolio.sell(ticker,price,held)
                    log_trade("TRAIL",ticker,"SELL",price,held)
                    cooldowns[ticker] = time.time()
                    high_prices.pop(ticker,None)
                    continue


            if held > 0:

                entry_price = portfolio.entry_prices.get(ticker,0)
                stop_price = entry_price*(1-STOP_LOSS_PCT)

                if price <= stop_price:
                    print(f"STOP LOSS triggered for {ticker}")
                    portfolio.sell(ticker,price,held)
                    log_trade("STOP",ticker,"SELL",price,held)
                    cooldowns[ticker] = time.time()
                    high_prices.pop(ticker,None)
                    continue


            portfolio_value = portfolio.total_value(prices)

            current_position = portfolio.positions.get(ticker,0)
            current_value = current_position*price

            max_allowed = portfolio_value*MAX_TICKER_ALLOCATION


            confidence = vote_strength/3

            if market_regime == "SIDEWAYS":
                risk_multiplier = 0.7
            elif market_regime == "TRENDING":
                risk_multiplier = 1.0
            else:
                risk_multiplier = 0.5


            risk_amount = portfolio_value*MAX_RISK_PER_TRADE*confidence*risk_multiplier
            shares = int(risk_amount/price)

            open_positions = len(portfolio.positions)


            if (
                signal == "BUY"
                and shares > 0
                and held == 0
                and open_positions < MAX_POSITIONS
                and current_value < max_allowed
            ):

                print(f"{strat} BUY {shares} {ticker} @ {round(price,2)}")

                portfolio.buy(ticker,price,shares)

                high_prices[ticker] = price

                log_trade("COUNCIL",ticker,"BUY",price,shares)

                generate_trade_chart(ticker)

                cooldowns[ticker] = time.time()


            elif signal == "SELL" and held > 0:

                print(f"{strat} SELL {held} {ticker}")

                portfolio.sell(ticker,price,held)

                log_trade("COUNCIL",ticker,"SELL",price,held)

                cooldowns[ticker] = time.time()

                high_prices.pop(ticker,None)


        time.sleep(2)


        if not prices:
            print("\nNo market data this cycle.")
            time.sleep(60)
            continue

        portfolio_value = portfolio.total_value(prices)

        today_pl = portfolio_value - 30000
        today_pct = (today_pl / 30000) * 100

        pl_str = f"+${today_pl:,.2f}" if today_pl >= 0 else f"-${abs(today_pl):,.2f}"
        pct_str = f"+{today_pct:.2f}%" if today_pct >= 0 else f"{today_pct:.2f}%"

        print("\nPORTFOLIO")
        print("---------")
        print(f"Value: ${portfolio_value:,.2f}")
        print(f"TODAY P/L: {pl_str} ({pct_str})")

        positions_value = portfolio_value - portfolio.cash
        exposure = (positions_value / portfolio_value) * 100 if portfolio_value > 0 else 0
        
        print(f"Cash: ${portfolio.cash:,.2f}")
        print(f"Positions Value: ${positions_value:,.2f}")
        print(f"Exposure: {exposure:.2f}%")






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

                position_value = current_price * qty

                print(
                    f"{ticker:<5} {qty:>4} "
                    f"entry:{entry_price:.2f} "
                    f"now:{current_price:.2f} "
                    f"value:${position_value:,.2f} "
                    f"P/L:{pnl_str}"
                )

            print(f"\nUnrealized P/L: ${total_pnl:,.2f}")



            print("\nRECENT TRADES")
            print("-------------")

            recent_trades = portfolio.trade_log[-5:]  # show last 5 trades

            if not recent_trades:
                print("None")
            else:
                for trade in recent_trades:
                    action = trade["action"]
                    ticker = trade["ticker"]
                    price = trade["price"]
                    shares = trade["shares"]

                    print(f"{action:<4} {ticker:<5} {shares} @ {price:.2f}")

        else:
            print("No open positions")



        log_equity({"MA": portfolio_value, "MR": portfolio_value, "AD": portfolio_value})

        strategy_equity["MA"] = portfolio_value
        strategy_equity["MR"] = portfolio_value
        strategy_equity["AD"] = portfolio_value

        print_leaderboard(strategy_equity)

        print("\nSTRATEGY PERFORMANCE")
        print("--------------------")

        for strat, equity in strategy_equity.items():
            pnl = equity - 30000
            pnl_pct = (pnl / 30000) * 100

            pnl_str = f"+{pnl_pct:.2f}%" if pnl_pct >= 0 else f"{pnl_pct:.2f}%"

            print(f"{strat:<4} P/L: {pnl_str}")

        generate_equity_chart()

        save_state({
              "cash": portfolio.cash,
              "positions": portfolio.positions,
              "entry_prices": portfolio.entry_prices
        })

        time.sleep(60)


if __name__ == "__main__":
    run_live_simulation()

