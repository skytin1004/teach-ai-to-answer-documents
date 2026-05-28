# 教 AI 根据您的文档回答问题

![基于文档的 AI RAG 系统概述](../../assets/images/readme-hero.svg)

本仓库收集了 2026 年关于使用 RAG、Azure AI 服务、开源替代方案及面向评估的工作流程构建基于文档的 AI 系统的系列博客。

## 背景

2023 年，我制作了两篇教程，讲解如何使用 Azure AI 搜索和 Azure OpenAI 教 ChatGPT 从 PDF 文档中回答问题。“ChatGPT 基于您的数据”这个理念当时仍然很新，目标是展示一个实用的工作流程：存储文档、建立索引、检索相关内容，并从检索上下文生成答案。

到了 2026 年，RAG 生态系统发展得更为庞大。Azure AI 搜索支持现代向量和混合检索模式，Azure OpenAI 是微软 Foundry 模型生态系统的一部分，而 LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama 和 vLLM 等开源工具也成为了构建实际系统的实用选择。

这正是我想重新探讨这个话题的原因。问题已不再仅是“如何构建 RAG？”现在有很多构建方法，更重要的问题变成了“针对我的具体情况，该选择哪种架构？”

本系列从决策层面开始，然后转向实践教程。第一个实现路径构建一个任何人都可以运行的本地开源 RAG 系统，使用示例数据、Qdrant、Ollama 和 Phi-4-mini。

## 文章

文章索引请参见 [articles/README.md](./articles/README.md)。

1. [系列 1：RAG、Azure 与开源替代方案及何时进行微调](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [系列 2：端到端构建本地开源 RAG 系统](./articles/series-2-open-source-rag-end-to-end.md)

接下来内容：

- 使用 Azure AI 搜索和 Azure OpenAI 重建相同的 RAG 系统。
- 添加超越演示答案的评估和回归检查。

## 笔记本

实现文章使用笔记本，便于直接检查检索与评估步骤。有关文件夹级别的指导，请参见 [notebooks/README.md](./notebooks/README.md)。

> [!TIP]
> 如果想要最快的路径，请从系列 2 开始。它使用示例数据在本地运行，CPU 友好的嵌入，Qdrant 本地模式，且不需要云凭据。

| 系列 | 笔记本 | 依赖要求 | 本地验证 |
| --- | --- | --- | --- |
| 系列 2 | [开源 RAG 笔记本](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | 验证了 Qdrant 本地模式、检索、重排序和来源链路 |

要在本地运行笔记本，请创建虚拟环境并安装对应的依赖文件。例如：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## 示例数据

笔记本使用 [sample_data](../../sample_data) 文件夹中的小型本地语料库，因此可以在无私有文档或云凭据环境中运行示例。详情见 [sample_data/README.md](./sample_data/README.md)。

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## 本地验证总结

验证结果记录于各篇文章和 [SERIES_PLAN.md](./SERIES_PLAN.md) 中。

| 区域 | 结果 |
| --- | --- |
| 系列 2 开源路径 | FastEmbed 生成了 384 维本地嵌入，Qdrant 内存集合插入了 8 个向量，轻量级重排序检索到了预期章节；可选 Ollama 生成使用 `phi4-mini:3.8b` 完成 |

本地笔记本刻意避免硬编码敏感信息。

## 本地 Ollama 生成

系列 2 笔记本默认本地安全。要启用本地 Ollama 生成，将 [.env.example](../../.env.example) 复制为 `.env` 并填写系列 2 对应数值。

系列 2 Ollama 生成需要取消注释：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

系列 2 笔记本通过 `python-dotenv` 自动加载仓库根目录下的 `.env` 文件。

> [!IMPORTANT]
> 切勿提交 `.env` 文件、API 密钥、私有端点或租户特定值。仓库故意将密钥排除在 Markdown 文件和笔记本之外。

依赖要求文件记录见 [requirements/README.md](./requirements/README.md)。

要验证链接、笔记本结构、笔记本输出清洁度以及高风险密钥模式：

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

验证脚本文档见 [scripts/README.md](./scripts/README.md)。

要在相同环境中执行所有本地安全的笔记本：

```powershell
python scripts\verify_notebooks.py --execute
```

相同的验证流程会在 GitHub Actions 中于代码提交、拉取请求及手动触发运行。草稿文章与笔记本故意排除于公开验证路径之外。

发布更新前，请参考 [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)。

查看当前未发布变更总结，请见 [CHANGELOG.md](./CHANGELOG.md)。

贡献及笔记本维护指南见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 多语言支持

### 通过协作翻译器支持（自动且始终最新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯语](../ar/README.md) | [孟加拉语](../bn/README.md) | [保加利亚语](../bg/README.md) | [缅甸语 (Myanmar)](../my/README.md) | [中文 (简体)](./README.md) | [中文 (繁体，香港)](../zh-HK/README.md) | [中文 (繁体，澳门)](../zh-MO/README.md) | [中文 (繁体，台湾)](../zh-TW/README.md) | [克罗地亚语](../hr/README.md) | [捷克语](../cs/README.md) | [丹麦语](../da/README.md) | [荷兰语](../nl/README.md) | [爱沙尼亚语](../et/README.md) | [芬兰语](../fi/README.md) | [法语](../fr/README.md) | [德语](../de/README.md) | [希腊语](../el/README.md) | [希伯来语](../he/README.md) | [印地语](../hi/README.md) | [匈牙利语](../hu/README.md) | [印尼语](../id/README.md) | [意大利语](../it/README.md) | [日语](../ja/README.md) | [坎纳达语](../kn/README.md) | [高棉语](../km/README.md) | [韩语](../ko/README.md) | [立陶宛语](../lt/README.md) | [马来语](../ms/README.md) | [马拉雅拉姆语](../ml/README.md) | [马拉地语](../mr/README.md) | [尼泊尔语](../ne/README.md) | [尼日利亚皮钦语](../pcm/README.md) | [挪威语](../no/README.md) | [波斯语 (法尔斯语)](../fa/README.md) | [波兰语](../pl/README.md) | [巴西葡萄牙语](../pt-BR/README.md) | [欧洲葡萄牙语](../pt-PT/README.md) | [旁遮普语 (古鲁穆奇)](../pa/README.md) | [罗马尼亚语](../ro/README.md) | [俄语](../ru/README.md) | [塞尔维亚语 (西里尔)](../sr/README.md) | [斯洛伐克语](../sk/README.md) | [斯洛文尼亚语](../sl/README.md) | [西班牙语](../es/README.md) | [斯瓦希里语](../sw/README.md) | [瑞典语](../sv/README.md) | [他加禄语 (菲律宾语)](../tl/README.md) | [泰米尔语](../ta/README.md) | [泰卢固语](../te/README.md) | [泰语](../th/README.md) | [土耳其语](../tr/README.md) | [乌克兰语](../uk/README.md) | [乌尔都语](../ur/README.md) | [越南语](../vi/README.md)

> **偏好本地克隆？**
>
> 本仓库包含 50 多种语言翻译，显著增加了下载大小。若要克隆时排除翻译，可以使用稀疏检出：
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
> 这会给你完成课程所需的全部内容，下载速度更快。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->