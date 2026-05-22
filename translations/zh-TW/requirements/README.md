# Requirements

每篇實作文章都有專注的需求檔案。

| 檔案 | 使用於 |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | 第 2 系列開源 RAG 筆記本，包括可選的 Ollama 生成輔助工具 |
| [all.txt](../../../requirements/all.txt) | 倉庫層級驗證與 CI |

執行單一筆記本時請使用專注檔案。驗證整個倉庫時請使用 `all.txt`。

`open-source-rag.txt` 與 `all.txt` 包含用於本地嵌入的 `fastembed` 以及 `python-dotenv`，使第 2 系列能從 `.env` 選擇性啟用 Ollama 生成，無需更改檢索流程。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->