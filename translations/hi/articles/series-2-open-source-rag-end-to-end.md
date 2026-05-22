# अपने दस्तावेज़ों के आधार पर AI को प्रश्नों का उत्तर देना सिखाएँ
## सीरीज़ 2: एक स्थानीय ओपन-सोर्स RAG सिस्टम शुरू से अंत तक बनाएं

![स्थानीय ओपन-सोर्स RAG ट्यूटोरियल पाइपलाइन](../../../assets/images/series-2-local-rag.svg)

> यह लेख सीरीज़ 1 के आर्किटेक्चर चर्चा को एक रन करने योग्य स्थानीय RAG ट्यूटोरियल में बदल देता है। लक्ष्य पहले नमूना डेटा के साथ पूरा वर्कफ़्लो बनाना है, बिना क्लाउड खाता बनाए और बिना कोई सीक्रेट्स के, फिर उस कार्यशील आधाररेखा का उपयोग करके बाद में बेहतर आर्किटेक्चर निर्णय लेना।

हम जो सिस्टम बनाएंगे वह एक छोटा स्कूल नीति सहायक है। मैं दो स्थानीय मार्कडाउन दस्तावेज़ों का उपयोग ज्ञान आधार के रूप में करता हूँ, फिर पूरे RAG पाइपलाइन से गुजरता हूँ: चंकिंग, स्थानीय एम्बेडिंग, Qdrant वेक्टर भंडारण, पुनःप्राप्ति, पुनःश्रेणीकरण, स्रोत-सचेत उत्तर रचना, और वैकल्पिक स्थानीय जनरेशन Ollama और Phi-4-mini के साथ।

सीरीज़ नेविगेशन: [रिपॉजिटरी होम](../README.md) | पिछला: [सीरीज़ 1 - RAG, Azure बनाम ओपन-सोर्स विकल्प, और जब फाइन-ट्यूनिंग समझ में आती है](./series-1-rag-azure-open-source-fine-tuning.md)

नोटबुक: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | आवश्यकताएँ: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> यदि आप क्लाउड संसाधन बनाने से पहले RAG पाइपलाइन समझना चाहते हैं, तो यह सबसे अच्छा प्रारंभिक बिंदु है। डिफ़ॉल्ट रास्ता CPU-अनुकूल एम्बेडिंग्स और बिना कोई सीक्रेट्स के स्थानीय रूप से चलता है।

## 1. हम क्या बना रहे हैं

2023 के ट्यूटोरियल में, मैंने Azure से शुरुआत की क्योंकि लक्ष्य यह दिखाना था कि Azure AI Search और Azure OpenAI PDF दस्तावेज़ों से प्रश्नों का उत्तर कैसे दे सकते हैं।

इस 2026 सीरीज़ के लिए, मैं एक लेयर नीचे से शुरुआत करना चाहता हूँ।

मैनेज्ड सेवाओं का उपयोग करने से पहले, मैं एक छोटा RAG सिस्टम स्थानीय रूप से बनाना चाहता हूँ और हर कदम को दृश्य बनाना चाहता हूँ: दस्तावेज़ों को लोड करना, टेक्स्ट को चंक करना, वेक्टर संग्रहण, साक्ष्य पुनःप्राप्ति, परिणाम पुनःश्रेणीकरण, और स्रोत-सचेत उत्तर लौटाना।

नमूना परिदृश्य एक स्कूल नीति सहायक है। उपयोगकर्ता पूछता है:

```text
Can I use generative AI for my final assignment?
```

सिस्टम को सामान्य मॉडल मेमोरी से उत्तर नहीं देना चाहिए। इसे संबंधित नीति अनुभाग पुनःप्राप्त करना चाहिए और उस साक्ष्य से उत्तर देना चाहिए।

पूरा चलाने योग्य संस्करण [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) में है। नीचे दिए गए कोड मुख्य चरण दिखाते हैं ताकि लेख को एक ट्यूटोरियल के रूप में पढ़ा जा सके।

## 2. स्थानीय निर्भरताएँ स्थापित करें

एक वर्चुअल एन्वायरनमेंट बनाएं और सीरीज़ 2 आवश्यकताएँ इंस्टॉल करें:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

पहला संस्करण Qdrant स्थानीय मोड और FastEmbed का उपयोग करता है। Qdrant का Python क्लाइंट `QdrantClient(":memory:")` के साथ एक मेमोरी-आधारित स्थानीय मोड का समर्थन करता है, जो स्थानीय ट्यूटोरियल और CI-शैली सत्यापन के लिए उपयोगी है। FastEmbed हमें एक वास्तविक स्थानीय एम्बेडिंग मॉडल देता है, जिसमें क्लाउड API कुंजी की आवश्यकता नहीं होती।

आवश्यकताएँ फ़ाइल में `python-dotenv` भी शामिल है क्योंकि नोटबुक वैकल्पिक रूप से `.env` से Ollama मॉडल नाम पढ़ सकता है। इस स्थानीय ट्यूटोरियल के लिए Azure OpenAI या OpenAI API कुंजी आवश्यक नहीं है।

## 3. नमूना दस्तावेज़ लोड करें

नमूना कॉर्पस जानबूझकर छोटा है:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

नोटबुक में, मैं `sample_data/` से सभी मार्कडाउन फ़ाइलें लोड करता हूँ:

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

जब मैंने नोटबुक चलाया, तो उसने 2 दस्तावेज़ लोड किए। यह मैन्युअल रूप से निरीक्षण करने के लिए पर्याप्त छोटा है, जो एक RAG पाइपलाइन का पहला संस्करण बनाते समय उपयोगी होता है।

## 4. मार्कडाउन हैडिंग्स के अनुसार चंक करें

अगला कदम दस्तावेज़ों को टुकड़ों में विभाजित करना है।

इस ट्यूटोरियल के लिए, मैं संरचना संकेत के रूप में मार्कडाउन हैडिंग्स का उपयोग करता हूँ। दस्तावेज़ का शीर्षक `#` से आता है, और प्रत्येक अनुभाग का टुकड़ा `##` से आता है।

> [!NOTE]
> चंकिंग हर जगह एक जैसी नहीं होती। इस ट्यूटोरियल में, मैंने मार्कडाउन हैडिंग्स का उपयोग किया क्योंकि नमूना दस्तावेज़ों में स्पष्ट `#` और `##` संरचना है। PDFs, Word दस्तावेज़, स्लाइड्स, टिकट्स, या वेब पेजेस के लिए, बेहतर रणनीति पृष्ठ सीमाओं, लेआउट जानकारी, सैमांतिक सेक्शन, टोकन सीमा, टेबल्स या मेटाडेटा का उपयोग कर सकती है। महत्वपूर्ण बात यह है कि ऐसी चंकिंग रणनीति चुनें जो आपके दस्तावेज़ों के अर्थ और स्रोत की ट्रेसबिलीटी बनाए रखे।

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

फिर मैं इसे हर दस्तावेज़ पर लागू करता हूँ:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

मेरे स्थानीय रन में इससे 8 टुकड़े बने।

इस चरण में मुझे जो पसंद आया वह यह था कि मेटाडेटा पहले से ही उपयोगी होता है। प्रत्येक टुकड़ा अपने `source`, `sectionHeading`, `documentVersion`, और प्लेसहोल्डर `permissions` को जानता है। एक छोटे ट्यूटोरियल में भी, यह उद्धरण और बाद में अनुमति-सचेत पुनःप्राप्ति को समझना आसान बनाता है।

## 5. स्थानीय एम्बेडिंग बनाएं

पहले सार्वजनिक संस्करण के लिए, मैं FastEmbed के माध्यम से `BAAI/bge-small-en-v1.5` का उपयोग करता हूँ।

यह ट्यूटोरियल को स्थानीय और CPU-अनुकूल रखता है, लेकिन फिर भी एक वास्तविक एम्बेडिंग मॉडल का उपयोग करता है न कि केवल प्लेसहोल्डर वेक्टर फ़ंक्शन। पहली बार रन पर मॉडल वज़न डाउनलोड होते हैं। उसके बाद, नोटबुक स्थानीय कैश का पुनः उपयोग कर सकता है।

> [!NOTE]
> मैं `BAAI/bge-small-en-v1.5` का उपयोग करता हूँ क्योंकि यह एक हल्का अंग्रेज़ी एम्बेडिंग मॉडल है जो FastEmbed और Qdrant के साथ स्थानीय ट्यूटोरियल के लिए अच्छा काम करता है। यह 384-आयामी वेक्टर बनाता है, जिससे उदाहरण तेज़ और स्थानीय रूप से चलाने में सस्ता रहता है। यह एकमात्र अच्छा विकल्प नहीं है। 2023 में, कई ट्यूटोरियल मेज़बान एम्बेडिंग मॉडल जैसे `text-embedding-ada-002` का उपयोग करते थे। आज, OpenAI के `text-embedding-3-small` और `text-embedding-3-large` जैसे नए मेज़बान विकल्प, और ओपन-सोर्स विकल्प जैसे BGE, E5, MiniLM, Nomic Embed, और बहुभाषी मॉडल जैसे `BAAI/bge-m3` सभी वर्कलोड के अनुसार उचित विकल्प हैं। उत्पादन में, सही एम्बेडिंग मॉडल को अपने दस्तावेज़ों पर पुनःप्राप्ति मूल्यांकन के माध्यम से चुना जाना चाहिए।

कुछ व्यावहारिक विकल्प:

| मॉडल परिवार | मैं इसे कब विचार करता हूँ |
| --- | --- |
| `text-embedding-ada-002` | पुराना मेज़बान बेसलाइन जो कई 2023-दौर के ट्यूटोरियल में आया। मैं इसे आज के नए ट्यूटोरियल के लिए डिफ़ॉल्ट नहीं चुनता। |
| `text-embedding-3-small` | आधुनिक मेज़बान डिफ़ॉल्ट जब मुझे लागत/प्रदर्शन संतुलन चाहिए और स्थानीय-केवल एम्बेडिंग की आवश्यकता नहीं। |
| `text-embedding-3-large` | मेज़बान विकल्प जब पुनःप्राप्ति गुणवत्ता वेक्टर आकार या एम्बेडिंग लागत से अधिक महत्वपूर्ण हो। |
| `BAAI/bge-small-en-v1.5` | ट्यूटोरियल, प्रोटोटाइप, और CPU-अनुकूल प्रयोगों के लिए हल्का स्थानीय अंग्रेज़ी बेसलाइन। |
| `BAAI/bge-base-en-v1.5` या `BAAI/bge-large-en-v1.5` | बेहतर पुनःप्राप्ति गुणवत्ता के लिए बड़े स्थानीय अंग्रेज़ी मॉडल, जब अधिक कंप्यूट संभव हो। |
| `BAAI/bge-m3` | बहुभाषी या लंबी-कॉन्टेक्स्ट पुनःप्राप्ति, खासकर जब दस्तावेज़ केवल अंग्रेज़ी नहीं हों। |
| `sentence-transformers/all-MiniLM-L6-v2` | बहुत छोटा और तेज सैमांंटिक सर्च बेसलाइन। जब स्पीड और सरलता सबसे ज़्यादा मायने रखती हो तो उपयोगी। |
| `nomic-embed-text-v1.5` | खुले स्थानीय एम्बेडिंग विकल्प जो लंबी कॉन्टेक्स्ट या पोर्टेबिलिटी-फोकस्ड सेटअप के लिए परीक्षण योग्य। |

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

फिर हर टुकड़े को एक एम्बेडिंग मिलती है:

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

## 6. Qdrant स्थानीय मोड में वेक्टर संग्रहित करें

अब हम मेमोरी-आधारित Qdrant संग्रह बनाते हैं और टुकड़ों को पेलोड मेटाडेटा के साथ डालते हैं।

> [!NOTE]
> 2023 के ट्यूटोरियल में, मैंने FAISS का उपयोग किया क्योंकि यह स्थानीय वेक्टर समानता खोज को LangChain के साथ दिखाने का सरल और लोकप्रिय तरीका था। FAISS अभी भी तेज स्थानीय प्रयोगों के लिए उपयोगी है। इस 2026 संस्करण में, मैं Qdrant का उपयोग करता हूँ क्योंकि मैं चाहता हूँ कि ट्यूटोरियल प्रोडक्शन RAG सिस्टम के करीब अनुभव हो। Qdrant मुझे वेक्टर को स्रोत फ़ाइल, सेक्शन हैडिंग, दस्तावेज़ संस्करण, और अनुमतियाँ जैसे पेलोड मेटाडेटा के साथ संग्रहित करने देता है। इससे पुनःप्राप्ति को निरीक्षण करना आसान होता है और उदाहरण को फिल्टरिंग, उद्धरण, और भविष्य के स्थायी या सर्वर-आधारित परिनियोजन के लिए तैयार करता है।

FAISS वेक्टर समानता खोज दिखाने के लिए शानदार है। Qdrant एक छोटे लेकिन प्रोडक्शन-रूप से आकारित RAG पुनःप्राप्ति परत दिखाने में बेहतर है।

कुछ व्यावहारिक विकल्प:

| वेक्टर स्टोर / खोज परत | मैं इसे कब विचार करता हूँ |
| --- | --- |
| Qdrant | स्थानीय प्रोटोटाइप, मेटाडेटा फिल्टरिंग, प्रोडक्शन-अनुकूल वेक्टर खोज, और सरल Python वर्कफ़्लो। |
| Chroma | तेज़ स्थानीय RAG प्रयोग और नोटबुक्स जहाँ सरलता सबसे ज़रूरी हो। |
| FAISS | हल्का स्थानीय वेक्टर खोज जब मुझे केवल समानता खोज चाहिए और मेटाडेटा अलग से प्रबंधित कर सकता हूँ। |
| Milvus | बड़े पैमाने पर ओपन-सोर्स वेक्टर खोज जब टीम समर्पित वेक्टर डेटाबेस चलाने के लिए तैयार हो। |
| Weaviate | स्कीमा, मेटाडेटा, हाइब्रिड खोज, और प्रबंधित या स्वयं-होस्टेड परिनियोजन विकल्पों के साथ वेक्टर खोज। |
| Azure AI Search | Azure पर एंटरप्राइज RAG जब मुझे कीवर्ड खोज, वेक्टर खोज, हाइब्रिड पुनःप्राप्ति, सैमांटिक रैंकिंग, फिल्टरिंग, सुरक्षा, और प्रबंधित संचालन एक खोज परत में चाहिए। |
| PostgreSQL + pgvector | पहले से PostgreSQL का उपयोग करने वाली टीम जो वेक्टर खोज को एप्लिकेशन डेटा के करीब रखना चाहती हो। |

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

फिर पॉइंट्स डालें:

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

मेरे रन में, संग्रह ने 8 वेक्टर डाले।

यह वह जगह है जहाँ RAG सिस्टम निरीक्षणीय होना शुरू होता है। वेक्टर डेटाबेस केवल वेक्टर ही नहीं संग्रहीत करता, बल्कि साक्ष्य टेक्स्ट और उद्धरण के लिए आवश्यक मेटाडेटा भी संग्रहीत करता है।

## 7. उम्मीदवार टुकड़े पुनःप्राप्त करें

अब हम प्रश्न पूछते हैं और उम्मीदवार टुकड़े पुनःप्राप्त करते हैं।

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

इस बिंदु पर, मैं उत्तर उत्पन्न करने से पहले पुनःप्राप्त टुकड़ों को प्रिंट करता हूँ। यह महत्वपूर्ण है। अगर पुनःप्राप्ति गलत है, तो जनरेशन केवल समस्या को प्रवाही टेक्स्ट के पीछे छुपा देगा।

## 8. एक हल्का पुनःश्रेणीकर्ता जोड़ें

जब मैंने पहली बार पुनःप्राप्ति पथ का परीक्षण किया, तो वेक्टर समानता अकेले संबंधित नीति सामग्री पाती थी, लेकिन सबसे सटीक अनुभाग हमेशा शीर्ष पर नहीं था।

इसलिए मैंने एक छोटा स्थानीय पुनःश्रेणीकर्ता जोड़ा। यह प्रश्न शब्दों के सेक्शन हैडिंग और सामग्री से ओवरलैप होने पर अतिरिक्त वजन देता है।

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

पुनःश्रेणीकरण के बाद, शीर्ष परिणाम बन गया:

```text
school_ai_policy.md / Final Assignments
```

यह परीक्षण प्रश्न के लिए अपेक्षित अनुभाग था।

यह पहली कार्यान्वयन से सबसे उपयोगी सबक था। एक छोटे स्थानीय उदाहरण में भी, जब मैंने वेक्टर समानता को एक अन्य संकेत के साथ जोड़ा तो पुनःप्राप्ति गुणवत्ता में सुधार हुआ।

## 9. एक आधारभूत स्थानीय उत्तर तैयार करें

डिफ़ॉल्ट पथ के लिए, मैं LLM के बजाय एक पारदर्शी स्थानीय उत्तर संयोजक का उपयोग करता हूँ।

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

यह अंतिम उत्पाद उत्तर जनरेटर बनने का उद्देश्य नहीं है। यह एक डिबगिंग उपकरण है। यह साबित करता है कि मॉडल परिवर्तनशीलता जोड़ने से पहले पुनःप्राप्ति, मेटाडेटा, और उद्धरण तारिका काम करती है।

## 10. Ollama और Phi-4-mini के साथ स्थानीय उत्तर जनरेट करें

एक बार पुनःप्राप्ति काम करने लगे, नोटबुक केवल अंतिम उत्तर चरण को Ollama और `phi4-mini:3.8b` से प्रतिस्थापित कर सकता है।

> [!NOTE]
> Ollama को केवल अंतिम उत्तर-जनरेशन चरण को बदलना चाहिए। दस्तावेज़ लोडिंग, चंकिंग, वेक्टर स्टोरेज, पुनःप्राप्ति, पुनःश्रेणीकरण, और उद्धरण तारिका समान रहनी चाहिए।

पहले, नोटबुक पुनःप्राप्त टुकड़ों से साक्ष्य प्रॉम्प्ट बनाता है:

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

इस ट्यूटोरियल के लिए, मैं Microsoft के Phi-4-mini परिवार को Ollama के माध्यम से डिफ़ॉल्ट स्थानीय जनरेशन विकल्प के रूप में सुझाता हूँ। Ollama में, मैंने जिस मॉडल का परीक्षण किया वह है:

```powershell
ollama pull phi4-mini:3.8b
```

आप जल्दी से जांच सकते हैं कि मॉडल उपलब्ध है:

```powershell
ollama list
```

फिर इन वेरिएबल्स को सेट करें:

```powershell
Copy-Item .env.example .env
```

`.env` खोलें और सीरीज़ 2 Ollama मानों की अनकमेंट करें:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

नोटबुक `python-dotenv` के साथ रिपॉजिटरी रूट से `.env` लोड करता है, फिर ओल्लामा के स्थानीय `/api/chat` एंडपॉइंट को स्ट्रीमिंग बंद करके वही साक्ष्य प्रॉम्प्ट भेजता है। यदि Ollama चल नहीं रहा है या `SERIES2_OLLAMA_MODEL` अनुपस्थित है, तो यह ट्रैक स्किप कर दिया जाता है।

> [!NOTE]
> इस मशीन पर, `phi4-mini:3.8b` ने लगभग 2.49GB मॉडल फ़ाइलें डाउनलोड कीं। अनुमान के दौरान, Ollama ने 3.3GB लोडेड मॉडल आकार रिपोर्ट किया और RTX 3060 लैपटॉप GPU का उपयोग किया।

यह ट्यूटोरियल को दो स्तर देता है:

1. CPU-केवल निर्धारक उत्तर संयोजक।
2. Ollama और Phi-4-mini के साथ स्थानीय उत्तर जनरेशन।

पुनःप्राप्ति पाइपलाइन दोनों में समान रहती है।

## 11. सत्यापन परिणाम

मैंने नोटबुक स्थानीय रूप से Windows पर Python 3.12.6 के साथ चलाया।

इंस्टॉल किए गए पैकेज:

| पैकेज | संस्करण |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

नोटबुक निष्पादन:

- नोटबुक: `notebooks/series-2-open-source-rag.ipynb`
- निष्पादन परिणाम: `nbclient` के साथ सफल
- लोड किए गए दस्तावेज़: 2
- बनाए गए चंक: 8
- Qdrant संग्रह: `school_policy_local`
- डाले गए वेक्टर: 8
- एम्बेडिंग मॉडल: `BAAI/bge-small-en-v1.5`
- एम्बेडिंग आकार: 384
- पुनःप्राप्ति प्रश्न: "क्या मैं अपनी अंतिम असाइनमेंट के लिए जनरेटिव एआई का उपयोग कर सकता हूँ?"
- पुनःक्रमण पथ: हल्का स्थानीय शब्दगत पुनःक्रमण
- पुनःक्रमण के बाद शीर्ष प्राप्त स्रोत: `school_ai_policy.md`
- पुनःक्रमण के बाद शीर्ष प्राप्त अनुभाग: `अंतिम असाइनमेंट`
- डिफ़ॉल्ट उत्तर पथ: स्थानीय पारदर्शी उत्तर संयोजक
- Ollama जनरेशन पथ: `phi4-mini:3.8b` के साथ पूरा हुआ
- Ollama मॉडल फ़ाइल आकार: डिस्क पर 2.49GB
- Ollama लोड किया गया मॉडल आकार: `ollama ps` द्वारा रिपोर्ट किया गया 3.3GB
- GPU ऑफलोड: `ollama ps` द्वारा रिपोर्ट किया गया 100% GPU
- जनरेशन के बाद GPU मेमोरी देखी गई: RTX 3060 लैपटॉप GPU पर लगभग 3.5GB के 6GB उपयोग में
- कैश्ड FastEmbed मॉडल और Ollama जनरेशन सक्षम के साथ नोटबुक निष्पादन: सत्यापन स्क्रिप्ट के माध्यम से लगभग 34 सेकंड में पास

Ollama-जनित उत्तर था:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

मैं इस उत्तर को परिपूर्ण नहीं कहूंगा। यह सही साक्ष्य से उत्तर देता है, लेकिन अंतिम स्रोत पंक्ति निर्धारक उद्धरण प्रारूप जितनी सटीक नहीं है। इसे ट्यूटोरियल में दिखाना उपयोगी है क्योंकि यह अगला इंजीनियरिंग प्रश्न स्पष्ट बनाता है: उत्तर निर्माण को भी मूल्यांकन की आवश्यकता होती है, सिर्फ पुनःप्राप्ति नहीं।

प्रमाणित करते हुए मैंने मुख्य रूप से यह सीखा कि उत्तर निर्माण से पहले पुनःप्राप्ति गुणवत्ता की जांच करनी चाहिए। एम्बेडिंग परिणाम पहले से ही उपयोगी था, और हल्के पुनःक्रमक ने अपेक्षित नीति अनुभाग को विश्वसनीय रूप से पहले स्थान पर लाया। यही वह प्रकार का छोटा सिस्टम व्यवहार है जिसे मैं ट्यूटोरियल में छिपाने के बजाय उजागर करना चाहता हूं।

## 12. अगले क्या है

अगला सुधार इस स्थानीय सेटअप की तुलना वही स्कूल नीति सहायक परिदृश्य के प्रबंधित Azure संस्करण से करना है। परिदृश्य को स्थिर रखने से ट्रेडऑफ़ को देखना आसान होगा: सेटअप जटिलता, पुनःप्राप्ति नियंत्रण, पहचान एकीकरण, संचालन स्वामित्व, और लागत।

## 13. संदर्भ

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub repository](https://github.com/qdrant/qdrant-client)
- [FastEmbed समर्थित मॉडल](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI एम्बेडिंग निर्देशिका](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 मॉडल कार्ड](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 मॉडल कार्ड](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 मॉडल कार्ड](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini मॉडल पेज](https://ollama.com/library/phi4-mini)
- [Ollama Windows दस्तावेज़](https://docs.ollama.com/windows)
- [Ollama API स्ट्रीमिंग दस्तावेज़](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct मॉडल कार्ड](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph अवलोकन](https://docs.langchain.com/oss/python/langgraph)
- [RAG का परिचय - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

पूर्व: [श्रृंखला 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
इस दस्तावेज़ का अनुवाद AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->