# 貢獻

此存儲庫組織為博客系列加上可執行的筆記本範例。

## 開啟拉取請求之前

請運行本地驗證腳本：

```powershell
python scripts\verify_notebooks.py
```

對於實作或筆記本變更，運行本地安全的筆記本執行：

```powershell
python scripts\verify_notebooks.py --execute
```

## 筆記本準則

- 保持筆記本易讀並聚焦於相關文章。
- 不要提交儲存的筆記本輸出或執行計數。
- 除非文章要求特定外部資源，否則使用來自 `sample_data/` 的小型範例資料。
- 當行為改變時，請在相關文章中記錄驗證結果。

## 機密與憑證

- 不要提交 API 金鑰、令牌、密碼、私人端點或 `.env` 檔案。
- `.env.example` 僅用作占位符值。
- 使用環境變數進行可選的本地 Ollama 實驗。

## 文件

- 保持文章導航連結最新。
- 新增文章、筆記本、需求文件或範例資料檔案時，更新 `README.md`。
- 在發布可見的存儲庫更新前，更新 `CHANGELOG.md`。

## 驗證

GitHub Actions 工作流程會執行：

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

存於 `drafts/` 下的草稿材料在準備公開索引前會被存儲庫驗證跳過。

## 問題

對於文章修正，請使用文章反饋範本；對於筆記本執行問題，請使用筆記本問題範本。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->