import MetaTrader5 as mt5
import random
import csv
from datetime import datetime
from technical_analysis import technical_analysis
from fundamental_analysis import fundamental_analysis
from sentiment_analysis import sentiment_analysis

LOG_FILE = "trade_log.csv"

if not mt5.initialize():
    print("MT5 failed to initialize")
    exit()
try:
    with open(LOG_FILE, mode='x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "symbol", "action", "price", "lot", "technical", "fundamental", "sentiment"])
except FileExistsError:
    pass

def log_trade(action, symbol, price, lot, technical, fundamental, sentiment):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), symbol, action, price, lot, technical, fundamental, sentiment])

def calculate_lot_size(balance, stop_loss_pips, risk_percent, symbol="EURUSD"):
    pip_value = 0.0001 if "JPY" not in symbol else 0.01
    sl_price_distance = stop_loss_pips * pip_value
    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (sl_price_distance * 100000)
    return round(max(0.01, min(lot_size, 1.0)), 2)

def buy(symbol, technical, fundamental, sentiment):
    tick = mt5.symbol_info_tick(symbol)
    account_info = mt5.account_info()
    risk_percent = round(random.uniform(1.0, 2.0), 2)
    lot = calculate_lot_size(account_info.balance, 50, risk_percent, symbol)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "sl": tick.ask - 0.005,
        "tp": tick.ask + 0.01,
        "deviation": 10,
        "magic": 123456,
        "comment": f"Greedy Buy {risk_percent}%",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    result = mt5.order_send(request)
    print(f"BUY Order result: {result.retcode}")
    log_trade("BUY", symbol, tick.ask, lot, technical, fundamental, sentiment)

def sell(symbol, volume, technical, fundamental, sentiment):
    tick = mt5.symbol_info_tick(symbol)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL,
        "price": tick.bid,
        "deviation": 10,
        "magic": 123456,
        "comment": "Greedy Sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    result = mt5.order_send(request)
    print(f"SELL Order result: {result.retcode}")
    log_trade("SELL", symbol, tick.bid, volume, technical, fundamental, sentiment)

def run_greedy_strategy(symbol, close_prices):
    current_price = close_prices[-1]
    max_drop = 0
    for i in range(len(close_prices) - 1):
        drop = (close_prices[i] - current_price) / close_prices[i]
        if drop > max_drop:
            max_drop = drop

    technical = technical_analysis(close_prices)
    fundamental = fundamental_analysis()
    sentiment = sentiment_analysis()
    positions = mt5.positions_get(symbol=symbol)

    if not positions and max_drop > 0.03 and technical == "BUY" and fundamental == "positive" and sentiment == "positive":
        buy(symbol, technical, fundamental, sentiment)
    elif positions:
        last_buy_price = positions[0].price_open
        gain = (current_price - last_buy_price) / last_buy_price
        if gain > 0.05:
            sell(symbol, positions[0].volume, technical, fundamental, sentiment)
