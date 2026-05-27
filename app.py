import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from core.state import SYMBOLS, INITIAL_CASH
from core.portfolio import Portfolio
from core.auto_trader import AutoTrader
from core.data import get_data


# ---------------- PAGE ----------------

st.set_page_config(
    page_title="QUANT-X V2",
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

.stMetric {
    background-color: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 15px;
}

.stButton > button {
    width: 100%;
    border-radius: 15px;
    background: linear-gradient(90deg, #ff00cc, #3333ff);
    color: white;
    font-weight: bold;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------

st.markdown(
    "<h1 style='text-align:center;'>🚀 QUANT-X V2</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<center>Autonomous AI Trading Terminal</center>",
    unsafe_allow_html=True
)


# ---------------- SESSION ----------------

if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio(INITIAL_CASH)

if "trader" not in st.session_state:
    st.session_state.trader = AutoTrader(
        st.session_state.portfolio
    )


# ---------------- AUTO TRADE ----------------

with st.spinner("Scanning market..."):
    market = st.session_state.trader.auto_trade(SYMBOLS)


# ---------------- KPIs ----------------

portfolio_value = st.session_state.portfolio.value({
    stock["symbol"]: stock["price"]
    for stock in market
})

buy_count = len([
    s for s in market
    if s["signal"] == "BUY"
])

sell_count = len([
    s for s in market
    if s["signal"] == "SELL"
])

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💰 Portfolio", f"${portfolio_value:.2f}")

with c2:
    st.metric("📈 Buy Signals", buy_count)

with c3:
    st.metric("📉 Sell Signals", sell_count)

with c4:
    st.metric(
        "📦 Positions",
        len(st.session_state.portfolio.positions)
    )


# ---------------- MARKET TABLE ----------------

st.subheader("⚡ AI Market Scanner")

market_df = pd.DataFrame(market)

st.dataframe(
    market_df,
    use_container_width=True
)


# ---------------- CHART ----------------

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

st.plotly_chart(fig, use_container_width=True)


# ---------------- POSITIONS ----------------

st.subheader("📦 Portfolio Positions")

positions = []

for stock, qty in st.session_state.portfolio.positions.items():
    if qty > 0:
        positions.append({
            "Stock": stock,
            "Quantity": qty
        })

if positions:
    st.dataframe(
        pd.DataFrame(positions),
        use_container_width=True
    )

else:
    st.info("No active positions")


# ---------------- HISTORY ----------------

st.subheader("📜 Trade History")

history = []

for trade in st.session_state.portfolio.history:
    history.append({
        "Action": trade[0],
        "Stock": trade[1],
        "Price": trade[2],
        "Qty": trade[3]
    })

if history:
    st.dataframe(
        pd.DataFrame(history),
        use_container_width=True
    )

else:
    st.info("No trades yet")