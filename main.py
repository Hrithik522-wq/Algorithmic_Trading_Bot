from data_fetcher import get_close_prices
from statistical_analysis import analyze_statistics, trend_analysis, plot_graphs
from trading_strategy import run_greedy_strategy
import time

SYMBOL = "EURUSD"
SLEEP_SECONDS = 60 * 60  # Run every 1 hour

if __name__ == "__main__":
    try:
        while True:
            all_close_prices = get_close_prices(SYMBOL, days=365)

            if len(all_close_prices) < 30:
                print("Not enough data for analysis.")
                time.sleep(SLEEP_SECONDS)
                continue
            analyze_statistics(all_close_prices)
            trend_analysis(all_close_prices)
            plot_graphs(all_close_prices)

            run_greedy_strategy(SYMBOL, all_close_prices)

            time.sleep(SLEEP_SECONDS)

    except KeyboardInterrupt:
        print("Bot manually stopped.")
