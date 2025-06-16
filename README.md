# Algorithmic Trading Bot

A trading bot that analyzes the market using statistics, sentiment, technical and fundamental analysis, and trades using a greedy strategy.

# Features
- 1-year data analysis
- Technical, sentiment, fundamental signals
- Greedy algorithm for buy/sell
- Graphs and logs generated

# How to Run
1. Install requirements:
2. Create a `.env` file:
3. Then run:
4. run main.py file 


##  What It Does

-  Connects to MetaTrader5 to fetch **1-year historical price data**
-  Performs:
  - 📊 Statistical analysis (volatility, trend, mean, SMA, EMA)
  - 🔍 Technical analysis (SMA-based buy/sell signal)
  - 💬 Sentiment analysis (from live news headlines)
  - 📰 Fundamental analysis (from ECB-related financial news)
-  Uses a **Greedy Algorithm** to:
  - Buy when price has dropped most in 1 year (and signals agree)
  - Sell when profit > 5%
- Logs trades in `trade_log.csv`
- Saves price/volatility graphs in `visuals/` folder

- ## 📂 Project Structure

trading_bot/
├── main.py
├── data_fetcher.py
├── statistical_analysis.py
├── technical_analysis.py
├── sentiment_analysis.py
├── fundamental_analysis.py
├── trading_strategy.py
├── trade_log.csv
├── .env (not uploaded)
└── visuals/
└── price_moving_avg.png
└── volatility.png


