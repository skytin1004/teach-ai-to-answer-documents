# 教 AI 根據你的文件回答問題

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

本倉庫收集了一個 2026 年的博客系列，內容關於使用 RAG、Azure AI 服務、開源替代方案以及面向評估的工作流程構建以文件為基礎的 AI 系統。

## 背景

在 2023 年，我做了一對教學教程，關於如何使用 Azure AI Search 和 Azure OpenAI 教 ChatGPT 從 PDF 文件中回答問題。「ChatGPT 在你的數據上」的概念當時仍然感覺新穎，目標是展示一個實用的工作流程：存儲文件、索引它們、檢索相關內容，並從檢索到的上下文中生成答案。

到了 2026 年，RAG 生態系統大為擴展。Azure AI Search 支援現代的向量和混合檢索模式，Azure OpenAI 是微軟 Foundry 模型生態系統的一部分，而 LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama 以及 vLLM 等開源工具已成為實際系統的可行選擇。

這就是為何我想重新探討這個主題。現在的問題不僅是「我如何構建 RAG？」，而是有許多構建方式，更重要的問題是「我應該為我的情況選擇哪種架構？」

本系列從這個決策層開始，然後轉成動手教程。第一條實現路徑構建了一個本地開源的 RAG 系統，任何人都可以使用範例數據、Qdrant、Ollama 和 Phi-4-mini 運行。

## 文章

請參閱 [articles/README.md](./articles/README.md) 了解文章索引。

1. [系列一：RAG、Azure 與開源替代方案，及何時進行微調是合理的](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [系列二：端到端構建本地開源 RAG 系統](./articles/series-2-open-source-rag-end-to-end.md)

接下來：

- 使用 Azure AI Search 和 Azure OpenAI 重建相同的 RAG 系統。
- 添加評估與回歸檢查，超越演示答案。

## 筆記本

實現文章使用筆記本，這樣可以直接檢查檢索和評估步驟。請參閱 [notebooks/README.md](./notebooks/README.md) 獲取資料夾層級指導。

> [!TIP]
> 如果想走最快路徑，請從系列二開始。它在本地運行，使用範例數據、CPU 友好的嵌入、Qdrant 本地模式，且無需雲端憑證。

| 系列 | 筆記本 | 需求 | 本地驗證 |
| --- | --- | --- | --- |
| 系列二 | [開源 RAG 筆記本](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | 已驗證 Qdrant 本地模式、檢索、重新排名及來源連接 |

要在本地運行筆記本，請建立虛擬環境並安裝相應的需求檔。例如：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## 範例數據

筆記本使用小型本地語料庫放在 [sample_data](../../sample_data) 中，因此範例可以在無需私人文件或雲端憑證情況下運行。詳情請參閱 [sample_data/README.md](./sample_data/README.md)。

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## 本地驗證摘要

驗證結果記錄於各文章及 [SERIES_PLAN.md](./SERIES_PLAN.md)。

| 項目 | 結果 |
| --- | --- |
| 系列二開源路徑 | FastEmbed 生成 384 維本地嵌入，Qdrant 內存集合插入 8 個向量，輕量重新排名檢索到預期段落；可選 Ollama 生成完成，使用 `phi4-mini:3.8b` |

本地筆記本刻意避免硬編碼機密。

## 本地 Ollama 生成

系列二筆記本預設是本地安全。要啟用本地 Ollama 生成，請複製 [.env.example](../../.env.example) 為 `.env`，並填入系列二的值。

為系列二 Ollama 生成，取消註解：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

系列二筆記本會利用 `python-dotenv` 自動從倉庫根目錄載入 `.env`。

> [!IMPORTANT]
> 請勿提交 `.env` 檔案、API 金鑰、私有端點或租戶專屬值。倉庫刻意讓機密不出現在 Markdown 檔和筆記本中。

需求檔說明請參見 [requirements/README.md](./requirements/README.md)。

要驗證連結、筆記本結構、輸出清潔度，以及高風險秘密模式：

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

驗證腳本記錄於 [scripts/README.md](./scripts/README.md)。

要在同一環境執行所有本地安全的筆記本：

```powershell
python scripts\verify_notebooks.py --execute
```

相同的驗證流程會在 GitHub Actions 的 push、pull request 以及手動工作流程調度時運行。草稿文章及筆記本會故意排除在公眾驗證路徑外。

發佈更新前，請使用 [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)。

目前未發佈變更摘要請參考 [CHANGELOG.md](./CHANGELOG.md)。

關於貢獻及筆記本維護指引，詳見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 多語言支援

### 透過協作翻譯器支援（自動且隨時更新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯文](../ar/README.md) | [孟加拉文](../bn/README.md) | [保加利亞文](../bg/README.md) | [緬甸語（緬甸）](../my/README.md) | [中文（簡體）](../zh-CN/README.md) | [中文（繁體，香港）](../zh-HK/README.md) | [中文（繁體，澳門）](./README.md) | [中文（繁體，台灣）](../zh-TW/README.md) | [克羅地亞文](../hr/README.md) | [捷克文](../cs/README.md) | [丹麥文](../da/README.md) | [荷蘭文](../nl/README.md) | [愛沙尼亞文](../et/README.md) | [芬蘭文](../fi/README.md) | [法文](../fr/README.md) | [德文](../de/README.md) | [希臘文](../el/README.md) | [希伯來文](../he/README.md) | [印地文](../hi/README.md) | [匈牙利文](../hu/README.md) | [印尼文](../id/README.md) | [義大利文](../it/README.md) | [日文](../ja/README.md) | [卡納達文](../kn/README.md) | [高棉文](../km/README.md) | [韓文](../ko/README.md) | [立陶宛文](../lt/README.md) | [馬來文](../ms/README.md) | [馬拉雅拉姆文](../ml/README.md) | [馬拉地文](../mr/README.md) | [尼泊爾文](../ne/README.md) | [奈及利亞皮欽語](../pcm/README.md) | [挪威文](../no/README.md) | [波斯文（法爾西語）](../fa/README.md) | [波蘭文](../pl/README.md) | [葡萄牙文（巴西）](../pt-BR/README.md) | [葡萄牙文（葡萄牙）](../pt-PT/README.md) | [旁遮普文（古魯穆基）](../pa/README.md) | [羅馬尼亞文](../ro/README.md) | [俄文](../ru/README.md) | [塞爾維亞文（西里爾字母）](../sr/README.md) | [斯洛伐克文](../sk/README.md) | [斯洛文尼亞文](../sl/README.md) | [西班牙文](../es/README.md) | [斯瓦希里文](../sw/README.md) | [瑞典文](../sv/README.md) | [他加祿語（菲律賓語）](../tl/README.md) | [泰米爾文](../ta/README.md) | [泰盧固文](../te/README.md) | [泰文](../th/README.md) | [土耳其文](../tr/README.md) | [烏克蘭文](../uk/README.md) | [烏爾都文](../ur/README.md) | [越南文](../vi/README.md)

> **想要本地克隆？**
>
> 本倉庫包含 50 多種語言翻譯，這大幅增加下載大小。若要不下載翻譯內容，可使用稀疏檢出：
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD（Windows）：**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> 這樣可快速下載完成課程所需的所有內容。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->