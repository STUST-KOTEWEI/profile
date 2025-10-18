"""
Main Semantic Analyzer module that coordinates all semantic analysis components.
"""

from typing import Dict, List, Any
from .sentiment_analyzer import SentimentAnalyzer
from .tone_analyzer import ToneAnalyzer
from .relationship_extractor import RelationshipExtractor
from .context_analyzer import ContextAnalyzer


class SemanticAnalyzer:
    """
    Comprehensive semantic analyzer that combines multiple NLP analysis components.
    
    This class serves as the main interface for performing deep semantic analysis
    on narrative text, including sentiment, tone, character relationships, and context.
    """
    
    def __init__(self, model_name: str = "bert-base-uncased"):
        """
        Initialize the semantic analyzer with all sub-analyzers.
        
        Args:
            model_name: Name of the Hugging Face model to use for base embeddings
        """
        self.model_name = model_name
        self.sentiment_analyzer = SentimentAnalyzer()
        self.tone_analyzer = ToneAnalyzer()
        self.relationship_extractor = RelationshipExtractor()
        self.context_analyzer = ContextAnalyzer()
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive semantic analysis on the input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing all analysis results including:
            - semantic_units: List of semantic units (sentences/paragraphs)
            - sentiment: Sentiment analysis results
            - tone: Tone and mood analysis
            - relationships: Character relationships
            - context: Story background and context
        """
        semantic_units = self._decompose_text(text)
        
        results = {
            'semantic_units': semantic_units,
            'sentiment': self.sentiment_analyzer.analyze(text),
            'tone': self.tone_analyzer.analyze(text),
            'relationships': self.relationship_extractor.extract(text),
            'context': self.context_analyzer.analyze(text)
        }
        
        return results
    
    def _decompose_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Decompose text into semantic units (sentences).
        
        Args:
            text: Input text to decompose
            
        Returns:
            List of semantic units with metadata
        """
        import re
        
        # Split into sentences using common sentence delimiters
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        semantic_units = []
        for idx, sentence in enumerate(sentences):
            unit = {
                'id': idx,
                'text': sentence,
                'length': len(sentence.split()),
                'type': 'sentence'
            }
            semantic_units.append(unit)
        
        return semantic_units
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze multiple texts in batch.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of analysis results for each text
        """
        return [self.analyze(text) for text in texts]
