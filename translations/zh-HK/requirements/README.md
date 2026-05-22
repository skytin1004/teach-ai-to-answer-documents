# 需求

每篇實作文章都會有專注的需求檔案。

| 檔案 | 使用者 |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | 系列 2 開源 RAG 筆記本，包括可選的 Ollama 生成輔助工具 |
| [all.txt](../../../requirements/all.txt) | 倉庫級別的驗證和 CI |

執行單一筆記本時使用專注的檔案。驗證整個倉庫時使用 `all.txt`。

`open-source-rag.txt` 和 `all.txt` 都包含本地嵌入的 `fastembed` 與 `python-dotenv`，以便系列 2 可選擇從 `.env` 啟用 Ollama 生成，而無需更改檢索流程。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->