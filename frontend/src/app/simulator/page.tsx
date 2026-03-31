"use client";
import { useState } from "react";
import axios from "axios";

export default function SimulatorPage() {
  const [symbols, setSymbols] = useState("AAPL,GOOGL,MSFT");
  const [biasType, setBiasType] = useState("loss_averse");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runSimulation = async () => {
    setLoading(true);
    try {
      const [biasedRes, rationalRes] = await Promise.all([
        axios.get("http://localhost:8000/portfolio/optimize", {
          params: { symbols, user_bias: biasType, method: "max_sharpe" }
        }),
        axios.get("http://localhost:8000/portfolio/optimize", {
          params: { symbols, user_bias: "rational", method: "max_sharpe" }
        })
      ]);

      setResult({
        biased: biasedRes.data,
        rational: rationalRes.data
      });
    } catch (error) {
      console.error("Error:", error);
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

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-blue-900 text-white p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold">🔮 What-If Simulator</h1>
          <p className="text-blue-200 mt-1">
            See how bias-free decisions would improve your returns
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Simulator Controls */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            ⚙️ Simulation Settings
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Stock Symbols
              </label>
              <input
                type="text"
                value={symbols}
                onChange={(e) => setSymbols(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3"
                placeholder="AAPL,GOOGL,MSFT"
              />
            </div>
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Your Bias Type
              </label>
              <select
                value={biasType}
                onChange={(e) => setBiasType(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3"
              >
                <option value="overconfident">Overconfident</option>
                <option value="loss_averse">Loss Averse</option>
                <option value="fomo">FOMO</option>
                <option value="herd_mentality">Herd Mentality</option>
              </select>
            </div>
          </div>
          <button
            onClick={runSimulation}
            disabled={loading}
            className="mt-4 w-full bg-blue-900 text-white py-3 rounded-xl font-semibold hover:bg-blue-800 transition disabled:opacity-50"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Running simulation...
              </span>
            ) : (
              "🔮 Run What-If Simulation"
            )}
          </button>
        </div>

        {/* Results */}
        {result && (
          <>
            {/* Comparison Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              {/* Biased Portfolio */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-red-200">
                <h3 className="text-xl font-bold text-red-700 mb-4">
                  😰 With Your {biasType.replace(/_/g, " ")} Bias
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Expected Return</span>
                    <span className="font-bold text-red-600">
                      {result.biased.portfolios?.bias_adjusted?.metrics?.expected_return}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Volatility</span>
                    <span className="font-bold text-orange-600">
                      {result.biased.portfolios?.bias_adjusted?.metrics?.volatility}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Sharpe Ratio</span>
                    <span className="font-bold text-gray-700">
                      {result.biased.portfolios?.bias_adjusted?.metrics?.sharpe_ratio}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Drawdown</span>
                    <span className="font-bold text-red-600">
                      {result.biased.portfolios?.bias_adjusted?.metrics?.max_drawdown}%
                    </span>
                  </div>
                </div>

                {/* Monte Carlo */}
                <div className="mt-4 p-4 bg-red-50 rounded-xl">
                  <p className="text-red-700 font-medium text-sm">
                    📊 1 Year Projection (₹1,00,000)
                  </p>
                  <div className="mt-2 space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Best Case</span>
                      <span className="text-green-600 font-medium">
                        {formatCurrency(result.biased.monte_carlo?.best_case)}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Median</span>
                      <span className="text-blue-600 font-medium">
                        {formatCurrency(result.biased.monte_carlo?.median_case)}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Worst Case</span>
                      <span className="text-red-600 font-medium">
                        {formatCurrency(result.biased.monte_carlo?.worst_case)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Rational Portfolio */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-green-200">
                <h3 className="text-xl font-bold text-green-700 mb-4">
                  😊 Without Bias (Rational)
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Expected Return</span>
                    <span className="font-bold text-green-600">
                      {result.rational.portfolios?.bias_adjusted?.metrics?.expected_return}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Volatility</span>
                    <span className="font-bold text-orange-600">
                      {result.rational.portfolios?.bias_adjusted?.metrics?.volatility}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Sharpe Ratio</span>
                    <span className="font-bold text-gray-700">
                      {result.rational.portfolios?.bias_adjusted?.metrics?.sharpe_ratio}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Max Drawdown</span>
                    <span className="font-bold text-red-600">
                      {result.rational.portfolios?.bias_adjusted?.metrics?.max_drawdown}%
                    </span>
                  </div>
                </div>

                {/* Monte Carlo */}
                <div className="mt-4 p-4 bg-green-50 rounded-xl">
                  <p className="text-green-700 font-medium text-sm">
                    📊 1 Year Projection (₹1,00,000)
                  </p>
                  <div className="mt-2 space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Best Case</span>
                      <span className="text-green-600 font-medium">
                        {formatCurrency(result.rational.monte_carlo?.best_case)}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Median</span>
                      <span className="text-blue-600 font-medium">
                        {formatCurrency(result.rational.monte_carlo?.median_case)}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Worst Case</span>
                      <span className="text-red-600 font-medium">
                        {formatCurrency(result.rational.monte_carlo?.worst_case)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Impact Summary */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">
                💡 Bias Impact Summary
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-xl">
                  <div className="text-3xl font-bold text-blue-600">
                    {(
                      (result.rational.portfolios?.bias_adjusted?.metrics?.expected_return || 0) -
                      (result.biased.portfolios?.bias_adjusted?.metrics?.expected_return || 0)
                    ).toFixed(2)}%
                  </div>
                  <div className="text-blue-700 text-sm mt-1">
                    Return Difference
                  </div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-xl">
                  <div className="text-3xl font-bold text-green-600">
                    {formatCurrency(
                      (result.rational.monte_carlo?.median_case || 0) -
                      (result.biased.monte_carlo?.median_case || 0)
                    )}
                  </div>
                  <div className="text-green-700 text-sm mt-1">
                    Extra Money (Median)
                  </div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-xl">
                  <div className="text-3xl font-bold text-purple-600">
                    {(
                      (result.rational.portfolios?.bias_adjusted?.metrics?.sharpe_ratio || 0) -
                      (result.biased.portfolios?.bias_adjusted?.metrics?.sharpe_ratio || 0)
                    ).toFixed(3)}
                  </div>
                  <div className="text-purple-700 text-sm mt-1">
                    Sharpe Improvement
                  </div>
                </div>
              </div>

              <div className="mt-4 p-4 bg-yellow-50 rounded-xl border border-yellow-200">
                <p className="text-yellow-800 font-medium">
                  💰 By reducing your {biasType.replace(/_/g, " ")} bias,
                  you could potentially earn{" "}
                  <span className="font-bold text-green-600">
                    {formatCurrency(
                      Math.abs(
                        (result.rational.monte_carlo?.median_case || 0) -
                        (result.biased.monte_carlo?.median_case || 0)
                      )
                    )}
                  </span>{" "}
                  more over the next year on a ₹1,00,000 investment!
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}