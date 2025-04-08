import requests
from newsapi import NewsApiClient
import logging


# --- Load Environment Variables ---
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY", NEWS_API_KEY)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("news_analyzer.log"),
        logging.StreamHandler()
    ]
)

# --- News Analyzer Class ---
class NewsAnalyzer:
    def __init__(self):
        if not NEWS_API_KEY:
            logging.error("NEWS_API_KEY is not set.")
            raise ValueError("Missing News API key.")
        self.news_api = NewsApiClient(api_key=NEWS_API_KEY)

        def get_stock_news(self, stock_symbol):
        """
        Fetches recent news articles related to the given stock symbol.
        """
        if not stock_symbol or not isinstance(stock_symbol, str):
            logging.warning("Invalid stock symbol provided.")
            return ["Invalid stock symbol provided."]
        
        try:
            logging.info(f"Fetching news for stock symbol: {stock_symbol}")
            response = self.news_api.get_everything(
                q=stock_symbol,
                language="en",
                sort_by="relevancy",
                page_size=10,
            )
            articles = response.get("articles", [])
            if not articles:
                logging.info(f"No articles found for: {stock_symbol}")
                return [f"No news articles found for stock: {stock_symbol}"]
            return [article["title"] for article in articles]
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error while fetching stock news: {e}")
            return ["Network error. Please try again later."]
        except KeyError as e:
            logging.error(f"Unexpected response format: {e}")
            return ["Unexpected response format from the API."]
        except Exception as e:
            logging.error(f"Error fetching stock news: {e}")
            return [f"Error fetching stock news: {e}"]

    def get_global_news(self):
        """
        Fetches global news related to major economic events.
        """
        global_keywords = [
            "tariffs", "chip shortages", "global recession",
            "oil prices", "interest rates", "inflation",
            "supply chain disruptions"
        ]
        query = " OR ".join(global_keywords)
        
        try:
            logging.info("Fetching global economic news.")
            response = self.news_api.get_everything(
                q=query,
                language="en",
                sort_by="relevancy",
                page_size=10,
            )
            articles = response.get("articles", [])
            return [article["title"] for article in articles]
        except Exception as e:
            logging.error(f"Error fetching global news: {e}")
            return [f"Error fetching global news: {e}"]

    def get_international_stock_news(self, country):
        """
        Fetches stock market news for a specific country.
        """
        try:
            logging.info(f"Fetching international news for: {country}")
            response = self.news_api.get_everything(
                q=f"{country} stock market",
                language="en",
                sort_by="relevancy",
                page_size=10,
            )
            articles = response.get("articles", [])
            return [article["title"] for article in articles]
        except Exception as e:
            logging.error(f"Error fetching international stock news: {e}")
            return [f"Error fetching international stock news: {e}"]
