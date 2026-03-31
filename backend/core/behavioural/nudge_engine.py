from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random

class NudgeEngine:
    """
    Personalized Nudge System
    
    Delivers the right message
    at the right time
    to prevent biased decisions
    """
    
    def __init__(self):
        self.cooling_off_hours = 24
        self.nudge_types = [
            "warning",
            "tip", 
            "education",
            "celebration",
            "commitment"
        ]
    
    # ==================
    # CORE NUDGE GENERATOR
    # ==================
    def generate_nudge(
        self,
        bias_type: str,
        bias_score: int,
        context: Dict = {}
    ) -> Dict:
        """
        Generate personalized nudge
        based on detected bias
        """
        nudge_generators = {
            "overconfidence": self._overconfidence_nudge,
            "loss_aversion": self._loss_aversion_nudge,
            "recency_bias": self._recency_nudge,
            "herd_mentality": self._herd_nudge,
            "anchoring": self._anchoring_nudge,
            "fomo": self._fomo_nudge,
            "disposition_effect": self._disposition_nudge,
            "confirmation_bias": self._confirmation_nudge
        }
        
        generator = nudge_generators.get(
            bias_type,
            self._default_nudge
        )
        
        nudge = generator(bias_score, context)
        nudge['bias_type'] = bias_type
        nudge['bias_score'] = bias_score
        nudge['generated_at'] = datetime.now().isoformat()
        nudge['nudge_id'] = f"NUDGE_{random.randint(1000, 9999)}"
        
        return nudge
    
    def _overconfidence_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ Trading Too Frequently!",
                "message": (
                    "You've made many trades this month. "
                    "Research shows frequent traders earn "
                    "40% LESS than buy-and-hold investors."
                ),
                "action": "Consider a 30-day trading pause",
                "cooling_off": True,
                "cooling_off_hours": 48,
                "educational_tip": (
                    "Warren Buffett says: 'The stock market "
                    "is a device for transferring money from "
                    "the impatient to the patient.'"
                ),
                "severity": "high"
            }
        elif score >= 50:
            return {
                "type": "tip",
                "title": "💡 Trading Frequency Check",
                "message": (
                    "Before your next trade, ask yourself: "
                    "Would I make this trade if I couldn't "
                    "trade again for 1 month?"
                ),
                "action": "Review your last 5 trades first",
                "cooling_off": True,
                "cooling_off_hours": 24,
                "educational_tip": (
                    "Studies show investors who trade less "
                    "frequently outperform by 1.5% annually."
                ),
                "severity": "medium"
            }
        else:
            return {
                "type": "celebration",
                "title": "✅ Great Trading Discipline!",
                "message": "Your trading frequency is healthy!",
                "action": "Keep maintaining this discipline",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "Consistency is key to long-term returns.",
                "severity": "low"
            }
    
    def _loss_aversion_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ Loss Aversion Detected!",
                "message": (
                    "You're holding losing positions too long "
                    "and selling winners too early. "
                    "This is costing you returns!"
                ),
                "action": "Set stop-losses at -10% for all positions",
                "cooling_off": True,
                "cooling_off_hours": 24,
                "educational_tip": (
                    "Loss aversion makes losses feel 2x worse "
                    "than gains feel good. Don't let this "
                    "control your decisions!"
                ),
                "severity": "high",
                "commitment_suggestion": (
                    "I commit to selling any position "
                    "that drops more than 10% from purchase price."
                )
            }
        elif score >= 50:
            return {
                "type": "tip",
                "title": "💡 Check Your Exit Strategy",
                "message": (
                    "Some signs of loss aversion detected. "
                    "Do you have a clear exit strategy "
                    "for each position?"
                ),
                "action": "Review your stop-loss levels",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": (
                    "Having pre-set exit rules removes "
                    "emotion from selling decisions."
                ),
                "severity": "medium"
            }
        else:
            return {
                "type": "celebration",
                "title": "✅ Great Loss Management!",
                "message": "You're managing wins and losses well!",
                "action": "Keep following your exit strategy",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "Cutting losses early is a sign of discipline.",
                "severity": "low"
            }
    
    def _fomo_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ FOMO Alert!",
                "message": (
                    "You're buying stocks that have already "
                    "risen significantly. Buying at peaks "
                    "often leads to losses!"
                ),
                "action": "Wait for a 10% pullback before buying",
                "cooling_off": True,
                "cooling_off_hours": 72,
                "educational_tip": (
                    "The best time to buy is when others "
                    "are fearful, not when they're greedy. "
                    "- Warren Buffett"
                ),
                "severity": "high",
                "commitment_suggestion": (
                    "I commit to only buying stocks that "
                    "are below their 52-week high by at least 10%."
                )
            }
        elif score >= 50:
            return {
                "type": "tip",
                "title": "💡 Check Your Entry Points",
                "message": (
                    "Some FOMO buying detected. "
                    "Are you buying because of fundamentals "
                    "or because the stock is trending?"
                ),
                "action": "Research the fundamentals before buying",
                "cooling_off": True,
                "cooling_off_hours": 24,
                "educational_tip": (
                    "Price is what you pay, "
                    "value is what you get. - Warren Buffett"
                ),
                "severity": "medium"
            }
        else:
            return {
                "type": "celebration",
                "title": "✅ Great Entry Discipline!",
                "message": "You're not chasing performance!",
                "action": "Keep researching before buying",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "Patient investors find the best entry points.",
                "severity": "low"
            }
    
    def _herd_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ Following the Crowd!",
                "message": (
                    "You're buying what everyone else is buying. "
                    "By the time everyone knows about a stock, "
                    "the best gains are usually over!"
                ),
                "action": "Look for contrarian opportunities",
                "cooling_off": True,
                "cooling_off_hours": 48,
                "educational_tip": (
                    "Be fearful when others are greedy "
                    "and greedy when others are fearful. "
                    "- Warren Buffett"
                ),
                "severity": "high"
            }
        else:
            return {
                "type": "tip",
                "title": "💡 Think Independently",
                "message": "Always research independently before following trends.",
                "action": "Find one contrarian view before any trade",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "The best investors think differently from the crowd.",
                "severity": "low"
            }
    
    def _recency_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ Recency Bias Detected!",
                "message": (
                    "You're making decisions based on "
                    "recent market moves. "
                    "Recent performance rarely predicts future returns!"
                ),
                "action": "Look at 5-year trends, not 5-day trends",
                "cooling_off": True,
                "cooling_off_hours": 24,
                "educational_tip": (
                    "Markets move in cycles. "
                    "What goes up often comes down, "
                    "and vice versa."
                ),
                "severity": "high"
            }
        else:
            return {
                "type": "tip",
                "title": "💡 Long-term Thinking",
                "message": "Keep focusing on long-term fundamentals!",
                "action": "Review your investment thesis quarterly",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "Time in market beats timing the market.",
                "severity": "low"
            }
    
    def _anchoring_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ Anchoring Bias!",
                "message": (
                    "You seem fixated on your purchase price. "
                    "A stock doesn't know what you paid for it! "
                    "Evaluate based on future prospects."
                ),
                "action": "Evaluate each stock fresh every week",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": (
                    "Ask yourself: Would I buy this stock today "
                    "at current price? If no, consider selling."
                ),
                "severity": "high"
            }
        else:
            return {
                "type": "celebration",
                "title": "✅ Good Price Flexibility!",
                "message": "You evaluate stocks on merit, not purchase price!",
                "action": "Keep this rational approach",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "Focus on future value, not past cost.",
                "severity": "low"
            }
    
    def _disposition_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ Disposition Effect!",
                "message": (
                    "You tend to sell winners too early "
                    "and hold losers too long. "
                    "Let your winners run!"
                ),
                "action": "Hold winners for at least 30 more days",
                "cooling_off": True,
                "cooling_off_hours": 24,
                "educational_tip": (
                    "The disposition effect costs investors "
                    "an average of 1.5% per year in returns."
                ),
                "severity": "high"
            }
        else:
            return {
                "type": "tip",
                "title": "💡 Good Position Management",
                "message": "You're managing your positions well!",
                "action": "Keep letting winners run",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "Cut losers short, let winners run.",
                "severity": "low"
            }
    
    def _confirmation_nudge(self, score: int, context: Dict) -> Dict:
        if score >= 75:
            return {
                "type": "warning",
                "title": "⚠️ Confirmation Bias!",
                "message": (
                    "You're too concentrated in a few stocks. "
                    "Diversify to reduce risk and "
                    "challenge your assumptions!"
                ),
                "action": "Add 2 new sectors to your portfolio",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": (
                    "Seek out opinions that DISAGREE "
                    "with your investment thesis. "
                    "It will make you a better investor!"
                ),
                "severity": "high"
            }
        else:
            return {
                "type": "celebration",
                "title": "✅ Good Diversification!",
                "message": "You have a well-diversified portfolio!",
                "action": "Keep seeking different perspectives",
                "cooling_off": False,
                "cooling_off_hours": 0,
                "educational_tip": "Diversification is the only free lunch in investing.",
                "severity": "low"
            }
    
    def _default_nudge(self, score: int, context: Dict) -> Dict:
        return {
            "type": "tip",
            "title": "💡 Investment Tip",
            "message": "Keep making informed investment decisions!",
            "action": "Review your portfolio weekly",
            "cooling_off": False,
            "cooling_off_hours": 0,
            "educational_tip": "Knowledge is the best investment.",
            "severity": "low"
        }
    
    # ==================
    # COOLING OFF PERIOD
    # ==================
    def check_cooling_off(
        self,
        user_id: str,
        last_trade_time: Optional[str] = None
    ) -> Dict:
        """
        Check if investor should wait
        before making next trade
        """
        if not last_trade_time:
            return {
                "in_cooling_off": False,
                "message": "No recent trades detected",
                "can_trade": True
            }
        
        last_trade = datetime.fromisoformat(last_trade_time)
        cooling_off_end = last_trade + timedelta(hours=self.cooling_off_hours)
        now = datetime.now()
        
        if now < cooling_off_end:
            remaining = cooling_off_end - now
            hours_remaining = remaining.seconds // 3600
            
            return {
                "in_cooling_off": True,
                "can_trade": False,
                "hours_remaining": hours_remaining,
                "cooling_off_ends": cooling_off_end.isoformat(),
                "message": (
                    f"⏰ Please wait {hours_remaining} more hours "
                    f"before your next trade. "
                    f"Cooling-off periods help you make "
                    f"better decisions!"
                )
            }
        
        return {
            "in_cooling_off": False,
            "can_trade": True,
            "message": "✅ You can trade now!"
        }
    
    # ==================
    # GENERATE ALL NUDGES
    # ==================
    def generate_all_nudges(
        self,
        bias_analysis: Dict
    ) -> Dict:
        """
        Generate nudges for all detected biases
        Prioritizes highest bias scores
        """
        biases = bias_analysis.get("biases", {})
        nudges = []
        
        # Generate nudge for each bias
        for bias_type, bias_data in biases.items():
            score = bias_data.get("score", 0)
            nudge = self.generate_nudge(bias_type, score)
            nudges.append(nudge)
        
        # Sort by severity
        severity_order = {"high": 0, "medium": 1, "low": 2}
        nudges.sort(
            key=lambda x: severity_order.get(x.get("severity", "low"), 2)
        )
        
        # Get urgent nudges (high severity)
        urgent_nudges = [n for n in nudges if n.get("severity") == "high"]
        
        # Check if cooling off needed
        needs_cooling_off = any(n.get("cooling_off", False) for n in urgent_nudges)
        
        return {
            "total_nudges": len(nudges),
            "urgent_nudges": len(urgent_nudges),
            "needs_cooling_off": needs_cooling_off,
            "cooling_off_hours": max(
                (n.get("cooling_off_hours", 0) for n in urgent_nudges),
                default=0
            ),
            "nudges": nudges,
            "top_nudge": nudges[0] if nudges else None,
            "generated_at": datetime.now().isoformat()
        }