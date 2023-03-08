import requests

class Finnhub():
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://finnhub.io/api/v1/'
        self.quote_url = self.base_url + 'quote?symbol={}&token={self.api_key}'
    
    def get_quote(self, symbol):
        url = self.quote_url.format(symbol, self=self)
        response = requests.get(url)
        return response.json()
    
    def get_price(self, symbol):
        quote = self.get_quote(symbol)
        return quote['c']

    def get_prices(self, symbols):
        prices = {}
        for symbol in symbols:
            prices[symbol] = self.get_price(symbol)
        return prices
