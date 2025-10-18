# Integration Guide for Deep Semantic Analysis Module

This document provides guidance on integrating the semantic analysis module
into larger systems for multi-modal narrative immersion.

## Module Architecture

The semantic analysis module is designed to be modular and extensible:

```
┌─────────────────────────────────────────────┐
│        SemanticAnalyzer (Main Entry)        │
├─────────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────┐     │
│  │  Sentiment   │  │     Tone        │     │
│  │   Analyzer   │  │   Analyzer      │     │
│  └──────────────┘  └─────────────────┘     │
│  ┌──────────────┐  ┌─────────────────┐     │
│  │ Relationship │  │    Context      │     │
│  │  Extractor   │  │   Analyzer      │     │
│  └──────────────┘  └─────────────────┘     │
└─────────────────────────────────────────────┘
```

## Integration Points

### 1. Text-to-Speech (TTS) Integration

Use sentiment and tone analysis to modulate voice characteristics:

```python
from semantic_analysis import SemanticAnalyzer

analyzer = SemanticAnalyzer()
results = analyzer.analyze(text)

# Extract tone and sentiment
tone = results['tone']['primary_tone']
sentiment = results['sentiment']['label']
intensity = results['tone']['intensity']

# Map to TTS parameters
voice_params = {
    'speed': 1.0 + (intensity * 0.3),  # Faster for intense passages
    'pitch': 1.0 if sentiment == 'POSITIVE' else 0.9,
    'emotion': tone  # Use tone for emotion parameter
}

# Apply to TTS engine
# tts_engine.set_parameters(voice_params)
# tts_engine.speak(text)
```

### 2. Haptic Feedback Integration

Map emotions and intensity to haptic patterns:

```python
# Extract emotional information
emotions = results['sentiment']['emotions']
intensity = results['tone']['intensity']

# Map to haptic patterns
if emotions.get('fear', 0) > 0.5:
    haptic_pattern = 'rapid_pulse'
elif emotions.get('joy', 0) > 0.5:
    haptic_pattern = 'gentle_wave'
elif intensity > 0.7:
    haptic_pattern = 'strong_vibration'
else:
    haptic_pattern = 'subtle_pulse'

# Send to haptic device
# haptic_device.play_pattern(haptic_pattern, intensity)
```

### 3. Scent Generation Integration

Use context and themes to trigger appropriate scents:

```python
# Extract context
context = results['context']
themes = context['themes']
spatial = context['spatial_context']['primary_setting']

# Map to scent profiles
scent_mapping = {
    'outdoor': 'fresh_grass',
    'rural': 'wildflowers',
    'urban': 'coffee_shop',
    'indoor': 'wood_smoke'
}

# Theme-based scents
if 'mystery' in themes:
    scent = 'old_books'
elif 'romance' in themes:
    scent = 'rose_petals'
else:
    scent = scent_mapping.get(spatial, 'neutral')

# Trigger scent device
# scent_device.emit(scent, duration=10)
```

### 4. Dynamic Music Selection

Use mood and themes to select background music:

```python
mood = results['tone']['mood']
themes = results['context']['themes']

# Map to music genres/tracks
music_selection = {
    'intense': 'dramatic_orchestra',
    'lighthearted': 'playful_strings',
    'somber': 'melancholic_piano',
    'uplifting': 'inspirational_soundtrack'
}

background_music = music_selection.get(mood, 'ambient_calm')

# If specific themes are strong, override
if themes.get('adventure', 0) > 0.7:
    background_music = 'epic_adventure'
elif themes.get('romance', 0) > 0.7:
    background_music = 'romantic_melody'

# Apply to audio system
# audio_system.play_background(background_music)
```

### 5. Visual Effects Integration

Use character relationships and context for visual storytelling:

```python
relationships = results['relationships']
characters = relationships['characters']

# Create character network visualization
# for character in characters:
#     visual_system.add_character_node(character)
#
# for rel in relationships['relationships']:
#     visual_system.add_relationship_edge(
#         rel['character1'], 
#         rel['character2'],
#         rel['type']
#     )

# Set visual atmosphere based on mood
temporal = results['context']['temporal_context']['primary_period']
if temporal == 'past':
    visual_filter = 'sepia_tone'
elif results['context']['temporal_context']['is_futuristic']:
    visual_filter = 'neon_glow'
else:
    visual_filter = 'natural'

# visual_system.apply_filter(visual_filter)
```

## Real-Time Processing Pipeline

For continuous narrative processing:

```python
import queue
import threading

class NarrativeProcessor:
    def __init__(self):
        self.analyzer = SemanticAnalyzer()
        self.text_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
    def process_stream(self):
        """Process text segments in real-time."""
        while True:
            text_segment = self.text_queue.get()
            if text_segment is None:
                break
                
            # Analyze segment
            results = self.analyzer.analyze(text_segment)
            
            # Put results for consumption
            self.result_queue.put(results)
            
    def start(self):
        """Start background processing thread."""
        self.thread = threading.Thread(target=self.process_stream)
        self.thread.start()
        
    def add_text(self, text):
        """Add text segment for analysis."""
        self.text_queue.put(text)
        
    def get_results(self, timeout=1.0):
        """Get analysis results."""
        try:
            return self.result_queue.get(timeout=timeout)
        except queue.Empty:
            return None

# Usage
processor = NarrativeProcessor()
processor.start()

# As narrative text arrives...
processor.add_text("Chapter 1: The Beginning...")
results = processor.get_results()

# Apply results to multi-modal outputs
# apply_to_tts(results)
# apply_to_haptics(results)
# apply_to_scent(results)
```

## Performance Optimization

### Batch Processing

For better performance when analyzing multiple segments:

```python
# Instead of processing one by one
results = [analyzer.analyze(text) for text in texts]

# Use batch processing
results = analyzer.analyze_batch(texts)
```

### Caching Results

For frequently analyzed content:

```python
import hashlib
import json

class CachedSemanticAnalyzer:
    def __init__(self):
        self.analyzer = SemanticAnalyzer()
        self.cache = {}
        
    def analyze(self, text):
        # Create cache key
        key = hashlib.md5(text.encode()).hexdigest()
        
        # Check cache
        if key in self.cache:
            return self.cache[key]
            
        # Analyze and cache
        results = self.analyzer.analyze(text)
        self.cache[key] = results
        return results
```

## Future Enhancement Possibilities

1. **Multi-language Support**: Extend to support Chinese, Japanese, etc.
2. **Fine-tuned Models**: Train custom models for specific narrative domains
3. **Temporal Analysis**: Track emotional arcs across entire narratives
4. **Advanced NER**: Use spaCy or custom models for better character extraction
5. **Knowledge Graphs**: Build relationship graphs that persist across chapters
6. **Real-time Sentiment Tracking**: Create emotional timeline visualizations

## API Reference

See the main README.md for complete API documentation.

## Contributing

To add new analyzers or enhance existing ones:

1. Follow the existing analyzer pattern
2. Implement the core `analyze()` method
3. Add batch processing support
4. Update the main SemanticAnalyzer to include your analyzer
5. Add tests and documentation
