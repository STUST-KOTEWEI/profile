"""
Sentiment Analysis module using Hugging Face Transformers.
"""

from typing import Dict, Any, List


class SentimentAnalyzer:
    """
    Analyzes sentiment in text using pre-trained transformer models.
    
    Provides sentiment classification (positive, negative, neutral) and
    emotion detection (joy, sadness, anger, fear, etc.).
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_name: Name of the sentiment analysis model from Hugging Face
        """
        self.model_name = model_name
        self.pipeline = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Lazy initialization of the sentiment analysis pipeline."""
        try:
            from transformers import pipeline
            self.pipeline = pipeline("sentiment-analysis", model=self.model_name)
        except ImportError:
            # Fallback to simple rule-based analysis if transformers not available
            self.pipeline = None
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment in the given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing sentiment analysis results with:
            - label: Sentiment label (POSITIVE, NEGATIVE, NEUTRAL)
            - score: Confidence score
            - emotions: Detected emotions with scores
        """
        if self.pipeline is not None:
            # Use transformer model
            result = self.pipeline(text[:512])[0]  # Limit to 512 tokens
            return {
                'label': result['label'],
                'score': float(result['score']),
                'emotions': self._extract_emotions(text)
            }
        else:
            # Fallback to rule-based analysis
            return self._rule_based_sentiment(text)
    
    def _extract_emotions(self, text: str) -> Dict[str, float]:
        """
        Extract emotion scores from text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping emotion names to confidence scores
        """
        emotion_keywords = {
            'joy': ['happy', 'joyful', 'delighted', 'pleased', 'cheerful', 'excited'],
            'sadness': ['sad', 'unhappy', 'depressed', 'melancholy', 'sorrowful'],
            'anger': ['angry', 'furious', 'enraged', 'mad', 'irritated'],
            'fear': ['afraid', 'scared', 'terrified', 'fearful', 'anxious'],
            'surprise': ['surprised', 'amazed', 'astonished', 'shocked'],
            'love': ['love', 'affection', 'adore', 'cherish', 'devoted']
        }
        
        text_lower = text.lower()
        emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            emotions[emotion] = min(count / len(keywords), 1.0)
        
        return emotions
    
    def _rule_based_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Simple rule-based sentiment analysis fallback.
        
        Args:
            text: Input text
            
        Returns:
            Basic sentiment analysis result
        """
        positive_words = ['good', 'great', 'excellent', 'wonderful', 'happy', 'joy', 'love']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'fear']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            label = 'POSITIVE'
            score = 0.6 + (0.4 * pos_count / (pos_count + neg_count + 1))
        elif neg_count > pos_count:
            label = 'NEGATIVE'
            score = 0.6 + (0.4 * neg_count / (pos_count + neg_count + 1))
        else:
            label = 'NEUTRAL'
            score = 0.5
        
        return {
            'label': label,
            'score': score,
            'emotions': self._extract_emotions(text)
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment analysis results
        """
        return [self.analyze(text) for text in texts]
