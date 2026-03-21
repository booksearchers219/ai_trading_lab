from datetime import datetime
class Portfolio:


    def __init__(self, cash):
        self.cash = cash
        self.positions = {}
        self.entry_prices = {}
        self.trade_log = []

    def buy(self, ticker, price, shares):

        cost = price * shares

        if self.cash >= cost:
            self.cash -= cost

            self.positions[ticker] = self.positions.get(ticker, 0) + shares

            # store entry price
            self.entry_prices[ticker] = price



            self.trade_log.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "action": "BUY",
                "ticker": ticker,
                "price": price,
                "shares": shares
            })

    def sell(self, ticker, price, shares):

        if self.positions.get(ticker, 0) >= shares:

            self.positions[ticker] -= shares
            self.cash += price * shares



            self.trade_log.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "action": "SELL",
                "ticker": ticker,
                "price": price,
                "shares": shares
            })

            # remove position if closed
            if self.positions[ticker] == 0:
                del self.positions[ticker]
                if ticker in self.entry_prices:
                    del self.entry_prices[ticker]

    def total_value(self, prices):

        value = self.cash

        for ticker, shares in list(self.positions.items()):

            price = prices.get(ticker)

            # fallback to entry price if market price missing
            if price is None:
                price = self.entry_prices.get(ticker)

            if price is None:
                continue

            entry = self.entry_prices.get(ticker)

            if entry:

                profit_pct = (price - entry) / entry

                # take full profit at +20%
                if profit_pct > 0.20:

                    print(f"Taking full profit on {ticker}")

                    self.sell(ticker, price, shares)

                    continue

                # take partial profit at +10%
                elif profit_pct > 0.10 and shares > 0:

                    sell_size = round(shares * 0.5, 6)

                    print(f"Taking partial profit on {ticker}")

                    self.sell(ticker, price, sell_size)

                    shares = self.positions.get(ticker, 0)

            value += shares * price

        return value