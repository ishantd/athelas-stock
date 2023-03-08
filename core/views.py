from flask import render_template
from core import app

@app.route('/')
def index():
    prices = {
        "APPLE": 1.2,
        "AMAZON": 3.45,
        "NETFLIX": 2.34,
        "FACEBOOK": 1.23,
        "GOOGLE": 1.54
    }
    return render_template('index.html', prices=prices)