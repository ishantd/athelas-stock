from flask import render_template, request, Response
from core import app
from core.finnhub import Finnhub

finnhub = Finnhub(app.config['FINNHUB_API_KEY'])

@app.route('/', methods=['GET', 'POST'])
def index():
    prices = finnhub.fetch_prices()
    most_volatile_stock = finnhub.get_most_volatile_stock()
    # if method is GET, render the index.html template
    if request.method == 'GET':
        return render_template('index.html', prices=prices, most_volatile_stock=most_volatile_stock)
    # if method is POST, return the csv data
    if request.method == 'POST':
        return Response(finnhub.get_csv_for_most_volatile_stock(), mimetype='text/csv')
    return render_template('index.html', prices=prices, most_volatile_stock=most_volatile_stock)