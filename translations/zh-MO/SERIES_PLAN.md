# Teach AI to Answer Questions Based on Your Documents - 系列計劃

此計劃追蹤公開的系列 1 及系列 2 發布。後續的 Azure 及評估工作將作為草稿保存，直至範例完全端到端並獲確認。

未獲明確指示前，不可提交或推送更改。

## 公開範圍

當前公開版本：

- 系列 1 文章：RAG 架構決策，Azure 與開源折衷，以及微調的應用位置。
- 系列 2 文章：本地開源 RAG 教學。
- 系列 2 筆記本：可執行的本地 RAG 實驗室，包括 FastEmbed、Qdrant、Ollama 和 Phi-4-mini。
- 範例資料：學校政策及課程 AI 指引 Markdown 檔案。

已草擬但尚未納入公開索引：

- Azure AI Search 與 Azure OpenAI 重建。
- RAG 評估及迴歸檢查。

## 教學情境

共用的情境為學校政策助理。

助理根據本地文件回答以下問題：

```text
Can I use generative AI for my final assignment?
```
  
預期行為如下：

1. 載入本地 Markdown 文件。  
2. 按標題解析並分塊。  
3. 建立本地嵌入並與元資料一起存儲可搜尋的表示。  
4. 檢索相關的政策段落。  
5. 需要時重新排序。  
6. 產生或組合有依據的答案。  
7. 返回引證資料。  
8. 記錄驗證結果。

## 當前公開結構

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```
  
草稿資料存放於 `drafts/`，在準備公開索引前不會進行倉庫驗證。

## 系列 2 驗證

在 Windows，Python 3.12.6 上驗證通過。

- 成功安裝 `requirements/open-source-rag.txt`。  
- 使用 `nbclient` 執行 `notebooks/series-2-open-source-rag.ipynb`。  
- 本地驗證通過：載入 2 個示例文件，建立 8 個分塊，FastEmbed 產生 384 維本地嵌入，Qdrant 初始化內存集合，插入 8 個向量。  
- 測試問題：「我可否使用生成式 AI 幫助我的期末作業？」  
- 輕量重新排序後，最相關檢索來源為 `school_ai_policy.md`。  
- 輕量重新排序後，最相關檢索段落為「期末作業」。  
- 預設回答路徑：本地透明答案組合器。  
- Ollama 使用 winget 安裝；成功拉取 `phi4-mini:3.8b`。  
- Ollama 回答生成流程：使用 `phi4-mini:3.8b` 完成。  
- Ollama 模型檔案大小：約 2.49GB。  
- Ollama 加載模型大小：`ollama ps` 報告約 3.3GB。  
- GPU 卸載狀況：在 RTX 3060 筆記型電腦 GPU 上 `ollama ps` 報告 100% GPU 使用率。  
- 生成後 GPU 記憶體使用：約 3.5GB（總 6GB）。  
- 帶有 FastEmbed 模型快取及 Ollama 生成的筆記本執行通過驗證腳本，約 34 秒完成。  
- 觀察：早期文件載入過程誤加載了 `sample_data/README.md`；現在筆記本明確只載入兩個預期的示例文檔。

## 倉庫驗證

- `scripts/verify_notebooks.py` 驗證本地 Markdown 連結、筆記本 JSON、筆記本輸出潔淨度及高風險密鑰模式。  
- `scripts/verify_notebooks.py --execute` 從倉庫根目錄執行公開筆記本。  
- `drafts/` 領域的草稿資料故意略過驗證。

## 後續工作

- 將同一情境以 Azure AI Search 和 Azure OpenAI 重建，作為未來系列部分。  
- 當本地和 Azure 實作皆穩定後，加入檢索和回答評估。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->