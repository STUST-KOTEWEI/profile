# 貢獻指南 (Contributing Guidelines)

感謝您有興趣為這個專案做出貢獻！以下是參與貢獻的指南。

Thank you for your interest in contributing to this project! Here are the guidelines for contributing.

## 如何貢獻 (How to Contribute)

### 回報問題 (Reporting Issues)

1. 在提交新問題前，請先搜尋現有的 Issues，確認問題尚未被回報。
2. 使用清晰、描述性的標題。
3. 提供詳細的步驟來重現問題。
4. 包含相關的錯誤訊息或截圖。

### 提交程式碼 (Submitting Code)

1. Fork 這個 repository。
2. 建立一個新的 branch：
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. 進行您的修改，並確保遵循現有的程式碼風格。
4. 撰寫或更新相關的測試。
5. 確保所有測試通過：
   ```bash
   cd A-Neuro-Semantic-Framework-for-Multi-Modal-Narrative-Immersion
   python test_semantic_analysis.py
   ```
6. 提交您的修改：
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
7. 推送到您的 fork：
   ```bash
   git push origin feature/your-feature-name
   ```
8. 開啟一個 Pull Request。

## 程式碼風格 (Code Style)

- 遵循 PEP 8 Python 程式碼風格指南
- 使用有意義的變數和函數名稱
- 為函數和類別撰寫 docstrings
- 保持程式碼簡潔、可讀

## 提交訊息格式 (Commit Message Format)

請使用以下格式撰寫提交訊息：

- `Add:` 新增功能
- `Fix:` 修復問題
- `Update:` 更新現有功能
- `Docs:` 文件更新
- `Test:` 測試相關
- `Refactor:` 程式碼重構

例如：`Add: sentiment analysis batch processing support`

## 授權 (License)

提交貢獻即表示您同意您的貢獻將依據本專案的 MIT 授權條款進行授權。

## 聯絡方式 (Contact)

如有任何問題，請透過以下方式聯繫：
- Email: 4b4g0077@stust.edu.tw
- GitHub Issues: https://github.com/STUST-KOTEWEI/profile/issues
