"""
Character relationship extraction module.
"""

from typing import Dict, List, Any
import re


class RelationshipExtractor:
    """
    Extracts and analyzes character relationships from narrative text.
    
    Identifies characters, their interactions, and the nature of their relationships.
    """
    
    def __init__(self):
        """Initialize the relationship extractor."""
        self.relationship_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """
        Initialize relationship detection patterns.
        
        Returns:
            Dictionary mapping relationship types to indicator patterns
        """
        return {
            'family': ['mother', 'father', 'sister', 'brother', 'parent', 'child', 
                      'son', 'daughter', 'family', 'relative'],
            'friendship': ['friend', 'companion', 'buddy', 'pal', 'ally'],
            'romantic': ['love', 'lover', 'partner', 'beloved', 'romance', 'kiss'],
            'professional': ['colleague', 'coworker', 'boss', 'employee', 'partner'],
            'antagonistic': ['enemy', 'rival', 'opponent', 'adversary', 'foe'],
            'mentor': ['teacher', 'mentor', 'guide', 'master', 'instructor']
        }
    
    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extract character relationships from text.
        
        Args:
            text: Input narrative text
            
        Returns:
            Dictionary containing:
            - characters: List of detected character names
            - relationships: List of relationship tuples
            - relationship_types: Count of each relationship type
            - interaction_summary: Summary of character interactions
        """
        characters = self._extract_characters(text)
        relationships = self._detect_relationships(text, characters)
        relationship_types = self._count_relationship_types(relationships)
        
        return {
            'characters': characters,
            'relationships': relationships,
            'relationship_types': relationship_types,
            'interaction_summary': self._summarize_interactions(relationships)
        }
    
    def _extract_characters(self, text: str) -> List[str]:
        """
        Extract potential character names from text.
        
        Args:
            text: Input text
            
        Returns:
            List of character names
        """
        # Simple extraction: capitalized words that appear multiple times
        # In a production system, would use NER (Named Entity Recognition)
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        # Count occurrences
        character_counts = {}
        for word in words:
            if len(word) > 2:  # Filter short words
                character_counts[word] = character_counts.get(word, 0) + 1
        
        # Return names that appear more than once (likely characters)
        characters = [name for name, count in character_counts.items() if count > 1]
        return characters[:10]  # Limit to top 10
    
    def _detect_relationships(self, text: str, characters: List[str]) -> List[Dict[str, Any]]:
        """
        Detect relationships between characters.
        
        Args:
            text: Input text
            characters: List of character names
            
        Returns:
            List of relationship dictionaries
        """
        relationships = []
        text_lower = text.lower()
        
        # Look for relationship indicators
        for rel_type, keywords in self.relationship_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Find nearby characters
                    pattern = r'\b[A-Z][a-z]+\b'
                    matches = list(re.finditer(pattern, text))
                    keyword_pos = text_lower.find(keyword)
                    
                    # Find characters near the relationship keyword
                    nearby_chars = []
                    for match in matches:
                        if abs(match.start() - keyword_pos) < 100:  # Within 100 chars
                            char_name = match.group()
                            if char_name in characters:
                                nearby_chars.append(char_name)
                    
                    # Create relationships for nearby character pairs
                    if len(nearby_chars) >= 2:
                        relationships.append({
                            'character1': nearby_chars[0],
                            'character2': nearby_chars[1],
                            'type': rel_type,
                            'indicator': keyword
                        })
        
        return relationships
    
    def _count_relationship_types(self, relationships: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Count occurrences of each relationship type.
        
        Args:
            relationships: List of detected relationships
            
        Returns:
            Dictionary mapping relationship types to counts
        """
        counts = {}
        for rel in relationships:
            rel_type = rel['type']
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts
    
    def _summarize_interactions(self, relationships: List[Dict[str, Any]]) -> str:
        """
        Create a summary of character interactions.
        
        Args:
            relationships: List of detected relationships
            
        Returns:
            Human-readable summary
        """
        if not relationships:
            return "No significant character relationships detected."
        
        unique_chars = set()
        for rel in relationships:
            unique_chars.add(rel['character1'])
            unique_chars.add(rel['character2'])
        
        summary = f"Detected {len(unique_chars)} characters with {len(relationships)} relationships. "
        
        # Most common relationship type
        type_counts = self._count_relationship_types(relationships)
        if type_counts:
            most_common = max(type_counts, key=type_counts.get)
            summary += f"Primary relationship type: {most_common}."
        
        return summary
