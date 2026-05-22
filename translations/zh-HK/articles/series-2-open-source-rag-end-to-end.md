# 教 AI 根據你的文件回答問題
## 系列 2：從頭開始構建本地開源 RAG 系統

![本地開源 RAG 教程流程](../../../assets/images/series-2-local-rag.svg)

> 本文將系列1的架構討論轉化為可運行的本地 RAG 教程。目標是先用範例數據構建整個工作流程，無需雲端帳號和密鑰，然後用這個運作基線做更好的架構決策。

我們將構建的系統是一個小型的學校政策助理。我使用兩個本地 Markdown 文件作為知識庫，然後演示完整的 RAG 流程：分塊、本地嵌入、Qdrant 向量存儲、檢索、重新排序、帶來源意識的答案合成，以及可選的使用 Ollama 和 Phi-4-mini 進行的本地生成。

系列導航：[倉庫首頁](../README.md) | 上一篇：[系列1 - RAG，Azure 與開源替代方案，以及何時微調合適](./series-1-rag-azure-open-source-fine-tuning.md)

筆記本：[series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | 需求：[open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> 如果你想了解 RAG 流程但還未準備創建雲端資源，這是最佳起點。預設路徑在本地運行，使用 CPU 友好的嵌入且無密鑰。

## 1. 我們要構建什麼

在 2023 年的教程中，我是從 Azure 開始，因為目標是展示 Azure AI Search 和 Azure OpenAI 如何從 PDF 文件回答問題。

而這個 2026 系列，我想從更底層開始。

在使用托管服務之前，我想在本地構建一個小型 RAG 系統，並使每個步驟都可見：載入文件、分塊文本、存儲向量、檢索證據、重新排序結果，以及返回帶來源的答案。

範例情境是一個學校政策助理。使用者詢問：

```text
Can I use generative AI for my final assignment?
```

系統不應該從通用模型記憶中回答。它應檢索相關政策章節，並從該證據作答。

完整可運行版本在 [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)。以下程式碼展示主要步驟，讓本文可作為教學閱讀。

## 2. 安裝本地依賴

建立虛擬環境並安裝系列2需求：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

第一版使用 Qdrant 本地模式和 FastEmbed。Qdrant 的 Python 客戶端支持用 `QdrantClient(":memory:")` 建立內存本地模式，適合本地教程和 CI 式驗證。FastEmbed 提供了真實本地的嵌入模型，無需雲端 API 金鑰。

需求檔中還包含 `python-dotenv`，因為筆記本可選從 `.env` 讀取 Ollama 模型名稱。本地教程不需 Azure OpenAI 或 OpenAI API 密鑰。

## 3. 載入範例文件

範例語料故意很小：

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

在筆記本中，我載入 `sample_data/` 內所有 Markdown 文件：

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

我執行時載入了 2 份文件。這麼小方便手工檢查，對建立第一版 RAG 流程很有幫助。

## 4. 以 Markdown 標題分塊

下一步是把文件分成塊。

本教程採用 Markdown 標題作為結構訊號。文件標題來自 `#`，每節分塊來自 `##`。

> [!NOTE]
> 分塊無萬用方法。本教程因範例文件具明確 `#` 和 `##` 結構，故採用 Markdown 標題。對 PDF、Word、投影片、票務或網頁，可能用頁面邊界、排版資訊、語義分段、字元限制、表格或元資料更合適。重點是選擇保存語義和來源可追蹤性的分塊策略。

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

然後應用到每份文件：

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

我的本地執行創建了 8 個分塊。

我喜歡這步驟的地方是元資料已經很有用。每個分塊都知道 `source`、`sectionHeading`、`documentVersion` 和佔位的 `permissions`。即使在小型教程，這讓引用和後續依權限檢索更易理解。

## 5. 創建本地嵌入

首個公開版本，我用 `BAAI/bge-small-en-v1.5` 配合 FastEmbed。

這保持教程本地且 CPU 友好，但仍是實際嵌入模型，不是佔位向量。首輪會下載模型權重，以後筆記本可重用本地快取。

> [!NOTE]
> 我使用 `BAAI/bge-small-en-v1.5`，因它是輕量英文嵌入模型，配合 FastEmbed 和 Qdrant 本地教程表現良好。產生 384 維向量，使範例在本地運行快速且成本低。這不是唯一好選擇。2023 年多數教程用過托管嵌入如 `text-embedding-ada-002`。現今新版托管選項如 OpenAI `text-embedding-3-small` 和 `text-embedding-3-large`，開源選項如 BGE、E5、MiniLM、Nomic Embed，以及多語言模型 `BAAI/bge-m3`，依工作負載均有合理用途。生產環境應通過自己文件的檢索評估選對嵌入模型。

實用替代：

| 模型家族 | 我會考慮的時機 |
| --- | --- |
| `text-embedding-ada-002` | 2023 年常見的舊托管基準，不會是我新教程的預設選。 |
| `text-embedding-3-small` | 現代托管預設，成本效益平衡且不需本地嵌入時用。 |
| `text-embedding-3-large` | 檢索品質比向量大小或嵌入成本更重要時選用。 |
| `BAAI/bge-small-en-v1.5` | 教程、原型、CPU 友好測試的輕量本地英文基準。 |
| `BAAI/bge-base-en-v1.5` 或 `BAAI/bge-large-en-v1.5` | 想要更好檢索質量且能負擔更多計算時的大型本地模型。 |
| `BAAI/bge-m3` | 多語言或長語境檢索，尤其文件不只是英文。 |
| `sentence-transformers/all-MiniLM-L6-v2` | 極小且快速的語義搜索基準，當速度與簡單性最重要時用。 |
| `nomic-embed-text-v1.5` | 開源本地嵌入選項，值得在長語境或可攜性配置中測試。 |

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

每個分塊綁定嵌入向量：

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

## 6. 在 Qdrant 本地模式中存向量

現在建立一個內存 Rdrant 集合，並插入帶載荷元數據的分塊。

> [!NOTE]
> 2023 教程我用 FAISS，因其在 LangChain 中示範本地向量相似度搜索簡單且普及。FAISS 對快速本地測試仍很有用。這個 2026 版本，我用 Qdrant 希望教程更接近生產 RAG 系統。Qdrant 讓我能和載荷元資料（如來源文件、章節標題、文件版本和權限）一同存向量，方便檢視及後續過濾、引用和未來持久化或伺服器佈署。

FAISS 很適合示範向量相似搜索；Qdrant則是示範小型且近生產化的 RAG 檢索層更好。

實用替代方案：

| 向量庫 / 搜索層 | 我會考慮的時機 |
| --- | --- |
| Qdrant | 本地原型、元資料過濾、生產友好向量搜索，以及簡單 Python 工作流。 |
| Chroma | 快速本地 RAG 實驗和筆記本，當簡單性最關鍵。 |
| FAISS | 輕量本地向量搜索，只需相似度搜索且能獨立管理元資料時。 |
| Milvus | 團隊準備運維專用向量庫時使用的較大規模開源向量搜索。 |
| Weaviate | 支持結構、元資料、混合搜索，且有管理或自主部署的向量搜索。 |
| Azure AI Search | 企業級 RAG，想要關鍵詞搜索、向量搜索、混合檢索、語義排名、過濾、安全，以及單一管理層服務。 |
| PostgreSQL + pgvector | 已在用 PostgreSQL，想要離應用資料更近的向量搜索的團隊。 |

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

插入向量點：

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

我執行時集合插入了 8 個向量。

這裡 RAG 系統開始可被檢視。向量庫不只是存向量，也存有證據文本和引用所需的元資料。

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

此時我印出檢索到的分塊再生成答案。這很重要。若檢索錯誤，生成只會用流暢文本掩蓋問題。

## 8. 增加輕量重新排序器

測試檢索路徑時，我發現向量相似度雖能找相關政策內容，但最精確章節不一定在首位。

因此我加了小型本地重新排序器。當問題詞與章節標題及內容重疊時給予額外權重。

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

重新排序後，首位結果是：

```text
school_ai_policy.md / Final Assignments
```

這是測試問題的預期章節。

這是第一版實作最寶貴的教訓。即使是微小本地例子，結合向量相似度和另一信號能提升檢索質量。

## 9. 組合有根據的本地答案

預設路徑，我使用透明本地答案合成器而非 LLM。

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

這不是最終產品的答案生成器，而是除錯工具。證明檢索、元資料和引用連結在加模型變異前可正常運作。

## 10. 使用 Ollama 和 Phi-4-mini 生成本地答案

確認檢索運作後，筆記本可只換答案生成步驟，使用 Ollama 和 `phi4-mini:3.8b`。

> [!NOTE]
> Ollama 僅應替換最後答案生成步驟。文件載入、分塊、向量存儲、檢索、重新排序和引用連結應保持不變。

首先筆記本從檢索分塊建立證據提示：

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

本教程推薦使用 Microsoft 的 Phi-4-mini 家族透過 Ollama 作為預設本地生成選項。測試的模型名稱是：

```powershell
ollama pull phi4-mini:3.8b
```

你可快速檢查模型是否可用：

```powershell
ollama list
```

然後設定變數：

```powershell
Copy-Item .env.example .env
```

打開 `.env` 並取消註解系列 2 的 Ollama 值：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

筆記本用 `python-dotenv` 從倉庫根目錄載入 `.env`，再將相同證據提示發送到 Ollama 本地 `/api/chat` 端點，關閉流式輸出。若 Ollama 未啟動或缺少 `SERIES2_OLLAMA_MODEL`，會跳過此路徑。

> [!NOTE]
> 本機上，`phi4-mini:3.8b` 下載了約 2.49GB 模型檔案。推理時，Ollama 報告模型大小為 3.3GB，並使用了 RTX 3060 Laptop GPU。

教程提供兩個層次：

1. 僅 CPU 的確定性答案合成器。
2. 使用 Ollama 和 Phi-4-mini 的本地答案生成。

兩者檢索流程相同。

## 11. 驗證結果

我在 Windows 上使用 Python 3.12.6 本地執行筆記本。

安裝套件：

| 套件 | 版本 |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

筆記本執行：

- 筆記本：`notebooks/series-2-open-source-rag.ipynb`
- 執行結果：通過 `nbclient`
- 載入文件：2
- 創建分塊：8
- Qdrant 集合名稱：`school_policy_local`
- 插入向量數：8
- 嵌入模型：`BAAI/bge-small-en-v1.5`
- 嵌入維度：384
- 檢索問題：「我可以使用生成式 AI 來完成我的期末作業嗎？」
- 重新排序路徑：輕量級本地詞彙重排序
- 重新排序後的頂尖檢索來源：`school_ai_policy.md`
- 重新排序後的頂尖檢索段落：`Final Assignments`
- 預設回答路徑：本地透明的答案組合器
- Ollama 生成路徑：使用 `phi4-mini:3.8b` 完成
- Ollama 模型檔案大小：磁碟上 2.49GB
- Ollama 已載入模型大小：`ollama ps` 報告為 3.3GB
- GPU 卸載：`ollama ps` 報告 100% GPU
- 生成後觀察到的 GPU 記憶體：RTX 3060 筆電 GPU 6GB 中約使用 3.5GB
- 啟用快取 FastEmbed 模型及 Ollama 生成的筆記本執行：通過驗證腳本約 34 秒

Ollama 生成的答案為：

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

我不會稱這個答案為完美。它從正確的證據回答，但最終來源行不像確定性引用格式那樣精確。這在教程中是有用的，因為它使下一個工程問題變得明顯：答案生成也需要評估，而不僅僅是檢索。

我在驗證過程中學到的主要事情是應該先檢查檢索品質，再進行答案生成。嵌入結果已經很有用，輕量級重排序器使預期的政策段落可靠地排在第一。這正是我希望教程揭示而非隱藏的那種系統小行為。

## 12. 接下來的步驟

下一步改進是將此本地設置與相同校園政策助理場景的受管理 Azure 版本進行比較。保持場景固定應該使取捨更容易看清：設置複雜度、檢索控制、身份整合、運營所有權和成本。

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
- [LangGraph 概覽](https://docs.langchain.com/oss/python/langgraph)
- [RAG 說明 - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

之前：[系列 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->