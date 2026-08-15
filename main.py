import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_KEY = os.environ["POLYGON_API_KEY"]

try:
    url = f"https://api.massive.com/v2/snapshot/locale/us/markets/stocks/gainers?apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    movers = data.get("tickers", [])

    message = "🚀 MJ Morning Scanner\n\nTop Market Movers\n\n"

    for i, stock in enumerate(movers[:10], start=1):

        ticker = stock.get("ticker", "N/A")

        change = stock.get("todaysChangePerc", 0)

        volume = stock.get("day", {}).get("v", 0)

        message += (
            f"{i}. {ticker}\n"
            f"Change: {change:.2f}%\n"
            f"Volume: {volume:,}\n\n"
        )

except Exception as e:
    message = f"❌ Error\n\n{str(e)}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
