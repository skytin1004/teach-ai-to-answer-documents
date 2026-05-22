# 教AI基于您的文档回答问题
## 系列2：端到端构建本地开源RAG系统

![本地开源RAG教程流程](../../../assets/images/series-2-local-rag.svg)

> 本文将系列1的架构讨论转化为可运行的本地RAG教程。目标是先用示例数据构建完整工作流程，无需云账户和机密信息，然后基于这个工作基线进行更好的架构决策。

我们将构建的系统是一个小型学校政策助手。我使用两个本地Markdown文档作为知识库，然后演示完整的RAG流程：分块、本地嵌入、Qdrant向量存储、检索、重排序、带来源的答案合成，以及可选的使用Ollama和Phi-4-mini进行本地生成。

系列导航：[仓库主页](../README.md) | 上一篇：[系列1 - RAG、Azure与开源替代方案，以及微调何时有意义](./series-1-rag-azure-open-source-fine-tuning.md)

笔记本：[series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | 依赖：[open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> 如果您想在创建云资源前理解RAG流程，这是最佳起点。默认路径在本地运行，使用CPU友好的嵌入，无需机密信息。

## 1. 我们要构建的内容

在2023年的教程中，我从Azure开始，因为目标是展示如何使用Azure AI Search和Azure OpenAI从PDF文档中回答问题。

对于2026年的本系列，我想从更基础的层面开始。

在使用托管服务前，我想本地构建一个小型RAG系统，让每一步都可见：加载文档、分块文本、存储向量、检索证据、重新排序结果、返回带来源的答案。

示例场景是学校政策助手。用户提问：

```text
Can I use generative AI for my final assignment?
```

系统不应从通用模型记忆中回答。它应该检索相关的政策部分，并基于该证据回答。

完整可运行版本见[series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)。代码如下展示了主要步骤，方便将本文作为教程阅读。

## 2. 安装本地依赖

创建虚拟环境，安装系列2所需依赖：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

第一个版本使用Qdrant本地模式和FastEmbed。Qdrant的Python客户端支持内存中的本地模式 `QdrantClient(":memory:")`，适合本地教程和CI式验证。FastEmbed提供了真正的本地嵌入模型，无需云端API密钥。

依赖文件还包含`python-dotenv`，因为笔记本可以选择性读取`.env`中的Ollama模型名。本地教程不需要Azure OpenAI或OpenAI API密钥。

## 3. 加载示例文档

示例语料故意设置为很小：

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

在笔记本中，我加载了`sample_data/`下所有Markdown文件：

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

运行时加载了2个文档。体积小，便于手动检查，对于构建第一个版本的RAG流程非常有用。

## 4. 按Markdown标题进行分块

下一步是将文档拆分为块。

本教程中，我使用Markdown标题作为结构信号。文档标题取自`#`，每个章节块取自`##`。

> [!NOTE]
> 分块没有一刀切方案。此处用Markdown标题是因为示例文档有明显的`#`和`##`结构。PDF、Word文档、幻灯片、工单或网页，可能更好的策略是基于分页边界、布局信息、语义章节、令牌限制、表格或元数据。重点是选择能保留含义和可追踪性的分块策略。

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

然后对每个文档应用：

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

本地运行时，我创建了8个分块。

我喜欢这一步的原因是元数据已经很有用。每个分块都知道其`source`、`sectionHeading`、`documentVersion`和占位的`permissions`。即使是小型教程，也让引用和后续权限感知的检索更容易理解。

## 5. 创建本地嵌入

首次公开版本，我使用FastEmbed调用`BAAI/bge-small-en-v1.5`。

这保持教程本地且CPU友好，不过仍是实打实的嵌入模型，而非占位向量函数。首次运行会下载模型权重，之后笔记本可复用本地缓存。

> [!NOTE]
> 我选择`BAAI/bge-small-en-v1.5`，因为它是轻量级的英文嵌入模型，适合FastEmbed和Qdrant本地教程使用。生成384维向量，保持示例快速且费用低。这不是唯一的好选择。2023年许多教程用托管嵌入模型如`text-embedding-ada-002`。如今，新一代托管模型如OpenAI的`text-embedding-3-small`和`text-embedding-3-large`，开源模型如BGE、E5、MiniLM、Nomic Embed，以及多语种模型`BAAI/bge-m3`，都在不同工作负载下是合理选项。生产环境应根据自有文档的检索评估选择合适嵌入模型。

一些实用替代：

| 模型系列 | 适用情况 |
| --- | --- |
| `text-embedding-ada-002` | 2023年广泛出现的老托管基线，今天不建议作为默认新教程选项。 |
| `text-embedding-3-small` | 现代托管默认，适合追求性价比且不限制本地嵌入的场景。 |
| `text-embedding-3-large` | 当检索质量比向量大小或成本更重要时的托管选项。 |
| `BAAI/bge-small-en-v1.5` | 本地英文轻量基线，适合教程、原型及CPU优先实验。 |
| `BAAI/bge-base-en-v1.5` 或 `BAAI/bge-large-en-v1.5` | 需要更好检索质量且能承担更多计算时的本地英文大模型。 |
| `BAAI/bge-m3` | 多语种或更长上下文检索，特别是文档不只英文时。 |
| `sentence-transformers/all-MiniLM-L6-v2` | 极小且快速的语义搜索基线。适用于速度和简洁最优先的情况。 |
| `nomic-embed-text-v1.5` | 开源本地嵌入，适合更长上下文或注重可移植性的方案测试。 |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

然后为每个分块生成嵌入：

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. 在Qdrant本地模式存储向量

现在创建内存中的Qdrant集合，并插入带laden附件的分块。

> [!NOTE]
> 2023教程中用FAISS，因为它是展示本地向量相似度搜索的简单流行方式，适合LangChain。FAISS适合快速本地实验。2026版本我用Qdrant，想让教程更接近生产RAG系统。Qdrant支持将向量与文件源、章节标题、文档版本和权限等元数据一起存储，方便检查检索结果，也为过滤、引用和未来持久或服务器部署做准备。

FAISS适合展示向量相似度搜索。Qdrant适合展示带有生产特征的RAG检索层。

一些实用替代：

| 向量存储/搜索层 | 适用情况 |
| --- | --- |
| Qdrant | 本地原型、元数据过滤、生产级向量搜索和简单Python流程。 |
| Chroma | 快速本地RAG实验和笔记本，适合简洁优先。 |
| FAISS | 只需相似度搜索，可单独管理元数据时的轻量本地向量搜索。 |
| Milvus | 团队准备运营专门向量数据库时的大规模开源向量搜索。 |
| Weaviate | 支持schema、元数据、混合搜索的向量搜索，有托管与自托管选项。 |
| Azure AI Search | 想要集成关键词搜索、向量搜索、混合检索、语义排序、过滤、安全和托管操作的一站式企业RAG。 |
| PostgreSQL + pgvector | 已用PostgreSQL的团队，想让向量搜索紧邻应用数据。 |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

然后插入点：

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

我跑时，集合插入了8个向量。

这里RAG系统开始可视化。向量数据库不仅存向量，还存证据文本和引用所需元数据。

## 7. 检索候选分块

现在提出问题，检索候选分块。

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

此时我打印检索到的分块再生成答案。这非常重要。若检索出错，生成的流畅文本只会掩盖问题。

## 8. 添加轻量级重排序器

初测检索路径时，单纯向量相似度能找到相关政策内容，但最精确章节不总是排首位。

所以我添加了本地小型重排序器。当问题词与章节标题和内容重叠时，额外加权。

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

重排序后，首位结果是：

```text
school_ai_policy.md / Final Assignments
```

是测试问题预期的章节。

这是首个实现里最有用的教训。即使是很小的本地示例，结合向量相似度和其它信号能提升检索质量。

## 9. 组合有据可依的本地答案

默认路径，我使用透明的本地答案合成器，而非大语言模型。

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

这并非最终产品答案生成器，而是调试工具。证实检索、元数据和引用连接功能正常后，才加模型可变性。

## 10. 使用Ollama和Phi-4-mini生成本地答案

一旦检索奏效，笔记本可用Ollama和`phi4-mini:3.8b`替换最终生成答案步骤。

> [!NOTE]
> Ollama应只替换最终答案生成步骤。文档加载、分块、向量存储、检索、重排序和引用线路保持不变。

笔记本先基于检索分块构建证据提示：

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

本教程推荐通过Ollama使用微软Phi-4-mini系列作为默认本地生成选项。在Ollama中，我测试的模型名是：

```powershell
ollama pull phi4-mini:3.8b
```

可快速检查模型是否可用：

```powershell
ollama list
```

然后设置变量：

```powershell
Copy-Item .env.example .env
```

打开`.env`，取消注释系列2的Ollama配置：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

笔记本用`python-dotenv`加载仓库根目录的`.env`，再将相同证据提示发送到Ollama本地`/api/chat`接口，禁用流式输出。如果Ollama未运行或缺少`SERIES2_OLLAMA_MODEL`，则跳过此路径。

> [!NOTE]
> 本机上，`phi4-mini:3.8b`模型文件约2.49GB。推理时，Ollama报告加载模型3.3GB，使用了RTX 3060笔记本GPU。

教程提供两种级别：

1. 纯CPU的确定性答案合成器。
2. 搭配Ollama和Phi-4-mini的本地答案生成。

检索流程两者一致。

## 11. 验证结果

我在Windows上用Python 3.12.6本地运行了此笔记本。

安装包版本：

| 包 | 版本 |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

笔记本执行：

- 笔记本文件：`notebooks/series-2-open-source-rag.ipynb`
- 执行结果：`nbclient`成功执行
- 加载文档数：2
- 创建分块数：8
- Qdrant集合名：`school_policy_local`
- 插入向量数：8
- 嵌入模型：`BAAI/bge-small-en-v1.5`
- 嵌入维度：384
- 检索问题: “我可以在期末作业中使用生成式 AI 吗？”
- 重排序路径: 轻量级本地词汇重排序
- 重排序后排名最高的检索来源: `school_ai_policy.md`
- 重排序后排名最高的检索章节: `期末作业`
- 默认答案路径: 本地透明答案合成器
- Ollama 生成路径: 使用 `phi4-mini:3.8b` 完成
- Ollama 模型文件大小: 磁盘上 2.49GB
- Ollama 加载模型大小: `ollama ps` 报告为 3.3GB
- GPU 卸载: `ollama ps` 报告 100% GPU
- 生成后观察到的 GPU 内存: RTX 3060 笔记本 GPU 上约用 3.5GB / 6GB
- 运行缓存的 FastEmbed 模型和启用 Ollama 生成的笔记本: 通过验证脚本约 34 秒内完成

Ollama 生成的答案是:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

我不会称这个答案为完美。它基于正确的证据进行回答，但最后的来源行没有确定性引用格式那么精确。在教程中展示这点很有用，因为它使得下一个工程问题显而易见：答案生成也需要评估，而不仅仅是检索。

我在验证过程中学到的主要内容是，应该在答案生成之前检查检索质量。嵌入结果已经很有用，轻量级重排序器使预期的政策章节可靠地排在第一位。这正是我希望教程暴露的那种小系统行为，而不是隐藏起来。

## 12. 接下来是什么

下一步改进是将这个本地设置与相同学校政策助手场景的 Azure 托管版本进行比较。保持场景不变将使权衡更容易看到：设置复杂度、检索控制、身份集成、运营所有权和成本。

## 13. 参考资料

- [Qdrant Python 客户端快速入门](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant 客户端 GitHub 仓库](https://github.com/qdrant/qdrant-client)
- [FastEmbed 支持的模型](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI 嵌入指南](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 模型卡](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 模型卡](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 模型卡](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini 模型页](https://ollama.com/library/phi4-mini)
- [Ollama Windows 文档](https://docs.ollama.com/windows)
- [Ollama API 流式传输文档](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct 模型卡](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph 概览](https://docs.langchain.com/oss/python/langgraph)
- [RAG 介绍 - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

上一篇: [系列 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->