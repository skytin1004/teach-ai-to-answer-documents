# আপনার ডকুমেন্টের ভিত্তিতে AI কে প্রশ্নের উত্তর দিতে শেখান
## সিরিজ ২: একটি স্থানীয় ওপেন-সোর্স RAG সিস্টেম শুরু থেকে শেষ পর্যন্ত নির্মাণ করুন

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> এই নিবন্ধটি সিরিজ ১ এর স্থাপত্য আলোচনা থেকে একটি চালানোর উপযোগী স্থানীয় RAG টিউটোরিয়ালে রূপান্তরিত করে। উদ্দেশ্য হল প্রথমে নমুনা ডেটা দিয়ে পুরো কর্মপ্রবাহ তৈরি করা, কোনো ক্লাউড অ্যাকাউন্ট বা গোপনীয়তা ছাড়া, তারপর সেই কার্যকরী বেসলাইন ব্যবহার করে পরে ভাল স্থাপত্য সিদ্ধান্ত নেওয়া।

আমরা যে সিস্টেমটি তৈরি করব তা একটি ছোট স্কুল নীতি সহকারী। আমি দুটি স্থানীয় মার্কডাউন ডকুমেন্টকে জ্ঞানভিত্তি হিসেবে ব্যবহার করি, তারপরে পুরো RAG পাইপলাইনটি পার করি: চাংকিং, স্থানীয় এমবেডিং, Qdrant ভেক্টর সংরক্ষণ, পুনরুদ্ধার, পুনর্বিন্যাস, উত্স-সচেতন উত্তর রচনা, এবং ঐচ্ছিক স্থানীয় জেনারেশন Ollama এবং Phi-4-mini ব্যবহার করে।

সিরিজ নেভিগেশন: [রিপোজিটরি হোম](../README.md) | পূর্ববর্তী: [সিরিজ ১ - RAG, Azure বনাম ওপেন-সোর্স বিকল্প এবং কখন ফাইন-টিউনিং সঙ্গত](./series-1-rag-azure-open-source-fine-tuning.md)

নোটবুক: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | প্রয়োজনীয়তা: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> ক্লাউড রিসোর্স তৈরির আগে RAG পাইপলাইন বুঝতে চাইলে এটি সেরা শুরু পয়েন্ট। ডিফল্ট পথটি CPU-বান্ধব এমবেডিং সহ স্থানীয়ভাবে চলে এবং কোনো গোপনীয়তা দরকার হয় না।

## ১. আমরা যা তৈরি করছি

2023 টিউটোরিয়ালে আমি Azure থেকে শুরু করেছিলাম কারণ লক্ষ্য ছিল দেখানো কীভাবে Azure AI Search এবং Azure OpenAI PDF ডকুমেন্ট থেকে প্রশ্নের উত্তর দিতে পারে।

এই 2026 সিরিজে, আমি এক স্তর নিচে শুরু করতে চাই।

ম্যানেজ্ড সার্ভিস ব্যবহার করার আগে, আমি স্থানীয়ভাবে একটি ছোট RAG সিস্টেম তৈরি করতে চাই এবং প্রতিটি ধাপ দৃশ্যমান করতে চাই: ডকুমেন্ট লোড করা, টেক্সট চাংক করা, ভেক্টর সংরক্ষণ, প্রমাণ পুনরুদ্ধার, পুনর্বিন্যাস, এবং উত্সসচেতন উত্তর প্রদান।

নমুনা দৃশ্যটি একটি স্কুল নীতি সহকারী। ব্যবহারকারী প্রশ্ন করেন:

```text
Can I use generative AI for my final assignment?
```

সিস্টেম সাধারণ মডেল মেমরি থেকে উত্তর দেবে না। এটি প্রাসঙ্গিক নীতি সেকশন পুনরুদ্ধার করবে এবং সেই প্রমাণ থেকে উত্তর দেবে।

সম্পূর্ণ চালানো সংস্করণটি আছে [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)-এ। নিচের কোডে প্রধান ধাপগুলো দেখানো হয়েছে যাতে নিবন্ধটি টিউটোরিয়াল হিসেবে পড়া যায়।

## ২. স্থানীয় নির্ভরতা ইনস্টল করুন

একটি ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন এবং সিরিজ ২ এর প্রয়োজনীয়তাগুলি ইনস্টল করুন:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

প্রথম সংস্করণটি Qdrant স্থানীয় মোড এবং FastEmbed ব্যবহার করে। Qdrant এর পাইথন ক্লায়েন্ট `QdrantClient(":memory:")` দিয়ে ইন-মেমোরি স্থানীয় মোড সমর্থন করে, যা স্থানীয় টিউটোরিয়াল এবং CI-স্টাইল যাচাইয়ের জন্য উপযোগী। FastEmbed আমাদের একটি প্রকৃত স্থানীয় এমবেডিং মডেল দেয় ক্লাউড API কী ছাড়াই।

প্রয়োজনীয়তা ফাইলে `python-dotenv` অন্তর্ভুক্ত রয়েছে কারণ নোটবুক ঐচ্ছিকভাবে `.env` থেকে একটি Ollama মডেলের নাম পড়তে পারে। এই স্থানীয় টিউটোরিয়ালের জন্য Azure OpenAI বা OpenAI API কী প্রয়োজন নেই।

## ৩. নমুনা ডকুমেন্ট লোড করুন

নমুনা করপাস উদ্দেশ্যমূলকভাবে ছোট:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

নোটবুকে, আমি `sample_data/` থেকে সব মার্কডাউন ফাইল লোড করি:

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

যখন আমি নোটবুক চালিয়েছিলাম, এটি ২টি ডকুমেন্ট লোড করেছিল। এটি ম্যানুয়ালি পরিদর্শন করার জন্য যথেষ্ট ছোট, যা প্রথম RAG পাইপলাইন তৈরি করার সময় উপকারী।

## ৪. মার্কডাউন শিরোনাম অনুযায়ী চাংক করা

পরবর্তী ধাপ হল ডকুমেন্টগুলোকে চাংকে বিভক্ত করা।

এই টিউটোরিয়ালে, আমি মার্কডাউন শিরোনাম ব্যবহার করি গঠন সংকেত হিসেবে। ডকুমেন্টের শিরোনাম হয়ে থাকে `#` থেকে, এবং প্রতিটি সেকশন চাংক হয় `##` থেকে।

> [!NOTE]
> চাংকিং একমাত্র পন্থা নয়। এই টিউটোরিয়ালে আমি মার্কডাউন শিরোনাম ব্যবহার করলাম কারণ নমুনা ডকুমেন্টগুলোতে স্পষ্ট `#` এবং `##` গঠন আছে। PDF, ওয়ার্ড ডকুমেন্ট, স্লাইড, টিকিট, বা ওয়েব পেজে পেজ সীমান্ত, লেআউট তথ্য, সেমান্টিক সেকশন, টোকেন সীমা, টেবিল, বা মেটাডেটা ব্যবহার করে আরও ভাল কৌশল ব্যবহার করা যেতে পারে। গুরুত্বপূর্ণ হল এমন একটি চাংকিং কৌশল বেছে নেওয়া যা অর্থ এবং উত্স ট্রেসযোগ্যতা সংরক্ষণ করে।

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

তারপর আমি এটি প্রতিটি ডকুমেন্টে প্রয়োগ করি:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

আমার স্থানীয় রান-এ এটি ৮টি চাংক তৈরি করেছিল।

এই ধাপে যা ভালো লাগলো তা হল মেটাডেটা ইতিমধ্যেই উপকারী। প্রতিটি চাংক জানে তার `source`, `sectionHeading`, `documentVersion`, এবং প্লেসহোল্ডার `permissions`। একটি ছোট টিউটোরিয়াল থেকেও এটি উদ্ধৃতি এবং পরবর্তী অনুমতিসচেতন পুনরুদ্ধার সহজ করে তোলে।

## ৫. স্থানীয় এমবেডিং তৈরি করুন

প্রথম পাবলিক সংস্করণের জন্য, আমি FastEmbed এর মাধ্যমে `BAAI/bge-small-en-v1.5` ব্যবহার করি।

এটি টিউটোরিয়ালটিকে স্থানীয় এবং CPU-বান্ধব রাখে, তবে এটি এখনও একটি প্রকৃত এমবেডিং মডেল ব্যবহার করে, প্লেসহোল্ডার ভেক্টর ফাংশন নয়। প্রথম রান মডেলের ওজন ডাউনলোড করে। এরপর নোটবুক স্থানীয় ক্যাশ ব্যবহার করতে পারে।

> [!NOTE]
> আমি `BAAI/bge-small-en-v1.5` ব্যবহার করি কারণ এটি একটি হালকা ইংরেজি এমবেডিং মডেল যা FastEmbed এবং Qdrant সহ স্থানীয় টিউটোরিয়ালের জন্য ভালো কাজ করে। এটি ৩৮৪-ডাইমেনশন ভেক্টর তৈরি করে, যা উদাহরণটিকে দ্রুত এবং স্থানীয়ভাবে সাশ্রয়ী করে তোলে। এটি একমাত্র ভাল বিকল্প নয়। ২০২৩ সালে অনেক টিউটোরিয়ালে হোস্টেড এমবেডিং মডেল যেমন `text-embedding-ada-002` ব্যবহৃত হয়। আজ, নতুন হোস্টেড অপশন যেমন OpenAI এর `text-embedding-3-small` এবং `text-embedding-3-large`, এবং ওপেন-সোর্স অপশন যেমন BGE, E5, MiniLM, Nomic Embed, এবং বহুভাষিক মডেল যেমন `BAAI/bge-m3` সবই কাজের ধরন অনুযায়ী যৌক্তিক বিকল্প। প্রোডাকশনে, সঠিক এমবেডিং মডেলটি আপনার ডকুমেন্ট উপর পুনরুদ্ধার মূল্যায়নের মাধ্যমে নির্বাচন করা উচিত।

কিছু বাস্তবসম্মত বিকল্প:

| মডেল পরিবার | কখন আমি বিবেচনা করব |
| --- | --- |
| `text-embedding-ada-002` | পুরানো হোস্টেড বেসলাইন যা অনেক ২০২৩-এপোক টিউটোরিয়ালে ব্যবহৃত হয়েছে। নতুন টিউটোরিয়ালের ডিফল্ট হিসেবে আমি এটিকে বেছে নেব না। |
| `text-embedding-3-small` | আধুনিক হোস্টেড ডিফল্ট যখন আমি শক্তিশালী মূল্য/কার্যকারিতা ভারসাম্য চাই এবং শুধুমাত্র স্থানীয় এমবেডিং দরকার নেই। |
| `text-embedding-3-large` | হোস্টেড অপশন যখন পুনরুদ্ধার গুণগত মান ভেক্টরের আকার বা এমবেডিং খরচের চেয়ে বেশি গুরুত্বপূর্ণ। |
| `BAAI/bge-small-en-v1.5` | টিউটোরিয়াল, প্রোটোটাইপ, এবং CPU-বান্ধব পরীক্ষার জন্য হালকা স্থানীয় ইংরেজি বেসলাইন। |
| `BAAI/bge-base-en-v1.5` বা `BAAI/bge-large-en-v1.5` | বড় স্থানীয় ইংরেজি মডেল যেখানে উন্নত পুনরুদ্ধার গুণগত মান লাগে এবং বেশি কম্পিউট উপস্থাপন করা যায়। |
| `BAAI/bge-m3` | বহুভাষিক বা দীর্ঘ-কন্টেক্সট পুনরুদ্ধার, বিশেষ করে যেখানে ডকুমেন্ট শুধু ইংরেজি নয়। |
| `sentence-transformers/all-MiniLM-L6-v2` | খুব ছোট এবং দ্রুত সেমান্টিক সার্চ বেসলাইন। গতি এবং সরলতা সবচেয়ে গুরুত্বপূর্ণ হলে উপকারী। |
| `nomic-embed-text-v1.5` | দীর্ঘ-কন্টেক্সট বা পোর্টেবিলিটি-কেন্দ্রিক সেটআপের জন্য খোলামেলা স্থানীয় এমবেডিং অপশন যা পরীক্ষার যোগ্য। |

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

তারপর প্রতিটি চাংকে একটি এমবেডিং পায়:

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

## ৬. Qdrant স্থানীয় মোডে ভেক্টর সংরক্ষণ করুন

এখন আমরা একটি ইন-মেমোরি Qdrant কালেকশন তৈরি করি এবং মেটাডেটাসহ চাংকগুলো ঢোকাই।

> [!NOTE]
> ২০২৩ টিউটোরিয়ালে আমি FAISS ব্যবহার করেছিলাম কারণ এটি একটি সহজ এবং জনপ্রিয় উপায় লোকাল ভেক্টর সাদৃশ্য অনুসন্ধান দেখানোর জন্য LangChain এর সাথে। FAISS এখনও দ্রুত স্থানীয় পরীক্ষার জন্য উপকারী। এই ২০২৬ সংস্করণে, আমি Qdrant ব্যবহার করি কারণ আমি চাই টিউটোরিয়ালটি একটি প্রোডাকশন RAG সিস্টেমের কাছে অনুভূত হোক। Qdrant আমাকে ভেক্টরগুলো সংরক্ষণ করতে দেয় পে্লোড মেটাডেটাসমেত যেমন উত্স ফাইল, সেকশন শিরোনাম, ডকুমেন্ট সংস্করণ, এবং অনুমতি। এতে পুনরুদ্ধার পরিদর্শন করা সহজ হয় এবং উদাহরণটি ফিল্টারিং, উদ্ধৃতি, এবং ভবিষ্যতের স্থায়ী বা সার্ভার-ভিত্তিক বাস্তবায়নের প্রস্তুত করে।

FAISS ভেক্টর সাদৃশ্য অনুসন্ধান প্রদর্শনের জন্য চমৎকার। Qdrant ছোট কিন্তু প্রোডাকশনমুখী RAG পুনরুদ্ধার স্তর প্রদর্শনের জন্য ভালো।

কিছু বাস্তবসম্মত বিকল্প:

| ভেক্টর সংরক্ষণ / অনুসন্ধান স্তর | কখন আমি বিবেচনা করব |
| --- | --- |
| Qdrant | স্থানীয় প্রোটোটাইপ, মেটাডেটা ফিল্টারিং, প্রোডাকশন-বন্ধুত্বপূর্ণ ভেক্টর অনুসন্ধান এবং সরল পাইথন কর্মপ্রবাহ। |
| Chroma | দ্রুত স্থানীয় RAG পরীক্ষা এবং নোটবুক যেখানে সরলতা সবচেয়ে গুরুত্বপূর্ণ। |
| FAISS | হালকা স্থানীয় ভেক্টর অনুসন্ধান যখন শুধুমাত্র সাদৃশ্য অনুসন্ধান দরকার এবং মেটাডেটা আলাদাভাবে পরিচালনা করা যায়। |
| Milvus | বড়-স্কেল ওপেন-সোর্স ভেক্টর অনুসন্ধান যখন দল নিবেদিত ভেক্টর ডাটাবেস পরিচালনার জন্য প্রস্তুত। |
| Weaviate | ভেক্টর অনুসন্ধান স্কিমা, মেটাডেটা, হাইব্রিড অনুসন্ধান, এবং পরিচালিত বা স্ব-হোস্টেড ডিপ্লয়মেন্ট বিকল্প সহ। |
| Azure AI Search | এন্টারপ্রাইজ RAG Azure-তে যখন আমি কীওয়ার্ড অনুসন্ধান, ভেক্টর অনুসন্ধান, হাইব্রিড পুনরুদ্ধার, সেমান্টিক র‌্যাঙ্কিং, ফিল্টারিং, সুরক্ষা, এবং পরিচালিত অপারেশন একসাথে চাই। |
| PostgreSQL + pgvector | যাদের ইতিমধ্যেই PostgreSQL ব্যবহার করে তারা যখন অ্যাপ্লিকেশন ডেটার কাছাকাছি ভেক্টর অনুসন্ধান চায়। |

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

তারপর পয়েন্টগুলো ঢোকান:

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

আমার রান-এ, কালেকশনে ৮টি ভেক্টর ঢোকানো হয়েছিল।

এখান থেকেই RAG সিস্টেম পরিদর্শনযোগ্য হতে শুরু করে। ভেক্টর ডাটাবেস শুধু ভেক্টর রাখে না; এটি প্রমাণ টেক্সট এবং উদ্ধৃতির জন্য প্রয়োজনীয় মেটাডেটাও রাখে।

## ৭. প্রার্থী চাংক পুনরুদ্ধার করুন

এখন আমরা প্রশ্ন করি এবং প্রার্থী চাংকগুলো পুনরুদ্ধার করি।

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

এই পর্যায়ে, আমি উত্তর তৈরির আগে পুনরুদ্ধারকৃত চাংকগুলি প্রিন্ট করি। এটি গুরুত্বপূর্ণ। যদি পুনরুদ্ধার ভুল হয়, তবে উত্তর তৈরি শুধুমাত্র বার্তা দেবে মসৃণ টেক্সটের আড়ালে।

## ৮. হালকা ওজনের পুনর্বিন্যাসক যুক্ত করুন

যখন আমি প্রথমবার পুনরুদ্ধার পথ পরীক্ষা করেছিলাম, ভেক্টর সাদৃশ্যই সম্পর্কিত নীতি বিষয়বস্তু খুঁজে পেত, কিন্তু সবচেয়ে সুনির্দিষ্ট সেকশন সবসময়ই শীর্ষে থাকত না।

তাই আমি একটি ছোট স্থানীয় পুনর্বিন্যাসক যুক্ত করলাম। এটি অতিরিক্ত গুরুত্ব দেয় যখন প্রশ্নের শব্দগুলো সেকশন শিরোনাম এবং কন্টেন্টের সাথে ওভারল্যাপ করে।

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

পুনর্বিন্যাসের পর শীর্ষ ফলাফল হলো:

```text
school_ai_policy.md / Final Assignments
```

এটি পরীক্ষার প্রশ্নের জন্য প্রত্যাশিত সেকশন ছিল।

এটাই প্রথম বাস্তবায়নের সবচেয়ে উপকারী শিক্ষা। এমনকি একটি ছোট স্থানীয় উদাহরণতেই, যখন আমি ভেক্টর সাদৃশ্যের সাথে অন্য সংকেত যোগ করলাম তখন পুনরুদ্ধারের মান উন্নত হলো।

## ৯. একটি স্থির স্থানীয় উত্তর তৈরি করুন

ডিফল্ট পথে, আমি একটি স্বচ্ছ স্থানীয় উত্তর রচয়িতা ব্যবহার করি LLM এর পরিবর্তে।

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

এটি চূড়ান্ত পণ্য উত্তর জেনারেটর হিসেবে নয়। এটি একটি ডিবাগিং টুল। এটি প্রমাণ করে যে পুনরুদ্ধার, মেটাডেটা, এবং উদ্ধৃতি ওয়্যারিং কাজ করে মডেল পরিবর্তন যোগ করার আগে।

## ১০. Ollama এবং Phi-4-mini দিয়ে স্থানীয় উত্তর তৈরি করুন

একবার পুনরুদ্ধার কাজ করলে, নোটবুক শুধু চূড়ান্ত উত্তর ধাপ Ollama এবং `phi4-mini:3.8b` দিয়ে প্রতিস্থাপন করতে পারে।

> [!NOTE]
> Ollama শুধুমাত্র চূড়ান্ত উত্তর-জেনারেশন ধাপ প্রতিস্থাপন করা উচিত। ডকুমেন্ট লোডিং, চাংকিং, ভেক্টর স্টোরেজ, পুনরুদ্ধার, পুনর্বিন্যাস এবং উদ্ধৃতি ওয়্যারিং একই থাকা উচিত।

প্রথমে, নোটবুক পুনরুদ্ধৃত চাংক থেকে একটি প্রমাণ প্রম্পট তৈরি করে:

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

এই টিউটোরিয়ালের জন্য, আমি Ollama মাধ্যমে Microsoft এর Phi-4-mini পরিবারকে ডিফল্ট স্থানীয় জেনারেশন অপশন হিসেবে সুপারিশ করি। Ollama তে আমার পরীক্ষিত মডেলের নাম হল:

```powershell
ollama pull phi4-mini:3.8b
```

আপনি দ্রুত চেক করতে পারেন যে মডেলটি উপলব্ধ:

```powershell
ollama list
```

তারপর এই ভেরিয়েবলগুলো সেট করুন:

```powershell
Copy-Item .env.example .env
```

`.env` খুলুন এবং সিরিজ ২ Ollama মান আনকমেন্ট করুন:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

নোটবুক রিপোজিটরি রুট থেকে `python-dotenv` দিয়ে `.env` লোড করে, তারপর একই প্রমাণ প্রম্পট Ollama এর স্থানীয় `/api/chat` এন্ডপয়েন্টে স্ট্রিমিং বন্ধ রেখে পাঠায়। Ollama চালু না থাকলে বা `SERIES2_OLLAMA_MODEL` অনুপস্থিত থাকলে এই ট্র্যাকটি বাদ দেয়া হয়।

> [!NOTE]
> এই যন্ত্রে, `phi4-mini:3.8b` প্রায় ২.৪৯GB মডেল ফাইল ডাউনলোড করেছিল। ইনফারেন্স চলাকালীন, Ollama রিপোর্ট করেছিল ৩.৩GB লোড করা মডেল সাইজ এবং ব্যবহার করেছিল RTX 3060 ল্যাপটপ GPU।

এটি টিউটোরিয়ালকে দুটি স্তরে নিয়ে আসে:

1. শুধুমাত্র CPU-ভিত্তিক স্থায়ী উত্তর রচয়িতা।
2. Ollama এবং Phi-4-mini দিয়ে স্থানীয় উত্তর উৎপাদন।

পুনরুদ্ধার পাইপলাইন দুটিতেই একই থাকে।

## ১১. যাচাই ফলাফল

আমি স্থানীয়ভাবে Windows এ Python 3.12.6 দিয়ে নোটবুক চালিয়েছি।

ইনস্টল করা প্যাকেজসমূহ:

| প্যাকেজ | সংস্করণ |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

নোটবুক এক্সিকিউশন:

- নোটবুক: `notebooks/series-2-open-source-rag.ipynb`
- এক্সিকিউশন ফলাফল: `nbclient` দিয়ে সফল
- লোড করা ডকুমেন্ট: ২
- তৈরিকৃত চাংক: ৮
- Qdrant কালেকশন: `school_policy_local`
- ঢোকানো ভেক্টর: ৮
- এমবেডিং মডেল: `BAAI/bge-small-en-v1.5`
- এমবেডিং আকার: ৩৮৪
- পুনরুদ্ধার প্রশ্ন: "কি আমি আমার চূড়ান্ত অ্যাসাইনমেন্টের জন্য জেনারেটিভ AI ব্যবহার করতে পারি?"
- পুনরায় র‌্যাঙ্কিং পথ: হালকা স্থানীয় শ্রুতিমধুর পুনরায় র‌্যাঙ্কিং
- পুনরায় র‌্যাঙ্কিংয়ের পর সর্বোচ্চ পুনরুদ্ধারকৃত উৎস: `school_ai_policy.md`
- পুনরায় র‌্যাঙ্কিংয়ের পর সর্বোচ্চ পুনরদ্ধারকৃত অংশ: `Final Assignments`
- ডিফল্ট উত্তর পথ: স্থানীয় স্বচ্ছ উত্তর সংযোজক
- Ollama জেনারেশন পথ: `phi4-mini:3.8b` দ্বারা সম্পন্ন
- Ollama মডেল ফাইলের আকার: ডিস্কে ২.৪৯ জিবি
- Ollama লোড করা মডেলের আকার: `ollama ps` দ্বারা রিপোর্ট করা ৩.৩ জিবি
- GPU অফলোড: `ollama ps` দ্বারা ১০০% GPU রিপোর্ট করা হয়েছে
- জেনারেশনের পর GPU মেমরি পর্যবেক্ষণ: RTX ৩০৬০ ল্যাপটপ GPU তে ৬ জিবির মধ্যে প্রায় ৩.৫ জিবি ব্যবহার হয়েছে
- ক্যাশড FastEmbed মডেল এবং Ollama জেনারেশন সক্ষম করে নোটবুক এক্সিকিউশন: যাচাইকরণ স্ক্রিপ্টের মাধ্যমে প্রায় ৩৪ সেকেন্ডে সফল হয়েছে

Ollama-উত্পাদিত উত্তর ছিল:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

আমি এই উত্তরের পাকা বলা উচিত নয়। এটি সঠিক প্রমাণ থেকে উত্তর দেয়, তবে চূড়ান্ত উৎস লাইনটি দৃঢ়তাসূচক উদ্ধৃত ফরম্যাটের তুলনায় কম স্পষ্ট। এটি টিউটোরিয়ালে দেখানো দরকার কারণ এটি পরবর্তী প্রকৌশল প্রশ্নটি স্পষ্ট করে তোলে: শুধু পুনরুদ্ধার নয়, উত্তর উত্পাদনও মূল্যায়ন দরকার।

যা আমি যাচাই করার সময় শিখেছি মূল বিষয় হচ্ছে উত্তর উৎপাদনের আগেই পুনরুদ্ধারের গুণমান পরীক্ষা করা উচিত। এমবেডিং ফলাফল ইতিমধ্যে উপকারী ছিল, এবং হালকা পুনরায় র্যাঙ্কার প্রত্যাশিত নীতিমালা অংশ নির্ভরযোগ্যভাবে প্রথমে দেখিয়েছিল। এটি ঠিক সেই ছোট সিস্টেম আচরণ যা আমি টিউটোরিয়ালে প্রদর্শন করতে চাই, লুকানো নয়।

## ১২. পরবর্তী কী আসছে

পরবর্তী উন্নতি হল এই স্থানীয় সেটআপের তুলনা পরিচালিত Azure সংস্করণের সঙ্গে একই স্কুল নীতি সহকারী স্কেনারিয়োর। স্কেনারিও নির্দিষ্ট রেখে রাখা ট্রেডঅফগুলি আরও স্পষ্ট দেখা সহজ করবে: সেটআপ জটিলতা, পুনরুদ্ধার নিয়ন্ত্রণ, পরিচয় সংহতি, অপারেশনাল মালিকানা, এবং খরচ।

## ১৩. রেফারেন্সসমূহ

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

পূর্ববর্তী: [সিরিজ ১](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা শুদ্ধতার জন্য চেষ্টা করি, অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার স্বভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে প্রয়োজনীয় ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়বদ্ধ নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->