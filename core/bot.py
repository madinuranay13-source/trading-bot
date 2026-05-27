from core.data import get_data
from core.strategy import generate_signal


class Bot:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def run(self, symbol):
        df = get_data(symbol)

        signal = generate_signal(df)

        price = float(df["Close"].values[-1])

        if signal == "BUY":
            self.portfolio.buy(symbol, price)

        elif signal == "SELL":
            self.portfolio.sell(symbol, price)

        return signal, price