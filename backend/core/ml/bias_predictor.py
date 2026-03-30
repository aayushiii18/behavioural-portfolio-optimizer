import pickle
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime

class MLBiasPredictor:
    """
    Connects the trained ML model 
    to the FastAPI backend
    
    This is the bridge between:
    ml_pipeline/ (where model lives)
    backend/ (where API lives)
    """
    
    def __init__(self):
        # Path to saved model
        self.model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "..",
            "ml_pipeline", "models", "saved_models"
        )
        self.model = None
        self.scaler = None
        self.is_loaded = False
        
        self.feature_columns = [
            "trades_per_month",
            "avg_quantity",
            "avg_value",
            "buy_sell_ratio",
            "bull_ratio",
            "bear_ratio",
            "volatile_ratio",
            "avg_holding_days",
            "max_trade_value",
            "total_trades",
            "unique_stocks",
            "concentration_ratio"
        ]
    
    def load_model(self):
        """Load the trained model"""
        try:
            model_file = os.path.join(
                self.model_path, "bias_model.pkl"
            )
            scaler_file = os.path.join(
                self.model_path, "scaler.pkl"
            )
            
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(scaler_file, 'rb') as f:
                self.scaler = pickle.load(f)
            
            self.is_loaded = True
            print("ML Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def extract_features(self, transactions: list) -> dict:
        """
        Extract features from transactions
        Same as in training data generator
        """
        if not transactions:
            return None
        
        df = pd.DataFrame(transactions)
        
        trades_per_month = len(transactions) / 12
        avg_quantity = df['quantity'].mean()
        avg_value = df['total_value'].mean()
        
        buys = len(df[df['action'] == 'BUY'])
        sells = len(df[df['action'] == 'SELL'])
        buy_sell_ratio = buys / sells if sells > 0 else buys
        
        bull_trades = len(df[df['market_condition'] == 'bull'])
        bull_ratio = bull_trades / len(transactions)
        
        bear_trades = len(df[df['market_condition'] == 'bear'])
        bear_ratio = bear_trades / len(transactions)
        
        volatile_trades = len(df[df['market_condition'] == 'volatile'])
        volatile_ratio = volatile_trades / len(transactions)
        
        avg_holding = df['holding_days'].mean() if 'holding_days' in df.columns else 30
        max_trade_value = df['total_value'].max()
        total_trades = len(transactions)
        unique_stocks = df['symbol'].nunique()
        
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
    
    def predict_bias(self, transactions: list) -> dict:
        """
        Main prediction function
        
        Input: List of transactions
        Output: Bias prediction with confidence
        """
        # Load model if not loaded
        if not self.is_loaded:
            success = self.load_model()
            if not success:
                return {
                    "error": "Model not loaded",
                    "predicted_bias": "unknown",
                    "confidence_score": 0
                }
        
        # Extract features
        features = self.extract_features(transactions)
        if not features:
            return {
                "error": "No transactions to analyze",
                "predicted_bias": "unknown",
                "confidence_score": 0
            }
        
        # Convert to DataFrame
        X = pd.DataFrame([features])[self.feature_columns]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get prediction
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        classes = self.model.classes_
        
        # Confidence scores for each bias
        confidence = {
            cls: round(float(prob) * 100, 1)
            for cls, prob in zip(classes, probabilities)
        }
        
        # Generate personalized nudges
        nudges = self.generate_nudges(prediction, confidence)
        
        return {
            "predicted_bias": prediction,
            "confidence_score": round(float(max(probabilities)) * 100, 1),
            "all_bias_scores": confidence,
            "features_analyzed": features,
            "nudges": nudges,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def generate_nudges(self, bias: str, confidence: dict) -> list:
        """Generate personalized nudges based on bias"""
        nudges = []
        
        if bias == "overconfident":
            nudges = [
                {
                    "type": "warning",
                    "message": "⚠️ You trade very frequently. Research shows frequent traders earn 40% less than buy-and-hold investors.",
                    "action": "Consider holding positions for at least 30 days before selling."
                },
                {
                    "type": "tip",
                    "message": "💡 Before making a trade, ask yourself: Would I make this trade if I couldn't trade again for 1 month?",
                    "action": "Set a 24-hour cooling off period before executing trades."
                }
            ]
        
        elif bias == "loss_averse":
            nudges = [
                {
                    "type": "warning",
                    "message": "⚠️ You tend to sell winners too early and hold losers too long.",
                    "action": "Set a rule: Let winners run until they drop 10% from peak."
                },
                {
                    "type": "tip",
                    "message": "💡 Remember: The pain of a loss feels 2x stronger than the joy of an equal gain. Don't let this affect your decisions!",
                    "action": "Use stop-loss orders to remove emotion from selling decisions."
                }
            ]
        
        elif bias == "fomo":
            nudges = [
                {
                    "type": "warning",
                    "message": "⚠️ You frequently buy stocks after they've already risen significantly.",
                    "action": "Wait for a 10% pullback before buying stocks that have recently surged."
                },
                {
                    "type": "tip",
                    "message": "💡 Missing a trade is not a loss. Buying at the peak IS a loss.",
                    "action": "Set price alerts below current price instead of chasing momentum."
                }
            ]
        
        else:  # rational
            nudges = [
                {
                    "type": "success",
                    "message": "✅ Great job! Your trading patterns show rational decision-making.",
                    "action": "Keep maintaining your disciplined approach to investing."
                },
                {
                    "type": "tip",
                    "message": "💡 Continue diversifying and maintaining your long-term perspective.",
                    "action": "Consider rebalancing your portfolio quarterly."
                }
            ]
        
        return nudges