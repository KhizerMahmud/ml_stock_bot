import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
from newsapi import NewsApiClient

# --- Load Environment Variables ---
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY", NEWS_API_KEY)


class StockBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Stock Advisor")
        self.root.geometry("800x600")

        self.news_api = NewsApiClient(api_key=NEWS_API_KEY)

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self.root, text="Stock Advisor Bot", font=("Helvetica", 20))
        title.pack(pady=10)

        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        self.stock_entry = ttk.Entry(search_frame, width=40)
        self.stock_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(
            search_frame, text="Analyze", command=self.analyze_stock
        )
        search_button.pack(side=tk.LEFT)

        self.recommendation_label = ttk.Label(
            self.root, text="", font=("Helvetica", 16)
        )
        self.recommendation_label.pack(pady=10)

        self.analysis_text = tk.Text(self.root, wrap="word", height=25, width=90)
        self.analysis_text.pack(padx=10, pady=10)

    def analyze_stock(self):
        symbol = self.stock_entry.get().upper()
        if not symbol:
            messagebox.showerror("Input Error", "Please enter a stock symbol.")
            return

        try:
            stock_data = yf.download(symbol, period="1mo", interval="1d")
            if stock_data.empty:
                raise ValueError("No data found")

            # Technical indicators
            stock_data["RSI"] = ta.rsi(stock_data["Close"], length=14)
            macd = ta.macd(stock_data["Close"])
            stock_data = pd.concat([stock_data, macd], axis=1)

            latest = stock_data.iloc[-1]
            rsi = latest["RSI_14"]
            macd_hist = latest["MACDh_12_26_9"]

            # News headlines
            headlines = self.get_news(symbol)
            sentiment_score = self.calculate_sentiment(headlines)

            # Decision logic
            recommendation = self.make_recommendation(rsi, macd_hist, sentiment_score)

            # Display
            self.recommendation_label.config(text=f"Recommendation: {recommendation}")
            breakdown = f"Analyzing {symbol}\n\n"
            breakdown += f"Current Price: ${latest['Close']:.2f}\n"
            breakdown += f"RSI (14): {rsi:.2f}\n"
            breakdown += f"MACD Histogram: {macd_hist:.2f}\n"
            breakdown += f"Sentiment Score: {sentiment_score:.2f}\n"
            breakdown += f"\nNews Headlines:\n"
            for h in headlines:
                breakdown += f"- {h}\n"

            breakdown += f"\nConclusion: {recommendation} based on technical, sentiment, and risk analysis."
            self.analysis_text.delete("1.0", tk.END)
            self.analysis_text.insert(tk.END, breakdown)

        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error analyzing stock: {e}")

    def calculate_sentiment(self, headlines):
        """
        Calculate the average sentiment score of the news headlines.
        """
        if not headlines:
            return 0  # Neutral sentiment if no headlines are available

        sentiment_scores = []
        for headline in headlines:
            analysis = TextBlob(headline)
            sentiment_scores.append(analysis.sentiment.polarity)

        return sum(sentiment_scores) / len(sentiment_scores)

    def make_recommendation(self, rsi, macd_hist, sentiment_score):
        """
        Make a recommendation based on RSI, MACD, sentiment, and risk management.
        """
        # Risk management thresholds
        risk_tolerance = 0.5  # Example: 0.5 for moderate risk tolerance
        sentiment_threshold = 0.1  # Positive sentiment threshold

        if rsi < 30 and macd_hist > 0 and sentiment_score > sentiment_threshold:
            return "BUY (Low RSI, Positive Sentiment)"
        elif rsi > 70 and macd_hist < 0 and sentiment_score < -sentiment_threshold:
            return "SELL (High RSI, Negative Sentiment)"
        elif abs(sentiment_score) < risk_tolerance:
            return "HOLD (Neutral Sentiment)"
        else:
            return "HOLD (Risk Management Applied)"

    def get_news(self, symbol):
        try:
            response = self.news_api.get_everything(
                q=symbol, language="en", sort_by="relevancy", page_size=5
            )
            return [article["title"] for article in response["articles"]]
        except Exception:
            return ["News unavailable or API limit reached."]


if __name__ == "__main__":
    root = tk.Tk()
    app = StockBotApp(root)
    root.mainloop()
