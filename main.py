import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_KEY = os.environ["POLYGON_API_KEY"]

url = f"https://api.massive.com/v2/snapshot/locale/us/markets/stocks/gainers?apiKey={API_KEY}"

try:
    response = requests.get(url)
    data = response.json()

    message = "DEBUG\n\n"
    message += str(data)[:3500]

except Exception as e:
    message = f"ERROR\n\n{str(e)}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

