from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, UserProfile
from schemas import UserRegister, UserLogin, Token, UserResponse
from auth import hash_password, verify_password, create_access_token, get_current_user
from data.collectors.market_data import MarketDataCollector
from data.processors.transaction_analyzer import TransactionAnalyzer
from core.behavioural.bias_detection import BiasDetector
from core.behavioural.sentiment_analyzer import SentimentAnalyzer
from core.ml.bias_predictor import MLBiasPredictor
from core.optimization.portfolio_optimizer import PortfolioOptimizer
import numpy as np

router = APIRouter()

# ==================
# AUTH ROUTES
# ==================

@router.post("/auth/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(UserProfile).filter(
        UserProfile.email == user_data.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = UserProfile(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(UserProfile).filter(
        UserProfile.email == user_data.email
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Create token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user: UserProfile = Depends(get_current_user)):
    return current_user

@router.get("/market/stock/{symbol}")
def get_stock_data(symbol: str, period: str = "1y"):
    collector = MarketDataCollector()
    data = collector.get_stock_data(symbol.upper(), period)
    if not data:
        raise HTTPException(
            status_code=404, 
            detail="Stock not found"
        )
    return data

@router.get("/market/returns/{symbol}")
def get_stock_returns(symbol: str, period: str = "1y"):
    collector = MarketDataCollector()
    returns = collector.calculate_returns(symbol.upper(), period)
    if not returns:
        raise HTTPException(
            status_code=404, 
            detail="Could not calculate returns"
        )
    return returns

@router.get("/market/multiple")
def get_multiple_stocks(
    symbols: str = "AAPL,GOOGL,MSFT",
    period: str = "1y"
):
    collector = MarketDataCollector()
    symbol_list = symbols.split(",")
    data = collector.get_multiple_stocks(symbol_list, period)
    return data


# ==================
# TRANSACTION ROUTES
# ==================

@router.get("/transactions/mock/{user_id}")
def get_mock_transactions(user_id: str):
    analyzer = TransactionAnalyzer()
    transactions = analyzer.generate_mock_transactions(user_id)
    return {"transactions": transactions}

@router.get("/transactions/analyze/{user_id}")
def analyze_transactions(user_id: str):
    analyzer = TransactionAnalyzer()
    transactions = analyzer.generate_mock_transactions(user_id)
    analysis = analyzer.full_analysis(transactions)
    return analysis

# ==================
# SENTIMENT ROUTES
# ==================

@router.get("/sentiment/stock/{symbol}")
def get_stock_sentiment(symbol: str):
    """Get sentiment analysis for a stock"""
    analyzer = SentimentAnalyzer()
    result = analyzer.get_stock_sentiment(symbol.upper())
    return result

@router.get("/sentiment/market")
def get_market_sentiment():
    """Get overall market sentiment"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_market_sample_news()
    return result

@router.get("/sentiment/emotional/{user_id}")
def get_emotional_trading(user_id: str):
    """Detect emotional trading patterns"""
    txn_analyzer = TransactionAnalyzer()
    sentiment_analyzer = SentimentAnalyzer()
    
    transactions = txn_analyzer.generate_mock_transactions(user_id)
    market_sentiment = sentiment_analyzer.analyze_market_sample_news()
    
    emotional_analysis = sentiment_analyzer.detect_emotional_trading(
        transactions,
        market_sentiment['avg_compound_score']
    )
    
    return {
        "user_id": user_id,
        "market_sentiment": market_sentiment['overall_sentiment'],
        "market_sentiment_score": market_sentiment['avg_compound_score'],
        "emotional_trading": emotional_analysis

    }
# ==================
# ML PREDICTION ROUTES
# ==================

@router.get("/ml/predict/{user_id}")
def ml_predict_bias(user_id: str):
    """
    Use ML model to predict investor bias
    More accurate than rule-based detection
    """
    txn_analyzer = TransactionAnalyzer()
    ml_predictor = MLBiasPredictor()
    
    # Get transactions
    transactions = txn_analyzer.generate_mock_transactions(user_id)
    
    # ML prediction
    prediction = ml_predictor.predict_bias(transactions)
    
    return {
        "user_id": user_id,
        "ml_prediction": prediction
    }

@router.get("/ml/full-analysis/{user_id}")
def ml_full_analysis(user_id: str):
    """
    Complete analysis combining:
    1. ML bias prediction
    2. Rule-based bias detection
    3. Sentiment analysis
    4. Personalized nudges
    """
    txn_analyzer = TransactionAnalyzer()
    ml_predictor = MLBiasPredictor()
    bias_detector = BiasDetector()
    sentiment_analyzer = SentimentAnalyzer()
    
    # Get transactions
    transactions = txn_analyzer.generate_mock_transactions(user_id)
    
    # Run all analyses
    ml_prediction = ml_predictor.predict_bias(transactions)
    rule_based = bias_detector.analyze_all_biases(transactions)
    market_sentiment = sentiment_analyzer.analyze_market_sample_news()
    transaction_analysis = txn_analyzer.full_analysis(transactions)
    
    return {
        "user_id": user_id,
        "ml_prediction": ml_prediction,
        "rule_based_analysis": rule_based,
        "market_sentiment": market_sentiment,
        "transaction_analysis": transaction_analysis,
        "summary": {
            "primary_bias": ml_prediction.get("predicted_bias"),
            "confidence": ml_prediction.get("confidence_score"),
            "overall_bias_score": rule_based.get("overall_score"),
            "market_sentiment": market_sentiment.get("overall_sentiment"),
            "nudges": ml_prediction.get("nudges", [])
        }
    }
# ==================
# BIAS DETECTION ROUTES
# ==================

@router.get("/bias/analyze/{user_id}")
def analyze_biases(user_id: str):
    """Analyze all 8 biases for a user"""
    analyzer = TransactionAnalyzer()
    detector = BiasDetector()
    
    # Get transactions
    transactions = analyzer.generate_mock_transactions(user_id)
    
    # Analyze biases
    bias_report = detector.analyze_all_biases(transactions)
    
    return bias_report

@router.get("/bias/score/{user_id}")
def get_bias_score(user_id: str):
    """Get quick bias score summary"""
    analyzer = TransactionAnalyzer()
    detector = BiasDetector()
    
    transactions = analyzer.generate_mock_transactions(user_id)
    bias_report = detector.analyze_all_biases(transactions)
    
    return {
        "user_id": user_id,
        "overall_score": bias_report["overall_score"],
        "overall_level": bias_report["overall_level"],
        "dominant_bias": bias_report["dominant_bias"],
        "bias_scores": {
            bias: data["score"] 
            for bias, data in bias_report["biases"].items()
        }
    }
# ==================
# PORTFOLIO OPTIMIZATION ROUTES
# ==================

@router.get("/portfolio/optimize")
def optimize_portfolio(
    symbols: str = "AAPL,GOOGL,MSFT,AMZN,JPM",
    user_bias: str = "rational",
    method: str = "max_sharpe"
):
    """
    Optimize portfolio with bias adjustments
    symbols: comma separated stock symbols
    user_bias: overconfident/loss_averse/fomo/rational
    method: max_sharpe/min_volatility
    """
    optimizer = PortfolioOptimizer()
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    
    result = optimizer.optimize_portfolio(
        symbols=symbol_list,
        user_bias=user_bias,
        optimization_method=method
    )
    return result

@router.get("/portfolio/monte-carlo")
def run_monte_carlo(
    symbols: str = "AAPL,GOOGL,MSFT",
    user_bias: str = "rational"
):
    """Run Monte Carlo simulation"""
    optimizer = PortfolioOptimizer()
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    
    prices = optimizer.get_stock_data(symbol_list)
    returns = optimizer.calculate_returns(prices)
    
    n_assets = len(symbol_list)
    equal_weights = np.array([1/n_assets] * n_assets)
    
    monte_carlo = optimizer.run_monte_carlo(equal_weights, returns)
    return monte_carlo

@router.get("/portfolio/frontier")
def get_efficient_frontier(
    symbols: str = "AAPL,GOOGL,MSFT,AMZN"
):
    """Get efficient frontier data"""
    optimizer = PortfolioOptimizer()
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    
    prices = optimizer.get_stock_data(symbol_list)
    returns = optimizer.calculate_returns(prices)
    
    frontier = optimizer.generate_efficient_frontier(returns, 50)
    return {"frontier": frontier}