# 教 AI 根據你的文件回答問題

![基於文件的 AI RAG 系統概述](../../assets/images/readme-hero.svg)

此存儲庫收集了一個關於使用 RAG、Azure AI 服務、開源替代方案及評估導向工作流程構建基於文件的 AI 系統的 2026 博客系列。

## 背景

2023 年，我做了一對關於如何教 ChatGPT 使用 Azure AI Search 和 Azure OpenAI 從 PDF 文件回答問題的教程。當時「ChatGPT 在你的數據上」的概念仍然感覺很新，目標是展示一個實際的工作流程：存儲文件、編制索引、檢索相關內容，並從檢索到的上下文生成答案。

到了 2026 年，RAG 生態系統已大幅擴展。Azure AI Search 支持現代的向量和混合檢索模式，Azure OpenAI 是更廣泛的 Microsoft Foundry Models 生態系統的一部分，LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama 和 vLLM 等開源工具已成為實際系統的可行選擇。

這也是我想重訪這個主題的原因。現在問題不再只是「我如何構建 RAG？」而是有很多構建方式，更重要的是「我應該為我的情況選擇哪種架構？」

這個系列從這個決策層開始，然後變成動手教程。第一條實現路徑構建一個本地開源 RAG 系統，任何人都能用示例數據、Qdrant、Ollama 和 Phi-4-mini 運行。

## 文章

參見 [articles/README.md](./articles/README.md) 以查看文章索引。

1. [系列一：RAG、Azure vs 開源替代方案，及何時微調更合適](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [系列二：從頭到尾構建本地開源 RAG 系統](./articles/series-2-open-source-rag-end-to-end.md)

接下來:

- 使用 Azure AI Search 和 Azure OpenAI 重建同一個 RAG 系統。
- 新增超出示範答案的評估和回歸檢查。

## 筆記本

實現文章使用筆記本，使檢索和評估步驟可以直接檢查。參見 [notebooks/README.md](./notebooks/README.md) 獲取文件夾級指引。

> [!TIP]
> 如果想要最速路徑，請從系列二開始。它使用本地示例數據、CPU 友好的嵌入、Qdrant 本地模式，且無需雲端憑證。

| 系列 | 筆記本 | 需求 | 本地驗證 |
| --- | --- | --- | --- |
| 系列二 | [開源 RAG 筆記本](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | 已驗證 Qdrant 本地模式、檢索、重排名及來源接線 |

要在本地運行筆記本，建立虛擬環境並安裝相應需求文件。例如：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## 示例數據

筆記本使用位於 [sample_data](../../sample_data) 中的小型本地語料庫，讓示例能在無需私有文件或雲端憑證的情況下執行。詳情請參見 [sample_data/README.md](./sample_data/README.md)。

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## 本地驗證摘要

驗證結果記錄於每篇文章及 [SERIES_PLAN.md](./SERIES_PLAN.md) 中。

| 模塊 | 結果 |
| --- | --- |
| 系列二開源路徑 | FastEmbed 生成 384 維本地嵌入，Qdrant 內存集合插入 8 個向量，輕量級重排名檢索預期段落；可選 Ollama 使用 `phi4-mini:3.8b` 成功生成 |

本地筆記本故意避免硬編碼密鑰。

## 本地 Ollama 生成功能

系列二筆記本預設安全可在本地執行。要啟用本地 Ollama 生成功能，複製 [.env.example](../../.env.example) 至 `.env` 並填寫系列二相關數值。

對於系列二 Ollama 生成功能，取消註解：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

系列二筆記本通過 `python-dotenv` 自動從倉庫根目錄加載 `.env`。

> [!IMPORTANT]
> 請勿提交 `.env` 文件、API 金鑰、私有端點或租戶專用數值。此倉庫故意將密鑰排除在 Markdown 文件和筆記本外。

需求文件記錄於 [requirements/README.md](./requirements/README.md)。

要驗證鏈接、筆記本結構、輸出清潔度及高風險密鑰模式：

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

驗證腳本記錄於 [scripts/README.md](./scripts/README.md)。

要在同一環境中執行所有本地安全的筆記本：

```powershell
python scripts\verify_notebooks.py --execute
```

同一套驗證流程會在 GitHub Actions 中對推送、拉取請求和手動工作流程調度運行。草稿文章和筆記本故意排除於公開驗證路徑之外。

發布更新前，請使用 [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)。

有關當前未發布變更摘要，請參見 [CHANGELOG.md](./CHANGELOG.md)。

關於貢獻和筆記本維護指南，請參見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 多語言支持

### 透過 Co-op Translator 支持（自動且始終更新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯語](../ar/README.md) | [孟加拉語](../bn/README.md) | [保加利亞語](../bg/README.md) | [緬甸語](../my/README.md) | [中文 (簡體)](../zh-CN/README.md) | [中文 (繁體，香港)](./README.md) | [中文 (繁體，澳門)](../zh-MO/README.md) | [中文 (繁體，臺灣)](../zh-TW/README.md) | [克羅地亞語](../hr/README.md) | [捷克語](../cs/README.md) | [丹麥語](../da/README.md) | [荷蘭語](../nl/README.md) | [愛沙尼亞語](../et/README.md) | [芬蘭語](../fi/README.md) | [法語](../fr/README.md) | [德語](../de/README.md) | [希臘語](../el/README.md) | [希伯來語](../he/README.md) | [印地語](../hi/README.md) | [匈牙利語](../hu/README.md) | [印尼語](../id/README.md) | [義大利語](../it/README.md) | [日語](../ja/README.md) | [卡納達語](../kn/README.md) | [高棉語](../km/README.md) | [韓語](../ko/README.md) | [立陶宛語](../lt/README.md) | [馬來語](../ms/README.md) | [馬拉雅拉姆語](../ml/README.md) | [馬拉地語](../mr/README.md) | [尼泊爾語](../ne/README.md) | [奈及利亞皮欽語](../pcm/README.md) | [挪威語](../no/README.md) | [波斯語 (法爾西語)](../fa/README.md) | [波蘭語](../pl/README.md) | [葡萄牙語 (巴西)](../pt-BR/README.md) | [葡萄牙語 (葡萄牙)](../pt-PT/README.md) | [旁遮普語 (古魯木奇文)](../pa/README.md) | [羅馬尼亞語](../ro/README.md) | [俄語](../ru/README.md) | [塞爾維亞語 (西里爾文)](../sr/README.md) | [斯洛伐克語](../sk/README.md) | [斯洛文尼亞語](../sl/README.md) | [西班牙語](../es/README.md) | [斯瓦希里語](../sw/README.md) | [瑞典語](../sv/README.md) | [他加祿語 (菲律賓語)](../tl/README.md) | [泰米爾語](../ta/README.md) | [泰盧固語](../te/README.md) | [泰語](../th/README.md) | [土耳其語](../tr/README.md) | [烏克蘭語](../uk/README.md) | [烏爾都語](../ur/README.md) | [越南語](../vi/README.md)

> **想本地克隆？**
>
> 本倉庫包含超過 50 種語言翻譯，會大幅增加下載大小。若想無翻譯克隆，請使用稀疏檢出：
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> 這樣可以讓你快速獲得完成課程所需的全部內容，下載速度更快。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->