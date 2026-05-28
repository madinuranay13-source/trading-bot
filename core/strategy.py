import pandas as pd


def moving_average_strategy(df):

    close = df["Close"]

    sma_5 = close.rolling(5).mean()

    sma_20 = close.rolling(20).mean()

    momentum = (
        (
            close.iloc[-1] -
            close.iloc[-5]
        ) / close.iloc[-5]
    ) * 100

    volatility = abs(
        close.pct_change().std() * 100
    )

    confidence = min(
        abs(momentum) * 10,
        100
    )

    if volatility < 2:
        risk = "LOW"

    elif volatility < 4:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

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


def rsi_strategy(df):

    close = df["Close"]

    delta = close.diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    latest_rsi = rsi.iloc[-1]

    volatility = abs(
        close.pct_change().std() * 100
    )

    if latest_rsi < 30:
        signal = "BUY"

    elif latest_rsi > 70:
        signal = "SELL"

    else:
        signal = "HOLD"

    return {
        "signal": signal,
        "momentum": round(latest_rsi, 2),
        "volatility": round(volatility, 2),
        "confidence": 75,
        "risk": "MEDIUM"
    }


def generate_signal(
    df,
    strategy_name="Moving Average"
):

    if strategy_name == "RSI":
        return rsi_strategy(df)

    return moving_average_strategy(df)