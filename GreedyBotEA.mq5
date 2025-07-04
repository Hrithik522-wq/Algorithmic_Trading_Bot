//EA using Greedy logic + SMA (MQL5 fixed version)        
#property strict

input int    LookbackBars    = 250;   // Lookback range for max price (approx 1 year on D1)
input double DropThreshold   = 3.0;   // % drop from max price to trigger BUY
input double TakeProfit      = 100;   // TP in points (10 pips)
input double StopLoss        = 50;    // SL in points (5 pips)
input double RiskPercent     = 1.0;   // Risk % of balance

int OnInit()
  {
   Print("✅ GreedyBotEA initialized.");
   return(INIT_SUCCEEDED);
  }
  
void OnTick()
  {
   string symbol = _Symbol;
   ENUM_TIMEFRAMES tf = PERIOD_D1;

   // Ensure enough data
   if (Bars(symbol, tf) < LookbackBars + 5)
     {
      Print("❌ Not enough bars for analysis.");
      return;
     }

   // Technical Analysis: 5-day SMA
   int ma_handle = iMA(symbol, tf, 5, 0, MODE_SMA, PRICE_CLOSE);
   double sma_val[];
   if (CopyBuffer(ma_handle, 0, 0, 1, sma_val) <= 0)
     {
      Print("❌ Failed to get SMA.");
      return;
     }

   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double sma = sma_val[0];
   string techSignal = (ask > sma) ? "BUY" : "SELL";

   // Greedy Drop Check
   double maxPrice = iHigh(symbol, tf, iHighest(symbol, tf, MODE_HIGH, LookbackBars, 1));
   double dropPercent = 100 * (maxPrice - ask) / maxPrice;

   // Simulated sentiment/fundamental
   bool sentimentPositive = true;
   bool fundamentalPositive = true;

   // Place BUY if conditions met
   if (PositionsTotal() == 0 && dropPercent > DropThreshold && techSignal == "BUY" && sentimentPositive && fundamentalPositive)
     {
      double lotSize = CalculateLot(symbol, StopLoss);
      MqlTradeRequest request;
      MqlTradeResult result;
      ZeroMemory(request);

      request.action = TRADE_ACTION_DEAL;
      request.symbol = symbol;
      request.volume = lotSize;
      request.type = ORDER_TYPE_BUY;
      request.price = ask;
      request.sl = ask - StopLoss * _Point;
      request.tp = ask + TakeProfit * _Point;
      request.deviation = 10;
      request.type_filling = ORDER_FILLING_IOC;
      request.comment = "GreedyBotEA Buy";

      if (OrderSend(request, result) && result.retcode == TRADE_RETCODE_DONE)
         Print("✅ BUY order placed at ", ask);
      else
         Print("❌ Buy failed: ", result.retcode);
     }

   // Sell if profit > 5%
   if (PositionSelect(symbol))
     {
      double entry = PositionGetDouble(POSITION_PRICE_OPEN);
      double profitPercent = 100 * (bid - entry) / entry;

      if (profitPercent > 5.0)
        {
         double vol = PositionGetDouble(POSITION_VOLUME);
         MqlTradeRequest request;
         MqlTradeResult result;
         ZeroMemory(request);

         request.action = TRADE_ACTION_DEAL;
         request.symbol = symbol;
         request.volume = vol;
         request.type = ORDER_TYPE_SELL;
         request.price = bid;
         request.deviation = 10;
         request.type_filling = ORDER_FILLING_IOC;
         request.comment = "GreedyBotEA Close";

         if (OrderSend(request, result) && result.retcode == TRADE_RETCODE_DONE)
            Print("✅ SELL closed at ", bid, " profit: ", profitPercent, "%");
         else
            Print("❌ Sell failed: ", result.retcode);
        }
     }
  }
// Calculate lot size based on balance and risk

double CalculateLot(string symbol, double stopLossPips)
  {
   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount = balance * RiskPercent / 100;
   double pipValue = 10.0; // approx for 1 lot on major pairs
   double lot = riskAmount / (stopLossPips * pipValue);
   return NormalizeDouble(MathMax(0.01, MathMin(1.0, lot)), 2);
  }
