from flask import Flask, render_template, request, jsonify
from backend.logic.decision_making import StockBotApp
from backend.logic.database import StockDatabase

app = Flask(__name__)
db = StockDatabase()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_stock():
    symbol = request.form.get("symbol").upper()
    if not symbol:
        return jsonify({"error": "Please enter a stock symbol."}), 400

    try:
        stock_bot = StockBotApp(None)
        analysis = stock_bot.analyze_stock(symbol)
        return jsonify({"analysis": analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/portfolio", methods=["GET"])
def portfolio():
    try:
        trades = db.fetch_trade_history()
        return jsonify({"portfolio": trades})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)