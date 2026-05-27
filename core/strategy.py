import numpy as np


def generate_signal(df):
    close = df["Close"]

    sma_5 = close.rolling(5).mean()
    sma_20 = close.rolling(20).mean()

    momentum = (
        (close.iloc[-1] - close.iloc[-5]) /
        close.iloc[-5]
    ) * 100

    volatility = close.pct_change().std() * 100

    # AI confidence score
    confidence = abs(momentum) * 2

    # Risk score
    if volatility > 4:
        risk = "HIGH"
    elif volatility > 2:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # Signal logic
    if sma_5.iloc[-1] > sma_20.iloc[-1]:
        signal = "BUY"

    elif sma_5.iloc[-1] < sma_20.iloc[-1]:
        signal = "SELL"

    else:
        signal = "HOLD"

    return {
        "signal": signal,
        "momentum": round(momentum, 2),
        "volatility": round(volatility, 2),
        "confidence": round(confidence, 2),
        "risk": risk
    }
    
