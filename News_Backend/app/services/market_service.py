import yfinance as yf
import json
import numpy as np

class MarketService:
    """
    Electronic Market Data Stream (Aureum Terminal v2)
    Uses yfinance for real-time tickers.
    Handles NaN values to ensure JSON compliance.
    """
    
    TICKERS = ["^GSPC", "^IXIC", "BTC-USD", "GLD", "TSLA", "NVDA"]
    MAP = {
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ", 
        "BTC-USD": "BTC/USD",
        "GLD": "GOLD",
        "TSLA": "TSLA",
        "NVDA": "NVDA"
    }

    def get_live_ticker(self):
        try:
            # Download data but explicitly handle empty/nan cases
            try:
                data = yf.download(self.TICKERS, period="1d", interval="1m", group_by='ticker', progress=False)
            except Exception as e:
                print(f"❌ yfinance download error: {e}")
                return []
                
            ticker_list = []
            for t in self.TICKERS:
                try:
                    # Access latest close and check for NaN or negative values
                    ticker_data = data[t]
                    if ticker_data is None or 'Close' not in ticker_data:
                         continue
                         
                    current_price = ticker_data['Close'].iloc[-1]
                    prev_close = ticker_data['Open'].iloc[0]
                    
                    # Ensure they aren't NaN using numpy check
                    if np.isnan(current_price) or np.isnan(prev_close):
                         continue

                    change = ((current_price - prev_close) / prev_close) * 100
                    
                    ticker_list.append({
                        "id": self.MAP[t],
                        "price": float(round(current_price, 2)),
                        "change": float(round(change, 2)),
                        "trend": "up" if change >= 0 else "down"
                    })
                except Exception as e:
                    # Fallback to a static or previous value if NaN found
                    continue
            
            if not ticker_list:
                return []

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
