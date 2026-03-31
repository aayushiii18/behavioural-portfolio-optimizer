"use client";
import { useState, useEffect } from "react";
import axios from "axios";

interface Nudge {
  nudge_id: string;
  type: string;
  title: string;
  message: string;
  action: string;
  cooling_off: boolean;
  cooling_off_hours: number;
  educational_tip: string;
  severity: string;
  bias_type: string;
  bias_score: number;
}

interface Badge {
  id: string;
  name: string;
  description: string;
  points: number;
  rarity: string;
}

interface Level {
  level: number;
  name: string;
  min_points: number;
  perks: string[];
}

interface GameStats {
  user_id: string;
  total_points: number;
  current_level: Level;
  next_level: Level;
  points_to_next_level: number;
  earned_badges: Badge[];
  available_badges: Badge[];
  stats: {
    total_trades: number;
    unique_stocks: number;
    bias_score: number;
    bias_level: string;
  };
}

interface Challenge {
  id: string;
  title: string;
  description: string;
  points: number;
  duration: string;
  date: string;
}

export default function NudgesPage() {
  const [nudges, setNudges] = useState<Nudge[]>([]);
  const [gameStats, setGameStats] = useState<GameStats | null>(null);
  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("nudges");

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);

      // Fetch nudges
      const nudgesRes = await axios.get(
        "http://localhost:8000/nudges/user123"
      );
      setNudges(nudgesRes.data.nudges.nudges || []);

      // Fetch gamification stats
      const gameRes = await axios.get(
        "http://localhost:8000/gamification/user123"
      );
      setGameStats(gameRes.data);

      // Fetch daily challenge
      const challengeRes = await axios.get(
        "http://localhost:8000/gamification/challenge/daily"
      );
      setChallenge(challengeRes.data);

      // Fetch leaderboard
      const leaderRes = await axios.get(
        "http://localhost:8000/gamification/leaderboard"
      );
      setLeaderboard(leaderRes.data.leaderboard || []);

    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const getNudgeColor = (severity: string) => {
    switch (severity) {
      case "high": return "border-red-400 bg-red-50";
      case "medium": return "border-yellow-400 bg-yellow-50";
      default: return "border-green-400 bg-green-50";
    }
  };

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case "legendary": return "text-yellow-600 bg-yellow-50";
      case "epic": return "text-purple-600 bg-purple-50";
      case "rare": return "text-blue-600 bg-blue-50";
      default: return "text-gray-600 bg-gray-50";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-900 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading your nudges...</p>
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
            🎯 Nudge & Rewards Center
          </h1>
          <p className="text-blue-200 mt-1">
            Personalized guidance to improve your investment decisions
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Tabs */}
        <div className="flex gap-2 mb-6 bg-white rounded-xl p-2 shadow">
          {[
            { id: "nudges", label: "🔔 Nudges" },
            { id: "badges", label: "🏆 Badges" },
            { id: "challenge", label: "🎯 Challenge" },
            { id: "leaderboard", label: "📊 Leaderboard" }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 py-2 px-4 rounded-lg font-medium transition ${
                activeTab === tab.id
                  ? "bg-blue-900 text-white"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Points & Level Card - Always visible */}
        {gameStats && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-800">
                  {gameStats.current_level.name}
                </h2>
                <p className="text-gray-500">
                  {gameStats.earned_badges.length} badges earned
                </p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-900">
                  {gameStats.total_points}
                </div>
                <div className="text-gray-500 text-sm">Total Points</div>
              </div>
            </div>

            {/* Level Progress */}
            {gameStats.next_level && (
              <div className="mt-4">
                <div className="flex justify-between text-sm text-gray-500 mb-2">
                  <span>{gameStats.current_level.name}</span>
                  <span>{gameStats.next_level.name}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div
                    className="h-4 rounded-full bg-blue-600 transition-all"
                    style={{
                      width: `${Math.min(
                        100,
                        ((gameStats.total_points - gameStats.current_level.min_points) /
                          (gameStats.next_level.min_points - gameStats.current_level.min_points)) * 100
                      )}%`
                    }}
                  ></div>
                </div>
                <p className="text-gray-500 text-sm mt-2">
                  {gameStats.points_to_next_level} points to next level
                </p>
              </div>
            )}

            {/* Quick Stats */}
            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="text-center p-3 bg-blue-50 rounded-xl">
                <div className="text-2xl font-bold text-blue-600">
                  {gameStats.stats.total_trades}
                </div>
                <div className="text-blue-700 text-xs">Total Trades</div>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-xl">
                <div className="text-2xl font-bold text-green-600">
                  {gameStats.stats.unique_stocks}
                </div>
                <div className="text-green-700 text-xs">Stocks Held</div>
              </div>
              <div className="text-center p-3 bg-purple-50 rounded-xl">
                <div className="text-2xl font-bold text-purple-600">
                  {gameStats.stats.bias_score}
                </div>
                <div className="text-purple-700 text-xs">Bias Score</div>
              </div>
            </div>
          </div>
        )}

        {/* NUDGES TAB */}
        {activeTab === "nudges" && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-gray-800">
              🔔 Your Personalized Nudges
            </h2>
            {nudges.length === 0 ? (
              <div className="bg-white rounded-2xl shadow p-8 text-center">
                <div className="text-5xl mb-4">✅</div>
                <h3 className="text-xl font-bold text-gray-700">
                  No urgent nudges!
                </h3>
                <p className="text-gray-500 mt-2">
                  Your trading behavior looks great!
                </p>
              </div>
            ) : (
              nudges.map((nudge, index) => (
                <div
                  key={index}
                  className={`bg-white rounded-2xl shadow-lg p-6 border-l-4 ${getNudgeColor(nudge.severity)}`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-800">
                        {nudge.title}
                      </h3>
                      <p className="text-gray-600 mt-2">
                        {nudge.message}
                      </p>

                      {/* Action */}
                      <div className="mt-3 p-3 bg-white rounded-lg border border-gray-200">
                        <p className="text-gray-700 font-medium text-sm">
                          👉 Action: {nudge.action}
                        </p>
                      </div>

                      {/* Educational tip */}
                      <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                        <p className="text-blue-700 text-sm">
                          💡 {nudge.educational_tip}
                        </p>
                      </div>

                      {/* Cooling off */}
                      {nudge.cooling_off && (
                        <div className="mt-3 p-3 bg-orange-50 rounded-lg border border-orange-200">
                          <p className="text-orange-700 text-sm font-medium">
                            ⏰ Cooling-off recommended:{" "}
                            {nudge.cooling_off_hours} hours
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Severity Badge */}
                    <div className={`ml-4 px-3 py-1 rounded-full text-xs font-bold ${
                      nudge.severity === "high"
                        ? "bg-red-100 text-red-700"
                        : nudge.severity === "medium"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-green-100 text-green-700"
                    }`}>
                      {nudge.severity.toUpperCase()}
                    </div>
                  </div>

                  {/* Bias info */}
                  <div className="mt-4 flex items-center gap-2">
                    <span className="text-gray-500 text-xs">
                      Bias: {nudge.bias_type?.replace(/_/g, " ")}
                    </span>
                    <span className="text-gray-300">|</span>
                    <span className="text-gray-500 text-xs">
                      Score: {nudge.bias_score}/100
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* BADGES TAB */}
        {activeTab === "badges" && gameStats && (
          <div>
            {/* Earned Badges */}
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              🏆 Earned Badges ({gameStats.earned_badges.length})
            </h2>
            {gameStats.earned_badges.length === 0 ? (
              <div className="bg-white rounded-2xl shadow p-8 text-center mb-6">
                <div className="text-5xl mb-4">🎯</div>
                <h3 className="text-xl font-bold text-gray-700">
                  No badges yet!
                </h3>
                <p className="text-gray-500 mt-2">
                  Keep trading wisely to earn badges!
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {gameStats.earned_badges.map((badge, index) => (
                  <div
                    key={index}
                    className="bg-white rounded-2xl shadow-lg p-6 border-2 border-yellow-300"
                  >
                    <div className="flex items-center gap-4">
                      <div className="text-4xl">{badge.name.split(" ")[0]}</div>
                      <div>
                        <h3 className="font-bold text-gray-800">
                          {badge.name}
                        </h3>
                        <p className="text-gray-500 text-sm">
                          {badge.description}
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          <span className="text-yellow-600 font-bold text-sm">
                            +{badge.points} pts
                          </span>
                          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getRarityColor(badge.rarity)}`}>
                            {badge.rarity}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Available Badges */}
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              🎯 Badges to Earn
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {gameStats.available_badges.map((badge, index) => (
                <div
                  key={index}
                  className="bg-white rounded-2xl shadow p-6 opacity-60"
                >
                  <div className="flex items-center gap-4">
                    <div className="text-4xl grayscale">
                      {badge.name.split(" ")[0]}
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-600">
                        {badge.name}
                      </h3>
                      <p className="text-gray-400 text-sm">
                        {badge.description}
                      </p>
                      <div className="flex items-center gap-2 mt-2">
                        <span className="text-gray-400 font-bold text-sm">
                          +{badge.points} pts
                        </span>
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getRarityColor(badge.rarity)}`}>
                          {badge.rarity}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* CHALLENGE TAB */}
        {activeTab === "challenge" && challenge && (
          <div>
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              🎯 Today's Challenge
            </h2>
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
              <div className="text-6xl mb-4">🏆</div>
              <h3 className="text-2xl font-bold text-gray-800">
                {challenge.title}
              </h3>
              <p className="text-gray-600 mt-3 text-lg">
                {challenge.description}
              </p>
              <div className="mt-6 inline-block bg-yellow-50 px-6 py-3 rounded-xl">
                <span className="text-yellow-600 font-bold text-xl">
                  +{challenge.points} points
                </span>
              </div>
              <div className="mt-4">
                <span className="text-gray-400 text-sm">
                  Duration: {challenge.duration}
                </span>
              </div>
              <button className="mt-6 w-full bg-blue-900 text-white py-3 rounded-xl font-semibold hover:bg-blue-800 transition">
                ✅ Accept Challenge
              </button>
            </div>

            {/* Tips */}
            <div className="mt-6 bg-white rounded-2xl shadow p-6">
              <h3 className="font-bold text-gray-800 mb-4">
                💡 Investment Tips for Today
              </h3>
              <div className="space-y-3">
                {[
                  "Review your portfolio's sector allocation",
                  "Read one financial news article",
                  "Check if any positions need rebalancing",
                  "Review your investment goals"
                ].map((tip, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg"
                  >
                    <span className="text-blue-600 font-bold">
                      {index + 1}.
                    </span>
                    <span className="text-gray-700">{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* LEADERBOARD TAB */}
        {activeTab === "leaderboard" && (
          <div>
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              📊 Top Investors Leaderboard
            </h2>
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              {leaderboard.map((investor, index) => (
                <div
                  key={index}
                  className={`flex items-center gap-4 p-4 border-b border-gray-100 ${
                    index === 0 ? "bg-yellow-50" :
                    index === 1 ? "bg-gray-50" :
                    index === 2 ? "bg-orange-50" : ""
                  }`}
                >
                  <div className="text-2xl font-bold w-8 text-center">
                    {index === 0 ? "🥇" :
                     index === 1 ? "🥈" :
                     index === 2 ? "🥉" :
                     `#${investor.rank}`}
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800">
                      {investor.username}
                    </div>
                    <div className="text-gray-500 text-sm">
                      {investor.level}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-blue-600">
                      {investor.points} pts
                    </div>
                    <div className="text-gray-400 text-sm">
                      {investor.badges} badges
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Your Rank */}
            {gameStats && (
              <div className="mt-4 bg-blue-900 text-white rounded-2xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-bold text-lg">Your Ranking</div>
                    <div className="text-blue-200">
                      {gameStats.current_level.name}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold">
                      {gameStats.total_points}
                    </div>
                    <div className="text-blue-200 text-sm">points</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Navigation */}
        <div className="flex gap-4 mt-6">
          
            href="/dashboard"
            className="flex-1 text-center bg-blue-900 text-white py-3 rounded-xl font-semibold hover:bg-blue-800 transition"
          <a>
            🧠 Bias Dashboard
          </a>
          
            href="/portfolio"
            className="flex-1 text-center bg-green-600 text-white py-3 rounded-xl font-semibold hover:bg-green-700 transition"
          <a>
            📈 Portfolio
          </a>
        </div>
      </div>
    </div>
  );
}
