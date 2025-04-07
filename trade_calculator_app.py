import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Crypto Profit Calculator", page_icon="🧮", layout="wide")
st.title("🧮 Crypto Trade Profit Calculator")
st.caption("Quickly calculate potential profits and losses on long/short trades with leverage.")

# --- Load Signal from CSV ---
CSV_PATH = "parsed_signals.csv"

if "loaded_signal" not in st.session_state:
    st.session_state.loaded_signal = False

if st.button("⚡️ Load Latest Gigabrain Signal"):
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        if not df.empty:
            latest = df.iloc[-1]
            st.session_state.trade_type = "Short"  # Default for now
            st.session_state.entry_price = float(latest["entry"])
            st.session_state.exit_price = float(latest["take_profit"])  # Assume user will take profit
            st.session_state.take_profit = float(latest["take_profit"])
            st.session_state.stop_loss = float(latest["stop_loss"])
            st.session_state.leverage = 5.0
            st.session_state.bet_gbp = 100.0
            st.session_state.loaded_signal = True
            st.success(f"✅ Signal loaded: {latest['token']} | Entry ${latest['entry']} | TP ${latest['take_profit']} | SL ${latest['stop_loss']}")
        else:
            st.warning("⚠️ Signal file is empty.")
    else:
        st.error("❌ Signal file not found.")

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    trade_type = st.selectbox("🔁 Trade Type", ["Short", "Long"],
        index=0 if st.session_state.get("trade_type", "Short") == "Short" else 1,
        help="Short = price goes down. Long = price goes up.")
    entry_price = st.number_input("🎯 Entry Price ($)", value=st.session_state.get("entry_price", 2.17), step=0.01)
    exit_price = st.number_input("🚪 Exit Price ($)", value=st.session_state.get("exit_price", 2.05), step=0.01)
    leverage = st.slider("⚡ Leverage", 1.0, 10.0, value=st.session_state.get("leverage", 3.0), step=0.5)

with col2:
    bet_gbp = st.number_input("💷 Your Bet (£)", value=st.session_state.get("bet_gbp", 100.0), step=10.0)
    take_profit = st.number_input("🟢 Take Profit Target ($)", value=st.session_state.get("take_profit", 2.05), step=0.01)
    stop_loss = st.number_input("🔴 Stop Loss Price ($)", value=st.session_state.get("stop_loss", 2.24), step=0.01)

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

# --- Display All Summaries in One Row ---
st.divider()
colA, colB, colC = st.columns(3)

with colA:
    st.markdown("### 📊 Trade Metrics")
    st.markdown(f"<span style='font-size:16px;'>💰 Est. Profit: £{profit:.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>💷 Final Balance: £{final_balance:.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>📊 Position Size: £{position_size:.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>🟢 Profit at TP: £{profit_tp:.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>🔴 Loss at SL: £{loss_sl:.2f}</span>", unsafe_allow_html=True)

    rr_color = "green" if risk_reward_ratio >= 2.0 else "red"
    rr_tip = "A good trade setup usually has at least a 2:1 risk/reward ratio."
    st.markdown(
        f"<span title='{rr_tip}' style='font-size:16px; font-weight:bold;'>"
        f"🔁 Risk/Reward: <span style='color:{rr_color}'>{risk_reward_ratio:.2f} : 1</span>"
        f"</span>",
        unsafe_allow_html=True
    )

with colB:
    st.markdown("### 🔍 Trade Setup Overview")
    st.markdown(f"<span style='font-size:16px;'>📉 Trade Type: {trade_type.upper()}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>💼 Entry Price: ${entry_price}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>🚪 Exit Price: ${exit_price}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>🟢 Take Profit: ${take_profit}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>🔴 Stop Loss: ${stop_loss}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>⚡ Leverage: {leverage}x</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px;'>💷 Bet Size: £{bet_gbp}</span>", unsafe_allow_html=True)

with colC:
    st.markdown("### 🧠 Trade Breakdown Summary")
    trade_direction = "you profit if the price <strong>drops</strong>" if trade_type.lower() == "short" else "you profit if the price <strong>goes up</strong>"
    summary_text = f"""
    <div style='font-size:16px;'>
    You’re using <strong>£{bet_gbp:.2f}</strong>, but with <strong>{leverage:.1f}x leverage</strong>, so you’re actually trading <strong>£{position_size:.2f}</strong>.<br><br>
    You’re <strong>{trade_type.lower()}ing</strong> — so {trade_direction}<br><br>
    Entry = <strong>${entry_price:.2f}</strong> → Exit = <strong>${exit_price:.2f}</strong> = a price move of <strong>${price_diff:.2f}</strong><br><br>
    That move = <strong>{price_move_percent_display:.2f}%</strong> of ${entry_price:.2f}<br>
    So your profit = <strong>{price_move_percent_display:.2f}% of £{position_size:.2f} = £{profit:.2f}</strong>
    </div>
    """
    st.markdown(summary_text, unsafe_allow_html=True)

# --- Chart ---
st.divider()
st.subheader("📈 Trade Setup Chart")

fig, ax = plt.subplots(figsize=(6, 2.5))
ax.axhline(entry_price, color="blue", linestyle="--", label=f"Entry: ${entry_price}")
ax.axhline(take_profit, color="green", linestyle="--", label=f"Take Profit: ${take_profit}")
ax.axhline(stop_loss, color="red", linestyle="--", label=f"Stop Loss: ${stop_loss}")
ax.axhline(exit_price, color="purple", linestyle="--", label=f"Exit: ${exit_price}")

# Zones
if trade_type.lower() == "short":
    if take_profit < entry_price:
        ax.fill_betweenx([take_profit, entry_price], 0, 1, color="green", alpha=0.1, label="Profit Zone")
    if stop_loss > entry_price:
        ax.fill_betweenx([entry_price, stop_loss], 0, 1, color="red", alpha=0.1, label="Loss Zone")
else:
    if take_profit > entry_price:
        ax.fill_betweenx([entry_price, take_profit], 0, 1, color="green", alpha=0.1, label="Profit Zone")
    if stop_loss < entry_price:
        ax.fill_betweenx([stop_loss, entry_price], 0, 1, color="red", alpha=0.1, label="Loss Zone")

ax.set_title("Visual of Your Trade Setup")
ax.set_xlabel("Timeline")
ax.set_ylabel("Price ($)")
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
ax.set_yticks(sorted(set([entry_price, exit_price, take_profit, stop_loss])))
ax.grid(True)

st.pyplot(fig)
st.caption("This tool is for educational and simulation purposes only. Always DYOR before investing.")
