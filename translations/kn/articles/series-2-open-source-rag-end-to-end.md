# ನಿಮ್ಮ ದಾಖಲೆಗಳ ಆಧಾರದ ಮೇಲೆ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಲು AI ಯನ್ನು ತರಬೇತುಮಾಡಿ
## ಸರಣಿ 2: ಸ್ಥಳೀಯ ಓಪನ್-ಸೋರ್ಸ್ RAG ವ್ಯವಸ್ಥೆಯನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ನಿರ್ಮಿಸಿ

![ಸ್ಥಳೀಯ ಓಪನ್-ಸೋರ್ಸ್ RAG ಟ್ಯುಟೋರಿಯಲ್ ಪೈಪ್‌ಲೈನ್](../../../assets/images/series-2-local-rag.svg)

> ಈ ಲೇಖನವು ಸರಣಿ 1 ವಿನ್ಯಾಸ ಚರ್ಚೆಯನ್ನು ಚಲಿಸುವ ಸ್ಥಳೀಯ RAG ಟ್ಯುಟೋರಿಯಲ್ ಆಗಿ ಪರಿವರ್ತಿಸುತ್ತದೆ. ಗುರಿಯೇ ಪ್ರಾರಂಭದಲ್ಲಿ ಮಾದರಿ ಡೇಟಾ, ಯಾವುದೇ ಕ್ಲೌಡ್ ಖಾತೆ ಇಲ್ಲದೆ ಮತ್ತು ಯಾವುದೇ ರಹಸ್ಯವಿಲ್ಲದೆ ಪೂರ್ಣ ಕಾರ್ಯಪಟು ಕ್ರಮವನ್ನು ನಿರ್ಮಿಸುವುದು, ನಂತರ ಕಾರ್ಯನಿರ್ವಹಿಸುವ ಮೂಲಭೂತ ಆಧಾರದ ಮೂಲಕ ಉತ್ತಮ ವಿನ್ಯಾಸ ನಿರ್ಧಾರಗಳನ್ನು ತಯಾರಿಸುವುದು.

ನಾವು ನಿರ್ಮಿಸಲಿರುವ ವ್ಯವಸ್ಥೆಯು ಒಂದು ಸಣ್ಣ ಶಾಲಾ ನೀತಿ ಸಹಾಯಕ. ನಾನು ಎರಡು ಸ್ಥಳೀಯ ಮಾರ್ಕ್ಡೌನ್ ಕಡತಗಳನ್ನು ಜ್ಞಾನ ಮೂಲವಾಗಿ ಬಳಸುತ್ತೇನೆ, ನಂತರ ಪೂರ್ಣ RAG ಪೈಪ್‌ಲೈನ್ ಮೂಲಕ ನಡೆದುಕೊಳ್ಳುತ್ತೇನೆ: ತುಂಡು ಮಾಡುವುದು, ಸ್ಥಳೀಯ ಪ್ರತಿಬಿಂಬಗಳು, Qdrant ವೆಕ್ಟರ್ ಸಂಗ್ರಹಣೆ, ಪ್ರಾಪ್ತಿ, ಮರುಸ್ಥಾನ, ಮೂಲ-ಜಾಗೃತ ಉತ್ತರ ರಚನೆ ಮತ್ತು ಐಚ್ಛಿಕವಾಗಿ ಸ್ಥಳೀಯ Oluama ಮತ್ತು Phi-4-mini ಜೊತೆಗೆ ಜನೆರೇಶನ್.

ಸರಣಿ ನಿಯಾಗಮನ: [ಮಡಿಕೆ ಮನೆ](../README.md) | ಹಿಂದೆ: [ಸರಣಿ 1 - RAG, ಅಜೂರ್ ಮತ್ತು ಓಪನ್-ಸೋರ್ಸ್ ಪರ್ಯಾಯಗಳು, ಮತ್ತು ಫೈನ್-ಟ್ಯೂನಿಂಗ್ ಸೂಕ್ತವಾಗಿರುವ ಸಂದರ್ಭದಲ್ಲಿ](./series-1-rag-azure-open-source-fine-tuning.md)

ನೋಟ್‌ಬುಕ್: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | ಅಗತ್ಯಗಳು: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> ನೀವು ಕ್ಲೌಡ್ ಸಂಪನ್ಮೂಲಗಳನ್ನು ರಚಿಸುವ ಮುಂಚೆ RAG ಪೈಪ್‌ಲೈನ್ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಬಯಸಿದರೆ ಇದು ಉತ್ತಮ ಪ್ರಾರಂಭದ ಬಿಂದುವಾಗಿದೆ. ಡೀಫಾಲ್ಟ್ ಮಾರ್ಗವು ಸಿಪಿಯು ಸ್ನೇಹಿ ಪ್ರತಿಬಿಂಬಗಳೊಂದಿಗೆ ಮತ್ತು ಯಾವುದೇ ರಹಸ್ಯವಿಲ್ಲದೆ ಸ್ಥಳೀಯವಾಗಿ ಚಾಲನೆ ಮಾಡುತ್ತದೆ.

## 1. ನಾವು ಏನನ್ನು ನಿರ್ಮಿಸುತ್ತಿದ್ದೇವೆ

2023 ರ ಟ್ಯುಟೋರಿಯಲ್‌ನಲ್ಲಿ, ನಾನು ಅಜೂರ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿರಲಿಲ್ಲ ಏಕೆ ಎಂದರೆ ಗುರಿಯೇ ಅಜೂರ್ AI ಮಹೋದ್ಯಮ ಮತ್ತು ಅಜೂರ್ OpenAI PDF ಕಡತಗಳಿಂದ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರ ಕೊಡಿಸುವುದನ್ನು ತೋರಿಸುವುದು.

ಈ 2026 ಸರಣಿಗೆ, ನಾನು ಒಂದು ಹಂತ ಕೆಳಗೆ ಪ್ರಾರಂಭಿಸಲು ಬಯಸುತ್ತೇನೆ.

ನಿರ್ವಹಿಸಲಾದ ಸೇವೆಗಳನ್ನು ಬಳಸುವುದಕ್ಕೆ ಮುಂಚೆ, ನಾನು ಸಣ್ಣ RAG ವ್ಯವಸ್ಥೆಯನ್ನು ಸ್ಥಳೀಯವಾಗಿ ನಿರ್ಮಿಸಬೇಕೆಂದು ಮತ್ತು ಪ್ರತಿ ಹಂತವನ್ನು ಕಾಣಿಸುವಂತೆ ಮಾಡಬೇಕೆಂದು ಬಯಸುತ್ತೇನೆ: ಕಡತಗಳನ್ನು ಲೋಡ್ ಮಾಡುವುದು, ಪಠ್ಯವನ್ನು ತುಂಡು ಮಾಡುವುದು, ವೆಕ್ಟರ್ಗಳನ್ನು ಸಂಗ್ರಹಿಸುವುದು, ಸಾಕ್ಷ್ಯವನ್ನು ಪ್ರಾಪ್ತಿಪಡಿಸುವುದು, ಮರುಸ್ಥಾನಗೊಳಿಸುವುದು, ಮತ್ತು ಮೂಲ-ಜಾಗೃತ ಉತ್ತರವನ್ನು ನೀಡುವುದು.

ಮಾದರಿ ಪರಿಸ್ಥಿತಿ ಶಾಲಾ ನೀತಿ ಸಹಾಯಕ. ಬಳಕೆದಾರನು ಕೇಳುತ್ತಾನೆ:

```text
Can I use generative AI for my final assignment?
```

ವ್ಯವಸ್ಥೆ ಸಾಮಾನ್ಯ ಮಾದರಿ ಸ್ಮೃತಿ ನಿಂದ ಉತ್ತರಿಸುವುದಿಲ್ಲ. ಅದು ಸಂಬಂಧಿತ ನೀತಿ ವಿಭಾಗವನ್ನು ಪ್ರಾಪ್ತಿಪಡಿಸಿ ಆ ಸಾಕ್ಷ್ಯದಿಂದ ಉತ್ತರ ನೀಡಬೇಕು.

ಪೂರ್ಣ ಚಲಿಸುವ ಆವೃತ್ತಿ [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) ನಲ್ಲಿ ಇದೆ. ಕೆಳಗಿನ ಕೋಡ್ ಮುಖ್ಯ ಹಂತಗಳನ್ನು ತೋರಿಸುತ್ತದೆ ಆದ್ದರಿಂದ ಲೇಖನವನ್ನು ಟ್ಯುಟೋರಿಯಲ್ ಆಗಿ ಓದಬಹುದು.

## 2. ಸ್ಥಳೀಯ ಅವಲಂಬನೆಗಳನ್ನು ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಿ

ವರ್ಚುವಲ್ ಪರಿಸರವನ್ನು ರಚಿಸಿ ಮತ್ತು ಸರಣಿ 2 ಅಗತ್ಯವಿರುವ ಪ್ಯಾಕೇಜ್‌ಗಳನ್ನು ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಿ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

ಪ್ರಥಮ ಆವೃತ್ತಿ Qdrant ಸ್ಥಳೀಯ ಮೋಡ್ ಮತ್ತು FastEmbed ಅನ್ನು ಬಳಸುತ್ತದೆ. Qdrant ರ ಪೈಥಾನ್ ಕ್ಲೈಂಟ್ `QdrantClient(":memory:")` ಮೂಲಕ in-memory ಸ್ಥಳೀಯ ಮೋಡ್ ಅನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ, ಇದು ಸ್ಥಳೀಯ ಟ್ಯುಟೋರಿಯಲ್‌ಗಳು ಮತ್ತು CI ಶೈಲಿಯ ಪರಿಶೀಲನೆಗೆ ಉಪಯುಕ್ತ. FastEmbed ನಿಂದ ನಾವು ಕ್ಲೌಡ್ API ಕೀ ಅಗತ್ಯವಿಲ್ಲದೆ ನಿಜವಾದ ಸ್ಥಳೀಯ embedding ಮಾದರಿಯನ್ನು ಪಡೆಯುತ್ತೇವೆ.

ಅಗತ್ಯತೆ ಕಡತದಲ್ಲಿಯೂ `python-dotenv` ಸೇರಿಸಲಾಗಿದೆ, ಏಕೆಂದರೆ ನೋಟ್‌ಬುಕ್ ಐಚ್ಛಿಕವಾಗಿ `.env` ನಿಂದ Oluama ಮಾದರಿ ಹೆಸರನ್ನು ಓದಲು ಸಾಧ್ಯ. ಈ ಸ್ಥಳೀಯ ಟ್ಯುಟೋರಿಯಲ್‌ಗೆ ಯಾವುದೇ ಅಜೂರ್ OpenAI ಅಥವಾ OpenAI API ಕೀ ಅಗತ್ಯವಿಲ್ಲ.

## 3. ಮಾದರಿ ದಾಖಲೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಿ

ಮಾದರಿ ಗುಂಪು ಉದ್ದೇಶಪೂರ್ವಕವಾಗಿ ಸಣ್ಣದು:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

ನೋಟ್‌ಬುಕ್‌ನಲ್ಲಿ, ನಾನು `sample_data/` ನ ಎಲ್ಲ ಮಾರ್ಕ್ಡೌನ್ ಕಡತಗಳನ್ನು ಲೋಡ್ ಮಾಡುತ್ತೇನೆ:

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

ನೋಟ್‌ಬುಕ್ ಅನ್ನು ಗಡುವಿದಾಗ, 2 ಕಡತಗಳನ್ನು ಲೋಡ್ ಮಾಡಿತು. ಇದು ಕೈಯಿಂದ ಪರಿಶೀಲಿಸಲು ಸಣ್ಣದಾಗಿದೆ, ಇದು RAG ಪೈಪ್‌ಲೈನ್ ಪ್ರಥಮ ಆವೃತ್ತಿ ನಿರ್ಮಾಣಕ್ಕೆ ಉಪಯುಕ್ತ.

## 4. Markdown ಶಿವಿರಗಳಿಂದ ತುಂಡುಮಾಡಿ

ಮುಂದಿನ ಹಂತವು ಕಡತಗಳನ್ನು ತುಂಡುಗಳಾಗಿ ಹಂಚುವುದು.

ಈ ಟ್ಯುಟೋರಿಯಲ್ ಗೆ ನಾನು Markdown ಶಿವಿರಗಳನ್ನು ಸಾಂರಚನಾತ್ಮಕ ಸಂಕೇತವಾಗಿ ಬಳಸುತ್ತೇನೆ. ದಾಖಲೆ ಶೀರ್ಷಿಕೆ `#` ನಿಂದ ಬರುತ್ತದೆ, ಮತ್ತು ಪ್ರತಿ ವಿಭಾಗದ ತುಂಡು `##` ನಿಂದ ಬರುತ್ತದೆ.

> [!NOTE]
> ತುಂಡು ಸಾಧಿಸುವುದು ಎಲ್ಲಾ-ಒಮ್ಮೆಯಲ್ಲ. ಈ ಟ್ಯುಟೋರಿಯಲ್ ನಲ್ಲಿ ನಾನು Markdown ಶಿವಿರಗಳನ್ನು ಬಳಸುತ್ತೇನೆ ಏಕೆಂದರೆ ಮಾದರಿ ದಾಖಲೆಗಳು ಸ್ಪಷ್ಟ `#` ಮತ್ತು `##` ಸಾಂರಚನೆ ಹೊಂದಿವೆ. PDFs, ವರ್ಡ್ ದಾಖಲೆಗಳು, ಸ್ಲೈಡ್‌ಗಳು, ಟಿಕೆಟ್‌ಗಳು, ಅಥವಾ ವೆಬ್ ಪುಟಗಳುಗಾಗಿ ಉತ್ತಮ ತಂತ್ರವು ಪುಟ ಗಡಿಗಳು, ವಿನ್ಯಾಸ ಮಾಹಿತಿ, ಅರ್ಥಾತ್ಮಕ ವಿಭಾಗಗಳು, ಟೋಕನ್ ಮಿತಿಗಳು, ಪಟ್ಟಿಗಳು ಅಥವಾ ಮೆಟಾಡೇಟಾ ಬಳಸಬಹುದು. ಮುಖ್ಯ ಬಿಂದು ನಿಮ್ಮ ದಾಖಲೆಗಳ ಅರ್ಥ ಮತ್ತು ಮೂಲ ಟ್ರೇಸಬಿಲಿಟಿ ಕಾಯ್ದುಕೊಳ್ಳುವ ತುಂಡು ಸಾಧಿಸುವ ತಂತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡುವುದು.

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

ನಂತರ ಪ್ರತಿಯೊಂದು ಕಡತಕ್ಕೆ ಇದು ಅನ್ವಯಿಸಲಾಗುವುದು:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

ನನ್ನ ಸ್ಥಳೀಯ ಚಲಾವಣೆಯಲ್ಲಿ ಇದರಿಂದ 8 ತುಂಡುಗಳು ರಚನೆಗೊಂಡವು.

ನನಗೆ ಈ ಹಂತದಲ್ಲಿ ಮೆಟಾಡೇಟಾ ಈಗಾಗಲೇ ಉಪಯುಕ್ತವಾಗಿದೆ ಎಂಬುದು ಇಷ್ಟವಾಯಿತು. ಪ್ರತಿ ತುಂಡು ಇದರ `ಸ्रोत`, `ವಿಭಾಗಶೀರ್ಷಿಕೆ`, `ದಾಖಲೆ ಆವೃತ್ತಿ` ಮತ್ತು ಸ್ಥಳಾಪಕ `ಅನುವಾದಗಳು` ತಿಳಿಸುತ್ತದೆ. ಸಣ್ಣ ಟ್ಯುಟೋರಿಯಲಲ್ಲಿಯೂ ಇದರಿಂದ ಉಲ್ಲೇಖ ಮತ್ತು ನಂತರ ಅನುಮತಿ-ಜಾಗೃತ ಪ್ರಾಪ್ತಿಗೆ ಸುಲಭವಾಗಿ ಕಲ್ಪನೆ ಮಾಡಬಹುದು.

## 5. ಸ್ಥಳೀಯ embedding ಗಳು ರಚಿಸಿ

ಪ್ರಥಮ ಸಾರ್ವಜನಿಕ ಆವೃತ್ತಿಗೆ, ನಾನು FastEmbed ಮೂಲಕ `BAAI/bge-small-en-v1.5` ಬಳಸುತ್ತೇನೆ.

ಇದು ಟ್ಯುಟೋರಿಯಲ್ನು ಸ್ಥಳೀಯ ಮತ್ತು CPU-ಸ್ನೇಹಿಯನ್ನಾಗಿಸುತ್ತದೆ, ಆದರೆ ಇದು ಇನ್ನೂ ನಿಜವಾದ embedding ಮಾದರಿಯನ್ನು ಬಳಸುತ್ತದೆ, ಸ್ಥಳಾಪಕ ವೆಕ್ಟರ್ ಕ್ರಿಯೆಯ ಬದಲು. ಪ್ರಥಮ ಚಾಲನೆಯು ಮಾದರಿ ತೂಕಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡುತ್ತದೆ. ಆನಂತರ, ನೋಟ್‌ಬುಕ್ ಸ್ಥಳೀಯ ಕ್ಯಾಶೆ ಮರುಬಳಕೆ ಮಾಡಬಹುದು.

> [!NOTE]
> ನಾನು `BAAI/bge-small-en-v1.5`ನ್ನು ಬಳಸುತ್ತೇನೆ ಏಕೆಂದರೆ ಇದು FastEmbed ಮತ್ತು Qdrant ಜೊತೆಗೆ ಉತ್ತಮವಾಗಿ ಕೆಲಸ ಮಾಡುವ ತೂಕಗಳಿಲ್ಲದ ಇಂಗ್ಲಿಷ್ embedding ಮಾದರಿ. ಇದು 384-ನಿರ್ದಿಷ್ಟ ವೈಮ್ಯುಕ್ತಿ ವೆಕ್ಟರ್ ಗಳನ್ನು ಸೃಷ್ಟಿಸುತ್ತದೆ, ಉದಾಹರಣೆ ಸ್ಥಳೀಯವಾಗಿ ವೇಗವಾಗಿ ಮತ್ತು ಕಡಿಮೆ ఖರ್ಚಿನಲ್ಲಿ ಚಲಿಸಬೇಕಾಗಿ ಇರುತ್ತದೆ. ಇದು ಏಕಮಾತ್ರ ಉತ್ತಮ ಆಯ್ಕೆಯಾಗಿಲ್ಲ. 2023 ರಲ್ಲಿ ಹಲವು ಟ್ಯುಟೋರಿಯಲ್ಗಳು `text-embedding-ada-002` ಎಂಬ ಹೋಷ್ಟ್ ಮಾಡಿದ embedding ಮಾದರಿಗಳನ್ನು ಬಳಿಸಿದರು. ಇಂದಿನಂದು, ಇತ್ತೀಚಿನ ಹೋಷ್ಟ್ ಆಯ್ಕೆಗಳಲ್ಲಿ OpenAI `text-embedding-3-small` ಮತ್ತು `text-embedding-3-large` ಇವೆ, ಮತ್ತು ಓಪನ್-ಸೋರ್ಸ್ ಆಯ್ಕೆಗಳನ್ನು BGE, E5, MiniLM, Nomic Embed ಮತ್ತು ಬಹುಭಾಷಾ ಮಾದರಿಗಳು `BAAI/bge-m3` ಸೇರಿದಂತೆ ಬಲವಾದ ಆಯ್ಕೆಗಳಾಗಿವೆ ವೈ ಮತ್ಯಧಿದಂತೆ. ಉತ್ಸವದಲ್ಲಿ, ಸರಿಯಾದ embedding ಮಾದರಿಯನ್ನು ನಿಮ್ಮದೇ ದಾಖಲೆಗಳ ಮೇಲಿನ ಪ್ರಾಪ್ತಿ ಮೌಲ್ಯಮಾಪನದ ಮೂಲಕ ಆಯ್ಕೆ ಮಾಡಬೇಕು.

ಕೆಲವು ಪ್ರಾಯೋಗಿಕ ಪರ್ಯಾಯಗಳು:

| ಮಾದರಿ ಕುಟುಂಬ | ನಾನು ಇದನ್ನು ಯಾವಾಗ ಪರಿಗಣಿಸುತ್ತೇನೆ |
| --- | --- |
| `text-embedding-ada-002` | 2023 ಯುಗದ ಹಲವಾರು ಟ್ಯುಟೋರಿಯಲ್ಗಳಲ್ಲಿ ಕಂಡುಬಂದ ಹಳೆಯ ಹೋಸ್ಥ ಘಟಕ. ನಾನು ಈಗಿನ ದಿನ ಹೊಸ ಟ್ಯುಟೋರಿಯಲ್‌ಗೆ ಇವನ್ನು ಡೀಫಾಲ್ಟ್ ಆಯ್ಕೆ ಮಾಡಿಕೊಳ್ಳುವುದಿಲ್ಲ. |
| `text-embedding-3-small` | ಕಡ್ಡಾಯ ಸ್ಥಳೀಯ embedding ಅಗತ್ಯವಿಲ್ಲದ ಬಲವಾದ ವೆಚ್ಚ/ಕಾರ್ಯಕ್ಷಮತೆ ಸಮತೋಲನ ಬೇಕಾದಾಗ ಆಧುನಿಕ ಹೋಸ್ಥ ಡೀಫಾಲ್ಟ್. |
| `text-embedding-3-large` | ವೆಕ್ಟರ್ ಗಾತ್ರ ಅಥವಾ embedding ವೆಚ್ಚಕ್ಕಿಂತ ಪ್ರಾಪ್ತಿಯ ಗುಣಾತ್ಮಕತೆ ಹೆಚ್ಚಾಗುತ್ತಿರುವಾಗ ಹೋಸ್ಥ ಆಯ್ಕೆ. |
| `BAAI/bge-small-en-v1.5` | ಟ್ಯುಟೋರಿಯಲ್‌ಗಳು, ಪ್ರೋಟೋಟೈಪ್ಗಳು ಮತ್ತು CPU ಸ್ನೇಹಿ ಪ್ರಯೋಗಗಳಿಗೆ ತೂಕ ಕಡಿಮೆ ಇಂಗ್ಲಿಷ್ ಸ್ಥಳೀಯ ಮೂಲಭೂತ. |
| `BAAI/bge-base-en-v1.5` ಅಥವಾ `BAAI/bge-large-en-v1.5` | ಉತ್ತಮ ಪ್ರಾಪ್ತಿಯ ಗುಣಮಟ್ಟ ಬೇಕಾದಾಗ ಮತ್ತು ಹೆಚ್ಚು ಗಣನೆಯ ಹೆಚ್ೕಗೆ ಮೊದಲು ಬಳಸಬಹುದಾದ ಸ್ಥಳೀಯ ಇಂಗ್ಲಿಷ್ ಮಾದರಿಗಳು. |
| `BAAI/bge-m3` | ಬಹುಭಾಷಾ ಅಥವಾ ಹೆಚ್ಚು ಪ್ರಸರಣContexts retrieval, ವಿಶೇಷವಾಗಿ ದಾಖಲೆಗಳು ಇಂಗ್ಲಿಷ್ ಮಾತ್ರವಲ್ಲ. |
| `sentence-transformers/all-MiniLM-L6-v2` | ಬಹಳ ಸಣ್ಣ ಮತ್ತು ವೇಗವಾದ ಅರ್ಥಸಾಧಕ ಹುಡುಕಾಟ ಮೂಲಭೂತ. ವೇಗ ಮತ್ತು ಸರಳತೆ ಅತ್ಯುತ್ತಮವಾಗಿರುವಾಗ ಉಪಯುಕ್ತ. |
| `nomic-embed-text-v1.5` | ದೀರ್ಘContexts ಅಥವಾ ಸಾಗಣೆ ಕಡೆಗೆ ಗಮನ ನೀಡಿ ಪರೀಕ್ಷಿಸಲು ತೆರೆಯಲ್ಪಟ್ಟ ಸ್ಥಳೀಯ embedding ಆಯ್ಕೆ. |

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

ನಂತರ ಪ್ರತಿ ತುಂಡಿಗೆ embedding ಸಿಗುತ್ತದೆ:

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

## 6. Qdrant ಸ್ಥಳೀಯ ಮೋಡ್ ನಲ್ಲಿ ವೆಕ್ಟರ್ಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ

ಈಗ ನಾವು in-memory Qdrant ಸಂಗ್ರಹಣೆಯನ್ನು ರಚಿಸಿ ತುಂಡುಗಳನ್ನು ಲೋಡ್ ಮಾಡಿದರೂ ಪೇಲೋಡ್ ಮೆಟಾಡೇಟಾ ಜೊತೆಗೆ ಸೇರ್ಪಡೆ ಮಾಡುತ್ತೇವೆ.

> [!NOTE]
> 2023 ಟ್ಯುಟೋರಿಯಲ್‌ನಲ್ಲಿ, ನಾನು FAISS ಬಳಸಿದೆ ಏಕೆಂದರೆ ಇದು LangChain ಜೊತೆಗೆ ಸ್ಥಳೀಯ ವೆಕ್ಟರ್ ಸಾದೃಶ್ಯ ಹುಡುಕಾಟ ತೋರಿಸಲು ಸರಳ ಮತ್ತು ಜನಪ್ರಿಯ ಮಾರ್ಗ. FAISS ಇನ್ನೂ ವೇಗವಾದ ಸ್ಥಳೀಯ ಪ್ರಯೋಗಗಳಿಗೆ ಉಪಯುಕ್ತವಾಗಿದೆ. 2026 ಆವೃತ್ತಿಯಲ್ಲಿ, ನಾನು Qdrant ಬಳಸುತ್ತೇನೆ ಏಕೆಂದರೆ ನಾನು ಟ್ಯುಟೋರಿಯಲ್ ಅನ್ನು ಉತ್ಪಾದನಾ RAG ವ್ಯವಸ್ಥೆಗೆ ಹೆಚ್ಚು ಹತ್ತಿರ ಅನುಭವಿಸಲು ಬಯಸುತ್ತೇನೆ. Qdrant ನನಗೆ ವೆಕ್ಟರ್ಗಳ ಜೊತೆಗೆ ಮೂಲ ಕಡತ, ವಿಭಾಗ ಶೀರ್ಷಿಕೆ, ದಾಖಲೆ ಆವೃತ್ತಿ ಮತ್ತು ಅನುಮತಿಗಳಂತಹ ಪೇಲೋಡ್ ಮೆಟಾಡೇಟಾ ಸಂಗ್ರಹಿಸಲು ಅವಕಾಶ ನೀಡುತ್ತದೆ. ಇದರಿಂದ ಪ್ರಾಪ್ತಿಯನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಪರಿಶೀಲಿಸುವುದು ಸುಲಭವಾಗುತ್ತದೆ ಹಾಗೂ ಉದಾಹರಣೆಯನ್ನು ಫಿಲ್ಟರಿಂಗ್, ಉಲ್ಲೇಖ ಮತ್ತು ಭವಿಷ್ಯದಲ್ಲಿ ಸ್ಥಿರ ಅಥವಾ ಸರ್ವರ್ ಆಧಾರಿತ ನಿಯೋಜನೆಗೆ ಸಿದ್ಧಮಾಡುತ್ತದೆ.

FAISS ವೆಕ್ಟರ್ ಸಾದೃಶ್ಯ ಹುಡುಕಾಟ ತೋರಿಸಲು ಉತ್ತಮವಾಗಿದೆ. Qdrant ಸಣ್ಣ ಆದರೆ ಉತ್ಪಾದನಾ ರೂಪಿಲ RAG ಪ್ರಾಪ್ತಿ ಪದರ ತೋರಿಸಲು ಉತ್ತಮ.

ಕೆಲವು ಪ್ರಾಯೋಗಿಕ ಪರ್ಯಾಯಗಳು:

| ವೆಕ್ಟರ್ ಸಂಗ್ರಹಣೆಯ / ಹುಡುಕಾಟ ಪದರ | ನಾನು ಯಾವಾಗ ಪರಿಗಣಿಸುವೆ |
| --- | --- |
| Qdrant | ಸ್ಥಳೀಯ ಪ್ರೋಟೋಟೈಪ್ಗಳು, ಮೆಟಾಡೇಟಾ ಫಿಲ್ಟರಿಂಗ್, ಉತ್ಪಾದನಾ-ಸ್ನೇಹಿ ವೆಕ್ಟರ್ ಹುಡುಕಾಟ ಮತ್ತು ಸುಲಭ ಪೈಥಾನ್ ಕಾರ್ಯಪ್ರವಾಹ. |
| Chroma | ತ್ವರಿತ ಸ್ಥಳೀಯ RAG ಪ್ರಯೋಗ ಮತ್ತು ಸರಳತೆ ಅತ್ಯಂತ ಮುಖ್ಯವಾದ ನೋಟ್‌ಬುಕ್‌ಗಳು. |
| FAISS | ಸರಳ ಸ್ಥಳೀಯ ವೆಕ್ಟರ್ ಹುಡುಕಾಟ ಅಗತ್ಯವಿದ್ದಾಗ ಮತ್ತು ಮೆಟಾಡೇಟಾ ಪ್ರತ್ಯೇಕವಾಗಿ ನಿರ್ವಹಿಸಬಹುದಾದಾಗ ತೂಕ ಕಡಿಮೆ. |
| Milvus | ತಂಡವು ವಿಶೇಷ ವೆಕ್ಟರ್ ಡೇಟಾಬೇಸ್ ನಂತೆ ದೊಡ್ಡ ಮಟ್ಟದ ಓಪನ್-ಸೋರ್ಸ್ ವೆಕ್ಟರ್ ಹುಡುಕಾಟ ನಡೆಸಲು ಸಿದ್ಧನಾಗಿರುವಾಗ. |
| Weaviate | ಸ್ಕೀಮಾ, ಮೆಟಾಡೇಟಾ, ಹೈಬ್ರಿಡ್ ಹುಡುಕಾಟ ಮತ್ತು ನಿರ್ವಹಿತ ಅಥವಾ ಸ್ವಯಂ-ಹೋಸ್ಟ್ ಆದ ನಿಯೋಜನೆ ಆಯ್ಕೆಗಳೊಂದಿಗೆ ವೆಕ್ಟರ್ ಹುಡುಕಾಟ. |
| ಅಜೂರ್ AI ಸರ್ಚ್ | ಮಾಹಿತಿ ಹುಡುಕಾಟ, ವೆಕ್ಟರ್ ಹುಡುಕಾಟ, ಹೈಬ್ರಿಡ್ ಪ್ರಾಪ್ತಿ, ಅರ್ಥಮೌಲ್ಯ ಕ್ರಮ, ಫಿಲ್ಟರಿಂಗ್, ಭದ್ರತೆ ಹಾಗೂ ನಿರ್ವಹಿತ ಕಾರ್ಯಾಚರಣೆಗಳನ್ನು ಒಬ್ಬಶಃ ಹುಡುಕಾಟ ಪದರದಲ್ಲಿ ಬೇಕಾದಾಗ ಎಂಟರ್‌ಪ್ರೈಸ್ RAG. |
| PostgreSQL + pgvector | PostgreSQL ಬಳಸುತ್ತಿರುವ ತಂಡಗಳಿಗೆ ಅಪ್ಲಿಕೇಶನ್ ಡೇಟಾ ಹತ್ತಿರವೇ ವೆಕ್ಟರ್ ಹುಡುಕಾಟ ಇಚ್ಛಿಸಿದಾಗ. |

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

ನಂತರ ಪಾಯಿಂಟ್ ಗಳನ್ನು ಸೇರ್ಪಡೆಗೊಳಿಸಿ:

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

ನನ್ನ ಚಾಲನೆಯಲ್ಲಿ, ಸಂಗ್ರಹಣೆ 8 ವೆಕ್ಟರ್ಗಳನ್ನು ಸೇರಿಸಿತು.

ಇಲ್ಲಿಂದ RAG ವ್ಯವಸ್ಥೆ ಪರಿಶೀಲನೀಯವಾಗಲು ಪ್ರಾರಂಭಿಸುತ್ತದೆ. ವೆಕ್ಟರ್ ಡೇಟಾಬೇಸ್ ಕೇವಲ ವೆಕ್ಟರ್ಗಳನ್ನು ಸಂಗ್ರಹಿಸುವುದಲ್ಲ; ಇದು ಸಾಕ್ಷ್ಯ ಪಠ್ಯ ಮತ್ತು ಉಲ್ಲೇಖಗಳಿಗೆ ಅಗತ್ಯವಿರುವ ಮೆಟಾಡೇಟಾವನ್ನು ಸಂಗ್ರಹಿಸುತ್ತದೆ.

## 7. ಅಭ್ಯರ್ಥಿ ತುಂಡುಗಳನ್ನು ಪ್ರಾಪ್ತಿಪಡಿಸಿ

ಈಗ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ ಅಭ್ಯರ್ಥಿ ತುಂಡುಗಳನ್ನು ಪ್ರಾಪ್ತಿಪಡಿಸೋಣ.

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

ಈ ಸಂದರ್ಭದಲ್ಲಿ, ಉತ್ತರ ನಿರ್ಮಿಸುವ ಮೊದಲು ನಾನು ಪ್ರಾಪ್ತಿಪಡಿಸಿದ ತುಂಡುಗಳನ್ನು ಮುದ್ರಿಸುತ್ತೇನೆ. ಇದು ಮಹತ್ವಪೂರ್ಣ. ಪ್ರಾಪ್ತಿಯಲ್ಲಿ ತಪ್ಪಿದ್ದರೆ, ಉತ್ಪಾದನೆ ಸಮಸ್ಯೆಯನ್ನು ಪಾಠಪರ ಚಿಂತನೆಯ ಅಡಿಯಲ್ಲಿ ಮರೆಯಬಹುದು.

## 8. ತೂಕ ಕಡಿಮೆ ಮರುಸ್ಥಾನಕಾರನನ್ನು ಸೇರಿಸಿ

ನಾನು ಪ್ರಥಮವಾಗಿ ಪ್ರಾಪ್ತಿ ಮಾರ್ಗವನ್ನು ಪರೀಕ್ಷಿಸಿದಾಗ, ವೆಕ್ಟರ್ ಸಾದೃಶ್ಯ ಮಾತ್ರ ಸಂಬಂಧಿಸಿದ ನীতি ವಿಷಯವನ್ನು ಕಂಡುಹಿಡಿದಿತು, ಆದರೆ ಅತಿ ಖಚಿತ ವಿಭಾಗ ಮೇಲುಗೈಗಿಲ್ಲ.

ಹೀಗಾಗಿ ನಾನು ಸಣ್ಣ ಸ್ಥಳೀಯ ಮರುಸ್ಥಾನಕಾರನನ್ನು ಸೇರಿಸಿರುತ್ತೇನೆ. ಇದು ಪ್ರಶ್ನೆಯ ಪದಗಳು ವಿಭಾಗ ಶೀರ್ಷಿಕೆ ಮತ್ತು ವಿಷಯದೊಂದಿಗೆ ಹೊಂದಿದಾಗ ಹೆಚ್ಚಿನ ತೂಕ ನೀಡುತ್ತದೆ.

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

ಮರುಸ್ಥಾನ ಮಾಡಿದ ಮೇಲೆ, ಮೇಲುಗೈ ಫಲಿತಾಂಶ:

```text
school_ai_policy.md / Final Assignments
```

ಅದು ಪರೀಕ್ಷಾ ಪ್ರಶ್ನೆಗೆ ನಿರೀಕ್ಷಿತ ವಿಭಾಗ.

ಇದು ಮೊದಲ ಅನುಷ್ಠಾನದ ಅತ್ಯಂತ ಉಪಯುಕ್ತ ಪಾಠವಾಗಿತ್ತು. ಸಣ್ಣ ಸ್ಥಳೀಯ ಉದಾಹರಣೆಯಲ್ಲೂ ಪ್ರಾಪ್ತಿಗುಣಮಟ್ಟವು ವೆಕ್ಟರ್ ಸಾದೃಶ್ಯವನ್ನು ಮತ್ತೊಂದು ಸಂಕೇತದೊಂದಿಗೆ ಸಂಯೋಜಿಸಿದಾಗ ಸುಧಾರಿತವಾಯಿತು.

## 9. ನೆಲಸಿದ ಸ್ಥಳೀಯ ಉತ್ತರವನ್ನು ರಚಿಸಿ

ಡೀಫಾಲ್ಟ್ ಮಾರ್ಗದಲ್ಲಿ, ನಾನು LLM ಬದಲು ಪಾರದರ್ಶಕ ಸ್ಥಳೀಯ ಉತ್ತರ ರಚನಕಾರನನ್ನು ಬಳಸುತ್ತೇನೆ.

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

ಇದು ಅಂತಿಮ ಉತ್ಪನ್ನ ಉತ್ತರ ರಚತೆ ಅಲ್ಲ. ಇದು ದೋಷಾಂಶ ಪರಿಶೋಧನೆ ಸಾಧನ. ಇದು retrieval, metadata ಮತ್ತು ಉಲ್ಲೇಖ ತಂತಿಯನ್ನು ಕಾರ್ಯನಿರ್ವಹಿಸುವುದು ವಿಚಲನ ಸೇರಿಸುವ ಮುಂಚೆ ಸಾಬೀತುಪಡಿಸುತ್ತದೆ.

## 10. Oluama ಮತ್ತು Phi-4-mini ಜೊತೆಗೆ ಸ್ಥಳೀಯ ಉತ್ತರವನ್ನು ರಚಿಸಿ

ಪ್ರಾಪ್ತಿ ಕೆಲಸ ಮಾಡುವಾಗ, ನೋಟ್‌ಬುಕ್ ಕೊನೆಯ ಉತ್ತರ ಹಂತವನ್ನು Oluama ಮತ್ತು `phi4-mini:3.8b` ಮೂಲಕ ಬದಲಾಯಿಸಬಹುದು.

> [!NOTE]
> Oluama ಕೇವಲ ಅಂತಿಮ ಉತ್ತರ-ತಯಾರಿಕೆ ಹಂತವನ್ನು ಬದಲಾಯಿಸಬೇಕು. ಕಡತ ಲೋಡ್ ಮಾಡುವುದು, ತುಂಡುಮಾಡುವುದು, ವೆಕ್ಟರ್ ಸಂಗ್ರಹಣೆಯ, ಪ್ರಾಪ್ತಿ, ಮರುಸ್ಥಾನ ಮತ್ತು ಉಲ್ಲೇಖ ತಂತಿಗಳು ಹಾಗೆ ಇದೆ.

ಮೊದಲು, ನೋಟ್‌ಬುಕ್ ಪ್ರಾಪ್ತಿಪಡಿಸಿದ ತುಂಡುಗಳಿಂದ ಸಾಕ್ಷ್ಯ ಪ್ರಾಂಪ್ಟ್ ರಚಿಸುತ್ತದೆ:

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

ಈ ಟ್ಯುಟೋರಿಯಲ್ ಗೆ ನಾನು Oluama ಮೂಲಕ Microsoft's Phi-4-mini ಕುಟುಂಬವನ್ನು ಡೀಫಾಲ್ಟ್ ಸ್ಥಳೀಯ ನಿರ್ಮಾಣ ಆಯ್ಕೆಯಾಗಿ ಶಿಫಾರಸು ಮಾಡುತ್ತೇನೆ. Oluama ಯಲ್ಲಿ ನಾನು ಪರೀಕ್ಷಿಸಿದ ಮಾದರಿಯ ಹೆಸರು:

```powershell
ollama pull phi4-mini:3.8b
```

ನೀವು ತ್ವರಿತವಾಗಿ ಮಾದರಿ ಲಭ್ಯವಿದೆಯೋ ಇಲ್ಲವೋ ಚೆಕ್ ಮಾಡಬಹುದು:

```powershell
ollama list
```

ನಂತರ ಈ ವ್ಯತ್ಯಯಗಳನ್ನು ಹೊಂದಿಸಿ:

```powershell
Copy-Item .env.example .env
```

`.env` ಅನ್ನು ತೆರೆಯಿರಿ ಮತ್ತು ಸರಣಿ 2 Oluama ಮೌಲ್ಯಗಳನ್ನು ಅನ್‌ಕಮೆಂಟ್ ಮಾಡಿ:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

ನೋಟ್‌ಬುಕ್ `python-dotenv` ಮೂಲಕ `.env` ಅನ್ನು ಸಂಗ್ರಹಣಾ ಮೂಲದಿಂದ ಲೋಡ್ ಮಾಡುತ್ತದೆ, ನಂತರ ಒಂದೇ ಸಾಕ್ಷ್ಯ ಪ್ರಾಂಪ್ಟ್ Oluama ಯ ಸ್ಥಳೀಯ `/api/chat` ಅಂತರ್ಜಾಲಕ್ಕೆ ಸ್ಟ್ರೀಮಿಂಗ್ ನಿಷ್ಕ್ರೀಯಗೊಂಡಂತೆ ಕಳುಹಿಸುತ್ತದೆ. Oluama ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿಲ್ಲ ಅಥವಾ `SERIES2_OLLAMA_MODEL` ಲಭ್ಯವಿಲ್ಲದಿದ್ದರೆ, ಈ ಮಾರ್ಗವನ್ನು ತವಕಿಸಲಾಗುತ್ತದೆ.

> [!NOTE]
> ಈ ಯಂತ್ರದಲ್ಲಿ, `phi4-mini:3.8b` ಸುಮಾರು 2.49GB ಮಾದರಿ ಕಡತಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿತು. ನಿರ್ಧಾರ ವೇಳೆ Oluama 3.3GB ಓಲಾಗಿರುವ ಮಾದರಿ ಗಾತ್ರವನ್ನು ವರದಿ ಮಾಡಿತು ಮತ್ತು RTX 3060 ಲ್ಯಾಪ್‌ಟಾಪ್ GPU ಬಳಸಿ.

ಇದರಿಂದ ಟ್ಯುಟೋರಿಯಲ್ ಎರಡು ಹಂತಗಳಾಗಿವೆ:

1. CPU-ಮಾತ್ರ ನಿರ್ದಿಷ್ಟ ಉತ್ತರ ರಚನಕಾರ.
2. Oluama ಮತ್ತು Phi-4-mini ಸಹಿತ ಸ್ಥಳೀಯ ಉತ್ತರ ರಚನೆ.

ಎರಡೂಲ್ಲಿ retrieval ಪೈಪ್‌ಲೈನ್ ಇನ್ನೂ ಒಂದೇ.

## 11. ಪರಿಶೀಲನಾ ಫಲಿತಾಂಶ

ನಾನು ನೋಟ್‌ಬುಕ್ ಅನ್ನು ವಿಂಡೋಸ್ ನಲ್ಲಿ Python 3.12.6 ಸಹಿತ ಸ್ಥಳೀಯವಾಗಿ ನಡೆಸಿದೆ.

ಸಂಸ್ಥಾಪಿತ ಪ್ಯಾಕೇಜುಗಳು:

| ಪ್ಯಾಕೇಜ್ | ಆವೃತ್ತಿ |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

ನೋಟ್‌ಬುಕ್ ನಿರ್ವಹಣೆ:

- ನೋಟ್‌ಬುಕ್: `notebooks/series-2-open-source-rag.ipynb`
- ನಿರ್ವಹಣಾ ಫಲಿತಾಂಶ: `nbclient` ಮೂಲಕ ಯಶಸ್ವಿ
- ಲೋಡ್ ಮಾಡಿದುದಾದ ದಾಖಲೆಗಳ ಸಂಖ್ಯೆ: 2
- ಸೃಷ್ಟಿಸಿದ ತುಂಡುಗಳ ಸಂಖ್ಯೆ: 8
- Qdrant ಸಂಗ್ರಹಣೆ: `school_policy_local`
- ಸೇರಿಸಲಾದ ವೆಕ್ಟರ್ಗಳು: 8
- embedding ಮಾದರಿ: `BAAI/bge-small-en-v1.5`
- embedding ಗಾತ್ರ: 384
- ರಿಟ್ರೀವಲ್ ಪ್ರಶ್ನೆ: "ನಾನು ನನ್ನ ಅಂತಿಮ ಹುದ್ದೆಗಾಗಿ ಜನರೇಟಿವ್ AI ಬಳಸಬಹುದೇ?"
- ರೆರ್ಯಾಂಕಿಂಗ್ ಮಾರ್ಗ: ತೂಕ ಕಡಿಮೆ ಸ್ಥಳೀಯ ಲೆಕ್ಸಿಕಲ್ ರೆರ್ಯಾಂಕಿಂಗ್
- ರೆರ್ಯಾಂಕಿಂಗ್ ನಂತರ ಟಾಪ್ ರಿಟ್ರೈವ್ಡ് ಮೂಲ: `school_ai_policy.md`
- ರೆರ್ಯಾಂಕಿಂಗ್ ನಂತರ ಟಾಪ್ ರಿಟ್ರೈವ್ಡ് ವಿಭಾಗ: `Final Assignments`
- ಡೀಫಾಲ್ಟ್ ಉತ್ತರ ಮಾರ್ಗ: ಸ್ಥಳೀಯ ಪಾರದರ್ಶಕ ಉತ್ತರ ರಚನೆ
- ಒಲ್ಲಾಮಾ ಉತ್ಪಾದನಾ ಮಾರ್ಗ: `phi4-mini:3.8b` ಮೂಲಕ ಪೂರ್ಣಗೊಂಡಿದೆ
- ಒಲ್ಲಾಮಾ ಮಾದರಿ ಫೈಲ್ ಗಾತ್ರ: ಡಿಸ್ಕ್‌ನಲ್ಲಿ 2.49GB
- ಒಲ್ಲಾಮಾ ಲೋಡ್ ಮಾಡಿದ ಮಾದರಿ ಗಾತ್ರ: `ollama ps` ಮೂಲಕ ವರದಿಯಾದ 3.3GB
- GPU ಆಫ್‌ಲೋಡ್: `ollama ps` ಮೂಲಕ ವರದಿಯಾದಂತೆ 100% GPU
- ಉತ್ಪಾದನೆಯ ನಂತರ GPU 메모ರಿ: RTX 3060 ಲ್ಯಾಪ್‌ಟಾಪ್ GPU ನಲ್ಲಿ 6GB ನಿಂದ ಸುಮಾರು 3.5GB ಬಳಕೆ
- ಫಾಸ್ಟ್‌ಎಂಬೆಡ್ ಮಾದರಿ ಮತ್ತು ಒಲ್ಲಾಮಾ ಉತ್ಪಾದನೆ ಸಕ್ರಿಯಗೊಂಡ ನೋಟ್ಬುಕ್ ಕಾರ್ಯನಿರ್ವಹಣೆ: ಪರಿಶೀಲನಾ ಸ್ಕ್ರಿಪ್ಟ್ ಮೂಲಕ ಸುಮಾರು 34 ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಯಶಸ್ವಿ

ಒಲ್ಲಾಮಾ-ಉತ್ಪಾದಿತ ಉತ್ತರ:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

ನಾನು ಈ ಉತ್ತರವನ್ನು ಪರಿಪೂರ್ಣ ಎಂದು ಕರೆಯುವುದಿಲ್ಲ. ಇದು ಸರಿಯಾದ ಸಾಕ್ಷ್ಯದಿಂದ ಉತ್ತರ ನೀಡುತ್ತದೆ, ಆದರೆ ಅಂತಿಮ ಮೂಲ ಸಾಲು ನಿರ್ಧಾರಾತ್ಮಕ ಉಲ್ಲೇಖ ಫಾರ್ಮ್ಯಾಟ್ ಹೋಲಿಕೆಯಂತೆ ಸ್ಪಷ್ಟವಿಲ್ಲ. ಇದು ಟ್ಯೂಟೋರಿಯಲ್‌ನಲ್ಲಿ ತೋರಿಸುವುದಕ್ಕೆ ಉಪಯುಕ್ತ, ಏಕೆಂದರೆ ಮುಂದಿನ ಎಂಜಿನಿಯರಿಂಗ್ ಪ್ರಶ್ನೆಯನ್ನು ಸ್ಪಷ್ಟಪಡಿಸುತ್ತದೆ: ಉತ್ತರ ಉತ್ಪಾದನೆಗೆ ನಿರ್ವಹಣೆ ಅಗತ್ಯವಿದೆ, ಕೇವಲ ರಿಟ್ರೀವಲ್ ಮಾತ್ರವಲ್ಲ.

ಈ ಪರಿಶೀಲನೆ ವೇಳೆ ನಾನು ಮುಖ್ಯವಾಗಿ ಕಲಿತದ್ದು, ಉತ್ತರ ಉತ್ಪಾದನೆಗೆ ಮುನ್ನ ರಿಟ್ರೀವಲ್ ಗುಣಮಟ್ಟ ಪರೀಕ್ಷಿಸಬೇಕು ಎಂಬುದು. ಎಂಬೆಡ್ಡಿಂಗ್ ಫಲಿತಾಂಶ ಈಗಾಗಲೇ ಉಪಯುಕ್ತವಾಗಿತ್ತು, ಮತ್ತು ತೂಕ ಕಡಿಮೆ ರೆರ್ಯಾಂಕರ್ ನಿರೀಕ್ಷಿತ ನೀತಿ ವಿಭಾಗವನ್ನು ನಂಬಿಕೆಗೊಳ್ಳುವಂತೆ ಮೊದಲು ತೋರಿಸಿತು. ಇದು ನಾನು ಟ್ಯೂಟೋರಿಯಲ್‌ನಲ್ಲಿ ಬಹಿರಂಗಪಡಿಸಲು ಬಯಸುವ ಸಣ್ಣ ವ್ಯವಸ್ಥೆಯ ನಡವಳಿಕೆಯಾಗಿದೆ, ಅದನ್ನು ಮರೆಯಬೇಡಿ.

## 12. ಮುಂದೇನು ಬರುತ್ತದೆ

ಮುಂದಿನ ಸುಧಾರಣೆವೆಂದರೆ ಈ ಸ್ಥಳೀಯ ಸജ್ಜಿಕರಣವನ್ನು ಆಜೂರ್ ನ ನಿರ್ವಹಿತ ಆವೃತ್ತಿಯೊಂದಿಗೆ ಹೋಲಿಸಲಾಗುವುದು, ಏಕೆಂದರೆ ಇದು ಶಾಲಾ ನೀತಿ ಸಹಾಯಕ ನೇರತೆಗೆ ಸೇರಿದುದು. ಸನ್ನಿವೇಶ ನಿಗದಿ ಪಡಿಸಿದರೆ, ಸ್ಥಾಪನೆಯ ಸಂಕೀರ್ಣತೆ, ರಿಟ್ರೀವಲ್ ನಿಯಂತ್ರಣಗಳು, ಗುರುತುಮಾಡುವಿಕೆಯ ಒಗ್ಗೂಡಿಕೆ, ಕಾರ್ಯಾಚರಣೆ ಮಾಲೀಕತ್ವ ಮತ್ತು ವೆಚ್ಚವನ್ನು ಸುಲಭವಾಗಿ ನೋಡಿ ತಿಳಿಯಬಹುದಾಗಿದೆ.

## 13. ಉಲ್ಲೇಖಗಳು

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

ಹಿಂದಿನದು: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ಅಸ್ವೀಕಾರ**:
ಈ ದಸ್ತಾವೇಜು AI ಅನುವಾದ ಸೇವೆ [Co-op Translator](https://github.com/Azure/co-op-translator) ಬಳಸಿ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ನಿಖರತೆಯನ್ನು ಸಾಧಿಸಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದರೂ, ದಯವಿಟ್ಟು ಗಮನಿಸಿ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ದೋಷಗಳು ಅಥವಾ ಅಸಡ್ಡೆಗಳು ಇರಬಹುದು. ಮೂಲ ಭಾಷೆಯಲ್ಲಿರುವ ಮೂಲ ದಸ್ತಾವೇಜು ಪ್ರಾಮಾಣಿಕ ಮೂಲವೆಂದು ಪರಿಗಣಿಸಬೇಕು. ಪ್ರಮುಖ ಮಾಹಿತಿಗಾಗಿ, ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ. ಈ ಅನುವಾದವನ್ನು ಬಳಸುವ ಮೂಲಕ ಉಂಟಾಗುವ ಯಾವುದೇ ತಪ್ಪು ಅರ್ಥಗಳ ಅಥವಾ ತಪ್ಪು ವ್ಯಾಖ್ಯಾನಗಳ ಬಗ್ಗೆ ನಾವು ಹೊಣೆಗಾರರಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->