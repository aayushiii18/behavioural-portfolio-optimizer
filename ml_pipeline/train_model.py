import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import pickle
import os
import json
from datetime import datetime

class BiasDetectionModel:
    """
    Random Forest model to detect investor biases
    
    How it works:
    1. Takes 12 trading features as input
    2. Predicts which bias the investor has
    3. Returns confidence score for each bias
    """
    
    def __init__(self):
        # Random Forest with 100 trees
        self.model = RandomForestClassifier(
            n_estimators=100,  # 100 decision trees
            max_depth=10,      # How deep each tree goes
            random_state=42,   # For reproducibility
            n_jobs=-1          # Use all CPU cores
        )
        self.scaler = StandardScaler()
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
        self.is_trained = False
        self.model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "models", "saved_models"
        )
    
    def load_data(self, data_path: str):
        """Load and prepare training data"""
        print("Loading training data...")
        df = pd.read_csv(data_path)
        
        # Separate features and labels
        X = df[self.feature_columns]
        y = df['bias_label']
        
        print(f"Dataset shape: {X.shape}")
        print(f"Labels: {y.value_counts().to_dict()}")
        
        return X, y
    
    def train(self, X, y):
        """
        Train the model
        
        Steps:
        1. Split data into train/test
        2. Scale features
        3. Train Random Forest
        4. Evaluate accuracy
        """
        print("\nTraining ML model...")
        
        # Step 1: Split into 80% train, 20% test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,    # 20% for testing
            random_state=42,
            stratify=y        # Keep equal distribution
        )
        
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        
        # Step 2: Scale features
        # (makes all features same scale)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Step 3: Train the model
        print("Training Random Forest...")
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        # Step 4: Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'='*50}")
        print(f"MODEL ACCURACY: {accuracy*100:.2f}%")
        print(f"{'='*50}")
        print("\nDetailed Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop Features (what matters most):")
        print(importance.head(5).to_string())
        
        return {
            "accuracy": round(accuracy * 100, 2),
            "training_samples": len(X_train),
            "testing_samples": len(X_test),
            "feature_importance": importance.to_dict()
        }
    
    def predict(self, features: dict):
        """
        Predict bias for a new investor
        
        Input: Dictionary of 12 features
        Output: Predicted bias + confidence scores
        """
        if not self.is_trained:
            self.load_model()
        
        # Convert to DataFrame
        X = pd.DataFrame([features])[self.feature_columns]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get prediction
        prediction = self.model.predict(X_scaled)[0]
        
        # Get probability for each bias
        probabilities = self.model.predict_proba(X_scaled)[0]
        classes = self.model.classes_
        
        # Create confidence scores
        confidence = {
            cls: round(prob * 100, 1)
            for cls, prob in zip(classes, probabilities)
        }
        
        return {
            "predicted_bias": prediction,
            "confidence": confidence,
            "confidence_score": round(max(probabilities) * 100, 1)
        }
    
    def save_model(self):
        """Save model to disk"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save model
        model_file = os.path.join(self.model_path, "bias_model.pkl")
        with open(model_file, 'wb') as f:
            pickle.dump(self.model, f)
        
        # Save scaler
        scaler_file = os.path.join(self.model_path, "scaler.pkl")
        with open(scaler_file, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save metadata
        metadata = {
            "trained_at": datetime.now().isoformat(),
            "feature_columns": self.feature_columns,
            "model_type": "RandomForestClassifier",
            "n_estimators": 100
        }
        metadata_file = os.path.join(self.model_path, "metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nModel saved to {self.model_path}")
    
    def load_model(self):
        """Load saved model from disk"""
        model_file = os.path.join(self.model_path, "bias_model.pkl")
        scaler_file = os.path.join(self.model_path, "scaler.pkl")
        
        if not os.path.exists(model_file):
            raise FileNotFoundError("Model not found! Please train first.")
        
        with open(model_file, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(scaler_file, 'rb') as f:
            self.scaler = pickle.load(f)
        
        self.is_trained = True
        print("Model loaded successfully!")


if __name__ == "__main__":
    # Paths
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data", "raw", "training_data.csv"
    )
    
    # Create and train model
    model = BiasDetectionModel()
    
    # Load data
    X, y = model.load_data(data_path)
    
    # Train
    results = model.train(X, y)
    
    # Save model
    model.save_model()
    
    # Test prediction
    print("\nTesting prediction with sample data...")
    sample_features = {
        "trades_per_month": 25,
        "avg_quantity": 30,
        "avg_value": 15000,
        "buy_sell_ratio": 1.2,
        "bull_ratio": 0.7,
        "bear_ratio": 0.1,
        "volatile_ratio": 0.6,
        "avg_holding_days": 3,
        "max_trade_value": 25000,
        "total_trades": 300,
        "unique_stocks": 8,
        "concentration_ratio": 0.2
    }
    
    prediction = model.predict(sample_features)
    print(f"\nSample Prediction:")
    print(f"Predicted Bias: {prediction['predicted_bias']}")
    print(f"Confidence: {prediction['confidence_score']}%")
    print(f"All Scores: {prediction['confidence']}")
    
    print(f"\nFinal Accuracy: {results['accuracy']}%")