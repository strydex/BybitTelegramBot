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

TOKEN = config.TELEGRAM_BOT_TOKEN
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=MemoryStorage())

# Словарь для отслеживания состояния пользователей, времени последней отправки сообщения и количества сообщений
user_states = {}
last_message_time = {}
message_count = {}
monitoring_task = None

# Инициализация клиента Bybit
client = BybitClient(config.BYBIT_API_KEY, config.BYBIT_API_SECRET)

# Интервал между сообщениями в секундах (5 минут = 300 секунд)
MESSAGE_INTERVAL = 2
# Лимит сообщений в день
DAILY_MESSAGE_LIMIT = 3

async def start_monitoring():
    global monitoring_task
    if monitoring_task is None or monitoring_task.done():
        monitoring_task = asyncio.create_task(monitor_market())

async def stop_monitoring():
    global monitoring_task
    if monitoring_task and not monitoring_task.done():
        monitoring_task.cancel()
        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = True  # Отмечаем, что бот активен для этого пользователя
    message_count[user_id] = {'count': 0, 'reset_time': datetime.now() + timedelta(days=1), 'limit_reached': False}
    await message.reply("Бот начал работу!")
    await start_monitoring()

@dp.message(Command("stop"))
async def stop(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = False  # Отмечаем, что бот неактивен для этого пользователя
    await message.reply("Бот остановлен!")
    await stop_monitoring()

async def monitor_market():
    while True:
        current_time = time.time()
        for user_id, is_active in user_states.items():
            if is_active:
                if user_id not in last_message_time or current_time - last_message_time[user_id] >= MESSAGE_INTERVAL:
                    if message_count[user_id]['count'] < DAILY_MESSAGE_LIMIT:
                        tickers = client.get_tickers()
                        for ticker in tickers:
                            symbol = ticker['symbol']
                            price_change = client.get_price_change(symbol)
                            if abs(price_change) > config.PRICE_CHANGE_THRESHOLD:
                                message = f"🚨<b>Crypto Alert!</b>🚨\n\n<b>Symbol:</b> {symbol}\n<b>Price Change:</b> {price_change:.2f}%"
                                await bot.send_message(user_id, message)
                                last_message_time[user_id] = current_time
                                message_count[user_id]['count'] += 1
                                message_count[user_id]['limit_reached'] = False
                                break  # Отправляем только одно сообщение за интервал времени
                    else:
                        reset_time = message_count[user_id]['reset_time']
                        if datetime.now() >= reset_time:
                            message_count[user_id] = {'count': 0, 'reset_time': datetime.now() + timedelta(days=1), 'limit_reached': False}
                        elif not message_count[user_id]['limit_reached']:
                            await bot.send_message(user_id, "Это последние новости на сегодня, в данный момент лимит получения новостей достигнут.")
                            message_count[user_id]['limit_reached'] = True
        await asyncio.sleep(config.CHECK_INTERVAL)

@dp.message(F.text)
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, False):
        await message.reply("Бот активен и получил ваше сообщение!")
    else:
        await message.reply("Бот неактивен. Используйте /start для активации.")

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/stop", description="Остановить бота"),
    ]
    await bot.set_my_commands(commands)

async def main():
    await set_commands(bot)
    # Запускаем поллинг
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
