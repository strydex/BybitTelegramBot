import time
import config
from bybit_client import BybitClient
from telegram_bot import send_message, send_photo
import matplotlib.pyplot as plt

def main():
    client = BybitClient(config.BYBIT_API_KEY, config.BYBIT_API_SECRET)
    while True:
        tickers = client.get_tickers()
        for ticker in tickers:
            symbol = ticker['symbol']
            price_change = client.get_price_change(symbol)
            if abs(price_change) > config.PRICE_CHANGE_THRESHOLD:
                message = f"🚨Crypto Alert!🚨\n\n**Symbol: {symbol}**\nPrice Change: {price_change:.2f}%"
                send_message(message)
                prices = [float(ticker['last_price'])]  # Здесь можно добавить больше данных для графика
        time.sleep(config.CHECK_INTERVAL)

if __name__ == "__main__":
    main()