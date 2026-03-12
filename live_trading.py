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
import math
from datetime import datetime, timedelta
import pytz
import shutil
import json


MAX_POSITIONS = 20
MAX_RISK_PER_TRADE = 0.02
MAX_TICKER_ALLOCATION = 0.10
MAX_PORTFOLIO_EXPOSURE = 0.65
STOP_LOSS_PCT = 0.05
TRAILING_STOP_PCT = 0.05
SIGNAL_CONFIRM_CYCLES = 3
MIN_VOLATILITY = 0.5
MAX_NEW_TRADES_PER_CYCLE = 5



SCAN_UNIVERSE = [
    "SPY",
    "NVDA", "AMD", "TSLA", "META", "AAPL",
    "MSFT", "GOOGL", "AMZN", "AVGO", "NFLX"
]

MEMORY_FILE = "strategy_memory.json"

def load_strategy_memory():

    if not os.path.exists(MEMORY_FILE):
        return {
            "MA": {"pnl": 0, "trades": 0},
            "MR": {"pnl": 0, "trades": 0},
            "AD": {"pnl": 0, "trades": 0}
        }

    with open(MEMORY_FILE) as f:
        return json.load(f)


def save_strategy_memory(memory):

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)





def compute_sector_flow(prices, data_cache):
    sectors = {
        "AI": ["NVDA", "AMD", "AVGO"],
        "TECH": ["AAPL", "MSFT"],
        "MEDIA": ["META", "GOOGL", "NFLX"]
    }

    sector_scores = {}

    for sector, tickers in sectors.items():

        changes = []

        for ticker in tickers:

            data = data_cache.get(ticker)
            price = prices.get(ticker)

            if data is None or price is None:
                continue

            try:
                prev_close = data["Close"].iloc[-2]
                pct = (price - prev_close) / prev_close
                changes.append(pct)
            except Exception:
                continue

        if not changes:
            sector_scores[sector] = ("UNKNOWN", 0)
            continue

        avg = sum(changes) / len(changes)

        if avg > 0.01:
            label = "🟢 STRONG"
        elif avg < -0.01:
            label = "🔴 WEAK"
        else:
            label = "🟡 MIXED"

        sector_scores[sector] = (label, avg)

    return sector_scores


def run_live_simulation(universe=None, crypto_universe=None):
    if universe is None:
        universe = SCAN_UNIVERSE

    if crypto_universe is None:
        crypto_universe = []

    all_symbols = universe + crypto_universe

    strategy_equity = {
        "MA": 30000,
        "MR": 30000,
        "AD": 30000
    }

    regime_weights = {
        "TRENDING": {"MA": 1.8, "MR": 0.6, "AD": 1.2},
        "SIDEWAYS": {"MA": 0.6, "MR": 1.8, "AD": 1.2},
        "UNKNOWN": {"MA": 0.8, "MR": 0.8, "AD": 1.6}
    }

    strategy_memory = load_strategy_memory()

    strategy_weights = regime_weights["UNKNOWN"].copy()

    state = load_state()

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
    position_scores = {}

    data_refresh_time = 0
    DATA_REFRESH_SECONDS = 300

    data_cache = {}

    while True:

        os.system("clear")

        print("========== AI TRADING LAB ==========")
        print("-" * shutil.get_terminal_size().columns)

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

        tickers = " ".join(universe)

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

            for ticker in all_symbols:
                try:
                    data_cache[ticker] = get_recent_data(ticker, 1)

                    # Single ticker dataframe
                    if "Close" in live_data and not isinstance(live_data["Close"], yf.pandas.Series):
                        price = live_data["Close"].iloc[-1]

                    # Multi-ticker grouped dataframe
                    elif ticker in live_data:
                        price = live_data[ticker]["Close"].iloc[-1]

                    else:
                        price = live_data["Close"][ticker].iloc[-1]

                    if price is not None and not math.isnan(price):
                        prices[ticker] = float(price)

                except Exception:
                    continue

            # Fetch crypto prices (batch)
            if crypto_universe:

                try:

                    crypto_tickers = " ".join(crypto_universe)

                    crypto_data = yf.download(
                        crypto_tickers,
                        period="5d",
                        interval="5m",
                        group_by="ticker",
                        progress=False
                    )

                    for ticker in crypto_universe:

                        try:

                            if ticker in crypto_data:

                                price = crypto_data[ticker]["Close"].iloc[-1]

                                if price == price:  # avoid NaN
                                    prices[ticker] = float(price)

                        except Exception:
                            continue

                except Exception:
                    pass

        current_time = time.time()

        if current_time - data_refresh_time > DATA_REFRESH_SECONDS:

            for ticker in universe:
                try:
                    data_cache[ticker] = get_recent_data(ticker, 1)
                except Exception:
                    continue

            data_refresh_time = current_time

        print("MARKET")
        print("------")

        row = ""

        for t in all_symbols:

            p = prices.get(t)

            if p is None or math.isnan(p):
                cell = f"{t}:data"
            else:
                cell = f"{t}:{p:.2f}"

            row += f"{cell:<18}"

        print(row)

        print()

        # repair missing entry prices
        for ticker in portfolio.positions:
            if ticker not in portfolio.entry_prices or portfolio.entry_prices[ticker] == 0:
                p = prices.get(ticker)
                if p:
                    portfolio.entry_prices[ticker] = p

        print("TOP MOVERS")
        print("----------")

        volatility_data = []

        movers = []

        for ticker in prices:

            data = data_cache.get(ticker)

            if data is None:
                continue

            try:
                prev_close = data["Close"].iloc[-2]
                current = prices[ticker]

                pct_move = ((current - prev_close) / prev_close) * 100
                movers.append((ticker, pct_move))

            except Exception:
                continue

        # sort biggest movers
        movers.sort(key=lambda x: abs(x[1]), reverse=True)

        mover_row = ""

        for ticker, pct in movers[:5]:
            sign = "+" if pct >= 0 else ""
            mover_row += f"{ticker}:{sign}{pct:.2f}%   "

        print(mover_row)
        print()

        signal_list = []
        pending_signals = []

        confirmed_signals = []

        signal_debug = []
        trade_filters = []

        strategy_matrix = {}

        breadth_buy = 0
        breadth_sell = 0
        breadth_hold = 0
        acceleration = []
        breakout_radar = []
        liquidity_spikes = []
        trend_strength = []

        market_regime = "UNKNOWN"

        market_symbol = universe[0]

        spy_data = data_cache.get(market_symbol)

        if spy_data is not None:
            try:
                market_regime = regime_history(spy_data)[-1]
            except Exception:
                market_regime = "UNKNOWN"

        risk_mode = {
            "TRENDING": "AGGRESSIVE",
            "SIDEWAYS": "NORMAL",
            "UNKNOWN": "DEFENSIVE"
        }.get(market_regime, "DEFENSIVE")

        print(f"\nMARKET REGIME: {market_regime}")
        print(f"RISK MODE: {risk_mode}\n")

        # Update strategy weights based on regime
        if market_regime in regime_weights:
            strategy_weights = regime_weights[market_regime].copy()

        regime_row = ""

        for ticker in prices:

            if ticker == "SPY":
                continue

            data = data_cache.get(ticker)

            if data is None:
                continue

            try:
                volume = data["Volume"]

                if len(volume) > 10:
                    recent = volume.iloc[-1]
                    avg = volume.tail(10).mean()

                    if avg > 0 and recent > avg * 2:
                        liquidity_spikes.append(ticker)

            except Exception:
                pass

            if data is None:
                continue

            try:
                returns = data["Close"].pct_change().dropna()
                vol = returns.std() * 100

                if vol < MIN_VOLATILITY:
                    continue

                volatility_data.append((ticker, vol))

                try:
                    closes = data["Close"]

                    # ACCELERATION CALCULATION
                    m1 = closes.iloc[-1] - closes.iloc[-2]
                    m2 = closes.iloc[-2] - closes.iloc[-3]

                    accel = m1 - m2

                    if accel > 0.5:
                        accel_symbol = "↑↑"
                    elif accel > 0:
                        accel_symbol = "↑"
                    elif accel < -0.5:
                        accel_symbol = "↓↓"
                    else:
                        accel_symbol = "→"

                    acceleration.append((ticker, accel_symbol))

                    # TREND STRENGTH CALCULATION
                    try:
                        ma5 = closes.tail(5).mean()
                        ma10 = closes.tail(10).mean()
                        ma20 = closes.tail(20).mean()

                        score = 0

                        if ma5 > ma10:
                            score += 1
                        if ma10 > ma20:
                            score += 1
                        if closes.iloc[-1] > ma5:
                            score += 1

                        if score == 3:
                            symbol = "↑↑↑"
                        elif score == 2:
                            symbol = "↑↑"
                        elif score == 1:
                            symbol = "↑"
                        else:
                            symbol = "→"

                        trend_strength.append((ticker, symbol))

                    except Exception:
                        pass

                    accel = m1 - m2

                    if accel > 0.5:
                        accel_symbol = "↑↑"
                    elif accel > 0:
                        accel_symbol = "↑"
                    elif accel < -0.5:
                        accel_symbol = "↓↓"
                    else:
                        accel_symbol = "→"

                    if accel_symbol == "↑↑" and vol > 2:
                        breakout_radar.append(ticker)

                except Exception:
                    pass

            except Exception:
                pass

            regime = regime_history(data)[-1]

            if regime == "TRENDING":
                symbol = "🟢"
            elif regime == "SIDEWAYS":
                symbol = "🟡"
            elif regime == "REVERSAL":
                symbol = "🔴"
            else:
                symbol = "⚪"

            regime_row += f"{ticker} {symbol} {regime:<10}  "

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
            vote_details = signals.copy()

            strategy_matrix[ticker] = signals

            debug_line = f"{ticker} "
            for strat_name, vote in signals.items():
                debug_line += f"{strat_name}:{vote} "
            signal_debug.append(debug_line)

            buy_votes = 0
            sell_votes = 0

            for strat_name, vote in signals.items():

                weight = strategy_weights.get(strat_name, 1)

                if vote == "BUY":
                    buy_votes += weight
                elif vote == "SELL":
                    sell_votes += weight

            combined_signal = "HOLD"
            vote_strength = 0

            if buy_votes >= 2:
                combined_signal = "BUY"
                vote_strength = buy_votes

            elif sell_votes >= 2:
                combined_signal = "SELL"
                vote_strength = sell_votes

            if combined_signal == "BUY":
                breadth_buy += 1
            elif combined_signal == "SELL":
                breadth_sell += 1
            else:
                breadth_hold += 1

            if combined_signal in ("BUY", "SELL"):
                score = vote_strength

                signal_list.append(("COUNCIL", combined_signal, ticker, vote_strength, vote_details, score))

        active_keys = {(ticker, signal) for _, signal, ticker, _, _, _ in signal_list}

        for key in list(signal_history.keys()):
            if key not in active_keys:
                signal_history.pop(key)

        print("\nREGIMES")
        print("-------")
        print(regime_row)

        print("\nHEATMAP")
        print("-------")

        heat_row = ""

        for ticker in prices:

            data = data_cache.get(ticker)
            if data is None:
                continue

            try:
                prev_close = data["Close"].iloc[-2]
                current = prices[ticker]

                pct_move = ((current - prev_close) / prev_close) * 100

                if pct_move > 1:
                    color = "🟢"
                elif pct_move < -1:
                    color = "🔴"
                else:
                    color = "🟡"

                heat_row += f"{ticker}:{color}{pct_move:+.2f}%  "

            except Exception:
                continue

        print(heat_row)
        print()

        print("\nBREADTH")
        print("-------")
        print(f"BUY:{breadth_buy}   SELL:{breadth_sell}   HOLD:{breadth_hold}")

        total = breadth_buy + breadth_sell + breadth_hold

        if total > 0:
            bull_pct = breadth_buy / total
            bear_pct = breadth_sell / total
            neutral_pct = breadth_hold / total

            bull_bar = "█" * int(bull_pct * 10) + "░" * (10 - int(bull_pct * 10))
            bear_bar = "█" * int(bear_pct * 10) + "░" * (10 - int(bear_pct * 10))
            neutral_bar = "█" * int(neutral_pct * 10) + "░" * (10 - int(neutral_pct * 10))

            print("\nMARKET HEALTH")
            print("-------------")
            print(f"Bullish {bull_bar} {bull_pct * 100:.0f}%")
            print(f"Bearish {bear_bar} {bear_pct * 100:.0f}%")
            print(f"Neutral {neutral_bar} {neutral_pct * 100:.0f}%")

        total_signals = breadth_buy + breadth_sell + breadth_hold

        if total_signals > 0:
            sentiment = breadth_buy / total_signals
        else:
            sentiment = 0

        bars = int(sentiment * 10)
        meter = "█" * bars + "░" * (10 - bars)

        avg_vol = 0

        if volatility_data:
            avg_vol = sum(v for _, v in volatility_data) / len(volatility_data)

        pressure_score = breadth_buy - breadth_sell - (avg_vol * 0.5)

        if pressure_score > 2:
            pressure = "BULLISH"
        elif pressure_score < -2:
            pressure = "BEARISH"
        else:
            pressure = "NEUTRAL"

        print("\nACCELERATION")
        print("------------")

        accel_row = ""

        for ticker, symbol in acceleration:
            accel_row += f"{ticker}:{symbol:<3}  "

        print(accel_row)

        print("\nTREND STRENGTH")
        print("--------------")

        row = ""

        for ticker, symbol in trend_strength:
            row += f"{ticker}:{symbol:<4}"

        print(row)

        print("\nBREAKOUT RADAR")
        print("--------------")

        if breakout_radar:
            row = ""
            for ticker in breakout_radar:
                row += f"{ticker} 🚀  "
            print(row)
        else:
            print("None")

        print("\nLIQUIDITY SPIKES")
        print("----------------")

        if liquidity_spikes:
            row = ""
            for ticker in liquidity_spikes:
                row += f"{ticker} ⚡  "
            print(row)
        else:
            print("None")

        print("\nMARKET PRESSURE")
        print("----------------")
        print(pressure)

        print("\nMARKET SENTIMENT")
        print("----------------")
        print(f"Bullish {meter} {sentiment * 100:.0f}%")

        # AI MARKET PULSE
        pulse_score = 0

        # breadth contribution
        pulse_score += breadth_buy - breadth_sell

        # breakout signals
        pulse_score += len(breakout_radar)

        # acceleration signals
        strong_accel = sum(1 for _, s in acceleration if s == "↑↑")
        pulse_score += strong_accel

        # normalize score
        pulse_score = max(0, min(10, pulse_score + 5))

        bars = "█" * pulse_score + "░" * (10 - pulse_score)

        if pulse_score >= 7:
            pulse_trend = "STRONG"
        elif pulse_score >= 4:
            pulse_trend = "MODERATE"
        else:
            pulse_trend = "WEAK"

        if strong_accel >= 2:
            momentum_state = "BUILDING"
        elif strong_accel == 1:
            momentum_state = "STABLE"
        else:
            momentum_state = "FLAT"

        print("\nAI MARKET PULSE")
        print("---------------")
        print(f"Confidence {bars} {pulse_score * 10}%")
        print(f"Trend Strength: {pulse_trend}")
        print(f"Momentum: {momentum_state}")

        print("\nSTRATEGY CAPITAL")
        print("----------------")

        total_weight = sum(strategy_weights.values())

        for strat, w in sorted(strategy_weights.items(), key=lambda x: x[1], reverse=True):
            pct = (w / total_weight) * 100
            bars = "█" * int(pct / 5)

            print(f"{strat:<3} {bars:<10} {pct:5.1f}%")

        print("\nVOLATILITY")
        print("----------")

        volatility_data.sort(key=lambda x: x[1], reverse=True)

        vol_row = ""

        for ticker, vol in volatility_data[:5]:
            vol_row += f"{ticker}:{vol:.2f}%   "

        print(vol_row)
        print()

        sectors = compute_sector_flow(prices, data_cache)

        print("\nCAPITAL FLOW")
        print("------------")

        for sector, (label, pct) in sectors.items():
            pct_str = f"{pct * 100:+.2f}%"
            print(f"{sector:<7} {label:<10} {pct_str}")

        print("\nSTRATEGY MATRIX")
        print("---------------")

        print(f"{'':8} {'MA':6} {'MR':6} {'AD':6}")

        sorted_matrix = []

        for ticker, sigs in strategy_matrix.items():

            ma = sigs.get("MA", "-")
            mr = sigs.get("MR", "-")
            ad = sigs.get("AD", "-")

            score = 0

            if mr == "BUY":
                score += 1
            if ad == "BUY":
                score += 1
            if mr == "SELL":
                score -= 1
            if ad == "SELL":
                score -= 1

            sorted_matrix.append((score, ticker, ma, mr, ad))

        sorted_matrix.sort(reverse=True)

        for score, ticker, ma, mr, ad in sorted_matrix:
            agree = "⚡" if (mr == ad and mr in ("BUY", "SELL")) else ""

            print(f"{ticker:8} {ma:6} {mr:6} {ad:6} {agree}")

        for strat, signal, ticker, vote_strength, vote_details, _ in signal_list:

            key = (ticker, signal)

            signal_history[key] = signal_history.get(key, 0) + 1

            # Signal persistence boost
            persistence = signal_history[key]
            vote_strength = vote_strength + (persistence * 0.25)

            if signal_history[key] >= SIGNAL_CONFIRM_CYCLES:
                confirmed_signals.append((strat, signal, ticker, vote_strength, vote_details, vote_strength))
            else:
                pending_signals.append((strat, signal, ticker, vote_strength, vote_details))

        print("\nPENDING SIGNALS")
        print("----------------")

        if not pending_signals:
            print("None")

        for strat, signal, ticker, vote_strength, _ in pending_signals:
            count = signal_history.get((ticker, signal), 0)
            print(f"{ticker:<6} {signal:<4} votes:{vote_strength} confirm:{count}/{SIGNAL_CONFIRM_CYCLES}")

        print("\nCONFIRMED SIGNALS")
        print("-----------------")

        if not confirmed_signals:
            print("None")

        # Rank signals by strength
        confirmed_signals.sort(key=lambda x: x[3], reverse=True)
        confirmed_signals = confirmed_signals[:MAX_NEW_TRADES_PER_CYCLE]

        for strat, signal, ticker, vote_strength, vote_details, _ in confirmed_signals:
            print(f"{ticker:<6} {signal:<4} votes:{vote_strength}")

        print("\nTOP OPPORTUNITIES")
        print("-----------------")

        opportunities = []
        best_opportunity = None
        best_score = 0

        for strat, signal, ticker, vote_strength, vote_details, score in confirmed_signals:
            if signal == "BUY":
                opportunities.append((ticker, score))

        opportunities.sort(key=lambda x: x[1], reverse=True)

        if not opportunities:
            print("None")
        else:
            for ticker, score in opportunities[:5]:
                print(f"{ticker:<6} score:{score}")

                if score > best_score:
                    best_score = score
                    best_opportunity = ticker

        # Rank signals by strength
        confirmed_signals.sort(key=lambda x: x[3], reverse=True)

        for strat, signal, ticker, vote_strength, vote_details, _ in confirmed_signals:
            print(f"{ticker:<6} {signal:<4} votes:{vote_strength}")

        print("\nCOOLDOWN")
        print("--------")

        cooling = False

        for ticker, ts in cooldowns.items():

            remaining = int(COOLDOWN_SECONDS - (time.time() - ts))

            if remaining > 0:
                cooling = True
                print(f"{ticker:<6} {remaining}s")

        if not cooling:
            print("None")

        for strat, signal, ticker, vote_strength, *_ in confirmed_signals:

            now = time.time()

            if ticker in cooldowns:
                if now - cooldowns[ticker] < COOLDOWN_SECONDS:
                    trade_filters.append(f"{ticker}: cooldown")
                    continue

            price = prices.get(ticker)

            if price is None or price != price:
                continue

            held = portfolio.positions.get(ticker, 0)

            if ticker in portfolio.positions:
                prev_high = high_prices.get(ticker, price)
                high_prices[ticker] = max(prev_high, price)

            if held > 0:

                high_price = high_prices.get(ticker, price)
                trailing_stop = high_price * (1 - TRAILING_STOP_PCT)

                if price <= trailing_stop:
                    print(f"TRAILING STOP triggered for {ticker}")
                    portfolio.sell(ticker, price, held)
                    log_trade("TRAIL", ticker, "SELL", price, held)
                    cooldowns[ticker] = time.time()
                    high_prices.pop(ticker, None)
                    continue

            if held > 0:

                entry_price = portfolio.entry_prices.get(ticker, price)
                stop_price = entry_price * (1 - STOP_LOSS_PCT)

                if price <= stop_price:
                    print(f"STOP LOSS triggered for {ticker}")
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

            if market_regime == "SIDEWAYS":
                risk_multiplier = 0.7
            elif market_regime == "TRENDING":
                risk_multiplier = 1.0
            else:
                risk_multiplier = 0.5

            risk_amount = portfolio_value * MAX_RISK_PER_TRADE * confidence * risk_multiplier
            shares = int(risk_amount / price)

            if signal == "BUY" and shares == 0:
                trade_filters.append(f"{ticker}: position size too small")
                continue

            open_positions = len(portfolio.positions)

            if (
                    signal == "BUY"
                    and shares > 0
                    and held == 0
                    and current_value < max_allowed
                    and (
                    open_positions < MAX_POSITIONS
                    or (
                            open_positions >= MAX_POSITIONS
                            and position_scores
                            and vote_strength > min(position_scores.values())
                    )
            )
            ):

                # Rotate weakest position if portfolio full
                if open_positions >= MAX_POSITIONS:

                    weakest = min(position_scores, key=position_scores.get)
                    weakest_score = position_scores[weakest]

                    if vote_strength > weakest_score:

                        qty = portfolio.positions.get(weakest, 0)
                        w_price = prices.get(weakest)

                        if qty > 0 and w_price:
                            print(f"ROTATING OUT {weakest}")

                            portfolio.sell(weakest, w_price, qty)

                            log_trade("ROTATE", weakest, "SELL", w_price, qty)

                            position_scores.pop(weakest, None)

                print(f"{strat} BUY {shares} {ticker} @ {round(price, 2)}")

                reason = " ".join([f"{k}={v}" for k, v in vote_details.items()])
                print(f"Reason: {reason} ({vote_strength} votes)")

                portfolio.buy(ticker, price, shares)

                position_scores[ticker] = vote_strength

                high_prices[ticker] = price

                log_trade("COUNCIL", ticker, "BUY", price, shares)

                generate_trade_chart(ticker)

                cooldowns[ticker] = time.time()


            elif signal == "SELL" and held > 0:

                print(f"{strat} SELL {held} {ticker}")

                reason = " ".join([f"{k}={v}" for k, v in vote_details.items()])
                print(f"Reason: {reason} ({vote_strength} votes)")

                portfolio.sell(ticker, price, held)

                portfolio.sell(ticker, price, held)

                # --- strategy learning memory ---
                entry = portfolio.entry_prices.get(ticker, price)
                pnl = (price - entry) * held

                if strat in strategy_memory:
                    strategy_memory[strat]["pnl"] += pnl
                    strategy_memory[strat]["trades"] += 1
                    save_strategy_memory(strategy_memory)
                # --------------------------------

                position_scores.pop(ticker, None)

                log_trade("COUNCIL", ticker, "SELL", price, held)

                cooldowns[ticker] = time.time()

                high_prices.pop(ticker, None)

                position_scores.pop(ticker, None)

                log_trade("COUNCIL", ticker, "SELL", price, held)

                cooldowns[ticker] = time.time()

                high_prices.pop(ticker, None)

        time.sleep(2)

        if not prices:
            print("\nNo market data this cycle.")
            time.sleep(300)
            continue

        portfolio_value = portfolio.total_value(prices)

        today_pl = portfolio_value - 30000
        today_pct = (today_pl / 30000) * 100

        pl_str = f"+${today_pl:,.2f}" if today_pl >= 0 else f"-${abs(today_pl):,.2f}"
        pct_str = f"+{today_pct:.2f}%" if today_pct >= 0 else f"{today_pct:.2f}%"

        print("\nPORTFOLIO")
        print("---------")

        # Portfolio intelligence tracking
        weakest_position = None
        weakest_score = None

        if position_scores:
            weakest_position = min(position_scores, key=position_scores.get)
            weakest_score = position_scores[weakest_position]

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
                current_price = prices.get(ticker)

                if current_price is None:
                    continue

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

        print("\nPORTFOLIO INTELLIGENCE")
        print("----------------------")

        if weakest_position:
            print(f"Weakest Position : {weakest_position} (score {weakest_score})")
        else:
            print("Weakest Position : None")

        if best_opportunity:
            print(f"Top Opportunity  : {best_opportunity} (score {best_score})")
        else:
            print("Top Opportunity  : None")

        if weakest_position and best_opportunity and best_score > weakest_score:
            print("Rotation Signal  : YES")
        else:
            print("Rotation Signal  : NO")

        log_equity({"MA": portfolio_value, "MR": portfolio_value, "AD": portfolio_value})

        strategy_equity["MA"] = portfolio_value
        strategy_equity["MR"] = portfolio_value
        strategy_equity["AD"] = portfolio_value

        # Strategy learning allocation
        for strat, stats in strategy_memory.items():

            trades = stats["trades"]
            pnl = stats["pnl"]

            if trades == 0:
                score = 1
            else:
                score = pnl / trades

            strategy_weights[strat] = max(0.5, min(2.5, 1 + score / 100))

        print("\nSTRATEGY LEADERBOARD")
        print("--------------------")

        leader_row = ""

        for strat, equity in strategy_equity.items():
            leader_row += f"{strat}:${equity:,.2f}   "

        print(leader_row)

        print("\nSTRATEGY PERFORMANCE")
        print("--------------------")

        perf_row = ""

        for strat, equity in strategy_equity.items():
            pnl = equity - 30000
            pnl_pct = (pnl / 30000) * 100

            pnl_str = f"+{pnl_pct:.2f}%" if pnl_pct >= 0 else f"{pnl_pct:.2f}%"

            perf_row += f"{strat}:{pnl_str}   "

        print(perf_row)

        # generate_equity_chart()

        save_state({
            "cash": portfolio.cash,
            "positions": portfolio.positions,
            "entry_prices": portfolio.entry_prices
        })

        time.sleep(300)


if __name__ == "__main__":
    run_live_simulation()
