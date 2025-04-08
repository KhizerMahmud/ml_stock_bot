import tkinter as tk
from tkinter import ttk
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import datetime

class StockChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Stock Chart")
        self.root.geometry("900x700")

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="Real-Time Stock Chart", font=("Helvetica", 20))
        title.pack(pady=10)

        # Stock input frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        self.stock_entry = ttk.Entry(input_frame, width=30)
        self.stock_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(input_frame, text="Show Chart", command=self.start_chart)
        search_button.pack(side=tk.LEFT)

        # Matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.ax.set_title("Stock Price")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

    def start_chart(self):
        stock_symbol = self.stock_entry.get().upper()
        if not stock_symbol:
            return

        # Clear the previous plot
        self.ax.clear()
        self.ax.set_title(f"Real-Time Stock Price: {stock_symbol}")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")

        # Start real-time updates
        self.update_chart(stock_symbol)

    def update_chart(self, stock_symbol):
        def fetch_data():
            # Fetch the latest stock data
            now = datetime.datetime.now()
            start_time = now - datetime.timedelta(minutes=5)  # Fetch last 5 minutes of data
            data = yf.download(
                stock_symbol,
                start=start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end=now.strftime("%Y-%m-%d %H:%M:%S"),
                interval="1m",
            )
            return data

        def animate(i):
            data = fetch_data()
            if not data.empty:
                self.ax.clear()
                self.ax.plot(data.index, data["Close"], label="Close Price", color="blue")
                self.ax.set_title(f"Real-Time Stock Price: {stock_symbol}")
                self.ax.set_xlabel("Time")
                self.ax.set_ylabel("Price")
                self.ax.legend()
                self.canvas.draw()

        # Use Matplotlib's FuncAnimation for real-time updates
        self.animation = FuncAnimation(self.figure, animate, interval=1000)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockChartApp(root)
    root.mainloop()