"""
Multi-language support module for semantic analysis.

Provides language detection and multilingual text analysis capabilities.
"""

from typing import Dict, Any, List, Optional


class LanguageDetector:
    """
    Detects the language of input text.
    
    Supports detection of multiple languages including:
    - English (en)
    - Chinese (zh)
    - Japanese (ja)
    - Korean (ko)
    - And more...
    """
    
    def __init__(self):
        """Initialize the language detector."""
        self.language_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize language detection patterns.
        
        Returns:
            Dictionary of language patterns and characteristics
        """
        return {
            'zh': {
                'name': 'Chinese',
                'name_native': '中文',
                'unicode_ranges': [(0x4E00, 0x9FFF), (0x3400, 0x4DBF)],  # CJK Unified Ideographs
                'keywords': ['的', '是', '在', '有', '和', '了', '我', '你', '他', '她']
            },
            'ja': {
                'name': 'Japanese',
                'name_native': '日本語',
                'unicode_ranges': [(0x3040, 0x309F), (0x30A0, 0x30FF)],  # Hiragana, Katakana
                'keywords': ['の', 'は', 'を', 'に', 'が', 'で', 'と', 'た', 'です', 'ます']
            },
            'ko': {
                'name': 'Korean',
                'name_native': '한국어',
                'unicode_ranges': [(0xAC00, 0xD7AF)],  # Hangul Syllables
                'keywords': ['의', '이', '가', '을', '를', '에', '와', '과', '는', '은']
            },
            'en': {
                'name': 'English',
                'name_native': 'English',
                'unicode_ranges': [(0x0041, 0x007A)],  # Basic Latin
                'keywords': ['the', 'is', 'are', 'was', 'were', 'have', 'has', 'will', 'would', 'could']
            }
        }
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing:
            - language_code: ISO 639-1 language code
            - language_name: Full language name
            - confidence: Detection confidence score
            - is_multilingual: Whether text contains multiple languages
        """
        if not text.strip():
            return {
                'language_code': 'unknown',
                'language_name': 'Unknown',
                'confidence': 0.0,
                'is_multilingual': False
            }
        
        scores = self._calculate_language_scores(text)
        
        # Find the language with highest score
        if scores:
            best_lang = max(scores, key=scores.get)
            best_score = scores[best_lang]
            
            # Check if multilingual
            significant_languages = [lang for lang, score in scores.items() if score > 0.2]
            is_multilingual = len(significant_languages) > 1
            
            lang_info = self.language_patterns.get(best_lang, {})
            
            return {
                'language_code': best_lang,
                'language_name': lang_info.get('name', 'Unknown'),
                'language_native': lang_info.get('name_native', ''),
                'confidence': best_score,
                'is_multilingual': is_multilingual,
                'all_scores': scores
            }
        
        return {
            'language_code': 'en',
            'language_name': 'English',
            'confidence': 0.5,
            'is_multilingual': False
        }
    
    def _calculate_language_scores(self, text: str) -> Dict[str, float]:
        """
        Calculate detection scores for each supported language.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping language codes to confidence scores
        """
        scores = {}
        text_lower = text.lower()
        
        for lang_code, lang_info in self.language_patterns.items():
            score = 0.0
            
            # Check Unicode ranges
            unicode_score = self._check_unicode_ranges(text, lang_info['unicode_ranges'])
            score += unicode_score * 0.6
            
            # Check keywords
            keyword_score = self._check_keywords(text_lower, lang_info['keywords'])
            score += keyword_score * 0.4
            
            scores[lang_code] = min(score, 1.0)
        
        return scores
    
    def _check_unicode_ranges(self, text: str, ranges: List[tuple]) -> float:
        """Check how many characters fall within specified Unicode ranges."""
        if not text:
            return 0.0
        
        count = 0
        for char in text:
            code_point = ord(char)
            for start, end in ranges:
                if start <= code_point <= end:
                    count += 1
                    break
        
        return count / len(text)
    
    def _check_keywords(self, text: str, keywords: List[str]) -> float:
        """Check for presence of language-specific keywords."""
        if not keywords:
            return 0.0
        
        found = sum(1 for keyword in keywords if keyword in text)
        return found / len(keywords)


class MultilingualAnalyzer:
    """
    Provides multilingual text analysis with language-specific processing.
    """
    
    def __init__(self):
        """Initialize the multilingual analyzer."""
        self.detector = LanguageDetector()
        self.sentiment_lexicons = self._initialize_lexicons()
    
    def _initialize_lexicons(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Initialize sentiment lexicons for multiple languages.
        
        Returns:
            Dictionary of language-specific sentiment lexicons
        """
        return {
            'en': {
                'positive': ['good', 'great', 'excellent', 'wonderful', 'happy', 'love', 'beautiful', 'amazing'],
                'negative': ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'ugly', 'horrible']
            },
            'zh': {
                'positive': ['好', '棒', '優秀', '美麗', '快樂', '愛', '幸福', '喜歡', '開心', '精彩'],
                'negative': ['壞', '糟糕', '可怕', '恨', '悲傷', '生氣', '醜', '討厭', '難過', '失望']
            },
            'ja': {
                'positive': ['良い', '素晴らしい', '美しい', '嬉しい', '好き', '幸せ', '楽しい', '素敵'],
                'negative': ['悪い', 'ひどい', '嫌い', '悲しい', '怒り', '辛い', '寂しい', '残念']
            },
            'ko': {
                'positive': ['좋다', '훌륭하다', '아름답다', '행복하다', '사랑', '기쁘다', '즐겁다'],
                'negative': ['나쁘다', '싫다', '슬프다', '화나다', '미워하다', '끔찍하다', '실망']
            }
        }
    
    def analyze(self, text: str, target_language: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform multilingual analysis on the input text.
        
        Args:
            text: Input text to analyze
            target_language: Optional target language code for analysis
            
        Returns:
            Dictionary containing multilingual analysis results
        """
        # Detect language
        lang_result = self.detector.detect(text)
        detected_lang = lang_result['language_code']
        
        # Use target language if specified, otherwise use detected language
        analysis_lang = target_language or detected_lang
        
        # Perform language-specific sentiment analysis
        sentiment = self._analyze_sentiment(text, analysis_lang)
        
        return {
            'language_detection': lang_result,
            'sentiment': sentiment,
            'text_stats': self._get_text_stats(text, detected_lang)
        }
    
    def _analyze_sentiment(self, text: str, language: str) -> Dict[str, Any]:
        """
        Perform language-specific sentiment analysis.
        
        Args:
            text: Input text
            language: Language code
            
        Returns:
            Sentiment analysis results
        """
        lexicon = self.sentiment_lexicons.get(language, self.sentiment_lexicons['en'])
        
        text_lower = text.lower()
        pos_count = sum(1 for word in lexicon['positive'] if word in text_lower)
        neg_count = sum(1 for word in lexicon['negative'] if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return {
                'label': 'NEUTRAL',
                'score': 0.5,
                'positive_count': 0,
                'negative_count': 0
            }
        
        if pos_count > neg_count:
            label = 'POSITIVE'
            score = 0.5 + (0.5 * pos_count / total)
        elif neg_count > pos_count:
            label = 'NEGATIVE'
            score = 0.5 - (0.5 * neg_count / total)  # Negative sentiment scores below 0.5
        else:
            label = 'NEUTRAL'
            score = 0.5
        
        return {
            'label': label,
            'score': score,
            'positive_count': pos_count,
            'negative_count': neg_count
        }
    
    def _get_text_stats(self, text: str, language: str) -> Dict[str, Any]:
        """
        Get text statistics appropriate for the detected language.
        
        Args:
            text: Input text
            language: Detected language code
            
        Returns:
            Text statistics
        """
        # Character count (important for CJK languages)
        char_count = len(text)
        
        # Word count (space-separated for most languages)
        if language in ['zh', 'ja']:
            # For CJK, count characters as approximate word count
            word_count = len([c for c in text if not c.isspace()])
        else:
            word_count = len(text.split())
        
        return {
            'character_count': char_count,
            'word_count': word_count,
            'language': language
        }
    
    def translate_sentiment_label(self, label: str, target_language: str) -> str:
        """
        Translate sentiment label to target language.
        
        Args:
            label: Sentiment label (POSITIVE, NEGATIVE, NEUTRAL)
            target_language: Target language code
            
        Returns:
            Translated label
        """
        translations = {
            'zh': {'POSITIVE': '正面', 'NEGATIVE': '負面', 'NEUTRAL': '中性'},
            'ja': {'POSITIVE': 'ポジティブ', 'NEGATIVE': 'ネガティブ', 'NEUTRAL': 'ニュートラル'},
            'ko': {'POSITIVE': '긍정적', 'NEGATIVE': '부정적', 'NEUTRAL': '중립적'},
            'en': {'POSITIVE': 'Positive', 'NEGATIVE': 'Negative', 'NEUTRAL': 'Neutral'}
        }
        
        lang_translations = translations.get(target_language, translations['en'])
        return lang_translations.get(label, label)
