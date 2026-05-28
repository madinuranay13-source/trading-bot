import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.state import SYMBOLS
from core.data import get_data


def render():

    st.title("📊 QUANT-X Dashboard")

    trader = st.session_state.trader
    portfolio = st.session_state.portfolio

    strategy = st.selectbox(
        "Strategy",
        [
            "Moving Average",
            "RSI"
        ]
    )

    if st.button("🚀 Run AI Market Scan"):

        with st.spinner(
            "Scanning markets..."
        ):

            market = trader.scan_market(
                SYMBOLS
            )

            st.session_state.market = market

    market = st.session_state.get(
        "market",
        []
    )

    if market:

        portfolio_value = portfolio.value({
            stock["symbol"]: stock["price"]
            for stock in market
        })

        pnl, pnl_percent = portfolio.pnl({
            stock["symbol"]: stock["price"]
            for stock in market
        })

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Portfolio Value",
                f"${portfolio_value:,.2f}"
            )

        with c2:
            st.metric(
                "Cash",
                f"${portfolio.cash:,.2f}"
            )

        with c3:
            st.metric(
                "PnL",
                f"${pnl:,.2f}",
                f"{pnl_percent:.2f}%"
            )

        with c4:
            st.metric(
                "Positions",
                len(portfolio.positions)
            )

        st.subheader(
            "⚡ Market Scanner"
        )

        df_market = pd.DataFrame(market)

        st.dataframe(
            df_market,
            use_container_width=True
        )

        symbol = st.selectbox(
            "Inspect Asset",
            SYMBOLS
        )

        df = get_data(symbol)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                mode="lines",
                name=symbol
            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )