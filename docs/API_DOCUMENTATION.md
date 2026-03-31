# API Documentation
## Behavioural Portfolio Optimizer API v1.0.0

Base URL: http://localhost:8000

## Authentication

### Register User
\`\`\`
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}

Response 200:
{
  "user_id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "risk_tolerance": 0.5,
  "loss_aversion_coefficient": 2.25,
  "overconfidence_score": 0.5
}
\`\`\`

### Login
\`\`\`
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}

Response 200:
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
\`\`\`

## Bias Detection

### Full Bias Analysis
\`\`\`
GET /bias/analyze/{user_id}

Response 200:
{
  "biases": {
    "overconfidence": {
      "score": 75,
      "level": "High",
      "description": "...",
      "nudge": "..."
    },
    ...
  },
  "overall_score": 45,
  "overall_level": "Low",
  "dominant_bias": "loss_aversion"
}
\`\`\`

## Portfolio Optimization

### Optimize Portfolio
\`\`\`
GET /portfolio/optimize?symbols=AAPL,GOOGL,MSFT&user_bias=rational&method=max_sharpe

Response 200:
{
  "portfolios": {
    "equal_weight": {...},
    "optimal": {...},
    "bias_adjusted": {...}
  },
  "monte_carlo": {
    "best_case": 125000,
    "worst_case": 85000,
    "median_case": 108000,
    "probability_of_profit": 72.5
  }
}
\`\`\`

## Error Codes
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error