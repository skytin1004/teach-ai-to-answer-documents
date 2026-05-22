# 教 AI 根據您的文件回答問題 - 系列計劃

本計劃追蹤公開 Series 1 和 Series 2 的發布。後續的 Azure 和評估工作將保持為草稿，直到示例完全集成並驗證完成。

未經明確指示，請勿提交或推送更改。

## 公開範圍

當前公開發布：

- Series 1 文章：RAG 架構決策、Azure 與開源的取捨，以及微調的位置。
- Series 2 文章：本地開源 RAG 教程。
- Series 2 筆記本：可運行的本地 RAG 實驗室，使用 FastEmbed、Qdrant、Ollama 和 Phi-4-mini。
- 範例數據：學校政策和課程 AI 指導 Markdown 文件。

已草擬但尚未列入公開索引：

- Azure AI Search 和 Azure OpenAI 重建。
- RAG 評估和回歸檢查。

## 教程場景

共用場景為學校政策助手。

助手根據本地文件回答此問題：

```text
Can I use generative AI for my final assignment?
```


預期行為為：

1. 載入本地 Markdown 文件。
2. 按標題解析並分塊。
3. 創建本地嵌入並存儲帶元數據的可搜索表示。
4. 檢索相關政策部分。
5. 需要時重新排序。
6. 生成或組合有根據的答案。
7. 返回引用資料。
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


草稿材料存放於 `drafts/`，在準備好公開索引前，該目錄會被倉庫驗證機制跳過。

## Series 2 驗證

在 Windows 上使用 Python 3.12.6 驗證通過。

- 成功安裝 `requirements/open-source-rag.txt`。
- 使用 `nbclient` 執行 `notebooks/series-2-open-source-rag.ipynb`。
- 本地驗證通過：載入 2 份範例文件，創建 8 個分塊，FastEmbed 生成 384 維本地嵌入，初始化 Qdrant 內存集合，插入 8 個向量。
- 測試問題：「我可以用生成式 AI 完成期末作業嗎？」
- 輕量級重新排序後頂級檢索來源：`school_ai_policy.md`。
- 輕量級重新排序後頂級檢索章節：`Final Assignments`。
- 預設回答路徑：本地透明回答組合器。
- 透過 winget 安裝 Ollama；成功拉取 `phi4-mini:3.8b`。
- Ollama 回答生成路徑：使用 `phi4-mini:3.8b` 完成。
- Ollama 模型檔案大小：約 2.49GB（磁碟空間）。
- Ollama 加載模型大小：`ollama ps` 報告約 3.3GB。
- GPU 卸載：在 RTX 3060 筆記本 GPU 上由 `ollama ps` 報告 100% GPU 利用率。
- 生成後觀察 GPU 記憶體：約使用 3.5GB（共 6GB）。
- 筆記本執行（使用快取的 FastEmbed 模型及 Ollama 生成）約 34 秒，通過驗證腳本。
- 發現：早期文件載入過程意外包含了 `sample_data/README.md`；現今筆記本明確僅載入兩份目標樣本文件。

## 倉庫驗證

- `scripts/verify_notebooks.py` 驗證本地 Markdown 連結、筆記本 JSON、筆記本輸出清潔度，以及高風險秘密模式。
- `scripts/verify_notebooks.py --execute` 從倉庫根目錄執行公開筆記本。
- `drafts/` 下的草稿材料故意被跳過。

## 下一步工作

- 將同場景使用 Azure AI Search 和 Azure OpenAI 重建，作為未來系列部分。
- 本地與 Azure 實現均穩定後，新增檢索與回答評估。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->