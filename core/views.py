from flask import render_template
from core import app
from core.finnhub import Finnhub

finnhub = Finnhub(app.config['FINNHUB_API_KEY'])

@app.route('/')
def index():
    prices = finnhub.get_prices(['AAPL', 'AMZN', 'NFLX', 'META', 'GOOGL'])
    return render_template('index.html', prices=prices)