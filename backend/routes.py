# routes.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from backend.decision_making import StockBotApp
from backend.logic.database import StockDatabase
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for local frontend on a different port)
db = StockDatabase()

# --- Load Environment Variables ---
load_dotenv()  # Load environment variables from .env file
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# --- Logging Config ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/suggest", methods=["GET"])
def suggest_stocks():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"suggestions": []})

    url = "https://finnhub.io/api/v1/search"
    params = {"q": query, "token": FINNHUB_API_KEY}

    try:
        response = requests.get(url, params=params)
        data = response.json()
        suggestions = [
            {"symbol": item["symbol"], "description": item["description"]}
            for item in data.get("result", [])
            if item.get("symbol") and item.get("description")
        ]

        return jsonify({"suggestions": suggestions})

    except Exception as e:
        return jsonify({"error": str(e), "suggestions": []}), 500


@app.route("/analyze", methods=["POST"])
def analyze_stock():
    try:
        symbol = request.json.get("symbol", "").upper()
        if not symbol:
            logging.warning("No stock symbol provided.")
            return jsonify({"error": "Please enter a stock symbol."}), 400

        logging.info(f"Analyzing stock: {symbol}")
        stock_bot = StockBotApp()
        analysis = stock_bot.analyze_stock(symbol)
        if "error" in analysis:
            logging.error(f"Error analyzing stock: {analysis['error']}")
            return jsonify({"error": analysis["error"]}), 400

        logging.info(f"Analysis result for {symbol}: {analysis}")
        return jsonify({"analysis": analysis})

    except Exception as e:
        logging.error(f"Error analyzing stock: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/portfolio", methods=["GET"])
def portfolio():
    try:
        trades = db.fetch_trade_history()
        return jsonify({"portfolio": trades})
    except Exception as e:
        logging.error(f"Error fetching portfolio: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
