"use client";
import { useState, useEffect } from "react";
import axios from "axios";

export default function JournalPage() {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [txnRes, analysisRes] = await Promise.all([
        axios.get("http://localhost:8000/transactions/mock/user123"),
        axios.get("http://localhost:8000/transactions/analyze/user123")
      ]);
      setTransactions(txnRes.data.transactions || []);
      setAnalysis(analysisRes.data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredTransactions = transactions.filter(t => {
    if (filter === "all") return true;
    if (filter === "buy") return t.action === "BUY";
    if (filter === "sell") return t.action === "SELL";
    if (filter === "bull") return t.market_condition === "bull";
    if (filter === "bear") return t.market_condition === "bear";
    return true;
  });

  const getBiasTag = (txn: any) => {
    if (txn.action === "SELL" && txn.market_condition === "bear") {
      return { label: "Panic Sell", color: "bg-red-100 text-red-700" };
    }
    if (txn.action === "BUY" && txn.market_condition === "bull" && txn.quantity > 8) {
      return { label: "FOMO Buy", color: "bg-orange-100 text-orange-700" };
    }
    if (txn.quantity > 15) {
      return { label: "Overconfident", color: "bg-yellow-100 text-yellow-700" };
    }
    return { label: "Rational", color: "bg-green-100 text-green-700" };
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-900"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-blue-900 text-white p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold">📓 Trade Journal</h1>
          <p className="text-blue-200 mt-1">
            Your complete trading history with bias analysis
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Analysis Summary */}
        {analysis && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-2xl shadow p-4 text-center">
              <div className="text-3xl font-bold text-blue-600">
                {analysis.total_transactions}
              </div>
              <div className="text-gray-500 text-sm">Total Trades</div>
            </div>
            <div className="bg-white rounded-2xl shadow p-4 text-center">
              <div className="text-3xl font-bold text-green-600">
                {analysis.win_loss?.win_rate}%
              </div>
              <div className="text-gray-500 text-sm">Win Rate</div>
            </div>
            <div className="bg-white rounded-2xl shadow p-4 text-center">
              <div className="text-3xl font-bold text-red-600">
                {analysis.panic_selling?.panic_sell_count}
              </div>
              <div className="text-gray-500 text-sm">Panic Sells</div>
            </div>
            <div className="bg-white rounded-2xl shadow p-4 text-center">
              <div className="text-3xl font-bold text-orange-600">
                {analysis.fomo_buying?.fomo_buy_count}
              </div>
              <div className="text-gray-500 text-sm">FOMO Buys</div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex gap-2 mb-4 flex-wrap">
          {["all", "buy", "sell", "bull", "bear"].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg font-medium capitalize transition ${
                filter === f
                  ? "bg-blue-900 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-100"
              }`}
            >
              {f === "all" ? "All Trades" :
               f === "buy" ? "🟢 Buys" :
               f === "sell" ? "🔴 Sells" :
               f === "bull" ? "📈 Bull Market" :
               "📉 Bear Market"}
            </button>
          ))}
        </div>

        {/* Transactions Table */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="text-left p-4 text-gray-600 font-medium">Date</th>
                  <th className="text-left p-4 text-gray-600 font-medium">Symbol</th>
                  <th className="text-left p-4 text-gray-600 font-medium">Action</th>
                  <th className="text-left p-4 text-gray-600 font-medium">Qty</th>
                  <th className="text-left p-4 text-gray-600 font-medium">Price</th>
                  <th className="text-left p-4 text-gray-600 font-medium">Value</th>
                  <th className="text-left p-4 text-gray-600 font-medium">Market</th>
                  <th className="text-left p-4 text-gray-600 font-medium">Bias Tag</th>
                </tr>
              </thead>
              <tbody>
                {filteredTransactions.slice(0, 20).map((txn, index) => {
                  const biasTag = getBiasTag(txn);
                  return (
                    <tr
                      key={index}
                      className="border-b hover:bg-gray-50 transition"
                    >
                      <td className="p-4 text-gray-600 text-sm">
                        {new Date(txn.date).toLocaleDateString()}
                      </td>
                      <td className="p-4 font-bold text-gray-800">
                        {txn.symbol}
                      </td>
                      <td className="p-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                          txn.action === "BUY"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}>
                          {txn.action}
                        </span>
                      </td>
                      <td className="p-4 text-gray-700">{txn.quantity}</td>
                      <td className="p-4 text-gray-700">${txn.price}</td>
                      <td className="p-4 font-medium text-gray-800">
                        ${txn.total_value?.toLocaleString()}
                      </td>
                      <td className="p-4">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          txn.market_condition === "bull"
                            ? "bg-green-50 text-green-600"
                            : txn.market_condition === "bear"
                            ? "bg-red-50 text-red-600"
                            : "bg-gray-50 text-gray-600"
                        }`}>
                          {txn.market_condition}
                        </span>
                      </td>
                      <td className="p-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${biasTag.color}`}>
                          {biasTag.label}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <div className="p-4 text-center text-gray-400 text-sm border-t">
            Showing 20 of {filteredTransactions.length} transactions
          </div>
        </div>
      </div>
    </div>
  );
}