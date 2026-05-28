# Teach AI to Answer Questions Based on Your Documents - 系列計畫

本計畫追蹤公開 Series 1 與 Series 2 的發布。後續的 Azure 與評估工作則保留為草稿，直到範例完全端對端並經過驗證。

未經明確指示，請勿提交或推送變更。

## 公開範圍

目前公開發布：

- Series 1 文章：RAG 架構決策、Azure 與開源的取捨、以及微調的定位。
- Series 2 文章：本地開源 RAG 教學。
- Series 2 筆記本：可執行的本地 RAG 實驗室，包含 FastEmbed、Qdrant、Ollama、和 Phi-4-mini。
- 範例資料：學校政策與課程 AI 指南的 Markdown 檔案。

草擬中但尚未納入公開索引：

- Azure AI 搜尋與 Azure OpenAI 重建。
- RAG 評估與迴歸檢查。

## 教學場景

共享的場景是一個學校政策助理。

助理根據本地文件回答以下問題：

```text
Can I use generative AI for my final assignment?
```

預期行為為：

1. 載入本地 Markdown 文件。
2. 依據標題解析與分塊。
3. 建立本地嵌入向量並存儲含有元資料的可搜尋表示。
4. 檢索相關政策章節。
5. 必要時重新排序。
6. 產生或組合具依據的答案。
7. 回傳引用資料。
8. 紀錄驗證結果。

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

草稿材料儲存在 `drafts/` 資料夾中，且在公開索引準備好之前會被倉庫驗證忽略。

## Series 2 驗證

於 Windows 及 Python 3.12.6 環境下驗證。

- 成功安裝 `requirements/open-source-rag.txt`。
- 使用 `nbclient` 執行 `notebooks/series-2-open-source-rag.ipynb`。
- 本地驗證通過：載入2個範例文件，創建8個文本塊，FastEmbed 生成了384維的本地嵌入向量，Qdrant 初始化了記憶體集合並插入8個向量。
- 測試問題：「我可以將生成式 AI 用於我的期末作業嗎？」
- 輕量級重新排序後，最高檢索來源為 `school_ai_policy.md`。
- 輕量級重新排序後，最高檢索章節為 `Final Assignments`。
- 預設回答路徑：本地透明答案組合器。
- Ollama 透過 winget 安裝，成功拉取 `phi4-mini:3.8b`。
- Ollama 生成答案路徑：使用 `phi4-mini:3.8b` 完成。
- Ollama 模型檔案大小：約 2.49GB（磁碟上）。
- Ollama 載入模型大小：`ollama ps` 報告約 3.3GB。
- GPU 卸載：RTX 3060 筆電 GPU 上 `ollama ps` 報告 100% 使用率。
- 生成後觀察 GPU 記憶體：約使用 3.5GB（共 6GB）。
- 使用快取的 FastEmbed 模型及 Ollama 生成，在驗證腳本中筆記本執行約 34 秒通過。
- 觀察：早期文件載入階段意外包含了 `sample_data/README.md`；目前筆記本僅明確載入兩個指定範例文件。

## 倉庫驗證

- `scripts/verify_notebooks.py` 驗證本地 Markdown 連結、筆記本 JSON、筆記本輸出維持乾淨，以及高風險密鑰模式。
- `scripts/verify_notebooks.py --execute` 從倉庫根目錄執行公開筆記本。
- 草稿材料位於 `drafts/` 下，故意被跳過。

## 後續工作

- 使用 Azure AI 搜尋與 Azure OpenAI 重建相同場景作為未來系列的一部分。
- 當本地及 Azure 實作皆穩定後，加入檢索與答案評估。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->