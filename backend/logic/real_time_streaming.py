import websocket
import json
import threading
from decision_making import StockBotApp

class RealTimeStockBot:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.ws_url = "wss://your-websocket-api-url"  # Replace with your WebSocket API URL
        self.app = StockBotApp(None)  # Initialize your decision-making logic

    def on_message(self, ws, message):
        data = json.loads(message)
        if "price" in data:  # Adjust based on your WebSocket API response
            current_price = data["price"]
            print(f"Real-time price for {self.stock_symbol}: {current_price}")
            # Trigger decision-making logic
            self.app.analyze_stock(self.stock_symbol, current_price)

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(self, ws):
        # Subscribe to the stock symbol
        subscribe_message = json.dumps({
            "type": "subscribe",
            "symbol": self.stock_symbol
        })
        ws.send(subscribe_message)

    def start_streaming(self):
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.on_open = self.on_open
        threading.Thread(target=ws.run_forever).start()

if __name__ == "__main__":
    stock_bot = RealTimeStockBot("AAPL")  # Replace with your stock symbol
    stock_bot.start_streaming()