import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas_ta as ta
from textblob import TextBlob
from newsapi import NewsApiClient
from strategies import TradingStrategies
from trading_patterns import (
    bull_flag,
    bear_flag,
    double_top,
    double_bottom,
    head_and_shoulders,
    inverse_head_and_shoulders,
    cup_and_handle,
    ascending_triangle,
    descending_triangle,
    symmetrical_triangle,
    rising_wedge,
    falling_wedge,
    rectangle_pattern,
    pennant,
    rounded_bottom,
    triple_top,
    triple_bottom,
)

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
            # Download stock data
            stock_data = yf.download(symbol, period="1mo", interval="1d")
            if stock_data.empty:
                raise ValueError("No data found")

            # Add technical indicators
            stock_data["RSI"] = ta.rsi(stock_data["Close"], length=14)
            macd = ta.macd(stock_data["Close"])
            stock_data = pd.concat([stock_data, macd], axis=1)

            # Create an instance of TradingStrategies class
            strategy = TradingStrategies(stock_data)

            # Get strategy signals
            breakout_signals = strategy.breakout_strategy()
            vwap_signals = strategy.vwap_bounce()
            ema_signals = strategy.ema_crossover()

            # Pattern recognition
            bull_flag_signal = bull_flag(stock_data)
            bear_flag_signal = bear_flag(stock_data)
            double_top_signal = double_top(stock_data)
            double_bottom_signal = double_bottom(stock_data)
            head_and_shoulders_signal = head_and_shoulders(stock_data)
            inverse_head_and_shoulders_signal = inverse_head_and_shoulders(stock_data)
            cup_and_handle_signal = cup_and_handle(stock_data)
            ascending_triangle_signal = ascending_triangle(stock_data)
            descending_triangle_signal = descending_triangle(stock_data)

            latest = stock_data.iloc[-1]
            rsi = latest["RSI_14"]
            macd_hist = latest["MACDh_12_26_9"]

            # News headlines
            headlines = self.get_news(symbol)
            sentiment_score = self.calculate_sentiment(headlines)

            # Combine all signals into a final recommendation
            recommendation = self.make_recommendation(
                rsi,
                macd_hist,
                sentiment_score,
                breakout_signals,
                vwap_signals,
                ema_signals,
                bull_flag_signal,
                bear_flag_signal,
                double_top_signal,
                double_bottom_signal,
                head_and_shoulders_signal,
                inverse_head_and_shoulders_signal,
                cup_and_handle_signal,
                ascending_triangle_signal,
                descending_triangle_signal,
            )

            # Display the results
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

    def make_recommendation(
        self,
        rsi,
        macd_hist,
        sentiment_score,
        breakout_signals,
        vwap_signals,
        ema_signals,
        bull_flag_signal,
        bear_flag_signal,
        double_top_signal,
        double_bottom_signal,
        head_and_shoulders_signal,
        inverse_head_and_shoulders_signal,
        cup_and_handle_signal,
        ascending_triangle_signal,
        descending_triangle_signal,
    ):
        """
        Make a recommendation based on technical indicators, chart patterns, and sentiment.
        """
        # Risk management thresholds
        risk_tolerance = 0.5  # Example: 0.5 for moderate risk tolerance
        sentiment_threshold = 0.1  # Positive sentiment threshold

        # Combine all signals (from strategies and patterns)
        signals = []
        if breakout_signals:
            signals.append("Breakout")
        if vwap_signals:
            signals.append("VWAP Bounce")
        if ema_signals:
            signals.append("EMA Crossover")
        if bull_flag_signal:
            signals.append("Bull Flag")
        if bear_flag_signal:
            signals.append("Bear Flag")
        if double_top_signal:
            signals.append("Double Top")
        if double_bottom_signal:
            signals.append("Double Bottom")
        if head_and_shoulders_signal:
            signals.append("Head and Shoulders")
        if inverse_head_and_shoulders_signal:
            signals.append("Inverse Head and Shoulders")
        if cup_and_handle_signal:
            signals.append("Cup and Handle")
        if ascending_triangle_signal:
            signals.append("Ascending Triangle")
        if descending_triangle_signal:
            signals.append("Descending Triangle")

        # Decision logic
        if (
            rsi < 30
            and macd_hist > 0
            and sentiment_score > sentiment_threshold
            and "Breakout" in signals
        ):
            return "BUY (Low RSI, Positive Sentiment, Breakout)"
        elif (
            rsi > 70
            and macd_hist < 0
            and sentiment_score < -sentiment_threshold
            and "Head and Shoulders" in signals
        ):
            return "SELL (High RSI, Negative Sentiment, Head and Shoulders)"
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
