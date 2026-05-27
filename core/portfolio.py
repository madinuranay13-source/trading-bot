class Portfolio:
    def __init__(self, cash):
        self.cash = float(cash)
        self.positions = {}
        self.history = []

    def buy(self, symbol, price, qty=1):
        price = float(price)
        cost = price * qty

        if self.cash >= cost:
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + qty
            self.history.append(("BUY", symbol, price, qty))

    def sell(self, symbol, price, qty=1):
        price = float(price)

        if self.positions.get(symbol, 0) >= qty:
            self.positions[symbol] -= qty
            self.cash += price * qty
            self.history.append(("SELL", symbol, price, qty))

    def value(self, prices):
        total = float(self.cash)

        for symbol, qty in self.positions.items():
            price = float(prices.get(symbol, 0))
            total += price * qty

        return float(total)