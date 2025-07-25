# Smart Stock Advisor

Smart Stock Advisor is a web-based application that analyzes stock market data, detects technical patterns, and provides actionable recommendations (BUY, SELL, HOLD) using real-time data from the Twelve Data API. The app features a modern frontend, interactive candlestick charts, and a robust backend with pattern recognition and technical indicator calculations.

---
## 📸 Application Preview
<img width="1536" height="1024" alt="Stock Analysis Interface Snapshot" src="https://github.com/user-attachments/assets/cb7da0ca-44df-4685-9e68-507a2e1f55b3" />


## Features

- **Real-Time Stock Data**: Fetches OHLCV data using the Twelve Data API.
- **Technical Pattern Detection**: Identifies patterns such as Bull Flag, Bear Flag, Double Top/Bottom, Head and Shoulders, and more.
- **Technical Indicators**: Calculates MACD, RSI, EMA, Bollinger Bands, Fibonacci retracement, and support/resistance levels.
- **Actionable Recommendations**: Provides BUY, SELL, or HOLD suggestions based on detected patterns.
- **Interactive Candlestick Charts**: Visualizes stock price movements using Plotly.
- **Responsive UI**: Clean, modern interface with light/dark mode toggle.
- **Easy Deployment**: Simple setup using Flask for the backend and static HTML/JS for the frontend.

---

## Project Structure

```
.env
.gitattributes
README.md
requirements.txt
.vscode/
backend/
    app.py
    trading_patterns.py
    trading_patterns.txt
    trading_strategies.py
    __pycache__/
frontend/
    index.html
    stock_logo.png.png
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (optional, for advanced frontend development)
- pip

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/KhizerMahmud/ml_stock_bot.git
   cd stock_bot
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env` and add your API keys for Twelve Data, Alpha Vantage, and Finnhub.

4. **Run the backend server:**
   ```sh
   cd backend
   python app.py
   ```

5. **Open the frontend:**
   - Open `frontend/index.html` in your browser.

---

## Usage

1. Enter a stock symbol (e.g., `AAPL`) in the input field.
2. Select a time interval (e.g., `1min`, `5min`, etc.).
3. Click **Analyze** to fetch data and view the analysis.
4. View the candlestick chart and the recommendation (BUY, SELL, HOLD).

---

## Technical Overview

- **Backend:** Flask API ([backend/app.py](backend/app.py)), pattern detection ([backend/trading_patterns.py](backend/trading_patterns.py)), and technical indicators ([backend/trading_strategies.py](backend/trading_strategies.py)).
- **Frontend:** Responsive HTML/CSS/JS ([frontend/index.html](frontend/index.html)), Bootstrap, Plotly for charts.
- **Pattern Definitions:** See [backend/trading_patterns.txt](backend/trading_patterns.txt) for detailed pattern descriptions.

---

## Screenshot

Add a screenshot of the application below (replace the placeholder with your actual screenshot):

![Smart Stock Advisor Screenshot](frontend/screenshot.png)

---

## API Keys

- Store your API keys in the `.env` file:
  ```
  FINNHUB_API_KEY=your_finnhub_key
  ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
  TWELVE_DATA_API_KEY=your_twelve_data_key
  ```

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- [Twelve Data](https://twelvedata.com/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Plotly](https://plotly.com/)

---

<!-- Remove sensitive information before sharing publicly -->
