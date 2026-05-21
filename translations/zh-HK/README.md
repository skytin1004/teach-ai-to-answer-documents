# 教 AI 根據你的文件回答問題

本存儲庫收集了 2026 年的博客系列文章，介紹如何構建基於文件的 AI 系統，內容涵蓋 RAG、Azure AI 服務、開源替代方案及以評估為導向的工作流程。

## 背景

2023 年，我製作了一對教程，介紹如何利用 Azure AI Search 和 Azure OpenAI 教 ChatGPT 根據 PDF 文件回答問題。當時「ChatGPT 用於你自己的數據」這個概念仍然很新，目標是展示一個實用的工作流程：存儲文件、建立索引、檢索相關內容，然後根據檢索到的上下文生成答案。

到了 2026 年，RAG 生態系統已經大大擴展。Azure AI Search 支援現代向量和混合檢索模式，Azure OpenAI 成為更廣泛的 Microsoft Foundry 模型生態系統的一部分，而像 LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama 和 vLLM 等開源工具，已成為實際系統的可行選擇。

這也是為什麼我想要重新探討這個主題。問題不再只是「我如何構建 RAG？」現在有很多構建方式，更重要的問題是「我應該為我的情況選擇哪種架構？」

本系列從決策層面開始，在深入實作之前，先探討為什麼 AI 服務需要檢索、什麼時候 Azure 托管服務更合適、什麼時候開源替代方案更適合，以及微調技術的位置。

## 文章

1. [系列 1：RAG、Azure 與開源替代方案，以及什麼時候適合微調](./series-1-rag-azure-open-source-fine-tuning.md)

## 多語言支持

### 透過協作翻譯工具支援（自動且始終保持最新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯文](../ar/README.md) | [孟加拉文](../bn/README.md) | [保加利亞文](../bg/README.md) | [緬甸文 (Myanmar)](../my/README.md) | [中文（簡體）](../zh-CN/README.md) | [中文（繁體，香港）](./README.md) | [中文（繁體，澳門）](../zh-MO/README.md) | [中文（繁體，臺灣）](../zh-TW/README.md) | [克羅地亞文](../hr/README.md) | [捷克文](../cs/README.md) | [丹麥文](../da/README.md) | [荷蘭文](../nl/README.md) | [愛沙尼亞文](../et/README.md) | [芬蘭文](../fi/README.md) | [法文](../fr/README.md) | [德文](../de/README.md) | [希臘文](../el/README.md) | [希伯來文](../he/README.md) | [印地文](../hi/README.md) | [匈牙利文](../hu/README.md) | [印尼文](../id/README.md) | [義大利文](../it/README.md) | [日語](../ja/README.md) | [坎那達文](../kn/README.md) | [高棉文](../km/README.md) | [韓文](../ko/README.md) | [立陶宛文](../lt/README.md) | [馬來文](../ms/README.md) | [馬拉雅拉姆文](../ml/README.md) | [馬拉地文](../mr/README.md) | [尼泊爾文](../ne/README.md) | [奈及利亞皮欽語](../pcm/README.md) | [挪威文](../no/README.md) | [波斯文（法爾西語）](../fa/README.md) | [波蘭文](../pl/README.md) | [葡萄牙文（巴西）](../pt-BR/README.md) | [葡萄牙文（葡萄牙）](../pt-PT/README.md) | [旁遮普文（Gurmukhi）](../pa/README.md) | [羅馬尼亞文](../ro/README.md) | [俄文](../ru/README.md) | [塞爾維亞文（西里爾字母）](../sr/README.md) | [斯洛伐克文](../sk/README.md) | [斯洛文尼亞文](../sl/README.md) | [西班牙文](../es/README.md) | [斯瓦希里文](../sw/README.md) | [瑞典文](../sv/README.md) | [他加祿文（菲律賓語）](../tl/README.md) | [泰米爾文](../ta/README.md) | [泰盧固文](../te/README.md) | [泰文](../th/README.md) | [土耳其文](../tr/README.md) | [烏克蘭文](../uk/README.md) | [烏爾都文](../ur/README.md) | [越南文](../vi/README.md)

> **想要本地克隆？**
>
> 本存儲庫包括 50 多種語言的翻譯，這大幅增加了下載大小。若想不下載翻譯內容，可使用稀疏簽出：
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD（Windows）:**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> 如此你可以更快下載所需內容，完成課程。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->