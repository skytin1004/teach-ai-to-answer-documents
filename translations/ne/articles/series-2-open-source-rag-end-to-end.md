# तपाईँको कागजातहरूमा आधारित प्रश्नहरू उत्तर दिन AI सिखाउनुहोस्
## सिरिज २: स्थानीय खुला-स्रोत RAG प्रणाली अन्तदेखि अन्त्यसम्म बनाउनुहोस्

![स्थानीय खुला-स्रोत RAG ट्युटोरियल पाइपलाइन](../../../assets/images/series-2-local-rag.svg)

> यो लेख सिरिज १ को वास्तुकला छलफललाई चलाउन सकिने स्थानीय RAG ट्युटोरियलमा परिणत गर्दछ। उद्देश्य पहिलोमा नमूना डाटा सहित पूर्ण वर्कफ्लो निर्माण गर्नु हो, कुनै क्लाउड खाता वा गोप्य जानकारी बिना, त्यसपछि त्यो कार्यरत आधारलाई प्रयोग गरेर पछि अझ राम्रो वास्तुकला निर्णयहरू लिनु।

हामी बनाउने प्रणाली सानो विद्यालय नीति सहायक हो। म दुई स्थानीय Markdown कागजातहरूलाई ज्ञान भण्डारको रूपमा प्रयोग गर्छु, त्यसपछि पूरा RAG पाइपलाइन: खण्ड विभाजन, स्थानीय एम्बेडिङ्स, Qdrant भेक्टर भण्डारण, पुनःप्राप्ति, पुनःक्रमण, स्रोत-जानकारी उत्तर सँगठन, र वैकल्पिक स्थानीय उत्पादन Ollama र Phi-4-mini सँग प्रदर्शन गर्दछु।

सिरिज नेभिगेसन: [रिपोजिटरी होम](../README.md) | अघिल्लो: [सिरिज १ - RAG, Azure बनाम खुला-स्रोत विकल्पहरू, र कहिले फाइन-ट्यूनिङ उपयुक्त हुन्छ](./series-1-rag-azure-open-source-fine-tuning.md)

नोटबुक: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | आवश्यकताहरू: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> यदि तपाईँ क्लाउड स्रोतहरू सिर्जना गर्नु अघि RAG पाइपलाइन बुझ्न चाहनुहुन्छ भने यो सबैभन्दा राम्रो सुरुवात बिन्दु हो। डिफल्ट मार्ग स्थानीय रूपमा CPU-अनुकूल एम्बेडिङ्स र कुनै गोप्य जानकारी बिना चल्छ।

## १. के निर्माण गर्दैछौं

२०२३ को ट्युटोरियलमा, मैले Azure बाट शुरू गरें किनभने उद्देश्य Azure AI Search र Azure OpenAI बाट PDF कागजातहरूबाट प्रश्नहरूको जवाफ कसरी दिन सकिन्छ देखाउनु थियो।

यो २०२६ सिरिजका लागि, म एक तह तलबाट सुरु गर्न चाहन्छु।

प्रबन्धित सेवा उपयोग गर्नु अघि, म स्थानीय रूपमा सानो RAG प्रणाली बनाउनु र प्रत्येक चरणलाई देखाउन चाहन्छु: कागजात लोड गर्नु, पाठ खण्ड विभाजन, भेक्टर भण्डारण, प्रमाण पुनःप्राप्ति, पुनःक्रमण, र स्रोत-जानकारी उत्तर फिर्ता गर्नु।

नমूना परिदृश्य स्कूल नीति सहायक हो। प्रयोगकर्ताले सोध्छ:

```text
Can I use generative AI for my final assignment?
```
  
प्रणालीले सामान्य मोडेल स्मरणबाट उत्तर दिनु हुँदैन। यसले सान्दर्भिक नीति खण्डलाई पुनःप्राप्त गर्नुपर्छ र त्यस प्रमाणबाट उत्तरदिनुपर्छ।

पूर्ण चल्ने संस्करण [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) मा छ। तलको कोड मुख्य चरणहरू देखाउँछ जसले लेखलाई ट्युटोरियलको रूपमा पढ्न योग्य बनाउँछ।

## २. स्थानीय निर्भरताहरू स्थापना गर्नुहोस्

भर्चुअल वातावरण सिर्जना गरी सिरिज २ का आवश्यकताहरू स्थापना गर्नुहोस्:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```
  
पहिलो संस्करण Qdrant स्थानीय मोड र FastEmbed प्रयोग गर्छ। Qdrant को Python क्लाइन्ट `QdrantClient(":memory:")` प्रयोग गर्दै इन-मेमोरी स्थानीय मोड समर्थन गर्छ, जुन स्थानीय ट्युटोरियलहरू र CI-शैलीको प्रमाणीकरणका लागि उपयोगी छ। FastEmbed ले हामीलाई एक वास्तविक स्थानीय एम्बेडिङ मोडेल दिन्छ क्लाउड API कुञ्जी आवश्यक नपर्ने।

आवश्यकताहरू फाइलमा `python-dotenv` पनि समावेश छ किनकि नोटबुकले वैकल्पिक रूपमा `.env` बाट Ollama मोडेल नाम पढ्न सक्छ। यो स्थानीय ट्युटोरियलका लागि Azure OpenAI वा OpenAI API कुञ्जी आवश्यक छैन।

## ३. नमूना कागजातहरू लोड गर्नुहोस्

नमूना सङ्ग्रह जानाजानी सानो छ:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)  
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

नोटबुकमा, मैले `sample_data/` बाट सबै Markdown फाइलहरू लोड गर्छु:

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
  
जब मैले नोटबुक चलाएँ, यसले २ कागजातहरू लोड गर्यो। त्यो म्यानुअली जाँच्न पर्याप्त सानो हो, जुन पहिलो RAG पाइपलाइन संस्करण निर्माण गर्दा उपयोगी छ।

## ४. Markdown शीर्षक अनुसार खण्ड विभाजन गर्नुहोस्

अर्को चरण कागजातहरूलाई खण्डमा विभाजन गर्नु हो।

यस ट्युटोरियलका लागि, मैले संरचना संकेतको रूपमा Markdown शीर्षक प्रयोग गरेको छु। कागजात शीर्षक `#` बाट आउँछ, र प्रत्येक खण्ड `##` बाट।

> [!NOTE]  
> खण्ड विभाजन सबैमा समान हुँदैन। यस ट्युटोरियलमा मैले Markdown शीर्षकहरू प्रयोग गरेको छु किनकि नमूना कागजातहरूमा स्पष्ट `#` र `##` संरचना छ। PDF, Word कागजात, स्लाइड, टिकट, वा वेब पृष्ठहरूका लागि पृष्ठ सीमाहरू, लेआउट जानकारी, सिमान्तिक खण्डहरू, टोकन सिमाना, तालिका, वा मेटाडाटा जस्ता स्त्रोत प्रयोग गर्ने उत्तम रणनीति हुन सक्छ। महत्वपूर्ण कुरा भनेको तपाईँको कागजातका लागि अर्थ र स्रोत ट्रेसयोग्यतालाई सुरक्षित राख्ने खण्ड विभाजन रणनीति छनोट गर्नु हो।

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
  
पछि यसलाई प्रत्येक कागजातमा लागू गर्नुहोस्:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```
  
मेरो स्थानीय चलाए अनुसार यसले ८ खण्डहरू निर्माण गर्यो।

यो चरणमा मलाई मन परेको कुरा भनेको मेटाडाटा पहिले नै उपयोगी हुनु हो। प्रत्येक खण्डले आफ्नो `source`, `sectionHeading`, `documentVersion`, र प्लेसहोल्डर `permissions` थाहा हुन्छ। सानो ट्युटोरियलमा पनि, यसले उद्धरण र पछि अनुमति-आधारित पुनःप्राप्तिलाई बुझ्न सजिलो बनाउँछ।

## ५. स्थानीय एम्बेडिङ्स सिर्जना गर्नुहोस्

पहिलो सार्वजनिक संस्करणका लागि, मैले FastEmbed मार्फत `BAAI/bge-small-en-v1.5` प्रयोग गरेको छु।

यसले ट्युटोरियललाई स्थानीय र CPU-अनुकूल राख्छ, तर यो अझै वास्तविक एम्बेडिङ मोडेल प्रयोग गर्छ प्लेसहोल्डर भेक्टर फङ्सनको सट्टा। पहिलो पटक चलाउँदा मोडेल तौल डाउनलोड हुन्छ। त्यसपछि नोटबुकले स्थानीय क्यासलाई पुनः प्रयोग गर्न सक्छ।

> [!NOTE]  
> मैले `BAAI/bge-small-en-v1.5` प्रयोग गरेको छु किनभने यो हल्का अंग्रेजी एम्बेडिङ मोडेल हो जुन FastEmbed र Qdrant सँग राम्रो काम गर्छ स्थानीय ट्युटोरियलका लागि। यसले ३८४-आयामिक भेक्टरहरू सिर्जना गर्छ, जसले उदाहरणलाई तेज र सस्तो बनाउन मद्दत गर्छ। यो एकमात्र राम्रा विकल्प होइन। २०२३ मा धेरै ट्युटोरियलहरूले होस्ट गरिएको एम्बेडिङ मोडेलहरू जस्तै `text-embedding-ada-002` प्रयोग गरे। आज, नयाँ होस्ट गरिएको विकल्पहरू जस्तै OpenAI का `text-embedding-3-small` र `text-embedding-3-large`, र खुला-स्रोत विकल्पहरू जस्तै BGE, E5, MiniLM, Nomic Embed, र बहुभाषिक मोडेलहरू जस्तै `BAAI/bge-m3` सबै कार्यभार अनुसार उपयुक्त छनोट हुन सक्छन्। उत्पादनमा, तपाईंका आफ्ना कागजातमा पुनःप्राप्ति मूल्यांकनबाट उपयुक्त एम्बेडिङ मोडेल चयन गर्नुपर्छ।

केही व्यवहारिक विकल्पहरू:

| मोडेल परिवार | उपयोग गर्ने सन्दर्भ |
| --- | --- |
| `text-embedding-ada-002` | पुरानो होस्ट गरिएको आधारभूत मोडेल जुन धेरै २०२३-युगका ट्युटोरियलहरूमा देखियो। म नयाँ ट्युटोरियलमा डिफल्टको रूपमा यसलाई रोज्दिनँ। |
| `text-embedding-3-small` | आधुनिक होस्ट गरिएको डिफल्ट, जब म बलियो लागत/प्रदर्शन सन्तुलन चाहन्छु र स्थानीय मात्र एम्बेडिङ आवश्यक छैन। |
| `text-embedding-3-large` | पुनःप्राप्ति गुणस्तर महत्वपूर्ण हुँदा होस्ट गरिएको विकल्प, भेक्टर आकार वा एम्बेडिङ लागत भन्दा बढी प्राथमिकता। |
| `BAAI/bge-small-en-v1.5` | ट्युटोरियल, प्रोटोटाइप, र CPU-अनुकूल प्रयोगका लागि हल्का स्थानीय अंग्रेजी आधार। |
| `BAAI/bge-base-en-v1.5` वा `BAAI/bge-large-en-v1.5` | राम्रो पुनःप्राप्ति गुणस्तर चाहिँदा र बढी कम्प्युटिङ क्षमतासँग काम गर्दा ठूलो स्थानीय अंग्रेजी मोडेलहरू। |
| `BAAI/bge-m3` | बहुभाषिक वा लामो सन्दर्भ पुनःप्राप्ति, विशेष गरी कागजातहरू केवल अंग्रेजी नभएका बेला। |
| `sentence-transformers/all-MiniLM-L6-v2` | छिटो र सानो सिमान्टिक खोज आधार। गति र सरलता सबैभन्दा महत्वपूर्ण हुँदा उपयोगी। |
| `nomic-embed-text-v1.5` | खुला स्थानीय एम्बेडिङ विकल्प, लामो सन्दर्भ वा पोर्टेबिलिटी-केंद्रित सेटअपहरूको परीक्षणको लागि योग्य। |

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
  
त्यसपछि प्रत्येक खण्डले एम्बेडिङ पाउँछ:

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
  
## ६. Qdrant स्थानीय मोडमा भेक्टरहरू भण्डारण गर्नुहोस्

अब हामी एक इन-मेमोरी Qdrant संग्रह बनाएर खण्डहरू पेलोड मेटाडाटा सहित राख्छौं।

> [!NOTE]  
> २०२३ को ट्युटोरियलमा, मैले FAISS प्रयोग गरेको थिएँ किनभने यो स्थानीय भेक्टर समानता खोज प्रदर्शन गर्न सजिलो र लोकप्रिय तरिका हो। FAISS अझै छिटो स्थानीय प्रयोगहरूको लागि उपयोगी छ। २०२६ संस्करणमा, मैले Qdrant प्रयोग गरेको छु किनभने म ट्युटोरियललाई उत्पादन-जस्तो RAG प्रणाली नजिकका अनुभव दिन चाहन्छु। Qdrant ले मलाई भेक्टरहरू स्रोत फाइल, खण्ड शीर्षक, दस्तावेज نسخه, र अनुमति जस्ता पेलोड मेटाडाटासँग भण्डारण गर्न दिन्छ। यसले पुनःप्राप्ति निरीक्षण सजिलो बनाउँछ र फिल्टरिन्ग, उद्धरण, र भविष्य स्थायी वा सर्भर-आधारित परिनियोजनका लागि तयारी गर्छ।

FAISS भेक्टर समानता खोज प्रदर्शन गर्न राम्रो हो। Qdrant सानो तर उत्पादन-जस्तो RAG पुनःप्राप्ति तह देखाउन राम्रो।

केही व्यवहारिक विकल्पहरू:

| भेक्टर भण्डारण / खोज तह | उपयोग गर्ने सन्दर्भ |
| --- | --- |
| Qdrant | स्थानीय प्रोटोटाइप, मेटाडाटा फिल्टरिङ, उत्पादन-अनुकूल भेक्टर खोज, र सरल Python वर्कफ्लो। |
| Chroma | छिटो स्थानीय RAG परीक्षण र नोटबुक, जहाँ सरलता आवश्यक छ। |
| FAISS | हल्का स्थानीय भेक्टर खोज जब मैले मात्र समानता खोज चाहन्छु र मेटाडाटालाई अलग व्यवस्थापन गर्न सक्छु। |
| Milvus | ठूलो स्तरको खुला-स्रोत भेक्टर खोज, जब टोली समर्पित भेक्टर डाटाबेस सञ्चालन गर्न सक्षम हुन्छ। |
| Weaviate | स्कीमा, मेटाडाटा, हाइब्रिड खोज, र प्रबन्धित वा स्व-होस्टेड परिनियोजन विकल्पहरूसँग भेक्टर खोज। |
| Azure AI Search | Azure मा एंटरप्राइज RAG, जब मलाई कुञ्जीशब्द खोज, भेक्टर खोज, हाइब्रिड पुनःप्राप्ति, सिमान्टिक र्याङ्किङ, फिल्टरिङ, सुरक्षा, र प्रबन्धित सञ्चालन एकै खोज तहमा चाहिन्छ। |
| PostgreSQL + pgvector | जस टोलीले PostgreSQL पहिले नै प्रयोग गरिरहेका छन् र एप्लिकेसन डेटासँग नजिकै भेक्टर खोज चाहन्छन्। |

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
  
पछि पोइन्टहरू राख्नुहोस्:

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
  
मेरो चलाउँदा, संग्रहले ८ भेक्टरहरू राख्यो।

यहाँ RAG प्रणाली निरीक्षणयोग्य हुन थाल्छ। भेक्टर डाटाबेस मात्र भेक्टरहरू भण्डारण गर्दैन; यसले प्रमाण पाठ र उद्धरणका लागि आवश्यक मेटाडाटा पनि भण्डारण गर्छ।

## ७. उम्मेदवार खण्डहरू पुनःप्राप्त गर्नुहोस्

अब प्रश्न सोध्नुहोस् र उम्मेदवार खण्डहरू पुनःप्राप्त गर्नुहोस्।

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
  
यस चरणमा, म उत्तर उत्पादन गर्नु अघि पुनःप्राप्त खण्डहरू प्रिन्ट गर्छु। यो महत्वपूर्ण छ। यदि पुनःप्राप्ति गलत छ भने, उत्पादनले मात्र समस्यालाई प्रवाही पाठ पछाडि लुकाउँछ।

## ८. हल्का पुनःक्रमक थप्नुहोस्

जब मैले पहिलो पटक पुनःप्राप्ति मार्ग परीक्षण गरें, भेक्टर समानता मात्रले सान्दर्भिक नीति सामग्री भेटायो, तर सबैभन्दा सटीक खण्ड सधैं शीर्षमा थिएन।

त्यसैले मैले सानो स्थानीय पुनःक्रमक थपें। यसले प्रश्न शब्दहरू खण्ड शीर्षक र सामग्रीसँग मिल्दा अतिरिक्त वजन दिन्छ।

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
  
पुनःक्रमण पछि, शीर्ष परिणाम भयो:

```text
school_ai_policy.md / Final Assignments
```
  
त्यो परीक्षण प्रश्नको लागि अपेक्षित खण्ड थियो।

यो पहिलो कार्यान्वयनबाट सबैभन्दा उपयोगी पाठ थियो। सानो स्थानीय उदाहरणमा पनि, जब मैले भेक्टर समानतालाई अर्को संकेतसँग जोडें, पुनःप्राप्ति गुणस्तर सुधार भयो।

## ९. आधारित स्थानीय उत्तर सँगठन गर्नुहोस्

डिफल्ट मार्गका लागि, मैले पारदर्शी स्थानीय उत्तर सँगठानकर्ता प्रयोग गर्छु LLM को सट्टा।

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
  
यो अन्तिम उत्पादन उत्तर जेनेरेटर होइन। यो डिबगिङ उपकरण हो। यसले मोडेल भेरिएबिलिटी थप्नुअघि पुनःप्राप्ति, मेटाडाटा, र उद्धरण जडान काम गर्छ भनेर प्रमाणित गर्दछ।

## १०. Ollama र Phi-4-mini सँग स्थानीय उत्तर उत्पादन गर्नुहोस्

पुनःप्राप्ति काम गरेपछि, नोटबुकले केवल अन्तिम उत्तर चरण Ollama र `phi4-mini:3.8b` सँग प्रतिस्थापन गर्न सक्छ।

> [!NOTE]  
> Ollama ले केवल अन्तिम उत्तर-जेनेरेसन चरण प्रतिस्थापन गर्नुपर्छ। कागजात लोडिङ, खण्ड विभाजन, भेक्टर भण्डारण, पुनःप्राप्ति, पुनःक्रमण, र उद्धरण जडान यस्तै रहनुपर्छ।

पहिलो, नोटबुकले पुनःप्राप्त खण्डबाट प्रमाण प्रॉम्प्ट बनाउँछ:

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
  
यस ट्युटोरियलका लागि, म Microsoft को Phi-4-mini परिवारलाई Ollama मार्फत डिफल्ट स्थानीय उत्पादन विकल्पको रूपमा सिफारिस गर्छु। Ollama मा मैले परीक्षण गरेको मोडेल नाम हो:

```powershell
ollama pull phi4-mini:3.8b
```
  
तपाईँ छिटो जाँच गर्न सक्नुहुन्छ कि मोडेल उपलब्ध छ:

```powershell
ollama list
```
  
त्यसपछि यी भेरिएबलहरू सेट गर्नुहोस्:

```powershell
Copy-Item .env.example .env
```
  
`.env` खोल्नुहोस् र सिरिज २ Ollama मानहरू अनकमेन्ट गर्नुहोस्:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```
  
नोटबुकले रिपोजिटरी मूलबाट `python-dotenv` सँग `.env` लोड गर्छ, त्यसपछि सोही प्रमाण प्रॉम्प्टलाई Ollama को स्थानीय `/api/chat` अन्तबिन्दुमा स्ट्रीमिङ बन्द गरेर पठाउँछ। यदि Ollama चलिरहेको छैन वा `SERIES2_OLLAMA_MODEL` छुटेको छ भने, यो ट्रयाक छोडिन्छ।

> [!NOTE]  
> यस मेसिनमा, `phi4-mini:3.8b` ले लगभग २.४९GB मोडेल फाइलहरू डाउनलोड गर्यो। inference समयमा, Ollama ले ३.३GB लोड गरिएको मोडेल साइज रिपोर्ट गर्यो र RTX 3060 ल्यापटप GPU प्रयोग गर्यो।

यसले ट्युटोरियललाई दुई तह दिन्छ:

1. CPU-मैत्री निर्धारक उत्तर सँगठनकर्ता।  
2. Ollama र Phi-4-mini सँग स्थानीय उत्तर जेनेरेशन।

दुबैमा पुनःप्राप्ति पाइपलाइन उस्तै रहन्छ।

## ११. प्रमाणीकरण परिणाम

मैले नोटबुक स्थानीय Windows मा Python 3.12.6 सँग चलाएँ।

स्थापित प्याकेजहरू:

| प्याकेज | भर्सन |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

नोटबुक कार्यान्वयन:

- नोटबुक: `notebooks/series-2-open-source-rag.ipynb`  
- कार्यान्वयन परिणाम: `nbclient` सँग सफल  
- लोड गरिएको कागजातहरू: २  
- बनाइएका खण्डहरू: ८  
- Qdrant संग्रह: `school_policy_local`  
- राखिएका भेक्टरहरू: ८  
- एम्बेडिङ मोडेल: `BAAI/bge-small-en-v1.5`  
- एम्बेडिङ आकार: ३८४
- पुनःप्राप्ति प्रश्न: "के म मेरो अन्तिम असाइनमेन्टको लागि जेनेरेटिभ AI प्रयोग गर्न सक्दछु?"
- पुनःक्रम निर्धारण मार्ग: हल्का तौलको स्थानीय शब्दावली पुनःक्रम निर्धारण
- पुनःक्रम निर्धारण पछि शीर्ष प्राप्त स्रोत: `school_ai_policy.md`
- पुनःक्रम निर्धारण पछि शीर्ष प्राप्त खण्ड: `अन्तिम असाइनमेन्टहरू`
- डिफल्ट उत्तर मार्ग: स्थानीय पारदर्शी उत्तर निर्माता
- Ollama उत्पादन मार्ग: `phi4-mini:3.8b` द्वारा पूरा
- Ollama मोडल फाइल साइज: डिस्कमा 2.49GB
- Ollama लोड गरिएको मोडल साइज: `ollama ps` अनुसार 3.3GB रिपोर्ट गरिएको
- GPU अफलोड: `ollama ps` अनुसार 100% GPU
- उत्पादन पछि GPU मेमोरी देखिएको: RTX 3060 ल्यापटप GPU मा ६GB मध्ये करिब 3.5GB प्रयोग गरिएको
- क्याच गरिएको FastEmbed मोडल र Ollama उत्पादन सक्षम गरेर नोटबुक कार्यान्वयन: मान्यता स्क्रिप्ट मार्फत करिब 34 सेकेण्डमा पास

Ollama-ले उत्पादन गरेको उत्तर:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

म यो उत्तरलाई पूर्ण भन्दिन। यो सही प्रमाणबाट जवाफ दिन्छ, तर अन्तिम स्रोत पंक्ति निर्धारण गरिएको उद्धरण ढाँचाभन्दा कम सटीक छ। यो ट्युटोरियलमा देखाउन उपयोगी छ किनकि यसले अर्को इञ्जिनियरिङ प्रश्न स्पष्ट बनाउँछ: जवाफ उत्पादनलाई पनि मूल्याङ्कन चाहिन्छ, मात्र पुनःप्राप्ति मात्रै होइन।

पुष्टि गर्दा मैले मुख्य रूपमा सिकेको कुरा यो हो कि उत्तर उत्पादन गर्नु अघि पुनःप्राप्ति गुणस्तर जाँचिनु पर्छ। एम्बेडिङ नतिजा पहिले नै उपयोगी थियो, र हल्का तौलको पुनःक्रम निर्धारकले अपेक्षित नीतिको खण्डलाई पहिलो बनाउनु विश्वसनीय बनायो। यो नै त्यस्तो सानो प्रणाली व्यवहार हो जुन म ट्युटोरियलले देखाउन चाहन्छु र लुकाउन होइन।

## 12. के आउने छ

अर्को सुधार भनेको यो स्थानीय सेटअपलाई एउटै विद्यालय नीति सहायकको स्थितिको प्रबन्धित Azure संस्करणसँग तुलना गर्नु हो। स्थितिलाई स्थिर राख्दा व्यापारिक तौलहरू सजिलै देख्न सकिन्छ: सेटअप जटिलता, पुनःप्राप्ति नियन्त्रणहरू, पहिचान एकीकरण, सञ्चालन स्वामित्व, र लागत।

## 13. सन्दर्भहरू

- [Qdrant Python क्लाइन्ट क्विकस्टार्ट](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant क्लाइन्ट GitHub भण्डार](https://github.com/qdrant/qdrant-client)
- [FastEmbed समर्थित मोडलहरू](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI एम्बेडिङ्स मार्गदर्शन](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 मोडल कार्ड](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 मोडल कार्ड](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 मोडल कार्ड](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini मोडल पृष्ठ](https://ollama.com/library/phi4-mini)
- [Ollama Windows कागजात](https://docs.ollama.com/windows)
- [Ollama API स्ट्रिमिङ कागजात](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct मोडल कार्ड](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph सिंहावलोकन](https://docs.langchain.com/oss/python/langgraph)
- [RAG परिचय - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

अघिल्लो: [सिरिज १](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी सही हुन प्रयास गर्छौं, तर कृपया जानकार हुनुस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छन्। मूल दस्तावेज़ यसको मूल भाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलत बुझाइ वा त्रुटिको लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->