import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Profit Calculator", page_icon="🧮", layout="wide")

st.title("🧮 Crypto Trade Profit Calculator")
st.caption("Quickly calculate potential profits and losses on long/short trades with leverage.")

# --- 1. Input layout with 2 columns ---
col1, col2 = st.columns(2)

with col1:
    trade_type = st.selectbox("🔁 Trade Type", ["Short", "Long"], help="Short = price goes down. Long = price goes up.")
    entry_price = st.number_input("🎯 Entry Price ($)", value=2.17, step=0.01, help="Price you enter the trade.")
    exit_price = st.number_input("🚪 Exit Price ($)", value=2.05, step=0.01, help="Price you plan to exit the trade.")
    leverage = st.slider("⚡ Leverage", 1.0, 10.0, 3.0, 0.5, help="3x leverage on £100 = £300 position.")

with col2:
    bet_gbp = st.number_input("💷 Your Bet (£)", value=100.0, step=10.0, help="Your own money in the trade.")
    take_profit = st.number_input("🟢 Take Profit Target ($)", value=2.05, step=0.01, help="Your ideal exit for profit.")
    stop_loss = st.number_input("🔴 Stop Loss Price ($)", value=2.24, step=0.01, help="The price you'll exit if trade goes bad.")

# --- 2. Calculations ---
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

# --- 3. Display Metrics Neatly ---
st.divider()
colA, colB, colC = st.columns(3)

with colA:
    st.metric("💰 Est. Profit", f"£{profit:.2f}")
    st.metric("💷 Final Balance", f"£{final_balance:.2f}")
    st.metric("📊 Position Size", f"£{position_size:.2f}")

with colB:
    st.metric("🟢 Profit at TP", f"£{profit_tp:.2f}")
    st.metric("🔴 Loss at SL", f"£{loss_sl:.2f}")
    st.metric("🔁 Risk/Reward", f"{risk_reward_ratio:.2f} : 1")

with colC:
    st.markdown("### ✅ Summary")
    st.markdown(f"• Trade Type: **{trade_type}**")
    st.markdown(f"• Entry: **${entry_price}**")
    st.markdown(f"• Exit: **${exit_price}**")
    st.markdown(f"• Take Profit: **${take_profit}**")
    st.markdown(f"• Stop Loss: **${stop_loss}**")
    st.markdown(f"• Leverage: **{leverage}x**")
    st.markdown(f"• Bet: **£{bet_gbp}**")

# --- 4. Simple Visual Trade Chart (with annotations) ---
st.divider()
st.subheader("📈 Trade Setup Chart")

fig, ax = plt.subplots(figsize=(6, 2.5))

# Plot price levels
ax.axhline(entry_price, color="blue", linestyle="--", label=f"Entry: ${entry_price}")
ax.axhline(take_profit, color="green", linestyle="--", label=f"Take Profit: ${take_profit}")
ax.axhline(stop_loss, color="red", linestyle="--", label=f"Stop Loss: ${stop_loss}")
ax.axhline(exit_price, color="purple", linestyle="--", label=f"Exit: ${exit_price}")

# Fill profit/loss zones
if trade_type.lower() == "short":
    if take_profit < entry_price:
        ax.fill_betweenx([take_profit, entry_price], x1=0, x2=1, color="green", alpha=0.1, label="Profit Zone")
    if stop_loss > entry_price:
        ax.fill_betweenx([entry_price, stop_loss], x1=0, x2=1, color="red", alpha=0.1, label="Loss Zone")
else:
    if take_profit > entry_price:
        ax.fill_betweenx([entry_price, take_profit], x1=0, x2=1, color="green", alpha=0.1, label="Profit Zone")
    if stop_loss < entry_price:
        ax.fill_betweenx([stop_loss, entry_price], x1=0, x2=1, color="red", alpha=0.1, label="Loss Zone")

# Clean up chart
ax.set_title("Visual of Your Trade Setup")
ax.set_xlabel("Timeline")
ax.set_ylabel("Price ($)")
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
ax.set_yticks(sorted(set([entry_price, take_profit, stop_loss, exit_price])))
ax.grid(True)

st.pyplot(fig)

