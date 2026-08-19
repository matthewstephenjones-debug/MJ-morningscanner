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

    candidates = []

    for stock in movers:

        ticker = stock.get("ticker", "")

        price = stock.get("min", {}).get("c", 0)

        volume = stock.get("min", {}).get("av", 0)

        change = stock.get("todaysChangePerc", 0)

        dollar_volume = price * volume

        if (
            price > 1
            and volume > 100000
            and len(ticker) <= 5
        ):

            candidates.append({
                "ticker": ticker,
                "price": price,
                "change": change,
                "volume": volume,
                "dollar_volume": dollar_volume
            })

    candidates = sorted(
        candidates,
        key=lambda x: x["dollar_volume"],
        reverse=True
    )

    message = "🚀 MJ Morning Scanner V5\n\n"

    for i, stock in enumerate(candidates[:10], start=1):

        message += (
            f"{i}. {stock['ticker']}\n"
            f"💰 ${stock['price']:.2f}\n"
            f"🚀 +{stock['change']:.1f}%\n"
            f"💵 ${stock['dollar_volume']/1000000:.1f}m traded\n\n"
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
