from flask import render_template
from core import app
from core.finnhub import Finnhub

finnhub = Finnhub(app.config['FINNHUB_API_KEY'])

@app.route('/')
def index():
    prices = finnhub.fetch_prices()
    most_volatile_stock = finnhub.get_most_volatile_stock()
    return render_template('index.html', prices=prices, most_volatile_stock=most_volatile_stock)