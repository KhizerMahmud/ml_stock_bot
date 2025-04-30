class CandlePattern:
    def __init__(self, symbol, interval, period="1d"):
        self.symbol = symbol
        self.interval = interval
        self.period = period
        self.data = self.fetch_data()

    def fetch_data(self):
        """Fetch historical stock data using Yahoo Finance."""
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(period=self.period, interval=self.interval)
        return data
    

    def detect_bull_flag(self):
        """Detect Bull Flag pattern: strong upward move followed by consolidation."""
        data = self.data
        recent_data = data.tail(30)
        uptrend = recent_data['Close'].iloc[0] < recent_data['Close'].iloc[-1]
        consolidation = recent_data['Close'].std() < 0.01  # Price stays within a narrow range

        if uptrend and consolidation:
            return {"pattern": "Bull Flag", "status": "Detected"}
        else:
            return {"pattern": "Bull Flag", "status": "Not Detected"}

    def detect_bear_flag(self):
        """Detect Bear Flag pattern: strong downward move followed by consolidation."""
        data = self.data
        recent_data = data.tail(30)
        downtrend = recent_data['Close'].iloc[0] > recent_data['Close'].iloc[-1]
        consolidation = recent_data['Close'].std() < 0.01  # Price stays within a narrow range

        if downtrend and consolidation:
            return {"pattern": "Bear Flag", "status": "Detected"}
        else:
            return {"pattern": "Bear Flag", "status": "Not Detected"}

    def detect_double_top(self):
        """Detect Double Top pattern: two peaks at a similar price level."""
        data = self.data
        recent_data = data.tail(40)
        peaks = recent_data['Close'].rolling(window=10).max()  # Detect peaks in the last 40 bars
        top_peak = peaks.max()
        peak_distance = (recent_data['Close'] == top_peak).sum()

        if peak_distance >= 2:
            return {"pattern": "Double Top", "status": "Detected"}
        else:
            return {"pattern": "Double Top", "status": "Not Detected"}

    def detect_double_bottom(self):
        """Detect Double Bottom pattern: two troughs at a similar price level."""
        data = self.data
        recent_data = data.tail(40)
        troughs = recent_data['Close'].rolling(window=10).min()  # Detect troughs
        bottom_trough = troughs.min()
        trough_distance = (recent_data['Close'] == bottom_trough).sum()

        if trough_distance >= 2:
            return {"pattern": "Double Bottom", "status": "Detected"}
        else:
            return {"pattern": "Double Bottom", "status": "Not Detected"}

    def detect_head_and_shoulders(self):
        """Detect Head and Shoulders pattern: a higher middle peak with lower shoulders."""
        data = self.data
        recent_data = data.tail(40)
        max_price = recent_data['Close'].max()
        min_price = recent_data['Close'].min()

        # A more refined condition for head and shoulders
        if max_price / min_price > 1.2:
            return {"pattern": "Head and Shoulders", "status": "Detected"}
        else:
            return {"pattern": "Head and Shoulders", "status": "Not Detected"}

    def detect_inverse_head_and_shoulders(self):
        """Detect Inverse Head and Shoulders pattern: a lower middle trough with higher shoulders."""
        data = self.data
        recent_data = data.tail(40)
        min_price = recent_data['Close'].min()
        max_price = recent_data['Close'].max()

        # A more refined condition for inverse head and shoulders
        if max_price / min_price < 0.8:
            return {"pattern": "Inverse Head and Shoulders", "status": "Detected"}
        else:
            return {"pattern": "Inverse Head and Shoulders", "status": "Not Detected"}

    def detect_cup_and_handle(self):
        """Detect Cup and Handle pattern: a "U" shape followed by a small consolidation."""
        data = self.data
        recent_data = data.tail(40)
        min_price = recent_data['Close'].min()

        if recent_data['Close'].iloc[0] < min_price and recent_data['Close'].iloc[-1] > min_price:
            return {"pattern": "Cup and Handle", "status": "Detected"}
        else:
            return {"pattern": "Cup and Handle", "status": "Not Detected"}

    def detect_ascending_triangle(self):
        """Detect Ascending Triangle pattern: rising support with flat resistance."""
        data = self.data
        recent_data = data.tail(40)
        lows = recent_data['Close'].rolling(window=10).min()
        highs = recent_data['Close'].rolling(window=10).max()

        # Check for higher lows and constant resistance
        if lows.iloc[-1] > lows.iloc[0] and highs.iloc[-1] == highs.max():
            return {"pattern": "Ascending Triangle", "status": "Detected"}
        else:
            return {"pattern": "Ascending Triangle", "status": "Not Detected"}

    def detect_descending_triangle(self):
        """Detect Descending Triangle pattern: falling resistance with flat support."""
        data = self.data
        recent_data = data.tail(40)
        highs = recent_data['Close'].rolling(window=10).max()
        lows = recent_data['Close'].rolling(window=10).min()

        # Check for lower highs and constant support
        if highs.iloc[-1] < highs.iloc[0] and lows.iloc[-1] == lows.min():
            return {"pattern": "Descending Triangle", "status": "Detected"}
        else:
            return {"pattern": "Descending Triangle", "status": "Not Detected"}

    def detect_symmetrical_triangle(self):
        """Detect Symmetrical Triangle pattern: converging trendlines."""
        data = self.data
        recent_data = data.tail(40)
        highs = recent_data['Close'].rolling(window=10).max()
        lows = recent_data['Close'].rolling(window=10).min()

        # Check for converging highs and lows (higher lows, lower highs)
        higher_lows = lows.iloc[-1] > lows.iloc[0]  # Higher lows (ascending support)
        lower_highs = highs.iloc[-1] < highs.iloc[0]  # Lower highs (descending resistance)

        if higher_lows and lower_highs:
            return {"pattern": "Symmetrical Triangle", "status": "Detected"}
        else:
            return {"pattern": "Symmetrical Triangle", "status": "Not Detected"}

    def detect_rising_wedge(self):
        """Detect Rising Wedge pattern: narrowing upward trend."""
        data = self.data
        recent_data = data.tail(40)
        highs = recent_data['Close'].rolling(window=10).max()
        lows = recent_data['Close'].rolling(window=10).min()

        if highs.iloc[-1] > highs.iloc[0] and lows.iloc[-1] > lows.iloc[0]:
            return {"pattern": "Rising Wedge", "status": "Detected"}
        else:
            return {"pattern": "Rising Wedge", "status": "Not Detected"}

    def detect_falling_wedge(self):
        """Detect Falling Wedge pattern: narrowing downward trend."""
        data = self.data
        recent_data = data.tail(40)
        highs = recent_data['Close'].rolling(window=10).max()
        lows = recent_data['Close'].rolling(window=10).min()

        if highs.iloc[-1] < highs.iloc[0] and lows.iloc[-1] < lows.iloc[0]:
            return {"pattern": "Falling Wedge", "status": "Detected"}
        else:
            return {"pattern": "Falling Wedge", "status": "Not Detected"}

    def detect_rectangle_pattern(self):
        """Detect Rectangle Pattern: horizontal price movement between support and resistance."""
        data = self.data
        recent_data = data.tail(40)
        highs = recent_data['Close'].rolling(window=10).max()
        lows = recent_data['Close'].rolling(window=10).min()

        if highs.iloc[-1] == highs.max() and lows.iloc[-1] == lows.min():
            return {"pattern": "Rectangle Pattern", "status": "Detected"}
        else:
            return {"pattern": "Rectangle Pattern", "status": "Not Detected"}

    def detect_pennant(self):
        """Detect Pennant pattern: small consolidation after strong trend."""
        data = self.data
        recent_data = data.tail(40)
        trend = recent_data['Close'].iloc[0] < recent_data['Close'].iloc[-1]

        if trend and recent_data['Close'].std() < 0.01:
            return {"pattern": "Pennant", "status": "Detected"}
        else:
            return {"pattern": "Pennant", "status": "Not Detected"}

    def detect_rounded_bottom(self):
        """Detect Rounded Bottom pattern: gradual shift from downtrend to uptrend."""
        data = self.data
        recent_data = data.tail(40)
        min_price = recent_data['Close'].min()

        if recent_data['Close'].iloc[0] < min_price and recent_data['Close'].iloc[-1] > min_price:
            return {"pattern": "Rounded Bottom", "status": "Detected"}
        else:
            return {"pattern": "Rounded Bottom", "status": "Not Detected"}

    def detect_triple_top(self):
        """Detect Triple Top pattern: three peaks at similar price levels."""
        data = self.data
        recent_data = data.tail(60)
        peaks = recent_data['Close'].rolling(window=10).max()
        top_peak = peaks.max()
        peak_distance = (recent_data['Close'] == top_peak).sum()

        if peak_distance >= 3:
            return {"pattern": "Triple Top", "status": "Detected"}
        else:
            return {"pattern": "Triple Top", "status": "Not Detected"}

    def detect_triple_bottom(self):
        """Detect Triple Bottom pattern: three troughs at similar price levels."""
        data = self.data
        recent_data = data.tail(60)
        troughs = recent_data['Close'].rolling(window=10).min()
        bottom_trough = troughs.min()
        trough_distance = (recent_data['Close'] == bottom_trough).sum()

        if trough_distance >= 3:
            return {"pattern": "Triple Bottom", "status": "Detected"}
        else:
            return {"pattern": "Triple Bottom", "status": "Not Detected"}