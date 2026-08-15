import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_KEY = os.environ["FINNHUB_API_KEY"]

url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"

r = requests.get(url)

message = str(r.json())[:3500]

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

