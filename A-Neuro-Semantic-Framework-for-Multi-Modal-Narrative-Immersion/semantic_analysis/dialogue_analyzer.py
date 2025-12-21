"""
Dialogue Analysis module for narrative text.

Provides capabilities to detect, extract, and analyze dialogue/conversations
within narrative text, including speaker identification and turn-taking analysis.
"""

from typing import Dict, List, Any, Optional, Tuple
import re


class DialogueAnalyzer:
    """
    Analyzes dialogue and conversations in narrative text.
    
    Provides:
    - Dialogue detection and extraction
    - Speaker identification
    - Turn-taking analysis
    - Dialogue sentiment analysis
    - Conversation flow analysis
    """
    
    def __init__(self):
        """Initialize the dialogue analyzer."""
        self.dialogue_patterns = self._initialize_patterns()
        self.speech_verbs = self._initialize_speech_verbs()
    
    def _initialize_patterns(self) -> Dict[str, Any]:
        """
        Initialize dialogue detection patterns.
        
        Returns:
            Dictionary of regex patterns for dialogue detection
        """
        return {
            # English dialogue patterns
            'double_quotes': r'"([^"]*)"',
            'single_quotes': r"'([^']*)'",
            # Chinese dialogue patterns
            'chinese_quotes': r'「([^」]*)」|『([^』]*)』|"([^"]*)"',
            # Japanese dialogue patterns
            'japanese_quotes': r'「([^」]*)」|『([^』]*)』',
            # Speaker attribution patterns
            'speaker_said': r'(\w+)\s+(?:said|says|asked|replied|whispered|shouted|exclaimed)',
            'said_speaker': r'(?:said|says|asked|replied|whispered|shouted|exclaimed)\s+(\w+)',
        }
    
    def _initialize_speech_verbs(self) -> Dict[str, List[str]]:
        """
        Initialize speech verbs for multiple languages.
        
        Returns:
            Dictionary of speech verbs by language
        """
        return {
            'en': [
                'said', 'says', 'asked', 'replied', 'answered', 'whispered',
                'shouted', 'exclaimed', 'muttered', 'yelled', 'screamed',
                'wondered', 'questioned', 'stated', 'declared', 'announced'
            ],
            'zh': [
                '說', '問', '回答', '喊', '叫', '低聲說', '大叫',
                '驚呼', '嘟囔', '宣布', '聲明', '回應'
            ],
            'ja': [
                '言った', '聞いた', '答えた', '叫んだ', 'つぶやいた',
                '尋ねた', '返事した', '話した'
            ]
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive dialogue analysis on the input text.
        
        Args:
            text: Input narrative text
            
        Returns:
            Dictionary containing dialogue analysis results
        """
        # Extract all dialogue segments
        dialogues = self.extract_dialogues(text)
        
        # Identify speakers
        speakers = self.identify_speakers(text, dialogues)
        
        # Analyze conversation flow
        flow = self.analyze_conversation_flow(dialogues, speakers)
        
        # Calculate dialogue statistics
        stats = self.calculate_statistics(text, dialogues)
        
        return {
            'dialogues': dialogues,
            'speakers': speakers,
            'conversation_flow': flow,
            'statistics': stats,
            'summary': self._generate_summary(dialogues, speakers, stats)
        }
    
    def extract_dialogues(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract dialogue segments from text.
        
        Args:
            text: Input text
            
        Returns:
            List of dialogue segments with metadata
        """
        dialogues = []
        dialogue_id = 0
        
        # Try different quote patterns
        for pattern_name, pattern in self.dialogue_patterns.items():
            if 'speaker' in pattern_name:
                continue  # Skip speaker patterns
            
            matches = re.finditer(pattern, text)
            for match in matches:
                # Get the matched dialogue content
                content = None
                for group in match.groups():
                    if group:
                        content = group
                        break
                
                if content and content.strip():
                    dialogue = {
                        'id': dialogue_id,
                        'content': content.strip(),
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                        'pattern_type': pattern_name,
                        'full_match': match.group()
                    }
                    dialogues.append(dialogue)
                    dialogue_id += 1
        
        # Sort by position in text
        dialogues.sort(key=lambda x: x['start_pos'])
        
        # Re-assign IDs after sorting
        for i, d in enumerate(dialogues):
            d['id'] = i
        
        return dialogues
    
    def identify_speakers(self, text: str, dialogues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify speakers for each dialogue segment.
        
        Args:
            text: Full text
            dialogues: List of extracted dialogues
            
        Returns:
            Dictionary mapping dialogue IDs to identified speakers
        """
        speaker_map = {}
        all_speakers = set()
        
        for dialogue in dialogues:
            speaker = self._find_speaker_for_dialogue(text, dialogue)
            speaker_map[dialogue['id']] = speaker
            if speaker and speaker != 'Unknown':
                all_speakers.add(speaker)
        
        return {
            'speaker_map': speaker_map,
            'unique_speakers': list(all_speakers),
            'speaker_count': len(all_speakers)
        }
    
    def _find_speaker_for_dialogue(self, text: str, dialogue: Dict[str, Any]) -> Optional[str]:
        """
        Find the speaker for a specific dialogue segment.
        
        Args:
            text: Full text
            dialogue: Dialogue segment
            
        Returns:
            Identified speaker name or None
        """
        # Get context around the dialogue
        start = max(0, dialogue['start_pos'] - 100)
        end = min(len(text), dialogue['end_pos'] + 100)
        context = text[start:end]
        
        # Try to find speaker attribution
        # Pattern: "Speaker said" before dialogue
        for pattern in [self.dialogue_patterns['speaker_said'], self.dialogue_patterns['said_speaker']]:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        # Look for capitalized words (potential names) near the dialogue
        words = re.findall(r'\b([A-Z][a-z]+)\b', context)
        if words:
            # Return the first capitalized word that's not a common word
            common_words = {'The', 'This', 'That', 'These', 'Those', 'What', 'When', 'Where', 'Who', 'How', 'Why'}
            for word in words:
                if word not in common_words:
                    return word
        
        return 'Unknown'
    
    def analyze_conversation_flow(
        self, 
        dialogues: List[Dict[str, Any]], 
        speakers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze the flow of conversation.
        
        Args:
            dialogues: List of dialogues
            speakers: Speaker identification results
            
        Returns:
            Conversation flow analysis
        """
        if not dialogues:
            return {
                'turns': [],
                'turn_count': 0,
                'average_turn_length': 0
            }
        
        turns = []
        speaker_map = speakers.get('speaker_map', {})
        
        for dialogue in dialogues:
            turn = {
                'dialogue_id': dialogue['id'],
                'speaker': speaker_map.get(dialogue['id'], 'Unknown'),
                'content': dialogue['content'],
                'word_count': len(dialogue['content'].split())
            }
            turns.append(turn)
        
        # Calculate average turn length
        total_words = sum(t['word_count'] for t in turns)
        avg_length = total_words / len(turns) if turns else 0
        
        # Detect turn-taking patterns
        speaker_sequence = [t['speaker'] for t in turns]
        
        return {
            'turns': turns,
            'turn_count': len(turns),
            'average_turn_length': avg_length,
            'speaker_sequence': speaker_sequence
        }
    
    def calculate_statistics(
        self, 
        text: str, 
        dialogues: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate dialogue statistics.
        
        Args:
            text: Full text
            dialogues: List of dialogues
            
        Returns:
            Dialogue statistics
        """
        total_text_length = len(text)
        
        if not dialogues:
            return {
                'dialogue_count': 0,
                'dialogue_percentage': 0.0,
                'average_dialogue_length': 0,
                'longest_dialogue': None,
                'shortest_dialogue': None
            }
        
        dialogue_lengths = [len(d['content']) for d in dialogues]
        total_dialogue_length = sum(dialogue_lengths)
        
        return {
            'dialogue_count': len(dialogues),
            'dialogue_percentage': (total_dialogue_length / total_text_length * 100) if total_text_length > 0 else 0,
            'average_dialogue_length': sum(dialogue_lengths) / len(dialogue_lengths),
            'longest_dialogue': max(dialogues, key=lambda x: len(x['content']))['content'][:100] + '...' if dialogues else None,
            'shortest_dialogue': min(dialogues, key=lambda x: len(x['content']))['content'] if dialogues else None,
            'total_dialogue_characters': total_dialogue_length
        }
    
    def _generate_summary(
        self, 
        dialogues: List[Dict[str, Any]], 
        speakers: Dict[str, Any],
        stats: Dict[str, Any]
    ) -> str:
        """
        Generate a summary of the dialogue analysis.
        
        Args:
            dialogues: List of dialogues
            speakers: Speaker information
            stats: Statistics
            
        Returns:
            Summary string
        """
        if not dialogues:
            return "No dialogue detected in the text."
        
        speaker_count = speakers.get('speaker_count', 0)
        dialogue_count = stats.get('dialogue_count', 0)
        dialogue_pct = stats.get('dialogue_percentage', 0)
        
        summary_parts = [
            f"Detected {dialogue_count} dialogue segment(s)",
            f"with {speaker_count} unique speaker(s).",
            f"Dialogue comprises {dialogue_pct:.1f}% of the text."
        ]
        
        return " ".join(summary_parts)
    
    def analyze_dialogue_sentiment(self, dialogues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment of each dialogue segment.
        
        Args:
            dialogues: List of dialogue segments
            
        Returns:
            Dialogues with sentiment analysis added
        """
        positive_words = {'happy', 'love', 'great', 'wonderful', 'excited', 'glad', 'pleased'}
        negative_words = {'sad', 'hate', 'terrible', 'awful', 'angry', 'upset', 'worried'}
        
        results = []
        for dialogue in dialogues:
            content_lower = dialogue['content'].lower()
            
            pos_count = sum(1 for word in positive_words if word in content_lower)
            neg_count = sum(1 for word in negative_words if word in content_lower)
            
            if pos_count > neg_count:
                sentiment = 'POSITIVE'
            elif neg_count > pos_count:
                sentiment = 'NEGATIVE'
            else:
                sentiment = 'NEUTRAL'
            
            result = dialogue.copy()
            result['sentiment'] = sentiment
            results.append(result)
        
        return results
