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

    filtered = []

    for stock in movers:

        ticker = stock.get("ticker", "").upper()
        volume = stock.get("day", {}).get("v", 0)
        price = stock.get("day", {}).get("c", 0)

        if (
            volume > 1000000
            and price > 2
            and len(ticker) <= 5
        ):
            filtered.append(stock)

    message = "🚀 MJ Morning Scanner V3\n\n"

    if len(filtered) == 0:
        message += "No qualifying movers found."

    else:

        for i, stock in enumerate(filtered[:20], start=1):

            ticker = stock.get("ticker", "N/A")
            change = stock.get("todaysChangePerc", 0)
            volume = stock.get("day", {}).get("v", 0)
            price = stock.get("day", {}).get("c", 0)

            message += (
                f"{i}. {ticker}\n"
                f"💰 ${price:.2f}\n"
                f"🚀 +{change:.1f}%\n"
                f"📊 Vol {volume:,.0f}\n\n"
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
