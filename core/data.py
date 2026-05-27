import yfinance as yf

def get_data(symbol):
    df = yf.download(symbol, period="5d", interval="1h")

    if df is None or df.empty:
        return None

    df = df.dropna()
    return df