import yfinance as yf
import pandas as pd


def get_data(symbol, period="6mo"):

    df = yf.download(
        symbol,
        period=period,
        progress=False
    )

    df = df.dropna()

    return df