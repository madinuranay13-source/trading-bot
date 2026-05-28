import streamlit as st
import pandas as pd
import plotly.express as px


def render():

    st.title("💼 Portfolio Analytics")

    portfolio = st.session_state.portfolio

    positions = []

    for symbol, qty in (
        portfolio.positions.items()
    ):

        if qty > 0:

            positions.append({
                "Symbol": symbol,
                "Quantity": qty
            })

    if positions:

        df = pd.DataFrame(
            positions
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        fig = px.pie(
            df,
            names="Symbol",
            values="Quantity",
            title="Portfolio Allocation"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No active positions"
        )