def technical_analysis(close_prices):
    current_price = close_prices[-1]
    moving_avg = sum(close_prices[-5:]) / 5
    signal = "BUY" if current_price > moving_avg else "SELL"
    print(f"Technical Analysis: Price {current_price:.5f} vs SMA(5) {moving_avg:.5f} => {signal}")
    return signal
