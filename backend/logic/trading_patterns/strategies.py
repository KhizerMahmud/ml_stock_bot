import pandas as pd
import numpy as np


class TradingStrategies:
    def __init__(self, df):
        self.df = df

    def breakout_strategy(self):
        """
        Detect breakout from previous resistance with volume surge.
        """
        breakout_signals = []
        for i in range(1, len(self.df)):
            prev_high = self.df["High"].iloc[:i].max()
            if (
                self.df["Close"].iloc[i] > prev_high
                and self.df["Volume"].iloc[i] > self.df["Volume"].iloc[i - 1] * 1.5
            ):
                breakout_signals.append((self.df["Timestamp"].iloc[i], "Breakout"))
        return breakout_signals

    def vwap_bounce(self):
        """
        Detect bounce off VWAP line.
        """
        self.df["VWAP"] = (self.df["Close"] * self.df["Volume"]).cumsum() / self.df[
            "Volume"
        ].cumsum()
        signals = []
        for i in range(1, len(self.df)):
            if (
                abs(self.df["Close"].iloc[i] - self.df["VWAP"].iloc[i]) < 0.2
                and self.df["Close"].iloc[i] > self.df["VWAP"].iloc[i]
            ):
                signals.append((self.df["Timestamp"].iloc[i], "VWAP Bounce"))
        return signals

    def ema_crossover(self, short=9, long=20):
        """
        Detect EMA crossover strategy.
        """
        self.df["EMA_short"] = self.df["Close"].ewm(span=short, adjust=False).mean()
        self.df["EMA_long"] = self.df["Close"].ewm(span=long, adjust=False).mean()
        signals = []
        for i in range(1, len(self.df)):
            if (
                self.df["EMA_short"].iloc[i - 1] < self.df["EMA_long"].iloc[i - 1]
                and self.df["EMA_short"].iloc[i] > self.df["EMA_long"].iloc[i]
            ):
                signals.append((self.df["Timestamp"].iloc[i], "Bullish EMA Crossover"))
        return signals

    def abcd_pattern(self):
        """
        Detect simplified ABCD pattern.
        """
        signals = []
        for i in range(3, len(self.df)):
            A = self.df["Low"].iloc[i - 3]
            B = self.df["High"].iloc[i - 2]
            C = self.df["Low"].iloc[i - 1]
            D = self.df["Close"].iloc[i]
            if A < C < B and D > B:
                signals.append((self.df["Timestamp"].iloc[i], "ABCD Pattern"))
        return signals

    def unusual_volume(self, threshold=2):
        """
        Detect volume spikes over average.
        """
        avg_volume = self.df["Volume"].rolling(window=10).mean()
        signals = []
        for i in range(10, len(self.df)):
            if self.df["Volume"].iloc[i] > avg_volume.iloc[i] * threshold:
                signals.append((self.df["Timestamp"].iloc[i], "Unusual Volume"))
        return signals
