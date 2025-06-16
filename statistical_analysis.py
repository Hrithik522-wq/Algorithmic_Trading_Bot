import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

VISUAL_DIR = "visuals"
os.makedirs(VISUAL_DIR, exist_ok=True)

def analyze_statistics(close_prices):
    mean_price = np.mean(close_prices)
    std_dev = np.std(close_prices)
    sma = np.mean(close_prices[-5:])
    ema = np.average(close_prices[-5:], weights=np.linspace(1, 2, 5))
    max_price = np.max(close_prices)
    min_price = np.min(close_prices)

    print(f"Statistical Analysis - Mean: {mean_price:.5f}, Std Dev: {std_dev:.5f}")
    print(f"SMA(5): {sma:.5f}, EMA(5): {ema:.5f}")
    print(f"Max: {max_price:.5f}, Min: {min_price:.5f}")

def trend_analysis(close_prices):
    x = list(range(len(close_prices)))
    slope, _, r_value, _, _ = linregress(x, close_prices)
    trend = "UPWARD" if slope > 0 else "DOWNWARD"
    print(f"Trend Slope: {slope:.5f} ({trend}), R²: {r_value**2:.4f}")

def plot_graphs(close_prices):
    days = list(range(len(close_prices)))
    sma = np.convolve(close_prices, np.ones(5)/5, mode='valid')
    ema = [np.average(close_prices[i-5:i], weights=np.linspace(1, 2, 5)) for i in range(5, len(close_prices))]
    volatility = [np.std(close_prices[i-5:i]) for i in range(5, len(close_prices))]

    plt.figure(figsize=(12, 6))
    plt.plot(days, close_prices, label='Close Price', alpha=0.5)
    plt.plot(days[4:], sma, label='SMA(5)')
    plt.plot(days[5:], ema, label='EMA(5)', linestyle='--')
    plt.title('EURUSD Price & Moving Averages')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{VISUAL_DIR}/price_moving_avg.png")
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(days[5:], volatility, label='5-Day Volatility', color='orange')
    plt.title('Rolling Volatility')
    plt.xlabel('Days')
    plt.ylabel('Standard Deviation')
    plt.tight_layout()
    plt.savefig(f"{VISUAL_DIR}/volatility.png")
    plt.close()
