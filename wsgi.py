from core import app
import os

if __name__ == '__main__':
    app.config["FINNHUB_API_KEY"] = os.environ.get("FINNHUB_API_KEY")
    app.run(debug=False, port=5000)