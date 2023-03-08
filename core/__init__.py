from flask import Flask
import os

app = Flask(__name__)
app.config["FINNHUB_API_KEY"] = os.environ.get("FINNHUB_API_KEY")

from core import views