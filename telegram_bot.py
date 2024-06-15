# telegram_bot.py

import requests
import config

def send_message(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': config.TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=data)
    return response.json()

def send_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendPhoto"
    data = {
        'chat_id': config.TELEGRAM_CHAT_ID,
        'caption': caption,
        'parse_mode': 'Markdown'
    }
    with open(photo_path, 'rb') as photo:
        files = {'photo': photo}
        response = requests.post(url, data=data, files=files)
    return response.json()