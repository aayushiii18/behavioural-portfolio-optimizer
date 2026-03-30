"use client";
import { useState, useEffect } from "react";
import axios from "axios";

// Types
interface BiasScore {
  score: number;
  level: string;
  description: string;
  nudge: string;
}

interface BiasData {
  biases: {
    overconfidence: BiasScore;
    loss_aversion: BiasScore;
    recency_bias: BiasScore;
    herd_mentality: BiasScore;
    anchoring: BiasScore;
    fomo: BiasScore;
    disposition_effect: BiasScore;
    confirmation_bias: BiasScore;
  };
  overall_score: number;
  overall_level: string;
  dominant_bias: string;
}

interface MLPrediction {
  predicted_bias: string;
  confidence_score: number;
  nudges: Array<{
    type: string;
    message: string;
    action: string;
  }>;
}

export default function Dashboard() {
  const [biasData, setBiasData] = useState<BiasData | null>(null);
  const [mlPrediction, setMLPrediction] = useState<MLPrediction | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch bias analysis
      const biasResponse = await axios.get(
        "http://localhost:8000/bias/analyze/user123"
      );
      setBiasData(biasResponse.data);

      // Fetch ML prediction
      const mlResponse = await axios.get(
        "http://localhost:8000/ml/predict/user123"
      );
      setMLPrediction(mlResponse.data.ml_prediction);

    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  // Color based on score
  const getScoreColor = (score: number) => {
    if (score >= 75) return "bg-red-500";
    if (score >= 50) return "bg-yellow-500";
    if (score >= 25) return "bg-blue-500";
    return "bg-green-500";
  };

  const getScoreTextColor = (score: number) => {
    if (score >= 75) return "text-red-600";
    if (score >= 50) return "text-yellow-600";
    if (score >= 25) return "text-blue-600";
    return "text-green-600";
  };

  const getBiasEmoji = (bias: string) => {
    const emojis: { [key: string]: string } = {
      overconfidence: "🦁",
      loss_aversion: "😰",
      recency_bias: "📅",
      herd_mentality: "🐑",
      anchoring: "⚓",
      fomo: "😱",
      disposition_effect: "🎭",
      confirmation_bias: "🔍"
    };
    return emojis[bias] || "📊";
  };

  const formatBiasName = (bias: string) => {
    return bias.split("_").map(
      word => word.charAt(0).toUpperCase() + word.slice(1)
    ).join(" ");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-900 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Analyzing your portfolio...</p>
          <p className="text-gray-400 text-sm mt-2">Running ML bias detection</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-900 text-white p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold">
            🧠 Behavioural Portfolio Optimizer
          </h1>
          <p className="text-blue-200 mt-1">
            Your personalized bias analysis and portfolio insights
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Overall Score Card */}
        {biasData && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-800">
                  Overall Bias Score
                </h2>
                <p className="text-gray-500">
                  Based on your trading history analysis
                </p>
              </div>
              <div className="text-center">
                <div className={`text-6xl font-bold ${getScoreTextColor(biasData.overall_score)}`}>
                  {biasData.overall_score}
                </div>
                <div className="text-gray-500 text-sm">out of 100</div>
                <div className={`mt-2 px-4 py-1 rounded-full text-white text-sm font-medium ${getScoreColor(biasData.overall_score)}`}>
                  {biasData.overall_level} Bias
                </div>
              </div>
            </div>

            {/* Overall Progress Bar */}
            <div className="mt-6">
              <div className="flex justify-between text-sm text-gray-500 mb-2">
                <span>Minimal</span>
                <span>Low</span>
                <span>Medium</span>
                <span>High</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className={`h-4 rounded-full transition-all duration-1000 ${getScoreColor(biasData.overall_score)}`}
                  style={{ width: `${biasData.overall_score}%` }}
                ></div>
              </div>
            </div>

            {/* Dominant Bias */}
            <div className="mt-4 p-4 bg-blue-50 rounded-xl">
              <p className="text-blue-800 font-medium">
                {getBiasEmoji(biasData.dominant_bias)} Your dominant bias is{" "}
                <span className="font-bold">
                  {formatBiasName(biasData.dominant_bias)}
                </span>
              </p>
            </div>
          </div>
        )}

        {/* ML Prediction Card */}
        {mlPrediction && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              🤖 ML Model Prediction
            </h2>
            <div className="flex items-center gap-6 flex-wrap">
              <div className="text-center p-4 bg-purple-50 rounded-xl">
                <div className="text-3xl mb-2">
                  {getBiasEmoji(mlPrediction.predicted_bias)}
                </div>
                <div className="font-bold text-purple-800 text-lg">
                  {formatBiasName(mlPrediction.predicted_bias)}
                </div>
                <div className="text-purple-600 text-sm">
                  Primary Bias
                </div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-xl">
                <div className="text-3xl font-bold text-green-600">
                  {mlPrediction.confidence_score}%
                </div>
                <div className="text-green-700 text-sm font-medium">
                  Confidence Score
                </div>
              </div>
            </div>

            {/* Nudges */}
            <div className="mt-6">
              <h3 className="font-bold text-gray-700 mb-3">
                💡 Personalized Recommendations
              </h3>
              <div className="space-y-3">
                {mlPrediction.nudges.map((nudge, index) => (
                  <div
                    key={index}
                    className={`p-4 rounded-xl border-l-4 ${
                      nudge.type === "warning"
                        ? "bg-red-50 border-red-400"
                        : nudge.type === "success"
                        ? "bg-green-50 border-green-400"
                        : "bg-blue-50 border-blue-400"
                    }`}
                  >
                    <p className="font-medium text-gray-800">
                      {nudge.message}
                    </p>
                    <p className="text-gray-600 text-sm mt-1">
                      👉 {nudge.action}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Individual Bias Scores */}
        {biasData && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-6">
              📊 Individual Bias Analysis
            </h2>
            <div className="space-y-5">
              {Object.entries(biasData.biases).map(([bias, data]) => (
                <div key={bias}>
                  <div className="flex justify-between items-center mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xl">
                        {getBiasEmoji(bias)}
                      </span>
                      <span className="font-medium text-gray-700">
                        {formatBiasName(bias)}
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`text-sm font-medium ${getScoreTextColor(data.score)}`}>
                        {data.level}
                      </span>
                      <span className={`font-bold text-lg ${getScoreTextColor(data.score)}`}>
                        {data.score}/100
                      </span>
                    </div>
                  </div>
                  {/* Progress Bar */}
                  <div className="w-full bg-gray-100 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-1000 ${getScoreColor(data.score)}`}
                      style={{ width: `${data.score}%` }}
                    ></div>
                  </div>
                  {/* Description */}
                  <p className="text-gray-500 text-sm mt-1">
                    {data.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Refresh Button */}
        <div className="text-center">
          <button
            onClick={fetchData}
            className="bg-blue-900 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-800 transition"
          >
            🔄 Refresh Analysis
          </button>
        </div>
      </div>
    </div>
  );
}