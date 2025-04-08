import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump, load

class StockPredictor:
    def __init__(self, model_path="stock_model.joblib"):
        self.model_path = model_path
        try:
            self.model = load(model_path)  # Load pre-trained model if available
        except FileNotFoundError:
            self.model = RandomForestClassifier()  # Initialize a new model

    def train(self, data):
        """
        Train the model using historical data.
        :param data: DataFrame with features and target labels.
        """
        features = data.drop(columns=["target"])  # Drop the target column
        target = data["target"]  # Target column (e.g., BUY=1, SELL=-1, HOLD=0)

        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model trained with accuracy: {accuracy:.2f}")

        # Save the trained model
        dump(self.model, self.model_path)

    def predict(self, features):
        """
        Predict the action (BUY, SELL, HOLD) based on input features.
        :param features: DataFrame with the same structure as training features.
        :return: Predicted action.
        """
        return self.model.predict(features)

    def update_model(self, data):
        """
        Update the model with new data to learn from mistakes.
        :param data: DataFrame with new features and target labels.
        """
        self.train(data)