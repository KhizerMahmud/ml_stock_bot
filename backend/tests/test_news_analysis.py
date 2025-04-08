import unittest
from unittest.mock import patch, MagicMock
from backend.news.new_analysis import NewsAnalyzer

class TestNewsAnalyzer(unittest.TestCase):
    def setUp(self):
        self.news_analyzer = NewsAnalyzer()

    @patch("backend.news.new_analysis.NewsApiClient.get_everything")
    def test_get_stock_news(self, mock_get_everything):
        # Mock response
        mock_get_everything.return_value = {
            "articles": [{"title": "Stock AAPL surges 5%"}]
        }

        # Test
        stock_news = self.news_analyzer.get_stock_news("AAPL")
        self.assertIn("Stock AAPL surges 5%", stock_news)

    @patch("backend.news.new_analysis.NewsApiClient.get_everything")
    def test_get_global_news(self, mock_get_everything):
        # Mock response
        mock_get_everything.return_value = {
            "articles": [{"title": "Global recession fears rise"}]
        }

        # Test
        global_news = self.news_analyzer.get_global_news()
        self.assertIn("Global recession fears rise", global_news)

    @patch("backend.news.new_analysis.NewsApiClient.get_everything")
    def test_get_international_stock_news(self, mock_get_everything):
        # Mock response
        mock_get_everything.return_value = {
            "articles": [{"title": "China stock market rebounds"}]
        }

        # Test
        international_news = self.news_analyzer.get_international_stock_news("China")
        self.assertIn("China stock market rebounds", international_news)

    @patch("backend.news.new_analysis.NewsApiClient.get_everything")
    def test_error_handling(self, mock_get_everything):
        # Mock an exception
        mock_get_everything.side_effect = Exception("API Error")

        # Test stock news
        stock_news = self.news_analyzer.get_stock_news("AAPL")
        self.assertIn("Error fetching stock news: API Error", stock_news)

        # Test global news
        global_news = self.news_analyzer.get_global_news()
        self.assertIn("Error fetching global news: API Error", global_news)

        # Test international news
        international_news = self.news_analyzer.get_international_stock_news("China")
        self.assertIn("Error fetching international stock news: API Error", international_news)

    @patch("backend.news.new_analysis.NewsApiClient.get_everything")
    def test_empty_stock_news(self, mock_get_everything):
        # Mock empty response
        mock_get_everything.return_value = {"articles": []}

        # Test
        stock_news = self.news_analyzer.get_stock_news("AAPL")
        self.assertIn("No news articles found for stock: AAPL", stock_news)

    def test_invalid_stock_symbol(self):
    # Test with invalid stock symbol
    stock_news = self.news_analyzer.get_stock_news("")
    self.assertIn("Invalid stock symbol provided.", stock_news)

    @patch("backend.news.new_analysis.logging.error")
    @patch("backend.news.new_analysis.NewsApiClient.get_everything")
    def test_logging_on_error(self, mock_get_everything, mock_logging):
        # Mock an exception
        mock_get_everything.side_effect = Exception("API Error")

        # Test
        stock_news = self.news_analyzer.get_stock_news("AAPL")
        self.assertIn("Error fetching stock news: API Error", stock_news)

        # Verify logging
        mock_logging.assert_called_with("Error fetching stock news for AAPL: API Error")

if __name__ == "__main__":
    unittest.main()