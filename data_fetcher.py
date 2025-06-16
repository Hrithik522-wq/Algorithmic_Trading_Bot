
import MetaTrader5 as mt5
from datetime import datetime, timedelta

def get_close_prices(symbol, days=365):
    if not mt5.initialize():
        print("MT5 initialize() failed")
        quit()

    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        mt5.shutdown()
        quit()

    utc_from = datetime.now() - timedelta(days=days)
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_D1, utc_from, days)
    mt5.shutdown()
    return list(rates['close']) if rates is not None else []
