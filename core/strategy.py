def generate_signal(df):
    if df is None or len(df) < 20:
        return "HOLD"

    df = df.copy()

    df["SMA_short"] = df["Close"].rolling(5).mean()
    df["SMA_long"] = df["Close"].rolling(20).mean()

    short = df["SMA_short"].iloc[-1]
    long = df["SMA_long"].iloc[-1]

    if short > long:
        return "BUY"
    elif short < long:
        return "SELL"
    else:
        return "HOLD"