"use client";
import { useState } from "react";
import axios from "axios";

interface PortfolioMetrics {
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
  sortino_ratio: number;
  max_drawdown: number;
}

interface Portfolio {
  allocation: { [key: string]: number };
  metrics: PortfolioMetrics;
}

interface MonteCarloResult {
  initial_value: number;
  best_case: number;
  worst_case: number;
  median_case: number;
  probability_of_profit: number;
  var_95: number;
}

interface OptimizationResult {
  symbols: string[];
  user_bias: string;
  portfolios: {
    equal_weight: Portfolio;
    optimal: Portfolio;
    bias_adjusted: Portfolio;
  };
  improvement: {
    sharpe_improvement: number;
    return_improvement: number;
  };
  monte_carlo: MonteCarloResult;
}

export default function PortfolioPage() {
  const [symbols, setSymbols] = useState("AAPL,GOOGL,MSFT,AMZN,JPM");
  const [userBias, setUserBias] = useState("rational");
  const [method, setMethod] = useState("max_sharpe");
  const [result, setResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const optimizePortfolio = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.get(
        `http://localhost:8000/portfolio/optimize`,
        {
          params: {
            symbols,
            user_bias: userBias,
            method
          }
        }
      );
      setResult(response.data);
    } catch (err) {
      setError("Failed to optimize portfolio. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(value);
  };

  const getMetricColor = (value: number, isGood: boolean) => {
    if (isGood) {
      return value > 0 ? "text-green-600" : "text-red-600";
    }
    return value < 0 ? "text-green-600" : "text-red-600";
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-900 text-white p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold">
            📈 Portfolio Optimizer
          </h1>
          <p className="text-blue-200 mt-1">
            Bias-adjusted Modern Portfolio Theory
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Input Section */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            ⚙️ Optimization Settings
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Symbols */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Stock Symbols
              </label>
              <input
                type="text"
                value={symbols}
                onChange={(e) => setSymbols(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
                placeholder="AAPL,GOOGL,MSFT"
              />
              <p className="text-gray-400 text-xs mt-1">
                Comma separated symbols
              </p>
            </div>

            {/* Bias */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Your Investor Bias
              </label>
              <select
                value={userBias}
                onChange={(e) => setUserBias(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
              >
                <option value="rational">Rational Investor</option>
                <option value="overconfident">Overconfident</option>
                <option value="loss_averse">Loss Averse</option>
                <option value="fomo">FOMO Investor</option>
                <option value="herd_mentality">Herd Mentality</option>
              </select>
            </div>

            {/* Method */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Optimization Method
              </label>
              <select
                value={method}
                onChange={(e) => setMethod(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
              >
                <option value="max_sharpe">Maximize Sharpe Ratio</option>
                <option value="min_volatility">Minimize Volatility</option>
              </select>
            </div>
          </div>

          <button
            onClick={optimizePortfolio}
            disabled={loading}
            className="mt-4 w-full bg-blue-900 text-white py-3 rounded-xl font-semibold hover:bg-blue-800 transition disabled:opacity-50"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Optimizing Portfolio... (downloading market data)
              </span>
            ) : (
              "🚀 Optimize My Portfolio"
            )}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-xl">
              {error}
            </div>
          )}
        </div>

        {/* Results */}
        {result && (
          <>
            {/* Portfolio Comparison */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              {/* Equal Weight */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="font-bold text-gray-700 mb-1">
                  ⚖️ Equal Weight
                </h3>
                <p className="text-gray-400 text-sm mb-4">
                  Baseline portfolio
                </p>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Return</span>
                    <span className={`font-bold ${getMetricColor(result.portfolios.equal_weight.metrics.expected_return, true)}`}>
                      {result.portfolios.equal_weight.metrics.expected_return}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Volatility</span>
                    <span className="font-bold text-orange-600">
                      {result.portfolios.equal_weight.metrics.volatility}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Sharpe Ratio</span>
                    <span className="font-bold text-blue-600">
                      {result.portfolios.equal_weight.metrics.sharpe_ratio}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Drawdown</span>
                    <span className="font-bold text-red-600">
                      {result.portfolios.equal_weight.metrics.max_drawdown}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Optimal */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-blue-500">
                <h3 className="font-bold text-blue-700 mb-1">
                  ⭐ Optimal Portfolio
                </h3>
                <p className="text-gray-400 text-sm mb-4">
                  MPT optimized
                </p>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Return</span>
                    <span className={`font-bold ${getMetricColor(result.portfolios.optimal.metrics.expected_return, true)}`}>
                      {result.portfolios.optimal.metrics.expected_return}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Volatility</span>
                    <span className="font-bold text-orange-600">
                      {result.portfolios.optimal.metrics.volatility}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Sharpe Ratio</span>
                    <span className="font-bold text-blue-600">
                      {result.portfolios.optimal.metrics.sharpe_ratio}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Drawdown</span>
                    <span className="font-bold text-red-600">
                      {result.portfolios.optimal.metrics.max_drawdown}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Bias Adjusted */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-green-500">
                <h3 className="font-bold text-green-700 mb-1">
                  🧠 Bias Adjusted
                </h3>
                <p className="text-gray-400 text-sm mb-4">
                  Personalized for you
                </p>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Return</span>
                    <span className={`font-bold ${getMetricColor(result.portfolios.bias_adjusted.metrics.expected_return, true)}`}>
                      {result.portfolios.bias_adjusted.metrics.expected_return}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Volatility</span>
                    <span className="font-bold text-orange-600">
                      {result.portfolios.bias_adjusted.metrics.volatility}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Sharpe Ratio</span>
                    <span className="font-bold text-blue-600">
                      {result.portfolios.bias_adjusted.metrics.sharpe_ratio}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Drawdown</span>
                    <span className="font-bold text-red-600">
                      {result.portfolios.bias_adjusted.metrics.max_drawdown}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Allocation */}
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">
                🥧 Portfolio Allocation
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Optimal Allocation */}
                <div>
                  <h3 className="font-bold text-blue-700 mb-3">
                    ⭐ Optimal Allocation
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(result.portfolios.optimal.allocation).map(
                      ([symbol, weight]) => (
                        <div key={symbol}>
                          <div className="flex justify-between mb-1">
                            <span className="font-medium text-gray-700">
                              {symbol}
                            </span>
                            <span className="font-bold text-blue-600">
                              {weight}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-100 rounded-full h-3">
                            <div
                              className="h-3 rounded-full bg-blue-500"
                              style={{ width: `${weight}%` }}
                            ></div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>

                {/* Bias Adjusted Allocation */}
                <div>
                  <h3 className="font-bold text-green-700 mb-3">
                    🧠 Bias Adjusted Allocation
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(
                      result.portfolios.bias_adjusted.allocation
                    ).map(([symbol, weight]) => (
                      <div key={symbol}>
                        <div className="flex justify-between mb-1">
                          <span className="font-medium text-gray-700">
                            {symbol}
                          </span>
                          <span className="font-bold text-green-600">
                            {weight}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-100 rounded-full h-3">
                          <div
                            className="h-3 rounded-full bg-green-500"
                            style={{ width: `${weight}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Monte Carlo */}
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
              <h2 className="text-xl font-bold text-gray-800 mb-2">
                🎲 Monte Carlo Simulation
              </h2>
              <p className="text-gray-500 text-sm mb-6">
                1000 simulations of possible portfolio outcomes over 1 year
              </p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-green-50 rounded-xl">
                  <div className="text-2xl font-bold text-green-600">
                    {formatCurrency(result.monte_carlo.best_case)}
                  </div>
                  <div className="text-green-700 text-sm font-medium mt-1">
                    Best Case (95th)
                  </div>
                </div>

                <div className="text-center p-4 bg-blue-50 rounded-xl">
                  <div className="text-2xl font-bold text-blue-600">
                    {formatCurrency(result.monte_carlo.median_case)}
                  </div>
                  <div className="text-blue-700 text-sm font-medium mt-1">
                    Median Case
                  </div>
                </div>

                <div className="text-center p-4 bg-red-50 rounded-xl">
                  <div className="text-2xl font-bold text-red-600">
                    {formatCurrency(result.monte_carlo.worst_case)}
                  </div>
                  <div className="text-red-700 text-sm font-medium mt-1">
                    Worst Case (5th)
                  </div>
                </div>

                <div className="text-center p-4 bg-purple-50 rounded-xl">
                  <div className="text-2xl font-bold text-purple-600">
                    {result.monte_carlo.probability_of_profit}%
                  </div>
                  <div className="text-purple-700 text-sm font-medium mt-1">
                    Profit Probability
                  </div>
                </div>
              </div>

              <div className="mt-4 p-4 bg-gray-50 rounded-xl">
                <p className="text-gray-600 text-sm">
                  💡 Starting with{" "}
                  {formatCurrency(result.monte_carlo.initial_value)},
                  there is a{" "}
                  <span className="font-bold text-green-600">
                    {result.monte_carlo.probability_of_profit}%
                  </span>{" "}
                  chance of making a profit over the next year.
                  In the worst case scenario, you could lose{" "}
                  <span className="font-bold text-red-600">
                    {formatCurrency(Math.abs(result.monte_carlo.var_95))}
                  </span>.
                </p>
              </div>
            </div>

            {/* Improvement Summary */}
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">
                📊 Optimization Improvement
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-xl">
                  <div className={`text-3xl font-bold ${result.improvement.sharpe_improvement >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {result.improvement.sharpe_improvement >= 0 ? '+' : ''}
                    {result.improvement.sharpe_improvement}
                  </div>
                  <div className="text-blue-700 text-sm font-medium mt-1">
                    Sharpe Ratio Improvement
                  </div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-xl">
                  <div className={`text-3xl font-bold ${result.improvement.return_improvement >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {result.improvement.return_improvement >= 0 ? '+' : ''}
                    {result.improvement.return_improvement}%
                  </div>
                  <div className="text-green-700 text-sm font-medium mt-1">
                    Return Improvement
                  </div>
                </div>
              </div>
            </div>

            {/* Navigation */}
            <div className="flex gap-4">
              
                href="/dashboard"
                className="flex-1 text-center bg-blue-900 text-white py-3 rounded-xl font-semibold hover:bg-blue-800 transition"
              <a>
                🧠 View Bias Dashboard
              </a>
              <button
                onClick={optimizePortfolio}
                className="flex-1 bg-green-600 text-white py-3 rounded-xl font-semibold hover:bg-green-700 transition"
              >
                🔄 Re-optimize
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
