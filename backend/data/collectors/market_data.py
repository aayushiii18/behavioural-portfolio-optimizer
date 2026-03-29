import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MarketDataCollector:
    def __init__(self):
        self.default_symbols = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 
            'TSLA', 'META', 'NVDA', 'JPM',
            'SPY', 'QQQ'
        ]
    
    def get_stock_data(self, symbol: str, period: str = "1y"):
        """Download stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return None
                
            return {
                "symbol": symbol,
                "data": data.reset_index().to_dict(orient="records"),
                "current_price": float(data['Close'].iloc[-1]),
                "price_change": float(data['Close'].iloc[-1] - data['Close'].iloc[-2]),
                "price_change_pct": float(
                    (data['Close'].iloc[-1] - data['Close'].iloc[-2]) / 
                    data['Close'].iloc[-2] * 100
                ),
                "52_week_high": float(data['High'].max()),
                "52_week_low": float(data['Low'].min()),
                "avg_volume": float(data['Volume'].mean())
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def get_multiple_stocks(self, symbols: list, period: str = "1y"):
        """Download data for multiple stocks"""
        results = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol, period)
            if data:
                results[symbol] = data
        return results
    
    def get_portfolio_data(self, holdings: dict, period: str = "1y"):
        """
        Get data for a portfolio
        holdings = {"AAPL": 10, "GOOGL": 5} 
        (symbol: number of shares)
        """
        portfolio_data = {}
        total_value = 0
        
        for symbol, shares in holdings.items():
            stock_data = self.get_stock_data(symbol, period)
            if stock_data:
                position_value = stock_data['current_price'] * shares
                total_value += position_value
                portfolio_data[symbol] = {
                    **stock_data,
                    "shares": shares,
                    "position_value": position_value
                }
        
        # Calculate weights
        for symbol in portfolio_data:
            portfolio_data[symbol]['weight'] = (
                portfolio_data[symbol]['position_value'] / total_value
            )
        
        return {
            "holdings": portfolio_data,
            "total_value": total_value,
            "last_updated": datetime.now().isoformat()
        }
    
    def calculate_returns(self, symbol: str, period: str = "1y"):
        """Calculate returns for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return None
            
            # Daily returns
            daily_returns = data['Close'].pct_change().dropna()
            
            return {
                "symbol": symbol,
                "daily_returns": daily_returns.tolist(),
                "mean_return": float(daily_returns.mean()),
                "std_return": float(daily_returns.std()),
                "total_return": float(
                    (data['Close'].iloc[-1] - data['Close'].iloc[0]) / 
                    data['Close'].iloc[0] * 100
                ),
                "sharpe_ratio": float(
                    daily_returns.mean() / daily_returns.std() * np.sqrt(252)
                ) if daily_returns.std() != 0 else 0
            }
        except Exception as e:
            print(f"Error calculating returns for {symbol}: {e}")
            return None