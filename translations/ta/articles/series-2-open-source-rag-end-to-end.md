# உங்கள் ஆவணங்களின் அடிப்படையில் கேள்விகளுக்கு பதிலளிக்க AI ஐ கற்றுத்தரவும்
## தொடர் 2: உள்ளூர் திறந்த மூல RAG அமைப்பை முழுமையாக உருவாக்கவும்

![உள்ளூர் திறந்த மூல RAG பயிற்சி குழாய்](../../../assets/images/series-2-local-rag.svg)

> இந்த கட்டுரை தொடர் 1 கட்டமைப்பு உரையாடலை இயக்கத்தக்க உள்ளூர் RAG பயிற்சியாக மாற்றுகிறது. இலக்காக இரண்டு நிலை தரவுடன் முதல் முழு வேலைப்பாட்டை மேக கணக்கு மற்றும் உயிரணு விவரங்கள் இல்லாமல் உருவாக்குவது, பின்னர் அந்த இயங்கும் அடிப்படையை சிறந்த கட்டமைப்பு முடிவுகளை எடுக்க பயன்படுத்துவது ஆகும்.

நாம் உருவாக்கப்போகும் அமைப்பு ஒரு சிறிய பள்ளி கொள்கை உதவியாளராகும். நான் இரண்டு உள்ளூர் மார்க்டவுன் ஆவணங்களை அறிவு அடிப்படையாக பயன்படுத்தி, பின் முழு RAG குழாயின் வழிமுறைகளை கடந்து செல்லுகிறேன்: துண்டிப்பது, உள்ளூர் ஒட்டுமொத்தங்கள், Qdrant வெக்டார் சேமிப்பு, மீட்பு, மறுவிருத்தம், மூல அறியப்பட்ட பதில் அமைத்தல், மற்றும் விருப்பமானுள்ளூர் உருவாக்கம் Ollama மற்றும் Phi-4-mini உடன்.

தொடர் வழிசெலுத்தல்: [கூடாரம் முகப்பு](../README.md) | முந்தையது: [தொடர் 1 - RAG, Azure மற்றும் திறந்த மூல மாற்றுகள், மற்றும் சிறந்த பயிற்சி தேவையெனில்](./series-1-rag-azure-open-source-fine-tuning.md)

குறியீடு புத்தகம்: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | தேவைகள்: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> மேக வளங்களை உருவாக்கும் முன் RAG குழாயை புரிந்து கொள்ள இது சிறந்த துவக்கம். இயல்புநிலை பாதை உள்ளூர்ப் பதில்கள் மற்றும் உயிரணு விவரங்கள் இல்லாமல் CPU நட்பு ஒட்டுமொத்தங்களை இயக்குகிறது.

## 1. நாம் உருவாக்கப்போகும் ஒன்று என்ன

2023 பயிற்சியில், நான் Azure மூலம் துவங்கினேன் ஏனெனெனில் இலக்காக Azure AI தேடல் மற்றும் Azure OpenAI PDF ஆவணங்களில் இருந்து கேள்விகளுக்கு பதில் அளிப்பதை காட்டுவது.

இந்த 2026 தொடருக்காக, நான் ஒரு அடுக்கு கிழிக்கவேண்டும்.

மேலாண்மை சேவைகளை பயன்படுத்தும் முன், ஒரு சிறிய RAG அமைப்பை உள்ளூரில் உருவாக்கி ஒவ்வொரு படியையும் பாங்காக்க விரும்புகிறேன்: ஆவணங்களை ஏற்றுதல், உரையை துண்டிப்பது, வெக்டார்கள் சேமித்தல், ஆதாரம் மீட்பது, மறுவிருத்தம் செய்தல், மற்றும் மூல அறிந்த பதிலை மீட்டெடுக்க.

மாதிரி காட்சி பள்ளி கொள்கை உதவியாளராகும். பயனர் கேட்கிறார்:

```text
Can I use generative AI for my final assignment?
```

அமைப்பு பொதுவான மாதிரி நினைவகத்திலிருந்து பதிலளிக்க கூடாது. தொடர்புடைய கொள்கை பிரிவை மீட்டெடுக்கவேண்டும் மற்றும் அதில் இருந்து பதில் வழங்கவேண்டும்.

முழு இயக்கக்கூடிய பதிப்பு [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) இல் உள்ளது. கீழே உள்ளக் குறியீடு முக்கிய படி நடவடிக்கைகளை காட்டுகிறது எனவே இந்த கட்டுரையை பயிற்சியாகப் படிக்கலாம்.

## 2. உள்ளூர் சார்புகளை நிறுவுதல்

ஒரு மெய்ப்பேர் சூழலை உருவாக்கி தொடர் 2 தேவைப்பட்டலை நிறுவவும்:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

முதல் பதிப்பு Qdrant உள்ளூர் செயல்பாட்டையும் FastEmbed ஐ பயன்படுத்துகிறது. Qdrant இன் Python கிளையன்ட் `QdrantClient(":memory:")` என்ற in-memory உள்ளூர் முறையை ஆதரிக்கிறது, இது உள்ளூர் பயிற்சிகள் மற்றும் CI-தொழில்நுட்ப சோதனைக்குப் பயன்படும். FastEmbed க்கு மேக API விசை தேவையற்ற மெய்யான உள்ளூர் embedding மாதிரி கிடைக்கிறது.

தேவைப்பட்டல் கோப்பில் `python-dotenv` கூட சேர்க்கப்பட்டுள்ளது ஏனெனெனில் குறியீடுபுத்தகம் விருப்பமாக Ollama மாதிரி பெயரை `.env` இலிருந்து வாசிக்கலாம். இந்த உள்ளூர் பயிற்சிக்கு Azure OpenAI அல்லது OpenAI API விசை தேவை இல்லை.

## 3. மாதிரி ஆவணங்களை ஏற்றல்

மாதிரி தொகுப்பு குறைவாக திட்டமிடப்பட்டுள்ளது:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

குறியீடுபுத்தகத்தில், நான் `sample_data/` இலிருந்த அனைத்து மார்க்டவுன் கோப்புகளையும் ஏற்றுகின்றேன்:

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

குறியீடுபுத்தகம் இயக்கும்போது 2 ஆவணங்கள் ஏற்றப்பட்டது. இது மிகச்சிறியதாக உள்ளது என்பதால் கையால் பரிசோதிப்பதற்கும் RAG குழாய் முதன்முதலான பதிப்பை உருவாக்குவதற்கும் உதவிகரமாகும்.

## 4. மார்க்டவுன் தலைப்புகளின்படி துண்டிப்பது

அடுத்த படி ஆவணங்களை துண்டுகளாகப் பிரிப்பது.

இந்த பயிற்சிக்காக, நான் கட்டமைப்பு அறிகுறியாக மார்க்டவுன் தலைப்புகளை பயன்படுத்துகிறேன். ஆவணத் தலைப்பு `#` இலிருந்து வரும், ஒவ்வொரு பிரிவு துண்டும் `##` இலிருந்து வரும்.

> [!NOTE]
> துண்டிமுறைகள் பல்-உறுதுணை இல்லை. இந்த பயிற்சியில் நான் மார்க்டவுன் தலைப்புகளை பயன்படுத்துகிறேன் ஏனெனெனில் மாதிரி ஆவணங்களில் தெளிவான `#` மற்றும் `##` கட்டமைப்பு உள்ளது. PDF-கள், Word ஆவணங்கள், ஸ்லைடுகள், டிக்கெட்டுகள் அல்லது வலைப்பக்கங்கள் ஆகியவற்றிற்காக வேறு நுட்பமாக பக்கம் எல்லைகள், வடிவமைப்பு தகவல், பொருத்த பிரிவுகள், டோக்கன் எல்லைகள், அட்டவணைகள் அல்லது மெட்டாடேட்டா போன்றவை பயன்படுத்தப்படலாம். முக்கியமானது உங்கள் ஆவணங்களுக்கு பொருள் மற்றும் மூலத்தை கண்காணிப்பதற்கு ஏற்ற துண்டிமுறை எடுக்க வேண்டும்.

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

பின்னர் இதை ஒவ்வொரு ஆவணத்திலும் பயன்படுத்துகிறேன்:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

இது எனது உள்ளூர் இயக்கத்தில் 8 துண்டுகளை உருவாக்கியது.

இந்த படியில் என்ன விரும்பியது என்றால், மெட்டாடேட்டா ஏற்கனவே பயனுள்ளதாக உள்ளது. ஒவ்வொரு துண்டும் அதன் `source`, `sectionHeading`, `documentVersion`, மற்றும் இடத்தை நிரப்பும் `permissions` ஐ அறிவது உள்ளது. சிறிய பயிற்சியிலும் இதனால் மேற்கோள்கள் மற்றும் பின்பு அனுமதி-அறிந்த மீட்பு எளிதாக யோசிக்க முடிகிறது.

## 5. உள்ளூர் ஒட்டுமொத்தங்களை உருவாக்குதல்

முதலாவது பொது பதிப்பிற்காக நான் FastEmbed மூலம் `BAAI/bge-small-en-v1.5` ஐ பயன்படுத்துகிறேன்.

இது பயிற்சியைக் உள்ளூர்வைத்து CPU நட்பு ஆக்குகிறது, ஆனால் இடத்தை நிரப்பும் வெக்டார் செயல்பாடுகளுக்கு பதிலாக உண்மையான ஓட்டுமொத்த மாதிரியைப் பயன்படுத்துகிறது. முதல் ஓட்டத்தில் மாதிரி எடையை பதிவிறக்குகிறது. பின்னர் குறியீடுபுத்தகம் உள்ளூர் கேஷை மீண்டும் பயன்படுத்தலாம்.

> [!NOTE]
> நான் `BAAI/bge-small-en-v1.5` ஐ பயன்படுத்துகிறேன் ஏனெனெனில் இது நகர நாள் English ஒட்டுமொத்த மாதிரியானது, FastEmbed மற்றும் Qdrant உடன் உள்ளூர் பயிற்சிக்காக பொருத்தமாக உள்ளது. இது 384 பரிமாண வெக்டார்கள் உருவாக்குகின்றது, எனவே இன்னும் வேகமாகவும் மற்றும் குறைந்த செலவில் உள்ளூரில் இயக்க முடிகிறது. இது ஒரே நல்ல தேர்வு அல்ல. 2023ல், பல பயிற்சிகள் `text-embedding-ada-002` போன்ற ஏற்பாடுகளுடன் நேர்த்துப்படுத்திய ஹோஸ்ட் ஓட்டுமொத்த மாதிரிகளைப் பயன்படுத்தின. இன்று மேம்பட்ட ஹோஸ்ட்டு விருப்பங்கள் `text-embedding-3-small` மற்றும் `text-embedding-3-large` போன்றவை மற்றும் திறந்த மூல விருப்பங்கள் BGE, E5, MiniLM, Nomic Embed மற்றும் பன்மொழி மாதிரிகள் `BAAI/bge-m3` போன்றவை உள்ளன; இவை உங்கள் ஏற்றுமதி வேலைப்பாடுக்களின் அடிப்படையில் எல்லாம் பொருத்தமான தேர்வுகள். உற்பத்தியில், சரியான ஓட்டுமொத்த மாதிரியை உங்கள் சொந்த ஆவணங்களில் மீட்புத்திறன் மதிப்பீட்டியுடன் தேர்ந்தெடுக்கவேண்டும்.

சில நடைமுறை மாற்றுகள்:

| மாதிரி குடும்பம் | நான் எப்பொழுது பரிசீலிப்பேன் |
| --- | --- |
| `text-embedding-ada-002` | 2023 காலத்தின் பல பயிற்சிகளில் தோன்றிய முதலாம் கால ஹோஸ்ட் அடிப்படை. இன்று புதிய பயிற்சிக்கு நான்இதை இயல்புநிலை தேர்வாக தேர்ந்தெடுக்க மாட்டேன். |
| `text-embedding-3-small` | சக்திவாய்ந்த செலவு/திறன் சமன்வயத்துடன் உள்ளூர் ஓட்டுமொத்தங்களை தேவையில்லை என்றால் நவீன ஹோஸ்ட் இயல்புநிலை. |
| `text-embedding-3-large` | வெக்டார் அளவு அல்லது ஓட்டுமொத்த செலவுக்கு அதிக பக்குவமுள்ளதே மீட்பு தரம் முக்கியமான போது ஹோஸ்ட் விருப்பம். |
| `BAAI/bge-small-en-v1.5` | பயிற்சிகள், மாதிரிகள் மற்றும் CPU நட்பு பரிசோதனைகளுக்கான இலகுவான உள்ளூர் ஆங்கில அடிப்படையாளர். |
| `BAAI/bge-base-en-v1.5` அல்லது `BAAI/bge-large-en-v1.5` | சிறந்த மீட்பு தரம் மற்றும் அதிக கணினி வளத்தைத் தர விரும்பும் போது பெரிய உள்ளூர் ஆங்கில மாதிரிகள். |
| `BAAI/bge-m3` | பன்மொழி அல்லது நீண்ட உள்ளடக்கம் மீட்பு, குறிப்பாக ஆவணங்கள் மட்டும் ஆங்கிலமல்லாத போது. |
| `sentence-transformers/all-MiniLM-L6-v2` | மிக சிறிய மற்றும் வேகமான பொருத்த தேடல் அடிப்படை. வேகம் மற்றும் எளிமை முக்கியமான போதும் உதவிகரமாக இருக்கும். |
| `nomic-embed-text-v1.5` | நீண்ட உள்ளடக்கம் அல்லது கடத்தலுக்கான திறந்த உள்ளூர் ஓட்டுமொத்த விருப்பம், சோதனைக்கு அர்ப்பணிக்கப்பட்டது. |

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

பின்னர் ஒவ்வொரு துண்டுக்கும் ஓட்டுமொத்தத்தை கொடுக்கிறது:

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

## 6. Qdrant உள்ளூர் முறையில் வெக்டார்கள் சேமித்தல்

இப்போது நாம் உள்ளமையில் Qdrant சேகரிப்பை உருவாக்கி துண்டுக்களையும் பிணைப்பு மெட்டாடேட்டாவுடனும் இணைக்கிறோம்.

> [!NOTE]
> 2023 பயிற்சியில், நான் LangChain உடன் உள்ளூர் வெக்டார் ஒப்பீட்டு தேடலை காண்பிக்க எளிமையான மற்றும் பிரபலமான வழியாக FAISS பயன்படுத்தினேன். FAISS இன்னும் வேக உள்ளூர் பரிசோதனைகளுக்கு பயனுள்ளது. இந்த 2026 பதிப்பில், நான் Qdrant ஐ பயன்படுத்துகிறேன் ஏனெனெனில் பயிற்சி உற்பத்தி RAG அமைப்பிற்கு அருகிலும் உணருமையானதாக இருக்க வேண்டும் என்பதை விரும்பினேன். Qdrant மூல கோப்பு, பிரிவு தலைப்பு, ஆவண பதிப்பு மற்றும் அனுமதிகள் போன்ற பிணைப்பு மெட்டாடேட்டாவுடன் வெக்டார்கள் சேமிக்க அனுமதிக்கிறது. இது மீட்பை சுலபமாக பரிசோதிக்கவும், வடிகட்டி பிரித்து மேலோட்டக் குறிப்புகள் மற்றும் எதிர்கால நிலையான அல்லது சேவையக அமைப்புக்கான உதவியுடன் உதவுகிறது.

FAISS வெக்டார் ஒப்பீட்டு தேடலை காட்ட சிறந்தது. Qdrant சிறிய ஆனால் உற்பத்தி வடிவமைப்புள்ள RAG மீட்பு அடுக்கை காட்ட சிறந்தது.

சில நடைமுறை மாற்றுகள்:

| வெக்டார் சேமிப்பு / தேடு அடுக்கு | நான் எப்பொழுது பரிசீலிப்பேன் |
| --- | --- |
| Qdrant | உள்ளூர் மாதிரிகள், மெட்டாடேட்டா வடிகட்டல், உற்பத்தி நட்பு வெக்டார் தேடல் மற்றும் எளிமையான Python வேலைப்பாடு. |
| Chroma | வேகமான உள்ளூர் RAG பரிசோதனைகள் மற்றும் எளிமை முக்கியமான குறியீடு புத்தகங்கள். |
| FAISS | வெக்டார் ஒப்பீட்டு தேடு தேவையாக இருந்தால் மற்றும் மெட்டாடேட்டாவை தனித்து நிர்வகிக்க முடிந்தால் இயல்பான உள்ளூர் வைக்டார் தேடல். |
| Milvus | பெரிய அளவுள்ள திறந்த மூல வெக்டார் தேடல் குழு பிரத்தியேக வெக்டார் தரவுத்தளத்தை இயக்க தயாராக இருக்கும்போது. |
| Weaviate | திட்டம், மெட்டாடேட்டா, கலவை தேடல் மற்றும் மேலாண்மை அல்லது சுய-ஹோஸ்ட் அம்சங்களுடன் வெக்டார் தேடல். |
| Azure AI Search | நான் ஒரு தேடல் அடுக்கில் திறவுகோல் தேடல், வெக்டார் தேடல், கலவை மீட்பு, பொருள் வரிசைப்படுத்தல், வடிகட்டல், பாதுகாப்பு, மற்றும் மேலாண்மை ஆப்பரேஷன்களை விரும்பும் போது Azure இல் நிறுவனர் RAG. |
| PostgreSQL + pgvector | ஏற்கனவே PostgreSQL பயன்படுத்தும் குழுக்களுக்கு, பயன்பாட்டு தரவிற்கு அருகில் வெக்டார் தேடலை விரும்பும் போது. |

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

பின்னர் புள்ளிகளைச் சேர்க்கவும்:

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

எனது இயக்கத்தில், சேகரிப்பு 8 வெக்டார்களைச் சேமித்தது.

இதுவே RAG அமைப்பு பரிசோதிக்கத்தக்கதாக ஆரம்பிக்கும் இடம். வெக்டார் தரவுத்தளம் வெக்டார்களை மட்டுமல்லாமல் ஆதார உரையும் மேற்கோள் தருவதற்கு வேண்டிய மெட்டாடேட்டாவையும் சேமிக்கிறது.

## 7. பொறுப்பான துண்டுகளை மீட்பது

இப்போது கேள்வியை கேட்டு பொருத்தமான துண்டுகளை மீட்கின்றோம்.

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

இந்த கட்டத்தில், பதில் உருவாக்குவதற்கு முன்பு மீட்டெடுக்கப்பட்ட துண்டுகளை அச்சிடுகிறேன். இது முக்கியம். மீட்பு தவறு என்றால் பதில் உருவாக்கம் பிரச்சினையை திரைக்குள் மறைக்கும்.

## 8. எளிய மறுவிருத்தி சேர்க்கவும்

முதல் முறையாக மீட்பு பாதையைச் சோதித்த போது வெக்டார் ஒப்பீடு தொடர்புடைய கொள்கை உள்ளடக்கத்தை கண்டுபிடித்தது, ஆனாலும் மிகவும் துல்லியமான பிரிவு முழு மேல் இல்லை.

எனவே நான் ஒரு சிறிய உள்ளூர் மறுவிருத்தியை சேர்த்தேன். கேள்வி வார்த்தைகள் பிரிவு தலைப்பும் உள்ளடக்கமும் பங்குபெறும் போது அது கூடுதல் எடையை அளிக்கிறது.

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

மறுவிருத்திற்குப் பிறகு, சிறந்த முடிவு:

```text
school_ai_policy.md / Final Assignments
```

சோதனை கேள்விக்கான எதிர்பார்க்கப்பட்ட பிரிவு அது.

இது முதலாவது நடைமுறையிலிருந்து மிகவும் பயனுள்ள பாடமாகியது. ஒரு சிறிய உள்ளூர் உதாரணத்திலும், வெக்டார் ஒப்பீடு மற்றொரு அறிகுறியுடன் சேர்க்கப்படும் போது மீட்பு தரம் மேம்பட்டது.

## 9. அடிப்படையான உள்ளூர் பதிலை அமைக்கவும்

இயல்புநிலை பாதைக்காக, நான் LLM அல்லாமல் வெளிச்சமான உள்ளூர் பதில் அமைப்பகரத்தைப் பயன்படுத்துகிறேன்.

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

இது இறுதி தயாரிப்பு பதில் உருவாக்கி அல்ல. இது பிழைதிருத்த உபகரணம். மாதிரி மாறுபாட்டைச் சேர்க்குவதற்கு முன்பு மீட்பு, மெட்டாடேட்டா, மற்றும் மேற்கோள் இணைப்பு வேலை செய்கிறது என்பதை நிரூபிக்கிறது.

## 10. Ollama மற்றும் Phi-4-mini உடன் உள்ளூர் பதிலை உருவாக்குதல்

மீட்பு செயல்படும்போது, குறியீடுபுத்தகம் இறுதியான பதில் படியை மட்டும் Ollama மற்றும் `phi4-mini:3.8b` உடன் மாற்றலாம்.

> [!NOTE]
> Ollama இறுதியான பதில் உருவாக்க படியை மட்டுமே மாற்ற வேண்டும். ஆவண ஏற்ற, துண்டிப்பது, வெக்டார் சேமிப்பு, மீட்பு, மறுவிருத்தம் மற்றும் மேற்கோள் இணைப்பு அனைத்தும் அதே நிலைமை தொடர வேண்டும்.

முதலில், குறியீடுப்புத்தகம் மீட்டெடுத்த துண்டுக்களிலிருந்து ஆதார கேள்விப்பதிவை உருவாக்குகிறது:

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

இந்த பயிற்சிக்காக, நான் Microsoft's Phi-4-mini குடும்பத்தை Ollama ட்ராக் மூலம் உள்ளூர் உருவாக்க விருப்பமாக பரிந்துரைக்கிறேன். Ollama இல் நான்பரிசோதித்த மாதிரி பெயர்:

```powershell
ollama pull phi4-mini:3.8b
```

உதவியாளரை விரைவில் கிடைக்கும் என்று பார்:

```powershell
ollama list
```

பின் இந்த மாறிகளை அமைக்கவும்:

```powershell
Copy-Item .env.example .env
```

`.env` ஐ திறந்து தொடர் 2 Ollama மதிப்புகளை இயக்கவும்:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

குறியீடுபுத்தகம் `python-dotenv` மூலம் களஞ்சியத்தின் மூலத்தில் `.env` ஐ ஏற்றி, அதே ஆதார கேள்விப்பதிவை Ollama உள்ளூர் `/api/chat` முடிவிடம் கொடுக்கிறது, ஒளிப்படவில்லை. Ollama இயங்காவிடில் அல்லது `SERIES2_OLLAMA_MODEL` இல்லை என்றால் இந்த பாதை தவிர்க்கப்படும்.

> [!NOTE]
> இந்த இயந்திரத்தில், `phi4-mini:3.8b` சுமார் 2.49GB மாதிரி கோப்புகளை பதிவிறக்கியது. மூலப்பெறும் பொழுது Ollama 3.3GB நிரப்பப்பட்ட மாதிரி அளவை தெரிவித்து RTX 3060 லேப்டாப் GPU பயன்படுத்தியது.

இதனால் பயிற்சிக்கு இரண்டு நிலைகள் கிடைக்கின்றன:

1. CPU மட்டும் நிர்ணயமான பதில் அமைப்பொருள்.
2. Ollama மற்றும் Phi-4-mini கொண்டு உள்ளூர் பதில் உருவாக்கம்.

இரண்டிலும் மீட்பு குழாய் ஒரே மாதிரிதான்.

## 11. சரிபார்ப்பு முடிவு

நான் குறியீடுபுத்தகத்தை Windows இல் Python 3.12.6 உடன் உள்ளூரில் இயக்கினேன்.

நிறுவப்பட்ட தொகுதிகள்:

| தொகுதி | பதிப்பு |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

குறியீடுபுத்தகம் இயக்கம்:

- குறியீடுபுத்தகம்: `notebooks/series-2-open-source-rag.ipynb`
- இயக்க முடிவு: `nbclient` உடன் வெற்றி
- ஏற்றப்பட்ட ஆவணங்கள்: 2
- உருவாக்கப்பட்ட துண்டுகள்: 8
- Qdrant சேகரிப்பு: `school_policy_local`
- சேர்க்கப்பட்ட வெக்டார்கள்: 8
- ஓட்டுமொத்த மாதிரி: `BAAI/bge-small-en-v1.5`
- ஓட்டுமொத்த அளவு: 384
- மீட்பு கேள்வி: "என் இறுதி பணிக்கான உருவாக்கி AI-யைப் பயன்படுத்தலாமா?"
- மறுவிருத்தி பாதை: எளிதான உள்ளூர் சொல் மறுவிருத்தி
- மறுவிருத்தியபின் உச்சமாக மீட்கப்பட்ட மூல வழி: `school_ai_policy.md`
- மறுவிருத்தியபின் உச்சமாக மீட்கப்பட்ட பிரிவு: `Final Assignments`
- இயல்புநிலை பதில் பாதை: உள்ளூர் வெளிப்படையான பதில் உருவாக்கி
- Ollama உருவாக்குதல் பாதை: `phi4-mini:3.8b` கொண்டு முடிக்கப்பட்டது
- Ollama மாதிரி கோப்பு அளவு: 2.49GB ডিস்கில்
- Ollama ஏற்றப்பட்ட மாதிரி அளவு: `ollama ps` மூலம் 3.3GB அறிக்கை
- GPU வெளியேற்றம்: `ollama ps` மூலம் 100% GPU
- உருவாக்கத்துக்குப் பிறகு கணியப்பட்ட GPU நினைவகம்: RTX 3060 லேப்டாப் GPUல் 6GB இல் சுமார் 3.5GB பயன்படுத்தப்படுகிறது
- FastEmbed மாதிரியுடன் கேச்ச் செய்யப்பட்ட நோட்புக் செயல்பாடு மற்றும் Ollama உருவாக்குதல் இயலுமையாக உள்ளன: சரிபார்ப்பு ஸ்கிரிப்ட்டின் மூலம் சுமார் 34 விநாடிகளில் கடக்கப்பட்டது

Ollama-உறுபடுத்தப்பட்ட பதில்:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

இந்த பதிலை நான் கண்மாயானதாக அழைக்க மாட்டேன். இது சரியான ஆதாரத்திலிருந்து பதில் அளிக்கிறது, ஆனால் இறுதி மூல வரி தீர்மானிப்பான மேற்கோள் வடிவத்தை விட குறைவாக துல்லியமாக உள்ளது. இது பயிற்சி வழிகாட்டலில் காட்ட பயனுள்ளதாக உள்ளது ஏனெனில் இது அடுத்த பொறியியல் கேள்வியை தெளிவாக்குகிறது: பதில் உருவாக்கம் மதிப்பீடு செய்யப்பட வேண்டும், வெறும் மீட்புதான் போதுமானது அல்ல.

நான் சரிபார்த்த போது கற்றுக்கொண்ட முதன்மையான விஷயம் என்னவென்றால் பதில் உருவாக்குவதற்கு முன் மீட்டு தரம் சரிபார்க்கப்பட வேண்டும் என்பதே. எம்பெட்டிங் முடிவு ஏற்கனவே பயனுள்ளதாக இருந்தது, மற்றும் எளிய மறுவிருத்தி எதிர்பார்க்கப்பட்ட கொள்கை பிரிவு முதலில் நம்பகமாக தோன்றச் செய்தது. இதுவே எடுத்துக்காட்டான சிறிய அமைப்பு நடத்தை, எச்சரிக்கை மறைக்காமல் பயிற்சி குறிப்பில் வெளிப்படுத்த விரும்புகிறேன்.

## 12. அடுத்தது என்ன

அடுத்த முன்னேற்றம் இதே பள்ளி கொள்கை உதவியாளரின் பராமரிக்கப்பட்ட Azure பதிப்புடன் உள்ளூர் அமைப்பை ஒப்பிடுவதாகும். காட்சிகரமாக நிலைத்துவைக்கும் போது பரிமாற்றங்கள் சுலபமாக தெரியும்: அமைப்பு சிக்கல், மீட்டு கட்டுப்பாடுகள், அடையாள ஒருங்கிணைப்பு, இயக்க உரிமை மற்றும் செலவு.

## 13. குறிப்பு

- [Qdrant Python கிளையாண்ட் வேகமாய்ச் செயல்படுத்துதல்](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant கிளையாண்ட் GitHub களஞ்சியம்](https://github.com/qdrant/qdrant-client)
- [FastEmbed ஆதரவு செய்யப்பட்ட மாதிரிகள்](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI எம்பெட்டிங்குகள் வழிகாட்டி](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 மாதிரி அட்டை](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 மாதிரி அட்டை](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 மாதிரி அட்டை](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini மாதிரி பக்கம்](https://ollama.com/library/phi4-mini)
- [Ollama விண்டோஸ் ஆவணங்கள்](https://docs.ollama.com/windows)
- [Ollama API ஸ்ட்ரீமிங் ஆவணங்கள்](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct மாதிரி அட்டை](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph கண்ணோட்டம்](https://docs.langchain.com/oss/python/langgraph)
- [RAG அறிமுகம் - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

முந்தையது: [தொடர் 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**மறுப்பு**:
இந்த ஆவணம் AI மொழிபெயர்ப்பு சேவை [Co-op Translator](https://github.com/Azure/co-op-translator) பயன்படுத்தி மொழிபெயர்க்கப்பட்டுள்ளது. நாங்கள் துல்லியத்திற்காக முயற்சி செய்துள்ளோம், ஆனால் தானாக செய்யப்படும் மொழிபெயர்ப்புகளில் பிழைகள் அல்லது தவறுகள் இருக்கலாம் என்பதை கவனத்தில் கொள்ளவும். அசல் ஆவணம் அதன் தாய்மொழியில் அதிகாரப்பூர்வ ஆதாரமாக கருதப்பட வேண்டும். முக்கியமான தகவல்களுக்கு, தொழில்நுட்பமான மனித மொழிபெயர்ப்பு பரிந்துரைக்கப்படுகிறது. இந்த மொழிபெயர்ப்பைப் பயன்படுத்துவதால் ஏற்படும் எந்த தவறான புரிதல்கள் அல்லது தவறான விளக்கத்திற்கும் நாங்கள் பொறுப்பில்வில்லை.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->