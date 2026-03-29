import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class TransactionAnalyzer:
    def __init__(self):
        self.panic_sell_threshold = -0.05  # 5% drop triggers panic
        self.fomo_buy_threshold = 0.05     # 5% rise triggers FOMO
    
    def generate_mock_transactions(self, user_id: str, num_transactions: int = 50):
        """Generate realistic mock trading history for testing"""
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA']
        actions = ['BUY', 'SELL']
        
        transactions = []
        start_date = datetime.now() - timedelta(days=365)
        
        for i in range(num_transactions):
            symbol = random.choice(symbols)
            action = random.choice(actions)
            price = random.uniform(50, 500)
            quantity = random.randint(1, 20)
            date = start_date + timedelta(days=random.randint(0, 365))
            
            transactions.append({
                "transaction_id": f"TXN{i+1:04d}",
                "user_id": user_id,
                "symbol": symbol,
                "action": action,
                "price": round(price, 2),
                "quantity": quantity,
                "total_value": round(price * quantity, 2),
                "date": date.isoformat(),
                "market_condition": random.choice([
                    "bull", "bear", "volatile", "stable"
                ])
            })
        
        return sorted(transactions, key=lambda x: x['date'])
    
    def analyze_holding_periods(self, transactions: list):
        """Analyze how long investor holds positions"""
        holdings = {}
        holding_periods = []
        
        for txn in transactions:
            symbol = txn['symbol']
            
            if txn['action'] == 'BUY':
                holdings[symbol] = txn['date']
            
            elif txn['action'] == 'SELL' and symbol in holdings:
                buy_date = datetime.fromisoformat(holdings[symbol])
                sell_date = datetime.fromisoformat(txn['date'])
                holding_period = (sell_date - buy_date).days
                holding_periods.append(holding_period)
                del holdings[symbol]
        
        if not holding_periods:
            return {"avg_holding_days": 0, "min_holding": 0, "max_holding": 0}
            
        return {
            "avg_holding_days": np.mean(holding_periods),
            "min_holding": min(holding_periods),
            "max_holding": max(holding_periods),
            "holding_periods": holding_periods
        }
    
    def detect_panic_selling(self, transactions: list):
        """Detect if investor panic sells during market drops"""
        panic_sells = []
        
        for txn in transactions:
            if (txn['action'] == 'SELL' and 
                txn['market_condition'] == 'bear' and
                txn['quantity'] > 5):
                panic_sells.append(txn)
        
        panic_score = min(100, len(panic_sells) * 15)
        
        return {
            "panic_sell_count": len(panic_sells),
            "panic_sell_score": panic_score,
            "panic_transactions": panic_sells[:5]
        }
    
    def detect_fomo_buying(self, transactions: list):
        """Detect FOMO buying during market highs"""
        fomo_buys = []
        
        for txn in transactions:
            if (txn['action'] == 'BUY' and 
                txn['market_condition'] == 'bull' and
                txn['quantity'] > 10):
                fomo_buys.append(txn)
        
        fomo_score = min(100, len(fomo_buys) * 15)
        
        return {
            "fomo_buy_count": len(fomo_buys),
            "fomo_buy_score": fomo_score,
            "fomo_transactions": fomo_buys[:5]
        }
    
    def calculate_win_loss_ratio(self, transactions: list):
        """Calculate ratio of winning to losing trades"""
        wins = 0
        losses = 0
        buy_prices = {}
        
        for txn in transactions:
            symbol = txn['symbol']
            
            if txn['action'] == 'BUY':
                buy_prices[symbol] = txn['price']
            
            elif txn['action'] == 'SELL' and symbol in buy_prices:
                if txn['price'] > buy_prices[symbol]:
                    wins += 1
                else:
                    losses += 1
        
        total = wins + losses
        win_rate = (wins / total * 100) if total > 0 else 0
        
        return {
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 2),
            "win_loss_ratio": round(wins / losses, 2) if losses > 0 else wins
        }
    
    def full_analysis(self, transactions: list):
        """Run complete transaction analysis"""
        return {
            "holding_periods": self.analyze_holding_periods(transactions),
            "panic_selling": self.detect_panic_selling(transactions),
            "fomo_buying": self.detect_fomo_buying(transactions),
            "win_loss": self.calculate_win_loss_ratio(transactions),
            "total_transactions": len(transactions)
        }