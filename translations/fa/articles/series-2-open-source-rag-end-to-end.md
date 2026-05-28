# آموزش هوش مصنوعی برای پاسخ به سوالات بر اساس اسناد شما
## سری ۲: ساخت سیستم RAG متن‌باز محلی از ابتدا تا انتها

![روند آموزشی سیستم RAG متن‌باز محلی](../../../assets/images/series-2-local-rag.svg)

> این مقاله بحث معماری سری ۱ را به یک آموزش قابل اجرا برای سیستم RAG محلی تبدیل می‌کند. هدف این است که ابتدا کل جریان کاری را با داده نمونه، بدون حساب ابری و بدون کلیدهای مخفی بسازیم، سپس از این پایه‌کار عملکردی برای اتخاذ تصمیمات بهتر معماری در آینده استفاده کنیم.

سیستمی که خواهیم ساخت، یک دستیار سیاست مدرسه کوچک است. من دو سند محلی به فرمت Markdown را به عنوان پایگاه دانش استفاده می‌کنم و سپس کل روند RAG را طی می‌کنم: بخش‌بندی، جاسازی‌های محلی، ذخیره وکتورها در Qdrant، بازیابی، رتبه‌بندی مجدد، ترکیب پاسخ آگاه به منبع، و تولید محلی اختیاری با Ollama و Phi-4-mini.

ناوبری سری: [صفحه اصلی مخزن](../README.md) | قبلی: [سری 1 - RAG، Azure در مقابل جایگزین‌های متن‌باز و زمان مناسب تنظیم دقیق](./series-1-rag-azure-open-source-fine-tuning.md)

دفترچه یادداشت: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | پیش‌نیازها: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> این بهترین نقطه شروع است اگر می‌خواهید جریان کاری RAG را قبل از ایجاد منابع ابری بفهمید. مسیر پیش‌فرض به صورت محلی با جاسازی‌های دوستانه CPU و بدون کلیدهای مخفی اجرا می‌شود.

## 1. آنچه می‌سازیم

در آموزش ۲۰۲۳، از Azure شروع کردم زیرا هدف نشان دادن نحوه پاسخ به سوالات از اسناد PDF با Azure AI Search و Azure OpenAI بود.

برای این سری ۲۰۲۶، می‌خواهم یک لایه پایین‌تر شروع کنم.

قبل از استفاده از سرویس‌های مدیریت شده، می‌خواهم یک سیستم RAG کوچک محلی ایجاد کنم و هر مرحله را قابل مشاهده سازم: بارگذاری اسناد، بخش‌بندی متن، ذخیره وکتورها، بازیابی شواهد، رتبه‌بندی مجدد نتایج و ارائه پاسخ آگاه به منبع.

سناریوی نمونه، دستیار سیاست مدرسه است. کاربر می‌پرسد:

```text
Can I use generative AI for my final assignment?
```

سیستم نباید از حافظه مدل عمومی پاسخ دهد. باید بخش سیاست مرتبط را بازیابی کند و پاسخ را از آن شواهد بدهد.

نسخه اجرایی کامل در [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) است. کد زیر مراحل اصلی را نشان می‌دهد تا مقاله به صورت آموزش خوانده شود.

## 2. نصب وابستگی‌های محلی

یک محیط مجازی بسازید و پیش‌نیازهای سری ۲ را نصب کنید:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

نسخه اول از حالت محلی Qdrant و FastEmbed استفاده می‌کند. کلاینت پایتون Qdrant حالت محلی در حافظه با `QdrantClient(":memory:")` را پشتیبانی می‌کند که برای آموزش‌های محلی و بررسی CI مفید است. FastEmbed به ما یک مدل جاسازی واقعی محلی می‌دهد بدون نیاز به کلید API ابری.

فایل پیش‌نیازها همچنین شامل `python-dotenv` است چون دفترچه یادداشت می‌تواند به صورت اختیاری نام مدل Ollama را از `.env` بخواند. برای این آموزش محلی نیازی به کلید Azure OpenAI یا OpenAI نیست.

## 3. بارگذاری اسناد نمونه

مجموعه نمونه عمداً کوچک است:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

در دفترچه یادداشت، همه فایل‌های Markdown را از `sample_data/` بارگذاری می‌کنم:

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

وقتی دفترچه یادداشت را اجرا کردم، ۲ سند بارگیری شد. این مقدار آن‌قدر کوچک است که بتوان آن را به صورت دستی بررسی کرد، که وقتی اولین نسخه یک خط لوله RAG را می‌سازید، مفید است.

## 4. بخش‌بندی بر اساس سرفصل‌های Markdown

گام بعدی تقسیم اسناد به بخش‌هاست.

برای این آموزش از سرفصل‌های Markdown به عنوان سیگنال ساختار استفاده می‌کنم. عنوان سند از `#` می‌آید و هر بخش از `##`.

> [!NOTE]
> بخش‌بندی یکسان برای همه نیست. در این آموزش، من از سرفصل‌های Markdown استفاده می‌کنم چون اسناد نمونه ساختار واضح `#` و `##` دارند. برای PDF، اسناد Word، اسلایدها، تیکت‌ها یا صفحات وب، استراتژی بهتر ممکن است از مرز صفحات، اطلاعات چینش، بخش‌های معنایی، محدودیت توکن، جداول یا متادیتا استفاده کند. نکته مهم این است که استراتژی بخش‌بندی‌ای را برگزینید که معنا و ردپای منبع اسناد شما را حفظ کند.

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

سپس این را به هر سند اعمال می‌کنم:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

این در اجرای محلی من ۸ بخش ایجاد کرد.

آنچه از این مرحله خوشم آمد این بود که متادیتا قبلاً مفید است. هر بخش `source`، `sectionHeading`، `documentVersion` و به صورت پلاسیه‌هولدر `permissions` را می‌داند. حتی در یک آموزش کوچک، این کار استنادها و بازیابی آگاه به مجوز را آسان‌تر برای استدلال می‌کند.

## 5. ایجاد جاسازی‌های محلی

برای اولین نسخه عمومی، از `BAAI/bge-small-en-v1.5` از طریق FastEmbed استفاده می‌کنم.

این آموزش را محلی و سازگار با CPU نگه می‌دارد، اما هنوز از یک مدل جاسازی واقعی به جای تابع وکتور پلاسیه‌هولدر استفاده می‌کند. اجرای اول وزن‌های مدل را دانلود می‌کند. پس از آن، دفترچه یادداشت می‌تواند کش محلی را بازاستفاده کند.

> [!NOTE]
> من از `BAAI/bge-small-en-v1.5` استفاده می‌کنم چون یک مدل جاسازی سبک انگلیسی است که با FastEmbed و Qdrant برای آموزش محلی به خوبی کار می‌کند. وکتورهای ۳۸۴ بُعدی ایجاد می‌کند که مثال را سریع و ارزان برای اجرا در محلی نگه می‌دارد. این تنها انتخاب خوب نیست. در ۲۰۲۳ بسیاری از آموزش‌ها از مدل‌های جاسازی میزبانی شده مانند `text-embedding-ada-002` استفاده می‌کردند. امروزه گزینه‌های جدیدتری مانند OpenAI `text-embedding-3-small` و `text-embedding-3-large` میزبانی شده، و گزینه‌های متن‌باز مانند BGE، E5، MiniLM، Nomic Embed و مدل‌های چندزبانه مانند `BAAI/bge-m3` همه گزینه‌های معقول بسته به بار کاری هستند. در تولید، مدل جاسازی مناسب باید از طریق ارزیابی بازیابی بر اساس اسناد خود انتخاب شود.

برخی گزینه‌های عملی:

| خانواده مدل | زمانی که آن را مد نظر قرار می‌دهم |
| --- | --- |
| `text-embedding-ada-002` | پایه میزبانی قدیمی که در بسیاری از آموزش‌های دوره ۲۰۲۳ دیده می‌شد. آن را به عنوان پیش‌فرض در آموزش جدید انتخاب نمی‌کنم. |
| `text-embedding-3-small` | پیش‌فرض مدرن میزبانی شده وقتی تعادل هزینه/عملکرد قوی می‌خواهم و نیازی به جاسازی فقط محلی ندارم. |
| `text-embedding-3-large` | گزینه میزبانی شده وقتی کیفیت بازیابی از اندازه وکتور یا هزینه جاسازی مهمتر است. |
| `BAAI/bge-small-en-v1.5` | پایه سبک انگلیسی محلی برای آموزش‌ها، نمونه‌های اولیه و آزمایش‌های سازگار با CPU. |
| `BAAI/bge-base-en-v1.5` یا `BAAI/bge-large-en-v1.5` | مدل‌های بزرگ‌تر محلی انگلیسی وقتی کیفیت بازیابی بهتر می‌خواهم و می‌توانم محاسبات بیشتری انجام دهم. |
| `BAAI/bge-m3` | بازیابی چندزبانه یا متن بلندتر، مخصوصاً وقتی اسناد فقط انگلیسی نیستند. |
| `sentence-transformers/all-MiniLM-L6-v2` | پایه بسیار کوچک و سریع جستجوی معنایی. وقتی سرعت و سادگی بیشترین اهمیت را دارند، مفید است. |
| `nomic-embed-text-v1.5` | گزینه جاسازی محلی متن‌باز که ارزش آزمایش برای متونی با زمینه طولانی یا طراحی قابل حمل دارد. |

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

سپس به هر بخش یک جاسازی داده می‌شود:

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

## 6. ذخیره وکتورها در حالت محلی Qdrant

اکنون یک کالکشن Qdrant در حافظه ایجاد می‌کنیم و بخش‌ها را به همراه متادیتای پِیلود وارد می‌کنیم.

> [!NOTE]
> در آموزش ۲۰۲۳، من از FAISS استفاده کردم چون روشی ساده و محبوب برای نمایش جستجوی شباهت وکتور محلی با LangChain بود. FAISS هنوز برای آزمایش‌های سریع محلی مفید است. در نسخه ۲۰۲۶، من از Qdrant استفاده می‌کنم چون می‌خواهم آموزش بیشتر شبیه سیستم RAG تولیدی باشد. Qdrant اجازه می‌دهد وکتورها را همراه با متادیتای پِیلود مانند فایل منبع، سرفصل بخش، نسخه سند و مجوزها ذخیره کنم. این کار بازیابی را آسان‌تر برای بررسی می‌کند و نمونه را برای فیلتر کردن، استناد‌ها و استقرار پایدار یا سرور آماده می‌کند.

FAISS عالی است برای نمایش جستجوی شباهت وکتور. Qdrant بهتر است برای نمایش لایه بازیابی RAG کوچک اما با شکل تولیدی.

برخی گزینه‌های عملی:

| فروشگاه/لایه جستجوی وکتور | زمانی که مد نظر دارم |
| --- | --- |
| Qdrant | نمونه‌های اولیه محلی، فیلتر متادیتا، جستجوی وکتور مناسب تولید و جریان کاری ساده پایتون. |
| Chroma | آزمایش‌های سریع RAG محلی و دفترچه یادداشت‌هایی که سادگی بیشترین اهمیت را دارند. |
| FAISS | جستجوی وکتور محلی سبک وقتی فقط به جستجوی شباهت نیاز دارم و می‌توانم متادیتا را جداگانه مدیریت کنم. |
| Milvus | جستجوی وکتور متن‌باز بزرگ‌تر وقتی تیم آماده است یک پایگاه داده وکتور اختصاصی را مدیریت کند. |
| Weaviate | جستجوی وکتور با اسکیما، متادیتا، جستجوی ترکیبی و گزینه‌های استقرار مدیریت شده یا خودمیزبان. |
| Azure AI Search | RAG سازمانی در Azure وقتی جستجوی کلمه کلیدی، جستجوی وکتور، بازیابی ترکیبی، رتبه‌بندی معنایی، فیلتر، امنیت و عملیات مدیریت شده را در یک لایه جستجو می‌خواهم. |
| PostgreSQL + pgvector | تیم‌هایی که از PostgreSQL استفاده می‌کنند و می‌خواهند جستجوی وکتور نزدیک به داده‌های برنامه داشته باشند. |

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

سپس نقاط را درج می‌کنیم:

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

در اجرای من، کالکشن ۸ وکتور درج کرد.

اینجا جایی است که سیستم RAG شروع به قابل بررسی شدن می‌کند. پایگاه داده وکتور فقط وکتورها را ذخیره نمی‌کند؛ بلکه متن شواهد و متادیتای لازم برای استناد را ذخیره می‌کند.

## 7. بازیابی بخش‌های کاندید

اکنون سوال می‌پرسیم و بخش‌های کاندید را بازیابی می‌کنیم.

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

در این مرحله، بخش‌های بازیابی شده را قبل از تولید پاسخ چاپ می‌کنم. این مهم است. اگر بازیابی اشتباه باشد، تولید فقط مشکل را با متن روان پشت پرده می‌کند.

## 8. افزودن رتبه‌بند سبُک

وقتی مسیر بازیابی را ابتدا تست کردم، شباهت وکتور به تنهایی محتوای سیاست مرتبط را می‌یافت، اما دقیق‌ترین بخش همیشه در بالا نبود.

پس یک رتبه‌بند کوچک محلی اضافه کردم. وقتی اصطلاحات سوال با سرفصل و محتوی بخش همپوشانی داشتند وزن بیشتری می‌دهد.

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

بعد از رتبه‌بندی مجدد، نتیجه برتر شد:

```text
school_ai_policy.md / Final Assignments
```

این همان بخش مورد انتظار برای سوال آزمایشی بود.

این مفیدترین درس از اولین پیاده‌سازی بود. حتی در یک مثال کوچک محلی، کیفیت بازیابی وقتی شباهت وکتور را با سیگنال دیگر ترکیب کردم بهبود یافت.

## 9. ترکیب پاسخ محلی مبتنی بر شواهد

برای مسیر پیش‌فرض، از یک ترکیب‌کننده پاسخ شفاف محلی به جای مدل زبان بزرگ استفاده می‌کنم.

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

این قرار نیست یک تولید کننده پاسخ نهایی باشد. این یک ابزار اشکال‌زدایی است. اثبات می‌کند که بازیابی، متادیتا و اتصال استنادها پیش از افزودن متغیرهای مدل درست کار می‌کنند.

## 10. تولید پاسخ محلی با Ollama و Phi-4-mini

وقتی بازیابی درست کار کرد، دفترچه یادداشت می‌تواند فقط مرحله نهایی تولید پاسخ را با Ollama و `phi4-mini:3.8b` جایگزین کند.

> [!NOTE]
> Ollama فقط باید مرحله تولید پاسخ نهایی را جایگزین کند. بارگذاری سند، بخش‌بندی، ذخیره وکتور، بازیابی، رتبه‌بندی مجدد و اتصال استنادها باید همان بمانند.

ابتدا دفترچه یادداشت پرامپت شواهد را از بخش‌های بازیابی شده می‌سازد:

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

برای این آموزش، خانواده Phi-4-mini مایکروسافت از طریق Ollama را به عنوان گزینه تولید محلی پیش‌فرض توصیه می‌کنم. در Ollama، نام مدلی که تست کردم:

```powershell
ollama pull phi4-mini:3.8b
```

می‌توانید سریع چک کنید که مدل در دسترس است:

```powershell
ollama list
```

سپس این متغیرها را تنظیم کنید:

```powershell
Copy-Item .env.example .env
```

فایل `.env` را باز کرده و مقادیر Ollama سری ۲ را از کامنت خارج کنید:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

دفترچه یادداشت `.env` را از ریشه مخزن با `python-dotenv` بارگذاری می‌کند، سپس همان پرامپت شواهد را به نقطه پایانی محلی `/api/chat` Ollama بدون استریم ارسال می‌کند. اگر Ollama اجرا نشود یا `SERIES2_OLLAMA_MODEL` موجود نباشد، این مسیر رد می‌شود.

> [!NOTE]
> روی این ماشین، `phi4-mini:3.8b` حدود ۲.۴۹ گیگابایت فایل مدل دانلود کرد. در حین استنتاج، Ollama سایز مدل بارگذاری شده ۳.۳ گیگابایت گزارش داد و از GPU لپ‌تاپ RTX 3060 استفاده کرد.

این آموزش دو سطح ارائه می‌دهد:

1. ترکیب‌کننده پاسخ قابل تعیین فقط با CPU.
2. تولید پاسخ محلی با Ollama و Phi-4-mini.

خط لوله بازیابی در هر دو همان باقی می‌ماند.

## 11. نتیجه تأیید

دفترچه یادداشت را به صورت محلی در ویندوز با Python 3.12.6 اجرا کردم.

پکیج‌های نصب شده:

| پکیج | نسخه |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

اجرای دفترچه یادداشت:

- دفترچه: `notebooks/series-2-open-source-rag.ipynb`
- نتیجه اجرا: با `nbclient` موفقیت‌آمیز
- اسناد بارگذاری شده: ۲
- بخش‌های ایجاد شده: ۸
- کالکشن Qdrant: `school_policy_local`
- وکتورهای درج شده: ۸
- مدل جاسازی: `BAAI/bge-small-en-v1.5`
- اندازه جاسازی: ۳۸۴
- سوال بازیابی: «آیا می‌توانم از هوش مصنوعی مولد برای تکلیف نهایی خود استفاده کنم؟»
- مسیر رتبه‌بندی مجدد: رتبه‌بندی محلی سبک واژگانی
- بهترین منبع بازیابی شده پس از رتبه‌بندی مجدد: `school_ai_policy.md`
- بهترین بخش بازیابی شده پس از رتبه‌بندی مجدد: `تکالیف نهایی`
- مسیر پاسخ پیش‌فرض: ترکیب‌کننده پاسخ شفاف محلی
- مسیر تولید اولاما: تکمیل شده با `phi4-mini:3.8b`
- حجم فایل مدل اولاما: ۲.۴۹ گیگابایت روی دیسک
- حجم مدل بارگذاری شده اولاما: ۳.۳ گیگابایت گزارش‌شده توسط `ollama ps`
- تخلیه GPU: ۱۰۰٪ GPU گزارش‌شده توسط `ollama ps`
- حافظه GPU مشاهده شده پس از تولید: حدود ۳.۵ گیگابایت از ۶ گیگابایت استفاده‌شده روی RTX 3060 لپ‌تاپ GPU
- اجرای نوت‌بوک با مدل FastEmbed کش‌شده و تولید اولاما فعال شده: حدود ۳۴ ثانیه از طریق اسکریپت اعتبارسنجی گذشت

پاسخ تولید شده توسط اولاما این بود:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```
  
من این پاسخ را کامل نمی‌دانم. این پاسخ از منبع درست استفاده می‌کند، اما خط منبع نهایی دقیق‌تر از فرمت ارجاع قطعی نیست. این موضوع در آموزش مفید است چون سؤال مهندسی بعدی را واضح می‌کند: ایجاد پاسخ نیز نیاز به ارزیابی دارد، نه فقط بازیابی.

مهم‌ترین چیزی که هنگام اعتبارسنجی آموختم این است که کیفیت بازیابی باید قبل از تولید پاسخ بررسی شود. نتیجه تعبیه قبلاً مفید بود و رتبه‌بندی‌کننده سبک باعث شد بخش سیاست مورد انتظار به طور قابل اطمینانی ابتدا ظاهر شود. این دقیقاً همان نوع رفتار کوچک سیستم است که می‌خواهم آموزش آن را نشان دهد نه پنهان کند.

## ۱۲. گام بعدی چیست

بهبود بعدی مقایسه این تنظیمات محلی با نسخه مدیریت‌شده Azure برای همان سناریوی دستیار سیاست مدرسه است. ثابت نگه‌داشتن سناریو باید باعث شود مبادلات راحت‌تر دیده شوند: پیچیدگی راه‌اندازی، کنترل‌های بازیابی، یکپارچه‌سازی هویت، مالکیت عملیاتی و هزینه.

## ۱۳. مراجع

- [شروع سریع کلاینت Qdrant پایتون](https://python-client.qdrant.tech/quickstart.html)
- [مخزن کلاینت Qdrant در گیت‌هاب](https://github.com/qdrant/qdrant-client)
- [مدل‌های پشتیبانی‌شده توسط FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [راهنمای تعبیه‌های OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [کارت مدل BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [کارت مدل BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [کارت مدل sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [صفحه مدل Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [مستندات Ollama برای ویندوز](https://docs.ollama.com/windows)
- [مستندات API پخش Ollama](https://docs.ollama.com/api/streaming)
- [کارت مدل Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [مروری بر LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [مقدمه‌ای بر RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

قبلی: [سری ۱](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان مادری خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما در قبال هرگونه سوء تفاهم یا برداشت نادرست ناشی از استفاده از این ترجمه مسئولیتی نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->