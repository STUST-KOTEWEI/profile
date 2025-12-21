# Deep Semantic Analysis Module

深度語意分析模組 - 用於多模態敘事沉浸式體驗框架

## 概述 (Overview)

這個模組提供了完整的自然語言處理（NLP）功能，用於深度分析敘事文本。它可以將文本解析為語意單元，並進行情感分析、語調檢測、角色關係提取和故事背景分析。

This module provides comprehensive Natural Language Processing (NLP) capabilities for deep semantic analysis of narrative text. It decomposes text into semantic units and performs sentiment analysis, tone detection, character relationship extraction, and story context analysis.

## 功能特點 (Features)

### 1. 語意單元解析 (Semantic Unit Decomposition)
- 將文本分解為句子級別的語意單元
- 提供每個單元的元數據（長度、類型等）

### 2. 情感分析 (Sentiment Analysis)
- 使用 Hugging Face Transformers 進行情感分類
- 支持正面、負面、中性情感檢測
- 提供多種情緒檢測（喜悅、悲傷、憤怒、恐懼等）
- 可選：整合預訓練的 BERT 模型

### 3. 語調分析 (Tone Analysis)
- 檢測敘事語調（正式、非正式、戲劇性、幽默等）
- 分析整體氛圍（黑暗、明亮、緊張、平靜等）
- 計算情感強度

### 4. 角色關係提取 (Character Relationship Extraction)
- 識別文本中的角色
- 分析角色之間的關係類型（家庭、友誼、愛情、敵對等）
- 生成角色互動摘要

### 5. 故事背景分析 (Context Analysis)
- 時間背景檢測（過去、現在、未來）
- 空間設定分析（室內、室外、城市、鄉村）
- 主題識別（冒險、神秘、浪漫、衝突等）

## 安裝 (Installation)

### 基本安裝
```bash
pip install -r requirements.txt
```

### 可選依賴（用於增強功能）
```bash
# For advanced NER (Named Entity Recognition)
pip install spacy
python -m spacy download en_core_web_sm

# For additional NLP utilities
pip install nltk
```

## 使用方法 (Usage)

### 基本用法

```python
from semantic_analysis import SemanticAnalyzer

# 初始化分析器
analyzer = SemanticAnalyzer()

# 分析文本
text = "Your narrative text here..."
results = analyzer.analyze(text)

# 訪問結果
print(results['sentiment'])        # 情感分析結果
print(results['tone'])              # 語調分析結果
print(results['relationships'])     # 角色關係
print(results['context'])           # 故事背景
```

### 運行示例

```bash
cd A-Neuro-Semantic-Framework-for-Multi-Modal-Narrative-Immersion
python example_usage.py
```

### 進階用法

```python
from semantic_analysis import (
    SentimentAnalyzer,
    ToneAnalyzer,
    RelationshipExtractor,
    ContextAnalyzer
)

# 使用單獨的分析器
sentiment_analyzer = SentimentAnalyzer()
sentiment = sentiment_analyzer.analyze("I am very happy today!")

# 批次處理
texts = ["Text 1", "Text 2", "Text 3"]
results = analyzer.analyze_batch(texts)
```

## API 文檔 (API Documentation)

### SemanticAnalyzer

主要的語意分析器，整合所有分析組件。

**方法：**
- `analyze(text: str) -> Dict[str, Any]`: 執行完整的語意分析
- `analyze_batch(texts: List[str]) -> List[Dict[str, Any]]`: 批次分析多個文本

**返回結果包含：**
- `semantic_units`: 語意單元列表
- `sentiment`: 情感分析結果
- `tone`: 語調分析結果
- `relationships`: 角色關係
- `context`: 故事背景

### SentimentAnalyzer

情感分析組件。

**方法：**
- `analyze(text: str) -> Dict[str, Any]`: 分析文本情感
- `analyze_batch(texts: List[str]) -> List[Dict[str, Any]]`: 批次分析

**返回：**
- `label`: 情感標籤（POSITIVE, NEGATIVE, NEUTRAL）
- `score`: 信心分數
- `emotions`: 情緒分數字典

### ToneAnalyzer

語調和氛圍分析組件。

**方法：**
- `analyze(text: str) -> Dict[str, Any]`: 分析語調

**返回：**
- `primary_tone`: 主要語調
- `tone_scores`: 各種語調的分數
- `mood`: 整體氛圍
- `intensity`: 強度級別

### RelationshipExtractor

角色關係提取組件。

**方法：**
- `extract(text: str) -> Dict[str, Any]`: 提取角色關係

**返回：**
- `characters`: 角色名單
- `relationships`: 關係列表
- `relationship_types`: 關係類型統計
- `interaction_summary`: 互動摘要

### ContextAnalyzer

故事背景分析組件。

**方法：**
- `analyze(text: str) -> Dict[str, Any]`: 分析故事背景

**返回：**
- `temporal_context`: 時間背景
- `spatial_context`: 空間設定
- `themes`: 主題
- `setting_description`: 設定描述

## 架構 (Architecture)

```
semantic_analysis/
├── __init__.py                 # 模組初始化
├── semantic_analyzer.py        # 主分析器
├── sentiment_analyzer.py       # 情感分析
├── tone_analyzer.py           # 語調分析
├── relationship_extractor.py  # 關係提取
└── context_analyzer.py        # 背景分析
```

## 技術細節 (Technical Details)

### 使用的技術
- **Hugging Face Transformers**: 用於情感分析的預訓練模型
- **PyTorch**: 深度學習框架
- **正則表達式**: 用於文本模式匹配
- **規則基礎方法**: 用於語調、關係和背景分析

### 設計原則
1. **模組化設計**: 每個分析組件都是獨立的，可單獨使用
2. **可擴展性**: 易於添加新的分析功能
3. **回退機制**: 當深度學習模型不可用時，提供規則基礎的替代方案
4. **效能考慮**: 支持批次處理以提高效率

## 未來改進 (Future Improvements)

- [ ] 整合更多預訓練的 Transformer 模型
- [ ] 添加多語言支持（中文、日文等）
- [ ] 實現更精確的命名實體識別（NER）
- [ ] 添加對話分析功能
- [ ] 支持更複雜的關係圖譜
- [ ] 添加時間軸追蹤
- [ ] 整合知識圖譜

## 貢獻 (Contributing)

歡迎提交問題報告和改進建議！

## 授權 (License)

此專案使用 MIT 授權條款 - 詳見 [LICENSE](../LICENSE) 檔案。

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 聯絡方式 (Contact)

- Email: 4b4g0077@stust.edu.tw
- GitHub: https://github.com/STUST-KOTEWEI
