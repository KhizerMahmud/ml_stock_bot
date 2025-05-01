from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Twelve Data API key from the .env file
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze_stock():
    data = request.get_json()
    print("Received data:", data)

    # Check if data was received
    if not data:
        return jsonify({"error": "No data provided"}), 400

    symbol = data.get('symbol')
    interval = data.get('interval')

    # Check if symbol or interval is missing
    if not symbol or not interval:
        return jsonify({"error": "Missing symbol or interval"}), 400

    try:
        print(f"Debug: Symbol={symbol}, Interval={interval}")

        # Define the endpoint and parameters for Twelve Data API
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={TWELVE_DATA_API_KEY}"

        # Send the request to Twelve Data
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": "Error fetching data from Twelve Data"}), 500

        stock_data = response.json()

        if 'values' not in stock_data:
            return jsonify({"error": "No data available for the given symbol and interval"}), 404

        # Prepare OHLCV data
        candles = []
        for data_point in stock_data['values']:
            candles.append({
                'timestamp': data_point['datetime'],
                'open': data_point['open'],
                'high': data_point['high'],
                'low': data_point['low'],
                'close': data_point['close'],
                'volume': data_point['volume']
            })

        # Define patterns (use your existing logic here)
        patterns = {
            "bull_flag": "Not Detected",  # Placeholder pattern detection logic
            "bear_flag": "Not Detected",  # Placeholder pattern detection logic
            # Add your other pattern logic here if available
        }

        # Determine recommendation based on detected patterns (example logic)
        recommendation = "HOLD"  # Default recommendation
        for pattern, result in patterns.items():
            if result == "Detected":
                if 'buy' in pattern.lower():
                    recommendation = "BUY"
                elif 'sell' in pattern.lower():
                    recommendation = "SELL"

        # Current stock price
        current_price = candles[0]['close'] if candles else None

        # Return the data to frontend in JSON format
        return jsonify({
            "symbol": symbol,
            "ohlcv": candles,
            "recommendation": recommendation,
            "current_price": current_price  # Returning current price
        })

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error for debugging
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500


# Ensure Flask is running only when this file is executed directly
if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5000)
