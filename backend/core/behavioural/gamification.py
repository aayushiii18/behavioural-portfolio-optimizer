from datetime import datetime, timedelta
from typing import List, Dict
import random

class GamificationEngine:
    """
    Gamification System for Behavioural Change
    
    Makes investing improvement fun!
    Uses badges, points and achievements
    to motivate better decisions.
    """
    
    def __init__(self):
        self.badges = self._define_badges()
        self.levels = self._define_levels()
    
    def _define_badges(self) -> Dict:
        """Define all available badges"""
        return {
            "iron_hands": {
                "id": "iron_hands",
                "name": "🏆 Iron Hands",
                "description": "Held position during 10%+ market drop",
                "points": 100,
                "rarity": "rare",
                "criteria": "No panic sells during market drop"
            },
            "zen_investor": {
                "id": "zen_investor",
                "name": "🧘 Zen Investor",
                "description": "No panic sells for 30 days",
                "points": 150,
                "rarity": "epic",
                "criteria": "30 days without panic selling"
            },
            "sharp_shooter": {
                "id": "sharp_shooter",
                "name": "🎯 Sharp Shooter",
                "description": "3 profitable trades in a row",
                "points": 75,
                "rarity": "uncommon",
                "criteria": "3 consecutive profitable trades"
            },
            "wise_owl": {
                "id": "wise_owl",
                "name": "🦉 Wise Owl",
                "description": "Followed all nudges for a week",
                "points": 200,
                "rarity": "epic",
                "criteria": "100% nudge compliance for 7 days"
            },
            "bias_buster": {
                "id": "bias_buster",
                "name": "⭐ Bias Buster",
                "description": "Reduced bias score by 20%",
                "points": 300,
                "rarity": "legendary",
                "criteria": "20% reduction in overall bias score"
            },
            "diversifier": {
                "id": "diversifier",
                "name": "🌈 Diversifier",
                "description": "Portfolio has 8+ different stocks",
                "points": 50,
                "rarity": "common",
                "criteria": "Hold 8 or more different stocks"
            },
            "patient_investor": {
                "id": "patient_investor",
                "name": "⏳ Patient Investor",
                "description": "Held a position for 6+ months",
                "points": 125,
                "rarity": "rare",
                "criteria": "Hold any position for 180+ days"
            },
            "contrarian": {
                "id": "contrarian",
                "name": "🔄 Contrarian",
                "description": "Bought during market fear (VIX > 30)",
                "points": 175,
                "rarity": "epic",
                "criteria": "Buy during high volatility period"
            },
            "first_trade": {
                "id": "first_trade",
                "name": "🌟 First Trade",
                "description": "Made your first trade!",
                "points": 25,
                "rarity": "common",
                "criteria": "Complete first trade"
            },
            "nudge_follower": {
                "id": "nudge_follower",
                "name": "👂 Good Listener",
                "description": "Followed 10 nudges",
                "points": 100,
                "rarity": "uncommon",
                "criteria": "Follow 10 system nudges"
            }
        }
    
    def _define_levels(self) -> List[Dict]:
        """Define investor levels"""
        return [
            {
                "level": 1,
                "name": "🌱 Seedling Investor",
                "min_points": 0,
                "max_points": 100,
                "perks": ["Basic bias detection"]
            },
            {
                "level": 2,
                "name": "🌿 Growing Investor",
                "min_points": 100,
                "max_points": 300,
                "perks": ["Advanced nudges", "Weekly reports"]
            },
            {
                "level": 3,
                "name": "🌳 Established Investor",
                "min_points": 300,
                "max_points": 600,
                "perks": ["Portfolio optimization", "Sentiment analysis"]
            },
            {
                "level": 4,
                "name": "💎 Diamond Investor",
                "min_points": 600,
                "max_points": 1000,
                "perks": ["AI predictions", "Custom strategies"]
            },
            {
                "level": 5,
                "name": "🏆 Master Investor",
                "min_points": 1000,
                "max_points": float('inf'),
                "perks": ["All features", "Priority support"]
            }
        ]
    
    def calculate_user_stats(
        self,
        user_id: str,
        transactions: List[Dict],
        bias_scores: Dict
    ) -> Dict:
        """
        Calculate user's gamification stats
        Points, badges, level
        """
        points = 0
        earned_badges = []
        
        # Points for trading activity
        total_trades = len(transactions)
        points += min(total_trades * 2, 100)
        
        # Points for low bias scores
        overall_bias = bias_scores.get("overall_score", 50)
        if overall_bias < 30:
            points += 150  # Low bias = lots of points!
        elif overall_bias < 50:
            points += 75
        elif overall_bias < 70:
            points += 25
        
        # Check badge criteria
        # Badge 1: First Trade
        if total_trades >= 1:
            earned_badges.append(self.badges["first_trade"])
            points += self.badges["first_trade"]["points"]
        
        # Badge 2: Diversifier
        symbols = set(t['symbol'] for t in transactions)
        if len(symbols) >= 8:
            earned_badges.append(self.badges["diversifier"])
            points += self.badges["diversifier"]["points"]
        
        # Badge 3: Bias Buster
        if overall_bias < 25:
            earned_badges.append(self.badges["bias_buster"])
            points += self.badges["bias_buster"]["points"]
        
        # Badge 4: Iron Hands
        panic_score = bias_scores.get(
            "biases", {}
        ).get(
            "loss_aversion", {}
        ).get("score", 100)
        
        if panic_score < 30:
            earned_badges.append(self.badges["iron_hands"])
            points += self.badges["iron_hands"]["points"]
        
        # Badge 5: Sharp Shooter
        wins = sum(
            1 for t in transactions
            if t.get('action') == 'SELL' and
            t.get('price', 0) > t.get('buy_price', 0)
        )
        if wins >= 3:
            earned_badges.append(self.badges["sharp_shooter"])
            points += self.badges["sharp_shooter"]["points"]
        
        # Calculate level
        current_level = self._calculate_level(points)
        next_level = self._get_next_level(points)
        
        # Points to next level
        points_to_next = (
            next_level["min_points"] - points
            if next_level else 0
        )
        
        # Available badges not yet earned
        earned_ids = [b["id"] for b in earned_badges]
        available_badges = [
            b for b_id, b in self.badges.items()
            if b_id not in earned_ids
        ]
        
        return {
            "user_id": user_id,
            "total_points": points,
            "current_level": current_level,
            "next_level": next_level,
            "points_to_next_level": points_to_next,
            "earned_badges": earned_badges,
            "badges_count": len(earned_badges),
            "available_badges": available_badges[:5],
            "stats": {
                "total_trades": total_trades,
                "unique_stocks": len(symbols),
                "bias_score": overall_bias,
                "bias_level": "Low" if overall_bias < 30 else "Medium" if overall_bias < 60 else "High"
            },
            "calculated_at": datetime.now().isoformat()
        }
    
    def _calculate_level(self, points: int) -> Dict:
        """Get current level based on points"""
        for level in reversed(self.levels):
            if points >= level["min_points"]:
                return level
        return self.levels[0]
    
    def _get_next_level(self, points: int) -> Dict:
        """Get next level to achieve"""
        for level in self.levels:
            if points < level["min_points"]:
                return level
        return None
    
    def get_daily_challenge(self) -> Dict:
        """
        Get today's investment challenge
        Encourages good behavior daily
        """
        challenges = [
            {
                "id": "no_panic",
                "title": "🧘 Stay Calm Challenge",
                "description": "Don't sell anything today, no matter what!",
                "points": 50,
                "duration": "1 day"
            },
            {
                "id": "research_first",
                "title": "📚 Research Challenge",
                "description": "Read 3 articles before making any trade today",
                "points": 30,
                "duration": "1 day"
            },
            {
                "id": "check_bias",
                "title": "🔍 Bias Check",
                "description": "Review your bias report before any trade",
                "points": 25,
                "duration": "1 day"
            },
            {
                "id": "diversify",
                "title": "🌈 Diversify Challenge",
                "description": "Look at a sector you've never invested in",
                "points": 40,
                "duration": "1 day"
            },
            {
                "id": "long_term",
                "title": "⏳ Long Term Thinking",
                "description": "Write down your 5-year investment goals",
                "points": 35,
                "duration": "1 day"
            }
        ]
        
        # Return random challenge
        challenge = random.choice(challenges)
        challenge['date'] = datetime.now().strftime("%Y-%m-%d")
        challenge['expires_at'] = (
            datetime.now() + timedelta(days=1)
        ).isoformat()
        
        return challenge
    
    def get_leaderboard(self) -> List[Dict]:
        """
        Mock leaderboard showing top investors
        In production this would use real data
        """
        leaderboard = [
            {
                "rank": 1,
                "username": "InvestorPro",
                "points": 1250,
                "level": "🏆 Master Investor",
                "badges": 8
            },
            {
                "rank": 2,
                "username": "ValueHunter",
                "points": 980,
                "level": "💎 Diamond Investor",
                "badges": 6
            },
            {
                "rank": 3,
                "username": "PatientBull",
                "points": 850,
                "level": "💎 Diamond Investor",
                "badges": 5
            },
            {
                "rank": 4,
                "username": "RationalRaj",
                "points": 720,
                "level": "🌳 Established Investor",
                "badges": 4
            },
            {
                "rank": 5,
                "username": "BiasFreeTader",
                "points": 650,
                "level": "🌳 Established Investor",
                "badges": 4
            }
        ]
        return leaderboard