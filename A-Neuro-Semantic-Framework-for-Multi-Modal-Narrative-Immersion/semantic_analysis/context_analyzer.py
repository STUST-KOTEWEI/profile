"""
Context and story background analysis module.
"""

from typing import Dict, Any, List


class ContextAnalyzer:
    """
    Analyzes story context, setting, and background information.
    
    Extracts temporal, spatial, and thematic context from narrative text.
    """
    
    def __init__(self):
        """Initialize the context analyzer."""
        self.context_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """
        Initialize context detection patterns.
        
        Returns:
            Dictionary mapping context types to keywords
        """
        return {
            'temporal': {
                'past': ['ago', 'yesterday', 'previously', 'before', 'earlier', 'once'],
                'present': ['now', 'today', 'currently', 'presently', 'at this moment'],
                'future': ['tomorrow', 'later', 'soon', 'will', 'going to', 'next']
            },
            'spatial': {
                'indoor': ['room', 'house', 'building', 'inside', 'indoor', 'hall'],
                'outdoor': ['outside', 'garden', 'street', 'park', 'outdoor', 'field'],
                'urban': ['city', 'town', 'street', 'building', 'urban', 'downtown'],
                'rural': ['village', 'countryside', 'farm', 'rural', 'forest', 'mountain']
            },
            'themes': {
                'adventure': ['journey', 'quest', 'adventure', 'explore', 'discovery'],
                'mystery': ['mystery', 'secret', 'hidden', 'unknown', 'puzzle'],
                'romance': ['love', 'romance', 'heart', 'passion', 'affection'],
                'conflict': ['war', 'battle', 'fight', 'conflict', 'struggle'],
                'growth': ['learn', 'grow', 'develop', 'change', 'transform']
            }
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze context and background of the narrative.
        
        Args:
            text: Input narrative text
            
        Returns:
            Dictionary containing:
            - temporal_context: Time period/setting
            - spatial_context: Location/setting
            - themes: Detected narrative themes
            - setting_description: Overall setting summary
        """
        temporal = self._detect_temporal_context(text)
        spatial = self._detect_spatial_context(text)
        themes = self._detect_themes(text)
        
        return {
            'temporal_context': temporal,
            'spatial_context': spatial,
            'themes': themes,
            'setting_description': self._generate_setting_description(temporal, spatial, themes)
        }
    
    def _detect_temporal_context(self, text: str) -> Dict[str, Any]:
        """
        Detect temporal context (when the story takes place).
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with temporal information
        """
        text_lower = text.lower()
        scores = {}
        
        for period, keywords in self.context_patterns['temporal'].items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[period] = count
        
        primary_period = max(scores, key=scores.get) if any(scores.values()) else 'unspecified'
        
        return {
            'primary_period': primary_period,
            'period_scores': scores,
            'is_historical': self._check_historical(text),
            'is_futuristic': self._check_futuristic(text)
        }
    
    def _detect_spatial_context(self, text: str) -> Dict[str, Any]:
        """
        Detect spatial context (where the story takes place).
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with spatial information
        """
        text_lower = text.lower()
        scores = {}
        
        for setting, keywords in self.context_patterns['spatial'].items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[setting] = count
        
        primary_setting = max(scores, key=scores.get) if any(scores.values()) else 'unspecified'
        
        return {
            'primary_setting': primary_setting,
            'setting_scores': scores
        }
    
    def _detect_themes(self, text: str) -> Dict[str, float]:
        """
        Detect narrative themes.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping themes to confidence scores
        """
        text_lower = text.lower()
        theme_scores = {}
        
        for theme, keywords in self.context_patterns['themes'].items():
            if len(keywords) > 0:
                count = sum(1 for keyword in keywords if keyword in text_lower)
                theme_scores[theme] = min(count / len(keywords), 1.0)
        
        # Filter out themes with zero score
        return {theme: score for theme, score in theme_scores.items() if score > 0}
    
    def _check_historical(self, text: str) -> bool:
        """Check if the narrative has historical elements."""
        historical_keywords = ['century', 'ancient', 'medieval', 'historical', 'era', 'dynasty']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in historical_keywords)
    
    def _check_futuristic(self, text: str) -> bool:
        """Check if the narrative has futuristic elements."""
        futuristic_keywords = ['future', 'technology', 'robot', 'space', 'cyber', 'virtual']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in futuristic_keywords)
    
    def _generate_setting_description(
        self, 
        temporal: Dict[str, Any], 
        spatial: Dict[str, Any],
        themes: Dict[str, float]
    ) -> str:
        """
        Generate a human-readable setting description.
        
        Args:
            temporal: Temporal context data
            spatial: Spatial context data
            themes: Detected themes
            
        Returns:
            Setting description string
        """
        parts = []
        
        # Temporal description
        period = temporal.get('primary_period', 'unspecified')
        if period != 'unspecified':
            parts.append(f"Set in the {period}")
        
        # Spatial description
        setting = spatial.get('primary_setting', 'unspecified')
        if setting != 'unspecified':
            parts.append(f"in a {setting} environment")
        
        # Themes
        if themes:
            top_theme = max(themes, key=themes.get)
            parts.append(f"with themes of {top_theme}")
        
        if not parts:
            return "Context information limited."
        
        return ", ".join(parts) + "."
