"""
Timeline Tracker module for narrative analysis.

Provides capabilities to extract, track, and visualize temporal events
and sequences within narrative text.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class TimelineEvent:
    """Represents an event in the timeline."""
    id: str
    description: str
    temporal_marker: str
    event_type: str
    position_in_text: int
    relative_order: int
    characters_involved: List[str] = field(default_factory=list)
    location: Optional[str] = None
    duration: Optional[str] = None
    certainty: float = 1.0


class TimelineTracker:
    """
    Tracks and analyzes temporal events and sequences in narrative text.
    
    Provides:
    - Temporal marker detection
    - Event extraction and ordering
    - Timeline construction
    - Sequence analysis
    - Duration estimation
    """
    
    def __init__(self):
        """Initialize the timeline tracker."""
        self.temporal_patterns = self._initialize_temporal_patterns()
        self.sequence_markers = self._initialize_sequence_markers()
        self.duration_patterns = self._initialize_duration_patterns()
    
    def _initialize_temporal_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize temporal detection patterns.
        
        Returns:
            Dictionary of temporal pattern categories
        """
        return {
            'absolute': {
                'patterns': [
                    # Year pattern with context - avoid matching standalone numbers
                    r'\b(?:in|year|circa|around)\s+(\d{4})\b',
                    r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,?\s+\d{4})?\b',
                    r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # Date format
                    r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
                ],
                'type': 'absolute'
            },
            'relative_past': {
                'patterns': [
                    r'\b(yesterday|last\s+(?:night|week|month|year))\b',
                    r'\b(\d+\s+(?:days?|weeks?|months?|years?)\s+ago)\b',
                    r'\b(previously|earlier|before|once|formerly)\b',
                    r'\b(in\s+the\s+past|back\s+then|long\s+ago)\b',
                ],
                'type': 'relative_past'
            },
            'relative_present': {
                'patterns': [
                    r'\b(now|today|currently|at\s+(?:the\s+)?(?:moment|present))\b',
                    r'\b(right\s+now|this\s+(?:moment|instant))\b',
                    r'\b(nowadays|these\s+days)\b',
                ],
                'type': 'relative_present'
            },
            'relative_future': {
                'patterns': [
                    r'\b(tomorrow|next\s+(?:day|week|month|year))\b',
                    r'\b(in\s+\d+\s+(?:days?|weeks?|months?|years?))\b',
                    r'\b(soon|later|eventually|someday)\b',
                    r'\b(in\s+the\s+future|from\s+now\s+on)\b',
                ],
                'type': 'relative_future'
            },
            'time_of_day': {
                'patterns': [
                    r'\b(morning|noon|afternoon|evening|night|midnight|dawn|dusk)\b',
                    r'\b(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?)\b',
                    r'\b(sunrise|sunset)\b',
                ],
                'type': 'time_of_day'
            },
            'seasons': {
                'patterns': [
                    r'\b(spring|summer|autumn|fall|winter)\b',
                    r'\b(rainy\s+season|dry\s+season)\b',
                ],
                'type': 'season'
            }
        }
    
    def _initialize_sequence_markers(self) -> Dict[str, List[str]]:
        """
        Initialize sequence/order markers.
        
        Returns:
            Dictionary of sequence marker types
        """
        return {
            'beginning': [
                'first', 'initially', 'at first', 'in the beginning',
                'to begin with', 'at the start', 'once upon a time'
            ],
            'continuation': [
                'then', 'next', 'after that', 'afterwards', 'subsequently',
                'following that', 'later', 'soon after', 'meanwhile'
            ],
            'ending': [
                'finally', 'at last', 'in the end', 'eventually',
                'ultimately', 'lastly', 'in conclusion'
            ],
            'simultaneous': [
                'meanwhile', 'at the same time', 'simultaneously',
                'while', 'during', 'as', 'when'
            ],
            'flashback': [
                'had', 'had been', 'used to', 'would often',
                'remembered', 'recalled', 'thought back'
            ]
        }
    
    def _initialize_duration_patterns(self) -> List[str]:
        """
        Initialize duration detection patterns.
        
        Returns:
            List of duration patterns
        """
        return [
            r'for\s+(\d+\s+(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?))',
            r'(\d+\s+(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?))\s+(?:long|later)',
            r'(?:lasted|continued|went on)\s+(?:for\s+)?(\d+\s+\w+)',
            r'(a\s+(?:few|couple\s+of)\s+(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?))',
            r'(brief(?:ly)?|moment(?:arily)?|instant(?:ly)?)',
            r'(all\s+(?:day|night|week|month|year)\s+long)',
        ]
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive timeline analysis on the input text.
        
        Args:
            text: Input narrative text
            
        Returns:
            Dictionary containing timeline analysis results
        """
        # Extract temporal markers
        temporal_markers = self.extract_temporal_markers(text)
        
        # Extract events with temporal context
        events = self.extract_events(text, temporal_markers)
        
        # Build timeline
        timeline = self.build_timeline(events)
        
        # Analyze narrative time structure
        time_structure = self.analyze_time_structure(text, events)
        
        # Calculate statistics
        stats = self.calculate_statistics(temporal_markers, events)
        
        return {
            'temporal_markers': temporal_markers,
            'events': [self._event_to_dict(e) for e in events],
            'timeline': timeline,
            'time_structure': time_structure,
            'statistics': stats,
            'summary': self._generate_summary(temporal_markers, events, time_structure)
        }
    
    def extract_temporal_markers(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all temporal markers from text.
        
        Args:
            text: Input text
            
        Returns:
            List of temporal markers with metadata
        """
        markers = []
        text_lower = text.lower()
        
        for category, info in self.temporal_patterns.items():
            for pattern in info['patterns']:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    markers.append({
                        'text': match.group(),
                        'category': category,
                        'type': info['type'],
                        'position': match.start(),
                        'end_position': match.end()
                    })
        
        # Sort by position
        markers.sort(key=lambda x: x['position'])
        
        return markers
    
    def extract_events(
        self, 
        text: str, 
        temporal_markers: List[Dict[str, Any]]
    ) -> List[TimelineEvent]:
        """
        Extract events based on temporal markers and context.
        
        Args:
            text: Input text
            temporal_markers: Extracted temporal markers
            
        Returns:
            List of TimelineEvent objects
        """
        events = []
        sentences = self._split_into_sentences(text)
        
        event_id = 0
        for i, sentence in enumerate(sentences):
            # Check if sentence contains a temporal marker
            sentence_markers = [
                m for m in temporal_markers 
                if self._marker_in_text(m['text'], sentence.lower())
            ]
            
            if sentence_markers or self._has_sequence_marker(sentence):
                # Extract characters mentioned
                characters = self._extract_characters(sentence)
                
                # Detect event type
                event_type = self._detect_event_type(sentence)
                
                # Get the primary temporal marker
                primary_marker = sentence_markers[0]['text'] if sentence_markers else ''
                marker_type = sentence_markers[0]['category'] if sentence_markers else 'sequence'
                
                event = TimelineEvent(
                    id=f"E{event_id}",
                    description=sentence.strip(),
                    temporal_marker=primary_marker,
                    event_type=event_type,
                    position_in_text=i,
                    relative_order=event_id,
                    characters_involved=characters,
                    certainty=0.8 if sentence_markers else 0.5
                )
                events.append(event)
                event_id += 1
        
        return events
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _marker_in_text(self, marker: str, text: str) -> bool:
        """Check if marker is in text."""
        return marker.lower() in text.lower()
    
    def _has_sequence_marker(self, sentence: str) -> bool:
        """Check if sentence has sequence markers."""
        sentence_lower = sentence.lower()
        for markers in self.sequence_markers.values():
            for marker in markers:
                if marker in sentence_lower:
                    return True
        return False
    
    def _extract_characters(self, sentence: str) -> List[str]:
        """Extract character names from sentence."""
        # Find capitalized words (potential names)
        words = re.findall(r'\b([A-Z][a-z]+)\b', sentence)
        # Filter common words
        skip_words = {'The', 'This', 'That', 'There', 'Here', 'When', 'Where', 'What', 'How', 'Why'}
        return [w for w in words if w not in skip_words]
    
    def _detect_event_type(self, sentence: str) -> str:
        """Detect the type of event."""
        sentence_lower = sentence.lower()
        
        event_indicators = {
            'action': ['went', 'came', 'ran', 'walked', 'jumped', 'fought', 'escaped'],
            'dialogue': ['said', 'asked', 'replied', 'shouted', 'whispered', 'told'],
            'discovery': ['found', 'discovered', 'realized', 'noticed', 'saw', 'learned'],
            'transformation': ['became', 'changed', 'transformed', 'turned into'],
            'meeting': ['met', 'encountered', 'introduced', 'greeted'],
            'departure': ['left', 'departed', 'went away', 'said goodbye'],
            'conflict': ['fought', 'argued', 'battled', 'confronted'],
            'resolution': ['resolved', 'solved', 'fixed', 'ended', 'concluded']
        }
        
        for event_type, indicators in event_indicators.items():
            for indicator in indicators:
                if indicator in sentence_lower:
                    return event_type
        
        return 'general'
    
    def build_timeline(self, events: List[TimelineEvent]) -> Dict[str, Any]:
        """
        Build a structured timeline from events.
        
        Args:
            events: List of extracted events
            
        Returns:
            Timeline structure
        """
        if not events:
            return {
                'phases': [],
                'event_sequence': [],
                'duration_estimate': 'unknown'
            }
        
        # Group events into phases
        phases = self._group_into_phases(events)
        
        # Create event sequence
        event_sequence = [
            {
                'order': e.relative_order,
                'id': e.id,
                'description': e.description[:100] + '...' if len(e.description) > 100 else e.description,
                'marker': e.temporal_marker
            }
            for e in events
        ]
        
        return {
            'phases': phases,
            'event_sequence': event_sequence,
            'total_events': len(events),
            'duration_estimate': self._estimate_duration(events)
        }
    
    def _group_into_phases(self, events: List[TimelineEvent]) -> List[Dict[str, Any]]:
        """Group events into narrative phases."""
        if not events:
            return []
        
        # Simple phase grouping: beginning, middle, end
        n = len(events)
        if n <= 3:
            return [{'phase': 'main', 'events': [e.id for e in events]}]
        
        third = n // 3
        return [
            {'phase': 'beginning', 'events': [e.id for e in events[:third]]},
            {'phase': 'middle', 'events': [e.id for e in events[third:2*third]]},
            {'phase': 'ending', 'events': [e.id for e in events[2*third:]]}
        ]
    
    def _estimate_duration(self, events: List[TimelineEvent]) -> str:
        """Estimate the duration of the narrative."""
        if not events:
            return 'unknown'
        
        # Check temporal markers for duration hints
        markers = [e.temporal_marker.lower() for e in events if e.temporal_marker]
        
        if any('year' in m for m in markers):
            return 'years'
        elif any('month' in m for m in markers):
            return 'months'
        elif any('week' in m for m in markers):
            return 'weeks'
        elif any('day' in m or 'morning' in m or 'night' in m for m in markers):
            return 'days'
        elif any('hour' in m for m in markers):
            return 'hours'
        
        return 'unspecified'
    
    def analyze_time_structure(
        self, 
        text: str, 
        events: List[TimelineEvent]
    ) -> Dict[str, Any]:
        """
        Analyze the narrative's time structure.
        
        Args:
            text: Input text
            events: Extracted events
            
        Returns:
            Time structure analysis
        """
        text_lower = text.lower()
        
        # Detect narrative perspective
        has_flashback = any(
            marker in text_lower 
            for marker in self.sequence_markers.get('flashback', [])
        )
        
        # Check for non-linear narrative
        has_future_reference = any(
            marker in text_lower 
            for marker in ['will', 'would', 'going to', 'foreshadow']
        )
        
        # Determine narrative type
        if has_flashback and has_future_reference:
            narrative_type = 'non-linear'
        elif has_flashback:
            narrative_type = 'flashback'
        elif has_future_reference:
            narrative_type = 'flash-forward'
        else:
            narrative_type = 'linear'
        
        # Analyze pacing
        pacing = self._analyze_pacing(events)
        
        return {
            'narrative_type': narrative_type,
            'has_flashback': has_flashback,
            'has_flash_forward': has_future_reference,
            'pacing': pacing,
            'time_span': self._estimate_duration(events)
        }
    
    def _analyze_pacing(self, events: List[TimelineEvent]) -> str:
        """Analyze the pacing of events."""
        if len(events) < 3:
            return 'brief'
        
        # Check event density
        event_types = [e.event_type for e in events]
        action_count = sum(1 for t in event_types if t in ['action', 'conflict', 'transformation'])
        
        if action_count / len(events) > 0.5:
            return 'fast-paced'
        elif action_count / len(events) < 0.2:
            return 'slow-paced'
        else:
            return 'moderate'
    
    def calculate_statistics(
        self, 
        temporal_markers: List[Dict[str, Any]], 
        events: List[TimelineEvent]
    ) -> Dict[str, Any]:
        """
        Calculate timeline statistics.
        
        Args:
            temporal_markers: Extracted markers
            events: Extracted events
            
        Returns:
            Statistics dictionary
        """
        # Count marker types
        marker_types: Dict[str, int] = {}
        for marker in temporal_markers:
            marker_type = marker['category']
            marker_types[marker_type] = marker_types.get(marker_type, 0) + 1
        
        # Count event types
        event_types: Dict[str, int] = {}
        for event in events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
        
        return {
            'total_temporal_markers': len(temporal_markers),
            'total_events': len(events),
            'marker_types': marker_types,
            'event_types': event_types,
            'average_certainty': sum(e.certainty for e in events) / len(events) if events else 0
        }
    
    def _generate_summary(
        self, 
        markers: List[Dict[str, Any]], 
        events: List[TimelineEvent],
        time_structure: Dict[str, Any]
    ) -> str:
        """Generate a summary of the timeline analysis."""
        if not events:
            return "No significant temporal events detected."
        
        parts = [
            f"Detected {len(events)} events",
            f"with {len(markers)} temporal markers.",
            f"Narrative type: {time_structure['narrative_type']}.",
            f"Pacing: {time_structure['pacing']}."
        ]
        
        return " ".join(parts)
    
    def _event_to_dict(self, event: TimelineEvent) -> Dict[str, Any]:
        """Convert TimelineEvent to dictionary."""
        return {
            'id': event.id,
            'description': event.description,
            'temporal_marker': event.temporal_marker,
            'event_type': event.event_type,
            'position': event.position_in_text,
            'order': event.relative_order,
            'characters': event.characters_involved,
            'location': event.location,
            'certainty': event.certainty
        }
    
    def to_mermaid(self, events: List[TimelineEvent]) -> str:
        """
        Convert timeline to Mermaid diagram format.
        
        Args:
            events: List of events
            
        Returns:
            Mermaid diagram string
        """
        if not events:
            return "gantt\n    title Empty Timeline\n"
        
        lines = [
            "gantt",
            "    title Narrative Timeline",
            "    dateFormat X",
            "    axisFormat %s",
            "    section Events"
        ]
        
        for i, event in enumerate(events):
            # Truncate description for display
            desc = event.description[:30].replace('"', "'").replace(':', '-')
            # Use relative ordering instead of hardcoded dates
            # Each event takes 1 unit of time in sequence
            marker = event.temporal_marker if event.temporal_marker else f"Event {i+1}"
            lines.append(f"    {desc} ({marker}) :e{i}, {i}, 1")
        
        return "\n".join(lines)
