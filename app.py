import streamlit as st
import sys
import os
import plotly.graph_objects as go

# Ensure project root is visible (fixes import issues in cloud)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.state import SYMBOLS, INITIAL_CASH
from core.portfolio import Portfolio
from core.bot import Bot
from core.data import get_data


# ---------------- UI SETUP ----------------
st.set_page_config(page_title="Trading Bot", layout="wide")
st.title("📊 AI Trading Simulator (Stable Version)")


# ---------------- SESSION STATE ----------------
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio(INITIAL_CASH)
    st.session_state.bot = Bot(st.session_state.portfolio)


# ---------------- SYMBOL SELECTION ----------------
symbol = st.selectbox("Select Stock", SYMBOLS)


# ---------------- DATA LOADING (SAFE) ----------------
df = get_data(symbol)

if df is None or df.empty:
    st.error("⚠️ No market data available (yfinance/cloud limitation)")
    st.stop()

st.subheader("📊 Price Data Preview")
st.dataframe(df.tail())


# ---------------- BUTTONS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🤖 Auto Trade"):
        signal, price = st.session_state.bot.run(symbol)
        st.success(f"Signal: {signal} | Price: {price:.2f}")

with col2:
    if st.button("💰 Portfolio Value"):
        price = df["Close"].iloc[-1]
        value = st.session_state.portfolio.value({symbol: price})
        st.info(f"Total Portfolio Value: ${value:.2f}")

with col3:
    if st.button("🔄 Refresh"):
        st.rerun()


# ---------------- CHART ----------------
st.subheader("📈 Price Chart")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Close"],
    mode="lines",
    name="Close Price"
))

fig.update_layout(
    height=500,
    margin=dict(l=10, r=10, t=30, b=10)
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- PORTFOLIO ----------------
st.subheader("📦 Portfolio")

st.write("Cash:", round(st.session_state.portfolio.cash, 2))
st.write("Positions:", st.session_state.portfolio.positions)
st.write("Trade History:", st.session_state.portfolio.history)