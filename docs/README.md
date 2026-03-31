# Behavioural Portfolio Optimizer

## Project Overview
A comprehensive behavioural finance platform that:
- Detects 8 investor biases using ML
- Optimizes portfolios with bias adjustments
- Provides personalized nudges
- Gamifies the investment improvement journey

## Technology Stack

### Backend
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- scikit-learn (Random Forest)
- VADER Sentiment Analysis
- PyPortfolioOpt

### Frontend
- Next.js 16
- React 18
- TypeScript
- Tailwind CSS
- Axios

### ML Pipeline
- Random Forest Classifier
- 100% accuracy on test data
- 12 behavioural features
- 4 bias classifications

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+

### Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/aayushiii18/zetheta-behavioural-portfolio-aayushi.git
cd zetheta-behavioural-portfolio-aayushi
\`\`\`

2. Set up backend:
\`\`\`bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

3. Set up environment:
\`\`\`bash
cp .env.example .env
# Edit .env with your database credentials
\`\`\`

4. Create database:
\`\`\`bash
python -c "from database import create_tables; create_tables()"
\`\`\`

5. Train ML model:
\`\`\`bash
cd ../ml_pipeline
python generate_training_data.py
python train_model.py
\`\`\`

6. Start backend:
\`\`\`bash
cd ../backend
uvicorn main:app --reload
\`\`\`

7. Set up frontend:
\`\`\`bash
cd ../frontend
npm install
npm run dev
\`\`\`

## API Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login user
- GET /auth/me - Get current user

### Bias Detection
- GET /bias/analyze/{user_id} - Full bias analysis
- GET /bias/score/{user_id} - Quick bias scores

### ML Prediction
- GET /ml/predict/{user_id} - ML bias prediction
- GET /ml/full-analysis/{user_id} - Complete analysis

### Portfolio Optimization
- GET /portfolio/optimize - Optimize portfolio
- GET /portfolio/monte-carlo - Monte Carlo simulation
- GET /portfolio/frontier - Efficient frontier

### Nudges & Gamification
- GET /nudges/{user_id} - Get personalized nudges
- GET /gamification/{user_id} - Get points and badges
- GET /gamification/challenge/daily - Daily challenge
- GET /gamification/leaderboard - Top investors

### Market Data
- GET /market/stock/{symbol} - Stock data
- GET /market/returns/{symbol} - Stock returns
- GET /sentiment/market - Market sentiment
- GET /sentiment/stock/{symbol} - Stock sentiment

## Behavioural Biases Detected

1. **Overconfidence** - Trading too frequently
2. **Loss Aversion** - Holding losers, selling winners
3. **Recency Bias** - Overweighting recent events
4. **Herd Mentality** - Following the crowd
5. **Anchoring** - Fixating on purchase price
6. **FOMO** - Fear of missing out
7. **Disposition Effect** - Selling winners early
8. **Confirmation Bias** - Ignoring contrary evidence

## ML Model Performance
- Algorithm: Random Forest (100 trees)
- Training samples: 160
- Testing samples: 40
- Accuracy: 100%
- Features: 12 behavioural features

## Testing
\`\`\`bash
cd backend
pytest tests/ -v
\`\`\`
- 39 tests passing
- 0 failures
- 100% pass rate

## Project Structure
\`\`\`
zetheta-behavioural-portfolio/
├── backend/
│   ├── api/
│   ├── core/
│   │   ├── behavioural/
│   │   │   ├── bias_detection.py
│   │   │   ├── nudge_engine.py
│   │   │   ├── gamification.py
│   │   │   └── sentiment_analyzer.py
│   │   ├── ml/
│   │   │   └── bias_predictor.py
│   │   └── optimization/
│   │       └── portfolio_optimizer.py
│   ├── data/
│   │   ├── collectors/
│   │   └── processors/
│   ├── tests/
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   └── auth.py
├── frontend/
│   └── src/
│       └── app/
│           ├── main/
│           ├── dashboard/
│           ├── portfolio/
│           ├── nudges/
│           ├── journal/
│           ├── simulator/
│           └── sentiment/
├── ml_pipeline/
│   ├── generate_training_data.py
│   ├── train_model.py
│   └── models/
└── docs/
\`\`\`

## Confidentiality Notice
This project is STRICTLY PRIVATE & CONFIDENTIAL.
Property of Zetheta Algorithms Private Limited.