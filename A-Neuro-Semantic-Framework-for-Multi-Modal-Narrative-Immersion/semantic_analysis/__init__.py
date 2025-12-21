"""
Deep Semantic Analysis Module for Multi-Modal Narrative Immersion

This module provides NLP-based semantic analysis capabilities including:
- Text decomposition into semantic units
- Sentiment analysis
- Tone and mood detection
- Character relationship extraction
- Story background and context analysis
- Multi-language support (Chinese, Japanese, Korean, English)
- Dialogue analysis
- Knowledge graph construction
- Timeline tracking and temporal analysis
- Advanced Named Entity Recognition (NER)
"""

from .semantic_analyzer import SemanticAnalyzer
from .sentiment_analyzer import SentimentAnalyzer
from .tone_analyzer import ToneAnalyzer
from .relationship_extractor import RelationshipExtractor
from .context_analyzer import ContextAnalyzer
from .multilingual import LanguageDetector, MultilingualAnalyzer
from .dialogue_analyzer import DialogueAnalyzer
from .knowledge_graph import KnowledgeGraphBuilder
from .timeline_tracker import TimelineTracker
from .entity_recognizer import EntityRecognizer

__all__ = [
    'SemanticAnalyzer',
    'SentimentAnalyzer',
    'ToneAnalyzer',
    'RelationshipExtractor',
    'ContextAnalyzer',
    'LanguageDetector',
    'MultilingualAnalyzer',
    'DialogueAnalyzer',
    'KnowledgeGraphBuilder',
    'TimelineTracker',
    'EntityRecognizer'
]

__version__ = '1.2.0'
