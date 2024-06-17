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
        random.shuffle(tickers)  # Shuffle the list of tickers
        return tickers

    def get_price_change(self, symbol):
        endpoint = '/v2/public/tickers'
        url = self.base_url + endpoint
        params = {'symbol': symbol}
        response = requests.get(url, params=params)
        data = response.json()['result'][0]
        price_change = (float(data['last_price']) - float(data['prev_price_24h'])) / float(data['prev_price_24h']) * 100
        return price_change
