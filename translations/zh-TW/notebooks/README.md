# 筆記本

這些筆記本支援文章系列，包含可執行的範例。

| 筆記本 | 文章 | 目的 |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [系列 2](../articles/series-2-open-source-rag-end-to-end.md) | 使用 FastEmbed、Qdrant 本地模式的開源 RAG，包含檢索、重排序、選用 Ollama 生成以及來源參考 |

## 本地執行

安裝您想執行的筆記本需求：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

或安裝所有相依套件：

```powershell
python -m pip install -r requirements\all.txt
```

## 驗證

自版本庫根目錄執行：

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

系列 2 可從版本庫根目錄的 `.env` 檔案讀取 Ollama 配置。可由 [../.env.example](../../../.env.example) 開始，此範例按系列分組。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->