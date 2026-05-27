import pandas as pd
import numpy as np


def get_data(symbol):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)

    prices = np.cumsum(np.random.randn(30)) + 100

    df = pd.DataFrame({
        "Close": prices
    }, index=dates)

    return df