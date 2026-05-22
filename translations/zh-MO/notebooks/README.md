# 筆記本

這些筆記本支援文章系列中的可執行範例。

| 筆記本 | 文章 | 目的 |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [系列 2](../articles/series-2-open-source-rag-end-to-end.md) | 使用 FastEmbed、Qdrant 本地模式、檢索、重新排序、可選 Ollama 生成和來源引用的開源 RAG |

## 本地運行

安裝你想運行的筆記本所需的依賴：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

或者安裝所有依賴：

```powershell
python -m pip install -r requirements\all.txt
```

## 驗證

從儲存庫根目錄執行：

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

系列 2 可以從儲存庫根目錄的 `.env` 檔案讀取 Ollama 配置。請從 [../.env.example](../../../.env.example) 開始，該檔案按系列分組。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->