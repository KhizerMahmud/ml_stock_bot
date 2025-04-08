import sqlite3
import datetime

class StockDatabase:
    def __init__(self, db_name="stock_bot.db"):
        """
        Initialize the database connection and create tables if they don't exist.
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Create tables for storing stock analysis, trades, and predictions.
        """
        # Table for storing stock analysis data
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                rsi REAL,
                macd_hist REAL,
                recommendation TEXT,
                news_headlines TEXT,
                current_price REAL
            )
        """)

        # Table for storing trade history
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_symbol TEXT NOT NULL,
                trade_date TEXT NOT NULL,
                action TEXT NOT NULL,  -- BUY, SELL, HOLD
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                profit_loss REAL
            )
        """)

        # Table for storing machine learning data
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ml_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                features TEXT NOT NULL,  -- JSON string of features
                outcome TEXT NOT NULL    -- BUY, SELL, HOLD
            )
        """)

        self.conn.commit()

    def insert_stock_analysis(self, stock_symbol, date, rsi, macd_hist, recommendation, news_headlines, current_price):
        """
        Insert stock analysis data into the database.
        """
        self.cursor.execute("""
            INSERT INTO stock_analysis (stock_symbol, date, rsi, macd_hist, recommendation, news_headlines, current_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (stock_symbol, date, rsi, macd_hist, recommendation, news_headlines, current_price))
        self.conn.commit()

    def insert_trade_history(self, stock_symbol, trade_date, action, price, quantity, profit_loss):
        """
        Insert trade history data into the database.
        """
        self.cursor.execute("""
            INSERT INTO trade_history (stock_symbol, trade_date, action, price, quantity, profit_loss)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (stock_symbol, trade_date, action, price, quantity, profit_loss))
        self.conn.commit()

    def insert_ml_data(self, stock_symbol, date, features, outcome):
        """
        Insert machine learning data into the database.
        """
        self.cursor.execute("""
            INSERT INTO ml_data (stock_symbol, date, features, outcome)
            VALUES (?, ?, ?, ?)
        """, (stock_symbol, date, features, outcome))
        self.conn.commit()

    def fetch_trade_history(self):
        """
        Fetch all trade history data.
        """
        self.cursor.execute("SELECT * FROM trade_history")
        return self.cursor.fetchall()

    def fetch_stock_analysis(self, stock_symbol):
        """
        Fetch stock analysis data for a specific stock symbol.
        """
        self.cursor.execute("SELECT * FROM stock_analysis WHERE stock_symbol = ?", (stock_symbol,))
        return self.cursor.fetchall()

    def fetch_ml_data(self):
        """
        Fetch all machine learning data.
        """
        self.cursor.execute("SELECT * FROM ml_data")
        return self.cursor.fetchall()

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()