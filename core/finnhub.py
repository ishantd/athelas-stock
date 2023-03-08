import requests

class Finnhub():
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://finnhub.io/api/v1/'
        self.quote_url = self.base_url + 'quote?symbol={}&token={self.api_key}'
        self.default_symbols = ['AAPL', 'AMZN', 'NFLX', 'META', 'GOOGL']
        self.symbol_quote_data = {}
    
    def get_quote(self, symbol):
        url = self.quote_url.format(symbol, self=self)
        response = requests.get(url)
        self.update_quote(symbol, response.json())
        return self.symbol_quote_data[symbol]
    
    def update_quote(self, symbol, data):
        self.symbol_quote_data[symbol] = data
    
    def get_price(self, symbol):
        quote = self.get_quote(symbol)
        return quote['c']

    def get_prices(self, symbols=None):
        symbols = symbols or self.default_symbols
        prices = {}
        for symbol in symbols:
            prices[symbol] = self.get_price(symbol)
        return prices

    def get_percentage_change_from_previous_close(self, symbol):
        return self.symbol_quote_data[symbol]["dp"]
    
    def get_most_volatile_stock(self, symbols=None):
        symbols = symbols or self.default_symbols
        most_volatile_stock = None
        most_volatile_stock_percentage_change = 0
        for symbol in symbols:
            percentage_change = self.get_percentage_change_from_previous_close(symbol)
            if percentage_change > most_volatile_stock_percentage_change:
                most_volatile_stock = symbol
                most_volatile_stock_percentage_change = percentage_change
        return {"symbol": most_volatile_stock, "percentage_change": round(most_volatile_stock_percentage_change, 2)}
