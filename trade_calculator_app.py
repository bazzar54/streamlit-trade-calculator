import streamlit as st

st.set_page_config(page_title="Crypto Profit Calculator", page_icon="🧮")

st.title("🧮 Crypto Trade Profit Calculator")

st.markdown("Easily test your profit/loss from long or short trades in crypto using leverage.")

# --- Inputs ---
trade_type = st.selectbox("Trade Type", ["Short", "Long"], help="Select 'Long' if you think the price will go up, or 'Short' if you think it will go down.")
entry_price = st.number_input("Entry Price ($)", value=2.17, step=0.01, help="The price you enter the trade at (buy or sell).")
exit_price = st.number_input("Exit Price ($)", value=2.05, step=0.01, help="The price you plan to exit the trade.")
leverage = st.slider("Leverage", 1.0, 10.0, 3.0, 0.5, help="Leverage lets you control a bigger position with a smaller amount of money. For example, 3x leverage on £100 = £300 position.")
bet_gbp = st.number_input("Your Bet (£)", value=100.0, step=10.0, help="The amount of your own money you're putting into the trade.")
take_profit = st.number_input("Take Profit Target ($)", value=2.05, step=0.01, help="Target price where you want to close the trade for profit.")
stop_loss = st.number_input("Stop Loss Price ($)", value=2.24, step=0.01, help="Price where you will exit if the trade goes against you.")

# --- Position size ---
position_size = bet_gbp * leverage
st.info(f"📊 **Your Position Size:** £{position_size:.2f} (Bet × Leverage)")

# --- Profit Calculation (main exit price) ---
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

# --- Risk/Reward Calculation ---
risk = abs(loss_sl)
reward = abs(profit_tp)
risk_reward_ratio = reward / risk if risk != 0 else 0

# --- Results ---
st.markdown("---")
st.subheader("📈 Main Exit Result")
st.success(f"💰 **Estimated Profit:** £{profit:.2f}")
st.info(f"📦 **Final Account Value:** £{final_balance:.2f}")

st.markdown("---")
st.subheader("📊 Stop Loss / Take Profit Overview")
st.warning(f"❌ **Potential Loss at Stop Loss:** £{loss_sl:.2f}")
st.success(f"🎯 **Potential Profit at Take Profit:** £{profit_tp:.2f}")
st.markdown(f"🔁 **Risk/Reward Ratio:** `{risk_reward_ratio:.2f}`")

st.caption("This tool is for educational and simulation purposes only. Always DYOR before investing.")
