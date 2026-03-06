class Portfolio:
    def __init__(self, starting_cash=10000):
        self.cash = starting_cash
        self.positions = {}
        self.trade_log = []

    def buy(self, ticker, price, shares):
        cost = price * shares

        if self.cash >= cost:
            self.cash -= cost
            self.positions[ticker] = self.positions.get(ticker, 0) + shares

            self.trade_log.append({
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

    def total_value(self, prices):

        value = self.cash

        for ticker, shares in self.positions.items():
            value += shares * prices[ticker]

        return value