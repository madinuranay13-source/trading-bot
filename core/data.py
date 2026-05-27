import yfinance as yf
import pandas as pd


def get_data(symbol):
    try:
        # Try normal download first
        df = yf.download(
            symbol,
            period="1mo",
            interval="1d",
            progress=False,
            auto_adjust=True
        )

        if df is not None and not df.empty:
            return df

    except Exception:
        pass

    # Fallback dummy data (prevents blank app)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)

   