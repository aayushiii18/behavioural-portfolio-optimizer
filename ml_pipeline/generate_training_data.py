import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
import os

class TrainingDataGenerator:
    """
    Generates realistic trading data for ML training
    
    Creates 4 types of investors:
    1. Overconfident trader (trades too much)
    2. Loss averse trader (holds losers, sells winners)
    3. FOMO trader (buys at peaks)
    4. Rational trader (balanced decisions)
    """
    
    def __init__(self):
        self.symbols = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 
            'TSLA', 'META', 'NVDA', 'JPM',
            'BAC', 'WMT', 'DIS', 'NFLX'
        ]
        self.market_conditions = ['bull', 'bear', 'volatile', 'stable']
    
    def generate_overconfident_trader(self, user_id: str):
        """
        Overconfident trader characteristics:
        - Trades very frequently (30+ per month)
        - Takes large positions
        - Short holding periods
        - Trades in volatile markets
        """
        transactions = []
        date = datetime.now() - timedelta(days=365)
        
        # Generate 300+ trades (very high frequency)
        for i in range(300):
            symbol = random.choice(self.symbols)
            action = random.choice(['BUY', 'SELL'])
            
            transactions.append({
                "transaction_id": f"TXN{i:04d}",
                "user_id": user_id,
                "symbol": symbol,
                "action": action,
                # Large quantities (overconfident)
                "quantity": random.randint(15, 50),
                "price": round(random.uniform(50, 500), 2),
                "total_value": round(random.uniform(1000, 25000), 2),
                "date": (date + timedelta(days=random.randint(0, 365))).isoformat(),
                # Trades in volatile conditions
                "market_condition": random.choice(['volatile', 'bull']),
                "holding_days": random.randint(1, 7),  # Very short holds
                "bias_label": "overconfident"
            })
        
        return transactions
    
    def generate_loss_averse_trader(self, user_id: str):
        """
        Loss averse trader characteristics:
        - Sells winners quickly (less than 10% gain)
        - Holds losers too long
        - Avoids selling at a loss
        - Conservative position sizes
        """
        transactions = []
        date = datetime.now() - timedelta(days=365)
        
        for i in range(150):
            symbol = random.choice(self.symbols)
            action = random.choice(['BUY', 'SELL'])
            buy_price = round(random.uniform(50, 500), 2)
            
            # If selling, sell winners early or hold losers
            if action == 'SELL':
                if random.random() > 0.3:
                    # Sell winner early (small gain)
                    sell_price = buy_price * random.uniform(1.01, 1.08)
                else:
                    # Hold loser (big loss)
                    sell_price = buy_price * random.uniform(0.60, 0.85)
            else:
                sell_price = buy_price
            
            transactions.append({
                "transaction_id": f"TXN{i:04d}",
                "user_id": user_id,
                "symbol": symbol,
                "action": action,
                "quantity": random.randint(5, 20),
                "price": round(sell_price, 2),
                "total_value": round(sell_price * random.randint(5, 20), 2),
                "date": (date + timedelta(days=random.randint(0, 365))).isoformat(),
                "market_condition": random.choice(self.market_conditions),
                # Long holds for losers
                "holding_days": random.randint(30, 365),
                "bias_label": "loss_averse"
            })
        
        return transactions
    
    def generate_fomo_trader(self, user_id: str):
        """
        FOMO trader characteristics:
        - Buys during bull markets at peaks
        - Large quantities when market is hot
        - Chases trending stocks
        - Panic sells during bear markets
        """
        transactions = []
        date = datetime.now() - timedelta(days=365)
        
        # FOMO stocks (trending/popular)
        fomo_symbols = ['TSLA', 'NVDA', 'META', 'AAPL', 'AMZN']
        
        for i in range(200):
            # Mostly buys trending stocks in bull market
            action = 'BUY' if random.random() > 0.3 else 'SELL'
            symbol = random.choice(fomo_symbols)
            
            transactions.append({
                "transaction_id": f"TXN{i:04d}",
                "user_id": user_id,
                "symbol": symbol,
                "action": action,
                # Large quantities (FOMO buying)
                "quantity": random.randint(10, 40),
                "price": round(random.uniform(100, 800), 2),
                "total_value": round(random.uniform(5000, 30000), 2),
                "date": (date + timedelta(days=random.randint(0, 365))).isoformat(),
                # Mostly bull market (chasing performance)
                "market_condition": random.choice(['bull', 'bull', 'volatile']),
                "holding_days": random.randint(1, 30),
                "bias_label": "fomo"
            })
        
        return transactions
    
    def generate_rational_trader(self, user_id: str):
        """
        Rational trader characteristics:
        - Moderate trading frequency
        - Balanced buy/sell decisions
        - Longer holding periods
        - Trades in all market conditions
        - Smaller position sizes
        """
        transactions = []
        date = datetime.now() - timedelta(days=365)
        
        for i in range(80):
            symbol = random.choice(self.symbols)
            action = random.choice(['BUY', 'SELL'])
            
            transactions.append({
                "transaction_id": f"TXN{i:04d}",
                "user_id": user_id,
                "symbol": symbol,
                "action": action,
                # Small balanced quantities
                "quantity": random.randint(1, 10),
                "price": round(random.uniform(50, 300), 2),
                "total_value": round(random.uniform(500, 5000), 2),
                "date": (date + timedelta(days=random.randint(0, 365))).isoformat(),
                # All market conditions
                "market_condition": random.choice(self.market_conditions),
                # Long holding periods
                "holding_days": random.randint(30, 180),
                "bias_label": "rational"
            })
        
        return transactions
    
    def generate_full_dataset(self, num_users_per_type: int = 50):
        """
        Generate complete training dataset
        with all 4 trader types
        """
        all_transactions = []
        all_labels = []
        
        print(f"Generating training data for {num_users_per_type * 4} users...")
        
        for i in range(num_users_per_type):
            # Overconfident traders
            user_id = f"overconfident_user_{i}"
            txns = self.generate_overconfident_trader(user_id)
            features = self.extract_features(txns)
            all_transactions.append(features)
            all_labels.append("overconfident")
            
            # Loss averse traders
            user_id = f"loss_averse_user_{i}"
            txns = self.generate_loss_averse_trader(user_id)
            features = self.extract_features(txns)
            all_transactions.append(features)
            all_labels.append("loss_averse")
            
            # FOMO traders
            user_id = f"fomo_user_{i}"
            txns = self.generate_fomo_trader(user_id)
            features = self.extract_features(txns)
            all_transactions.append(features)
            all_labels.append("fomo")
            
            # Rational traders
            user_id = f"rational_user_{i}"
            txns = self.generate_rational_trader(user_id)
            features = self.extract_features(txns)
            all_transactions.append(features)
            all_labels.append("rational")
        
        # Create DataFrame
        df = pd.DataFrame(all_transactions)
        df['bias_label'] = all_labels
        
        print(f"Dataset generated: {len(df)} samples")
        print(f"Label distribution:\n{df['bias_label'].value_counts()}")
        
        return df
    
    def extract_features(self, transactions: list) -> dict:
        """
        Extract numerical features from transactions
        These are the inputs to our ML model
        
        Think of features like:
        symptoms a doctor looks at
        before making a diagnosis
        """
        if not transactions:
            return {}
        
        df = pd.DataFrame(transactions)
        
        # Feature 1: Trading frequency
        trades_per_month = len(transactions) / 12
        
        # Feature 2: Average quantity per trade
        avg_quantity = df['quantity'].mean()
        
        # Feature 3: Average trade value
        avg_value = df['total_value'].mean()
        
        # Feature 4: Buy/Sell ratio
        buys = len(df[df['action'] == 'BUY'])
        sells = len(df[df['action'] == 'SELL'])
        buy_sell_ratio = buys / sells if sells > 0 else buys
        
        # Feature 5: Bull market trading ratio
        bull_trades = len(df[df['market_condition'] == 'bull'])
        bull_ratio = bull_trades / len(transactions)
        
        # Feature 6: Bear market trading ratio
        bear_trades = len(df[df['market_condition'] == 'bear'])
        bear_ratio = bear_trades / len(transactions)
        
        # Feature 7: Volatile market trading ratio
        volatile_trades = len(df[df['market_condition'] == 'volatile'])
        volatile_ratio = volatile_trades / len(transactions)
        
        # Feature 8: Average holding period
        avg_holding = df['holding_days'].mean()
        
        # Feature 9: Max single trade value
        max_trade_value = df['total_value'].max()
        
        # Feature 10: Total number of trades
        total_trades = len(transactions)
        
        # Feature 11: Unique stocks traded
        unique_stocks = df['symbol'].nunique()
        
        # Feature 12: Concentration ratio
        # (how concentrated in one stock)
        most_traded = df['symbol'].value_counts().iloc[0]
        concentration = most_traded / total_trades
        
        return {
            "trades_per_month": round(trades_per_month, 2),
            "avg_quantity": round(avg_quantity, 2),
            "avg_value": round(avg_value, 2),
            "buy_sell_ratio": round(buy_sell_ratio, 2),
            "bull_ratio": round(bull_ratio, 2),
            "bear_ratio": round(bear_ratio, 2),
            "volatile_ratio": round(volatile_ratio, 2),
            "avg_holding_days": round(avg_holding, 2),
            "max_trade_value": round(max_trade_value, 2),
            "total_trades": total_trades,
            "unique_stocks": unique_stocks,
            "concentration_ratio": round(concentration, 2)
        }
    
    def save_dataset(self, df: pd.DataFrame, filename: str = "training_data.csv"):
        """Save dataset to file"""
        # Save to ml_pipeline/data/raw/
        save_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data", "raw", filename
        )
        df.to_csv(save_path, index=False)
        print(f"Dataset saved to {save_path}")
        return save_path


if __name__ == "__main__":
    generator = TrainingDataGenerator()
    df = generator.generate_full_dataset(num_users_per_type=50)
    generator.save_dataset(df)
    print("\nFirst few rows:")
    print(df.head())
    print("\nFeature columns:")
    print(df.columns.tolist())