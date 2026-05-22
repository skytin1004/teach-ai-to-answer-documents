# تعليم الذكاء الاصطناعي للإجابة على الأسئلة بناءً على مستنداتك
## السلسلة 2: بناء نظام RAG مفتوح المصدر محلي من البداية إلى النهاية

![خط أنابيب درس RAG مفتوح المصدر محلي](../../../assets/images/series-2-local-rag.svg)

> يحول هذا المقال مناقشة بنية السلسلة 1 إلى درس RAG محلي قابل للتشغيل. الهدف هو بناء سير العمل الكامل أولاً ببيانات نموذجية، بدون حساب سحابي، وبدون أسرار، ثم استخدام هذا الأساس العملي لاتخاذ قرارات بنائية أفضل لاحقًا.

النظام الذي سنبنيه هو مساعد سياسة مدرسة صغير. أستخدم مستندين محليين بصيغة Markdown كقاعدة معرفة، ثم أستعرض كامل خط أنابيب RAG: التجزئة، التضمينات المحلية، تخزين المتجهات باستخدام Qdrant، الاسترجاع، إعادة الترتيب، تأليف الإجابة مع الوعي بالمصدر، والتوليد المحلي الاختياري باستخدام Ollama و Phi-4-mini.

تصفح السلسلة: [الصفحة الرئيسية للمستودع](../README.md) | السابق: [السلسلة 1 - RAG، أزور مقابل البدائل مفتوحة المصدر، ومتى يكون التخصيص الدقيق منطقيًا](./series-1-rag-azure-open-source-fine-tuning.md)

دفتر الملاحظات: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | المتطلبات: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> هذه هي نقطة الانطلاق الأفضل إذا أردت فهم خط أنابيب RAG قبل إنشاء موارد سحابية. المسار الافتراضي يعمل محليًا مع تضمينات صديقة للمعالج المركزي وبدون أسرار.

## 1. ما الذي نبنيه

في دروس عام 2023، بدأت من أزور لأن الهدف كان إظهار كيف يمكن لـ Azure AI Search و Azure OpenAI الإجابة على الأسئلة من مستندات PDF.

لهذه السلسلة لعام 2026، أريد البدء من طبقة أعمق.

قبل استخدام الخدمات المُدارة، أريد بناء نظام RAG صغير محليًا وجعل كل خطوة مرئية: تحميل المستندات، تجزئة النص، تخزين المتجهات، استرجاع الأدلة، إعادة ترتيب النتائج، وإرجاع إجابة مدعومة بالمصدر.

السيناريو النموذجي هو مساعد سياسة مدرسة. المستخدم يسأل:

```text
Can I use generative AI for my final assignment?
```

يجب ألا يجيب النظام استنادًا إلى ذاكرة النموذج العامة. يجب أن يسترجع القسم ذات الصلة من السياسة ويجيب من تلك الأدلة.

النسخة التشغيلية الكاملة موجودة في [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). يُظهر الكود أدناه الخطوات الرئيسية حتى يمكن قراءة المقالة كدرس تعليمي.

## 2. تثبيت المتطلبات المحلية

أنشئ بيئة افتراضية وقم بتثبيت متطلبات السلسلة 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

الإصدار الأول يستخدم وضع Qdrant المحلي و FastEmbed. يدعم عميل Qdrant في بايثون وضعًا محليًا في الذاكرة مع `QdrantClient(":memory:")`، وهو مفيد للدروس المحلية والتحقق بأسلوب CI. يتيح FastEmbed استخدام نموذج تضمين محلي حقيقي بدون الحاجة إلى مفتاح API سحابي.

يتضمن ملف المتطلبات أيضًا `python-dotenv` لأن دفتر الملاحظات يمكن أن يقرأ اختياريًا اسم نموذج Ollama من ملف `.env`. لا يتطلب هذا الدرس مفتاحا لـ Azure OpenAI أو OpenAI API.

## 3. تحميل المستندات النموذجية

المجموعة النموذجية صغيرة عمدًا:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

في دفتر الملاحظات، أحمل جميع ملفات Markdown من `sample_data/`:

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

عندما شغّلت دفتر الملاحظات، تم تحميل مستندين. هذا حجم صغير بما يكفي للفحص يدويًا، وهو مفيد عند بناء الإصدار الأول من خط أنابيب RAG.

## 4. التجزئة حسب عناوين Markdown

الخطوة التالية هي تقسيم المستندات إلى قطع.

لهذا الدرس، أستخدم عناوين Markdown كإشارة هيكلية. عنوان المستند يأتي من `#`، وكل قسم من `##`.

> [!NOTE]
> التجزئة ليست بحجم واحد يناسب الجميع. في هذا الدرس أستخدم عناوين Markdown لأن المستندات النموذجية تحتوي على هيكل واضح بعلامتين `#` و `##`. بالنسبة لملفات PDF، مستندات وورد، شرائح، تذاكر، أو صفحات ويب، قد تكون الاستراتيجية الأفضل باستخدام حدود الصفحات، معلومات التخطيط، الأقسام الدلالية، حدود الرموز، الجداول، أو البيانات الوصفية. المهم هو اختيار استراتيجية تجزئة تحافظ على المعنى وقابلية تتبع المصدر لمستنداتك.

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

ثم أطبقها على كل مستند:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

هذا خلق 8 قطع في تجربتي المحلية.

ما أعجبني في هذه الخطوة هو أن البيانات الوصفية مفيدة بالفعل. كل قطعة تعرف `source` و `sectionHeading` و `documentVersion` و `permissions` كعنصر نائب. حتى في درس صغير، هذا يجعل الاستشهادات والاسترجاع الواعي بالتصاريح أسهل للفهم.

## 5. إنشاء التضمينات المحلية

للنسخة العامة الأولى، أستخدم `BAAI/bge-small-en-v1.5` عبر FastEmbed.

هذا يحافظ على الدرس محليًا وصديقًا للمعالج المركزي، ولكنه لا يزال يستخدم نموذج تضمين حقيقي بدلاً من دالة متجه وهمية. في التشغيل الأول، يتم تنزيل أوزان النموذج. بعد ذلك، يمكن إعادة استخدام الكاش المحلي في دفتر الملاحظات.

> [!NOTE]
> أستخدم `BAAI/bge-small-en-v1.5` لأنه نموذج تضمين خفيف الوزن للغة الإنجليزية يعمل جيدًا مع FastEmbed وQdrant لدروس محلية. ينتج متجهات ذات 384 بُعدًا، مما يجعل المثال سريع وقليل التكلفة للتشغيل محليًا. هذا ليس الخيار الوحيد الجيد. في 2023، العديد من الدروس استخدمت نماذج مضيفة مثل `text-embedding-ada-002`. اليوم، الخيارات المضيفة الأحدث مثل OpenAI `text-embedding-3-small` و `text-embedding-3-large` والخيارات مفتوحة المصدر مثل BGE و E5 و MiniLM و Nomic Embed والنماذج متعددة اللغات مثل `BAAI/bge-m3` كلها خيارات معقولة حسب عبء العمل. في الإنتاج، يجب اختيار نموذج التضمين الصحيح من خلال تقييم الاسترجاع على مستنداتك الخاصة.

بعض البدائل العملية:

| عائلة النموذج | متى سأعتبره |
| --- | --- |
| `text-embedding-ada-002` | الأساس المضيف الأقدم الذي ظهر في العديد من دروس 2023. لن أختاره كخيار افتراضي لدرس جديد اليوم. |
| `text-embedding-3-small` | الخيار المضيف الحديث الافتراضي عندما أريد توازنًا قويًا بين التكلفة والأداء ولا أحتاج تضمينات محلية فقط. |
| `text-embedding-3-large` | خيار مضيف عندما تكون جودة الاسترجاع أهم من حجم المتجهات أو تكلفة التضمين. |
| `BAAI/bge-small-en-v1.5` | نموذج إنجليزي محلي خفيف الوزن للدروس، النماذج الأولية، والتجارب الصديقة للمعالج المركزي. |
| `BAAI/bge-base-en-v1.5` أو `BAAI/bge-large-en-v1.5` | نماذج إنجليزية محلية أكبر عندما أريد جودة استرجاع أفضل ويمكنني تحمل تكلفة حساب أعلى. |
| `BAAI/bge-m3` | استرجاع متعدد اللغات أو للسياقات الأطول، خاصة إذا لم تكن المستندات إنجليزية فقط. |
| `sentence-transformers/all-MiniLM-L6-v2` | نموذج بحث دلالي صغير وسريع جدًا. مفيد عندما تكون السرعة والبساطة أولوية. |
| `nomic-embed-text-v1.5` | خيار تضمين محلي مفتوح يستحق الاختبار للسياقات الأطول أو الإعدادات التي تركز على قابلية النقل. |

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

ثم يحصل كل جزء على تضمين:

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

## 6. تخزين المتجهات في وضع Qdrant المحلي

الآن ننشئ مجموعة Qdrant في الذاكرة وندرج القطع مع بيانات وصفية في الحمولة.

> [!NOTE]
> في درس 2023، استخدمت FAISS لأنه كان طريقة بسيطة وشائعة لعرض بحث تشابه المتجهات المحلي مع LangChain. لا يزال FAISS مفيدًا للتجارب المحلية السريعة. في نسخة 2026 هذه، أستخدم Qdrant لأنني أريد أن يشعر الدرس بأنه أقرب إلى نظام RAG إنتاجي. يسمح Qdrant بتخزين المتجهات مع بيانات وصفية مثل ملف المصدر، عنوان القسم، نسخة المستند، والتصاريح. هذا يجعل الاسترجاع أسهل للفحص ويهيئ المثال للترشيح، الاقتباسات، والنشر المستقبلي المستمر أو القائم على الخادم.

FAISS رائع لعرض بحث تشابه المتجهات. Qdrant أفضل لعرض طبقة استرجاع RAG صغيرة لكنها مُصممة للإنتاج.

بعض البدائل العملية:

| مخزن/طبقة البحث المتجه | متى سأعتبره |
| --- | --- |
| Qdrant | النماذج الأولية المحلية، ترشيح البيانات الوصفية، بحث المتجهات الملائم للإنتاج، وسير عمل بايثون بسيط. |
| Chroma | تجارب RAG محلية سريعة ودفاتر ملاحظات حيث البساطة هي الأهم. |
| FAISS | بحث متجه محلي خفيف الوزن عندما أحتاج فقط بحث التشابه ويمكنني إدارة البيانات الوصفية بشكل منفصل. |
| Milvus | بحث متجه مفتوح المصدر على نطاق أوسع عندما يكون الفريق مستعدًا لتشغيل قاعدة بيانات متجه مخصصة. |
| Weaviate | بحث متجه مع مخطط، بيانات وصفية، بحث هجين، وخيارات نشر مُدارة أو ذاتية الاستضافة. |
| Azure AI Search | RAG مؤسسي على أزور عندما أريد بحث بالكلمات المفتاحية، بحث متجه، استرجاع هجين، ترتيب دلالي، الترشيح، الأمان، والعمليات المُدارة في طبقة بحث واحدة. |
| PostgreSQL + pgvector | فرق تستخدم PostgreSQL بالفعل وترغب في البحث المتجه قريبًا من بيانات التطبيق. |

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

ثم إدخال النقاط:

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

في تجربتي، أدخلت المجموعة 8 متجهات.

هنا يبدأ نظام RAG ليصبح قابلاً للفحص. قاعدة بيانات المتجهات لا تخزن المتجهات فقط؛ إنها تخزن نص الأدلة والبيانات الوصفية اللازمة للاقتباسات.

## 7. استرجاع القطع المرشحة

الآن نطرح السؤال ونسترجع القطع المرشحة.

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

في هذه المرحلة، أطبع القطع المسترجعة قبل إنشاء إجابة. هذا مهم. إذا كان الاسترجاع خاطئًا، فالتوليد سيخفي المشكلة خلف نص سليم.

## 8. إضافة مُعاد ترتيب خفيف الوزن

عندما اختبرت مسار الاسترجاع لأول مرة، وجد تشابه المتجهات وحده محتوى سياسة مرتبط، لكن القسم الأكثر دقة لم يكن دائمًا في القمة.

لذا أضفت معيد ترتيب محلي صغير. يعطي وزنًا إضافيًا عندما تتداخل مصطلحات السؤال مع عنوان القسم والمحتوى.

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

بعد إعادة الترتيب، أصبح أعلى نتيجة:

```text
school_ai_policy.md / Final Assignments
```

كان ذلك القسم المتوقع لسؤال الاختبار.

كانت هذه أهم درس من التنفيذ الأول. حتى في مثال محلي صغير، تحسنت جودة الاسترجاع عندما جمعت بين تشابه المتجهات وإشارة أخرى.

## 9. تأليف إجابة محلية مدعومة

للمسار الافتراضي، أستخدم مؤلف إجابة شفاف محلي بدلاً من LLM.

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

هذا ليس مخصصًا ليكون مولد إجابة منتج نهائي. هو أداة تصحيح أخطاء. يثبت أن الاسترجاع، البيانات الوصفية، وربط الاقتباسات يعمل قبل إضافة تباين النموذج.

## 10. توليد إجابة محلية باستخدام Ollama و Phi-4-mini

عندما يعمل الاسترجاع، يمكن لدفتر الملاحظات استبدال خطوة الإجابة النهائية فقط بـ Ollama و `phi4-mini:3.8b`.

> [!NOTE]
> يجب أن يحل Ollama محل خطوة توليد الإجابة النهائية فقط. يجب أن تبقى عمليات تحميل المستند، التجزئة، تخزين المتجهات، الاسترجاع، إعادة الترتيب، وربط الاقتباسات كما هي.

أولًا، يبني دفتر الملاحظات موجه الأدلة من القطع المسترجعة:

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

لهذا الدرس، أوصي بأسرة Phi-4-mini من Microsoft عبر Ollama كخيار التوليد المحلي الافتراضي. اسم النموذج الذي جربته في Ollama هو:

```powershell
ollama pull phi4-mini:3.8b
```

يمكنك التحقق سريعًا من توفر النموذج:

```powershell
ollama list
```

ثم تعيين هذه المتغيرات:

```powershell
Copy-Item .env.example .env
```

افتح `.env` وأزل تعليق قيم Ollama للسلسلة 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

يحمّل دفتر الملاحظات `.env` من جذر المستودع باستخدام `python-dotenv`، ثم يرسل نفس موجه الأدلة إلى نقطة نهاية `/api/chat` المحلية لـ Ollama مع تعطيل البث. إذا لم يكن Ollama قيد التشغيل أو كان `SERIES2_OLLAMA_MODEL` مفقودًا، يتم تخطي هذا المسار.

> [!NOTE]
> على هذه الجهاز، تم تنزيل `phi4-mini:3.8b` بحجم حوالي 2.49 جيجابايت من ملفات النموذج. أثناء الاستدلال، ذكر Ollama حجم نموذج محمّل بحجم 3.3 جيجابايت واستخدم GPU من نوع RTX 3060 Laptop.

هذا يمنح الدرس مستويين:

1. مؤلف إجابة محدد المعالم باستخدام المعالج المركزي فقط.
2. توليد إجابة محلي باستخدام Ollama و Phi-4-mini.

خط أنابيب الاسترجاع يبقى نفسه في كلتا الحالتين.

## 11. نتيجة التحقق

شغّلت دفتر الملاحظات محليًا على ويندوز مع Python 3.12.6.

الحزم المثبتة:

| الحزمة | الإصدار |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

تنفيذ دفتر الملاحظات:

- الدفتر: `notebooks/series-2-open-source-rag.ipynb`
- نتيجة التنفيذ: ناجح باستخدام `nbclient`
- المستندات المحملة: 2
- القطع التي تم إنشاؤها: 8
- مجموعة Qdrant: `school_policy_local`
- المتجهات التي تم إدخالها: 8
- نموذج التضمين: `BAAI/bge-small-en-v1.5`
- حجم التضمين: 384
- سؤال الاسترجاع: "هل يمكنني استخدام الذكاء الاصطناعي التوليدي في مهمتي النهائية؟"
- مسار إعادة الترتيب: إعادة ترتيب معجمية محلية خفيفة الوزن
- أعلى مصدر تم استرجاعه بعد إعادة الترتيب: `school_ai_policy.md`
- أعلى قسم تم استرجاعه بعد إعادة الترتيب: `المهام النهائية`
- مسار الإجابة الافتراضي: مؤلف الإجابة الشفاف المحلي
- مسار توليد أولاما: مكتمل بـ `phi4-mini:3.8b`
- حجم ملف نموذج أولاما: 2.49 جيجابايت على القرص
- حجم النموذج المحمّل في أولاما: 3.3 جيجابايت حسب تقرير `ollama ps`
- إيقاف تحميل GPU: 100% GPU حسب تقرير `ollama ps`
- ذاكرة GPU التي لوحظت بعد التوليد: حوالي 3.5 جيجابايت من 6 جيجابايت مستخدمة على RTX 3060 Laptop GPU
- تنفيذ الدفتر مع نموذج FastEmbed المخزّن مؤقتًا وتوليد أولاما مفعّل: تم بنجاح في حوالي 34 ثانية عبر سكريبت التحقق

كانت الإجابة التي ولّدها أولاما:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```
  
لن أسمي هذه الإجابة مثالية. تجيب من الدليل الصحيح، لكن سطر المصدر النهائي أقل دقة من تنسيق الاقتباس الحتمي. هذا مفيد للعرض في الدرس لأنه يجعل سؤال الهندسة التالي واضحًا: توليد الإجابة يحتاج أيضًا إلى تقييم، وليس فقط الاسترجاع.

الشيء الرئيسي الذي تعلمته أثناء التحقق من ذلك هو أنه يجب فحص جودة الاسترجاع قبل توليد الإجابة. كانت نتيجة التضمين مفيدة بالفعل، وأعاد موقع الترتيب الخفيف الوزن قسم السياسة المتوقع للظهور أولاً بثقة. هذا بالضبط نوع سلوك النظام الصغير الذي أريد أن يتركز عليه الدرس بدلاً من إخفائه.

## 12. ما التالي

التحسين التالي هو مقارنة هذا الإعداد المحلي مع نسخة مدارة على Azure لنفس سيناريو مساعد سياسة المدرسة. إبقاء السيناريو ثابتًا يجب أن يجعل الموازنات أسهل للرؤية: تعقيد الإعداد، ضوابط الاسترجاع، دمج الهوية، ملكية التشغيل، والتكلفة.

## 13. المراجع

- [بدء سريع لعميل Qdrant بايثون](https://python-client.qdrant.tech/quickstart.html)  
- [مستودع عميل Qdrant على GitHub](https://github.com/qdrant/qdrant-client)  
- [نماذج مدعومة من FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)  
- [دليل تضمينات OpenAI](https://platform.openai.com/docs/guides/embeddings)  
- [بطاقة نموذج BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)  
- [بطاقة نموذج BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)  
- [بطاقة نموذج sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  
- [صفحة نموذج أولاما phi4-mini](https://ollama.com/library/phi4-mini)  
- [توثيق أولاما لأنظمة ويندوز](https://docs.ollama.com/windows)  
- [توثيق بث API أولاما](https://docs.ollama.com/api/streaming)  
- [بطاقة نموذج Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)  
- [نظرة عامة على LangGraph](https://docs.langchain.com/oss/python/langgraph)  
- [مقدمة عن RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

السابق: [السلسلة 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**تنويه**:
تمت ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والمعتمد. للمعلومات الهامة، يُنصح بالاستعانة بترجمة بشرية محترفة. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->