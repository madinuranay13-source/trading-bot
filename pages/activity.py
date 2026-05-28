import streamlit as st
import pandas as pd


def render():

    st.title("📜 Activity Feed")

    history = (
        st.session_state
        .portfolio
        .history
    )

    if history:

        st.dataframe(
            pd.DataFrame(history),
            use_container_width=True
        )

    else:
        st.info(
            "No trades yet"
        )