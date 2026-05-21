# 教授 AI 根據您的文件回答問題

本儲存庫收集了一個 2026 年的部落格系列文章，講述如何使用 RAG、Azure AI 服務、開源替代方案及評估導向工作流程來建立以文件為基礎的 AI 系統。

## 背景

在 2023 年，我曾製作一對教學，內容是如何教 ChatGPT 利用 Azure AI Search 和 Azure OpenAI 從 PDF 文件中回答問題。「在您的資料上使用 ChatGPT」的概念當時仍感新穎，目標是展示一個實用的工作流程：存儲文件、建立索引、檢索相關內容，並根據檢索到的上下文生成答案。

到了 2026 年，RAG 生態系統已大幅擴展。Azure AI Search 支援現代向量及混合檢索模式，Azure OpenAI 成為 Microsoft Foundry Models 生態系統的一部分，且開源工具如 LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama 及 vLLM 成為實際系統的可行選擇。

這就是我想重新探討此主題的原因。問題已不再是「我該怎麼建立 RAG？」而是有很多建構方式，更重要的問題是「我該為我的情況選擇哪種架構？」

本系列從這個決策層面切入。在深入實作之前，將探討為何 AI 服務需要檢索、何時使用基於 Azure 的託管服務合理、何時開源替代方案更合適，以及微調的角色。

## 文章

1. [系列 1：RAG，Azure 與開源替代方案，以及何時微調合理](./series-1-rag-azure-open-source-fine-tuning.md)

## 多語言支援

### 由協作翻譯器支援（自動且隨時更新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯文](../ar/README.md) | [孟加拉文](../bn/README.md) | [保加利亞文](../bg/README.md) | [緬甸文 (緬甸)](../my/README.md) | [中文（簡體）](../zh-CN/README.md) | [中文（繁體，香港）](../zh-HK/README.md) | [中文（繁體，澳門）](./README.md) | [中文（繁體，臺灣）](../zh-TW/README.md) | [克羅地亞文](../hr/README.md) | [捷克文](../cs/README.md) | [丹麥文](../da/README.md) | [荷蘭文](../nl/README.md) | [愛沙尼亞文](../et/README.md) | [芬蘭文](../fi/README.md) | [法文](../fr/README.md) | [德文](../de/README.md) | [希臘文](../el/README.md) | [希伯來文](../he/README.md) | [印地文](../hi/README.md) | [匈牙利文](../hu/README.md) | [印尼文](../id/README.md) | [義大利文](../it/README.md) | [日文](../ja/README.md) | [坎納達文](../kn/README.md) | [高棉文](../km/README.md) | [韓文](../ko/README.md) | [立陶宛文](../lt/README.md) | [馬來文](../ms/README.md) | [馬拉雅拉姆文](../ml/README.md) | [馬拉地文](../mr/README.md) | [尼泊爾文](../ne/README.md) | [奈及利亞皮欽語](../pcm/README.md) | [挪威文](../no/README.md) | [波斯語 (法爾西語)](../fa/README.md) | [波蘭文](../pl/README.md) | [葡萄牙文（巴西）](../pt-BR/README.md) | [葡萄牙文（葡萄牙）](../pt-PT/README.md) | [旁遮普文 (古魯穆奇體)](../pa/README.md) | [羅馬尼亞文](../ro/README.md) | [俄文](../ru/README.md) | [塞爾維亞文（西里爾字母）](../sr/README.md) | [斯洛伐克文](../sk/README.md) | [斯洛維尼亞文](../sl/README.md) | [西班牙文](../es/README.md) | [斯瓦希里文](../sw/README.md) | [瑞典文](../sv/README.md) | [他加祿文（菲律賓語）](../tl/README.md) | [泰米爾文](../ta/README.md) | [泰盧固文](../te/README.md) | [泰文](../th/README.md) | [土耳其文](../tr/README.md) | [烏克蘭文](../uk/README.md) | [烏爾都文](../ur/README.md) | [越南文](../vi/README.md)

> **傾向於本地克隆？**
>
> 本儲存庫包含 50 多種語言版本，會大幅增加下載大小。若欲不含翻譯版本克隆，請使用稀疏檢出：
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
> 這樣能讓您以更快的下載速度取得完成課程所需的所有內容。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->