import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set wide layout
st.set_page_config(page_title="Crypto Trade Calculator", layout="wide")

st.markdown("""
    <style>
    .big-font { font-size:18px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Crypto Trade Setup Calculator")

# Default state values
defaults = {
    "direction": "Long",
    "entry": 0.0,
    "stop_loss": 0.0,
    "take_profit": 0.0,
    "position_size": 100.0,
    "leverage": 3
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Load latest signal from CSV
if st.button("📡 Load Latest Gigabrain Signal"):
    try:
        df = pd.read_csv("parsed_signals.csv")
        latest = df.iloc[-1]
        st.success(f"✅ Loaded signal: {latest['token']}")
        st.session_state.entry = float(latest["entry"])
        st.session_state.stop_loss = float(latest["stop_loss"])
        st.session_state.take_profit = float(latest["take_profit"])
        st.session_state.position_size = 100.0
        st.session_state.leverage = 3
    except Exception as e:
        st.error(f"❌ Failed to load signal: {e}")

# Layout
left, right = st.columns([1.3, 1])

# Form: Inputs
with left:
    st.subheader("📝 Trade Setup")
    with st.form("trade_form"):
        direction = st.selectbox("Trade Direction", ["Long", "Short"], key="direction")
        entry = st.number_input("Entry Price", min_value=0.0, format="%.6f", key="entry")
        stop_loss = st.number_input("Stop Loss", min_value=0.0, format="%.6f", key="stop_loss")
        take_profit = st.number_input("Take Profit", min_value=0.0, format="%.6f", key="take_profit")
        position_size = st.number_input("Position Size (USDT)", min_value=0.0, format="%.2f", key="position_size")
        leverage = st.number_input("Leverage", min_value=1, step=1, key="leverage")
        submitted = st.form_submit_button("Calculate")

# Right side: Output
with right:
    if submitted:
        if entry <= 0 or stop_loss <= 0 or take_profit <= 0 or position_size <= 0:
            st.error("❌ Please enter values greater than zero.")
        else:
            trade_value = position_size * leverage
            risk_amount = abs(entry - stop_loss) * (position_size / entry)
            reward_amount = abs(take_profit - entry) * (position_size / entry)
            risk_to_reward = round(reward_amount / risk_amount, 2) if risk_amount != 0 else float("inf")
            pnl = round(reward_amount - risk_amount, 2)

            st.subheader("📘 Trade Summary")
            st.markdown(f"""
                <div class="big-font">
                <b>🧭 Direction:</b> {direction} <br>
                <b>💵 Entry:</b> ${entry:.6f} <br>
                <b>🛑 Stop Loss:</b> ${stop_loss:.6f} <br>
                <b>🎯 Take Profit:</b> ${take_profit:.6f} <br>
                <b>💰 Position Size:</b> ${position_size:.2f} <br>
                <b>⚙️ Leverage:</b> {leverage}× <br>
                <b>📈 Trade Value:</b> ${trade_value:.2f} <br>
                <b>📉 Risk Amount:</b> ${risk_amount:.2f} <br>
                <b>🚀 Reward Amount:</b> ${reward_amount:.2f} <br>
                </div>
            """, unsafe_allow_html=True)

            st.subheader("📊 Trade Metrics")
            st.markdown(f"""
                <div class="big-font">
                <b>📐 Risk to Reward:</b> {risk_to_reward} <br>
                <b>💹 Estimated Net PnL:</b> ${pnl:.2f}
                </div>
            """, unsafe_allow_html=True)

    with st.expander("📈 Show Trade Chart (optional)"):
        if submitted:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=["Entry", "Stop Loss", "Take Profit"],
                y=[entry, stop_loss, take_profit],
                mode="markers+lines",
                marker=dict(size=10),
                name="Trade Levels"
            ))
            fig.update_layout(title="Trade Price Levels", height=400, yaxis_title="Price")
            st.plotly_chart(fig)
