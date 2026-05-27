import random


def generate_signal(df):
    close = df["Close"]

    sma_5 = close.rolling(5).mean()
    sma_20 = close.rolling(20).mean()

    momentum = (
        (close.iloc[-1] - close.iloc[-5]) /
        close.iloc[-5]
    ) * 100

    volatility = abs(close.pct_change().std() * 100)

    confidence = min(abs(momentum) * 12, 100)

    # ---------- RANDOMIZED RISK ----------
    risk_pool = [
        "LOW",
        "LOW",
        "MEDIUM",
        "MEDIUM",
        "HIGH"
    ]

    risk = random.choice(risk_pool)

    # ---------- SIGNAL ----------
    if sma_5.iloc[-1] > sma_20.iloc[-1]:
        signal = "BUY"

    elif sma_5.iloc[-1] < sma_20.iloc[-1]:
        signal = "SELL"

    else:
        signal = random.choice([
            "BUY",
            "SELL",
            "HOLD"
        ])

    return {
        "signal": signal,
        "momentum": round(momentum, 2),
        "volatility": round(volatility, 2),
        "confidence": round(confidence, 2),
        "risk": risk
    }