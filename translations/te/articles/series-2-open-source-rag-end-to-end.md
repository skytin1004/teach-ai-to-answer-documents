# మీ డాక్యుమెంట్ల ఆధారంగా ప్రశ్నలకు AI ఎలా జవాబు చెప్పాలో నేర్పండి
## సిరీస్ 2: లోకల్ ఓపెన్-సోర్స్ RAG సిస్టమ్‌ను పూర్తిగా నిర్మించండి

![లోకల్ ఓపెన్-సోర్స్ RAG ట్యుటోరియల్ పైప్‌లైన్](../../../assets/images/series-2-local-rag.svg)

> ఈ ఆర్టికల్ సిరీస్ 1 ఆర్కిటెక్చర్ చర్చను రనబుల్ లోకల్ RAG ట్యుటోరియల్‌గా మార్చింది. లక్ష్యం మొదట నమూనా డేటాతో, క్లౌడ్ అకౌంట్ లేదా రహస్యాలు లేకుండా పూర్తి వర్క్‌ఫ్లోను నిర్మించడం, ఆ తరువాత ఆ వర్కింగ్ బేస్‌లైన్ ఉపయోగించి మెరుగైన ఆర్కిటెక్చర్ నిర్ణయాలను తీసుకోవడం.

మనం నిర్మించబోయే సిస్టమ్ ఒక చిన్న స్కూల్ పాలసీ అసిస్టెంట్. నేను రెండు లోకల్ మార్క్డౌన్ డాక్యుమెంట్లను జ్ఞాన ఆధారం గా ఉపయోగించి, అంతా RAG పైప్‌లైన్‌ను క్రమంగా చూచుకుంటాను: ఛంకింగ్, లోకల్ ఎంబెడ్డింగ్‌లు, Qdrant వెక్టర్ స్టోరేజి, రీట్రీవల్, రీరేంకింగ్, మూలంతో జాగ్రత్తగా జవాబు తయారీ, మరియు ఐచ్ఛిక లోకల్ జనరేషన్ Ollama మరియు Phi-4-mini తో.

సిరీస్ నావిగేషన్: [రిపాజిటరీ హోమ్](../README.md) | ముందు: [సిరీస్ 1 - RAG, Azure vs ఓపెన్-సోర్స్ ప్రత్యామ్నాయాలు, మరియు ఫైన్-ట్యూనింగ్ అవసరం అయ్యే సందర్భాలు](./series-1-rag-azure-open-source-fine-tuning.md)

నోట్‌బుక్: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | అవసరాలు: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> క్లౌడ్ వనరులు సృష్టించే ముందు RAG పైప్‌లైన్‌ను అర్థం చేసుకోవాలనుకునే వారికి ఇది ఉత్తమ ప్రారంభ పాయింట్. డిఫాల్ట్ మార్గం లోకల్‌లో CPU-ఫ్రెండ్లీ ఎంబెడ్డింగ్‌లతో మరియు రహస్యాలు లేకుండా నడుస్తుంది.

## 1. మనం ఏమి నిర్మిస్తున్నాము

2023 ట్యుటోరియల్‌లో, నేను Azure నుండి ప్రారంభించాను, ఎందుకంటే Azure AI Search మరియు Azure OpenAI PDF డాక్యుమెంట్ల నుండి ప్రశ్నలకు జవాబు చెప్పడం ఎలా ఉందో చూపించడానికి ఉద్దేశించబడింది.

ఈ 2026 సిరీస్ కోసం, నేను ఒక లేయర్ కింద ప్రారంభించాలనుకుంటున్నాను.

మేనేజ్డ్ సర్వీసెస్ ఉపయోగించే ముందు, చిన్న RAG సిస్టమ్‌ను లోకల్‌గా నిర్మించి, ప్రతి దశను స్పష్టంగా చూడాలని ఉంది: డాక్యుమెంట్లు లోడ్ చేయడం, టెక్స్ట్‌ను ఛంకింగ్ చేయడం, వెక్టర్లు నిల్వ చేయడం, సాక్ష్యాన్ని రీట్రీవ్ చేయడం, రీరేంక్ చేయడం, మూలాలతో జాగ్రత్తగా జవాబు తయారీ.

ఉదాహరణ సందర్భం ఒక స్కూల్ పాలసీ అసిస్టెంట్. ఉపయోగకర్త అడగాలి:

```text
Can I use generative AI for my final assignment?
```

సిస్టమ్ సాధారణ మోడల్ మెమరీ నుండి జవాబు ఇవ్వకూడదు. సంబంధిత పాలసీ సెక్షన్‌ను రీట్రీవ్ చేసి, ఆ సాక్ష్యంతోనే జవాబు చెప్పాలి.

పూర్తి రనబుల్ వెర్షన్ [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) లో ఉంది. క్రింది కోడ్ ప్రధాన దశలను చూపిస్తుంది కాబట్టి ఆర్టికల్ ను ట్యుటోరియల్ లాగా చదవవచ్చు.

## 2. లోకల్ డిపెండెన్సీలు ఇన్‌స్టాల్ చేయండి

వర్చువల్ ఎన్విరాన్‌మెంట్ సృష్టించి సిరీస్ 2 అవసరాలను ఇన్‌స్టాల్ చేయండి:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

మొదటి వెర్షన్ Qdrant లోకల్ మోడ్ మరియు FastEmbed ఉపయోగిస్తుంది. Qdrant యొక్క Python క్లయింట్ `QdrantClient(":memory:")` తో ఇన్-మెమరీ లోకల్ మోడ్‌ను మద్దతు ఇస్తుంది, ఇది లోకల్ ట్యుటోరియల్స్ మరియు CI-స్టైల్ వెరిఫికేషన్‌కు ఉపయోగకరం. FastEmbed మాకు క్లౌడ్ API కీ అవసరం లేకుండా నిజమైన లోకల్ ఎంబెడ్డింగ్ మోడల్ ఇస్తుంది.

అవసరాల ఫైల్‌లో `python-dotenv` కూడా ఉంటాయి, ఎందుకంటే నోట్‌బుక్ ఐచ్ఛికంగా Ollama మోడల్ పేరు `.env` నుండి చదవవచ్చు. ఈ లోకల్ ట్యుటోరియల్‌కు Azure OpenAI లేదా OpenAI API కీ అవసరం లేదు.

## 3. నమూనా డాక్యుమెంట్లు లోడ్ చేయండి

నమూనా కార్పస్ ఉద్దేశపూర్వకంగా చిన్నదిగా ఉంది:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

నోట్‌బుక్‌లో, నేను `sample_data/` నుండి అన్ని మార్క్డౌన్ ఫైళ్లను లోడ్ చేస్తాను:

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

నేను నోట్‌బుక్ నడిపినప్పుడు, 2 డాక్యుమెంట్లు లోడ్ అయ్యాయి. అది స్వయంగా తనిఖీ చేసుకోవడానికి చిన్నది, ఇది RAG పైప్‌లైన్ మొదటి వెర్షన్ నిర్మాణంలో ఉపయోగకరం.

## 4. మార్క్డౌన్ హెడ్డింగ్‌ల ద్వారా ఛంక్ చేయడం

తదుపరి దశ డాక్యుమెంట్లను ఛంక్‌లుగా విభజించడం.

ఈ ట్యుటోరియల్ కోసం, మార్క్డౌన్ హెడ్డింగ్‌లను నిర్మాణ సంకేతంగా ఉపయోగిస్తాను. డాక్యుమెంట్ శీర్షిక `#` నుండి వస్తుంది, ప్రతి సెక్షన్ ఛంక్ `##` నుండి వస్తుంది.

> [!NOTE]
> ఛంకింగ్ ఒకే విధంగా సరిపడదు. ఈ ట్యుటోరియల్‌లో, నమూనా డాక్యుమెంట్లకు స్పష్టమైన `#` మరియు `##` నిర్మాణం ఉన్నందున మార్క్డౌన్ హెడ్డింగ్‌లను ఉపయోగించాను. PDFలు, వర్డ్ డాక్యుమెంట్లు, స్లయిడ్లు, టిక్కెట్లు లేదా వెబ్ పేజీల కోసం, మెరుగైన వ్యూహం పేజీ సరిహద్దులు, లేఅవుట్ సమాచారం, సెమాంటిక్ సెక్షన్లు, టోకెన్ పరిమితులు, పట్టికలు లేదా మెటాడేటాను ఉపయోగించవచ్చు. ముఖ్యమైన విషయం మీరు మీ డాక్యుమెంట్ల అర్థం మరియు మూల ట్రేసబిలిటీని సంరక్షించే ఛంకింగ్ వ్యూహాన్ని ఎంచుకోవడం.

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

తరువాత ప్రతీ డాక్యుమెంట్‌కు దాన్ని వర్తింపజేస్తాను:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

నా లోకల్ రన్‌లో ఇది 8 ఛంక్‌లను సృష్టించింది.

ఈ దశలో నాకు ఇష్టం కలిగింది అంటే మెటాడేటా ఇప్పటికే ఉపయోగకరంగా ఉంది. ప్రతి ఛంక్ దాని `source`, `sectionHeading`, `documentVersion`, మరియు ప్లేస్ హోల్డర్ `permissions` ను తెలుసుకుంటుంది. చిన్న ట్యుటోరియల్ లో కూడా ఇది ఉటంకనలను, తరువాత అనుమతితో కూడిన రీట్రీవల్‌ను సులభతరం చేస్తుంది.

## 5. లోకల్ ఎంబెడ్డింగ్‌లు సృష్టించండి

మొదటి పబ్లిక్ వెర్షన్ కోసం, నేను FastEmbed ద్వారా `BAAI/bge-small-en-v1.5` ఉపయోగిస్తున్నాను.

ఇది ట్యుటోరియల్‌ను లోకల్ మరియు CPU-సౌమ్యంగా ఉంచుతుంది, కానీ ఇది ప్లేస్‌హోల్డర్ వెక్టర్ ఫంక్షన్ కాకుండా నిజమైన ఎంబెడ్డింగ్ మోడల్ ఉపయోగిస్తుంది. మొదటి రన్ మోడల్ వెయిట్స్ డౌన్లోడ్ చేస్తుంది. ఆ తరువాత, నోట్‌బుక్ లోకల్ క్యాష్‌ను తిరిగి ఉపయోగించవచ్చు.

> [!NOTE]
> నేను `BAAI/bge-small-en-v1.5` ఉపయోగిస్తాను ఎందుకంటే ఇది FastEmbed మరియు Qdrant తో చక్కగా పనిచేసే తేలికపాటి ఇంగ్లిష్ ఎంబెడ్డింగ్ మోడల్. ఇది 384-డైమెన్షన్ వెక్టర్‌లు సృష్టిస్తుంది, ఇది ఉదాహరణను లోకల్లో వేగంగా మరియు తక్కువ ఖర్చుతో నడిపేందుకు సహకరిస్తుంది. ఇది ఏకైక ఉత్తమ ఎంపిక కాదు. 2023లో, చాలా ట్యుటోరియల్స్ `text-embedding-ada-002` వంటి హోస్టెడ్ ఎంబెడ్డింగ్ మోడళ్లను ఉపయోగించాయి. ఇప్పుడు కొత్త హోస్టెడ్ ఎంపికలు `text-embedding-3-small` మరియు `text-embedding-3-large` (OpenAI), మరియు ఓపెన్-సోర్స్ ఎంపికలు BGE, E5, MiniLM, Nomic Embed, మరియు బహుభాషా మోడళ్లైన `BAAI/bge-m3` ఉన్నాయి, ఇవి వర్క్‌లోడ్‌ను బట్టి బాగుంటాయి. ఉత్పత్తిలో సరైన ఎంబెడ్డింగ్ మోడల్‌ను మీ డాక్యుమెంట్లపై రీట్రీవల్ మద్దతు ద్వారా ఎంపిక చేయాలి.

కొన్ని ప్రాక్టికల్ ప్రత్యామ్నాయాలు:

| మోడల్ ఫ్యామిలీ | నేను దాన్ని ఎప్పుడయినా పరిగణిస్తాను |
| --- | --- |
| `text-embedding-ada-002` | 2023 కాలంలో ఉన్న పాత హోస్టెడ్ బేస్లైన్, నేను నేటి కొత్త ట్యుటోరియల్‌కి డిఫాల్ట్ గా ఈ మోడల్ ఎంచుకోను. |
| `text-embedding-3-small` | బలమైన ఖర్చు/ప్రదర్శన Santulan కోసం ఆధునిక హోస్టెడ్ డిఫాల్ట్, లోకల్ మాత్రమె ఎంబెడ్డింగ్‌లు అవసరం లేకపోతే. |
| `text-embedding-3-large` | వెక్టర్ పరిమాణం లేదా ఎంబెడ్డింగ్ ఖర్చు కంటే రీట్రీవల్ నాణ్యత ముఖ్యం అయినప్పుడు హోస్టెడ్ ఎంపిక. |
| `BAAI/bge-small-en-v1.5` | ట్యుటోరియల్స్, ప్రోటోటైప్స్, CPU-సౌమ్య ప్రయోగాల కోసం తేలికపాటి లోకల్ ఇంగ్లీష్ బేస్లైన్. |
| `BAAI/bge-base-en-v1.5` లేదా `BAAI/bge-large-en-v1.5` | మెరుగైన రీట్రీవల్ నాణ్యత కోసం పెద్ద లోకల్ ఇంగ్లీష్ మోడళ్లను ఇష్టపడినప్పుడు. |
| `BAAI/bge-m3` | బహుభాషా లేదా పొడవైన సందర్భ రీట్రీవల్ కోసం, ప్రత్యేకంగా డాక్యుమెంట్లు కేవలం ఇంగ్లీష్ కాకపోతే. |
| `sentence-transformers/all-MiniLM-L6-v2` | చాలా చిన్న మరియు వేగవంతమైన సెమాంటిక్ సెర్చ్ బేస్లైన్. వేగం మరియు సరళత ముఖ్యం అయినప్పుడు ఉపయోగకరం. |
| `nomic-embed-text-v1.5` | పొడవైన సందర్భ లేదా పోర్టబిలిటీ ఫోకస్ చేయబడిన సెట్టప్‌ల కోసం పరీక్షించదగ్గ ఓపెన్ లోకల్ ఎంబెడ్డింగ్ ఎంపిక. |

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

తరువాత ప్రతీ ఛంక్‌కు ఒక ఎంబెడ్డింగ్ వస్తుంది:

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

## 6. Qdrant లోకల్ మోడ్‌లో వెక్టర్లు నిల్వ చేయండి

ఇప్పుడ हम ఇన్-మెమరీ Qdrant సేకరణను సృష్టించి ఛంక్‌లను పేమెంట్ మెటాడేటా తో చేర్స్తాము.

> [!NOTE]
> 2023 ట్యుటోరియల్‌లో, నేను FAISS ఉపయోగించాను ఎందుకంటే అది LangChain తో లోకల్ వెక్టర్ సమానత్వ సెర్చ్‌ను సులభంగా మరియు ప్రజాదరణ పొందిన విధంగా చూపించగలదు. FAISS ఇంకా వేగవంతమైన లోకల్ ప్రయోగాల కోసం ఉపయోగపడుతుంది. ఈ 2026 వెర్షన్‌లో, నేను Qdrant ఉపయోగిస్తున్నాను ఎందుకంటే ట్యుటోరియల్ ఉత్పత్తి RAG సిస్టమ్‌కు సమీపంగా ఉంటుందని అనిపించాలి. Qdrant వెక్టర్‌లను మూల డాక్యుమెంట్, సెక్షన్ హెడ్డింగ్, డాక్యుమెంట్ వెర్షన్ మరియు అనుమతులు వంటి పేమెంట్ మెటాడేటా తోనూ నిల్వ చేస్తుంది. ఇది రీట్రీవల్‌ను సులభతరం చేస్తుంది మరియు ఫిల్టరింగ్, ఉటంకనలు, భవిష్యత్ సర్వర్-ఆధారిత లేదా స్థిరీకృత ఆపరేషన్‌ల కోసం ఉదాహరణను సన్నద్ధం చేస్తుంది.

FAISS వెక్టర్ సమానత్వ సెర్చ్ చూపించడానికి గొప్పది. Qdrant చిన్న కానీ ఉత్పత్తి ఆకృతికి సంబంధించిన RAG రీట్రీవల్ లేయర్ చూపించడంలో మెరుగైనది.

కొంత عملي ప్రత్యామ్నాయాలు:

| వెక్టర్ స్టోర్ / శోధన లేయర్ | నేను ఎప్పుడు పరిగణిస్తాను |
| --- | --- |
| Qdrant | లోకల్ ప్రోటోటైప్స్, మెటాడేటా ఫిల్టరింగ్, ఉత్పత్తి-ఫ్రెండ్లీ వెక్టర్ శోధన, సరళ Python వర్క్‌ఫ్లో కోసం. |
| Chroma | వేగవంతమైన లోకల్ RAG ప్రయోగాలు మరియు సాదాసీదా నోట్‌బుక్స్ కోసం. |
| FAISS | సమానత్వ శోధన మాత్రమే అవసరమైనప్పుడు, మెటాడేటాను వేరుగా నిర్వహించవచ్చు, తేలికపాటి లోకల్ వెక్టర్ శోధనకు. |
| Milvus | పెద్ద స్థాయి ఓపెన్-సోర్స్ వెక్టర్ శోధన, టీమ్ ప్రత్యేక వెక్టర్ డేటాబేస్‌ను నిర్వహించేందుకు సిద్ధంగా ఉన్నప్పుడు. |
| Weaviate | స్కీమా, మెటాడేటా, హైబ్రిడ్ శోధన మరియు మేనేజ్ చేయబడిన లేదా స్వయం-హోస్ట్ చేసిన ఆప్షన్‌లతో వెక్టర్ శోధన. |
| Azure AI Search | Azureలో ఎంటర్‌ప్రైజ్ RAG కోసం, సంకేత పద శోధన, వెక్టర్ శోధన, హైబ్రిడ్ రీట్రీవల్, సెమాంటిక్ ర్యాంకింగ్, ఫిల్టరింగ్, సెక్యూరిటీ, మరియు ఒకే శోధన లేయర్‌లో మేనేజ్‌డ్ ఆపరేషన్స్ కావాలనుకుంటే. |
| PostgreSQL + pgvector | ఇప్పటికే PostgreSQL ఉపయోగిస్తున్న టీమ్‌లు, అప్లికేషన్ డేటాతో సమీపంగా వెక్టర్ శోధన కోరుకునేటప్పుడు. |

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

తరువాత పాయింట్లను చేర్చండి:

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

నా రన్‌లో, సేకరణ 8 వెక్టర్లు చేర్చింది.

ఇక్కడ RAG సిస్టమ్ పరిశీలించదగినదిగా మారటం మొదలవుతుంది. వెక్టర్ డేటాబేస్ కేవలం వెక్టర్‌లను నిల్వ చేయడం కాకుండా, సాక్ష్యపు టెక్స్టును మరియు ఉటంకనలు కోసం అవసరమైన మెటాడేటాను నిల్వ చేస్తుంది.

## 7. అభ్యర్థిత ఛంక్‌లను రీట్రీవ్ చేయండి

ఇప్పుడు ప్రశ్న అడిగి అభ్యర్థిత ఛంక్‌లను రీట్రీవ్ చేయండి.

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

ఈ దశలో, నేను జవాబు తయారుచేయక ముందే రీట్రీవ్ చేసిన ఛంక్‌లను ప్రింట్ చేస్తాను. ఇది ముఖ్యం. రీట్రీవల్ తప్పు అయితే, జనరేషన్ దాని సమస్యను ప్రయత్నశీలమైన టెక్స్ట్ వెనుక దాచుతుంది.

## 8. సులభమైన రీరేంకర్ జోడించడం

నేను మొదట రీట్రీవల్ మార్గం ప్రయోగించినప్పుడు, వెక్టర్ సమానత్వం సంబంధిత పాలసీ కంటెంట్ కనుగొంది, కానీ అత్యంత ఖచ్చితమైన సెక్షన్ ఎప్పుడు కూడా టాప్లో ఉండేది కాదు.

కాబట్టి నేను ఒక చిన్న లోకల్ రీరేంకర్ జోడించాను. ప్రశ్న పదాలు సెక్షన్ హెడ్డింగ్ మరియు కంటెంట్ తో సామాన్యంగా ఉంటే అదనపు బరువు ఇస్తుంది.

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

రీరేంకింగ్ తర్వాత టాప్ ఫలితం:

```text
school_ai_policy.md / Final Assignments
```

అది పరీక్షకు అనుగుణమైన సెక్షన్.

ఇది మొదటి అమలీకరణ నుండి అత్యంత ఉపయోగకర పాఠం. తక్కువ లోకల్ ఉదాహరణలో కూడా, వెక్టర్ సమానత్వం మరియు మరో సంకేతంతో కలిపినపుడు రీట్రీవల్ నాణ్యత మెరుగైంది.

## 9. స్థిరమైన లోకల్ జవాబు తయారు చేయండి

డిఫాల్ట్ మార్గానికి, నేను LLM కాకుండా పారదర్శక లోకల్ జవాబు కంపోజర్ ఉపయోగిస్తున్నాను.

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

ఇది తుది ఉత్పత్తి జవాబు జనరేటర్ కాదని గుర్తుంచుకోండి. ఇది డీబగ్గింగ్ సాధనం. మోడల్ వైవిధ్యాన్ని చేర్చేముందు రీట్రీవల్, మెటాడేటా, మరియు ఉటాంకి వైర్ చేస్తుందనే ధృవీకరణ.

## 10. Ollama మరియు Phi-4-mini తో లోకల్ జవాబు తయారు చేయండి

రీట్రీవల్ పనిచేస్తున్న తర్వాత, నోట్‌బుక్ కేవలం చివరి జవాబు దశను Ollama మరియు `phi4-mini:3.8b` తో ప్రత్యామ్నయం చేయవచ్చు.

> [!NOTE]
> Ollama కేవలం చివరి జవాబు-తయారీ దశను మార్చాలి. డాక్యుమెంట్ లోడింగ్, ఛంకింగ్, వెక్టర్ నిల్వ, రీట్రీవల్, రీరేంకింగ్, మరియు ఉటాంకి వైర్ అవలె సెటప్ అలాగే ఉండాలి.

మొదటగా, నోట్‌బుక్ రీట్రీవ్ అయిన ఛంక్‌ల నుండి సాక్ష్య ప్రాంప్ట్‌ను సృష్టిస్తుంది:

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

ఈ ట్యుటోరియల్‌కి, నేను Microsoft యొక్క Phi-4-mini ఫ్యామిలీని Ollama ద్వారా డిఫాల్ట్ లోకల్ జనరేషన్ ఆప్షన్‌గా సిఫార్సు చేస్తున్నాను. Ollamaలో నేను పరీక్షించిన మోడల్ పేరు:

```powershell
ollama pull phi4-mini:3.8b
```

మీరు మోడల్ అందుబాటులో ఉందో వేగంగా తనిఖీ చేయవచ్చు:

```powershell
ollama list
```

తరువాత ఈ వేరియబుల్స్ సెట్ చేయండి:

```powershell
Copy-Item .env.example .env
```

`.env` ఓపెన్ చేసి సిరీస్ 2 Ollama విలువలను అన్‌కమెంట్ చేయండి:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

నోట్‌బుక్ ریپازیٹరీ రూట్ నుండి `python-dotenv`తో `.env` ను లోడ్ చేస్తుంది, ఆపై Ollama యొక్క లోకల్ `/api/chat` ఎండ్‌పాయింట్‌కి అదే సాక్ష్య ప్రాంప్ట్ ని స్ట్రీమింగ్ లేకుండా పంపుతుంది. Ollama నడవకపోతే లేదా `SERIES2_OLLAMA_MODEL` లభ్యంకాలేదు అయితే, ఈ ట్రాక్ పాసు చేయబడుతుంది.

> [!NOTE]
> ఈ మెషీన్‌పై, `phi4-mini:3.8b` సుమారు 2.49GB మోడల్ ఫైళ్లను డౌన్లోడ్ చేసుకుంది. ఇన్ఫరెన్స్ సమయంలో, Ollama 3.3GB లోడ్ అయిన మోడల్ పరిమాణాన్ని తెలిపింది మరియు RTX 3060 ల్యాప్‌టాప్ GPU ఉపయోగించింది.

ఇది ట్యుటోరియల్‌కు రెండు స్థాయిలను ఇస్తుంది:

1. CPU-మాత్రమైన నిర్దిష్ట జవాబు కంపోజర్.
2. Ollama మరియు Phi-4-mini తో లోకల్ జవాబు తయారీ.

రీట్రీవల్ పైప్‌లైన్ రెండింటిలో ఒకటే ఉంటుంది.

## 11. ధృవీకరణ ఫలితం

నేను Windowsపై Python 3.12.6తో లొకల్‌గా నోట్‌బుక్ నడిపాను.

ఇన్‌స్టాల్ చేయబడిన ప్యాకేజీలు:

| ప్యాకేజీ | వెర్షన్ |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

నోట్‌బుక్ అమలు:

- నోట్‌బుక్: `notebooks/series-2-open-source-rag.ipynb`
- అమల ఫలితం: `nbclient`తో పాసయింది
- లోడ్ చేసిన డాక్యుమెంట్లు: 2
- రూపొందించిన ఛంక్‌లు: 8
- Qdrant సేకరణ: `school_policy_local`
- చొప్పించిన వెక్టర్లు: 8
- ఎంబెడ్డింగ్ మోడల్: `BAAI/bge-small-en-v1.5`
- ఎంబెడ్డింగ్ పరిమాణం: 384
- రిట్రీవల్ ప్రశ్న: "నా తుది అసైన్‌మెంట్ కోసం నేను జనరేటివ్ AI ఉపయోగించవచ్చా?"
- రీరాంకింగ్ పాథ్: లైట్వెయిట్ లోకల్ లెక్సికల్ రీరాంకింగ్
- రీరాంకింగ్ తర్వాత టాప్ రిట్రీవ్ అయిన మూలం: `school_ai_policy.md`
- రీరాంకింగ్ తర్వాత టాప్ రిట్రీవ్ అయిన విభాగం: `Final Assignments`
- డిఫాల్ట్ ఆన్‌సర్ పాథ్: లోకల్ ట్రాన్స్పరెంట్ ఆన్‌సర్ కంపోజర్
- ఒల్లామా నిర్మాణ పాథ్: `phi4-mini:3.8b` తో పూర్తి
- ఒల్లామా మోడల్ ఫైల్ పరిమాణం: డిస్క్‌పై 2.49GB
- ఒల్లామా లోడ్ చేసిన మోడల్ పరిమాణం: `ollama ps` ప్రకారం 3.3GB
- GPU ఆఫ్‌లోడ్: 100% GPU `ollama ps` ప్రకారం
- జనరేషన్ తర్వాత GPU జ్ఞాపకం: RTX 3060 ల్యాప్‌టాప్ GPUపై 6GBలో సుమారు 3.5GB వాడబడింది
- కాచ్డ్ ఫాస్ట్‌ఎంబెడ్ మోడల్ మరియు ఒల్లామా జనరేషన్ ఉపయోగించి నోట‌బుక్ ఎగ్జిక్యూషన్: వెరిఫికేషన్ స్క్రిప్ట్ ద్వారా సుమారు 34 సెకన్లలో పూర్తైంది

ఒల్లామా-ఉత్పత్తి ఇవ్వబడిన సమాధానం:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

నేను ఈ సమాధానాన్ని పర్ఫెక్ట్ అనవచ్చు. ఇది సరైన సాక్ష్యం నుంచి సమాధానం ఇస్తుంది, కానీ తుది మూలం లైన్ డిటర్మినిస్టిక్ సిటేషన్ ఫార్మాట్ కంటే తక్కువ ఖచ్చితంగా ఉంది. ఈ ట్యుటోరియల్‌లో దీన్ని చూపించడం ఉపయోగకరం ఎందుకంటే తదుపరి ఇంజినీరింగ్ ప్రశ్న స్పష్టమవుతుంది: సమాధానం ఉత్పత్తి కూడా మూల్యాంకనం అవసరం, కేవలం రిట్రీవల్ మాత్రమే కాదు.

ఇందులో నేను వెరిఫై చేసినప్పుడు ప్రధానంగా నేర్చుకున్నది ఏమిటంటే సమాధానం ఉత్పత్తికి ముందు రిట్రీవల్ నాణ్యతను తనిఖీ చేయాలి. ఎంబెడ్డింగ్ ఫలితం ఇప్పటికే ఉపయోగకరంగా ఉంది, మరియు లైట్వెయిట్ రీరాంకర్ ఆశించిన పాలసీ సెక్షన్‌ను విశ్వసనీయంగా మొట్టమొదట చూపించాడు. ఇది పక్కాగా చెప్పాలంటే, ఇది ట్యుటోరియల్ లో మలిచిపెట్టకుండా ప్రదర్శించదలచిన చిన్న సిస్టం ప్రవర్తన.

## 12. తదుపరి దశలు

తదుపరి మెరుగుదల ఇది: ఉచ్చితమైన స్కూల్ పాలసీ అసిస్టెంట్ సన్నివేశానికి అనుసరించి ఈ లోకల్ సెటప్‌ను మేనేజ్డ్ Azure వెర్షన్‌తో సరిపోల్చడం. సన్నివేశాన్ని స్థిరంగా ఉంచడం వల్ల వాణిజ్యాలు సులభంగా అర్థమవుతాయి: సెటప్ సంక్లిష్టత, రిట్రీవల్ నియంత్రణలు, ఐడెంటిటీ ఇంటిగ్రేషన్, నిర్వహణ స్వాధీనం, మరియు వ్యయం.

## 13. సూచనలు

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

మునుపటి: [సిరీస్ 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్వీకరణ**:
ఈ పత్రం AI అనువాద సేవ [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నిస్తున్నప్పటికీ, ఆటోమేటెడ్ అనువాదాలు తప్పులు లేదా అసమగ్రతలను కలిగి ఉండవచ్చు. దాని స్వదేశ భాషలో ఉన్న అసలు పత్రాన్ని అధికారం కలిగిన మూలంగా పరిగణించాలి. కీలకమైన సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదాన్ని సిఫారసు చేస్తాము. ఈ అనువాదం ఉపయోగం వల్ల కలిగే ఏవైనా అపార్థాలు లేదా తప్పుదారులు కోసం మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->