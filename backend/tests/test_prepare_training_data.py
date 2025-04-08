import unittest
from backend.data.prepare_training_data import calculate_rsi, generate_labels
import pandas as pd


class TestPrepareTrainingData(unittest.TestCase):
    def test_calculate_rsi(self):
        prices = pd.Series([100, 102, 104, 103, 105, 107, 106])
        rsi = calculate_rsi(prices)
        self.assertEqual(
            len(rsi), len(prices)
        )  # Ensure RSI has the same length as prices
        self.assertFalse(rsi.isnull().all())  # Ensure RSI is calculated

    def test_generate_labels(self):
        prices = pd.Series([100, 102, 104, 103, 105, 107, 106])
        labels = generate_labels(prices, threshold=0.02)
        self.assertEqual(len(labels), len(prices))  # Ensure labels have the same length
        self.assertIn(1, labels.values)  # Ensure BUY signals are generated
        self.assertIn(-1, labels.values)  # Ensure SELL signals are generated


if __name__ == "__main__":
    unittest.main()
