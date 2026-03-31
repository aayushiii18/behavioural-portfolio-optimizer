import pytest
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMLModel:
    """Tests for ML Bias Detection Model"""
    
    def test_model_files_exist(self):
        """Check if trained model files exist"""
        model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "ml_pipeline", "models", "saved_models"
        )
        
        model_file = os.path.join(model_path, "bias_model.pkl")
        scaler_file = os.path.join(model_path, "scaler.pkl")
        
        assert os.path.exists(model_file), \
            "Model file not found! Run train_model.py first"
        assert os.path.exists(scaler_file), \
            "Scaler file not found! Run train_model.py first"
        
        print(f"✅ Model Files Test: Both files exist!")
    
    def test_model_prediction(self):
        """Test ML model makes valid predictions"""
        from core.ml.bias_predictor import MLBiasPredictor
        from data.processors.transaction_analyzer import TransactionAnalyzer
        
        predictor = MLBiasPredictor()
        analyzer = TransactionAnalyzer()
        
        transactions = analyzer.generate_mock_transactions("test", 100)
        result = predictor.predict_bias(transactions)
        
        assert 'predicted_bias' in result
        assert 'confidence_score' in result
        
        valid_biases = [
            'overconfident', 'loss_averse', 
            'fomo', 'rational'
        ]
        assert result['predicted_bias'] in valid_biases, \
            f"Invalid bias: {result['predicted_bias']}"
        
        assert 0 <= result['confidence_score'] <= 100
        
        print(f"✅ Model Prediction Test: {result['predicted_bias']} ({result['confidence_score']}%)")
    
    def test_feature_extraction(self):
        """Test feature extraction from transactions"""
        from core.ml.bias_predictor import MLBiasPredictor
        from data.processors.transaction_analyzer import TransactionAnalyzer
        
        predictor = MLBiasPredictor()
        analyzer = TransactionAnalyzer()
        
        transactions = analyzer.generate_mock_transactions("test", 50)
        features = predictor.extract_features(transactions)
        
        required_features = [
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
        
        for feature in required_features:
            assert feature in features, \
                f"Missing feature: {feature}"
        
        print(f"✅ Feature Extraction Test: All {len(required_features)} features present!")
    
    def test_nudge_generation(self):
        """Test nudge generation for each bias"""
        from core.ml.bias_predictor import MLBiasPredictor
        
        predictor = MLBiasPredictor()
        
        biases = ['overconfident', 'loss_averse', 'fomo', 'rational']
        
        for bias in biases:
            nudges = predictor.generate_nudges(bias, {})
            assert len(nudges) > 0, f"No nudges for {bias}"
            
            for nudge in nudges:
                assert 'type' in nudge
                assert 'message' in nudge
                assert 'action' in nudge
            
            print(f"✅ Nudge Generation Test: {bias} has {len(nudges)} nudges")


class TestPortfolioOptimizer:
    """Tests for Portfolio Optimizer"""
    
    def setup_method(self):
        from core.optimization.portfolio_optimizer import PortfolioOptimizer
        self.optimizer = PortfolioOptimizer()
    
    def test_mock_price_generation(self):
        """Test mock price generation"""
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        prices = self.optimizer.generate_mock_prices(symbols)
        
        assert not prices.empty
        assert len(prices.columns) == len(symbols)
        assert len(prices) > 0
        
        # All prices should be positive
        assert (prices > 0).all().all()
        
        print(f"✅ Mock Prices Test: Generated {len(prices)} days for {len(symbols)} stocks")
    
    def test_returns_calculation(self):
        """Test returns calculation"""
        symbols = ['AAPL', 'GOOGL']
        prices = self.optimizer.generate_mock_prices(symbols)
        returns = self.optimizer.calculate_returns(prices)
        
        assert not returns.empty
        assert len(returns) == len(prices) - 1
        
        print(f"✅ Returns Calculation Test: {len(returns)} return periods")
    
    def test_portfolio_metrics(self):
        """Test portfolio metrics calculation"""
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        prices = self.optimizer.generate_mock_prices(symbols)
        returns = self.optimizer.calculate_returns(prices)
        
        weights = np.array([1/3, 1/3, 1/3])
        metrics = self.optimizer.calculate_portfolio_metrics(weights, returns)
        
        assert 'expected_return' in metrics
        assert 'volatility' in metrics
        assert 'sharpe_ratio' in metrics
        assert 'max_drawdown' in metrics
        
        # Volatility should be positive
        assert metrics['volatility'] > 0
        
        print(f"✅ Portfolio Metrics Test: Sharpe = {metrics['sharpe_ratio']}")
    
    def test_optimization(self):
        """Test portfolio optimization"""
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        prices = self.optimizer.generate_mock_prices(symbols)
        returns = self.optimizer.calculate_returns(prices)
        
        weights = self.optimizer.optimize_max_sharpe(returns)
        
        # Weights should sum to 1
        assert abs(sum(weights) - 1.0) < 0.01
        
        # All weights should be >= 0
        assert all(w >= 0 for w in weights)
        
        print(f"✅ Optimization Test: Weights = {[round(w*100, 1) for w in weights]}%")
    
    def test_monte_carlo_simulation(self):
        """Test Monte Carlo simulation"""
        symbols = ['AAPL', 'GOOGL']
        prices = self.optimizer.generate_mock_prices(symbols)
        returns = self.optimizer.calculate_returns(prices)
        
        weights = np.array([0.5, 0.5])
        result = self.optimizer.run_monte_carlo(
            weights, returns,
            n_simulations=100,
            n_days=252
        )
        
        assert 'best_case' in result
        assert 'worst_case' in result
        assert 'median_case' in result
        assert 'probability_of_profit' in result
        
        # Best case > worst case
        assert result['best_case'] > result['worst_case']
        
        # Probability between 0 and 100
        assert 0 <= result['probability_of_profit'] <= 100
        
        print(f"✅ Monte Carlo Test: {result['probability_of_profit']}% profit probability")