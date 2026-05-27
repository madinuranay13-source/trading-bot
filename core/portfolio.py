class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.positions = {}
        self.history = []

    def buy(self, symbol, price, qty=1):
        cost = price * qty

        if self.cash >= cost:
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + qty
            self.history.append(("BUY", symbol, price, qty))

    def sell(self, symbol, price, qty=1):
        if self.positions.get(symbol, 0) >= qty:
            self.positions[symbol] -= qty
            self.cash += price * qty
            self.history.append(("SELL", symbol, price, qty))

    def value(self, prices):
        total = self.cash

        for s, q in self.positions.items():
            total += prices.get(s, 0) * q

        return total