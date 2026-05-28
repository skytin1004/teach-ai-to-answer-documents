# 教AI根据您的文档回答问题 - 系列计划

此计划跟踪公开的系列1和系列2发布。后续的Azure和评估工作将作为草稿保存，直到示例完全端到端并经过验证。

未经明确指示，请勿提交或推送更改。

## 公开范围

当前公开发布：

- 系列1文章：RAG架构决策，Azure与开源权衡，以及微调的定位。
- 系列2文章：本地开源RAG教程。
- 系列2笔记本：可运行的本地RAG实验，包含FastEmbed、Qdrant、Ollama和Phi-4-mini。
- 示例数据：学校政策和课程AI指导的Markdown文件。

已草拟但尚未列入公开索引：

- Azure AI搜索和Azure OpenAI重建。
- RAG评估和回归检查。

## 教程场景

共享场景为学校政策助手。

助手根据本地文档回答此问题：

```text
Can I use generative AI for my final assignment?
```

预期行为为：

1. 加载本地Markdown文档。
2. 按标题解析并分块。
3. 创建本地嵌入并存储带元数据的可搜索表示。
4. 检索相关政策部分。
5. 在需要时重新排序。
6. 生成或撰写有依据的答案。
7. 返回引用来源。
8. 记录验证结果。

## 当前公开结构

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

草稿材料存放于`drafts/`目录，直到准备好公开索引前，仓库验证会跳过该目录。

## 系列2验证

在Windows上使用Python 3.12.6验证。

- 成功安装`requirements/open-source-rag.txt`。
- 使用`nbclient`执行`notebooks/series-2-open-source-rag.ipynb`。
- 本地验证通过：加载2个示例文档，创建8个分块，FastEmbed生成384维的本地嵌入，初始化Qdrant内存集合，并插入8个向量。
- 测试问题：“我可以为期末作业使用生成式AI吗？”
- 轻量重新排序后检索到的顶部来源：`school_ai_policy.md`。
- 轻量重新排序后检索到的顶部部分：`Final Assignments`。
- 默认回答路径：本地透明答案撰写者。
- 通过winget安装Ollama；成功拉取`phi4-mini:3.8b`。
- Ollama回答生成路径：使用`phi4-mini:3.8b`完成。
- Ollama模型文件大小：磁盘约2.49GB。
- Ollama加载模型大小：`ollama ps`报告3.3GB。
- GPU卸载：在RTX 3060笔记本GPU上，`ollama ps`报告100% GPU使用率。
- 生成后GPU内存观察：约3.5GB，满载为6GB。
- 使用缓存的FastEmbed模型和启用Ollama生成的笔记本执行约34秒，通过了验证脚本。
- 观察到一次早期文档加载错误地包含了`sample_data/README.md`；笔记本现在只显式加载两个预期的示例文档。

## 仓库验证

- `scripts/verify_notebooks.py`验证本地Markdown链接、笔记本JSON、笔记本输出清洁度以及高风险密钥模式。
- `scripts/verify_notebooks.py --execute`从仓库根目录运行公开笔记本。
- `drafts/`目录下的草稿材料故意跳过。

## 下一步工作

- 使用Azure AI搜索和Azure OpenAI重建相同场景，作为未来系列的一部分。
- 一旦本地和Azure实现均稳定，添加检索和答案评估。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->