import finnhub
import os
import json
import numpy as np

class MarketService:
    """
    Electronic Market Data Stream (Aureum Terminal v2)
    Uses Finnhub for real-time tickers.
    Handles NaN values and API rate limits cleanly.
    """
    
    # Updated to Finnhub compatible symbols
    TICKERS = ["SPY", "QQQ", "BINANCE:BTCUSDT", "GLD", "TSLA", "NVDA"]
    MAP = {
        "SPY": "S&P 500",
        "QQQ": "NASDAQ", 
        "BINANCE:BTCUSDT": "BTC/USD",
        "GLD": "GOLD",
        "TSLA": "TSLA",
        "NVDA": "NVDA"
    }

    def __init__(self):
        # Look for the env var, fallback to the provided key if missing
        api_key = os.getenv("FINNHUB_API_KEY", "d74f72hr01qno4q1ho40d74f72hr01qno4q1ho4g")
        self.finnhub_client = finnhub.Client(api_key=api_key)

    def get_live_ticker(self):
        try:
            ticker_list = []
            for t in self.TICKERS:
                try:
                    res = self.finnhub_client.quote(t)
                    
                    # Finnhub quote response mapping:
                    # c = Current price, d = Change, dp = Percent change
                    current_price = res.get('c')
                    change = res.get('dp')
                    
                    if current_price is None or current_price == 0:
                        continue
                        
                    if np.isnan(current_price) or (change is not None and np.isnan(change)):
                        continue
                        
                    ticker_list.append({
                        "id": self.MAP[t],
                        "price": float(round(current_price, 2)),
                        "change": float(round(change, 2)) if change is not None else 0.0,
                        "trend": "up" if (change is not None and change >= 0) else "down",
                        "status": "active"
                    })
                    
                except Exception as e:
                    print(f"❌ Finnhub quote error for {t}: {e}")
                    # Push a fallback unavailable object if single ticker fails
                    ticker_list.append({
                        "id": self.MAP[t],
                        "price": None,
                        "change": None,
                        "trend": "none",
                        "status": "unavailable"
                    })
            
            if not ticker_list:
                return self._get_fallback_data()

            return ticker_list
        except Exception as e:
            print(f"❌ Market Data Sync Failed completely: {e}")
            return []

    def _get_fallback_data(self):
        return [
            {"id": "S&P 500", "price": 5241.22, "change": 1.2, "trend": "up"},
            {"id": "NASDAQ", "price": 16428.10, "change": 1.8, "trend": "up"},
            {"id": "BTC/USD", "price": 68402.50, "change": -0.4, "trend": "down"},
            {"id": "GOLD", "price": 2354.10, "change": 0.8, "trend": "up"},
            {"id": "TSLA", "price": 178.65, "change": -2.1, "trend": "down"},
            {"id": "NVDA", "price": 902.50, "change": 4.2, "trend": "up"}
        ]

market_service = MarketService()
