# اپنے دستاویزات کی بنیاد پر سوالات کا جواب دینے کے لیے AI کو تربیت دیں
## سلسلہ 2: ایک مقامی اوپن سورس RAG سسٹم کی ابتدا سے آخر تک تعمیر کریں

![مقامی اوپن سورس RAG ٹیوٹوریل پائپ لائن](../../../assets/images/series-2-local-rag.svg)

> یہ مضمون سلسلہ 1 کی فن تعمیر پر بات چیت کو ایک چلانے کے قابل مقامی RAG ٹیوٹوریل میں تبدیل کرتا ہے۔ مقصد پہلے نمونہ ڈیٹا کے ساتھ مکمل ورک فلو بنانا ہے، بغیر کسی کلاؤڈ اکاؤنٹ اور راز کی معلومات کے، پھر اس کام کرنے والے بیس لائن کو بہتر فن تعمیر کے فیصلے کرنے کے لیے استعمال کرنا ہے۔

ہم جو نظام بنائیں گے وہ ایک چھوٹے اسکول کی پالیسی اسسٹنٹ ہے۔ میں دو مقامی مارک ڈاؤن دستاویزات کو علم کے ذخیرے کے طور پر استعمال کرتا ہوں، پھر پورے RAG پائپ لائن کے ذریعے چلتا ہوں: چنکنگ، مقامی ایمبیڈنگز، Qdrant ویکٹر اسٹوریج، بازیافت، ریرینکنگ، ماخذ سے آگاہ جواب کی ترکیب، اور اختیاری طور پر Ollama اور Phi-4-mini کے ساتھ مقامی جنریشن۔

سیریز نیویگیشن: [ریپوزیٹری ہوم](../README.md) | پچھلا: [سیریز 1 - RAG, Azure بمقابلہ اوپن سورس متبادلات، اور کب فائن ٹیوننگ معنی رکھتی ہے](./series-1-rag-azure-open-source-fine-tuning.md)

نوٹ بک: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | ضروریات: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> اگر آپ کلاؤڈ وسائل بنانے سے پہلے RAG پائپ لائن کو سمجھنا چاہتے ہیں تو یہ سب سے بہترین نقطہ آغاز ہے۔ ڈیفالٹ راہ مقامی طور پر CPU فرینڈلی ایمبیڈنگز اور بغیر راز کی معلومات کے چلتی ہے۔

## 1. ہم کیا بنا رہے ہیں

2023 کے ٹیوٹوریل میں، میں Azure سے شروع کیا کیونکہ مقصد یہ دکھانا تھا کہ Azure AI تلاش اور Azure OpenAI PDF دستاویزات سے سوالات کا جواب کیسے دے سکتے ہیں۔

اس 2026 کی سیریز کے لیے، میں ایک درجے نیچے سے شروع کرنا چاہتا ہوں۔

مینجڈ سروسز استعمال کرنے سے پہلے، میں ایک چھوٹا سا RAG سسٹم مقامی طور پر بنانا چاہتا ہوں اور ہر قدم کو دکھانا چاہتا ہوں: دستاویزات لوڈ کرنا، متن کو چنک کرنا، ویکٹرز کو محفوظ کرنا، شواہد بازیافت کرنا، نتائج کا دوبارہ رینک کرنا، اور ماخذ سے آگاہ جواب دینا۔

نمونہ منظر نامہ ایک اسکول کی پالیسی اسسٹنٹ ہے۔ صارف پوچھتا ہے:

```text
Can I use generative AI for my final assignment?
```

نظام عام ماڈل میموری سے جواب نہ دے۔ اسے متعلقہ پالیسی سیکشن بازیافت کرنا چاہیے اور اس شواہد سے جواب دینا چاہیے۔

مکمل چلانے کے قابل ورژن [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) میں ہے۔ نیچے دیا گیا کوڈ اہم مراحل دکھاتا ہے تاکہ مضمون بطور ٹیوٹوریل پڑھا جا سکے۔

## 2. مقامی انحصارات انسٹال کریں

ایک ورچوئل ماحول بنائیں اور سیریز 2 کی ضروریات انسٹال کریں:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

پہلا ورژن Qdrant لوکل موڈ اور FastEmbed استعمال کرتا ہے۔ Qdrant کا پائیتھن کلائنٹ ایک میموری میں لوکل موڈ کو سپورٹ کرتا ہے `QdrantClient(":memory:")` کے ساتھ، جو مقامی ٹیوٹوریلز اور CI طرز کی تصدیق کے لیے مفید ہے۔ FastEmbed ہمیں ایک حقیقی مقامی ایمبیڈنگ ماڈل دیتا ہے بغیر کلاؤڈ API کلید کی ضرورت کے۔

ضروریات کی فائل میں `python-dotenv` بھی شامل ہے کیونکہ نوٹ بک اختیاری طور پر `.env` سے Ollama ماڈل نام پڑھ سکتی ہے۔ اس مقامی ٹیوٹوریل کے لیے Azure OpenAI یا OpenAI API کی کلید کی ضرورت نہیں۔

## 3. نمونہ دستاویزات لوڈ کریں

نمونہ مواد جان بوجھ کر چھوٹا ہے:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

نوٹ بک میں، میں `sample_data/` سے تمام مارک ڈاؤن فائلیں لوڈ کرتا ہوں:

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

جب میں نے نوٹ بک چلائی، اس نے 2 دستاویزات لوڈ کیں۔ یہ اتنا چھوٹا ہے کہ دستی طور پر معائنہ کیا جا سکے، جو RAG پائپ لائن کا پہلا ورژن بنانے میں مددگار ہے۔

## 4. مارک ڈاؤن ہیڈنگز کے ذریعے چنک کریں

اگلا مرحلہ دستاویزات کو چنکس میں تقسیم کرنا ہے۔

اس ٹیوٹوریل کے لیے، میں مارک ڈاؤن ہیڈنگز کو ساختی اشارے کے طور پر استعمال کرتا ہوں۔ دستاویز کا عنوان `#` سے آتا ہے، اور ہر سیکشن کا چنک `##` سے آتا ہے۔

> [!NOTE]
> چنکنگ ہر جگہ ایک جیسی نہیں ہوتی۔ اس ٹیوٹوریل میں، میں مارک ڈاؤن ہیڈنگز استعمال کرتا ہوں کیونکہ نمونہ دستاویزات میں واضح `#` اور `##` ساخت ہے۔ PDFs، Word دستاویزات، سلائیڈز، ٹکٹیں، یا ویب صفحات کے لیے، بہتر حکمت عملی صفحہ کی حدود، لے آؤٹ معلومات، معنوی سیکشنز، ٹوکن کی حدیں، میزیں، یا میٹا ڈیٹا استعمال کر سکتی ہے۔ اہم بات یہ ہے کہ ایسی چنکنگ حکمت عملی منتخب کریں جو معنی اور ماخذ کا سراغ رکھنے کو برقرار رکھے۔

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

پھر میں اسے ہر دستاویز پر لاگو کرتا ہوں:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

میرے مقامی رن میں اس نے 8 چنک بنائے۔

جو مجھے اس مرحلے میں پسند آیا وہ یہ تھا کہ میٹا ڈیٹا پہلے سے ہی مفید تھا۔ ہر چنک اپنے `source`, `sectionHeading`, `documentVersion`, اور پلیس ہولڈر `permissions` کو جانتا ہے۔ حتیٰ کہ ایک چھوٹے سے ٹیوٹوریل میں بھی، یہ حوالہ جات اور بعد میں اجازت سے آگاہ بازیافت کو سمجھنے میں آسانی پیدا کرتا ہے۔

## 5. مقامی ایمبیڈنگز بنائیں

پہلے عوامی ورژن کے لیے، میں `BAAI/bge-small-en-v1.5` کو FastEmbed کے ذریعے استعمال کرتا ہوں۔

یہ ٹیوٹوریل کو مقامی اور CPU فرینڈلی رکھتا ہے، لیکن پھر بھی ایک حقیقی ایمبیڈنگ ماڈل استعمال کرتا ہے نہ کہ کوئی پلیس ہولڈر ویکٹر فنکشن۔ پہلی بار چلانے پر ماڈل کے ویٹس ڈاؤن لوڈ ہوتے ہیں۔ اس کے بعد نوٹ بک مقامی کیشے کو دوبارہ استعمال کر سکتی ہے۔

> [!NOTE]
> میں `BAAI/bge-small-en-v1.5` استعمال کرتا ہوں کیونکہ یہ ایک ہلکا پھلکا انگریزی ایمبیڈنگ ماڈل ہے جو FastEmbed اور Qdrant کے ساتھ مقامی ٹیوٹوریل کے لیے اچھا کام کرتا ہے۔ یہ 384 بُعدی ویکٹرز بناتا ہے، جو مقامی طور پر چلانے کے لیے مثال کو تیز اور کم خرچ رکھتا ہے۔ یہ واحد اچھا انتخاب نہیں ہے۔ 2023 میں، کئی ٹیوٹوریلز میزبانی شدہ ایمبیڈنگ ماڈلز جیسے `text-embedding-ada-002` استعمال کرتے تھے۔ آج، نئے میزبانی شدہ آپشنز جیسے OpenAI کے `text-embedding-3-small` اور `text-embedding-3-large`، اور اوپن سورس آپشنز جیسے BGE, E5, MiniLM, Nomic Embed، اور کثیر لسانی ماڈلز جیسے `BAAI/bge-m3` سب کام کے بوجھ کے مطابق معقول انتخاب ہیں۔ پیداوار میں، مناسب ایمبیڈنگ ماڈل کو اپنی دستاویزات پر بازیافت کی جانچ کے ذریعے منتخب کرنا چاہیے۔

کچھ عملی متبادلات:

| ماڈل فیملی | میں کب غور کرتا |
| --- | --- |
| `text-embedding-ada-002` | پرانا میزبانی شدہ بنیادی ماڈل جو کئی 2023 دور کے ٹیوٹوریلز میں آیا۔ آج کے نئے ٹیوٹوریل کے لیے میں اسے ڈیفالٹ نہیں منتخب کرتا۔ |
| `text-embedding-3-small` | جدید میزبانی شدہ ڈیفالٹ جب مجھے مضبوط قیمت/کارکردگی توازن چاہیے اور صرف مقامی ایمبیڈنگز کی ضرورت نہیں۔ |
| `text-embedding-3-large` | میزبانی شدہ آپشن جب بازیافت کا معیار ویکٹر سائز یا ایمبیڈنگ لاگت سے زیادہ اہم ہو۔ |
| `BAAI/bge-small-en-v1.5` | ہلکا پھلکا مقامی انگریزی بنیادی ماڈل ٹیوٹوریلز، پروٹوٹائپس، اور CPU دوستانہ تجربات کے لیے۔ |
| `BAAI/bge-base-en-v1.5` یا `BAAI/bge-large-en-v1.5` | بڑے مقامی انگریزی ماڈلز جب میں بہتر بازیافت معیار چاہتا ہوں اور زیادہ کمپیوٹ برداشت کر سکتا ہوں۔ |
| `BAAI/bge-m3` | کثیر لسانی یا طویل سیاق وسباق بازیافت، خاص طور پر جب دستاویزات صرف انگریزی نہ ہوں۔ |
| `sentence-transformers/all-MiniLM-L6-v2` | بہت چھوٹا اور تیز معنوی تلاش بنیادی ماڈل۔ جب رفتار اور سادگی سب سے زیادہ اہم ہوں تو مفید۔ |
| `nomic-embed-text-v1.5` | اوپن مقامی ایمبیڈنگ آپشن، طویل سیاق یا پورٹیبلٹی پر مبنی سیٹ اپس کے لیے قابلِ آزمائش۔ |

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

پھر ہر چنک کو ایمبیڈنگ ملتی ہے:

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

## 6. Qdrant لوکل موڈ میں ویکٹرز محفوظ کریں

اب ہم ایک میموری میں Qdrant کلیکشن بنائیں گے اور چنکس کو پیلوڈ میٹا ڈیٹا کے ساتھ داخل کریں گے۔

> [!NOTE]
> 2023 کے ٹیوٹوریل میں، میں نے FAISS استعمال کیا کیونکہ یہ LangChain کے ساتھ مقامی ویکٹر مماثلت تلاش کی مظاہرہ کرنے کا آسان اور مقبول طریقہ تھا۔ FAISS اب بھی تیز مقامی تجربات کے لیے مفید ہے۔ اس 2026 ورژن میں، میں Qdrant استعمال کرتا ہوں کیونکہ میں چاہتا ہوں کہ ٹیوٹوریل ایک پروڈکشن RAG سسٹم کے قریب محسوس ہو۔ Qdrant مجھے ویکٹرز کو ماخذ فائل، سیکشن ہیڈنگ، دستاویز ورژن، اور اجازت جیسے پیلوڈ میٹا ڈیٹا کے ساتھ محفوظ کرنے دیتا ہے۔ یہ بازیافت کو بہتر جانچنے میں آسانی دیتا ہے اور مثال کو فلٹرنگ، حوالے، اور مستقبل کے مستقل یا سرور پر مبنی تعیناتی کے لیے تیار کرتا ہے۔

FAISS ویکٹر مماثلت تلاش دکھانے کے لیے بہترین ہے۔ Qdrant ایک چھوٹے مگر پروڈکشن نما RAG بازیافت پرت دکھانے کے لیے بہتر ہے۔

کچھ عملی متبادلات:

| ویکٹر اسٹور / تلاش کی پرت | میں کب غور کروں گا |
| --- | --- |
| Qdrant | مقامی پروٹوٹائپس، میٹا ڈیٹا فلٹرنگ، پروڈکشن فرینڈلی ویکٹر تلاش، اور سادہ پائیتھن ورک فلو۔ |
| Chroma | تیز مقامی RAG تجربات اور نوٹ بکس جہاں سادگی سب سے زیادہ اہم ہو۔ |
| FAISS | ہلکا پھلکا مقامی ویکٹر تلاش جب مجھے صرف مماثلت تلاش چاہیے اور میٹا ڈیٹا کو الگ سے سنبھال سکتا ہوں۔ |
| Milvus | بڑی سطح کی اوپن سورس ویکٹر تلاش جب ٹیم ایک وقف شدہ ویکٹر ڈیٹا بیس چلانے کے لیے تیار ہو۔ |
| Weaviate | ویکٹر تلاش اسکیمہ، میٹا ڈیٹا، ہائبرڈ تلاش، اور منظم یا خود میزبانی تعیناتی کے آپشنز کے ساتھ۔ |
| Azure AI Search | Azure پر انٹرپرائز RAG جب میں چاہتا ہوں کی ورڈ تلاش، ویکٹر تلاش، ہائبرڈ بازیافت، معنوی درجہ بندی، فلٹرنگ، سیکیورٹی، اور منظم آپریشنز ایک تلاش پرت میں۔ |
| PostgreSQL + pgvector | ٹیمیں جو پہلے سے PostgreSQL استعمال کر رہی ہیں اور ڈیٹا کے قریب ویکٹر تلاش چاہتی ہیں۔ |

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

پھر پوائنٹس داخل کریں:

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

میرے رن میں، کلیکشن نے 8 ویکٹرز داخل کیے۔

یہ وہ مقام ہے جہاں RAG سسٹم دیکھنے کے قابل ہونا شروع ہوتا ہے۔ ویکٹر ڈیٹا بیس صرف ویکٹرز محفوظ نہیں کر رہا؛ یہ شواہد کے متن اور حوالہ جات کے لیے ضروری میٹا ڈیٹا بھی محفوظ کر رہا ہے۔

## 7. امیدوار چنکس بازیافت کریں

اب ہم سوال پوچھتے ہیں اور امیدوار چنکس بازیافت کرتے ہیں۔

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

اس مرحلے پر، میں جواب تیار کرنے سے پہلے بازیافت شدہ چنکس پرنٹ کرتا ہوں۔ یہ اہم ہے۔ اگر بازیافت غلط ہو، تو جنریشن صرف مسئلہ کو روانی سے چھپا دے گا۔

## 8. ہلکا پھلکا ریرینکر شامل کریں

جب میں نے پہلے بازیافت راستہ آزمایا، ویکٹر مماثلت نے متعلقہ پالیسی مواد تلاش کیا، لیکن سب سے درست سیکشن ہمیشہ اوپر نہیں تھا۔

اس لیے میں نے ایک چھوٹا مقامی ریرینکر شامل کیا۔ یہ اضافی وزن دیتا ہے جب سوال کے الفاظ سیکشن ہیڈنگ اور مواد کے ساتھ اوورلیپ کرتے ہیں۔

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

ریرینکنگ کے بعد، سب سے اوپر کا نتیجہ بن گیا:

```text
school_ai_policy.md / Final Assignments
```

یہ ٹیسٹ سوال کے لیے متوقع سیکشن تھا۔

یہ پہلے نفاذ سے سب سے زیادہ مفید سبق تھا۔ حتیٰ کہ ایک چھوٹے مقامی مثال میں بھی، جب میں نے ویکٹر مماثلت کو دوسرے اشارے کے ساتھ ملایا تو بازیافت کا معیار بہتر ہوا۔

## 9. ایک زمینی مقامی جواب ترکیب کریں

ڈیفالٹ راہ کے لیے، میں شفاف مقامی جواب کمپوزر استعمال کرتا ہوں بجائے LLM کے۔

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

یہ آخری مصنوع جواب بنانے والا نہیں ہے۔ یہ ایک ڈیبگنگ ٹول ہے۔ یہ ثابت کرتا ہے کہ بازیافت، میٹا ڈیٹا، اور حوالے کی وائرنگ ماڈل کی تبدیلی سے پہلے کام کرتی ہے۔

## 10. Ollama اور Phi-4-mini کے ساتھ مقامی جواب تیار کریں

جب بازیافت کام کر رہی ہو، تو نوٹ بک صرف آخری جواب کے مرحلے کو Ollama اور `phi4-mini:3.8b` سے تبدیل کر سکتی ہے۔

> [!NOTE]
> Ollama کو صرف آخری جواب کی تخلیق کے مرحلے سے بدلنا چاہیے۔ دستاویز لوڈنگ، چنکنگ، ویکٹر اسٹوریج، بازیافت، ریرینکنگ، اور حوالہ کی وائرنگ ویسی کی ویسی رہنی چاہیے۔

سب سے پہلے، نوٹ بک بازیافت شدہ چنکس سے ایک شواہد پریشان بناتی ہے:

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

اس ٹیوٹوریل کے لیے، میں Microsoft کی Phi-4-mini فیملی کو Ollama کے ذریعے ڈیفالٹ مقامی جنریشن آپشن کے طور پر تجویز کرتا ہوں۔ Ollama میں، جس ماڈل کو میں نے آزمایا ہے وہ ہے:

```powershell
ollama pull phi4-mini:3.8b
```

آپ جلدی چیک کر سکتے ہیں کہ ماڈل دستیاب ہے:

```powershell
ollama list
```

پھر یہ ویریبلز سیٹ کریں:

```powershell
Copy-Item .env.example .env
```

`.env` کھولیں اور سیریز 2 Ollama کی قیمتوں کی تشریح ہٹائیں:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

نوٹ بک ریپوزیٹری کی جڑ سے `python-dotenv` کے ذریعے `.env` لوڈ کرتی ہے، پھر وہی شواہد پرامپٹ Ollama کے مقامی `/api/chat` اینڈپوائنٹ کو بغیر اسٹریمنگ کے بھیجتی ہے۔ اگر Ollama چل رہا نہیں یا `SERIES2_OLLAMA_MODEL` موجود نہیں، تو یہ راستہ چھوڑ دیا جاتا ہے۔

> [!NOTE]
> اس مشین پر، `phi4-mini:3.8b` نے تقریباً 2.49GB ماڈل فائلیں ڈاؤن لوڈ کیں۔ انفرنس کے دوران، Ollama نے 3.3GB لوڈ شدہ ماڈل سائز رپورٹ کیا اور RTX 3060 لیپ ٹاپ GPU استعمال کیا۔

یہ ٹیوٹوریل کو دو سطحیں دیتا ہے:

1. صرف CPU پر فیصلہ کن جواب کمپوزر۔
2. Ollama اور Phi-4-mini کے ساتھ مقامی جواب کی تخلیق۔

دونوں میں بازیافت کی پائپ لائن ایک جیسی رہتی ہے۔

## 11. تصدیقی نتیجہ

میں نے نوٹ بک مقامی طور پر Windows پر Python 3.12.6 کے ساتھ چلائی۔

انسٹال شدہ پیکجز:

| پیکج | ورژن |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

نوٹ بک کا نفاذ:

- نوٹ بک: `notebooks/series-2-open-source-rag.ipynb`
- نفاذ کا نتیجہ: `nbclient` کے ساتھ کامیاب
- دستاویزات لوڈ کیں: 2
- چنکس بنائے: 8
- Qdrant کلیکشن: `school_policy_local`
- ویکٹرز داخل کیے: 8
- ایمبیڈنگ ماڈل: `BAAI/bge-small-en-v1.5`
- ایمبیڈنگ سائز: 384
- بازیافت کا سوال: "کیا میں اپنی آخری اسائنمنٹ کے لیے جنریٹیو AI استعمال کر سکتا ہوں؟"
- دوبارہ درجہ بندی کا راستہ: ہلکا پھلکا مقامی لسانی دوبارہ درجہ بندی
- دوبارہ درجہ بندی کے بعد سب سے اوپر بازیافت شدہ ماخذ: `school_ai_policy.md`
- دوبارہ درجہ بندی کے بعد سب سے اوپر بازیافت شدہ سیکشن: `Final Assignments`
- ڈیفالٹ جواب کا راستہ: مقامی شفاف جواب کمپوزر
- اولاما جنریشن کا راستہ: `phi4-mini:3.8b` کے ساتھ مکمل
- اولاما ماڈل فائل کا سائز: ڈسک پر 2.49GB
- اولاما لوڈ شدہ ماڈل کا سائز: `ollama ps` کے ذریعہ رپورٹ کردہ 3.3GB
- GPU آف لوڈ: `ollama ps` کے ذریعہ رپورٹ کردہ 100% GPU
- جنریشن کے بعد مشاہدہ شدہ GPU میموری: RTX 3060 لیپ ٹاپ GPU پر 6GB میں سے تقریباً 3.5GB استعمال ہوئی
- کیشڈ FastEmbed ماڈل اور اولاما جنریشن فعال کے ساتھ نوٹ بک کا عمل درآمد: تصدیقی اسکرپٹ کے ذریعے تقریباً 34 سیکنڈ میں کامیابی سے مکمل

اولاما کی طرف سے تیار کردہ جواب تھا:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

میں اس جواب کو کامل نہیں کہوں گا۔ یہ صحیح ثبوت سے جواب دیتا ہے، لیکن حتمی ماخذ کی لائن متعین حوالہ فارمیٹ کی طرح بالکل درست نہیں ہے۔ اسے ٹیوٹوریل میں دکھانا مفید ہے کیونکہ یہ اگلے انجینئرنگ سوال کو واضح کرتا ہے: جواب کی تیاری کو بھی جانچنے کی ضرورت ہے، نہ کہ صرف بازیافت کو۔

جو اصل بات میں نے اس کی تصدیق کرتے ہوئے سیکھی وہ یہ ہے کہ جواب کی تیاری سے پہلے بازیافت کے معیار کو چیک کرنا چاہیے۔ ایمبیڈنگ کا نتیجہ پہلے ہی مفید تھا، اور ہلکے پھلکے ری رینکر نے متوقع پالیسی سیکشن کو بھروسے سے پہلے ظاہر کیا۔ یہی وہ چھوٹا نظامی رویہ ہے جسے میں چاہتا ہوں کہ ٹیوٹوریل بے نقاب کرے نہ کہ چھپائے۔

## 12. آگے کیا آتا ہے

اگلی بہتری یہ ہے کہ اس مقامی سیٹ اپ کا موازنہ اسی اسکول پالیسی اسسٹنٹ منظرنامے کے ایک منظم Azure ورژن سے کیا جائے۔ منظرنامہ مستقل رکھنے سے موازنہ آسان ہو گا: سیٹ اپ کی پیچیدگی، بازیافت کے کنٹرول، شناخت کا انضمام، آپریشنل ملکیت، اور لاگت۔

## 13. حوالہ جات

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

پچھلا: [سیریز 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->