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

            from datetime import datetime

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

        for ticker, shares in self.positions.items():
            price = prices.get(ticker, 0)
            value += shares * price

        return value