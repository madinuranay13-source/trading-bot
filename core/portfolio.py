class Portfolio:
    def __init__(self, cash):
        self.cash = float(cash)
        self.positions = {}
        self.history = []

    def buy(self, symbol, price, qty=1):
        cost = price * qty

        if self.cash >= cost:
            self.cash -= cost

            self.positions[symbol] = (
                self.positions.get(symbol, 0) + qty
            )

            self.history.append(
                ("BUY", symbol, round(price, 2), qty)
            )

    def sell(self, symbol, price, qty=1):
        if self.positions.get(symbol, 0) >= qty:
            self.positions[symbol] -= qty

            self.cash += price * qty

            self.history.append(
                ("SELL", symbol, round(price, 2), qty)
            )

    def value(self, prices):
        total = self.cash

        for symbol, qty in self.positions.items():
            total += prices.get(symbol, 0) * qty

        return float(total)