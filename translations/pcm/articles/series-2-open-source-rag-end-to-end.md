# Teach AI to Answer Questions Based on Your Documents
## Series 2: Build a Local Open-Source RAG System End to End

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Dis article dey turn di Series 1 architecture discussion into one local RAG tutorial wey fit run. Di main aim na to build di full workflow first wit sample data, no cloud account, and no secrets, den use dat working baseline make betta architecture decisions later.

Di system we go build na small school policy assistant. I dey use two local Markdown documents as di knowledge base, den go waka through di full RAG pipeline: chunking, local embeddings, Qdrant vector storage, retrieval, reranking, source-aware answer composition, plus optional local generation wit Ollama and Phi-4-mini.

Series navigation: [Repository home](../README.md) | Previous: [Series 1 - RAG, Azure vs Open-Source Alternatives, and When Fine-Tuning Makes Sense](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Requirements: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Dis na di best starting point if you want understand di RAG pipeline before you begin create cloud resources. Di default path dey run locally wit CPU-friendly embeddings and no secrets.

## 1. Wetin We Dey Build

For di 2023 tutorial, I start from Azure because di goal na to show how Azure AI Search and Azure OpenAI fit answer questions from PDF documents.

For dis 2026 series, I wan start one layer lower.

Before I use managed services, I wan build small RAG system locally and make every step visible: loading documents, chunking text, storing vectors, retrieving evidence, reranking results, plus returning one source-aware answer.

Di sample scenario na school policy assistant. Di user go ask:

```text
Can I use generative AI for my final assignment?
```

Di system no suppose answer from general model memory. E suppose retrieve di relevant policy section and answer from dat evidence.

Di full runnable version dey for [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Di code wey dey below go show di main steps make dis article fit read like tutorial.

## 2. Install di Local Dependencies

Create virtual environment and install di Series 2 requirements:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Di first version dey use Qdrant local mode and FastEmbed. Qdrant Python client dey support one in-memory local mode wit `QdrantClient(":memory:")`, wey dey useful for local tutorials and CI-style verification. FastEmbed give us real local embedding model wey no need cloud API key.

Di requirements file still get `python-dotenv` because di notebook fit optionally read Ollama model name from `.env`. No Azure OpenAI or OpenAI API key dey needed for dis local tutorial.

## 3. Load di Sample Documents

Di sample corpus purposely small:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

For di notebook, I load all Markdown files from `sample_data/`:

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

When I run di notebook, e load 2 documents. Dat one small enough so you fit check am manually, wey dey useful when you dey build di first version of RAG pipeline.

## 4. Chunk by Markdown Headings

Next step na to split documents into chunks.

For dis tutorial, I dey use Markdown headings as di structure signal. Di document title dey come from `#`, and each section chunk dey come from `##`.

> [!NOTE]
> Chunking no be one-size-fits-all. For dis tutorial, I dey use Markdown headings because di sample documents get clear `#` and `##` structure. For PDFs, Word documents, slides, tickets, or web pages, better strategy fit use page boundaries, layout info, semantic sections, token limits, tables, or metadata. Di important thing na to choose chunking strategy wey go preserve meaning and source traceability for your documents.

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

Den I apply am to every document:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Dis one create 8 chunks for my local run.

Wetin I like about dis step na say di metadata don dey useful well. Each chunk sabi its `source`, `sectionHeading`, `documentVersion`, and placeholder `permissions`. Even for small tutorial, dis one make citations and later permission-aware retrieval easier to reason about.

## 5. Create Local Embeddings

For di first public version, I dey use `BAAI/bge-small-en-v1.5` through FastEmbed.

Dis one keep di tutorial local and CPU-friendly, but e still use real embedding model instead of placeholder vector function. Di first run go download di model weights. After dat, di notebook fit reuse di local cache.

> [!NOTE]
> I dey use `BAAI/bge-small-en-v1.5` because e lightweight English embedding model wey work well with FastEmbed and Qdrant for local tutorial. E create 384-dimensional vectors, wey dey keep di example fast and cheap to run locally. Dis no be di only beta choice. For 2023, many tutorials dey use hosted embedding models like `text-embedding-ada-002`. Today, newer hosted options like OpenAI `text-embedding-3-small` and `text-embedding-3-large`, plus open-source options like BGE, E5, MiniLM, Nomic Embed, and multilingual models like `BAAI/bge-m3` dey all reasonanble depending on workload. For production, di right embedding model suppose select through retrieval evaluation with your own documents.

Some practical alternatives:

| Model family | When I go consider am |
| --- | --- |
| `text-embedding-ada-002` | Older hosted baseline wey show for many 2023-era tutorials. I no go choose am as default for new tutorial today. |
| `text-embedding-3-small` | Modern hosted default when I want strong cost/performance balance and no need local-only embeddings. |
| `text-embedding-3-large` | Hosted option when retrieval quality matter pass vector size or embedding cost. |
| `BAAI/bge-small-en-v1.5` | Lightweight local English baseline for tutorials, prototypes, and CPU-friendly experiments. |
| `BAAI/bge-base-en-v1.5` or `BAAI/bge-large-en-v1.5` | Bigger local English models when I want better retrieval quality and fit afford more compute. |
| `BAAI/bge-m3` | Multilingual or longer-context retrieval, especially when documents no dey only English. |
| `sentence-transformers/all-MiniLM-L6-v2` | Very small and fast semantic search baseline. Useful when speed and simplicity matter most. |
| `nomic-embed-text-v1.5` | Open local embedding option wey worth testing, especially for longer-context or portability-focused setups. |

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

Den each chunk go get embedding:

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

## 6. Store Vectors in Qdrant Local Mode

Now we create in-memory Qdrant collection and insert di chunks with payload metadata.

> [!NOTE]
> For 2023 tutorial, I use FAISS because e simple and popular way to show local vector similarity search wit LangChain. FAISS still dey useful for fast local experiments. For dis 2026 version, I use Qdrant because I want di tutorial to feel closer to production RAG system. Qdrant let me store vectors plus payload metadata like source file, section heading, document version, and permissions. Dis one make retrieval easier to inspect and prepare di example for filtering, citations, and future persistent or server-based deployment.

FAISS dey good to show vector similarity search. Qdrant better to show small but production-shaped RAG retrieval layer.

Some practical alternatives:

| Vector store / search layer | When I go consider am |
| --- | --- |
| Qdrant | Local prototypes, metadata filtering, production-friendly vector search, and simple Python workflow. |
| Chroma | Quick local RAG experiments and notebooks where simplicity matter most. |
| FAISS | Lightweight local vector search when I only need similarity search and fit handle metadata separately. |
| Milvus | Bigger-scale open-source vector search when team ready to run dedicated vector database. |
| Weaviate | Vector search with schema, metadata, hybrid search, and managed or self-hosted deployment options. |
| Azure AI Search | Enterprise RAG on Azure when I want keyword search, vector search, hybrid retrieval, semantic ranking, filtering, security, and managed operations inside one search layer. |
| PostgreSQL + pgvector | Teams wey dey already use PostgreSQL wey want vector search close to application data. |

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

Den insert di points:

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

For my run, di collection insert 8 vectors.

Na here RAG system begin dey inspectable. Vector database no dey just store vectors; e dey store di evidence text plus di metadata wey needed for citations.

## 7. Retrieve Candidate Chunks

Now we ask di question and retrieve candidate chunks.

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

At dis point, I dey print di retrieved chunks before I generate answer. Dis one important. If retrieval wrong, di generation go just hide di problem behind fluent text.

## 8. Add Lightweight Reranker

When I first test di retrieval path, vector similarity alone fit find related policy content, but di most precise section no always dey top.

So I add small local reranker. E dey give extra weight when question terms overlap wit section heading and content.

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

After reranking, di top result become:

```text
school_ai_policy.md / Final Assignments
```

Dat one na di expected section for di test question.

Dis na di most useful lesson from di first implementation. Even for tiny local example, retrieval quality improve wen I combine vector similarity wit another signal.

## 9. Compose Grounded Local Answer

For default path, I dey use transparent local answer composer instead of LLM.

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

Dis one no suppose be final product answer generator. E be debugging tool. E prove say retrieval, metadata, and citation wiring dey work before you add model variability.

## 10. Generate Local Answer wit Ollama and Phi-4-mini

Once retrieval dey work, di notebook fit replace only di final answer step wit Ollama and `phi4-mini:3.8b`.

> [!NOTE]
> Ollama suppose replace only di final answer-generation step. Document loading, chunking, vector storage, retrieval, reranking, and citation wiring suppose remain same.

First, di notebook build evidence prompt from di retrieved chunks:

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

For dis tutorial, I recommend Microsoft's Phi-4-mini family through Ollama as default local generation option. For Ollama, di model name wey I test na:

```powershell
ollama pull phi4-mini:3.8b
```

You fit quick check say di model dey available:

```powershell
ollama list
```

Den set these variables:

```powershell
Copy-Item .env.example .env
```

Open `.env` and uncomment di Series 2 Ollama values:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Di notebook load `.env` from repository root wit `python-dotenv`, den send di same evidence prompt to Ollama local `/api/chat` endpoint wit streaming disabled. If Ollama no dey run or `SERIES2_OLLAMA_MODEL` dey miss, dis track go skip.

> [!NOTE]
> For dis machine, `phi4-mini:3.8b` download about 2.49GB model files. During inference, Ollama report 3.3GB loaded model size and use di RTX 3060 Laptop GPU.

Dis one give di tutorial two levels:

1. CPU-only deterministic answer composer.
2. Local answer generation wit Ollama and Phi-4-mini.

Di retrieval pipeline remain di same for both.

## 11. Verification Result

I run di notebook locally for Windows wit Python 3.12.6.

Installed packages:

| Package | Version |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Notebook execution:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Execution result: pass wit `nbclient`
- Documents loaded: 2
- Chunks created: 8
- Qdrant collection: `school_policy_local`
- Vectors inserted: 8
- Embedding model: `BAAI/bge-small-en-v1.5`
- Embedding size: 384
- Retrieval question: "Fit I use generative AI for my final assignment?"
- Reranking path: lightweight local lexical reranking
- Top retrieved source after reranking: `school_ai_policy.md`
- Top retrieved section after reranking: `Final Assignments`
- Default answer path: local transparent answer composer
- Ollama generation path: completed with `phi4-mini:3.8b`
- Ollama model file size: 2.49GB on disk
- Ollama loaded model size: 3.3GB reported by `ollama ps`
- GPU offload: 100% GPU reported by `ollama ps`
- GPU memory observed after generation: about 3.5GB of 6GB used on RTX 3060 Laptop GPU
- Notebook execution with cached FastEmbed model and Ollama generation enabled: passed in about 34 seconds through the verification script

The Ollama-generated answer was:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

I no go call dis answer perfect. E answer from correct evidence, but di final source line no too exact like di deterministic citation format. E dey useful to show for di tutorial because e make di next engineering question clear: answer generation need evaluation too, no be only retrieval.

Di main tins wey I learn while I dey verify dis na say retrieval quality suppose dey check before answer generation. Di embedding result don already useful, and di lightweight reranker make di expected policy section show first steady. Na di kain small system behavior I want di tutorial show make e no hide.

## 12. Wetin Go Happen Next

Di next improvement na to compare dis local setup with managed Azure version of di same school policy assistant scenario. If dem keep di scenario stable e go make di tradeoffs easier to understand: setup complexity, retrieval controls, identity integration, operational ownership, and cost.

## 13. References

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub repository](https://github.com/qdrant/qdrant-client)
- [FastEmbed supported models](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 model card](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 model card](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini model page](https://ollama.com/library/phi4-mini)
- [Ollama Windows documentation](https://docs.ollama.com/windows)
- [Ollama API streaming documentation](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct model card](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph)
- [Introduction to RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Previous: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->