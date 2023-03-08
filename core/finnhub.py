import requests
import concurrent.futures

class Finnhub():
    
    def __init__(self, api_key):
        # Set the API key, base URL, and quote URL
        self.api_key = api_key
        self.base_url = 'https://finnhub.io/api/v1/'
        self.quote_url = self.base_url + 'quote?symbol={}&token={self.api_key}'
        self.default_symbols = ['AAPL', 'AMZN', 'NFLX', 'META', 'GOOGL']
        # Initialize the symbol quote data
        # We use this to cache the quote data for each symbol
        # so we don't have to make a request to the API for each symbol
        # every time we want to get the percentage change from the previous close
        self.symbol_quote_data = {}
    
    def get_quote(self, symbol):
        # this is a simple wrapper around the requests.get() method
        # that also updates the symbol quote data
        url = self.quote_url.format(symbol, self=self)
        response = requests.get(url)
        self.update_quote(symbol, response.json())
        return self.symbol_quote_data[symbol]
    
    def update_quote(self, symbol, data):
        # this updates the symbol quote data
        self.symbol_quote_data[symbol] = data
    
    def get_price(self, symbol):
        # this is a simple wrapper around the get_quote() method
        return self.get_quote(symbol)['c']

    def get_prices(self, symbols=None):
        [self.get_price(symbol) for symbol in (symbols or self.default_symbols)]
        return self.symbol_quote_data

    def fetch_prices(self, symbols=None):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit a thread for each symbol
            futures = [executor.submit(self.get_price, symbol) for symbol in (symbols or self.default_symbols)]
            # Wait for all threads to complete
            concurrent.futures.wait(futures)
            # Collect the results from each thread
            [f.result() for f in futures]
        return self.symbol_quote_data

    def get_percentage_change_from_previous_close(self, symbol):
        return self.symbol_quote_data[symbol]["dp"]
    
    def get_most_volatile_stock(self, symbols=None):
        # this method returns the symbol and percentage change for the most volatile stock
        symbols = symbols or self.default_symbols
        most_volatile_stock = None
        most_volatile_stock_percentage_change = 0
        # Loop through each symbol and get the percentage change from the previous close
        for symbol in symbols:
            percentage_change = self.get_percentage_change_from_previous_close(symbol)
            if percentage_change > most_volatile_stock_percentage_change:
                # If the percentage change is greater than the current most volatile stock
                # then update the most volatile stock
                most_volatile_stock, most_volatile_stock_percentage_change = symbol, percentage_change
        return {"symbol": most_volatile_stock, "percentage_change": round(most_volatile_stock_percentage_change, 2)}
