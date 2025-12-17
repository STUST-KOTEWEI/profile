"""
Example usage of the Deep Semantic Analysis Module.

This script demonstrates how to use the semantic analysis module
for analyzing narrative text.
"""

import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from semantic_analysis import SemanticAnalyzer


def main():
    """Run example analysis on sample narrative text."""
    
    # Initialize the semantic analyzer
    print("Initializing Semantic Analyzer...")
    analyzer = SemanticAnalyzer()
    
    # Sample narrative text
    sample_text = """
    Once upon a time in a small village, there lived a young girl named Alice.
    She was a curious and adventurous soul, always seeking new mysteries to solve.
    One day, Alice met an old mentor named Professor Brown who taught her about
    the ancient secrets of the forest. Together, they embarked on a journey to
    discover the hidden treasure. Their friendship grew stronger as they faced
    numerous challenges. Alice felt excited and hopeful about their quest, while
    Professor Brown remained serious and focused on their mission.
    """
    
    print("\n" + "="*80)
    print("ANALYZING SAMPLE NARRATIVE TEXT")
    print("="*80)
    print(f"\nText:\n{sample_text}\n")
    
    # Perform comprehensive analysis
    print("Performing analysis...")
    results = analyzer.analyze(sample_text)
    
    # Display results
    print("\n" + "-"*80)
    print("ANALYSIS RESULTS")
    print("-"*80)
    
    # Semantic Units
    print("\n1. SEMANTIC UNITS:")
    for unit in results['semantic_units']:
        print(f"   [{unit['id']}] {unit['text'][:60]}... ({unit['length']} words)")
    
    # Sentiment Analysis
    print("\n2. SENTIMENT ANALYSIS:")
    sentiment = results['sentiment']
    print(f"   Label: {sentiment['label']}")
    print(f"   Confidence: {sentiment['score']:.2f}")
    print(f"   Emotions:")
    for emotion, score in sentiment['emotions'].items():
        if score > 0:
            print(f"      - {emotion}: {score:.2f}")
    
    # Tone Analysis
    print("\n3. TONE ANALYSIS:")
    tone = results['tone']
    print(f"   Primary Tone: {tone['primary_tone']}")
    print(f"   Mood: {tone['mood']}")
    print(f"   Intensity: {tone['intensity']:.2f}")
    print(f"   Tone Scores:")
    for tone_type, score in tone['tone_scores'].items():
        if score > 0:
            print(f"      - {tone_type}: {score:.2f}")
    
    # Relationship Analysis
    print("\n4. CHARACTER RELATIONSHIPS:")
    relationships = results['relationships']
    print(f"   Characters: {', '.join(relationships['characters'])}")
    print(f"   Relationship Summary: {relationships['interaction_summary']}")
    if relationships['relationships']:
        print(f"   Detected Relationships:")
        for rel in relationships['relationships'][:5]:  # Show first 5
            print(f"      - {rel['character1']} <-> {rel['character2']} ({rel['type']})")
    
    # Context Analysis
    print("\n5. STORY CONTEXT:")
    context = results['context']
    print(f"   Temporal: {context['temporal_context']['primary_period']}")
    print(f"   Spatial: {context['spatial_context']['primary_setting']}")
    print(f"   Setting: {context['setting_description']}")
    if context['themes']:
        print(f"   Themes:")
        for theme, score in context['themes'].items():
            print(f"      - {theme}: {score:.2f}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
