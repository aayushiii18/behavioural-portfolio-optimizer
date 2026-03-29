from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, UserProfile
from schemas import UserRegister, UserLogin, Token, UserResponse
from auth import hash_password, verify_password, create_access_token, get_current_user
from data.collectors.market_data import MarketDataCollector
from data.processors.transaction_analyzer import TransactionAnalyzer

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