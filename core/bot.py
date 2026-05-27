from core.data import get_data
from core.strategy import generate_signal


class Bot:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def run(self, symbol):
        df = get_data(symbol)

        if df is None or df.empty:
            return "NO DATA", 0

        signal = generate_signal(df)
        price = float(df["Close"].iloc[-1].item())

        if signal == "BUY":
            self.portfolio.buy(symbol, price)
        elif signal == "SELL":
            self.portfolio.sell(symbol, price)

        return signal, price