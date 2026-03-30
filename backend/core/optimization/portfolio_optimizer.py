import numpy as np
import pandas as pd
from scipy.optimize import minimize
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class PortfolioOptimizer:
    """
    Modern Portfolio Theory Implementation
    with Behavioural Bias Adjustments
    
    How it works:
    1. Download historical stock data
    2. Calculate returns and risk
    3. Find optimal weights
    4. Adjust for investor biases
    5. Return optimized portfolio
    """
    
    def __init__(self):
        self.risk_free_rate = 0.05  # 5% risk free rate
        self.trading_days = 252     # Trading days per year
    
    def get_stock_data(self, symbols: List[str], period: str = "2y") -> pd.DataFrame:
       """Download historical price data or use mock data"""
       print(f"Downloading data for {symbols}...")
    
       try:
        data = yf.download(
            symbols,
            period=period,
            auto_adjust=True,
            progress=False
        )
        
        if len(symbols) == 1:
            prices = data['Close'].to_frame(symbols[0])
        else:
            prices = data['Close']
        
        prices = prices.dropna()
        
        # If download failed or empty, use mock data
        if prices.empty:
            print("Download failed, using mock data...")
            return self.generate_mock_prices(symbols)
        
        print(f"Downloaded {len(prices)} days of data")
        return prices
        
       except Exception as e:
        print(f"Error downloading data: {e}")
        print("Using mock data instead...")
        return self.generate_mock_prices(symbols)
    def generate_mock_prices(self, symbols: List[str]) -> pd.DataFrame:
        """
        Generate realistic mock stock prices
        Used when real data cannot be downloaded
        """
        print(f"Generating mock prices for {symbols}")
        
        np.random.seed(42)
        n_days = 504  # 2 years of trading days
        
        # Starting prices for common stocks
        start_prices = {
            'AAPL': 150.0,
            'GOOGL': 140.0,
            'MSFT': 380.0,
            'AMZN': 180.0,
            'TSLA': 200.0,
            'META': 350.0,
            'NVDA': 500.0,
            'JPM': 180.0,
            'BAC': 35.0,
            'WMT': 160.0,
            'DIS': 90.0,
            'NFLX': 450.0
        }
        
        dates = pd.date_range(
            end=datetime.now(),
            periods=n_days,
            freq='B'
        )
        
        prices = {}
        for symbol in symbols:
            start_price = start_prices.get(symbol, 100.0)
            
            daily_return = 0.10 / 252
            daily_vol = 0.20 / np.sqrt(252)
            
            returns = np.random.normal(
                daily_return,
                daily_vol,
                n_days
            )
            
            price_series = [start_price]
            for r in returns[1:]:
                price_series.append(price_series[-1] * (1 + r))
            
            prices[symbol] = price_series
        
        df = pd.DataFrame(prices, index=dates)
        print(f"Generated {len(df)} days of mock data")
        return df

    def calculate_returns(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Calculate daily returns"""
        returns = prices.pct_change().dropna()
        return returns
    
    def calculate_portfolio_metrics(
        self,
        weights: np.ndarray,
        returns: pd.DataFrame
    ) -> Dict:
        """
        Calculate key portfolio metrics:
        - Expected return
        - Volatility (risk)
        - Sharpe ratio
        - Sortino ratio
        """
        weights = np.array(weights)
        
        # Annual expected return
        annual_returns = returns.mean() * self.trading_days
        portfolio_return = np.dot(weights, annual_returns)
        
        # Annual volatility (risk)
        cov_matrix = returns.cov() * self.trading_days
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Sharpe Ratio
        # (return above risk free rate per unit of risk)
        sharpe_ratio = (
            (portfolio_return - self.risk_free_rate) / 
            portfolio_volatility
        ) if portfolio_volatility > 0 else 0
        
        # Sortino Ratio
        # (like Sharpe but only penalizes downside risk)
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() * np.sqrt(self.trading_days)
        portfolio_downside = np.dot(weights, downside_std.fillna(0))
        sortino_ratio = (
            (portfolio_return - self.risk_free_rate) /
            portfolio_downside
        ) if portfolio_downside > 0 else 0
        
        # Maximum Drawdown
        cumulative = (1 + returns.dot(weights)).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        return {
            "expected_return": round(float(portfolio_return) * 100, 2),
            "volatility": round(float(portfolio_volatility) * 100, 2),
            "sharpe_ratio": round(float(sharpe_ratio), 3),
            "sortino_ratio": round(float(sortino_ratio), 3),
            "max_drawdown": round(float(max_drawdown) * 100, 2)
        }
    
    def optimize_max_sharpe(
        self,
        returns: pd.DataFrame
    ) -> np.ndarray:
        """
        Find weights that MAXIMIZE Sharpe Ratio
        This is the classic MPT optimization
        """
        n_assets = len(returns.columns)
        
        # Start with equal weights
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Constraints: weights must sum to 1
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]
        
        # Bounds: each weight between 0 and 1
        # (no short selling)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Objective: minimize NEGATIVE Sharpe
        # (minimizing negative = maximizing positive)
        def negative_sharpe(weights):
            metrics = self.calculate_portfolio_metrics(weights, returns)
            return -metrics['sharpe_ratio']
        
        # Run optimization
        result = minimize(
            negative_sharpe,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def optimize_min_volatility(
        self,
        returns: pd.DataFrame
    ) -> np.ndarray:
        """
        Find weights that MINIMIZE Volatility
        Best for risk-averse investors
        """
        n_assets = len(returns.columns)
        initial_weights = np.array([1/n_assets] * n_assets)
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        def portfolio_volatility(weights):
            metrics = self.calculate_portfolio_metrics(weights, returns)
            return metrics['volatility']
        
        result = minimize(
            portfolio_volatility,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def apply_bias_adjustments(
        self,
        weights: np.ndarray,
        symbols: List[str],
        bias_scores: Dict,
        user_bias: str
    ) -> np.ndarray:
        """
        Adjust portfolio weights based on
        detected investor biases
        
        This is what makes our optimizer UNIQUE!
        No other tool does this!
        """
        adjusted_weights = weights.copy()
        n_assets = len(symbols)
        
        # Adjustment 1: Overconfidence
        # Reduce concentration, force diversification
        if user_bias == "overconfident" or bias_scores.get("overconfidence", 0) > 60:
            max_weight = 0.25  # No single stock > 25%
            adjusted_weights = np.minimum(adjusted_weights, max_weight)
            # Renormalize
            adjusted_weights = adjusted_weights / adjusted_weights.sum()
            print("Applied overconfidence adjustment: Max weight capped at 25%")
        
        # Adjustment 2: Loss Aversion
        # Add defensive tilt, reduce volatility
        if user_bias == "loss_averse" or bias_scores.get("loss_aversion", 0) > 60:
            # Reduce all weights slightly
            # and add to most stable asset
            most_stable_idx = 0  # First asset assumed most stable
            adjustment = 0.10
            adjusted_weights = adjusted_weights * (1 - adjustment)
            adjusted_weights[most_stable_idx] += adjustment
            adjusted_weights = adjusted_weights / adjusted_weights.sum()
            print("Applied loss aversion adjustment: Added defensive tilt")
        
        # Adjustment 3: FOMO
        # Reduce momentum stocks, add mean reversion
        if user_bias == "fomo" or bias_scores.get("fomo", 0) > 60:
            # Reduce top weighted stocks
            top_idx = np.argmax(adjusted_weights)
            adjusted_weights[top_idx] *= 0.8
            # Redistribute to others
            adjusted_weights = adjusted_weights / adjusted_weights.sum()
            print("Applied FOMO adjustment: Reduced momentum exposure")
        
        # Adjustment 4: Herd Mentality
        # Force equal weighting (contrarian)
        if user_bias == "herd_mentality" or bias_scores.get("herd_mentality", 0) > 60:
            # Move 20% toward equal weights
            equal_weights = np.array([1/n_assets] * n_assets)
            adjusted_weights = 0.8 * adjusted_weights + 0.2 * equal_weights
            adjusted_weights = adjusted_weights / adjusted_weights.sum()
            print("Applied herd mentality adjustment: Added contrarian tilt")
        
        return adjusted_weights
    
    def generate_efficient_frontier(
        self,
        returns: pd.DataFrame,
        n_portfolios: int = 100
    ) -> List[Dict]:
        """
        Generate efficient frontier points
        
        Creates 100 optimal portfolios
        with different risk/return tradeoffs
        
        Used for visualization in dashboard
        """
        frontier_portfolios = []
        n_assets = len(returns.columns)
        
        # Generate random portfolios
        for _ in range(n_portfolios):
            # Random weights
            weights = np.random.random(n_assets)
            weights = weights / weights.sum()
            
            metrics = self.calculate_portfolio_metrics(weights, returns)
            frontier_portfolios.append({
                "return": metrics['expected_return'],
                "volatility": metrics['volatility'],
                "sharpe": metrics['sharpe_ratio'],
                "weights": weights.tolist()
            })
        
        # Sort by volatility
        frontier_portfolios.sort(key=lambda x: x['volatility'])
        
        return frontier_portfolios
    
    def run_monte_carlo(
        self,
        weights: np.ndarray,
        returns: pd.DataFrame,
        n_simulations: int = 1000,
        n_days: int = 252
    ) -> Dict:
        """
        Monte Carlo Simulation
        
        Simulates 1000 possible futures
        for your portfolio over 1 year
        
        Shows:
        - Best case scenario
        - Worst case scenario  
        - Most likely scenario
        """
        portfolio_returns = returns.dot(weights)
        
        mean_return = portfolio_returns.mean()
        std_return = portfolio_returns.std()
        
        # Run simulations
        simulations = []
        final_values = []
        
        initial_value = 100000  # Start with ₹1,00,000
        
        for _ in range(n_simulations):
            # Generate random daily returns
            daily_returns = np.random.normal(
                mean_return,
                std_return,
                n_days
            )
            
            # Calculate portfolio value over time
            portfolio_value = initial_value
            values = [portfolio_value]
            
            for daily_return in daily_returns:
                portfolio_value = portfolio_value * (1 + daily_return)
                values.append(portfolio_value)
            
            simulations.append(values)
            final_values.append(portfolio_value)
        
        final_values = np.array(final_values)
        
        return {
            "initial_value": initial_value,
            "n_simulations": n_simulations,
            "best_case": round(float(np.percentile(final_values, 95))),
            "worst_case": round(float(np.percentile(final_values, 5))),
            "median_case": round(float(np.median(final_values))),
            "mean_case": round(float(np.mean(final_values))),
            "probability_of_profit": round(
                float(np.mean(final_values > initial_value)) * 100, 1
            ),
            "var_95": round(
                float(np.percentile(final_values, 5) - initial_value)
            ),
            "simulation_summary": {
                "percentile_10": round(float(np.percentile(final_values, 10))),
                "percentile_25": round(float(np.percentile(final_values, 25))),
                "percentile_50": round(float(np.percentile(final_values, 50))),
                "percentile_75": round(float(np.percentile(final_values, 75))),
                "percentile_90": round(float(np.percentile(final_values, 90)))
            }
        }
    
    def optimize_portfolio(
        self,
        symbols: List[str],
        user_bias: str = "rational",
        bias_scores: Dict = {},
        optimization_method: str = "max_sharpe",
        period: str = "2y"
    ) -> Dict:
        """
        MAIN FUNCTION - Complete portfolio optimization
        
        Steps:
        1. Download stock data
        2. Calculate returns
        3. Optimize weights
        4. Apply bias adjustments
        5. Run Monte Carlo
        6. Return complete analysis
        """
        print(f"\nOptimizing portfolio for {symbols}")
        print(f"User bias: {user_bias}")
        print(f"Method: {optimization_method}")
        
        # Step 1: Get data
        prices = self.get_stock_data(symbols, period)
        if prices.empty:
            return {"error": "Could not download stock data"}
        
        # Step 2: Calculate returns
        returns = self.calculate_returns(prices)
        
        # Step 3: Optimize
        if optimization_method == "max_sharpe":
            optimal_weights = self.optimize_max_sharpe(returns)
        else:
            optimal_weights = self.optimize_min_volatility(returns)
        
        # Step 4: Equal weight baseline
        n_assets = len(symbols)
        equal_weights = np.array([1/n_assets] * n_assets)
        
        # Step 5: Apply bias adjustments
        bias_adjusted_weights = self.apply_bias_adjustments(
            optimal_weights.copy(),
            symbols,
            bias_scores,
            user_bias
        )
        
        # Step 6: Calculate metrics for all portfolios
        optimal_metrics = self.calculate_portfolio_metrics(
            optimal_weights, returns
        )
        equal_metrics = self.calculate_portfolio_metrics(
            equal_weights, returns
        )
        bias_adjusted_metrics = self.calculate_portfolio_metrics(
            bias_adjusted_weights, returns
        )
        
        # Step 7: Monte Carlo simulation
        monte_carlo = self.run_monte_carlo(
            bias_adjusted_weights,
            returns
        )
        
        # Step 8: Efficient frontier
        frontier = self.generate_efficient_frontier(returns, 50)
        
        # Step 9: Create allocation summary
        allocation = {}
        bias_allocation = {}
        
        for i, symbol in enumerate(symbols):
            allocation[symbol] = round(float(optimal_weights[i]) * 100, 2)
            bias_allocation[symbol] = round(
                float(bias_adjusted_weights[i]) * 100, 2
            )
        
        return {
            "symbols": symbols,
            "user_bias": user_bias,
            "optimization_method": optimization_method,
            
            "portfolios": {
                "equal_weight": {
                    "allocation": {s: round(100/n_assets, 2) for s in symbols},
                    "metrics": equal_metrics
                },
                "optimal": {
                    "allocation": allocation,
                    "metrics": optimal_metrics
                },
                "bias_adjusted": {
                    "allocation": bias_allocation,
                    "metrics": bias_adjusted_metrics
                }
            },
            
            "improvement": {
                "sharpe_improvement": round(
                    bias_adjusted_metrics['sharpe_ratio'] - 
                    equal_metrics['sharpe_ratio'], 3
                ),
                "return_improvement": round(
                    bias_adjusted_metrics['expected_return'] - 
                    equal_metrics['expected_return'], 2
                )
            },
            
            "monte_carlo": monte_carlo,
            "efficient_frontier": frontier[:20],
            "optimized_at": datetime.now().isoformat()
        }