import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Crypto Trade Calculator", page_icon="🧮", layout="wide")
st.markdown("<style>body { margin-top: -50px; } .stSlider { margin-top: -10px; } .stColumn > div { margin-bottom: -20px; }</style>", unsafe_allow_html=True)

st.title("Crypto Trade Calculator")
st.caption("Calculate potential profits/losses from Gigabrain signals.")

CSV_PATH = os.path.expanduser("~/Desktop/gigabrainhyperbot/parsed_signals.csv")

# --- Load Signal from CSV ---
if "loaded_signal" not in st.session_state:
    st.session_state.loaded_signal = False

latest_token = ""

if st.button("⚡ Load Latest Gigabrain Signal"):
    try:
        df = pd.read_csv(CSV_PATH).dropna(how='all')
        if not df.empty:
            latest = df.iloc[-1]
            st.session_state.trade_type = "Short"
            st.session_state.entry_price = float(latest["entry"])
            st.session_state.exit_price = float(latest["take_profit"])
            st.session_state.take_profit = float(latest["take_profit"])
            st.session_state.stop_loss = float(latest["stop_loss"])
            st.session_state.leverage = 5.0
            st.session_state.bet_gbp = 100.0
            st.session_state.loaded_signal = True
            latest_token = latest["token"]
            st.success(f"✅ Latest signal loaded: Token: {latest_token} | Entry: {latest['entry']} | TP: {latest['take_profit']} | SL: {latest['stop_loss']}")
        else:
            st.warning("⚠️ The CSV is empty.")
    except Exception as e:
        st.error(f"❌ Error loading signal: {e}")

if st.session_state.get("loaded_signal"):
    st.markdown(f"## 🔥 Token: <span style='color:#ff4b4b'>{latest_token}</span>", unsafe_allow_html=True)

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    trade_type = st.selectbox("Trade Type", ["Short", "Long"], index=0 if st.session_state.get("trade_type", "Short") == "Short" else 1)
    entry_price = st.number_input("Entry Price ($)", value=st.session_state.get("entry_price", 2.17), step=0.01)
    exit_price = st.number_input("Exit Price ($)", value=st.session_state.get("exit_price", 2.05), step=0.01)
    leverage = st.slider("Leverage", 1.0, 10.0, value=st.session_state.get("leverage", 3.0), step=0.5)

with col2:
    bet_gbp = st.number_input("Your Bet (£)", value=st.session_state.get("bet_gbp", 100.0), step=10.0)
    take_profit = st.number_input("Take Profit ($)", value=st.session_state.get("take_profit", 2.05), step=0.01)
    stop_loss = st.number_input("Stop Loss ($)", value=st.session_state.get("stop_loss", 2.24), step=0.01)

# --- Calculations ---
position_size = bet_gbp * leverage

if trade_type.lower() == "short":
    price_move_percent = (entry_price - exit_price) / entry_price
    tp_percent = (entry_price - take_profit) / entry_price
    sl_percent = (entry_price - stop_loss) / entry_price
else:
    price_move_percent = (exit_price - entry_price) / entry_price
    tp_percent = (take_profit - entry_price) / entry_price
    sl_percent = (stop_loss - entry_price) / entry_price

profit = price_move_percent * position_size
profit_tp = tp_percent * position_size
loss_sl = sl_percent * position_size
final_balance = bet_gbp + profit
risk = abs(loss_sl)
reward = abs(profit_tp)
risk_reward_ratio = reward / risk if risk != 0 else 0
price_diff = abs(entry_price - exit_price)
price_move_percent_display = abs(price_move_percent) * 100

# --- Summary Layout ---
st.markdown("<style>h3 { margin-bottom: 0.5rem; } .stColumn { padding-top: 0; }</style>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### 🧮 Metrics")
    st.write(f"• Profit: £{profit:.2f}")
    st.write(f"• Balance: £{final_balance:.2f}")
    st.write(f"• Size: £{position_size:.2f}")
    st.write(f"• TP Profit: £{profit_tp:.2f}")
    st.write(f"• SL Loss: £{loss_sl:.2f}")
    st.markdown(f"• Risk/Reward: <span style='color:{'green' if risk_reward_ratio >= 2 else 'red'}'>{risk_reward_ratio:.2f} : 1</span>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📋 Setup")
    st.write(f"• Type: {trade_type.upper()}")
    st.write(f"• Entry: ${entry_price}")
    st.write(f"• Exit: ${exit_price}")
    st.write(f"• TP: ${take_profit}")
    st.write(f"• SL: ${stop_loss}")
    st.write(f"• Leverage: {leverage}x")

with col3:
    st.markdown("### 🧠 Summary")
    st.write(f"Using £{bet_gbp:.2f} at {leverage:.1f}x leverage → £{position_size:.2f}")
    st.write(f"You profit if price goes {'down' if trade_type.lower() == 'short' else 'up'}")
    st.write(f"Entry = {entry_price}, Exit = {exit_price} → Move = ${price_diff:.2f} ({price_move_percent_display:.2f}%)")
