import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Profit Calculator", page_icon="🧮", layout="wide")
st.title("🧮 Crypto Trade Profit Calculator")
st.caption("Quickly calculate potential profits and losses on long/short trades with leverage.")

# --- Load Simulated Signal ---
if "loaded_signal" not in st.session_state:
    st.session_state.loaded_signal = False

if st.button("\u26a1\ufe0f Load Latest Gigabrain Signal"):
    st.session_state.trade_type = "Short"
    st.session_state.entry_price = 594.0
    st.session_state.exit_price = 580.0
    st.session_state.take_profit = 580.0
    st.session_state.stop_loss = 605.0
    st.session_state.leverage = 5.0
    st.session_state.bet_gbp = 100.0
    st.session_state.loaded_signal = True
    st.success("\u2705 Signal loaded: SHORT | Entry $594 | TP $580 | SL $605")

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    trade_type = st.selectbox("\ud83d\udd01 Trade Type", ["Short", "Long"],
        index=0 if st.session_state.get("trade_type", "Short") == "Short" else 1,
        help="Short = price goes down. Long = price goes up.")
    entry_price = st.number_input("\ud83c\udfaf Entry Price ($)", value=st.session_state.get("entry_price", 2.17), step=0.01)
    exit_price = st.number_input("\ud83d\udeaa Exit Price ($)", value=st.session_state.get("exit_price", 2.05), step=0.01)
    leverage = st.slider("\u26a1 Leverage", 1.0, 10.0, value=st.session_state.get("leverage", 3.0), step=0.5)

with col2:
    bet_gbp = st.number_input("\ud83d\udcb7 Your Bet (£)", value=st.session_state.get("bet_gbp", 100.0), step=10.0)
    take_profit = st.number_input("\ud83d\udfe2 Take Profit Target ($)", value=st.session_state.get("take_profit", 2.05), step=0.01)
    stop_loss = st.number_input("\ud83d\udd34 Stop Loss Price ($)", value=st.session_state.get("stop_loss", 2.24), step=0.01)

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

# --- Metrics ---
with colA:
    st.markdown("### 📊 Trade Metrics")
    st.markdown(f"**💰 Est. Profit:** £{profit:.2f}")
    st.markdown(f"**💷 Final Balance:** £{final_balance:.2f}")
    st.markdown(f"**📊 Position Size:** £{position_size:.2f}")
    st.markdown(f"**🟢 Profit at TP:** £{profit_tp:.2f}")
    st.markdown(f"**🔴 Loss at SL:** £{loss_sl:.2f}")

    rr_color = "green" if risk_reward_ratio >= 2.0 else "red"
    rr_tip = "A good trade setup usually has at least a 2:1 risk/reward ratio."
    st.markdown(
        f"<span title='{rr_tip}' style='font-size: 16px; font-weight:bold;'>"
        f"🔁 Risk/Reward: <span style='color:{rr_color}'>{risk_reward_ratio:.2f} : 1</span>"
        f"</span>",
        unsafe_allow_html=True
    )

# --- Trade Setup Overview ---
with colB:
    st.markdown("### 🔍 Trade Setup Overview")
    st.markdown(f"**📉 Trade Type:** `{trade_type.upper()}`")
    st.markdown(f"**💼 Entry Price:** ${entry_price}")
    st.markdown(f"**🚪 Exit Price:** ${exit_price}")
    st.markdown(f"**🟢 Take Profit:** ${take_profit}")
    st.markdown(f"**🔴 Stop Loss:** ${stop_loss}")
    st.markdown(f"**⚡ Leverage:** {leverage}x")
    st.markdown(f"**💷 Bet Size:** £{bet_gbp}")

# --- Trade Breakdown Summary ---
with colC:
    st.markdown("### 🧠 Trade Breakdown Summary")
    trade_direction = "you profit if the price **drops**" if trade_type.lower() == "short" else "you profit if the price **goes up**"
    summary_text = f"""
    You’re using **£{bet_gbp:.2f}**, but with **{leverage:.1f}x leverage**, so you’re actually trading **£{position_size:.2f}**.

    You’re **{trade_type.lower()}ing** — so {trade_direction}  

    **Entry = ${entry_price:.2f} → Exit = ${exit_price:.2f}** = a price move of **${price_diff:.2f}**

    That move = **{price_move_percent_display:.2f}%** of ${entry_price:.2f}  
    So your profit = **{price_move_percent_display:.2f}% of £{position_size:.2f} = £{profit:.2f}**
    """
    st.markdown(summary_text)

# --- Chart ---
st.divider()
st.subheader("\ud83d\udcc8 Trade Setup Chart")

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

