import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.behavioural.bias_detection import BiasDetector
from data.processors.transaction_analyzer import TransactionAnalyzer

class TestBiasDetection:
    """
    Unit tests for Bias Detection System
    
    Tests all 8 biases to make sure
    they detect correctly
    """
    
    def setup_method(self):
        """Setup before each test"""
        self.detector = BiasDetector()
        self.analyzer = TransactionAnalyzer()
    
    # ==================
    # TEST 1: OVERCONFIDENCE
    # ==================
    def test_overconfidence_high(self):
        """
        Test that high frequency trading
        = high overconfidence score
        """
        # Generate overconfident trades
        # (many trades = overconfident)
        transactions = []
        for i in range(300):
            transactions.append({
                "transaction_id": f"TXN{i}",
                "user_id": "test_user",
                "symbol": "AAPL",
                "action": "BUY" if i % 2 == 0 else "SELL",
                "quantity": 20,
                "price": 150.0,
                "total_value": 3000.0,
                "date": "2024-01-01T00:00:00",
                "market_condition": "volatile",
                "holding_days": 2
            })
        
        result = self.detector.detect_overconfidence(transactions)
        
        # High frequency = high score
        assert result['score'] >= 50, \
            f"Expected score >= 50, got {result['score']}"
        assert result['level'] in ['Medium', 'High'], \
            f"Expected Medium or High level"
        
        print(f"✅ Overconfidence High Test: Score = {result['score']}")
    
    def test_overconfidence_low(self):
        """
        Test that low frequency trading
        = low overconfidence score
        """
        # Generate rational trades (few trades)
        transactions = []
        for i in range(20):
            transactions.append({
                "transaction_id": f"TXN{i}",
                "user_id": "test_user",
                "symbol": "AAPL",
                "action": "BUY" if i % 2 == 0 else "SELL",
                "quantity": 5,
                "price": 150.0,
                "total_value": 750.0,
                "date": "2024-01-01T00:00:00",
                "market_condition": "stable",
                "holding_days": 90
            })
        
        result = self.detector.detect_overconfidence(transactions)
        
        # Low frequency = low score
        assert result['score'] <= 50, \
            f"Expected score <= 50, got {result['score']}"
        
        print(f"✅ Overconfidence Low Test: Score = {result['score']}")
    
    def test_overconfidence_empty(self):
        """Test with empty transactions"""
        result = self.detector.detect_overconfidence([])
        assert result['score'] == 0
        print(f"✅ Overconfidence Empty Test: Score = {result['score']}")
    
    # ==================
    # TEST 2: FOMO
    # ==================
    def test_fomo_detection(self):
        """
        Test FOMO detection
        Buying in bull market with large quantities
        """
        transactions = []
        for i in range(100):
            transactions.append({
                "transaction_id": f"TXN{i}",
                "user_id": "test_user",
                "symbol": "TSLA",
                "action": "BUY",
                "quantity": 20,  # Large quantity
                "price": 300.0,
                "total_value": 6000.0,
                "date": "2024-01-01T00:00:00",
                "market_condition": "bull",  # Bull market
                "holding_days": 5
            })
        
        result = self.detector.detect_fomo(transactions)
        
        assert result['score'] >= 0
        assert 'fomo_trades' in result
        assert 'nudge' in result
        
        print(f"✅ FOMO Detection Test: Score = {result['score']}")
    
    # ==================
    # TEST 3: HERD MENTALITY
    # ==================
    def test_herd_mentality(self):
        """
        Test herd mentality detection
        Trading popular stocks in bull market
        """
        # Popular/herd stocks
        herd_stocks = ['TSLA', 'NVDA', 'META', 'AAPL', 'AMC']
        
        transactions = []
        for i in range(50):
            transactions.append({
                "transaction_id": f"TXN{i}",
                "user_id": "test_user",
                "symbol": herd_stocks[i % len(herd_stocks)],
                "action": "BUY",
                "quantity": 10,
                "price": 200.0,
                "total_value": 2000.0,
                "date": "2024-01-01T00:00:00",
                "market_condition": "bull",
                "holding_days": 10
            })
        
        result = self.detector.detect_herd_mentality(transactions)
        
        assert result['score'] >= 0
        assert result['score'] <= 100
        assert 'herd_stock_trades' in result
        
        print(f"✅ Herd Mentality Test: Score = {result['score']}")
    
    # ==================
    # TEST 4: FULL ANALYSIS
    # ==================
    def test_full_bias_analysis(self):
        """
        Test complete bias analysis
        Should return all 8 biases
        """
        # Generate mock transactions
        transactions = self.analyzer.generate_mock_transactions(
            "test_user", 50
        )
        
        result = self.detector.analyze_all_biases(transactions)
        
        # Check structure
        assert 'biases' in result
        assert 'overall_score' in result
        assert 'dominant_bias' in result
        assert 'overall_level' in result
        
        # Check all 8 biases present
        expected_biases = [
            'overconfidence',
            'loss_aversion',
            'recency_bias',
            'herd_mentality',
            'anchoring',
            'fomo',
            'disposition_effect',
            'confirmation_bias'
        ]
        
        for bias in expected_biases:
            assert bias in result['biases'], \
                f"Missing bias: {bias}"
        
        # Score should be 0-100
        assert 0 <= result['overall_score'] <= 100
        
        print(f"✅ Full Analysis Test: Overall Score = {result['overall_score']}")
        print(f"   Dominant Bias = {result['dominant_bias']}")
    
    # ==================
    # TEST 5: BIAS SCORES RANGE
    # ==================
    def test_bias_scores_in_range(self):
        """
        All bias scores should be between 0 and 100
        """
        transactions = self.analyzer.generate_mock_transactions(
            "test_user", 50
        )
        
        result = self.detector.analyze_all_biases(transactions)
        
        for bias_name, bias_data in result['biases'].items():
            score = bias_data['score']
            assert 0 <= score <= 100, \
                f"{bias_name} score {score} is out of range!"
        
        print(f"✅ Bias Scores Range Test: All scores in valid range!")
    
    # ==================
    # TEST 6: LEVEL ASSIGNMENT
    # ==================
    def test_level_assignment(self):
        """
        Test that levels are assigned correctly
        """
        assert self.detector._get_level(80) == "High"
        assert self.detector._get_level(55) == "Medium"
        assert self.detector._get_level(30) == "Low"
        assert self.detector._get_level(10) == "Minimal"
        
        print(f"✅ Level Assignment Test: All levels correct!")


class TestTransactionAnalyzer:
    """
    Tests for Transaction Analyzer
    """
    
    def setup_method(self):
        self.analyzer = TransactionAnalyzer()
    
    def test_generate_mock_transactions(self):
        """Test mock transaction generation"""
        transactions = self.analyzer.generate_mock_transactions(
            "test_user", 50
        )
        
        assert len(transactions) == 50
        
        # Check structure of each transaction
        for txn in transactions:
            assert 'transaction_id' in txn
            assert 'symbol' in txn
            assert 'action' in txn
            assert 'quantity' in txn
            assert 'price' in txn
            assert txn['action'] in ['BUY', 'SELL']
        
        print(f"✅ Mock Transactions Test: Generated {len(transactions)} transactions")
    
    def test_panic_selling_detection(self):
        """Test panic selling detection"""
        transactions = self.analyzer.generate_mock_transactions(
            "test_user", 100
        )
        
        result = self.analyzer.detect_panic_selling(transactions)
        
        assert 'panic_sell_count' in result
        assert 'panic_sell_score' in result
        assert 0 <= result['panic_sell_score'] <= 100
        
        print(f"✅ Panic Selling Test: Count = {result['panic_sell_count']}")
    
    def test_win_loss_ratio(self):
        """Test win/loss ratio calculation"""
        transactions = self.analyzer.generate_mock_transactions(
            "test_user", 100
        )
        
        result = self.analyzer.calculate_win_loss_ratio(transactions)
        
        assert 'wins' in result
        assert 'losses' in result
        assert 'win_rate' in result
        assert 0 <= result['win_rate'] <= 100
        
        print(f"✅ Win/Loss Test: Win Rate = {result['win_rate']}%")
    
    def test_full_analysis(self):
        """Test complete transaction analysis"""
        transactions = self.analyzer.generate_mock_transactions(
            "test_user", 100
        )
        
        result = self.analyzer.full_analysis(transactions)
        
        assert 'holding_periods' in result
        assert 'panic_selling' in result
        assert 'fomo_buying' in result
        assert 'win_loss' in result
        assert 'total_transactions' in result
        
        print(f"✅ Full Analysis Test: {result['total_transactions']} transactions analyzed")