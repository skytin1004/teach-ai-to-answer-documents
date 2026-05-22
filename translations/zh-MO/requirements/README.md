# Requirements

Each implementation article has a focused requirements file.

| File | Used by |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | 第二系列開源 RAG 筆記本，包括可選的 Ollama 生成輔助工具 |
| [all.txt](../../../requirements/all.txt) | 倉庫級驗證和 CI |

運行單個筆記本時請使用專注文件。驗證整個倉庫時使用 `all.txt`。

`open-source-rag.txt` 和 `all.txt` 包含本地嵌入的 `fastembed` 以及允許第二系列可選從 `.env` 啟用 Ollama 生成而無需更改檢索管道的 `python-dotenv`。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->