import streamlit as st
import plotly.graph_objects as go

from core.state import SYMBOLS, INITIAL_CASH
from core.portfolio import Portfolio
from core.bot import Bot
from core.data import get_data


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Trading Simulator",
    layout="wide"
)

st.title("📊 AI Trading Simulator")


# ---------------- SESSION STATE ----------------

if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio(INITIAL_CASH)

if "bot" not in st.session_state:
    st.session_state.bot = Bot(st.session_state.portfolio)


# ---------------- STOCK SELECTOR ----------------

symbol = st.selectbox(
    "Select Stock",
    SYMBOLS
)


# ---------------- LOAD DATA ----------------

df = get_data(symbol)

if df is None or df.empty:
    st.error("No market data available")
    st.stop()


# ---------------- BUTTONS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🤖 Auto Trade"):
        signal, price = st.session_state.bot.run(symbol)

        st.success(
            f"{signal} executed at ${price:.2f}"
        )

with col2:
    if st.button("💰 Portfolio Value"):
        current_price = float(df["Close"].values[-1])

        value = st.session_state.portfolio.value({
            symbol: current_price
        })

        st.info(
            f"Total Portfolio Value: ${value:.2f}"
        )

with col3:
    if st.button("🔄 Refresh"):
        st.rerun()


# ---------------- CHART ----------------

st.subheader("📈 Price Chart")

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
    height=500,
    margin=dict(l=10, r=10, t=30, b=10)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------- CASH ----------------

st.subheader("💰 Cash")

st.metric(
    "Available Balance",
    f"${st.session_state.portfolio.cash:.2f}"
)


# ---------------- POSITIONS ----------------

st.subheader("📦 Positions")

positions = st.session_state.portfolio.positions

positions_data = []

for stock, qty in positions.items():
    if qty > 0:
        positions_data.append({
            "Symbol": stock,
            "Quantity": qty
        })

if positions_data:
    st.table(positions_data)

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
        "Quantity": trade[3]
    })

if trade_data:
    st.table(trade_data)

else:
    st.info("No trades yet")