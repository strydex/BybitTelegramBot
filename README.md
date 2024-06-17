# Bybit Alerts Telegram Bot

This is a Telegram bot that monitors the price changes of cryptocurrencies on Bybit and sends notifications to a Telegram channel.

## Installation on VPS

1. Clone the repository from GitHub:

```
git clone https://github.com/strydex/BybitTelegramBot/
```

2. Create a virtual environment with `venv` and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages from `requirements.txt` into activated environment:

```
pip3 install -r requirements.txt
```

4. Get a Telegram bot token from [@BotFather](https://telegram.me/BotFather) in Telegram.
   
5. Add your newly-created bot to channel members and make it an Administrator of the your TG channel. Give it permission to send messages into the channel.

6. Get the Telegram channel ID. Follow the instructions [here](https://support.autochartist.com/en/knowledgebase/article/how-to-find-the-channel-id-of-your-telegram-channel) to find the channel ID.

7. Change the bot token, API keys, Telegram channel ID, check interval, and price change threshold in `config.py`.

8. Run the bot with the following command:

```
python3 price_monitor.py
```

9. To run the bot in the background and automatically restart it if it crashes, you can use a process manager like [PM2](https://pm2.io/blog/2018/09/19/Manage-Python-Processes) or Supervisor.

## Usage

The bot will monitor the price changes of cryptocurrencies on Bybit and send notifications to the specified Telegram channel. The bot will send only one notification per interval and will not exceed the daily message limit.

## Configuration

The following configuration options can be changed in `config.py`:

- `BYBIT_API_KEY`: Your Bybit API key.
- `BYBIT_API_SECRET`: Your Bybit API secret.
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `TELEGRAM_CHANNEL_ID`: Your Telegram channel ID.
- `CHECK_INTERVAL`: The interval between price checks in seconds.
- `PRICE_CHANGE_THRESHOLD`: The price change threshold in percentage.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the GPL-3.0 License. See the `LICENSE` file for details.

## Updates

Probably in the future I will add an update with a chart of the cryptocurrency pair directly in the notification with a ticker and price change. If you wish to help with this, add the code and create a pull request to the repository. Also feel free to fork it if you need to use it for your own project.
