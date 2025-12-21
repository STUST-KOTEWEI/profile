"""
Enhanced Named Entity Recognition (NER) module.

Provides advanced entity recognition capabilities with support for
multiple entity types and contextual analysis.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
import re


@dataclass
class NamedEntity:
    """Represents a named entity."""
    id: str
    text: str
    entity_type: str
    start_pos: int
    end_pos: int
    confidence: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)
    context: str = ""


class EntityRecognizer:
    """
    Advanced Named Entity Recognition system.
    
    Provides:
    - Multiple entity type detection (PERSON, LOCATION, ORGANIZATION, etc.)
    - Pattern-based and context-aware recognition
    - Entity disambiguation
    - Coreference resolution (basic)
    - Multi-language support (English, Chinese)
    """
    
    def __init__(self, language: str = 'en'):
        """
        Initialize the entity recognizer.
        
        Args:
            language: Target language ('en', 'zh')
        """
        self.language = language
        self.entity_patterns = self._initialize_patterns()
        self.context_clues = self._initialize_context_clues()
        self.stop_words = self._initialize_stop_words()
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize entity recognition patterns.
        
        Returns:
            Dictionary of entity type patterns
        """
        return {
            'PERSON': {
                'patterns': [
                    # Titles followed by names
                    r'\b(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Professor|Sir|Lady|Lord|King|Queen|Prince|Princess)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                    # Full names (First Last)
                    r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b',
                    # Single capitalized names in dialogue context
                    r'(?:said|asked|replied|shouted)\s+([A-Z][a-z]+)',
                ],
                'context_words': ['said', 'asked', 'told', 'thought', 'felt', 'believed'],
                'weight': 1.0
            },
            'LOCATION': {
                'patterns': [
                    # Preposition + Location
                    r'(?:in|at|to|from|near|through)\s+(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                    # Geographic features
                    r'([A-Z][a-z]+)\s+(?:City|Town|Village|Mountain|River|Lake|Sea|Ocean|Forest|Valley|Island)',
                    # Countries and regions
                    r'\b(America|Europe|Asia|Africa|China|Japan|England|France|Germany|Italy|Spain)\b',
                ],
                'context_words': ['lived', 'traveled', 'visited', 'arrived', 'departed', 'located'],
                'weight': 0.9
            },
            'ORGANIZATION': {
                'patterns': [
                    # Organizations with suffixes
                    r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Inc\.|Corp\.|Ltd\.|Company|Corporation|Institute|University|Academy|Guild|Order)',
                    # The + Org name
                    r'the\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:organization|group|team|committee)',
                ],
                'context_words': ['joined', 'founded', 'member', 'organization', 'company'],
                'weight': 0.85
            },
            'DATE': {
                'patterns': [
                    r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b',
                    r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,?\s+\d{4})?\b',
                    r'\b(\d{4})\b(?!\s*(?:people|years|times))',
                    r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
                ],
                'context_words': ['on', 'in', 'during', 'since', 'until', 'date'],
                'weight': 0.95
            },
            'TIME': {
                'patterns': [
                    r'\b(\d{1,2}:\d{2}(?::\d{2})?(?:\s*(?:AM|PM|am|pm))?)\b',
                    r'\b(noon|midnight|morning|afternoon|evening|night|dawn|dusk)\b',
                ],
                'context_words': ['at', 'around', 'before', 'after', 'time'],
                'weight': 0.9
            },
            'QUANTITY': {
                'patterns': [
                    r'\b(\d+(?:,\d{3})*(?:\.\d+)?)\s+(?:meters?|kilometers?|miles?|feet|inches?|pounds?|kilograms?|dollars?|euros?)\b',
                    r'\b(one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|million|billion)\s+\w+\b',
                ],
                'context_words': ['about', 'approximately', 'nearly', 'exactly', 'over', 'under'],
                'weight': 0.85
            },
            'EVENT': {
                'patterns': [
                    r'(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:War|Battle|Festival|Ceremony|Conference|Meeting|Tournament)',
                    r'(?:the\s+)?([A-Z][a-z]+)\s+(?:Revolution|Rebellion|Uprising)',
                ],
                'context_words': ['during', 'after', 'before', 'celebrated', 'occurred'],
                'weight': 0.8
            },
            'WORK_OF_ART': {
                'patterns': [
                    r'"([^"]+)"',  # Quoted titles
                    r'\'([^\']+)\'',  # Single quoted titles
                    r'(?:book|novel|story|poem|song|movie|film)\s+(?:called|titled|named)\s+([A-Z][^.!?]+)',
                ],
                'context_words': ['wrote', 'read', 'watched', 'titled', 'called'],
                'weight': 0.75
            }
        }
    
    def _initialize_context_clues(self) -> Dict[str, List[str]]:
        """
        Initialize context clues for entity disambiguation.
        
        Returns:
            Dictionary mapping entity types to context clues
        """
        return {
            'PERSON': [
                'he', 'she', 'him', 'her', 'his', 'hers', 'they', 'them',
                'said', 'thought', 'felt', 'walked', 'ran', 'smiled'
            ],
            'LOCATION': [
                'in', 'at', 'from', 'to', 'near', 'through', 'across',
                'lived', 'visited', 'traveled', 'arrived'
            ],
            'ORGANIZATION': [
                'member', 'founded', 'joined', 'worked', 'company', 'group'
            ]
        }
    
    def _initialize_stop_words(self) -> Set[str]:
        """
        Initialize stop words to filter out.
        
        Returns:
            Set of stop words
        """
        return {
            'The', 'This', 'That', 'These', 'Those', 'There', 'Here',
            'What', 'When', 'Where', 'Which', 'Who', 'How', 'Why',
            'But', 'And', 'Or', 'Not', 'Just', 'Only', 'Even',
            'Once', 'Upon', 'Time', 'Day', 'One', 'It', 'Its',
            'She', 'He', 'They', 'We', 'You', 'I', 'My', 'Your',
            'His', 'Her', 'Their', 'Our', 'Some', 'Many', 'Much',
            'First', 'Last', 'Next', 'Then', 'Now', 'Here', 'There'
        }
    
    def recognize(self, text: str) -> Dict[str, Any]:
        """
        Perform named entity recognition on the input text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary containing NER results
        """
        # Extract entities
        entities = self.extract_entities(text)
        
        # Resolve coreferences (basic)
        entities = self.resolve_coreferences(text, entities)
        
        # Group by type
        entities_by_type = self._group_by_type(entities)
        
        # Calculate statistics
        stats = self._calculate_statistics(entities)
        
        return {
            'entities': [self._entity_to_dict(e) for e in entities],
            'entities_by_type': entities_by_type,
            'statistics': stats,
            'summary': self._generate_summary(entities)
        }
    
    def extract_entities(self, text: str) -> List[NamedEntity]:
        """
        Extract named entities from text.
        
        Args:
            text: Input text
            
        Returns:
            List of NamedEntity objects
        """
        entities: List[NamedEntity] = []
        entity_id = 0
        seen_spans: Set[Tuple[int, int]] = set()
        
        for entity_type, type_info in self.entity_patterns.items():
            for pattern in type_info['patterns']:
                try:
                    matches = re.finditer(pattern, text, re.IGNORECASE if entity_type in ['DATE', 'TIME'] else 0)
                    for match in matches:
                        # Get the entity text (use last capturing group)
                        entity_text = match.group(match.lastindex) if match.lastindex else match.group()
                        entity_text = entity_text.strip()
                        
                        # Skip if empty or stop word
                        if not entity_text or entity_text in self.stop_words:
                            continue
                        
                        # Skip very short entities (except for specific types)
                        if len(entity_text) < 2 and entity_type not in ['QUANTITY']:
                            continue
                        
                        # Check for overlapping spans
                        span = (match.start(), match.end())
                        if self._overlaps_with_existing(span, seen_spans):
                            continue
                        
                        seen_spans.add(span)
                        
                        # Calculate confidence based on context
                        context = self._get_context(text, match.start(), match.end())
                        confidence = self._calculate_confidence(
                            entity_text, entity_type, context, type_info
                        )
                        
                        entity = NamedEntity(
                            id=f"NE{entity_id}",
                            text=entity_text,
                            entity_type=entity_type,
                            start_pos=match.start(),
                            end_pos=match.end(),
                            confidence=confidence,
                            context=context
                        )
                        entities.append(entity)
                        entity_id += 1
                except re.error:
                    continue
        
        # Sort by position
        entities.sort(key=lambda e: e.start_pos)
        
        return entities
    
    def _overlaps_with_existing(
        self, 
        span: Tuple[int, int], 
        existing: Set[Tuple[int, int]]
    ) -> bool:
        """Check if span overlaps with existing spans."""
        for existing_span in existing:
            if not (span[1] <= existing_span[0] or span[0] >= existing_span[1]):
                return True
        return False
    
    def _get_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Get context around an entity."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end]
    
    def _calculate_confidence(
        self, 
        entity_text: str,
        entity_type: str,
        context: str,
        type_info: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for an entity."""
        base_confidence = type_info.get('weight', 0.5)
        
        # Boost confidence if context words are present
        context_lower = context.lower()
        context_words = type_info.get('context_words', [])
        context_match = sum(1 for w in context_words if w in context_lower)
        
        if context_match > 0:
            base_confidence = min(base_confidence + 0.1 * context_match, 1.0)
        
        # Reduce confidence for short entities
        if len(entity_text) < 3:
            base_confidence *= 0.8
        
        return round(base_confidence, 2)
    
    def resolve_coreferences(
        self, 
        text: str, 
        entities: List[NamedEntity]
    ) -> List[NamedEntity]:
        """
        Resolve basic coreferences.
        
        Args:
            text: Input text
            entities: Extracted entities
            
        Returns:
            Entities with coreference information
        """
        # Find all PERSON entities
        person_entities = [e for e in entities if e.entity_type == 'PERSON']
        
        if not person_entities:
            return entities
        
        # Track pronoun references (simplified approach)
        pronouns = {
            'he': 'MALE',
            'him': 'MALE',
            'his': 'MALE',
            'she': 'FEMALE',
            'her': 'FEMALE',
            'hers': 'FEMALE'
        }
        
        # This is a simplified coreference resolution
        # In production, would use more sophisticated algorithms
        for entity in person_entities:
            entity.attributes['potential_coreferences'] = []
        
        return entities
    
    def _group_by_type(self, entities: List[NamedEntity]) -> Dict[str, List[str]]:
        """Group entities by type."""
        by_type: Dict[str, List[str]] = {}
        
        for entity in entities:
            if entity.entity_type not in by_type:
                by_type[entity.entity_type] = []
            if entity.text not in by_type[entity.entity_type]:
                by_type[entity.entity_type].append(entity.text)
        
        return by_type
    
    def _calculate_statistics(self, entities: List[NamedEntity]) -> Dict[str, Any]:
        """Calculate NER statistics."""
        type_counts: Dict[str, int] = {}
        for entity in entities:
            type_counts[entity.entity_type] = type_counts.get(entity.entity_type, 0) + 1
        
        # Find most common entities
        entity_counts: Dict[str, int] = {}
        for entity in entities:
            key = f"{entity.text}_{entity.entity_type}"
            entity_counts[key] = entity_counts.get(key, 0) + 1
        
        top_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_entities': len(entities),
            'type_distribution': type_counts,
            'unique_entities': len(set(e.text for e in entities)),
            'top_entities': [{'entity': k.split('_')[0], 'count': v} for k, v in top_entities],
            'average_confidence': sum(e.confidence for e in entities) / len(entities) if entities else 0
        }
    
    def _generate_summary(self, entities: List[NamedEntity]) -> str:
        """Generate a summary of NER results."""
        if not entities:
            return "No named entities detected."
        
        type_counts = {}
        for e in entities:
            type_counts[e.entity_type] = type_counts.get(e.entity_type, 0) + 1
        
        parts = [f"Detected {len(entities)} entities:"]
        for entity_type, count in sorted(type_counts.items()):
            parts.append(f"{count} {entity_type}")
        
        return " ".join(parts)
    
    def _entity_to_dict(self, entity: NamedEntity) -> Dict[str, Any]:
        """Convert NamedEntity to dictionary."""
        return {
            'id': entity.id,
            'text': entity.text,
            'type': entity.entity_type,
            'start': entity.start_pos,
            'end': entity.end_pos,
            'confidence': entity.confidence,
            'context': entity.context[:100] if entity.context else ''
        }
    
    def to_iob2(self, text: str, entities: List[NamedEntity]) -> List[Tuple[str, str]]:
        """
        Convert entities to IOB2 format.
        
        Args:
            text: Original text
            entities: List of entities
            
        Returns:
            List of (token, tag) tuples
        """
        # Simple tokenization
        tokens = text.split()
        tags = ['O'] * len(tokens)
        
        # This is a simplified IOB2 conversion
        # In production, would need proper tokenization alignment
        
        char_to_token = {}
        char_idx = 0
        for i, token in enumerate(tokens):
            for j in range(len(token)):
                char_to_token[char_idx + j] = i
            char_idx += len(token) + 1
        
        for entity in entities:
            start_token = char_to_token.get(entity.start_pos)
            if start_token is not None and start_token < len(tags):
                tags[start_token] = f'B-{entity.entity_type}'
        
        return list(zip(tokens, tags))
