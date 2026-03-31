"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import Link from "next/link";

export default function MainDashboard() {
  const [biasData, setBiasData] = useState<any>(null);
  const [mlData, setMlData] = useState<any>(null);
  const [gameData, setGameData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [biasRes, mlRes, gameRes] = await Promise.all([
        axios.get("http://localhost:8000/bias/score/user123"),
        axios.get("http://localhost:8000/ml/predict/user123"),
        axios.get("http://localhost:8000/gamification/user123")
      ]);
      setBiasData(biasRes.data);
      setMlData(mlRes.data);
      setGameData(gameRes.data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const quickLinks = [
    {
      href: "/dashboard",
      icon: "🧠",
      title: "Bias Analysis",
      description: "View your 8 bias scores",
      color: "bg-blue-50 border-blue-200 hover:bg-blue-100"
    },
    {
      href: "/portfolio",
      icon: "📈",
      title: "Portfolio Optimizer",
      description: "Optimize with MPT + bias adjustments",
      color: "bg-green-50 border-green-200 hover:bg-green-100"
    },
    {
      href: "/nudges",
      icon: "🎯",
      title: "Nudges & Rewards",
      description: "View nudges, badges and challenges",
      color: "bg-purple-50 border-purple-200 hover:bg-purple-100"
    },
    {
      href: "/journal",
      icon: "📓",
      title: "Trade Journal",
      description: "Track and analyze your trades",
      color: "bg-yellow-50 border-yellow-200 hover:bg-yellow-100"
    },
    {
      href: "/simulator",
      icon: "🔮",
      title: "What-If Simulator",
      description: "Simulate bias-free decisions",
      color: "bg-red-50 border-red-200 hover:bg-red-100"
    },
    {
      href: "/sentiment",
      icon: "📰",
      title: "Market Sentiment",
      description: "NLP analysis of market news",
      color: "bg-orange-50 border-orange-200 hover:bg-orange-100"
    }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-900 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-900 to-indigo-900 text-white p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold mb-2">
            Welcome back, Aayushi! 👋
          </h1>
          <p className="text-blue-200 text-lg">
            Here's your investment health summary
          </p>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            {biasData && (
              <>
                <div className="bg-white bg-opacity-10 rounded-xl p-4">
                  <div className="text-3xl font-bold">
                    {biasData.overall_score}
                  </div>
                  <div className="text-blue-200 text-sm">
                    Overall Bias Score
                  </div>
                </div>
                <div className="bg-white bg-opacity-10 rounded-xl p-4">
                  <div className="text-3xl font-bold capitalize">
                    {biasData.dominant_bias?.replace(/_/g, " ")}
                  </div>
                  <div className="text-blue-200 text-sm">
                    Dominant Bias
                  </div>
                </div>
              </>
            )}
            {mlData && (
              <div className="bg-white bg-opacity-10 rounded-xl p-4">
                <div className="text-3xl font-bold">
                  {mlData.ml_prediction?.confidence_score}%
                </div>
                <div className="text-blue-200 text-sm">
                  ML Confidence
                </div>
              </div>
            )}
            {gameData && (
              <div className="bg-white bg-opacity-10 rounded-xl p-4">
                <div className="text-3xl font-bold">
                  {gameData.total_points}
                </div>
                <div className="text-blue-200 text-sm">
                  Total Points
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Alert Section */}
        {biasData && biasData.overall_score > 50 && (
          <div className="bg-red-50 border border-red-200 rounded-2xl p-4 mb-6 flex items-center gap-4">
            <span className="text-3xl">⚠️</span>
            <div>
              <h3 className="font-bold text-red-800">
                High Bias Detected!
              </h3>
              <p className="text-red-600 text-sm">
                Your overall bias score is {biasData.overall_score}/100.
                Check your nudges for personalized recommendations.
              </p>
            </div>
            <Link
              href="/nudges"
              className="ml-auto bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-700 transition"
            >
              View Nudges
            </Link>
          </div>
        )}

        {/* Quick Links Grid */}
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          🚀 Quick Access
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {quickLinks.map((link, index) => (
            <Link
              key={index}
              href={link.href}
              className={`p-6 rounded-2xl border-2 transition cursor-pointer ${link.color}`}
            >
              <div className="text-4xl mb-3">{link.icon}</div>
              <h3 className="font-bold text-gray-800 text-lg">
                {link.title}
              </h3>
              <p className="text-gray-500 text-sm mt-1">
                {link.description}
              </p>
            </Link>
          ))}
        </div>

        {/* Bias Score Summary */}
        {biasData && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              📊 Bias Score Summary
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(biasData.bias_scores || {}).map(
                ([bias, score]: [string, any]) => (
                  <div
                    key={bias}
                    className="text-center p-3 bg-gray-50 rounded-xl"
                  >
                    <div className={`text-2xl font-bold ${
                      score >= 75 ? "text-red-600" :
                      score >= 50 ? "text-yellow-600" :
                      score >= 25 ? "text-blue-600" :
                      "text-green-600"
                    }`}>
                      {score}
                    </div>
                    <div className="text-gray-500 text-xs mt-1 capitalize">
                      {bias.replace(/_/g, " ")}
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                      <div
                        className={`h-1.5 rounded-full ${
                          score >= 75 ? "bg-red-500" :
                          score >= 50 ? "bg-yellow-500" :
                          score >= 25 ? "bg-blue-500" :
                          "bg-green-500"
                        }`}
                        style={{ width: `${score}%` }}
                      ></div>
                    </div>
                  </div>
                )
              )}
            </div>
          </div>
        )}

        {/* ML Prediction Card */}
        {mlData && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              🤖 ML Prediction
            </h2>
            <div className="flex items-center gap-6 flex-wrap">
              <div className="text-center p-4 bg-purple-50 rounded-xl">
                <div className="text-3xl mb-2">🎯</div>
                <div className="font-bold text-purple-800 capitalize">
                  {mlData.ml_prediction?.predicted_bias?.replace(/_/g, " ")}
                </div>
                <div className="text-purple-600 text-sm">Primary Bias</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-xl">
                <div className="text-3xl font-bold text-green-600">
                  {mlData.ml_prediction?.confidence_score}%
                </div>
                <div className="text-green-700 text-sm">Confidence</div>
              </div>
              <div className="flex-1">
                {mlData.ml_prediction?.nudges?.slice(0, 1).map(
                  (nudge: any, i: number) => (
                    <div
                      key={i}
                      className="p-4 bg-blue-50 rounded-xl border-l-4 border-blue-400"
                    >
                      <p className="text-gray-800 font-medium">
                        {nudge.message}
                      </p>
                      <p className="text-gray-500 text-sm mt-1">
                        👉 {nudge.action}
                      </p>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        )}

        {/* Level Progress */}
        {gameData && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              🏆 Your Progress
            </h2>
            <div className="flex items-center justify-between mb-3">
              <span className="font-medium text-gray-700">
                {gameData.current_level?.name}
              </span>
              <span className="text-blue-600 font-bold">
                {gameData.total_points} pts
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className="h-4 rounded-full bg-blue-600 transition-all"
                style={{
                  width: `${Math.min(100,
                    ((gameData.total_points - (gameData.current_level?.min_points || 0)) /
                    ((gameData.next_level?.min_points || 1000) - (gameData.current_level?.min_points || 0))) * 100
                  )}%`
                }}
              ></div>
            </div>
            <p className="text-gray-500 text-sm mt-2">
              {gameData.points_to_next_level} points to{" "}
              {gameData.next_level?.name}
            </p>

            {/* Badges Preview */}
            <div className="flex gap-2 mt-4 flex-wrap">
              {gameData.earned_badges?.map((badge: any, i: number) => (
                <div
                  key={i}
                  className="px-3 py-1 bg-yellow-50 border border-yellow-200 rounded-full text-sm"
                >
                  {badge.name}
                </div>
              ))}
              {gameData.earned_badges?.length === 0 && (
                <p className="text-gray-400 text-sm">
                  No badges yet. Keep trading wisely!
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}