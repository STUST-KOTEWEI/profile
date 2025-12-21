# API 文件 (API Documentation)

本文件提供 Deep Semantic Analysis Module 的詳細 API 參考。

This document provides detailed API reference for the Deep Semantic Analysis Module.

## 目錄 (Table of Contents)

1. [SemanticAnalyzer](#semanticanalyzer)
2. [SentimentAnalyzer](#sentimentanalyzer)
3. [ToneAnalyzer](#toneanalyzer)
4. [RelationshipExtractor](#relationshipextractor)
5. [ContextAnalyzer](#contextanalyzer)

---

## SemanticAnalyzer

主要的語意分析器，整合所有分析組件。

The main semantic analyzer that integrates all analysis components.

### 初始化 (Initialization)

```python
from semantic_analysis import SemanticAnalyzer

analyzer = SemanticAnalyzer(model_name="bert-base-uncased")
```

**參數 (Parameters):**
| 參數 | 類型 | 預設值 | 描述 |
|------|------|--------|------|
| `model_name` | `str` | `"bert-base-uncased"` | Hugging Face 模型名稱 |

### 方法 (Methods)

#### `analyze(text: str) -> Dict[str, Any]`

執行完整的語意分析。

**參數:**
- `text` (str): 要分析的文本

**返回:**
```python
{
    'semantic_units': List[Dict],  # 語意單元列表
    'sentiment': Dict,              # 情感分析結果
    'tone': Dict,                   # 語調分析結果
    'relationships': Dict,          # 角色關係
    'context': Dict                 # 故事背景
}
```

#### `analyze_batch(texts: List[str]) -> List[Dict[str, Any]]`

批次分析多個文本。

**參數:**
- `texts` (List[str]): 文本列表

**返回:**
- `List[Dict[str, Any]]`: 每個文本的分析結果列表

---

## SentimentAnalyzer

情感分析組件，使用 Hugging Face Transformers。

Sentiment analysis component using Hugging Face Transformers.

### 初始化

```python
from semantic_analysis import SentimentAnalyzer

sentiment_analyzer = SentimentAnalyzer(
    model_name="distilbert-base-uncased-finetuned-sst-2-english"
)
```

### 方法

#### `analyze(text: str) -> Dict[str, Any]`

**返回結構:**
```python
{
    'label': str,       # 'POSITIVE', 'NEGATIVE', 或 'NEUTRAL'
    'score': float,     # 信心分數 (0.0 - 1.0)
    'emotions': {       # 情緒分數字典
        'joy': float,
        'sadness': float,
        'anger': float,
        'fear': float,
        'surprise': float,
        'love': float
    }
}
```

---

## ToneAnalyzer

語調和氛圍分析組件。

Tone and mood analysis component.

### 方法

#### `analyze(text: str) -> Dict[str, Any]`

**返回結構:**
```python
{
    'primary_tone': str,    # 主要語調
    'tone_scores': {        # 各語調分數
        'formal': float,
        'informal': float,
        'dramatic': float,
        'humorous': float,
        'serious': float,
        'optimistic': float,
        'pessimistic': float
    },
    'mood': str,            # 整體氛圍
    'intensity': float      # 強度 (0.0 - 1.0)
}
```

**語調類型 (Tone Types):**
- `formal` - 正式
- `informal` - 非正式
- `dramatic` - 戲劇性
- `humorous` - 幽默
- `serious` - 嚴肅
- `optimistic` - 樂觀
- `pessimistic` - 悲觀

---

## RelationshipExtractor

角色關係提取組件。

Character relationship extraction component.

### 方法

#### `extract(text: str) -> Dict[str, Any]`

**返回結構:**
```python
{
    'characters': List[str],        # 角色名單
    'relationships': [              # 關係列表
        {
            'character1': str,
            'character2': str,
            'type': str,
            'indicator': str
        }
    ],
    'relationship_types': Dict[str, int],  # 關係類型統計
    'interaction_summary': str             # 互動摘要
}
```

**關係類型 (Relationship Types):**
- `family` - 家庭關係
- `friendship` - 友誼
- `romantic` - 浪漫關係
- `professional` - 專業關係
- `antagonistic` - 敵對關係
- `mentor` - 師徒關係

---

## ContextAnalyzer

故事背景分析組件。

Story context analysis component.

### 方法

#### `analyze(text: str) -> Dict[str, Any]`

**返回結構:**
```python
{
    'temporal_context': {
        'primary_period': str,      # 'past', 'present', 'future'
        'period_scores': Dict,
        'is_historical': bool,
        'is_futuristic': bool
    },
    'spatial_context': {
        'primary_setting': str,     # 'indoor', 'outdoor', 'urban', 'rural'
        'setting_scores': Dict
    },
    'themes': {                     # 主題分數
        'adventure': float,
        'mystery': float,
        'romance': float,
        'conflict': float,
        'growth': float
    },
    'setting_description': str      # 設定描述
}
```

---

## 錯誤處理 (Error Handling)

所有分析器在遇到錯誤時會優雅地降級到規則基礎方法。

All analyzers gracefully fall back to rule-based methods when errors occur.

```python
try:
    result = analyzer.analyze(text)
except Exception as e:
    # 處理錯誤
    print(f"Analysis failed: {e}")
```

---

## 效能建議 (Performance Tips)

1. **批次處理**: 使用 `analyze_batch()` 處理多個文本
2. **文本長度**: 建議將長文本分段處理（< 512 tokens）
3. **模型載入**: 重複使用同一個分析器實例以避免重複載入模型

```python
# 推薦做法
analyzer = SemanticAnalyzer()
results = analyzer.analyze_batch(texts)  # 批次處理

# 避免
for text in texts:
    analyzer = SemanticAnalyzer()  # 每次都重新載入模型
    result = analyzer.analyze(text)
```
