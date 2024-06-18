import requests
import random

class BybitClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api.bybit.com'

    def get_tickers(self):
        endpoint = '/v2/public/tickers'
        url = self.base_url + endpoint
        response = requests.get(url)
        tickers = response.json()['result']
        positive_tickers = [ticker for ticker in tickers if self.get_price_change(ticker['symbol']) > 0]  # Filter out tickers with negative price changes
        random.shuffle(positive_tickers)  # Shuffle the list of positive tickers
        return positive_tickers

    def get_price_change(self, symbol):
        endpoint = '/v2/public/tickers'
        url = self.base_url + endpoint
        params = {'symbol': symbol}
        response = requests.get(url, params=params)
        data = response.json()['result'][0]
        price_change = (float(data['last_price']) - float(data['prev_price_24h'])) / float(data['prev_price_24h']) * 100
        return price_change
