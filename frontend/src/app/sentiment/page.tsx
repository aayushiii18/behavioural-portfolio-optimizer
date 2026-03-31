"use client";
import { useState, useEffect } from "react";
import axios from "axios";

export default function SentimentPage() {
  const [marketSentiment, setMarketSentiment] = useState<any>(null);
  const [stockSentiment, setStockSentiment] = useState<any>(null);
  const [symbol, setSymbol] = useState("AAPL");
  const [loading, setLoading] = useState(true);
  const [stockLoading, setStockLoading] = useState(false);

  useEffect(() => {
    fetchMarketSentiment();
  }, []);

  const fetchMarketSentiment = async () => {
    try {
      setLoading(true);
      const res = await axios.get(
        "http://localhost:8000/sentiment/market"
      );
      setMarketSentiment(res.data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStockSentiment = async () => {
    try {
      setStockLoading(true);
      const res = await axios.get(
        `http://localhost:8000/sentiment/stock/${symbol}`
      );
      setStockSentiment(res.data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setStockLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    if (sentiment === "POSITIVE") return "text-green-600 bg-green-50";
    if (sentiment === "NEGATIVE") return "text-red-600 bg-red-50";
    return "text-gray-600 bg-gray-50";
  };

  const getSentimentEmoji = (sentiment: string) => {
    if (sentiment === "POSITIVE") return "📈";
    if (sentiment === "NEGATIVE") return "📉";
    return "➡️";
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
          <h1 className="text-3xl font-bold">
            📰 Market Sentiment Analysis
          </h1>
          <p className="text-blue-200 mt-1">
            NLP-powered analysis of market news
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Market Sentiment */}
        {marketSentiment && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              🌍 Overall Market Sentiment
            </h2>
            <div className="flex items-center gap-6 flex-wrap">
              <div className={`text-center p-6 rounded-2xl ${getSentimentColor(marketSentiment.overall_sentiment)}`}>
                <div className="text-5xl mb-2">
                  {getSentimentEmoji(marketSentiment.overall_sentiment)}
                </div>
                <div className="text-2xl font-bold">
                  {marketSentiment.overall_sentiment}
                </div>
                <div className="text-sm mt-1">
                  Score: {marketSentiment.avg_compound_score}
                </div>
              </div>
              <div className="flex-1 grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-green-50 rounded-xl">
                  <div className="text-2xl font-bold text-green-600">
                    {marketSentiment.positive_count}
                  </div>
                  <div className="text-green-700 text-sm">
                    Positive News
                  </div>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-xl">
                  <div className="text-2xl font-bold text-red-600">
                    {marketSentiment.negative_count}
                  </div>
                  <div className="text-red-700 text-sm">
                    Negative News
                  </div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-xl">
                  <div className="text-2xl font-bold text-gray-600">
                    {marketSentiment.neutral_count}
                  </div>
                  <div className="text-gray-700 text-sm">
                    Neutral News
                  </div>
                </div>
              </div>
            </div>

            {/* Individual Headlines */}
            {marketSentiment.individual_results && (
              <div className="mt-6">
                <h3 className="font-bold text-gray-700 mb-3">
                  📋 News Analysis
                </h3>
                <div className="space-y-2">
                  {marketSentiment.individual_results.map(
                    (item: any, index: number) => (
                      <div
                        key={index}
                        className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
                      >
                        <span className="text-xl">
                          {getSentimentEmoji(item.sentiment)}
                        </span>
                        <span className="flex-1 text-gray-700 text-sm">
                          {item.text}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(item.sentiment)}`}>
                          {item.compound_score}
                        </span>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Stock Sentiment */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            🔍 Stock Sentiment Analyzer
          </h2>
          <div className="flex gap-3 mb-6">
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3"
              placeholder="Enter stock symbol (e.g. AAPL)"
            />
            <button
              onClick={fetchStockSentiment}
              disabled={stockLoading}
              className="bg-blue-900 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-800 transition disabled:opacity-50"
            >
              {stockLoading ? "Analyzing..." : "Analyze"}
            </button>
          </div>

          {stockSentiment && (
            <div>
              <div className="flex items-center gap-4 mb-4">
                <div className={`px-4 py-2 rounded-xl font-bold ${getSentimentColor(stockSentiment.overall_sentiment)}`}>
                  {getSentimentEmoji(stockSentiment.overall_sentiment)}{" "}
                  {stockSentiment.overall_sentiment}
                </div>
                <div className="text-gray-500 text-sm">
                  Score: {stockSentiment.sentiment_score} |
                  {stockSentiment.headlines_analyzed} headlines analyzed
                </div>
              </div>

              {stockSentiment.headlines && (
                <div className="space-y-2">
                  {stockSentiment.headlines.map(
                    (headline: string, index: number) => (
                      <div
                        key={index}
                        className="p-3 bg-gray-50 rounded-lg text-gray-700 text-sm"
                      >
                        📰 {headline}
                      </div>
                    )
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
