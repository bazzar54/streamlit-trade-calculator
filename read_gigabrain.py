from telethon.sync import TelegramClient
import re

# ✅ Your Telegram API credentials
api_id = 28243264
api_hash = '40aa41935065f94cd82c116a4f1427f1'
phone_number = '+447984222818'  # Replace this with your Telegram number

# 🔁 Group to pull from (use group name or username)
target_group = 'Gigabrain Alpha'  # Change this to the correct group if needed

with TelegramClient('gigabrain_session', api_id, api_hash) as client:
    client.start(phone=phone_number)

    print("✅ Connected to Telegram. Searching for signals...")

    for message in client.iter_messages(target_group, limit=20):
        if message.text and 'ENTRY' in message.text.upper():
            print("🔍 Found Signal Message:\n")
            print(message.text)

            # Try to extract direction, entry, TP, SL
            direction = re.search(r'(LONG|SHORT)', message.text.upper())
            entry = re.search(r'ENTRY\\s*[:=]?\\s*(\\d+\\.?\\d*)', message.text.upper())
            tp = re.search(r'TP\\s*[:=]?\\s*(\\d+\\.?\\d*)', message.text.upper())
            sl = re.search(r'SL\\s*[:=]?\\s*(\\d+\\.?\\d*)', message.text.upper())

            print(\"Parsed Details:\")
            print(\"Direction:\", direction.group(1) if direction else None)
            print(\"Entry:\", entry.group(1) if entry else None)
            print(\"Take Profit:\", tp.group(1) if tp else None)
            print(\"Stop Loss:\", sl.group(1) if sl else None)
            break
