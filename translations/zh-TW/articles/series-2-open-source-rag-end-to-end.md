# 教 AI 根據您的文件回答問題
## 系列 2：從頭建立本地開源 RAG 系統

![本地開源 RAG 教程流程](../../../assets/images/series-2-local-rag.svg)

> 本文將系列 1 的架構討論轉換為一個可執行的本地 RAG 教程。目標是先使用範例資料構建完整工作流程，無需雲端帳戶和密鑰，然後再利用這個工作基線進行更好的架構決策。

我們將建立的系統是一個小型校園政策助理。我使用兩個本地 Markdown 文件作為知識庫，然後演示完整的 RAG 流程：分塊、本地嵌入、Qdrant 向量存儲、檢索、重排序、來源感知的答案組合，以及可選的使用 Ollama 和 Phi-4-mini 進行本地生成。

系列導航：[存儲庫主頁](../README.md) | 上一篇：[系列 1 - RAG、Azure 與開源替代方案，以及何時適合微調](./series-1-rag-azure-open-source-fine-tuning.md)

筆記本：[series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | 需求清單：[open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> 如果您想在建立雲端資源前先了解 RAG 流程，這是最佳的起點。預設流程在本地運行，採用 CPU 友善的嵌入技術，無需密鑰。

## 1. 我們要建立什麼

在 2023 年的教程中，我從 Azure 開始，因為目標是展示如何使用 Azure AI Search 和 Azure OpenAI 從 PDF 文件中回答問題。

對於這個 2026 年的系列，我想從更底層開始。

在使用管理服務之前，我想先在本地建立一個小型 RAG 系統，並讓每一個步驟都可見：載入文件、分塊文本、儲存向量、檢索證據、重排序結果以及返回來源感知的答案。

範例場景是一個校園政策助理。使用者會問：

```text
Can I use generative AI for my final assignment?
```

系統不應從一般模型記憶回答，而應檢索相關政策章節，並根據該證據回答。

完整可執行版本位於 [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)。以下程式碼展示主要步驟，方便本文可作為教程閱讀。

## 2. 安裝本地依賴

建立虛擬環境並安裝系列 2 的需求：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

第一個版本使用 Qdrant 本地模式和 FastEmbed。Qdrant 的 Python 用戶端支援 `QdrantClient(":memory:")` 的記憶體本地模式，適合本地教程和 CI 風格驗證。FastEmbed 提供真實的本地嵌入模型，無需雲端 API 密鑰。

需求文件也包含 `python-dotenv`，因為筆記本可選讀取 `.env` 中的 Ollama 模型名稱。本地教程不需 Azure OpenAI 或 OpenAI API 密鑰。

## 3. 載入範例文件

樣本語料特意很小：

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

在筆記本中，我載入了 `sample_data/` 下的所有 Markdown 檔案：

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

我執行筆記本時，載入了 2 個文件。這樣足夠小，可以手動檢查，對建立第一版 RAG 流程很有用。

## 4. 以 Markdown 標題分塊

下一步是將文件切分成塊。

本教程用 Markdown 標題作為結構信號。文件標題來自 `#`，每個章節分塊來自 `##`。

> [!NOTE]
> 分塊沒有一體適用的策略。此處我用 Markdown 標題是因為範例文件有明確的 `#` 和 `##` 結構。對 PDF、Word 文件、簡報、工單或網頁，較好的方式可能會用頁面邊界、版面資訊、語意章節、Token 限制、表格或元資料。重點是選擇保留意義與來源追蹤的分塊策略。

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

然後套用於每個文件：

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

本地執行中產生了 8 個分塊。

我喜歡這個步驟的原因是元資料已經很有用。每個分塊知道自己的 `source`、`sectionHeading`、`documentVersion` 和佔位符 `permissions`。即使是一個小教程，也讓引用和後續依權限檢索變得更容易理解。

## 5. 建立本地嵌入

第一個公開版本使用 FastEmbed 透過 `BAAI/bge-small-en-v1.5`。

這讓教程保留本地、CPU 友善，但仍是實際的嵌入模型，而非佔位向量函數。首次執行會下載模型權重，之後可重用本地快取。

> [!NOTE]
> 我使用 `BAAI/bge-small-en-v1.5`，因為它是輕量且效果良好的英文嵌入模型，適合 FastEmbed 和 Qdrant 的本地教程。它產生 384 維向量，使例子快速且在本地運行成本低。這不是唯一好選擇。2023 年許多教程使用像是 `text-embedding-ada-002` 的託管嵌入模型。現在，更新的託管選擇有 OpenAI 的 `text-embedding-3-small` 和 `text-embedding-3-large`，開源選項則有 BGE、E5、MiniLM、Nomic Embed 和多語言模型如 `BAAI/bge-m3`，取決工作負載皆是合理選擇。生產環境中，應通過檢索評估選擇最適合您文件的嵌入模型。

一些實用替代方案：

| 模型系列 | 我會考慮的情境 |
| --- | --- |
| `text-embedding-ada-002` | 較舊且在許多 2023 年教程中出現的託管基準。如今不會預設選它做新教程。 |
| `text-embedding-3-small` | 現代託管預設選項，當我想兼顧成本/效能且無需本地嵌入時。 |
| `text-embedding-3-large` | 託管選擇，在檢索品質比向量大小或成本更重要時使用。 |
| `BAAI/bge-small-en-v1.5` | 輕量級本地英文基準，適合教學、原型和 CPU 友善試驗。 |
| `BAAI/bge-base-en-v1.5` 或 `BAAI/bge-large-en-v1.5` | 想要更好檢索品質與有更多計算資源時可用較大的本地英文模型。 |
| `BAAI/bge-m3` | 多語言或長上下文檢索，特別是文檔不只英文時。 |
| `sentence-transformers/all-MiniLM-L6-v2` | 非常小而快速的語義搜索基準。當速度和簡單為首要時有用。 |
| `nomic-embed-text-v1.5` | 值得嘗試的開源本地嵌入，適合長上下文或強調可攜性的設置。 |

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

接著為每個分塊取得嵌入：

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

## 6. 在 Qdrant 本地模式中存儲向量

現在建立一個記憶體 Qdrant 集合，並插入帶有載荷元資料的分塊。

> [!NOTE]
> 2023 年教程中，我使用了 FAISS，因為它是示範 LangChain 本地向量相似度搜尋的簡單且流行方案。FAISS 仍是快速本地實驗的利器。在 2026 版本，我改用 Qdrant，因為我想讓教程更貼近生產用 RAG 系統。Qdrant 可讓我將向量與來源文件、章節標題、文件版本和權限等載荷元資料一起儲存。這讓檢索更容易檢查，也為過濾、引用與未來持久或伺服器部署打下基礎。

FAISS 適合展示向量相似搜尋。Qdrant 適合示範小型但生產形態的 RAG 檢索層。

一些實用替代方案：

| 向量存儲／搜尋層 | 我會考慮的情境 |
| --- | --- |
| Qdrant | 本地原型、元資料過濾、生產友善的向量搜尋與簡單 Python 工作流程。 |
| Chroma | 快速本地 RAG 實驗及以簡便為主的筆記本。 |
| FAISS | 輕量本地向量搜尋，當只需相似度搜尋且可另管元資料時。 |
| Milvus | 較大規模開源向量搜尋，團隊準備操作專用向量資料庫時。 |
| Weaviate | 向量搜尋含結構、元資料、混合搜尋，及託管或自架選項。 |
| Azure AI Search | 在 Azure 上企業級 RAG，需關鍵字搜尋、向量搜尋、混合檢索、語意排序、過濾、安全性與託管操作整合時。 |
| PostgreSQL + pgvector | 已使用 PostgreSQL 的團隊，想將向量搜尋與應用資料鄰近整合時。 |

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

然後插入資料點：

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

我本地執行插入了 8 個向量。

這是 RAG 系統開始可檢視的階段。向量資料庫不僅儲存向量，還儲存了證據文本及引用所需的元資料。

## 7. 檢索候選分塊

現在詢問問題並檢索候選分塊。

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

此時我會在生成答案前印出檢索分塊。這很重要，因為檢索錯誤時，生成只會以流暢文字掩蓋問題。

## 8. 加入輕量重排序器

初測檢索時，純向量相似度能找出相關政策內容，但最精確章節不一定排在最前。

所以我加入一個小型本地重排序器。當問題詞彙與章節標題和內容有重疊時，給予額外加權。

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

重排序後，首個結果變成：

```text
school_ai_policy.md / Final Assignments
```

這正是測試問題對應的預期章節。

這是首次實作最有價值的教訓。即使在微小本地範例，結合向量相似度和其他訊號可提升檢索品質。

## 9. 組合本地有根據答案

預設路徑，我使用透明的本地答案組合器，而非大語言模型。

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

這非最終產品的答案生成器，而是除錯工具。它證明檢索、元資料及引用銜接在新增模型變異前可正常運作。

## 10. 使用 Ollama 和 Phi-4-mini 生成本地答案

檢索正常後，筆記本可只替換最終答案步驟為 Ollama 和 `phi4-mini:3.8b`。

> [!NOTE]
> Ollama 應只替換最終答案生成步驟。文件載入、分塊、向量存儲、檢索、重排序和引用銜接都保持不變。

首先，筆記本根據檢索到的分塊建立證據提示：

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

本教程推薦透過 Ollama 使用微軟 Phi-4-mini 系列作為預設本地生成方案。我測試的模型名稱是：

```powershell
ollama pull phi4-mini:3.8b
```

您可快速檢查模型是否可用：

```powershell
ollama list
```

然後設定這些變數：

```powershell
Copy-Item .env.example .env
```

打開 `.env` 並取消註解系列 2 的 Ollama 相關設定：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

筆記本透過 `python-dotenv` 載入存儲庫根目錄的 `.env`，然後將相同的證據提示傳送至 Ollama 本地的 `/api/chat` 端點，並禁用串流。如果 Ollama 未運行或缺少 `SERIES2_OLLAMA_MODEL`，則略過該路徑。

> [!NOTE]
> 本機器下載 `phi4-mini:3.8b` 模型檔約 2.49GB。推理時 Ollama 報告載入了 3.3GB 大小模型，並使用 RTX 3060 筆電 GPU。

本教程提供兩層：

1. 僅用 CPU 的決定性答案組合器。
2. 使用 Ollama 和 Phi-4-mini 的本地答案生成。

兩者皆使用相同的檢索流程。

## 11. 驗證結果

我在 Windows 環境，搭配 Python 3.12.6 本地執行此筆記本。

已安裝套件：

| 套件名稱 | 版本 |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

筆記本執行狀況：

- 筆記本：`notebooks/series-2-open-source-rag.ipynb`
- 執行結果：使用 `nbclient` 通過
- 載入文件數：2
- 建立分塊數：8
- Qdrant 集合名稱：`school_policy_local`
- 插入向量數：8
- 嵌入模型：`BAAI/bge-small-en-v1.5`
- 嵌入維度：384
- 檢索問題：「我可以在期末作業中使用生成式 AI 嗎？」
- 重排序路徑：輕量級本地詞彙重排序
- 重排序後最佳檢索來源：`school_ai_policy.md`
- 重排序後最佳檢索章節：`Final Assignments`
- 預設答案路徑：本地透明答案組合器
- Ollama 生成路徑：使用 `phi4-mini:3.8b` 完成
- Ollama 模型檔案大小：磁碟上 2.49GB
- Ollama 載入模型大小：`ollama ps` 報告 3.3GB
- GPU 卸載：`ollama ps` 報告 100% GPU
- 生成後觀察到 GPU 記憶體：RTX 3060 筆電 GPU 的 6GB 中約使用 3.5GB
- 使用快取 FastEmbed 模型並啟用 Ollama 生成的筆記本執行：通過驗證腳本約 34 秒

Ollama 生成的答案是：

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

我不會稱這個答案為完美。它是基於正確的證據回答，但最後的來源行不像確定性引用格式那麼精確。這在教學中很有用，因為它讓下一個工程問題變得明顯：答案生成也需要評估，而不只是檢索。

在驗證過程中我學到的主要一點是，應該先檢查檢索品質，再進行答案生成。嵌入結果已經有用，輕量級重排序器使預期的政策章節可靠地排在第一位。這正是我希望教學能揭露而非隱藏的小系統行為。

## 12. 接下來的步驟

下一個改進是將這個本地設置與同樣學校政策助理場景的管理型 Azure 版本進行比較。保持場景固定應該能更清楚地看到權衡：設置複雜度、檢索控管、身份整合、營運所有權和成本。

## 13. 參考資料

- [Qdrant Python 用戶快速入門](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant 用戶端 GitHub 倉庫](https://github.com/qdrant/qdrant-client)
- [FastEmbed 支援的模型](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI 嵌入指南](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 模型卡](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 模型卡](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 模型卡](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini 模型頁面](https://ollama.com/library/phi4-mini)
- [Ollama Windows 文件](https://docs.ollama.com/windows)
- [Ollama API 串流文件](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct 模型卡](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph 概述](https://docs.langchain.com/oss/python/langgraph)
- [RAG 介紹 - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

上篇：[系列 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->