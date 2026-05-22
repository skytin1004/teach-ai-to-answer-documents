# ਆਪਣੇ ਦਸਤਾਵੇਜ਼ਾਂ ਦੇ ਆਧਾਰ 'ਤੇ ਪ੍ਰਸ਼ਨਾਂ ਦਾ ਜਵਾਬ ਦੇਣ ਲਈ AI ਨੂੰ ਸਿਖਾਓ
## ਸਿਰੀਜ਼ 2: ਇੱਕ ਸਥਾਨਕ ਖੁੱਲ੍ਹਾ-ਸਰੋਤ RAG ਸਿਸਟਮ ਐਂਡ-ਟੂ-ਐਂਡ ਬਣਾਓ

![ਸਥਾਨਕ ਖੁੱਲ੍ਹਾ-ਸਰੋਤ RAG ਟਿਊਟੋਰિયલ ਪਾਈਪਲਾਈਨ](../../../assets/images/series-2-local-rag.svg)

> ਇਹ ਲੇਖ ਸਿਰੀਜ਼ 1 ਆਰਕੀਟੈਕਚਰ ਚਰਚਾ ਨੂੰ ਇੱਕ ਚਲਾਉਣ ਯੋਗ ਸਥਾਨਕ RAG ਟਿਊਟੋਰિયલ ਵਿੱਚ ਬਦਲਦਾ ਹੈ। ਟੀਚਾ ਹੈ ਪਹਿਲਾਂ ਸੈਂਪਲ ਡੇਟਾ ਨਾਲ ਪੂਰਾ ਵਰਕਫਲੋ ਬਣਾਉਣਾ, ਕੋਈ ਕਲਾਉਡ ਖਾਤਾ ਜਾਂ ਸੰਦਿ ਰਹਿਤ, ਅਤੇ ਫਿਰ ਇਸ ਕੰਮ ਕਰਨ ਵਾਲੇ ਬੇਸਲਾਈਨ ਨੂੰ ਬਿਹਤਰ ਆਰਕੀਟੈਕਚਰ ਫੈਸਲੇ ਕਰਨ ਲਈ ਵਰਤਣਾ।

ਅਸੀਂ ਜੋ ਸਿਸਟਮ ਬਣਾਉਣ ਜਾ ਰਹੇ ਹਾਂ ਉਹ ਇੱਕ ਛੋਟਾ ਸਕੂਲ ਨੀਤੀ ਸਹਾਇਕ ਹੈ। ਮੈਂ ਦੋ ਸਥਾਨਕ ਮਾਰਕਡਾਊਨ ਦਸਤਾਵੇਜ਼ਾਂ ਨੂੰ ਗਿਆਨ ਅਧਾਰ ਵਜੋਂ ਵਰਤਦਾ ਹਾਂ, ਫਿਰ ਪੂਰੀ RAG ਪਾਈਪਲਾਈਨ ਦੁਆਰਾ ਚੱਲਦਾ ਹਾਂ: ਚੰਕਿੰਗ, ਸਥਾਨਕ ਐਮਬੈੱਡਿੰਗ, Qdrant ਵੇਕਟਰ ਸਟੋਰੇਜ, ਰੀਟਰੀਵਲ, ਰੀਰੈਂਕਿੰਗ, ਸੋਰਸ-ਅਗਾਹ ਜਵਾਬ ਸੰਯੋਜਨ, ਅਤੇ ਵਿਕਲਪਕ ਸਥਾਨਕ ਜਨਰੇਸ਼ਨ ਓਲਾਮਾ ਅਤੇ Phi-4-mini ਨਾਲ।

ਸਿਰੀਜ਼ ਨੇਵੀਗੇਸ਼ਨ: [ਰਿਪੋਜ਼ਟਰੀ ਹੋਮ](../README.md) | ਪਹਿਲਾਂ: [ਸਿਰੀਜ਼ 1 - RAG, Azure ਵਿਰੁੱਧ ਖੁੱਲ੍ਹਾ-ਸਰੋਤ ਵਿਕਲਪ, ਅਤੇ ਜਦੋਂ ਫਾਈਨ-ਟਿਊਨਿੰਗ ਠੀਕ ਹੈ](./series-1-rag-azure-open-source-fine-tuning.md)

ਨੋਟਬੁੱਕ: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | ਲੋੜੀਂਦੀਆਂ ਚੀਜ਼ਾਂ: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> ਜੇ ਤੁਸੀਂ ਕਲਾਉਡ ਸਰੋਤ ਬਣਾਉਣ ਤੋਂ ਪਹਿਲਾਂ RAG ਪਾਈਪਲਾਈਨ ਨੂੰ ਸਮਝਣਾ ਚਾਹੁੰਦੇ ਹੋ ਤਾਂ ਇਹ ਸਭ ਤੋਂ ਵਧੀਆ ਸ਼ੁਰੂਆਤ ਬਿੰਦੂ ਹੈ। ਡੀਫੌਲਟ ਰਸਤਾ ਸੀਪੀਯੂ-ਮਿੱਤਰ ਐਮਬੈੱਡਿੰਗ ਨਾਲ ਸਥਾਨਕ ਰੂਪ ਵਿੱਚ ਚੱਲਦਾ ਹੈ ਅਤੇ ਕੋਈ ਸੰਦਿ ਨਹੀਂ ਵਰਤਦਾ।

## 1. ਅਸੀਂ ਕੀ ਬਣਾ ਰਹੇ ਹਾਂ

2023 ਟਿਊਟੋਰિયલ ਵਿੱਚ, ਮੈਂ ਐਜ਼ਿਊਰ ਤੋਂ ਸ਼ੁਰੂ ਕੀਤਾ ਕਿਉਂਕਿ ਟੀਚਾ ਸੀ ਦਿਖਾਣਾ ਕਿ ਕਿਵੇਂ Azure AI Search ਅਤੇ Azure OpenAI ਈ-PDF ਦਸਤਾਵੇਜ਼ਾਂ ਤੋਂ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਦੇ ਸਕਦੇ ਹਨ।

ਇਸ 2026 ਸਿਰੀਜ਼ ਲਈ, ਮੈਂ ਇੱਕ ਪੱਧਰ ਹੇਠਾਂ ਤੋਂ ਸ਼ੁਰੂ ਕਰਨਾ ਚਾਹੁੰਦਾ ਹਾਂ।

ਮੈਨੇਜਡ ਸੇਵਾਵਾਂ ਨੂੰ ਵਰਤਣ ਤੋਂ ਪਹਿਲਾਂ, ਮੈਂ ਇੱਕ ਛੋਟਾ RAG ਸਿਸਟਮ ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਬਣਾਉਣਾ ਚਾਹੁੰਦਾ ਹਾਂ ਅਤੇ ਹਰ ਕਦਮ ਨੂੰ ਦਿੱਖਾਉਣਾ ਚਾਹੁੰਦਾ ਹਾਂ: ਦਸਤਾਵੇਜ਼ ਲੋਡਿੰਗ, ਟੈਕਸਟ ਚੰਕਿੰਗ, ਵੇਕਟਰ ਸਟੋਰ ਕਰਨਾ, ਸਬੂਤ ਲੱਭਣਾ, ਨਤੀਜੇ ਰੀਰੈਂਕ ਕਰਨਾ, ਅਤੇ ਸੋਰਸ-ਅਗਾਹ ਜਵਾਬ ਵਾਪਸ ਕਰਨਾ।

ਸੈਂਪਲ ਪਰੀਪੇਖ ਇੱਕ ਸਕੂਲ ਨੀਤੀ ਸਹਾਇਕ ਹੈ। ਉਪਭੋਗਤਾ ਪੁੱਛਦਾ ਹੈ:

```text
Can I use generative AI for my final assignment?
```

ਸਿਸਟਮ ਨੂੰ ਆਮ ਮਾਡਲ ਮੈਮੋਰੀ ਤੋਂ ਜਵਾਬ ਨਹੀਂ ਦੇਣਾ ਚਾਹੀਦਾ। ਇਹ ਸਬੰਧਿਤ ਨੀਤੀ ਭਾਗ ਨੂੰ ਲੱਭ ਕੇ ਉਸ ਸਬੂਤ ਤੋਂ ਜਵਾਬ ਦੇਣਾ ਚਾਹੀਦਾ ਹੈ।

ਪੂਰਾ ਚਲਾਉਣ ਯੋਗ ਵਰਜਨ [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) ਵਿੱਚ ਹੈ। ਹੇਠਾਂ ਦਿੱਤਾ ਕੋਡ ਮੁੱਖ ਕਦਮ ਦਰਸਾਉਂਦਾ ਹੈ ਤਾਂ ਜੋ ਲੇਖ ਨੂੰ ਟਿਊਟੋਰியல் ਵਜੋਂ ਪੜ੍ਹਿਆ ਜਾ ਸਕੇ।

## 2. ਸਥਾਨਕ ਡਿਪੈਂਡੈਂਸੀਜ਼ ਇੰਸਟਾਲ ਕਰੋ

ਇਕ ਵਰਚੁਅਲ ਵਾਤਾਵਰਣ ਬਣਾਓ ਅਤੇ ਸਿਰੀਜ਼ 2 ਦੀਆਂ ਲੋੜੀਂਦੀਆਂ ਚੀਜ਼ਾਂ ਇੰਸਟਾਲ ਕਰੋ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

ਪਹਿਲਾ ਵਰਜਨ Qdrant ਦੀ ਸਥਾਨਕ ਮੋਡ ਅਤੇ FastEmbed ਵਰਤਦਾ ਹੈ। Qdrant ਦਾ ਪਾਈਥਨ ਕਲਾਇਟਸਟ `QdrantClient(":memory:")` ਨਾਲ ਇੱਕ ਸਮਰਥਿਤ ਇਨ-ਮੇਮੋਰੀ ਸਥਾਨਕ ਮੋਡ ਹੁੰਦਾ ਹੈ, ਜੋ ਸਥਾਨਕ ਟਿਊਟੋਰਿਯਲਾਂ ਅਤੇ CI-ਸਟਾਈਲ ਵੈਰੀਫਿਕੇਸ਼ਨ ਲਈ ਲਾਭਦਾਇਕ ਹੈ। FastEmbed ਸਾਨੂੰ ਇੱਕ ਅਸਲੀ ਸਥਾਨਕ ਐਮਬੈੱਡਿੰਗ ਮਾਡਲ ਦਿੰਦਾ ਹੈ ਬਿਨਾਂ ਕਿਸੇ ਕਲਾਉਡ API ਕੀ ਦੀ ਲੋੜ ਦੇ।

ਲੋੜੀਂਦੀਆਂ ਫਾਈਲ ਵਿੱਚ `python-dotenv` ਵੀ ਸ਼ਾਮਲ ਹੈ ਕਿਉਂਕਿ ਨੋਟਬੁੱਕ ਵਿਕਲਪਕ ਤੌਰ ਤੇ `.env` ਤੋਂ ਓਲਾਮਾ ਮਾਡਲ ਨਾਮ ਪੜ੍ਹ ਸਕਦੀ ਹੈ। ਇਸ ਸਥਾਨਕ ਟਿਊਟੋਰਿਯਲ ਲਈ Azure OpenAI ਜਾਂ OpenAI API ਕੀ ਦੀ ਲੋੜ ਨਹੀਂ ਹੈ।

## 3. ਸੈਂਪਲ ਦਸਤਾਵੇਜ਼ ਲੋਡ ਕਰੋ

ਸੈਂਪਲ ਕਾਪਸ ਬਜਾਵੇਂ ਛੋਟਾ ਹੈ:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

ਨੋਟਬੁੱਕ ਵਿੱਚ, ਮੈਂ ਸਾਰੇ ਮਾਰਕਡਾਊਨ ਫਾਈਲਾਂ `sample_data/` ਤੋਂ ਲੋਡ ਕਰਦਾ ਹਾਂ:

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

ਜਦੋਂ ਮੈਂ ਨੋਟਬੁੱਕ ਚਲਾਈ, ਇਸਨੇ 2 ਦਸਤਾਵੇਜ਼ ਲੋਡ ਕੀਤੇ। ਇਹ ਹੱਥੋਂ ਜਾਂਚਣ ਲਈ ਕਾਫੀ ਛੋਟਾ ਹੈ, ਜੋ ਪਹਿਲਾ RAG ਪਾਈਪਲਾਈਨ ਸੰਸਕਰਨ ਬਣਾਉਂਦੇ ਸਮੇਂ ਲਾਭਦਾਇਕ ਹੈ।

## 4. ਮਾਰਕਡਾਊਨ ਸਿਰਲੇਖਾਂ ਨਾਲ ਚੰਕ ਕਰੋ

ਅਗਲਾ ਕਦਮ ਦਸਤਾਵੇਜ਼ਾਂ ਨੂੰ ਚੰਕਾਂ ਵਿੱਚ ਵੰਡਣਾ ਹੈ।

ਇਸ ਟਿਊਟੋਰਿਯਲ ਲਈ, ਮੈਂ ਸਿੱਲਾ ਸਾਹਿਤ ਦੇ ਸਿਗਨਲ ਵਜੋਂ ਮਾਰਕਡਾਊਨ ਸਿਰਲੇਖਾਂ ਵਰਤਦਾ ਹਾਂ। ਦਸਤਾਵੇਜ਼ ਦਾ ਸਿਰਲੇਖ `#` ਤੋਂ ਆਉਂਦਾ ਹੈ, ਅਤੇ ਹਰ ਭਾਗ ਚੰਕ `##` ਤੋਂ ਆਉਂਦਾ ਹੈ।

> [!NOTE]
> ਚੰਕਿੰਗ ਹਰ ਜੋੜ ਲਈ ਇੱਕੋ ਜਿਹੀ ਨਹੀਂ ਹੁੰਦੀ। ਇਸ ਟਿਊਟੋਰਿਯਲ ਵਿੱਚ, ਮੈਂ ਮਾਰਕਡਾਊਨ ਸਿਰਲੇਖਾਂ ਵਰਤਦਾ ਹਾਂ ਕਿਉਂਕਿ ਸੈਂਪਲ ਦਸਤਾਵੇਜ਼ਾਂ ਵਿੱਚ ਸਾਫ `#` ਅਤੇ `##` ਸਿਰਲੇਖ ਬਣਾ ਹੈ। PDF, ਵਰਡ ਦਸਤਾਵੇਜ਼, ਸਮਾਰਟ ਇੰਟਰੈਕਟਿਵ ਭਾਗਾਂ, ਟਿਕਟਾਂ ਜਾਂ ਵੈੱਬ ਪੰਨਿਆਂ ਲਈ ਬਿਹਤਰ ਰਣਨੀਤੀ ਪੰਨਾ ਸੀਮਾ, ਲੇਆਉਟ ਜਾਣਕਾਰੀ, ਸੇਮਾਂਟਿਕ ਭਾਗ, ਟੋਕਨ ਸੀਮਾਵਾਂ, ਟੇਬਲਾਂ ਜਾਂ ਮੈਟਾਡੇਟਾ ਵਰਗੀ ਹੋ ਸਕਦੀ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਗੱਲ ਹੈ ਇਕ ਰਣਨੀਤੀ ਚੁਣੋ ਜੋ ਅਰਥ ਅਤੇ ਸਰੋਤ ਟ੍ਰੇਸਬਿਲਿਟੀ ਨੂੰ ਪੱਕਾ ਰੱਖਦੀ ਹੋਵੇ।

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

ਫਿਰ ਮੈਂ ਇਹ ਹਰ ਦਸਤਾਵੇਜ਼ 'ਤੇ ਲਾਗੂ ਕਰਦਾ ਹਾਂ:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

ਇਸ ਨਾਲ ਮੇਰੇ ਸਥਾਨਕ ਚਲਾਉਣ ਵਿੱਚ 8 ਚੰਕ ਬਣੇ।

ਇਸ ਕਦਮ ਦੀ ਜੋ ਗੱਲ ਮੈਨੂੰ ਪਸੰਦ ਆਈ ਉਹ ਇਹ ਸੀ ਕਿ ਮੈਟਾਡੇਟਾ ਪਹਿਲਾਂ ਹੀ ਲਾਭਕਾਰੀ ਸੀ। ਹਰ ਚੰਕ ਆਪਣੇ `source`, `sectionHeading`, `documentVersion`, ਅਤੇ ਪਲੇਸਹੋਲਡਰ `permissions` ਨੂੰ ਜਾਣਦਾ ਹੈ। ਛੋਟੇ ਟਿਊਟੋਰਿਯਲ ਵਿੱਚ ਵੀ, ਇਹ ਸੂਤਰ ਦੇਣ ਅਤੇ ਬਾਅਦ ਵਿੱਚ ਪਰਮੀਸ਼ਨ-ਅਗਾਹ ਰੀਟਰੀਵਲ ਨੂੰ ਸੋਚਣ ਵਿੱਚ ਸੌਖਾ ਬਣਾਉਂਦਾ ਹੈ।

## 5. ਸਥਾਨਕ ਐਮਬੈੱਡਿੰਗ ਬਣਾਓ

ਪਹਿਲੀ ਸਰਕਾਰੀ ਵਰਜਨ ਲਈ, ਮੈਂ `BAAI/bge-small-en-v1.5` ਨੂੰ FastEmbed ਰਾਹੀਂ ਵਰਤਦਾ ਹਾਂ।

ਇਸ ਨਾਲ ਟਿਊਟੋਰਿਯਲ ਸਥਾਨਕ ਅਤੇ ਸੀਪੀਯੂ-ਮਿੱਤਰ ਬਣਿਆ ਰਹਿੰਦਾ ਹੈ, ਪਰ ਇਹ ਇੱਕ ਅਸਲੀ ਐਮਬੈੱਡਿੰਗ ਮਾਡਲ ਵਰਤਦਾ ਹੈ ਨਾਂ ਕਿ ਕੇਵਲ ਪਲੇਸਹੋਲਡਰ ਵੇਕਟਰ ਫੰਕਸ਼ਨ। ਪਹਿਲੇ ਦੌੜ 'ਤੇ ਮਾਡਲ ਭਾਰ ਡਾਊਨਲੋਡ ਹੁੰਦਾ ਹੈ। ਉਸ ਤੋਂ ਬਾਅਦ, ਨੋਟਬੁੱਕ ਸਥਾਨਕ ਕੈਸ਼ ਰੀਯੂਜ਼ ਕਰ ਸਕਦਾ ਹੈ।

> [!NOTE]
> ਮੈਂ `BAAI/bge-small-en-v1.5` ਇਸ ਲਈ ਵਰਤਦਾ ਹਾਂ ਕਿਉਂਕਿ ਇਹ ਇੱਕ ਵਜਨੀ ਅੰਗਰੇਜ਼ੀ ਐਮਬੈੱਡਿੰਗ ਮਾਡਲ ਹੈ ਜੋ FastEmbed ਅਤੇ Qdrant ਨਾਲ ਖੁੱਲ੍ਹੇ ਟਿਊਟੋਰਿਯਲ ਲਈ ਅੱਛਾ ਕੰਮ ਕਰਦਾ ਹੈ। ਇਹ 384-ਡਾਈਮੇਨਸ਼ਨਲ ਵੇਕਟਰ ਬਣਾਉਂਦਾ ਹੈ, ਜੋ ਉਦਾਹਰਨ ਨੂੰ ਤੇਜ਼ ਅਤੇ ਸਸਤਾ ਸਥਾਨਕ ਚਲਾਉਣ ਵਿੱਚ ਰੱਖਦਾ ਹੈ। ਇਹ ਇਕੋ ਚੰਗਾ ਵਿਕਲਪ ਨਹੀਂ ਹੈ। 2023 ਵਿੱਚ, ਬਹੁਤ ਸਾਰੇ ਟਿਊਟੋਰਿਯਲ ਹੋਸਟ ਕੀਤੇ ਐਮਬੈੱਡਿੰਗ ਮਾਡਲ ਵਰਤਦੇ ਸਨ ਜਿਵੇਂ ਕਿ `text-embedding-ada-002`। ਅੱਜ, ਨਵੇਂ ਹੋਸਟ ਕੀਤੇ ਵਿਕਲਪਾਂ ਵਿੱਚ OpenAI `text-embedding-3-small` ਅਤੇ `text-embedding-3-large`, ਅਤੇ ਖੁੱਲ੍ਹੇ ਸਰੋਤ ਵਿਕਲਪਾਂ ਵਿੱਚ BGE, E5, MiniLM, Nomic Embed, ਅਤੇ ਬਹੁਭਾਸ਼ੀ ਮਾਡਲ ਜਿਵੇਂ `BAAI/bge-m3` ਸਭ ਵੱਖ-ਵੱਖ ਕਾਰਜ-ਭਾਰ ਤੇ ਨਿਰਭਰ ਕਰਕੇ ਵਾਜਬ ਚੋਣ ਹਨ। ਉਤਪਾਦਨ ਵਿੱਚ, ਠੀਕ ਐਮਬੈੱਡਿੰਗ ਮਾਡਲ ਤੁਹਾਡੇ ਆਪਣੇ ਦਸਤਾਵੇਜ਼ਾਂ 'ਤੇ ਰੀਟਰੀਵਲ ਮੁਲਾਂਕਣ ਰਾਹੀਂ ਚੁਣਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ।

ਕੁਝ ਵਿਆਪਕ ਵਿਕਲਪ:

| ਮਾਡਲ ਪਰਿਵਾਰ | ਮੈਂ ਕਦੋਂ ਇਸਨੂੰ ਵਿਚਾਰ ਕਰਾਂਗਾ |
| --- | --- |
| `text-embedding-ada-002` | ਬੁੱਢਾ ਹੋਸਟ ਕੀਤਾ ਗਿਆ ਬੇਸਲਾਈਨ ਜੋ ਬਹੁਤ ਸਾਰੇ 2023-ਦੌਰ ਟਿਊਟੋਰਿਯਲਾਂ ਵਿੱਚ ਸੀ। ਅੱਜ ਦੇ ਨਵੇਂ ਟਿਊਟੋਰਿਯਲ ਲਈ ਮੈਂ ਇਸਨੂੰ ਡੀਫੌਲਟ ਨਹੀਂ ਚੁਣਾਂਗਾ। |
| `text-embedding-3-small` | ਆਧੁਨਿਕ ਹੋਸਟ ਕੀਤਾ ਡੀਫੌਲਟ ਜਦੋਂ ਮੈਂ ਚੰਗੇ ਲਾਗਤ/ਕਰਗੁਜ਼ਾਰੀ ਸੰਤੁਲਨ ਦੀ ਲੋੜ ਹੋਵੇ ਅਤੇ ਸਿਰਫ ਸਥਾਨਕ ਐਮਬੈੱਡਿੰਗ ਦੀ ਲੋੜ ਨਹੀਂ। |
| `text-embedding-3-large` | ਜਦੋਂ ਰੀਟਰੀਵਲ ਗੁਣਵੱਤਾ ਵਿਅਾਪਕ ਮਹੱਤਵਪੂਰਨ ਹੋਵੇ, ਵੇਕਟਰ ਆਕਾਰ ਜਾਂ ਖਰਚ ਤੋਂ ਵੱਧ। |
| `BAAI/bge-small-en-v1.5` | ਟਿਊਟੋਰਿਯਲ, ਪ੍ਰੋਟੋਟਾਈਪ, ਅਤੇ ਸੀਪੀਯੂ-ਮਿੱਤਰ ਪ੍ਰਯੋਗਾਂ ਲਈ ਸੁਲਭ ਸਥਾਨਕ ਅੰਗਰੇਜ਼ੀ ਬੇਸਲਾਈਨ। |
| `BAAI/bge-base-en-v1.5` ਜਾਂ `BAAI/bge-large-en-v1.5` | ਵੱਡੇ ਸਥਾਨਕ ਅੰਗਰੇਜ਼ੀ ਮਾਡਲ ਜਦੋਂ ਮੈਂ ਚੰਗੀ ਰੀਟਰੀਵਲ ਗੁਣਵੱਤਾ ਚਾਹੁੰਦਾ ਹਾਂ ਅਤੇ ਵੱਧ ਕਮਪਿਊਟ ਸ਼ਕਤੀ ਦੇ ਸਕਦਾ ਹਾਂ। |
| `BAAI/bge-m3` | ਬਹੁਭਾਸ਼ੀ ਜਾਂ ਲੰਬੇ ਸੰਦਰਭ ਵਾਲੀ ਰੀਟਰੀਵਲ, ਖਾਸ ਕਰਕੇ ਜਦੋਂ ਦਸਤਾਵੇਜ਼ ਸਿਰਫ ਅੰਗਰੇਜ਼ੀ ਨਹੀਂ। |
| `sentence-transformers/all-MiniLM-L6-v2` | ਬਹੁਤ ਛੋਟਾ ਤੇ ਤੇਜ਼ ਸੇਮਾਂਟਿਕ ਖੋਜ ਬੇਸਲਾਈਨ। ਜਦੋਂ ਤੇਜ਼ੀ ਅਤੇ ਸਾਦਗੀ ਸਭ ਤੋਂ ਜ਼ਿਆਦਾ ਗੱਲ ਕਰਦੀ ਹੋਵੇ। |
| `nomic-embed-text-v1.5` | ਖੁੱਲ੍ਹਾ ਸਥਾਨਕ ਐਮਬੈੱਡਿੰਗ ਵਿਕਲਪ ਜੋ ਲੰਬੇ ਸੰਦਰਭ ਜਾਂ ਪੋਰਟੇਬਿਲਿਟੀ-ਕੇਂਦਰਤ ਸੈਟਅੱਪ ਲਈ ਟੈਸਟ ਕਰਨ ਯੋਗ। |

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

ਫਿਰ ਹਰ ਚੰਕ ਨੂੰ ਐਮਬੈੱਡਿੰਗ ਮਿਲਦੀ ਹੈ:

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

## 6. Qdrant ਸਥਾਨਕ ਮੋਡ ਵਿੱਚ ਵੇਕਟਰ ਸਟੋਰ ਕਰੋ

ਹੁਣ ਅਸੀਂ ਇੱਕ ਇਨ-ਮੇਮੋਰੀ Qdrant ਕਲੈਕਸ਼ਨ ਬਣਾਉਂਦੇ ਹਾਂ ਅਤੇ ਚੰਕਾਂ ਨੂੰ ਪੇਲੋਡ ਮੈਟਾਡੇਟਾ ਦੇ ਨਾਲ ਜੋੜਦੇ ਹਾਂ।

> [!NOTE]
> 2023 ਟਿਊਟੋਰਿਯਲ ਵਿੱਚ, ਮੈਂ FAISS ਵਰਤਿਆ ਕਿਉਂਕਿ ਇਹ ਲਾਂਗਚੇਨ ਨਾਲ ਸਥਾਨਕ ਵੇਕਟਰ ਸਮਰੂਪਤਾ ਖੋਜ ਦਿਖਾਉਣ ਦਾ ਇੱਕ ਸਾਦਾ ਅਤੇ ਲੋਕਪ੍ਰਿਯ ਤਰੀਕਾ ਸੀ। FAISS ਅਜੇ ਵੀ ਤੇਜ਼ ਸਥਾਨਕ ਪ੍ਰਯੋਗਾਂ ਲਈ ਲਾਭਦਾਇਕ ਹੈ। ਇਸ 2026 ਵਰਜਨ ਵਿੱਚ, ਮੈਂ Qdrant ਵਰਤਦਾ ਹਾਂ ਕਿਉਂਕਿ ਮੈਂ ਚਾਹੁੰਦਾ ਹਾਂ ਕਿ ਟਿਊਟੋਰਿਯਲ ਇੱਕ ਉਤਪਾਦਨ RAG ਸਿਸਟਮ ਦੇ ਨੇੜੇ ਮਹਿਸੂਸ ਹੋਵੇ। Qdrant ਮੈਨੂੰ ਵੇਕਟਰਾਂ ਨੂੰ ਸੋਰਸ ਫਾਈਲ, ਸੈਕਸ਼ਨ ਹੈਡਿੰਗ, ਦਸਤਾਵੇਜ਼ ਸੰસ્કਰਣ, ਅਤੇ ਪਰਮੀਸ਼ਨਾਂ ਵਰਗੇ ਪੇਲੋਡ ਮੈਟਾਡੇਟਾ ਨਾਲ ਸਟੋਰ ਕਰਨ ਦਿੰਦਾ ਹੈ। ਇਸ ਨਾਲ ਰੀਟਰੀਵਲ ਨੂੰ ਦੇਖਣਾ ਅਸਾਨ ਹੁੰਦਾ ਹੈ ਅਤੇ ਫਿਲਟਰੀਕਰਨ, ਸੂਤਰ, ਅਤੇ ਭਵਿੱਖੀ ਸਥਾਈ ਜਾਂ ਸਰਵਰ-ਆਧਾਰਿਤ ਡਿਪਲੌਇਮੈਂਟ ਲਈ ਉਦਾਹਰਨ ਤਿਆਰ ਹੁੰਦੀ ਹੈ।

FAISS ਵੇਕਟਰ ਸਮਾਨਤਾ ਖੋਜ ਦਿਖਾਉਣ ਲਈ ਬਹੁਤ ਵਧੀਆ ਹੈ। Qdrant ਇਕ ਛੋਟੇ ਪਰ ਉਤਪਾਦਨ-ਆਕਾਰ ਦੇ RAG ਰੀਟਰੀਵਲ ਲੇਅਰ ਦਿਖਾਉਣ ਲਈ ਬਿਹਤਰ ਹੈ।

ਕੁਝ ਵਿਆਪਕ ਵਿਕਲਪ:

| ਵੇਕਟਰ ਸਟੋਰ / ਖੋਜ ਲੇਅਰ | ਮੈਂ ਕਦੋਂ ਇਸਨੂੰ ਵਿਚਾਰ ਕਰਾਂਗਾ |
| --- | --- |
| Qdrant | ਸਥਾਨਕ ਨਮੂਨੇ, ਮੈਟਾਡੇਟਾ ਫਿਲਟਰੀਕਰਨ, ਉਤਪਾਦਨ-ਮਿਤਰ ਵੇਕਟਰ ਖੋਜ, ਅਤੇ ਇੱਕ ਸਾਦਾ ਪਾਈਥਨ ਵਰਕਫਲੋ। |
| Chroma | ਤੇਜ਼ ਸਥਾਨਕ RAG ਪ੍ਰਯੋਗ ਅਤੇ ਨੋਟਬੁੱਕ ਜਿੱਥੇ ਸਾਦਗੀ ਸਭ ਤੋਂ ਅਹੰਕਾਰਪੂਰਨ ਹੈ। |
| FAISS | ਸੁਲਭ ਸਥਾਨਕ ਵੇਕਟਰ ਖੋਜ ਜਦੋਂ ਮੈਨੂੰ ਕੇਵਲ ਸਮਾਨਤਾ ਖੋਜ ਦੀ ਲੋੜ ਹੋਵੇ ਅਤੇ ਮੈਟਾਡੇਟਾ ਵੱਖ ਕਰ ਕੇ ਸੰਭਾਲ ਸਕਾਂ। |
| Milvus | ਵੱਡੇ ਪੱਧਰ ਦੇ ਖੁੱਲ੍ਹা ਸਰੋਤ ਵੇਕਟਰ ਖੋਜ ਜਦੋਂ ਟੀਮ ਇੱਕ ਸਮਰਪਿਤ ਵੇਕਟਰ ਡੇਟਾਬੇਸ ਚਲਾਉਣ ਲਈ ਤਿਆਰ ਹੋਵੇ। |
| Weaviate | ਸਕੀਮਾ, ਮੈਟਾਡੇਟਾ, ਹਾਈਬਰਿਡ ਖੋਜ, ਅਤੇ ਪ੍ਰਬੰਧਿਤ ਜਾਂ ਸਵੈ-ਮਹਿਮਾਨ ਡਿਪਲੌਇਮੈਂਟ ਵਿਕਲਪਾਂ ਨਾਲ ਵੇਕਟਰ ਖੋਜ। |
| Azure AI Search | ਐਜ਼ਿਊਰ ਉੱਤੇ ਐਂਟਰਪ੍ਰਾਈਜ਼ RAG ਜਦੋਂ ਮੈਂ ਇੱਕੋ ਖੋਜ ਲੇਅਰ ਵਿੱਚ ਕੀਵਰਡ ਖੋਜ, ਵੇਕਟਰ ਖੋਜ, ਹਾਈਬਰਿਡ ਰੀਟਰੀਵਲ, ਸੇਮਾਂਟਿਕ ਰੈਂਕਿੰਗ, ਫਿਲਟਰੀਕਰਨ, ਸੁਰੱਖਿਆ ਅਤੇ ਪ੍ਰਬੰਧਿਤ ਸੰਚਾਲਨ ਚਾਹੁੰਦਾ ਹਾਂ। |
| PostgreSQL + pgvector | ਜੇ ਟੀਮਾਂ ਪਹਿਲਾਂ PostgreSQL ਵਰਤ ਰਹੀਆਂ ਹਨ ਤਾਂ ਖੋਜ ਨੂੰ ਐਪਲੀਕੇਸ਼ਨ ਡੇਟਾ ਦੇ ਨੇੜੇ ਚਾਹੁੰਦੇ ਹਨ। |

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

ਫਿਰ ਨੁਕਤੇ ਇਨਸਰਟ ਕਰੋ:

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

ਮੇਰੇ ਦੌੜ ਵਿੱਚ, ਕਲੈਕਸ਼ਨ ਵਿੱਚ 8 ਵੇਕਟਰ ਇਨਸਰਟ ਕੀਤੇ ਗਏ।

ਇੱਥੇ RAG ਸਿਸਟਮ ਇੰਸਪੈਕਟ ਕਰਨ ਯੋਗ ਹੋਣਾ ਸ਼ੁਰੂ ਕਰਦਾ ਹੈ। ਵੇਕਟਰ ਡੇਟਾਬੇਸ ਸਿਰਫ ਵੇਕਟਰ ਸਟੋਰ ਨਹੀਂ ਕਰ ਰਿਹਾ; ਇਹ ਸਬੂਤ ਟੈਕਸਟ ਅਤੇ ਸੂਤਰ ਲਈ ਮੈਟਾਡੇਟਾ ਸਟੋਰ ਕਰ ਰਿਹਾ ਹੈ।

## 7. ਉਮੀਦਵਾਰ ਚੰਕ ਰੀਟਰੀਵ ਕਰੋ

ਹੁਣ ਅਸੀਂ ਸਵਾਲ ਪੁੱਛਦੇ ਹਾਂ ਅਤੇ ਉਮੀਦਵਾਰ ਚੰਕ ਲੱਭਦੇ ਹਾਂ।

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

ਇਸ ਵੇਲੇ, ਮੈਂ ਜਵਾਬ ਤਿਆਰ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਪ੍ਰਾਪਤ ਚੰਕ ਛਪਾਉਂਦਾ ਹਾਂ। ਇਹ ਮਹੱਤਵਪੂਰਕ ਹੈ। ਜੇ ਰੀਟਰੀਵਲ ਗਲਤ ਹੋਵੇ, ਤਾ ਜਨਰੇਸ਼ਨ ਕੇਵਲ ਸੁਚਾਰੂ ਲਫ਼ਜ਼ਾਂ ਦੇ ਪਿੱਛੇ ਸਮੱਸਿਆ ਨੂੰ ਛੁਪਾਉਂਦਾ ਹੈ।

## 8. ਇੱਕ ਹਲਕਾ ਰੀਰੈਂਕਰ ਸ਼ਾਮਲ ਕਰੋ

ਜਦ ਮੈਂ ਪਹਿਲਾਂ ਰੀਟਰੀਵਲ ਪਾਥ ਟੈਸਟ ਕੀਤਾ, ਵੇਕਟਰ ਸਮਾਨਤਾ ਨੇ ਸਬੰਧਿਤ ਨੀਤੀ ਸਮੱਗਰੀ ਲੱਭੀ, ਪਰ ਸਭ ਤੋਂ ਸਟੀਕ ਸੈਕਸ਼ਨ ਹਮੇਸ਼ਾ ਸਿਖਰ 'ਤੇ ਨਹੀਂ ਸੀ।

ਤਾਂ ਮੈਂ ਛੋਟਾ ਸਥਾਨਕ ਰੀਰੈਂਕਰ ਸ਼ਾਮਲ ਕੀਤਾ। ਜਦੋਂ ਸਵਾਲ ਦੇ ਸ਼ਬਦ ਸੈਕਸ਼ਨ ਹੈਡਿੰਗ ਅਤੇ ਸਮੱਗਰੀ ਨਾਲ ਮਿਲਦੇ ਹਨ, ਤਾਂ ਇਹ ਵਧੀਆ ਵਜ਼ਨ ਦਿੰਦਾ ਹੈ।

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

ਰੀਰੈਂਕਿੰਗ ਤੋਂ ਬਾਅਦ, ਸਿਖਰਲਾ ਨਤੀਜਾ ਬਣ ਗਿਆ:

```text
school_ai_policy.md / Final Assignments
```

ਇਹ ਟੈਸਟ ਸਵਾਲ ਲਈ ਉਮੀਦਵਾਰ ਸੈਕਸ਼ਨ ਸੀ।

ਇਹ ਪਹਿਲੀ ਨਿਰਮਾਣ ਤੋਂ ਸਭ ਤੋਂ ਲਾਭਦਾਇਕ ਸਬਕ ਸੀ। ਛੋਟੇ ਸਥਾਨਕ ਉਦਾਹਰਨ ਵਿੱਚ ਵੀ, ਜਦੋਂ ਮੈਂ ਵੇਕਟਰ ਸਮਾਨਤਾ ਨੂੰ ਕਿਸੇ ਹੋਰ ਸਿਗਨਲ ਨਾਲ ਜੋੜਦਾ ਹਾਂ ਤਦ ਰੀਟਰੀਵਲ ਗੁਣਵੱਤਾ ਸੁਧਰਦੀ ਹੈ।

## 9. ਇੱਕ ਅਧਾਰਿਤ ਸਥਾਨਕ ਜਵਾਬ ਬਣਾਓ

ਡੀਫੌਲਟ ਰਸਤੇ ਲਈ, ਮੈਂ ਲੁਕਵਾਈ ਸਥਾਨਕ ਜਵਾਬ ਸੰਯੋਜਕ ਦੀ ਵਰਤੋਂ ਕਰਦਾ ਹਾਂ, ਨਾ ਕਿ ਕਿਸੇ LLM ਦੀ।

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

ਇਹ ਅੰਤਮ ਉਤਪਾਦ ਜਵਾਬ ਜਨਰੇਟਰ ਨਹੀਂ ਹੈ। ਇਹ ਡਿਬੱਗਿੰਗ ਟੂਲ ਹੈ। ਇਹ ਸਾਬਤ ਕਰਦਾ ਹੈ ਕਿ ਰੀਟਰੀਵਲ, ਮੈਟਾਡੇਟਾ, ਅਤੇ ਸੂਤਰ ਸੰਯੋਜਨ ਮਾਡਲ ਵਿਚ ਜਟਿਲਤਾ ਆਉਣ ਤੋਂ ਪਹਿਲਾਂ ਕੰਮ ਕਰਦੇ ਹਨ।

## 10. ਓਲਾਮਾ ਅਤੇ Phi-4-mini ਨਾਲ ਸਥਾਨਕ ਜਵਾਬ ਜਨਰੇਟ ਕਰੋ

ਜਦੋਂ ਰੀਟਰੀਵਲ ਕੰਮ ਕਰ ਰਿਹਾ ਹੈ, ਨੋਟਬੁੱਕ ਕੇਵਲ ਆਖਰੀ ਜਵਾਬ ਕਦਮ ਨੂੰ ਓਲਾਮਾ ਅਤੇ `phi4-mini:3.8b` ਨਾਲ ਬਦਲ ਸਕਦਾ ਹੈ।

> [!NOTE]
> ਓਲਾਮਾ ਸਿਰਫ ਆਖਰੀ ਜਵਾਬ-ਜਨਰੇਸ਼ਨ ਕਦਮ ਬਦਲੇ। ਦਸਤਾਵੇਜ਼ ਲੋਡਿੰਗ, ਚੰਕਿੰਗ, ਵੇਕਟਰ ਸਟੋਰੇਜ, ਰੀਟਰੀਵਲ, ਰੀਰੈਂਕਿੰਗ, ਅਤੇ ਸੂਤਰ ਸੰਯੋਜਨ ਬਰਕਰਾਰ ਰਹਿਣ।

ਸਭ ਤੋਂ ਪਹਿਲਾਂ, ਨੋਟਬੁੱਕ ਪ੍ਰਾਪਤ ਚੰਕਾਂ ਤੋਂ ਇੱਕ ਸਬੂਤ ਪ੍ਰਾਂਪਟ ਬਣਾਉਂਦਾ ਹੈ:

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

ਇਸ ਟਿਊਟੋਰਿਯਲ ਲਈ, ਮੈਂ ਪਹਿਲਾਂ ਮਾਈਕਰੋਸਾਫਟ ਦੇ Phi-4-mini ਪਰਿਵਾਰ ਨੂੰ ਓਲਾਮਾ ਰਾਹੀਂ ਡੀਫੌਲਟ ਸਥਾਨਕ ਜਨਰੇਸ਼ਨ ਵਿਕਲਪ ਵਜੋਂ ਸਿਫਾਰਸ਼ ਕਰਦਾ ਹਾਂ। ਓਲਾਮਾ ਵਿੱਚ, ਮੈਂ ਜਿਸ ਮਾਡਲ ਨੂੰ ਟੈਸਟ ਕੀਤਾ ਹੈ ਉਹ ਹੈ:

```powershell
ollama pull phi4-mini:3.8b
```

ਤੁਸੀਂ ਜਲਦੀ ਨਾਲ ਉਸ ਮਾਡਲ ਦੀ ਉਪਲਬਧਤਾ ਨੂੰ ਜਾਂਚ ਸਕਦੇ ਹੋ:

```powershell
ollama list
```

ਫਿਰ ਇਹ ਚਲਾਂਵੀਆਂ ਸੈੱਟ ਕਰੋ:

```powershell
Copy-Item .env.example .env
```

`.env` ਖੋਲ੍ਹੋ ਅਤੇ ਸਿਰੀਜ਼ 2 ਓਲਾਮਾ ਮੁੱਲ ਅਣਕਮੈਂਟ ਕਰੋ:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

ਨੋਟਬੁੱਕ `python-dotenv` ਨਾਲ ਰਿਪੋਜ਼ਟਰੀ ਰੂਟ ਤੋਂ `.env` ਲੋਡ ਕਰਦਾ ਹੈ, ਫਿਰ ਉਸੇ ਸਬੂਤ ਪ੍ਰਾਂਪਟ ਨੂੰ ਓਲਾਮਾ ਦੇ ਸਥਾਨਕ `/api/chat` ਐਂਡਪੁਆਇੰਟ ਤੇ ਕਿਸਮਤੀ ਬੰਦ ਕਰ ਕੇ ਭੇਜਦਾ ਹੈ। ਜੇ ਓਲਾਮਾ ਚੱਲ ਨਹੀਂ ਰਿਹਾ ਜਾਂ `SERIES2_OLLAMA_MODEL` ਨਾ ਹੋਵੇ, ਤਾਂ ਇਹ ਰਾਹ ਛੱਡ ਦਿੱਤਾ ਜਾਂਦਾ ਹੈ।

> [!NOTE]
> ਇਸ ਮਸ਼ੀਨ 'ਤੇ, `phi4-mini:3.8b` ਨੇ ਲਗਭਗ 2.49GB ਮਾਡਲ ਫਾਈਲਾਂ ਡਾਊਨਲੋਡ ਕੀਤੀਆਂ। ਅਨੁਮਾਨ ਦੌਰਾਨ, ਓਲਾਮਾ ਨੇ 3.3GB ਲੋਡ ਮਾਡਲ ਆਕਾਰ ਦਰਸਾਇਆ ਅਤੇ RTX 3060 ਲੈਪਟਾਪ GPU ਵਰਤਿਆ।

ਇਸ ਨਾਲ ਟਿਊਟੋਰਿਯਲ ਨੂੰ ਦੋ ਸਤਰਾਂ ਮਿਲਦੀਆਂ ਹਨ:

1. ਸੀਪੀਯੂ-ਕੇਵਲ ਨਿਰਧਾਰਿਤ ਜਵਾਬ ਸੰਯੋਜਕ।
2. ਓਲਾਮਾ ਅਤੇ Phi-4-mini ਨਾਲ ਸਥਾਨਕ ਜਵਾਬ ਜਨਰੇਸ਼ਨ।

ਦੋਹਾਂ ਵਿੱਚ ਰੀਟਰੀਵਲ ਪਾਈਪਲਾਈਨ ਉਹੀ ਰਹਿੰਦੀ ਹੈ।

## 11. ਜਾਂਚ ਨਤੀਜਾ

ਮੈਂ ਨੋਟਬੁੱਕ Windows 'ਤੇ ਪਾਈਥਨ 3.12.6 ਨਾਲ ਸਥਾਨਕ ਚਲਾਇਆ।

ਇੰਸਟਾਲ ਕੀਤੇ ਪੈਕੇਜ:

| ਪੈਕੇਜ | ਵਰਜ਼ਨ |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

ਨੋਟਬੁੱਕ ਕਾਰਗੁਜ਼ਾਰੀ:

- ਨੋਟਬੁੱਕ: `notebooks/series-2-open-source-rag.ipynb`
- ਕਾਰਗੁਜ਼ਾਰੀ ਨਤੀਜਾ: `nbclient` ਨਾਲ ਪਾਸ
- ਦਸਤਾਵੇਜ਼ ਲੋਡ ਹੋਏ: 2
- ਚੰਕ ਬਣਾਏ ਗਏ: 8
- Qdrant ਕਲੈਕਸ਼ਨ: `school_policy_local`
- ਵੇਕਟਰ ਇੰਸਰਟ ਕੀਤੇ: 8
- ਐਮਬੈੱਡਿੰਗ ਮਾਡਲ: `BAAI/bge-small-en-v1.5`
- ਐਮਬੈੱਡਿੰਗ ਅਕਾਰ: 384
- ਰੀਟ੍ਰੀਵਲ ਸਵਾਲ: "ਕੀ ਮੈਂ ਆਪਣੀ ਅੰਤਿਮ ਅਸਾਈਨਮੈਂਟ ਲਈ ਜਨਰੇਟਿਵ ਏਆਈ ਵਰਤ ਸਕਦਾ ਹਾਂ?"
- ਰੀਰੈਂਕਿੰਗ ਮਾਰਗ: ਹਲਕਾ-ਫੁਲਕਾ ਲੋਕਲ ਲੈਕਸੀਕਲ ਰੀਰੈਂਕਿੰਗ
- ਰੀਰੈਂਕਿੰਗ ਤੋਂ ਬਾਅਦ ਤੋਪ ਪ੍ਰਾਪਤ ਸਰੋਤ: `school_ai_policy.md`
- ਰੀਰੈਂਕਿੰਗ ਤੋਂ ਬਾਅਦ ਤੋਪ ਪ੍ਰਾਪਤ ਭਾਗ: `Final Assignments`
- ਡਿਫੌਲਟ ਜਵਾਬ ਮਾਰਗ: ਲੋਕਲ ਟਰਾਂਸਪੇਰੈਂਟ ਆਂਸਰ ਕੰਪੋਜ਼ਰ
- Ollama ਜਨਰੇਸ਼ਨ ਮਾਰਗ: `phi4-mini:3.8b` ਨਾਲ ਪCompleਟ
- Ollama ਮਾਡਲ ਫਾਇਲ ਆਕਾਰ: ਡਿਸਕ ਤੇ 2.49GB
- Ollama ਲੋਡ ਮਾਡਲ ਆਕਾਰ: `ollama ps` ਵੱਲੋਂ 3.3GB ਰਿਪੋਰਟ ਕੀਤਾ ਗਿਆ
- GPU ਆਫਲੋਡ: `ollama ps` ਵੱਲੋਂ 100% GPU ਰਿਪੋਰਟ ਕੀਤਾ ਗਿਆ
- ਜਨਰੇਸ਼ਨ ਤੋਂ ਬਾਅਦ GPU ਮੈਮੋਰੀ ਦਾ ਅੰਕੜਾ: RTX 3060 ਲੈਪਟਾਪ GPU ਉੱਤੇ ਤੱਕਰੀਬਨ 3.5GB 6GB ਵਿੱਚੋਂ ਵਰਤੀ ਗਈ
- ਕੈਸ਼ਡ FastEmbed ਮਾਡਲ ਅਤੇ Ollama ਜਨਰੇਸ਼ਨ ਸਮੇਤ ਨੋਟਬੁੱਕ ਐਗਜ਼ਿਕਿਊਸ਼ਨ: ਪ੍ਰਮਾਣੀਕਰਣ ਸਕ੍ਰਿਪਟ ਰਾਹੀਂ ਲਗਭਗ 34 ਸਕਿੰਟ ਵਿੱਚ ਪਾਸ ਹੋਇਆ

Ollama-ਦwara ਬਣਾਇਆ ਗਿਆ ਜਵਾਬ ਸੀ:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

ਮੈਂ ਇਸ ਜਵਾਬ ਨੂੰ ਪਰਫੈਕਟ ਨਹੀਂ ਕਹਾਂਦਾ। ਇਹ ਸਹੀ ਸਬੂਤ ਤੋਂ ਜਵਾਬ ਦਿੰਦਾ ਹੈ, ਪਰ ਅੰਤਿਮ ਸਰੋਤ ਲਾਈਨ ਨਿਰਧਾਰਤ ਹਵਾਲਾ ਫਾਰਮੈਟ ਨਾਲ ਕੁਝ ਘੱਟ ਸਟੀਕ ਹੈ। ਇਹ ਟਿਊਟੋਰਿਅਲ ਵਿਚ ਦਿਖਾਉਣਾ ਲਾਭਦਾਇਕ ਹੈ ਕਿਉਂਕਿ ਇਹ ਅਗਲੇ ਇੰਜੀਨੀਅਰਿੰਗ ਸਵਾਲ ਨੂੰ ਸਪਸ਼ਟ ਕਰਦਾ ਹੈ: ਜਵਾਬ ਬਣਾਉਣ ਦੀ ਵੀ ਜਾਂਚ ਲੋੜੀਂਦੀ ਹੈ, ਸਿਰਫ ਰੀਟ੍ਰੀਵਲ ਹੀ ਨਹੀਂ।

ਮੇਰੀ ਪ੍ਰਮਾਣੀਕਰਣ ਦੌਰਾਨ ਮੁੱਖ ਗੱਲ ਜੋ ਸਿੱਖੀ, ਉਹ ਇਹ ਹੈ ਕਿ ਜਵਾਬ ਬਣਾਉਣ ਤੋਂ ਪਹਿਲਾਂ ਰੀਟ੍ਰੀਵਲ ਦੀ ਗੁਣਵੱਤਾ ਦੀ ਜਾਂਚ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ। ਐਮਬੈਡਿੰਗ ਨਤੀਜਾ ਪਹਿਲਾਂ ਹੀ ਲਾਭਦਾਇਕ ਸੀ, ਅਤੇ ਹਲਕਾ-ਫੁਲਕਾ ਰੀਰੈਂਕਰ ਨੇ ਉਮੀਦ ਕੀਤੀ ਨੀਤੀ ਭਾਗ ਨੂੰ ਭਰੋਸੇਯੋਗ ਤੌਰ ਤੇ ਪਹਿਲਾਂ ਲਿਆ। ਇਹ ਉਹ ਕਿਸਮ ਦੀ ਛੋਟੀ ਸਿਸਟਮ ਪ੍ਰਵਿਰਤੀ ਹੈ ਜੋ ਮੈਂ ਟਿਊਟੋਰਿਅਲ ਵਿੱਚ ਛੁਪਾਉਣ ਦੀ ਬਜਾਏ ਬਾਹਰ ਲਿਆਉਣਾ ਚਾਹੁੰਦਾ ਹਾਂ।

## 12. ਅਗਲਾ ਕਿਉਂ ਆਉਂਦਾ ਹੈ

ਅਗਲਾ ਸੁਧਾਰ ਇਹ ਹੋਵੇਗਾ ਕਿ ਇਸ ਲੋਕਲ ਸੈਟਅਪ ਦੀ ਤੁਲਨਾ ਇੱਕ ਪ੍ਰਬੰਧਤ ਐਜ਼ੂਅਰ ਵਰਜਨ ਨਾਲ ਕੀਤੀ ਜਾਵੇ ਜੋ ਇਕੋ ਸਕੂਲ ਨੀਤੀ ਸਹਾਇਕ ਸਥਿਤੀ ਹੈ। ਸਥਿਤੀ ਨੂੰ ਫਿਕਸ ਰੱਖਣਾ ਤਨਾਜ਼ੇ ਨੂੰ ਆਸਾਨ ਬਣਾਏਗਾ: ਸੈਟਅਪ ਜਟਿਲਤਾ, ਰੀਟ੍ਰੀਵਲ ਕੰਟਰੋਲ, ਪਹਿਚਾਣ ਏਕੀਕਰਨ, ਆਪਰੇਸ਼ਨਲ ਮਲਕੀਅਤ ਅਤੇ ਲਾਗਤ।

## 13. ਹਵਾਲੇ

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

ਪਿਛਲਾ: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਪਣ**:
ਇਸ ਦਸਤਾਵੇਜ਼ ਦਾ ਅਨੁਵਾਦ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾਵਾਂ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮੱਤਿਆਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੇ ਉਪਯੋਗ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆਵਾਂ ਲਈ ਜਵਾਬਦੇਹ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->