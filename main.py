import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_KEY = os.environ["FINNHUB_API_KEY"]

message = "🚀 MJ Morning Scanner\n\n"

try:
    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"
    r = requests.get(url)
    symbols = r.json()

    movers = []

    for s in symbols[:50]:
        symbol = s.get("symbol")

        try:
            quote = requests.get(
                f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
            ).json()

            current = quote.get("c", 0)
            previous = quote.get("pc", 0)

            if current and previous:
                change = ((current - previous) / previous) * 100
                movers.append((symbol, change))

        except:
            pass

    movers = sorted(movers, key=lambda x: x[1], reverse=True)[:10]

    for idx, (symbol, change) in enumerate(movers, start=1):
        message += f"{idx}. {symbol} +{change:.1f}%\n"

except Exception as e:
    message = f"Bot error: {e}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
