import asyncio
import config
from bybit_client import BybitClient
from telegram_bot import send_message, send_photo
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = config.TELEGRAM_BOT_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Словарь для отслеживания состояния пользователей
user_states = {}
monitoring_task = None

# Инициализация клиента Bybit
client = BybitClient(config.BYBIT_API_KEY, config.BYBIT_API_SECRET)

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
        for user_id, is_active in user_states.items():
            if is_active:
                tickers = client.get_tickers()
                for ticker in tickers:
                    symbol = ticker['symbol']
                    price_change = client.get_price_change(symbol)
                    if abs(price_change) > config.PRICE_CHANGE_THRESHOLD:
                        message = f"🚨Crypto Alert!🚨\n\n**Symbol: {symbol}**\nPrice Change: {price_change:.2f}%"
                        await bot.send_message(user_id, message)
                        prices = [float(ticker['last_price'])]  # Здесь можно добавить больше данных для графика
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
