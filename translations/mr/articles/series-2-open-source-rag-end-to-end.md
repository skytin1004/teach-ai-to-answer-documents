# आपल्या दस्तऐवजांच्या आधारे प्रश्नांची उत्तरे देण्यासाठी AI शिकवा
## मालिका 2: स्थानिक ओपन-सोर्स RAG प्रणाली अखेरीस तयार करा

![स्थानिक ओपन-सोर्स RAG ट्युटोरियल पाइपलाइन](../../../assets/images/series-2-local-rag.svg)

> हा लेख मालिका 1 च्या आर्किटेक्चर चर्चेला एक चालवणारी स्थानिक RAG ट्युटोरियलमध्ये रूपांतरित करतो. उद्दिष्ट हे आहे की पहिले संपूर्ण वर्कफ्लो नमुना डेटासह तयार करणे, कोणताही क्लाउड खाते नसताना आणि गुपितांशिवाय, नंतर त्या काम करणाऱ्या बेसलाईनवरून उत्तम आर्किटेक्चर निर्णय घेणे.

आपण तयार करणार असलेली प्रणाली ही एक लहान शाळा धोरण सहाय्यक आहे. मी दोन स्थानिक मार्कडाऊन दस्तऐवज ज्ञानाधार म्हणून वापरतो, नंतर संपूर्ण RAG पाइपलाइनमधून जातो: चंकिंग, स्थानिक एम्बेडिंग्ज, Qdrant व्हेक्टर संग्रहण, रिट्रीव्हल, रीरेन्किंग, स्रोत-जाणून घेऊन उत्तर तयार करणे आणि ऐच्छिक स्थानिक जनरेशन Ollama आणि Phi-4-mini सह.

मालिका नेव्हिगेशन: [रेपॉझिटरी मुख्यपृष्ठ](../README.md) | मागील: [मालिका 1 - RAG, Azure vs Open-Source पर्याय, आणि जेव्हा फायन ट्यूनिंग अर्थपूर्ण असते](./series-1-rag-azure-open-source-fine-tuning.md)

नोटबुक: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | आवश्यकताः [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> जर आपण RAG पाइपलाइन समजून घ्यायची असल्यास, क्लाउड संसाधने तयार करण्यापूर्वी येथे सर्वोत्तम सुरुवात बिंदू आहे. डिफॉल्ट मार्ग स्थानिक CPU-मैत्रीपूर्ण एम्बेडिंग्जसह चालते आणि गुपितांशिवाय.

## 1. आपण काय तयार करीत आहोत

2023 च्या ट्युटोरियलमध्ये, मी Azure पासून सुरुवात केली कारण उद्दिष्ट होते Azure AI Search आणि Azure OpenAI द्वारे PDF दस्तऐवजांमधून प्रश्नांची उत्तरे देणे कसे शक्य आहे ते दाखवणे.

या 2026 मालिकेसाठी, मला एक स्तर खाली सुरुवात करायची आहे.

व्यवस्थापित सेवा वापरण्यापूर्वी, मला स्थानिकपणे एक लहान RAG प्रणाली तयार करायची आहे आणि प्रत्येक टप्पा दृश्यमान बना: दस्तऐवज लोड करणे, मजकूर चंक करणे, व्हेक्टर संग्रहित करणे, पुरावे शोधणे, रीरेन्क करणे आणि स्रोत-जाणून घेऊन उत्तर देणे.

नमुना परिस्थिती एक शाळा धोरण सहाय्यक आहे. वापरकर्ता विचारतो:

```text
Can I use generative AI for my final assignment?
```

सिस्टमने साधारण मॉडेल मेमरीवरून उत्तर देऊ नये. त्याने संबंधित धोरणाचा विभाग शोधून त्या पुराव्यापासून उत्तर द्यायला हवे.

संपूर्ण चालवणारे आवृत्ती [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) मध्ये आहे. खालील कोड प्रमुख टप्पे दाखवतो जेणेकरून लेख ट्युटोरियल म्हणून वाचता येईल.

## 2. स्थानिक अवलंबन स्थापित करा

व्हर्च्युअल एन्व्हायर्नमेंट तयार करा आणि मालिका 2 ची गरज असलेली भरती करा:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

पहिली आवृत्ती Qdrant स्थानिक मोड आणि FastEmbed वापरते. Qdrant चे Python क्लायंट `QdrantClient(":memory:")` सह इन-मेमरी स्थानिक मोडला समर्थन देते, जी स्थानिक ट्युटोरियल्स आणि CI-शैलीची पडताळणीसाठी उपयुक्त आहे. FastEmbed आपल्याला क्लाउड API कीशिवाय वास्तविक स्थानिक एम्बेडिंग मॉडेल देते.

गरजांची फाइलमध्ये `python-dotenv` देखील समाविष्ट आहे कारण नोटबुक ऐच्छिकरित्या `.env` मधून Ollama मॉडेल नाव वाचू शकतो. या स्थानिक ट्युटोरियलसाठी Azure OpenAI किंवा OpenAI API की आवश्यक नाही.

## 3. नमुना दस्तऐवज लोड करा

नमुना कॉर्पस हेतुपूर्वक लहान आहे:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

नोटबुकमध्ये, मी `sample_data/` मधील सर्व मार्कडाऊन फाईल्स लोड करतो:

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

नोटबुक चालवताना, त्याने 2 दस्तऐवज लोड केले. ते मॅन्युअली तपासण्यासाठी पुरेसे लहान आहे, जेव्हा RAG पाइपलाइनचा पहिला आवृत्ती बांधत असाल तेव्हा उपयोगी आहे.

## 4. मार्कडाऊन हेडिंगनुसार चंक करा

पुढील टप्पा म्हणजे दस्तऐवजांना चंकमध्ये विभागणे.

या ट्युटोरियलसाठी, मी संरचना संकेत म्हणून मार्कडाऊन हेडिंग्ज वापरतो. दस्तऐवजाचा शीर्षक `#` पासून येतो आणि प्रत्येक विभागाचा चंक `##` पासून तयार होतो.

> [!NOTE]
> चंकिंग सर्वसाधारण स्वरूपात नसते. या ट्युटोरियलमध्ये, मी मार्कडाऊन हेडिंग्ज वापरतो कारण नमुना दस्तऐवजांमध्ये स्पष्ट `#` आणि `##` संरचना आहे. PDFs, Word दस्तऐवज, स्लाइड्स, तिकीट किंवा वेबपेजेससाठी, चांगला धोरण म्हणजे पानाची सीमा, लेआउट माहिती, अर्थपूर्ण विभाग, टोकन मर्यादा, तक्ता किंवा मेटाडेटा वापरणे. महत्त्वाचे म्हणजे त्याचा अर्थ आणि स्रोत ट्रॅसिबिलिटी जपणारा चंकिंग धोरण निवडणे.

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

नंतर मी ते प्रत्येक दस्तऐवजात लागू करतो:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

माझ्या स्थानिक चाचणीत यामुळे 8 चंक तयार झाले.

मला या टप्प्याबद्दल आवडले की मेटाडेटा आधीच उपयुक्त आहे. प्रत्येक चंकला त्याचा `source`, `sectionHeading`, `documentVersion` आणि प्लेसेहोल्डर `permissions` माहित आहेत. अगदी लहान ट्युटोरियलमध्येही, हे संदर्भ देणे आणि नंतर परवानगी-आधारित रिट्रीव्हल सुलभ करते.

## 5. स्थानिक एम्बेडिंग्ज तयार करा

प्रथम सार्वजनिक आवृत्ती साठी, मी `BAAI/bge-small-en-v1.5` FastEmbed द्वारे वापरतो.

हे ट्युटोरियल स्थानिक आणि CPU-मैत्रीपूर्ण ठेवते, परंतु तरीही एक वास्तविक एम्बेडिंग मॉडेल वापरते, प्लेसहोल्डर व्हेक्टर फंक्शन नाही. पहिल्या चालवणीत मॉडेलचे वजन डाउनलोड होते. त्यानंतर नोटबुक स्थानिक कॅश पुनर्वापर करू शकतो.

> [!NOTE]
> मी `BAAI/bge-small-en-v1.5` वापरतो कारण ते एक हलके इंग्रजी एम्बेडिंग मॉडेल आहे जे FastEmbed आणि Qdrant सह चांगले कार्य करते स्थानिक ट्युटोरियलसाठी. हे 384-डायमेंशनल व्हेक्टर तयार करते, जे स्थानिकपणे जलद आणि कमी खर्चिक ठेवते. हे एकमेव चांगले पर्याय नाही. 2023 मध्ये बऱ्याच ट्युटोरियलने होस्टेड एम्बेडिंग मॉडेल्स वापरले जसे की `text-embedding-ada-002`. आज, नवीन होस्टेड पर्याय जसे OpenAI `text-embedding-3-small` आणि `text-embedding-3-large`, आणि ओपन-सोर्स पर्याय जसे BGE, E5, MiniLM, Nomic Embed, आणि बहुभाषिक मॉडेल जसे `BAAI/bge-m3` हे सर्व योग्य पर्याय आहेत कामाच्या भारानुसार. उत्पादनात, योग्य एम्बेडिंग मॉडेल निवडावे, आपले दस्तऐवज वापरून रिट्रीव्हल मूल्यांकन द्वारा.

काही व्यावहारिक पर्याय:

| मॉडेल कुटुंब | मी कधी विचार करेन |
| --- | --- |
| `text-embedding-ada-002` | जुनाट होस्टेड बेसलाइन, जी many 2023-युगातील ट्युटोरियलमध्ये दिसली. आज नवीन ट्युटोरियलसाठी मी हे डिफॉल्ट म्हणून निवडणार नाही. |
| `text-embedding-3-small` | आधुनिक होस्टेड डिफॉल्ट जो मला शक्तिशाली किंमत/कामगिरी संतुलन हवा आणि स्थानिक-अवश्यक्षम एम्बेडिंग नको असतील. |
| `text-embedding-3-large` | जेव्हा रिट्रीव्हल गुणवत्ता व्हेक्टर आकार किंवा एम्बेडिंग खर्चापेक्षा महत्त्वाची असते तेव्हा होस्टेड पर्याय. |
| `BAAI/bge-small-en-v1.5` | ट्युटोरियल्स, प्रोटोटाइप्स, आणि CPU-मैत्रीपूर्ण प्रयोगांसाठी हलके स्थानिक इंग्रजी बेसलाइन. |
| `BAAI/bge-base-en-v1.5` किंवा `BAAI/bge-large-en-v1.5` | मोठे स्थानिक इंग्रजी मॉडेल जेव्हा मला सुधारित रिट्रीव्हल गुणवत्ता हवी आणि अधिक गणना करू शकतो. |
| `BAAI/bge-m3` | बहुभाषिक किंवा दीर्घ-संदर्भ रिट्रीव्हल, विशेषतः जेव्हा दस्तऐवज फक्त इंग्रजी नसतात. |
| `sentence-transformers/all-MiniLM-L6-v2` | खूप लहान आणि जलद सेमॅंटिक सर्च बेसलाइन. जेव्हा वेग आणि सोपेपणा महत्वाचा असतो तेव्हा उपयोगी. |
| `nomic-embed-text-v1.5` | लांब संदर्भ किंवा पोर्टेबिलिटी केंद्रित सेटअपसाठी तपासण्याजोगा खुला स्थानिक एम्बेडिंग पर्याय. |

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

नंतर प्रत्येक चंकला एम्बेडिंग मिळतो:

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

## 6. Qdrant स्थानिक मोडमध्ये व्हेक्टर संग्रहित करा

आता आपण एक इन-मेमरी Qdrant संग्रह तयार करू आणि चंकसह पेलोड मेटाडेटा समाविष्ट करू.

> [!NOTE]
> 2023 च्या ट्युटोरियलमध्ये, मी FAISS वापरला कारण तो LangChain सह स्थानिक व्हेक्टर सादृश्यता शोध दाखवण्याचा सोपा आणि लोकप्रिय मार्ग होता. FAISS अजूनही जलद स्थानिक प्रयोगांसाठी उपयुक्त आहे. या 2026 आवृत्तीत, मी Qdrant वापरतो कारण मला ट्युटोरियल उत्पादन RAG प्रणालीजवळ आहे असे वाटावेसे वाटते. Qdrant मला व्हेक्टरस सोबत पेलोड मेटाडेटा जसे स्रोत फाईल, विभागाचे शीर्षक, दस्तऐवज आवृत्ती, आणि परवानग्या साठवण्याची मुभा देतो. त्यामुळे रिट्रीव्हल तपासणे सोपे होते आणि भविष्यातील फिल्टरिंग, संदर्भ देणे, आणि सतत किंवा सर्व्हर-आधारित तैनातीसाठी तयार करते.

FAISS व्हेक्टर समानता शोध दाखवण्यासाठी छान आहे. Qdrant एक लहान पण उत्पादनांसारखी RAG रिट्रीव्हल थर दाखवण्यासाठी चांगला आहे.

काही व्यावहारिक पर्याय:

| व्हेक्टर स्टोअर / शोध थर | मी कधी विचार करेन |
| --- | --- |
| Qdrant | स्थानिक प्रोटोटाइप, मेटाडेटा फिल्टरिंग, उत्पादन-स्नेही व्हेक्टर शोध, आणि सोपा Python वर्कफ्लो. |
| Chroma | जलद स्थानिक RAG प्रयोग आणि नोटबुक जिथे सोपेपणा महत्वाचा असतो. |
| FAISS | हलके स्थानिक व्हेक्टर शोध जेव्हा मला फक्त समानता शोध हवा आणि मेटाडेटा स्वतंत्रपणे सांभाळू शकतो. |
| Milvus | मोठ्या प्रमाणावर खुला व्हेक्टर शोध जेव्हा टीम समर्पित व्हेक्टर डेटाबेस चालवायला तयार आहे. |
| Weaviate | व्हेक्टर शोध स्कीमा, मेटाडेटा, हायब्रिड शोध, आणि व्यवस्थापित किंवा स्वयं-होस्टेड तैनातीसाठी पर्यायांसह. |
| Azure AI Search | Azure वर एंटरप्राइझ RAG जेव्हा मला किवर्ड शोध, व्हेक्टर शोध, हायब्रिड रिट्रीव्हल, सेमॅंटिक रँकिंग, फिल्टरिंग, सुरक्षा आणि व्यवस्थापित ऑपरेशन्स एकाच शोधथरात हवे असतील. |
| PostgreSQL + pgvector | आधीपासून PostgreSQL वापरणाऱ्या टीम्ससाठी जे अ‍ॅप्लिकेशन डेटाजवळ व्हेक्टर शोध हवे असते. |

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

नंतर पॉइंट्स समाविष्ट करा:

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

माझ्या चालवण्यात, संग्रहाने 8 व्हेक्टर जोडले.

इथे RAG प्रणाली तपासण्याजोगी होऊ लागते. व्हेक्टर डेटाबेस केवळ व्हेक्टर संग्रहित करत नाही; तो पुरावे मजकूर आणि संदर्भासाठी आवश्यक मेटाडेटा साठवतो.

## 7. उमेदवार चंक मिळवा

आता आपण प्रश्न विचारतो आणि उमेदवार चंक शोधतो.

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

या टप्प्यावर, मी उत्तर निर्माण करण्याआधी मिळालेली चंक प्रिंट करतो. हे महत्त्वाचे आहे. जर रिट्रीव्हल चुकीचे असेल, तर जनरेशन फक्त तो त्रुटी प्रवाही मजकूराच्या मागे लपवते.

## 8. हलका रीरेन्कर जोडा

जेव्हा मी रिट्रीव्हल मार्ग तपासला, तेव्हा फक्त व्हेक्टर समानता संबंधित धोरण सामग्री सापडली, पण सर्वात अचूक विभाग नेहमी शीर्षस्थानी नव्हता.

मग मी एक लहान स्थानिक रीरेन्कर जोडला. तो विभागाच्या हेडिंग आणि सामग्रीशी प्रश्नातील शब्द जुळा तेव्हा अतिरिक्त वजन देतो.

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

रीरेन्किंगनंतर, शीर्ष निकाल झाला:

```text
school_ai_policy.md / Final Assignments
```

हा चाचणी प्रश्नासाठी अपेक्षित विभाग होता.

ही पहिल्या अंमलबजावणीतील सर्वात उपयुक्त शिकवण होती. अगदी एका लहान स्थानिक उदाहरणातही, व्हेक्टर समानता आणि आणखी एका संकेताच्या जोडणीने रिट्रीव्हल गुणवत्ता सुधारली.

## 9. एक आधारभूत स्थानिक उत्तर तयार करा

डिफॉल्ट मार्गासाठी, मी LLM च्या ऐवजी एक पारदर्शक स्थानिक उत्तर संयोजक वापरतो.

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

हे अंतिम उत्पादन उत्तर जनरेटर म्हणून नव्हे. हे एक डिबगिंग साधन आहे. हे सिद्ध करते की रिट्रीव्हल, मेटाडेटा, आणि संदर्भ वायरिंग कार्यरत आहेत मॉडेलच्या बदलण्यासाठी आधी.

## 10. Ollama आणि Phi-4-mini सह स्थानिक उत्तर तयार करा

जेव्हा रिट्रीव्हल कार्यरत असेल, तेव्हा नोटबुक अखेरीस उत्तर टप्पा Ollama आणि `phi4-mini:3.8b` सह बदलेल.

> [!NOTE]
> Ollama ने फक्त अंतिम उत्तर-निर्माण टप्पा बदलेला पाहिजे. दस्तऐवज लोडिंग, चंकिंग, व्हेक्टर संग्रहण, रिट्रीव्हल, रीरेन्किंग, आणि संदर्भ वायरिंग तेच ठेवा.

प्रथम, नोटबुक रिट्रीव्ह केलेल्या चंकसह एक पुरावा प्रॉम्प्ट तयार करतो:

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

या ट्युटोरियलसाठी, Microsoft चे Phi-4-mini कुटुंब Ollama द्वारे स्थानिक जनरेशनसाठी डिफॉल्ट पर्याय म्हणून शिफारस करतो. Ollama मध्ये माझ्या तपासलेल्या मॉडेलचे नाव:

```powershell
ollama pull phi4-mini:3.8b
```

आपण लवकर तपासू शकता की मॉडेल उपलब्ध आहे:

```powershell
ollama list
```

नंतर हे व्हेरिएबल सेट करा:

```powershell
Copy-Item .env.example .env
```

`.env` फाइल उघडा आणि मालिका 2 Ollama मूल्ये अनकमेंट करा:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

नोटबुक रेपॉझिटरी रूट मधून `python-dotenv` वापरुन `.env` लोड करतो, नंतर तोच पुरावा प्रॉम्प्ट Ollama च्या स्थानिक `/api/chat` अन्तर्भूतावर पाठवतो, स्ट्रीमिंग डिसेबलसह. Ollama चालू नसेल किंवा `SERIES2_OLLAMA_MODEL` नसेल तर हा ट्रॅक वगळला जातो.

> [!NOTE]
> या मशीनवर, `phi4-mini:3.8b` सुमारे 2.49GB मॉडेल फायली डाउनलोड केल्या. अनुमानित काळात, Ollama ने 3.3GB लोड केलेले मॉडेल आकार रिपोर्ट केला आणि RTX 3060 लॅपटॉप GPU वापरला.

या ट्युटोरियलला दोन स्तर मिळाले:

1. CPU-फक्त निश्चित उत्तर संयोजक.
2. Ollama आणि Phi-4-mini सह स्थानिक उत्तर निर्माण.

रिट्रीव्हल पाइपलाइन दोन्हीतः सारखीच राहते.

## 11. पडताळणीचा निकाल

मी नोटबुक स्थानिक Windows वर Python 3.12.6 सह चालवला.

स्थापित पॅकेजेस:

| पॅकेज | आवृत्ती |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

नोटबुक चालवणं:

- नोटबुक: `notebooks/series-2-open-source-rag.ipynb`
- चालवण्याचा निकाल: `nbclient` सह उत्तीर्ण
- लोड केलेले दस्तऐवज: 2
- तयार केलेले चंक: 8
- Qdrant संग्रह: `school_policy_local`
- समाविष्ट केलेले व्हेक्टर: 8
- एम्बेडिंग मॉडेल: `BAAI/bge-small-en-v1.5`
- एम्बेडिंग आकार: 384
- पुनर्प्राप्ति प्रश्न: "मी माझ्या अंतिम असाइनमेंटसाठी जनरेटिव्ह AI वापरू शकतो का?"
- पुनरवालीकरण मार्ग: हलके स्थानिक लेक्सिकल पुनरवालीकरण
- पुनरवालीकरणानंतर शीर्ष पुनर्प्राप्त स्रोत: `school_ai_policy.md`
- पुनरवालीकरणानंतर शीर्ष पुनर्प्राप्त विभाग: `Final Assignments`
- डीफॉल्ट उत्तर मार्ग: स्थानिक पारदर्शक उत्तर रचयित्या
- Ollama उत्पत्ती मार्ग: `phi4-mini:3.8b` सह पूर्ण
- Ollama मॉडेल फाईल आकार: डिस्कवर 2.49GB
- Ollama लोड झालेले मॉडेल आकार: `ollama ps` द्वारा 3.3GB नोंदवलेले
- GPU ऑफलोड: `ollama ps` द्वारे 100% GPU नोंदवलेले
- उत्पत्ती नंतर GPU स्मृती निरीक्षण: RTX 3060 लॅपटॉप GPU वर 6GB पैकी सुमारे 3.5GB वापरलेले
- कॅश केलेल्या FastEmbed मॉडेलसह नोटबुक कार्यान्वयन आणि Ollama उत्पत्ती सक्षम: तपासणी स्क्रिप्टद्वारे सुमारे 34 सेकंदांत यशस्वी

Ollama-कडून उत्पन्न उत्तर होते:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

मी हे उत्तर परिपूर्ण म्हणणार नाही. हे योग्य पुराव्यांवरून उत्तर देते, परंतु अंतिम स्रोत ओळ निर्धारित संदर्भ स्वरूपापेक्षा कमी नेमकी आहे. हे ट्यूटोरियलमध्ये दाखवणे उपयुक्त आहे कारण ते पुढील अभियांत्रिकी प्रश्न स्पष्ट करते: फक्त पुनर्प्राप्ती नाही तर उत्तर निर्मितीसाठी देखील मूल्यांकन आवश्यक आहे.

तपासणी करताना मला मुख्य गोष्ट समजली की उत्तर निर्मिती करण्यापूर्वी पुनर्प्राप्ती गुणवत्तेची तपासणी करणे आवश्यक आहे. एम्बेडिंग परिणाम आधीच उपयुक्त होता, आणि हलका पुनरवालीकरण करणारा अपेक्षित धोरण विभाग प्रथमच विश्वासार्हरित्या दिसू लागला. हेच लहान सिस्टीमचे वर्तन आहे जे मी ट्यूटोरियलमध्ये उघड करायला आवडेल, लपवण्याऐवजी.

## 12. पुढे काय येईल

पुढील सुधारणा म्हणजे हा स्थानिक सेटअप त्याच शाळेच्या धोरण सहाय्यक प्रकरणाचा व्यवस्थापित Azure आवृत्तीशी तुलना करणे. प्रकरण स्थिर ठेवण्यामुळे व्यापार समजणे सोपे होईल: सेटअप जटिलता, पुनर्प्राप्ती नियंत्रण, ओळख समाकलन, ऑपरेशनल मालकी, आणि खर्च.

## 13. संदर्भ

- [Qdrant Python क्लायंट क्विकस्टार्ट](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant क्लायंट GitHub रेपॉजिटरी](https://github.com/qdrant/qdrant-client)
- [FastEmbed समर्थित मॉडेल्स](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI एम्बेडिंग्स मार्गदर्शक](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 मॉडेल कार्ड](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 मॉडेल कार्ड](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 मॉडेल कार्ड](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini मॉडेल पेज](https://ollama.com/library/phi4-mini)
- [Ollama Windows दस्तऐवज](https://docs.ollama.com/windows)
- [Ollama API प्रवाह दस्तऐवज](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct मॉडेल कार्ड](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph अवलोकन](https://docs.langchain.com/oss/python/langgraph)
- [RAG परिचय - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

पूर्वी: [सिरीज 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून अनुवादित केला आहे. जरी आम्ही अचूकतेसाठी प्रयत्न करतो, तरी कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या मूळ भाषेत अधिकृत स्रोत मानला पाहिजे. महत्त्वाची माहिती असल्यास, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थलावणीसाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->