# 筆記本

這些筆記本支援文章系列並附有可執行的範例。

| 筆記本 | 文章 | 目的 |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [系列 2](../articles/series-2-open-source-rag-end-to-end.md) | 使用 FastEmbed、Qdrant 本地模式、檢索、重排序、可選 Ollama 生成及來源引用的開源 RAG |

## 本地運行

安裝您想運行的筆記本所需的依賴：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

或安裝所有依賴：

```powershell
python -m pip install -r requirements\all.txt
```

## 驗證

從代碼庫根目錄：

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

系列 2 可以從代碼庫根目錄的 `.env` 檔案讀取 Ollama 配置。從 [../.env.example](../../../.env.example) 開始，該檔案按系列分組。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->