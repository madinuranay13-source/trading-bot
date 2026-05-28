import streamlit as st
import pandas as pd

from core.data import get_data
from core.strategy import generate_signal


def render():

    st.title("🧠 Strategy Lab")

    symbol = st.selectbox(
        "Choose Stock",
        [
            "AAPL",
            "TSLA",
            "NVDA",
            "MSFT"
        ]
    )

    strategy = st.selectbox(
        "Choose Strategy",
        [
            "Moving Average",
            "RSI"
        ]
    )

    df = get_data(symbol)

    result = generate_signal(
        df,
        strategy
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Signal",
            result["signal"]
        )

    with c2:
        st.metric(
            "Momentum",
            result["momentum"]
        )

    with c3:
        st.metric(
            "Risk",
            result["risk"]
        )

    st.dataframe(
        df.tail(20),
        use_container_width=True
    )