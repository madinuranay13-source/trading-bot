import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from core.state import SYMBOLS, INITIAL_CASH
from core.portfolio import Portfolio
from core.bot import Bot
from core.data import get_data


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="QUANT-X",
    page_icon="🚀",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}

h1, h2, h3 {
    color: white !important;
}

.stMetric {
    background-color: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

.stButton > button {
    width: 100%;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg, #ff00cc, #3333ff);
    color: white;
    font-weight: bold;
    font-size: 16px;
    padding: 12px;
}

.stButton > button:hover {
    transform: scale(1.03);
    transition: 0.2s;
}

[data-testid="stDataFrame"] {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------

st.markdown("""
<h1 style='text-align:center;'>🚀 QUANT-X AI TRADING TERMINAL</h1>
<p style='text-align:center; color:#d1d1ff;'>Gen-Z Quant Dashboard • AI Signals • Portfolio Tracking</p>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio(INITIAL_CASH)

if "bot" not in st.session_state:
    st.session_state.bot = Bot(st.session_state.portfolio)


# ---------------- SIDEBAR ----------------

st.sidebar.title("⚡ Control Center")

symbol = st.sidebar.selectbox(
    "Select Asset",
    SYMBOLS
)

risk = st.sidebar.slider(
    "Risk Level",
    1,
    10,
    5
)

trade_size = st.sidebar.slider(
    "Trade Size",
    1,
    10,
    1
)

mode = st.sidebar.radio(
    "Mode",
    ["Aggressive", "Balanced", "Safe"]
)


# ---------------- DATA ----------------

df = get_data(symbol)

if df is None or df.empty:
    st.error("No market data available")
    st.stop()


# ---------------- AI INDICATORS ----------------

close_prices = df["Close"]

sma_5 = close_prices.rolling(5).mean()
sma_20 = close_prices.rolling(20).mean()

latest_price = float(close_prices.values[-1])

momentum = round(((close_prices.iloc[-1] - close_prices.iloc[-5]) / close_prices.iloc[-5]) * 100, 2)

signal = "BUY" if sma_5.iloc[-1] > sma_20.iloc[-1] else "SELL"


# ---------------- KPI CARDS ----------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💵 Balance", f"${st.session_state.portfolio.cash:.2f}")

with col2:
    st.metric("📈 Price", f"${latest_price:.2f}")

with col3:
    st.metric("⚡ Momentum", f"{momentum}%")

with col4:
    st.metric("🤖 AI Signal", signal)


# ---------------- BUTTONS ----------------

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🤖 Execute AI Trade"):
        signal_result, price = st.session_state.bot.run(symbol)
        st.success(f"{signal_result} executed at ${price:.2f}")

with c2:
    if st.button("📊 Portfolio Value"):
        value = st.session_state.portfolio.value({
            symbol: latest_price
        })

        st.info(f"Total Portfolio Value: ${value:.2f}")

with c3:
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()


# ---------------- CHART ----------------

st.subheader("📈 Live Market Chart")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Price",
        line=dict(width=4)
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=sma_5,
        mode="lines",
        name="SMA 5"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=sma_20,
        mode="lines",
        name="SMA 20"
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=550,
    margin=dict(l=10, r=10, t=30, b=10)
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- POSITIONS ----------------

st.subheader("📦 Open Positions")

positions = st.session_state.portfolio.positions

positions_data = []

for stock, qty in positions.items():
    if qty > 0:
        positions_data.append({
            "Asset": stock,
            "Quantity": qty,
            "Mode": mode
        })

if positions_data:
    st.dataframe(pd.DataFrame(positions_data), use_container_width=True)

else:
    st.info("No open positions")


# ---------------- TRADE HISTORY ----------------

st.subheader("📜 Trade History")

history = st.session_state.portfolio.history

trade_data = []

for trade in history:
    trade_data.append({
        "Action": trade[0],
        "Symbol": trade[1],
        "Price": f"${trade[2]:.2f}",
        "Qty": trade[3]
    })

if trade_data:
    st.dataframe(pd.DataFrame(trade_data), use_container_width=True)

else:
    st.info("No trades yet")


# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    "<center>⚡ QUANT-X • AI Trading Dashboard • Built with Python + Streamlit</center>",
    unsafe_allow_html=True)