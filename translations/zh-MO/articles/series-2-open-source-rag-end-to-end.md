# 教授 AI 根據您的文件回答問題
## 系列 2：從頭到尾構建本地開源 RAG 系統

![本地開源 RAG 教程流程](../../../assets/images/series-2-local-rag.svg)

> 本文將系列 1 的架構討論轉化為可運行的本地 RAG 教程。目標是先用範例數據構建完整工作流程，不用雲帳戶，也沒有機密資訊，然後使用該工作基線在後續做出更好的架構決策。

我們將構建的系統是一個小型的學校政策助理。我使用兩個本地 Markdown 文件作為知識庫，然後演示完整的 RAG 流程：切塊、本地嵌入、Qdrant 向量存儲、檢索、重排名、基於來源的答案組合，以及使用 Ollama 和 Phi-4-mini 的本地生成（可選）。

系列導航：[倉庫首頁](../README.md) | 上一篇：[系列 1 - RAG、Azure 與開源替代方案，以及何時微調更合適](./series-1-rag-azure-open-source-fine-tuning.md)

筆記本：[series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | 需求：[open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> 如果你想在創建雲端資源之前了解 RAG 流程，這是最好的起點。預設路徑在本地執行，採用 CPU 友好的嵌入，無需機密資訊。

## 1. 我們要構建的東西

在 2023 年的教程中，我從 Azure 開始，因為目標是展示如何使用 Azure AI 搜索和 Azure OpenAI 從 PDF 文檔中回答問題。

而在這個 2026 年的系列中，我想從更底層開始。

在使用托管服務之前，我想構建一個小型的本地 RAG 系統，並使每一步都清晰可見：加載文件、切塊文本、存儲向量、檢索證據、重排名結果，以及返回基於來源的答案。

範例場景是學校政策助理。用戶提問：

```text
Can I use generative AI for my final assignment?
```

系統不應直接從通用模型記憶中回答。它應該檢索相關的政策部分，並根據該證據回答。

完整的可運行版本在 [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)。以下程式碼顯示了主要步驟，便於將本文作為教程閱讀。

## 2. 安裝本地依賴

創建虛擬環境並安裝系列 2 的需求：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

第一個版本使用 Qdrant 本地模式和 FastEmbed。Qdrant 的 Python 客戶端支持使用 `QdrantClient(":memory:")` 進行記憶體中的本地模式，非常適合本地教程和 CI 式驗證。FastEmbed 則提供真正的本地嵌入模型，無需雲端 API 鍵。

需求文件中還包括了 `python-dotenv`，因為筆記本可選地從 `.env` 中讀取 Ollama 模型名稱。本地教程無需 Azure OpenAI 或 OpenAI API 金鑰。

## 3. 加載範例文件

範例語料庫刻意很小：

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

在筆記本中，我從 `sample_data/` 加載所有 Markdown 文件：

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

當我執行筆記本時，載入了 2 份文件。這個數量足夠小，可手動檢查，對構建第一版 RAG 流程非常有用。

## 4. 按 Markdown 標題切塊

下一步是將文檔分割成多個塊。

在本教程中，我使用 Markdown 標題作為結構信號。標題使用 `#` 代表文件標題，每個章節塊使用 `##`。

> [!NOTE]
> 切塊方法沒有一種通用標準。在本教程中使用 Markdown 標題，是因為示例文檔有明顯的 `#` 和 `##` 結構。對於 PDF、Word、簡報、工單或網頁，更好的策略可能需要使用頁面邊界、布局信息、語義分段、令牌限制、表格或元數據。重點是選擇能保持意義和來源可追溯的切塊策略。

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

然後我將其應用於每個文件：

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

在我的本地執行中，產生了 8 個塊。

我喜歡這一步的原因是元數據已經很有用。每個塊都知道自己的 `source`、`sectionHeading`、`documentVersion` 和佔位符 `permissions`。即使在小型教程中，這也使後續的引用和權限感知檢索更容易理解。

## 5. 創建本地嵌入

公開的第一版使用 `BAAI/bge-small-en-v1.5`，通過 FastEmbed 加載。

這保持教程在本地且 CPU 友好，但依然使用真實的嵌入模型，而非簡單的向量函數。第一次運行會下載模型權重，之後筆記本可重用本地快取。

> [!NOTE]
> 我使用 `BAAI/bge-small-en-v1.5`，因為它是一款輕量的英語嵌入模型，配合 FastEmbed 和 Qdrant 本地教程使用效果佳。它創建 384 維的向量，使該示例快速且本地運行成本低廉。這不是唯一的好選擇。2023 年許多教程使用托管的嵌入模型如 `text-embedding-ada-002`。如今，更新的托管選項包括 OpenAI 的 `text-embedding-3-small` 和 `text-embedding-3-large`，以及開源選項如 BGE、E5、MiniLM、Nomic Embed 和多語言模型如 `BAAI/bge-m3`，根據工作負載均是合理選擇。生產中，應根據你自己的文檔通過檢索評估挑選合適的嵌入模型。

一些實用替代選擇：

| 模型系列 | 考慮使用的場合 |
| --- | --- |
| `text-embedding-ada-002` | 較舊的托管基線，2023 年很多教程中出現過。今天我不會將其設為新教程的預設。 |
| `text-embedding-3-small` | 現代托管預設，適合在追求良好成本/效能平衡且不需純本地嵌入時使用。 |
| `text-embedding-3-large` | 當檢索質量比向量大小或嵌入成本更重要時的托管選擇。 |
| `BAAI/bge-small-en-v1.5` | 輕量的本地英語基線，適合教程、原型和 CPU 友好實驗。 |
| `BAAI/bge-base-en-v1.5` 或 `BAAI/bge-large-en-v1.5` | 想要更好檢索質量且能支援更多計算的更大型本地英語模型。 |
| `BAAI/bge-m3` | 多語言或長上下文檢索，特別是文件不僅是英語時。 |
| `sentence-transformers/all-MiniLM-L6-v2` | 非常小且快速的語意搜尋基線，特別適合速度和簡易性最重要的場合。 |
| `nomic-embed-text-v1.5` | 開放本地嵌入選項，值得檢測於長上下文或注重可攜性環境。 |

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

接著給每個塊產生嵌入：

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

## 6. 使用 Qdrant 本地模式存儲向量

現在創建一個記憶體中 Qdrant 集合，並插入帶有元數據的塊。

> [!NOTE]
> 在 2023 年的教程中，我使用 FAISS，因為它是展示使用 LangChain 進行本地向量相似度搜尋的簡單且流行的方式。FAISS 仍適合快速的本地實驗。在這個 2026 版本中，我選擇 Qdrant，是因為我希望教程更貼近生產環境的 RAG 系統。Qdrant 讓我可以將向量和源文件、章節標題、文件版本與權限等元數據存放在一起。這讓檢索更容易檢視，並為篩選、引用與未來的持久化或服務器部署做好準備。

FAISS 適合展示向量相似搜尋，而 Qdrant 更適合展示小型但具備生產風格的 RAG 檢索層。

實用替代方案：

| 向量存儲 / 搜索層 | 考慮使用的場合 |
| --- | --- |
| Qdrant | 本地原型、元數據篩選、適合生產的向量搜索，以及簡單的 Python 工作流程。 |
| Chroma | 快速本地 RAG 實驗和筆記本，簡易性最重要時。 |
| FAISS | 當我只需要相似性搜索且可獨立管理元數據時，輕量的本地向量搜索。 |
| Milvus | 團隊已準備操作專用向量數據庫時的更大規模開源向量搜索。 |
| Weaviate | 支援模式、元數據、混合搜索，以及托管或自托管部署的向量搜索。 |
| Azure AI Search | 希望在 Azure 上獲得關鍵詞搜索、向量搜索、混合檢索、語義排序、篩選、安全性和托管操作整合一層的企業級 RAG。 |
| PostgreSQL + pgvector | 已使用 PostgreSQL 的團隊，想將向量搜索靠近應用資料。 |

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

然後插入向量點：

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

我的運行中，集合插入了 8 個向量。

這裡是 RAG 系統開始變得可檢視的地方。向量資料庫不僅存向量，還存放證據文本及引用所需的元數據。

## 7. 檢索候選塊

現在提出問題並檢索候選塊。

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

此時，我打印檢索出的塊，然後才生成答案。這很重要，因為檢索錯誤時，生成只會用流暢語句掩蓋問題。

## 8. 新增輕量重排名器

我最初測試檢索路徑時，單用向量相似度會找到相關政策內容，但最精確的章節不一定排最前。

因此我加了一個小型本地重排名器。當問題詞語與章節標題和內容重合時，會額外加權。

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

重排名後，頂端結果變為：

```text
school_ai_policy.md / Final Assignments
```

這就是測試問題期望得到的章節。

這是第一次實作中最有用的教訓。即使在微小的本地範例中，將向量相似度和另一種信號結合，檢索質量也會改善。

## 9. 組合有根據的本地答案

預設路徑下，我使用透明的本地答案組合器，而不是大型語言模型。

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

這不是要作為最終產品的答案生成器，而是除錯工具。它證明在加入模型變化之前，檢索、元數據和引證接線能夠正常工作。

## 10. 使用 Ollama 和 Phi-4-mini 生成本地答案

檢索工作正常後，筆記本可以只替換最後的答案生成步驟，改用 Ollama 和 `phi4-mini:3.8b`。

> [!NOTE]
> Ollama 應只替換最後的答案生成步驟。文件加載、切塊、向量存儲、檢索、重排名和引用接線都應保持不變。

首先，筆記本基於檢索出的塊建立證據提示：

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

在本教程中，我推薦透過 Ollama 使用微軟的 Phi-4-mini 系列作為預設本地生成方案。筆記本測試的模型名稱是：

```powershell
ollama pull phi4-mini:3.8b
```

你可以快速檢查模型是否可用：

```powershell
ollama list
```

然後設定以下變數：

```powershell
Copy-Item .env.example .env
```

打開 `.env`，取消注釋系列 2 的 Ollama 相關設定：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

筆記本使用 `python-dotenv` 從倉庫根目錄加載 `.env`，然後將同樣的證據提示發送到 Ollama 本地 `/api/chat` 端點，並禁用串流功能。如果 Ollama 未運行或者缺少 `SERIES2_OLLAMA_MODEL`，這條路徑會跳過。

> [!NOTE]
> 在這臺機器上，`phi4-mini:3.8b` 下載了約 2.49GB 的模型文件。推理期間，Ollama 報告加載了 3.3GB 的模型大小，使用 RTX 3060 筆記型電腦 GPU。

這樣，本教程就有兩個層次：

1. 僅使用 CPU 的確定性答案組合器。
2. 使用 Ollama 和 Phi-4-mini 的本地答案生成。

兩者的檢索管線保持相同。

## 11. 驗證結果

我在 Windows 上使用 Python 3.12.6 本地執行了該筆記本。

安裝的套件：

| 套件 | 版本 |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

筆記本執行狀態：

- 筆記本檔案：`notebooks/series-2-open-source-rag.ipynb`
- 執行結果：通過 `nbclient` 檢驗
- 載入文件數：2
- 創建塊數：8
- Qdrant 集合名稱：`school_policy_local`
- 插入向量數：8
- 嵌入模型：`BAAI/bge-small-en-v1.5`
- 嵌入維度：384
- 檢索問題: 「我可以使用生成式 AI 來完成我的期末作業嗎？」
- 重排序路徑: 輕量本地詞彙重排序
- 重排序後最佳檢索來源: `school_ai_policy.md`
- 重排序後最佳檢索章節: `Final Assignments`
- 預設答案路徑: 本地透明答案合成器
- Ollama 生成路徑: 完成於 `phi4-mini:3.8b`
- Ollama 模型檔案大小: 磁碟上 2.49GB
- Ollama 已載入模型大小: `ollama ps` 報告為 3.3GB
- GPU 卸載: `ollama ps` 報告 100% GPU
- 生成後觀察 GPU 記憶體: RTX 3060 筆電 GPU 的 6GB 中約使用 3.5GB
- 以快取 FastEmbed 模型及啟用 Ollama 生成執行筆記本：通過驗證腳本約 34 秒

Ollama 生成的回答為：

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

我不會稱這個答案為完美。它是從正確證據來回答的，但最終來源行比確定性引用格式較不精確。這在教學中是有用的，因為它讓下一個工程問題變得明顯：答案生成也需要評估，不只是檢索。

我在驗證時學到的主要事情是：檢索品質應該在答案生成前被檢查。嵌入結果已經很有用，輕量重排序器使預期的政策章節可靠地排在第一。這正是我希望教學揭露而非隱藏的那種小系統行為。

## 12. 接下來的步驟

下一個改進是將此本地設置與同一學校政策助理場景的 Azure 管理版本做比較。保持場景不變應該會讓權衡更容易看出來：設置複雜度、檢索控制、身份整合、運營所有權與成本。

## 13. 參考資料

- [Qdrant Python 用戶快速入門](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant 用戶端 GitHub 倉庫](https://github.com/qdrant/qdrant-client)
- [FastEmbed 支援模型](https://qdrant.github.io/fastembed/examples/Supported_Models/)
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

先前文章：[系列 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->