# 教AI根據您的文件回答問題

![以文件為基礎的AI RAG系統總覽](../../assets/images/readme-hero.svg)

本存放庫匯集了2026年的一系列部落格文章，關於使用RAG、Azure AI服務、開源替代方案與評估導向工作流程構建以文件為基礎的AI系統。

## 背景

2023年，我製作了一對教學課程，介紹如何使用Azure AI Search和Azure OpenAI教ChatGPT從PDF文件中回答問題。當時「將ChatGPT應用於您的數據」的想法仍然相當新鮮，而目標是展示一個實用流程：存儲文件、建立索引、檢索相關內容，並從檢索到的上下文產生回答。

到了2026年，RAG生態系統已經大幅擴展。Azure AI Search支援現代向量和混合檢索模式，Azure OpenAI是更廣泛的Microsoft Foundry模型生態系統的一部分，且LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama與vLLM等開源工具已成為實際系統的可行選擇。

這也是我想重新探討這個主題的原因。問題已不僅是「如何建立RAG？」現在有許多建置方式，更重要的問題是「我應該為我的情況選擇哪種架構？」

本系列從決策層開始，接著轉為實作教學。第一個實作路徑打造一個可與範例數據、Qdrant、Ollama與Phi-4-mini一起執行的本地開源RAG系統。

## 文章

請參閱 [articles/README.md](./articles/README.md) 以獲得文章索引。

1. [系列1：RAG、Azure vs 開源替代方案，以及何時進行微調才合理](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [系列2：完整建置本地開源RAG系統](./articles/series-2-open-source-rag-end-to-end.md)

接下來會有：

- 使用Azure AI Search和Azure OpenAI重建相同的RAG系統。
- 除了展示答案之外，加入評估與回歸檢查。

## 筆記本

實作文章使用筆記本，使檢索與評估步驟可直接檢視。請參閱 [notebooks/README.md](./notebooks/README.md) 以獲得資料夾層級的指引。

> [!TIP]
> 若想要最快路徑，從系列2開始。它可在本地運行，使用範例數據、對CPU友好的嵌入向量、Qdrant本地模式，且無需雲端憑證。

| 系列 | 筆記本 | 需求 | 本地驗證 |
| --- | --- | --- | --- |
| 系列2 | [開源RAG筆記本](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | 已驗證Qdrant本地模式、檢索、再排名與來源連接 |

要在本地執行筆記本，請建立虛擬環境並安裝相符的需求檔。例如：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```


## 範例數據

筆記本使用[ sample_data ](../../sample_data)中的小型本地語料庫，以便實例範例可在無私有文檔或雲端憑證狀況下運行。詳見 [sample_data/README.md](./sample_data/README.md)。

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## 本地驗證摘要

驗證結果記錄於各文章及 [SERIES_PLAN.md](./SERIES_PLAN.md)。

| 領域 | 結果 |
| --- | --- |
| 系列2開源路徑 | FastEmbed生成384維度的本地嵌入向量，Qdrant內存集合插入8個向量，輕量的再排名檢索出預期章節；選用Ollama執行`phi4-mini:3.8b`完成文本產生 |

本地筆記本刻意避免硬編碼祕密。

## 本地Ollama生成

系列2筆記本預設可本地安全執行。要啟用本地Ollama生成，請複製 [.env.example](../../.env.example) 為 `.env` 並填入系列2的設定值。

對於系列2的Ollama生成，取消註解：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```


系列2筆記本透過`python-dotenv`自動從存放庫根目錄載入`.env`。

> [!IMPORTANT]
> 請勿將`.env`檔案、API金鑰、私有端點或租戶特定值提交至版本庫。本存放庫刻意將祕密排除於Markdown文件與筆記本之外。

需求文件紀錄於 [requirements/README.md](./requirements/README.md)。

要驗證連結、筆記本結構、筆記本輸出清潔度及高風險祕密模式：

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```


驗證腳本紀錄於 [scripts/README.md](./scripts/README.md)。

要在同一環境中執行所有本地安全筆記本：

```powershell
python scripts\verify_notebooks.py --execute
```


相同的驗證流程會在GitHub Actions於推送、拉取請求與手動工作流程分派時執行。草稿文章與筆記本故意排除於公開驗證路徑之外。

發佈更新前，請使用 [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)。

參閱 [CHANGELOG.md](./CHANGELOG.md) 以了解目前未發佈的變更摘要。

欲知貢獻與筆記本維護規範，請參照 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 多語言支援

### 透過合作翻譯員支援 (自動且始終保持最新)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯文](../ar/README.md) | [孟加拉文](../bn/README.md) | [保加利亞文](../bg/README.md) | [緬甸文](../my/README.md) | [中文（簡體）](../zh-CN/README.md) | [中文（繁體，香港）](../zh-HK/README.md) | [中文（繁體，澳門）](../zh-MO/README.md) | [中文（繁體，臺灣）](./README.md) | [克羅埃西亞文](../hr/README.md) | [捷克文](../cs/README.md) | [丹麥文](../da/README.md) | [荷蘭文](../nl/README.md) | [愛沙尼亞文](../et/README.md) | [芬蘭文](../fi/README.md) | [法文](../fr/README.md) | [德文](../de/README.md) | [希臘文](../el/README.md) | [希伯來文](../he/README.md) | [印地文](../hi/README.md) | [匈牙利文](../hu/README.md) | [印尼文](../id/README.md) | [義大利文](../it/README.md) | [日文](../ja/README.md) | [坎那達文](../kn/README.md) | [高棉文](../km/README.md) | [韓文](../ko/README.md) | [立陶宛文](../lt/README.md) | [馬來文](../ms/README.md) | [馬拉雅拉姆文](../ml/README.md) | [馬拉地文](../mr/README.md) | [尼泊爾文](../ne/README.md) | [奈及利亞洋泾浜語](../pcm/README.md) | [挪威文](../no/README.md) | [波斯文（法爾西文）](../fa/README.md) | [波蘭文](../pl/README.md) | [葡萄牙文（巴西）](../pt-BR/README.md) | [葡萄牙文（葡萄牙）](../pt-PT/README.md) | [旁遮普文（古魯穆奇文）](../pa/README.md) | [羅馬尼亞文](../ro/README.md) | [俄文](../ru/README.md) | [塞爾維亞文（西里爾字母）](../sr/README.md) | [斯洛伐克文](../sk/README.md) | [斯洛維尼亞文](../sl/README.md) | [西班牙文](../es/README.md) | [斯瓦希里文](../sw/README.md) | [瑞典文](../sv/README.md) | [塔加洛語（菲律賓語）](../tl/README.md) | [泰米爾文](../ta/README.md) | [泰盧固文](../te/README.md) | [泰文](../th/README.md) | [土耳其文](../tr/README.md) | [烏克蘭文](../uk/README.md) | [烏爾都文](../ur/README.md) | [越南文](../vi/README.md)

> **想本地端克隆嗎？**
>
> 本存放庫包含超過50種語言的翻譯，使下載大小大幅增加。若想不含翻譯內容克隆，請使用稀疏簽出：
>
> **Bash / macOS / Linux：**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows)：**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> 這會給您完成課程所需的一切，且下載速度更快。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->