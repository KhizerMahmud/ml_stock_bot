import unittest
import os
import sqlite3
from backend.database import StockDatabase


class TestStockDatabase(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary database for testing.
        """
        self.test_db_name = "test_stock_bot.db"
        self.db = StockDatabase(db_name=self.test_db_name)

    def tearDown(self):
        """
        Clean up the test database after each test.
        """
        self.db.close()
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)

    def test_create_tables(self):
        """
        Test if tables are created successfully.
        """
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in self.db.cursor.fetchall()]
        self.assertIn("stock_analysis", tables)
        self.assertIn("trade_history", tables)
        self.assertIn("ml_data", tables)

    def test_insert_stock_analysis(self):
        """
        Test inserting stock analysis data.
        """
        self.db.insert_stock_analysis(
            stock_symbol="AAPL",
            date="2025-04-07",
            rsi=45.2,
            macd_hist=0.12,
            recommendation="BUY",
            news_headlines="Apple launches new product.",
            current_price=150.25,
        )
        self.db.cursor.execute(
            "SELECT * FROM stock_analysis WHERE stock_symbol = 'AAPL'"
        )
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "AAPL")  # stock_symbol
        self.assertEqual(result[4], 0.12)  # macd_hist

    def test_insert_trade_history(self):
        """
        Test inserting trade history data.
        """
        self.db.insert_trade_history(
            stock_symbol="AAPL",
            trade_date="2025-04-07",
            action="BUY",
            price=150.25,
            quantity=10,
            profit_loss=None,
        )
        self.db.cursor.execute(
            "SELECT * FROM trade_history WHERE stock_symbol = 'AAPL'"
        )
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[3], "BUY")  # action
        self.assertEqual(result[4], 150.25)  # price

    def test_insert_ml_data(self):
        """
        Test inserting machine learning data.
        """
        self.db.insert_ml_data(
            stock_symbol="AAPL",
            date="2025-04-07",
            features='{"rsi": 45.2, "macd_hist": 0.12, "news_sentiment": 0.8}',
            outcome="BUY",
        )
        self.db.cursor.execute("SELECT * FROM ml_data WHERE stock_symbol = 'AAPL'")
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(
            result[3], '{"rsi": 45.2, "macd_hist": 0.12, "news_sentiment": 0.8}'
        )  # features
        self.assertEqual(result[4], "BUY")  # outcome

    def test_fetch_trade_history(self):
        """
        Test fetching trade history data.
        """
        self.db.insert_trade_history(
            stock_symbol="AAPL",
            trade_date="2025-04-07",
            action="BUY",
            price=150.25,
            quantity=10,
            profit_loss=None,
        )
        trades = self.db.fetch_trade_history()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0][1], "AAPL")  # stock_symbol

    def test_fetch_stock_analysis(self):
        """
        Test fetching stock analysis data.
        """
        self.db.insert_stock_analysis(
            stock_symbol="AAPL",
            date="2025-04-07",
            rsi=45.2,
            macd_hist=0.12,
            recommendation="BUY",
            news_headlines="Apple launches new product.",
            current_price=150.25,
        )
        analysis = self.db.fetch_stock_analysis("AAPL")
        self.assertEqual(len(analysis), 1)
        self.assertEqual(analysis[0][1], "AAPL")  # stock_symbol

    def test_fetch_ml_data(self):
        """
        Test fetching machine learning data.
        """
        self.db.insert_ml_data(
            stock_symbol="AAPL",
            date="2025-04-07",
            features='{"rsi": 45.2, "macd_hist": 0.12, "news_sentiment": 0.8}',
            outcome="BUY",
        )
        ml_data = self.db.fetch_ml_data()
        self.assertEqual(len(ml_data), 1)
        self.assertEqual(ml_data[0][1], "AAPL")  # stock_symbol


if __name__ == "__main__":
    unittest.main()
