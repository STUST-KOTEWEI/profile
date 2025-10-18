"""
Tone and mood analysis module.
"""

from typing import Dict, Any, List


class ToneAnalyzer:
    """
    Analyzes tone and mood in narrative text.
    
    Detects narrative tone (formal, informal, dramatic, humorous, etc.)
    and overall mood (dark, light, tense, calm, etc.).
    """
    
    def __init__(self):
        """Initialize the tone analyzer."""
        self.tone_patterns = self._initialize_tone_patterns()
    
    def _initialize_tone_patterns(self) -> Dict[str, List[str]]:
        """
        Initialize tone detection patterns.
        
        Returns:
            Dictionary mapping tone types to keyword patterns
        """
        return {
            'formal': ['therefore', 'furthermore', 'consequently', 'moreover', 'thus'],
            'informal': ['yeah', 'gonna', 'wanna', 'kinda', 'pretty much'],
            'dramatic': ['suddenly', 'unexpectedly', 'shocking', 'intense', 'dramatic'],
            'humorous': ['funny', 'hilarious', 'amusing', 'comical', 'laugh'],
            'serious': ['serious', 'grave', 'solemn', 'critical', 'important'],
            'optimistic': ['hope', 'bright', 'positive', 'promising', 'encouraging'],
            'pessimistic': ['hopeless', 'grim', 'bleak', 'despair', 'unfortunate']
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze tone and mood in the given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing tone analysis with:
            - primary_tone: Main detected tone
            - tone_scores: Confidence scores for each tone
            - mood: Overall mood descriptor
            - intensity: Intensity level (0.0 to 1.0)
        """
        tone_scores = self._calculate_tone_scores(text)
        primary_tone = max(tone_scores, key=tone_scores.get) if tone_scores else 'neutral'
        
        mood = self._detect_mood(text, tone_scores)
        intensity = self._calculate_intensity(text)
        
        return {
            'primary_tone': primary_tone,
            'tone_scores': tone_scores,
            'mood': mood,
            'intensity': intensity
        }
    
    def _calculate_tone_scores(self, text: str) -> Dict[str, float]:
        """
        Calculate confidence scores for each tone type.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping tone types to confidence scores
        """
        text_lower = text.lower()
        scores = {}
        
        for tone, keywords in self.tone_patterns.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[tone] = min(count / max(len(keywords), 1), 1.0)
        
        return scores
    
    def _detect_mood(self, text: str, tone_scores: Dict[str, float]) -> str:
        """
        Detect overall mood based on tone analysis.
        
        Args:
            text: Input text
            tone_scores: Calculated tone scores
            
        Returns:
            Mood descriptor
        """
        mood_mapping = {
            'dramatic': 'intense',
            'serious': 'somber',
            'humorous': 'lighthearted',
            'optimistic': 'uplifting',
            'pessimistic': 'melancholic',
            'formal': 'professional',
            'informal': 'casual'
        }
        
        if tone_scores:
            primary_tone = max(tone_scores, key=tone_scores.get)
            return mood_mapping.get(primary_tone, 'neutral')
        
        return 'neutral'
    
    def _calculate_intensity(self, text: str) -> float:
        """
        Calculate emotional intensity of the text.
        
        Args:
            text: Input text
            
        Returns:
            Intensity score (0.0 to 1.0)
        """
        intensity_markers = [
            '!', '?', 'very', 'extremely', 'absolutely', 'completely',
            'totally', 'utterly', 'incredibly', 'amazingly'
        ]
        
        text_lower = text.lower()
        count = sum(1 for marker in intensity_markers if marker in text_lower)
        
        # Normalize to 0-1 range
        return min(count / 10.0, 1.0)
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze tone for multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of tone analysis results
        """
        return [self.analyze(text) for text in texts]
