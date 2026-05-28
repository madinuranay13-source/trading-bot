import os
import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.state import (
    INITIAL_CASH
)

from core.portfolio import Portfolio
from core.auto_trader import AutoTrader


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="QUANT-X V4",
    page_icon="🚀",
    layout="wide"
)


# ---------------- SESSION ----------------

if "portfolio" not in st.session_state:

    st.session_state.portfolio = Portfolio(
        INITIAL_CASH
    )

if "trader" not in st.session_state:

    st.session_state.trader = AutoTrader(
        st.session_state.portfolio
    )


# ---------------- SIDEBAR ----------------

st.sidebar.title("🚀 QUANT-X")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Strategy Lab",
        "Portfolio Analytics",
        "Activity Feed"
    ]
)


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    from pages.dashboard import render

    render()


# ---------------- STRATEGY LAB ----------------

elif page == "Strategy Lab":

    from pages.strategy_lab import render

    render()


# ---------------- PORTFOLIO ----------------

elif page == "Portfolio Analytics":

    from pages.portfolio_page import render

    render()


# ---------------- ACTIVITY ----------------

elif page == "Activity Feed":

    from pages.activity import render

    render()