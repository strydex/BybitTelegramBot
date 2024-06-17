import asyncio
import config
from bybit_client import BybitClient
from telegram_bot import send_message, send_photo
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
import time
from datetime import datetime, timedelta
import pytz

TOKEN = config.TELEGRAM_BOT_TOKEN
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=MemoryStorage())

# Инициализация клиента Bybit
client = BybitClient(config.BYBIT_API_KEY, config.BYBIT_API_SECRET)

# Интервал между сообщениями в секундах (5 минут = 300 секунд)
MESSAGE_INTERVAL = 300
# Лимит сообщений в день
DAILY_MESSAGE_LIMIT = 30

# Устанавливаем временную зону
timezone = pytz.timezone('Europe/Moscow')

async def monitor_market(last_message_time, message_count, message_count_reset_time):
    while True:
        current_time = datetime.now(timezone)
        if current_time - last_message_time >= timedelta(seconds=MESSAGE_INTERVAL):
            if message_count < DAILY_MESSAGE_LIMIT:
                try:
                    tickers = client.get_tickers()
                    for ticker in tickers:
                        symbol = ticker['symbol']
                        price_change = client.get_price_change(symbol)
                        if abs(price_change) > config.PRICE_CHANGE_THRESHOLD:
                            message = f"🚨<b>Crypto Alert!</b>🚨\n\n<b>Тикер:</b> {symbol}\n<b>Изменение цены:</b> {price_change:.2f}%"
                            await bot.send_message(chat_id=config.TELEGRAM_CHANNEL_ID, text=message, parse_mode='HTML')
                            last_message_time = current_time
                            message_count += 1
                            break  # Send only one message per interval
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                if current_time >= message_count_reset_time:
                    message_count = 0
                    message_count_reset_time = current_time + timedelta(days=1)
        await asyncio.sleep(config.CHECK_INTERVAL)

async def main():
    # Запускаем поллинг
    polling_task = asyncio.create_task(dp.start_polling(bot))
    # Запускаем мониторинг рынка
    monitoring_task = asyncio.create_task(monitor_market(datetime.now(timezone), 0, datetime.now(timezone) + timedelta(days=1)))
    # Ждем завершения обеих задач
    await asyncio.gather(polling_task, monitoring_task)

if __name__ == '__main__':
    asyncio.run(main())
