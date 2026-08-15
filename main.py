import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = """
🚀 MJ Morning Scanner

1. TEST +28%
Volume: 1.3m

2. TEST +24%
Volume: 950k

3. TEST +21%
Volume: 1.1m
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Message sent")
