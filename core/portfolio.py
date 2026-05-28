class Portfolio:

    def __init__(self, cash):

        self.initial_cash = float(cash)

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

            self.history.append({
                "type": "BUY",
                "symbol": symbol,
                "price": round(price, 2),
                "qty": qty
            })

    def sell(self, symbol, price, qty=1):

        if self.positions.get(symbol, 0) >= qty:

            self.positions[symbol] -= qty

            self.cash += price * qty

            self.history.append({
                "type": "SELL",
                "symbol": symbol,
                "price": round(price, 2),
                "qty": qty
            })

    def value(self, prices):

        total = self.cash

        for symbol, qty in self.positions.items():

            total += prices.get(symbol, 0) * qty

        return round(total, 2)

    def pnl(self, current_prices):

        total_value = self.value(current_prices)

        pnl = total_value - self.initial_cash

        pnl_percent = (
            pnl / self.initial_cash
        ) * 100

        return (
            round(pnl, 2),
            round(pnl_percent, 2)
        )