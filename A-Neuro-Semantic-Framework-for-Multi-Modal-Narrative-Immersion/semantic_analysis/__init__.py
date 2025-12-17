"""
Deep Semantic Analysis Module for Multi-Modal Narrative Immersion

This module provides NLP-based semantic analysis capabilities including:
- Text decomposition into semantic units
- Sentiment analysis
- Tone and mood detection
- Character relationship extraction
- Story background and context analysis
"""

from .semantic_analyzer import SemanticAnalyzer
from .sentiment_analyzer import SentimentAnalyzer
from .tone_analyzer import ToneAnalyzer
from .relationship_extractor import RelationshipExtractor
from .context_analyzer import ContextAnalyzer

__all__ = [
    'SemanticAnalyzer',
    'SentimentAnalyzer',
    'ToneAnalyzer',
    'RelationshipExtractor',
    'ContextAnalyzer'
]

__version__ = '1.0.0'
