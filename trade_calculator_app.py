import streamlit as st

st.set_page_config(page_title="Crypto Profit Calculator", page_icon="🧮")

st.title("🧮 Crypto Trade Profit Calculator")

st.markdown("Easily test your profit/loss from long or short trades in crypto using leverage.")

# 🔁 Trade type
trade_type = st.selectbox("Trade Type", ["Short", "Long"], help="Select 'Long' if you think the price will go up, or 'Short' if you think it will go down.")

# 💸 Entry price
entry_price = st.number_input("Entry Price ($)", value=2.175, step=0.01, help="The price you enter the trade at (buy or sell).")

# 🎯 Exit price
exit_price = st.number_input("Exit Price ($)", value=2.05, step=0.01, help="The price you plan to exit the trade.")

# ⚡ Leverage
leverage = st.slider("Leverage", 1.0, 10.0, 3.0, 0.5, help="Leverage lets you control a bigger position with a smaller amount of money. For example, 3x leverage on £100 = £300 position.")

# 💷 Your bet
bet_gbp = st.number_input("Your Bet (£)", value=100.0, step=10.0, help="The amount of your own money you're putting into the trade.")

# 🔢 Position size calculation
position_size = bet_gbp * leverage
st.info(f"📊 **Your Position Size:** £{position_size:.2f} (Bet × Leverage)")

# 🧮 Profit calculation
if trade_type.lower() == "short":
    price_move_percent = (entry_price - exit_price) / entry_price_

