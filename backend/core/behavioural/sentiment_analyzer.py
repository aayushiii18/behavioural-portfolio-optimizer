from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class SentimentAnalyzer:
    """
    Analyzes market sentiment using NLP
    
    VADER = Valence Aware Dictionary 
            and sEntiment Reasoner
    
    Perfect for financial text analysis!
    Works without training data.
    """
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_text(self, text: str) -> dict:
        """
        Analyze sentiment of any text
        
        Returns scores:
        - positive: 0 to 1
        - negative: 0 to 1  
        - neutral: 0 to 1
        - compound: -1 to +1
          (-1 = most negative, +1 = most positive)
        """
        scores = self.analyzer.polarity_scores(text)
        
        # Determine overall sentiment
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = "POSITIVE"
        elif compound <= -0.05:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"
        
        return {
            "text": text[:100],
            "sentiment": sentiment,
            "compound_score": round(compound, 3),
            "positive_score": round(scores['pos'], 3),
            "negative_score": round(scores['neg'], 3),
            "neutral_score": round(scores['neu'], 3)
        }
    
    def analyze_multiple_texts(self, texts: list) -> dict:
        """Analyze multiple news headlines"""
        results = []
        for text in texts:
            result = self.analyze_text(text)
            results.append(result)
        
        # Calculate overall sentiment
        avg_compound = sum(r['compound_score'] for r in results) / len(results)
        
        positive_count = sum(1 for r in results if r['sentiment'] == 'POSITIVE')
        negative_count = sum(1 for r in results if r['sentiment'] == 'NEGATIVE')
        neutral_count = sum(1 for r in results if r['sentiment'] == 'NEUTRAL')
        
        return {
            "individual_results": results,
            "overall_sentiment": "POSITIVE" if avg_compound > 0.05 else "NEGATIVE" if avg_compound < -0.05 else "NEUTRAL",
            "avg_compound_score": round(avg_compound, 3),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "total_analyzed": len(results)
        }
    
    def get_stock_sentiment(self, symbol: str) -> dict:
        """
        Get sentiment for a specific stock
        using its recent news
        """
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if not news:
                return {
                    "symbol": symbol,
                    "sentiment": "NEUTRAL",
                    "message": "No recent news found"
                }
            
            # Analyze headlines
            headlines = []
            for article in news[:10]:
                if 'title' in article:
                    headlines.append(article['title'])
            
            if not headlines:
                return {
                    "symbol": symbol,
                    "sentiment": "NEUTRAL",
                    "message": "No headlines found"
                }
            
            sentiment_results = self.analyze_multiple_texts(headlines)
            
            return {
                "symbol": symbol,
                "headlines_analyzed": len(headlines),
                "overall_sentiment": sentiment_results['overall_sentiment'],
                "sentiment_score": sentiment_results['avg_compound_score'],
                "positive_news": sentiment_results['positive_count'],
                "negative_news": sentiment_results['negative_count'],
                "headlines": headlines[:5],
                "analysis": sentiment_results
            }
            
        except Exception as e:
            return {
                "symbol": symbol,
                "sentiment": "NEUTRAL",
                "error": str(e)
            }
    
    def analyze_market_sample_news(self) -> dict:
        """
        Analyze sample market news
        for demonstration
        """
        sample_headlines = [
            "Stock market hits record high amid strong earnings",
            "Fed raises interest rates, market tumbles",
            "Tech stocks surge on AI optimism",
            "Recession fears grip Wall Street",
            "Apple reports better than expected profits",
            "Banking sector faces regulatory scrutiny",
            "Oil prices drop amid oversupply concerns",
            "Consumer confidence reaches 2-year high",
            "Inflation data shows signs of cooling",
            "Global markets rally on positive economic data"
        ]
        
        results = self.analyze_multiple_texts(sample_headlines)
        results['source'] = 'sample_market_news'
        return results
    
    def detect_emotional_trading(
        self, 
        transactions: list, 
        sentiment_score: float
    ) -> dict:
        """
        Detect if investor makes emotional
        decisions based on market sentiment
        
        If market is very negative but 
        investor is panic selling = emotional trading
        """
        if not transactions:
            return {"emotional_trading_score": 0}
        
        # Count panic sells during negative sentiment
        panic_sells = 0
        fomo_buys = 0
        
        for txn in transactions:
            # Panic selling when market is negative
            if (txn['action'] == 'SELL' and 
                txn['market_condition'] == 'bear' and
                sentiment_score < -0.3):
                panic_sells += 1
            
            # FOMO buying when market is positive
            if (txn['action'] == 'BUY' and
                txn['market_condition'] == 'bull' and
                sentiment_score > 0.3):
                fomo_buys += 1
        
        total = len(transactions)
        emotional_score = min(100, 
            ((panic_sells + fomo_buys) / total) * 100
        )
        
        return {
            "emotional_trading_score": round(emotional_score),
            "panic_sells": panic_sells,
            "fomo_buys": fomo_buys,
            "sentiment_influence": "HIGH" if emotional_score > 50 else "LOW",
            "recommendation": (
                "⚠️ Your trading is heavily influenced by market sentiment. "
                "Try to make decisions based on fundamentals, not emotions."
                if emotional_score > 50 else
                "✅ You show good emotional discipline in your trading!"
            )
        }