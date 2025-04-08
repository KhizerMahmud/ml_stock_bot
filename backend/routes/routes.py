from flask import Flask, render_template, request, jsonify
from backend.logic.decision_making import StockBotApp
from backend.logic.database import StockDatabase

app = Flask(__name__)
db = StockDatabase()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
@app.route("/analyze", methods=["POST"])
def analyze_stock():
    try:
        symbol = request.json.get("symbol", "").upper()
        if not symbol:
            logging.warning("No stock symbol provided.")
            return jsonify({"error": "Please enter a stock symbol."}), 400

        logging.info(f"Analyzing stock: {symbol}")
        stock_bot = StockBotApp(None)
        analysis = stock_bot.analyze_stock(symbol)
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
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
