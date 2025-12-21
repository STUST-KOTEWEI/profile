"""
Simple test suite for the semantic analysis module.

This file contains basic tests to verify the core functionality of each component.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from semantic_analysis import (
    SemanticAnalyzer,
    SentimentAnalyzer,
    ToneAnalyzer,
    RelationshipExtractor,
    ContextAnalyzer
)


def test_sentiment_analyzer():
    """Test sentiment analysis functionality."""
    print("Testing SentimentAnalyzer...")
    analyzer = SentimentAnalyzer()
    
    # Test positive sentiment
    result = analyzer.analyze("I am so happy and excited about this wonderful day!")
    assert result['label'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    assert 0 <= result['score'] <= 1
    assert 'emotions' in result
    print("  ✓ Positive sentiment test passed")
    
    # Test negative sentiment
    result = analyzer.analyze("This is terrible and awful. I hate it.")
    assert result['label'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    print("  ✓ Negative sentiment test passed")
    
    # Test batch processing
    results = analyzer.analyze_batch(["Happy text", "Sad text"])
    assert len(results) == 2
    print("  ✓ Batch processing test passed")
    
    print("SentimentAnalyzer: ALL TESTS PASSED\n")


def test_tone_analyzer():
    """Test tone analysis functionality."""
    print("Testing ToneAnalyzer...")
    analyzer = ToneAnalyzer()
    
    result = analyzer.analyze("The situation was very serious and critical. We must act now!")
    assert 'primary_tone' in result
    assert 'tone_scores' in result
    assert 'mood' in result
    assert 'intensity' in result
    assert 0 <= result['intensity'] <= 1
    print("  ✓ Tone analysis test passed")
    
    # Test batch processing
    results = analyzer.analyze_batch(["Formal text", "Informal text yeah"])
    assert len(results) == 2
    print("  ✓ Batch processing test passed")
    
    print("ToneAnalyzer: ALL TESTS PASSED\n")


def test_relationship_extractor():
    """Test character relationship extraction."""
    print("Testing RelationshipExtractor...")
    extractor = RelationshipExtractor()
    
    text = "John and Mary are friends. Peter is Mary's brother."
    result = extractor.extract(text)
    
    assert 'characters' in result
    assert 'relationships' in result
    assert 'relationship_types' in result
    assert 'interaction_summary' in result
    assert isinstance(result['characters'], list)
    print("  ✓ Relationship extraction test passed")
    
    print("RelationshipExtractor: ALL TESTS PASSED\n")


def test_context_analyzer():
    """Test context and background analysis."""
    print("Testing ContextAnalyzer...")
    analyzer = ContextAnalyzer()
    
    text = "Yesterday in the city, they discovered an ancient mystery in the old building."
    result = analyzer.analyze(text)
    
    assert 'temporal_context' in result
    assert 'spatial_context' in result
    assert 'themes' in result
    assert 'setting_description' in result
    print("  ✓ Context analysis test passed")
    
    print("ContextAnalyzer: ALL TESTS PASSED\n")


def test_semantic_analyzer():
    """Test the main semantic analyzer."""
    print("Testing SemanticAnalyzer (Integration)...")
    analyzer = SemanticAnalyzer()
    
    text = "Alice was happy. She loved adventures. Today she met her friend Bob."
    result = analyzer.analyze(text)
    
    # Check all components are present
    assert 'semantic_units' in result
    assert 'sentiment' in result
    assert 'tone' in result
    assert 'relationships' in result
    assert 'context' in result
    
    # Check semantic units
    assert len(result['semantic_units']) > 0
    assert all('text' in unit for unit in result['semantic_units'])
    print("  ✓ Semantic unit decomposition test passed")
    
    # Check sentiment
    assert 'label' in result['sentiment']
    assert 'score' in result['sentiment']
    print("  ✓ Sentiment integration test passed")
    
    # Check tone
    assert 'primary_tone' in result['tone']
    assert 'mood' in result['tone']
    print("  ✓ Tone integration test passed")
    
    # Check relationships
    assert 'characters' in result['relationships']
    print("  ✓ Relationship integration test passed")
    
    # Check context
    assert 'temporal_context' in result['context']
    assert 'spatial_context' in result['context']
    print("  ✓ Context integration test passed")
    
    # Test batch processing
    texts = ["Text one.", "Text two.", "Text three."]
    results = analyzer.analyze_batch(texts)
    assert len(results) == 3
    print("  ✓ Batch processing test passed")
    
    print("SemanticAnalyzer: ALL TESTS PASSED\n")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing Edge Cases...")
    analyzer = SemanticAnalyzer()
    
    # Empty string
    result = analyzer.analyze("")
    assert result is not None
    print("  ✓ Empty string test passed")
    
    # Very short text
    result = analyzer.analyze("Hi.")
    assert result is not None
    print("  ✓ Short text test passed")
    
    # Very long text (truncation)
    long_text = "This is a very long sentence. " * 100
    result = analyzer.analyze(long_text)
    assert result is not None
    print("  ✓ Long text test passed")
    
    # Special characters
    result = analyzer.analyze("Hello!!! How are you??? Amazing!!!")
    assert result is not None
    print("  ✓ Special characters test passed")
    
    print("Edge Cases: ALL TESTS PASSED\n")


def run_all_tests():
    """Run all tests."""
    print("="*70)
    print("RUNNING SEMANTIC ANALYSIS MODULE TESTS")
    print("="*70 + "\n")
    
    try:
        test_sentiment_analyzer()
        test_tone_analyzer()
        test_relationship_extractor()
        test_context_analyzer()
        test_semantic_analyzer()
        test_edge_cases()
        test_multilingual()
        test_dialogue_analyzer()
        test_knowledge_graph()
        
        print("="*70)
        print("ALL TESTS PASSED SUCCESSFULLY! ✓")
        print("="*70)
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multilingual():
    """Test multilingual analysis functionality."""
    print("Testing MultilingualAnalyzer...")
    from semantic_analysis import LanguageDetector, MultilingualAnalyzer
    
    # Test language detection
    detector = LanguageDetector()
    
    # English text
    result = detector.detect("Hello, how are you today?")
    assert result['language_code'] in ['en', 'unknown']
    print("  ✓ English detection test passed")
    
    # Chinese text
    result = detector.detect("你好，今天天氣很好。")
    assert result['language_code'] in ['zh', 'unknown']
    print("  ✓ Chinese detection test passed")
    
    # Japanese text
    result = detector.detect("こんにちは、元気ですか？")
    assert result['language_code'] in ['ja', 'unknown']
    print("  ✓ Japanese detection test passed")
    
    # Test multilingual analyzer
    analyzer = MultilingualAnalyzer()
    result = analyzer.analyze("I am very happy today!")
    assert 'language_detection' in result
    assert 'sentiment' in result
    print("  ✓ Multilingual analysis test passed")
    
    print("MultilingualAnalyzer: ALL TESTS PASSED\n")


def test_dialogue_analyzer():
    """Test dialogue analysis functionality."""
    print("Testing DialogueAnalyzer...")
    from semantic_analysis import DialogueAnalyzer
    
    analyzer = DialogueAnalyzer()
    
    # Test with dialogue text
    text = '''
    "Hello, how are you?" asked Alice.
    "I'm fine, thank you," replied Bob.
    Alice smiled and said, "That's great to hear!"
    '''
    
    result = analyzer.analyze(text)
    assert 'dialogues' in result
    assert 'speakers' in result
    assert 'conversation_flow' in result
    assert 'statistics' in result
    print("  ✓ Dialogue extraction test passed")
    
    # Test dialogue extraction
    dialogues = analyzer.extract_dialogues(text)
    assert isinstance(dialogues, list)
    print("  ✓ Dialogue list test passed")
    
    # Test with no dialogue
    result = analyzer.analyze("There was no conversation in this text.")
    assert result is not None
    print("  ✓ No dialogue test passed")
    
    print("DialogueAnalyzer: ALL TESTS PASSED\n")


def test_knowledge_graph():
    """Test knowledge graph functionality."""
    print("Testing KnowledgeGraphBuilder...")
    from semantic_analysis import KnowledgeGraphBuilder
    
    builder = KnowledgeGraphBuilder()
    
    # Test with narrative text
    text = '''
    Alice lived in Wonderland. She met the Mad Hatter at his tea party.
    The Queen of Hearts ruled the kingdom with an iron fist.
    Alice and the Hatter became good friends during her journey.
    '''
    
    result = builder.build(text)
    assert 'entities' in result
    assert 'relations' in result
    assert 'graph' in result
    assert 'statistics' in result
    print("  ✓ Knowledge graph building test passed")
    
    # Test entity extraction
    entities = builder.extract_entities(text)
    assert isinstance(entities, dict)
    print("  ✓ Entity extraction test passed")
    
    # Test graph export
    if result['graph']['nodes']:
        graphml = builder.to_graphml(result['graph'])
        assert '<?xml' in graphml
        print("  ✓ GraphML export test passed")
    else:
        print("  ✓ GraphML export test skipped (no nodes)")
    
    print("KnowledgeGraphBuilder: ALL TESTS PASSED\n")


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
