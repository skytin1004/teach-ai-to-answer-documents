# 教 AI 根据您的文档回答问题

本仓库汇集了一系列2026年的博客，内容关于使用RAG、Azure AI服务、开源替代方案以及面向评估的工作流来构建基于文档的AI系统。

## 背景

2023年，我制作了一对教程，讲述如何使用Azure AI搜索和Azure OpenAI教ChatGPT从PDF文档中回答问题。“在您的数据上运行ChatGPT”的理念当时仍然新颖，目标是展示一个实用的工作流：存储文档、索引文档、检索相关内容并从检索的上下文中生成答案。

到了2026年，RAG生态系统已经更大了。Azure AI搜索支持现代向量和混合检索模式，Azure OpenAI是更广泛的Microsoft Foundry模型生态系统的一部分，而开源工具如LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama和vLLM已经成为真实系统的实用选择。

这就是我想重新探讨这个话题的原因。问题不再只是“我如何构建RAG？”现在有许多构建方式，更重要的问题是“我应该为我的情况选择哪种架构？”

本系列从决策层面开始。在深入实现之前，它探讨了为什么AI服务需要检索，何时基于Azure的托管服务有意义，何时开源替代方案更合适，以及微调应用的场景。

## 文章

1. [系列1：RAG，Azure与开源替代方案，及微调何时有意义](./series-1-rag-azure-open-source-fine-tuning.md)

## 多语言支持

### 通过协同翻译器支持（自动且始终最新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯语](../ar/README.md) | [孟加拉语](../bn/README.md) | [保加利亚语](../bg/README.md) | [缅甸语](../my/README.md) | [中文（简体）](./README.md) | [中文（繁体，香港）](../zh-HK/README.md) | [中文（繁体，澳门）](../zh-MO/README.md) | [中文（繁体，台湾）](../zh-TW/README.md) | [克罗地亚语](../hr/README.md) | [捷克语](../cs/README.md) | [丹麦语](../da/README.md) | [荷兰语](../nl/README.md) | [爱沙尼亚语](../et/README.md) | [芬兰语](../fi/README.md) | [法语](../fr/README.md) | [德语](../de/README.md) | [希腊语](../el/README.md) | [希伯来语](../he/README.md) | [印地语](../hi/README.md) | [匈牙利语](../hu/README.md) | [印度尼西亚语](../id/README.md) | [意大利语](../it/README.md) | [日语](../ja/README.md) | [卡纳达语](../kn/README.md) | [高棉语](../km/README.md) | [韩语](../ko/README.md) | [立陶宛语](../lt/README.md) | [马来语](../ms/README.md) | [马拉雅拉姆语](../ml/README.md) | [马拉地语](../mr/README.md) | [尼泊尔语](../ne/README.md) | [尼日利亚皮钦语](../pcm/README.md) | [挪威语](../no/README.md) | [波斯语 (法尔西)](../fa/README.md) | [波兰语](../pl/README.md) | [巴西葡萄牙语](../pt-BR/README.md) | [葡萄牙语（葡萄牙）](../pt-PT/README.md) | [旁遮普语（古鲁穆奇）](../pa/README.md) | [罗马尼亚语](../ro/README.md) | [俄语](../ru/README.md) | [塞尔维亚语（西里尔字母）](../sr/README.md) | [斯洛伐克语](../sk/README.md) | [斯洛文尼亚语](../sl/README.md) | [西班牙语](../es/README.md) | [斯瓦希里语](../sw/README.md) | [瑞典语](../sv/README.md) | [他加禄语（菲律宾语）](../tl/README.md) | [泰米尔语](../ta/README.md) | [泰卢固语](../te/README.md) | [泰语](../th/README.md) | [土耳其语](../tr/README.md) | [乌克兰语](../uk/README.md) | [乌尔都语](../ur/README.md) | [越南语](../vi/README.md)

> **更喜欢本地克隆？**
>
> 本仓库包含50多种语言的翻译，显著增加了下载体积。若要不下载翻译内容进行克隆，请使用稀疏检出：
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
> 这样可以更快下载，包含完成课程所需的全部内容。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->