import yfinance as yf
from data_utils import get_recent_data
from strategies import adaptive_strategy
from trade_logger import log_trade


def run_crypto_engine(portfolio, universe):

    print("\nCRYPTO ENGINE")
    print("-------------")

    for symbol in universe:

        try:

            data = get_recent_data(symbol)

            if data is None or len(data) < 50:
                continue

            signal = adaptive_strategy(data)

            if signal:

                price = data["Close"].iloc[-1]

                portfolio.execute_trade(symbol, signal, price)

                log_trade(symbol, signal, price, "CRYPTO")

        except Exception as e:
            print(f"crypto error {symbol}: {e}")

