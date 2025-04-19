import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Crypto Trade Setup Calculator", layout="centered")
st.title("📈 Crypto Trade Setup Calculator")

# Load Gigabrain signal from CSV
def load_signal():
    csv_path = "parsed_signals.csv"
    if not os.path.exists(csv_path):
        st.error("❌ Signal file not found.")
        return
    df = pd.read_csv(csv_path)
    if df.empty:
        st.warning("⚠️ No signals in CSV.")
        return
    latest = df.iloc[0]
    st.session_state["entry"] = float(latest["entry"])
    st.session_state["take_profit"] = float(latest["take_profit"])
    st.session_state["stop_loss"] = float(latest["stop_loss"])
    st.session_state["leverage"] = float(latest["leverage"].split("-")[0]) if "-" in latest["leverage"] else float(latest["leverage"])
    st.session_state["asset"] = latest["asset"]
    st.session_state["confidence"] = latest["confidence"]
    st.session_state["duration"] = latest["duration"]
    st.success("✅ Signal loaded from Telegram!")

# Load button
st.button("📡 Load Latest Gigabrain Signal", on_click=load_signal)

# --- Trade Form ---
st.subheader("📝 Trade Setup")

trade_direction = st.selectbox("Trade Direction", ["Long", "Short"])
entry = st.number_input("Entry Price", value=st.session_state.get("entry", 0.0))
stop_loss = st.number_input("Stop Loss", value=st.session_state.get("stop_loss", 0.0))
take_profit = st.number_input("Take Profit", value=st.session_state.get("take_profit", 0.0))
position_size = st.number_input("Position Size (USDT)", value=100.0)
leverage = st.number_input("Leverage", value=st.session_state.get("leverage", 3.0))

# --- Calculator Logic ---
if st.button("Calculate"):
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)
    rr_ratio = round(reward / risk, 2) if risk else 0
    liquidation = round(entry - (entry / leverage), 4) if trade_direction == "Long" else round(entry + (entry / leverage), 4)

    st.markdown("### 📊 Results")
    st.write(f"📌 Asset: {st.session_state.get('asset', 'N/A')}")
    st.write(f"🎯 R:R Ratio: `{rr_ratio}`")
    st.write(f"💥 Est. Liquidation Price: `{liquidation}`")
    st.write(f"📅 Duration: {st.session_state.get('duration', 'N/A')}")
    st.write(f"📈 Confidence: {st.session_state.get('confidence', 'N/A')}%")
