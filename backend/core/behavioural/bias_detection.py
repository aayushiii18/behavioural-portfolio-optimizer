import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class BiasDetector:
    """
    Detects 8 investor behavioural biases
    Each bias is scored from 0-100
    0 = No bias detected
    100 = Extreme bias detected
    """
    
    def __init__(self):
        self.bias_weights = {
            "overconfidence": 0.15,
            "loss_aversion": 0.20,
            "recency_bias": 0.15,
            "confirmation_bias": 0.10,
            "herd_mentality": 0.15,
            "anchoring": 0.10,
            "fomo": 0.10,
            "disposition_effect": 0.05
        }
    
    # ==================
    # BIAS 1: OVERCONFIDENCE
    # ==================
    def detect_overconfidence(self, transactions: list) -> dict:
        """
        Overconfidence = Trading too frequently
        thinking you know better than the market
        Signs:
        - Too many trades
        - Large position sizes
        - Short holding periods
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        # Count trades per month
        total_trades = len(transactions)
        trades_per_month = total_trades / 12
        
        # Score based on trading frequency
        if trades_per_month > 20:
            score = 90
        elif trades_per_month > 15:
            score = 75
        elif trades_per_month > 10:
            score = 60
        elif trades_per_month > 5:
            score = 40
        else:
            score = 20
        
        # Check average position size
        avg_value = np.mean([t['total_value'] for t in transactions])
        if avg_value > 10000:
            score = min(100, score + 15)
        
        return {
            "score": round(score),
            "level": self._get_level(score),
            "trades_per_month": round(trades_per_month, 1),
            "description": self._get_overconfidence_description(score),
            "nudge": self._get_overconfidence_nudge(score)
        }
    
    # ==================
    # BIAS 2: LOSS AVERSION
    # ==================
    def detect_loss_aversion(self, transactions: list) -> dict:
        """
        Loss Aversion = Feeling losses more than gains
        Signs:
        - Holding losing positions too long
        - Selling winning positions too early
        - Panic selling during drops
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        buy_prices = {}
        early_wins = 0
        held_losses = 0
        total_sells = 0
        
        for txn in transactions:
            symbol = txn['symbol']
            if txn['action'] == 'BUY':
                buy_prices[symbol] = txn['price']
            elif txn['action'] == 'SELL' and symbol in buy_prices:
                total_sells += 1
                profit_pct = (txn['price'] - buy_prices[symbol]) / buy_prices[symbol]
                
                # Sold winner early (less than 10% gain)
                if 0 < profit_pct < 0.10:
                    early_wins += 1
                
                # Held loser too long (more than 15% loss)
                if profit_pct < -0.15:
                    held_losses += 1
        
        if total_sells == 0:
            return {"score": 0, "level": "Low", "description": "No sells yet"}
        
        early_win_ratio = early_wins / total_sells
        held_loss_ratio = held_losses / total_sells
        
        score = min(100, (early_win_ratio * 50) + (held_loss_ratio * 50))
        score = round(score * 100)
        
        return {
            "score": min(100, score),
            "level": self._get_level(score),
            "early_wins_pct": round(early_win_ratio * 100, 1),
            "held_losses_pct": round(held_loss_ratio * 100, 1),
            "description": self._get_loss_aversion_description(score),
            "nudge": self._get_loss_aversion_nudge(score)
        }
    
    # ==================
    # BIAS 3: RECENCY BIAS
    # ==================
    def detect_recency_bias(self, transactions: list) -> dict:
        """
        Recency Bias = Overweighting recent events
        Signs:
        - Buying after recent gains
        - Selling after recent losses
        - Following recent market trends blindly
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        # Sort by date
        sorted_txns = sorted(transactions, key=lambda x: x['date'])
        
        # Check last 30 days vs overall
        recent_date = datetime.now() - timedelta(days=30)
        
        recent_buys_in_bull = 0
        recent_sells_in_bear = 0
        recent_total = 0
        
        for txn in sorted_txns:
            txn_date = datetime.fromisoformat(txn['date'])
            if txn_date > recent_date:
                recent_total += 1
                if txn['action'] == 'BUY' and txn['market_condition'] == 'bull':
                    recent_buys_in_bull += 1
                if txn['action'] == 'SELL' and txn['market_condition'] == 'bear':
                    recent_sells_in_bear += 1
        
        if recent_total == 0:
            score = 20
        else:
            recency_ratio = (recent_buys_in_bull + recent_sells_in_bear) / recent_total
            score = min(100, recency_ratio * 100)
        
        return {
            "score": round(score),
            "level": self._get_level(score),
            "recent_trend_following": recent_buys_in_bull + recent_sells_in_bear,
            "description": self._get_recency_description(score),
            "nudge": self._get_recency_nudge(score)
        }
    
    # ==================
    # BIAS 4: HERD MENTALITY
    # ==================
    def detect_herd_mentality(self, transactions: list) -> dict:
        """
        Herd Mentality = Following the crowd
        Signs:
        - Buying popular stocks everyone is buying
        - Selling when everyone else sells
        - Following market trends blindly
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        # Popular stocks (meme stocks, trending)
        herd_stocks = ['TSLA', 'GME', 'AMC', 'NVDA', 'META']
        
        herd_trades = [t for t in transactions if t['symbol'] in herd_stocks]
        herd_ratio = len(herd_trades) / len(transactions)
        
        # Check if buying during bull market (following crowd)
        bull_buys = [t for t in transactions 
                    if t['action'] == 'BUY' and t['market_condition'] == 'bull']
        bull_ratio = len(bull_buys) / len(transactions)
        
        score = min(100, (herd_ratio * 50 + bull_ratio * 50) * 100)
        
        return {
            "score": round(score),
            "level": self._get_level(score),
            "herd_stock_trades": len(herd_trades),
            "description": self._get_herd_description(score),
            "nudge": self._get_herd_nudge(score)
        }
    
    # ==================
    # BIAS 5: ANCHORING
    # ==================
    def detect_anchoring(self, transactions: list) -> dict:
        """
        Anchoring = Fixating on a specific price point
        Signs:
        - Not selling below purchase price
        - Setting price targets based on purchase price
        - Waiting for stock to return to original price
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        buy_prices = {}
        anchored_trades = 0
        total_sells = 0
        
        for txn in transactions:
            symbol = txn['symbol']
            if txn['action'] == 'BUY':
                buy_prices[symbol] = txn['price']
            elif txn['action'] == 'SELL' and symbol in buy_prices:
                total_sells += 1
                price_diff_pct = abs(txn['price'] - buy_prices[symbol]) / buy_prices[symbol]
                # Sold very close to purchase price (within 2%)
                if price_diff_pct < 0.02:
                    anchored_trades += 1
        
        if total_sells == 0:
            return {"score": 0, "level": "Low", "description": "No sells yet"}
        
        anchor_ratio = anchored_trades / total_sells
        score = min(100, anchor_ratio * 100)
        
        return {
            "score": round(score),
            "level": self._get_level(score),
            "anchored_trades": anchored_trades,
            "description": self._get_anchoring_description(score),
            "nudge": self._get_anchoring_nudge(score)
        }
    
    # ==================
    # BIAS 6: FOMO
    # ==================
    def detect_fomo(self, transactions: list) -> dict:
        """
        FOMO = Fear of Missing Out
        Signs:
        - Buying at market peaks
        - Chasing performance
        - Buying trending stocks late
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        fomo_trades = [t for t in transactions 
                      if t['action'] == 'BUY' and 
                      t['market_condition'] == 'bull' and
                      t['quantity'] > 8]
        
        fomo_ratio = len(fomo_trades) / len(transactions)
        score = min(100, fomo_ratio * 200)
        
        return {
            "score": round(score),
            "level": self._get_level(score),
            "fomo_trades": len(fomo_trades),
            "description": self._get_fomo_description(score),
            "nudge": self._get_fomo_nudge(score)
        }
    
    # ==================
    # BIAS 7: DISPOSITION EFFECT
    # ==================
    def detect_disposition_effect(self, transactions: list) -> dict:
        """
        Disposition Effect = Selling winners too early,
        holding losers too long
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        buy_prices = {}
        winners_sold = 0
        losers_held = 0
        total_analyzed = 0
        
        for txn in transactions:
            symbol = txn['symbol']
            if txn['action'] == 'BUY':
                buy_prices[symbol] = txn['price']
            elif txn['action'] == 'SELL' and symbol in buy_prices:
                total_analyzed += 1
                pnl = txn['price'] - buy_prices[symbol]
                if pnl > 0:
                    winners_sold += 1
                else:
                    losers_held += 1
        
        if total_analyzed == 0:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        disposition_ratio = winners_sold / total_analyzed
        score = min(100, disposition_ratio * 100)
        
        return {
            "score": round(score),
            "level": self._get_level(score),
            "winners_sold_early": winners_sold,
            "losers_held": losers_held,
            "description": self._get_disposition_description(score),
            "nudge": self._get_disposition_nudge(score)
        }
    
    # ==================
    # BIAS 8: CONFIRMATION BIAS
    # ==================
    def detect_confirmation_bias(self, transactions: list) -> dict:
        """
        Confirmation Bias = Only seeking information
        that confirms existing beliefs
        Signs:
        - Repeatedly buying same stocks
        - Never diversifying
        - Ignoring negative signals
        """
        if not transactions:
            return {"score": 0, "level": "Low", "description": "No data"}
        
        # Check stock concentration
        symbol_counts = {}
        for txn in transactions:
            symbol = txn['symbol']
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        
        total = len(transactions)
        max_concentration = max(symbol_counts.values()) / total
        
        # High concentration in one stock = confirmation bias
        score = min(100, max_concentration * 100)
        
        return {
            "score": round(score),
            "level": self._get_level(score),
            "most_traded_stock": max(symbol_counts, key=symbol_counts.get),
            "concentration": round(max_concentration * 100, 1),
            "description": self._get_confirmation_description(score),
            "nudge": self._get_confirmation_nudge(score)
        }
    
    # ==================
    # FULL BIAS ANALYSIS
    # ==================
    def analyze_all_biases(self, transactions: list) -> dict:
        """Run all bias detections and return complete profile"""
        
        biases = {
            "overconfidence": self.detect_overconfidence(transactions),
            "loss_aversion": self.detect_loss_aversion(transactions),
            "recency_bias": self.detect_recency_bias(transactions),
            "herd_mentality": self.detect_herd_mentality(transactions),
            "anchoring": self.detect_anchoring(transactions),
            "fomo": self.detect_fomo(transactions),
            "disposition_effect": self.detect_disposition_effect(transactions),
            "confirmation_bias": self.detect_confirmation_bias(transactions)
        }
        
        # Calculate overall bias score
        overall_score = np.mean([b["score"] for b in biases.values()])
        
        # Find dominant bias
        dominant_bias = max(biases, key=lambda x: biases[x]["score"])
        
        return {
            "biases": biases,
            "overall_score": round(overall_score),
            "overall_level": self._get_level(overall_score),
            "dominant_bias": dominant_bias,
            "dominant_score": biases[dominant_bias]["score"],
            "analysis_date": datetime.now().isoformat(),
            "total_transactions_analyzed": len(transactions)
        }
    
    # ==================
    # HELPER METHODS
    # ==================
    def _get_level(self, score: float) -> str:
        if score >= 75:
            return "High"
        elif score >= 50:
            return "Medium"
        elif score >= 25:
            return "Low"
        else:
            return "Minimal"
    
    def _get_overconfidence_description(self, score):
        if score >= 75:
            return "You trade very frequently, suggesting overconfidence in your ability to time the market."
        elif score >= 50:
            return "You trade more than average. Consider if each trade is truly necessary."
        else:
            return "Your trading frequency is reasonable."
    
    def _get_overconfidence_nudge(self, score):
        if score >= 75:
            return "⚠️ You've made many trades this month. Research shows frequent traders earn less. Consider holding longer."
        elif score >= 50:
            return "💡 Before your next trade, ask yourself: Is this better than just holding my current positions?"
        else:
            return "✅ Great job! Your trading frequency is healthy."
    
    def _get_loss_aversion_description(self, score):
        if score >= 75:
            return "You tend to sell winners too early and hold losers too long."
        elif score >= 50:
            return "Some signs of loss aversion detected in your trading pattern."
        else:
            return "Your win/loss management looks balanced."
    
    def _get_loss_aversion_nudge(self, score):
        if score >= 75:
            return "⚠️ You sold winners early 3 times this month. Let your winners run longer!"
        elif score >= 50:
            return "💡 Consider setting stop losses to remove emotion from selling decisions."
        else:
            return "✅ Good job managing your positions!"
    
    def _get_recency_description(self, score):
        if score >= 75:
            return "You are heavily influenced by recent market events."
        elif score >= 50:
            return "Some recency bias detected. You may be overweighting recent performance."
        else:
            return "You show good long-term thinking."
    
    def _get_recency_nudge(self, score):
        if score >= 75:
            return "⚠️ Recent market moves are affecting your decisions. Look at 5-year trends before trading."
        else:
            return "💡 Remember: Past performance does not guarantee future results."
    
    def _get_herd_description(self, score):
        if score >= 75:
            return "You frequently follow market trends and popular stocks."
        else:
            return "You show some independence in your investment decisions."
    
    def _get_herd_nudge(self, score):
        if score >= 75:
            return "⚠️ You're buying what everyone else is buying. Be a contrarian investor!"
        else:
            return "💡 Great independent thinking! Keep researching before following trends."
    
    def _get_anchoring_description(self, score):
        if score >= 75:
            return "You appear fixated on purchase prices when making sell decisions."
        else:
            return "You show flexibility in your price targets."
    
    def _get_anchoring_nudge(self, score):
        if score >= 75:
            return "⚠️ Don't wait for a stock to return to your purchase price. Evaluate based on future prospects."
        else:
            return "✅ Good job evaluating stocks on their merits!"
    
    def _get_fomo_description(self, score):
        if score >= 75:
            return "You frequently buy stocks after they have already risen significantly."
        else:
            return "You show patience in your buying decisions."
    
    def _get_fomo_nudge(self, score):
        if score >= 75:
            return "⚠️ Buying after a big run-up is risky. Wait for pullbacks before entering."
        else:
            return "✅ Great patience! You're not chasing performance."
    
    def _get_disposition_description(self, score):
        if score >= 75:
            return "You tend to sell winners too quickly and hold losers too long."
        else:
            return "Your buy/sell decisions show reasonable balance."
    
    def _get_disposition_nudge(self, score):
        if score >= 75:
            return "⚠️ You sold 3 winners this week. Consider holding winners for at least 30 more days."
        else:
            return "💡 Keep letting your winners run while cutting losses early."
    
    def _get_confirmation_description(self, score):
        if score >= 75:
            return "You are heavily concentrated in a few stocks, suggesting confirmation bias."
        else:
            return "You show reasonable diversification in your portfolio."
    
    def _get_confirmation_nudge(self, score):
        if score >= 75:
            return "⚠️ You're too concentrated in one stock. Diversify to reduce risk!"
        else:
            return "✅ Good diversification! Keep spreading your investments."