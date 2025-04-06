import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Profit Calculator", page_icon="🧮", layout="wide")

st.title("🧮 Crypto Trade Profit Calculator")
st.caption("Quickly calculate potential profits and losses on long/short trades with leverage.")

# --- Load Signal Button + State ---
if "loaded_signal" not in st.session_state:
    st.session_state.loaded_signal = False

if st.button("⚡ Load Latest Gigabrain Signal"):
    st.session_state.trade_type = "Short"
    st.session_state.entry_price = 594.0
    st.session_state.exit_price = 580.0
    st.session_state.take_profit = 580.0
    st.session_state.stop_loss = 605.0
    st.session_state.leverage = 5.0
    st.session_state.bet_gbp = 100.0
    st.session_state.loaded_signal = True
    st.success("✅ Signal loaded: SHORT | Entry $594 | TP $580 | SL $605")

# --- Trade Inputs with session_state defaults ---
col1, col2 = st.columns(2)

with col1:
    trade_type = st.selectbox("🔁 Trade Type", ["Short", "Long"],
        index=0 if st.session_state.get("trade_type", "Short") == "Short" else 1,
        help="Short = price goes down. Long = price goes up."
    )
    entry_price = st.number_input("🎯 Entry Price ($)", value=st.session_state.get("entry_price", 2.17), step=0.01)
    exit_price = st.number_input("🚪 Exit Price ($)", value=st.session_state.get("exit_price", 2.05), step=0.01)
    leverage = st.slider("⚡ Leverage", 1.0, 10.0, value=st.session_state.get("leverage", 3.0), step=0.5,
        help="Leverage lets you trade more than your own capital. 3x leverage on £100 = £300 position.")

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

# --- Display Metrics ---
st.divider()
colA, colB, colC = st.columns(3)

with colA:
    st.metric("💰 Est. Profit", f"£{profit:.2f}")
    st.metric("💷 Final Balance", f"£{final_balance:.2f}")
    st.metric("📊 Position Size", f"£{position_size:.2f}")

with colB:
    st.metric("🟢 Profit at TP", f"£{profit_tp:.2f}")
    st.metric("🔴 Loss at SL", f"£{loss_sl:.2f}")

    # Risk/Reward with tooltip + color
    rr_color = "green" if risk_reward_ratio >= 2.0 else "red"
    st.markdown(
        f"<span title='A good trade setup usually has at least a 2:1 risk/reward ratio.'>"
        f"🔁 <strong style='color:{rr_color}'>Risk/Reward: {risk_reward_ratio:.2f} : 1</strong>"
        f"</span>",
        unsafe_allow_html=True
    )

with colC:
    st.markdown("### ✅ Summary")
    st.markdown(f"• Trade Type: **{trade_type}**")
    st.markdown(f"• Entry: **${entry_price}**")
    st.markdown(f"• Exit: **${exit_price}**")
    st.markdown(f"• Take Profit: **${take_profit}**")
    st.markdown(f"• Stop Loss: **${stop_loss}**")
    st.markdown(f"• Leverage: **{leverage}x**")
    st.markdown(f"• Bet: **£{bet_gbp}**")

# --- Trade Setup Chart with Zones ---
st.divider()
st.subheader("📈 Trade Setup Chart")

fig, ax = plt.subplots(figsize=(6, 2.5))
ax.axhline(entry_price, color="blue", linestyle="--", label=f"Entry: ${entry_price}")
ax.axhline(take_profit, color="green", linestyle="--", label=f"Take Profit: ${take_profit}")
ax.axhline(stop_loss, color="red", linestyle="--", label=f"Stop Loss: ${stop_loss}")
ax.axhline(exit_price, color="purple", linestyle="--", label=f"Exit: ${exit_price}")

# Profit/Loss Zones
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

# Final Touches
ax.set_title("Visual of Your Trade Setup")
ax.set_xlabel("Timeline")
ax.set_ylabel("Price ($)")
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
ax.set_yticks(sorted(set([entry_price, exit_price, take_profit, stop_loss])))
ax.grid(True)

st.pyplot(fig)
st.caption("This tool is for educational and simulation purposes only. Always DYOR before investing.")
