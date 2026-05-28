# ללמד את הבינה המלאכותית לענות על שאלות בהתבסס על המסמכים שלך
## סדרה 2: לבנות מערכת RAG קהילתית מקומית מקצה לקצה

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> מאמר זה הופך את דיון הארכיטקטורה של סדרה 1 למדריך רץ למערכת RAG מקומית. המטרה היא לבנות במלואה את זרם העבודה תחילה עם נתוני דוגמה, ללא חשבון ענן וללא סודות, ואז להשתמש בבסיס העבודה הזה לקבל החלטות ארכיטקטורה טובות יותר בהמשך.

המערכת שנבנה היא עוזר מדיניות בית ספר קטן. אני משתמש בשני מסמכי Markdown מקומיים כבסיס ידע, ואז עובר דרך כל זרם העבודה של RAG: חלקה, הטמעות מקומיות, אחסון וקטורים ב-Qdrant, אחזור, דירוג מחדש, הרכבת תשובה עם מודעות למקור, ויצירה מקומית אופציונלית עם Ollama ו-Phi-4-mini.

ניווט בסדרה: [דף הבית של המאגר](../README.md) | הקודם: [סדרה 1 - RAG, Azure מול חלופות קהילתיות, ומתי כיוון מדויק הגיוני](./series-1-rag-azure-open-source-fine-tuning.md)

מחברת: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | דרישות: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> זהו נקודת התחלה מעולה אם ברצונך להבין את זרם העבודה של RAG לפני יצירת משאבי ענן. הנתיב המוגדר פועל מקומית עם הטמעות נוחות ל-CPU וללא סודות.

## 1. מה אנחנו בונים

במדריך של 2023, התחלתי מ-Azure כי המטרה הייתה להראות כיצד Azure AI Search ו-Azure OpenAI יכולים לענות על שאלות מסמכי PDF.

לסדרה של 2026 הזו, אני רוצה להתחיל שכבה אחת נמוכה יותר.

לפני שימוש בשירותים מנוהלים, אני רוצה לבנות מערכת RAG קטנה מקומית ולהפוך כל שלב לגלוי: טעינת מסמכים, חלקת טקסט, אחסון וקטורים, אחזור ראיות, דירוג מחדש, והחזרת תשובה עם מודעות למקור.

התרחיש המדגם הוא עוזר מדיניות בית ספר. המשתמש שואל:

```text
Can I use generative AI for my final assignment?
```

המערכת לא אמורה לענות מזיכרון מודל כללי. היא אמורה לאחזר את הקטע הרלוונטי במדיניות ולענות מהראיות האלה.

הגרסה המלאה והרצה נמצאת ב-[series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). הקוד למטה מראה את השלבים העיקריים כך שהמאמר יכול להיקרא כמדריך.

## 2. התקנת התלויות המקומיות

צור סביבה וירטואלית והתקן את דרישות סדרה 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

הגרסה הראשונה משתמשת במצב מקומי של Qdrant וב-FastEmbed. לקוח Python של Qdrant תומך במצב מקומי בזיכרון עם `QdrantClient(":memory:")`, שימושי למדריכים מקומיים ולאימות בסגנון CI. FastEmbed נותן לנו מודל הטמעות מקומי אמיתי ללא צורך במפתח API ענן.

קובץ הדרישות כולל גם `python-dotenv` כיוון שהמחברת יכולה לקרוא אופציונלית שם מודל Ollama מתוך `.env`. אין צורך במפתח Azure OpenAI או OpenAI למדריך המקומי הזה.

## 3. טוענים את המסמכים המדגמיים

הקורפוס המדגמי הוא קטן במכוון:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

במחברת אני טוען את כל קבצי Markdown מתיקיית `sample_data/`:

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

כשהרצתי את המחברת, היא טענה 2 מסמכים. זה מספיק קטן לבדיקה ידנית, שימושי בבניית הגרסה הראשונה של זרם העבודה של RAG.

## 4. חלוקה לפי כותרות Markdown

השלב הבא הוא לפרק את המסמכים לחתיכות.

למדריך הזה אני משתמש בכותרות Markdown כאות המבנה. כותרת המסמך מגיעה מ-`#` וכל קטע מגיע מ-`##`.

> [!NOTE]
> החלוקה אינה בגודל אחד שמתאים לכולם. במדריך הזה אני משתמש בכותרות Markdown כי המסמכים המדגמיים כוללים מבנה ברור עם `#` ו-`##`. עבור PDF, מסמכי Word, מצגות, כרטיסים או אתרי אינטרנט, אסטרטגיה טובה יותר עשויה להשתמש בגבולות עמוד, מידע על הפריסה, קטעים סֶמנטיים, מגבלות טוקנים, טבלאות או מטא-נתונים. הנקודה החשובה היא לבחור אסטרטגיית חלוקה ששומרת על משמעות ויכולת זיהוי מקור במסמכים שלך.

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

ואז אני מיישם את זה על כל מסמך:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

יצרתי 8 חתיכות בהרצה המקומית שלי.

מה שאהבתי בשלב הזה הוא שמטא-נתונים כבר שימושיים. כל חתיכה יודעת את ה-`source`, `sectionHeading`, `documentVersion` ואת ה-`permissions` כמקום מילוי. אפילו במדריך קטן זה מקל על הציטוטים ועל אחזור מבוסס הרשאות בעתיד.

## 5. יצירת הטמעות מקומיות

לגרסה הציבורית הראשונה אני משתמש ב-`BAAI/bge-small-en-v1.5` באמצעות FastEmbed.

זה שומר את המדריך מקומי ונוח ל-CPU, אבל עדיין משתמש במודל הטמעות אמיתי במקום פונקציית וקטור מקום מילוי. בהרצה הראשונה מורידים את משקלי המודל. לאחר מכן המחברת יכולה להשתמש במטמון המקומי.

> [!NOTE]
> אני משתמש ב-`BAAI/bge-small-en-v1.5` כי זהו מודל הטמעות אנגלית קל שמתחבר טוב ל-FastEmbed ול-Qdrant למדריך מקומי. הוא יוצר וקטורים בגודל 384 ממדים, מה שגורם לדוגמה להיות מהירה וזולה להרצה מקומית. זו לא הבחירה היחידה הטובה. ב-2023, רבים השתמשו במודלים מאוחסנים כמו `text-embedding-ada-002`. כיום, אפשרויות מאוחסנות חדשות כמו OpenAI `text-embedding-3-small` ו-`text-embedding-3-large`, ואפשרויות קהילתיות כמו BGE, E5, MiniLM, Nomic Embed, ומודלים רב-לשוניים כמו `BAAI/bge-m3` הן אפשרויות ריאליות בהתאם לעומס העבודה. בייצור, יש לבחור את מודל ההטמעות הנכון באמצעות הערכת אחזור במסמכים שלך.

כמה חלופות מעשיות:

| משפחת מודל | מתי הייתי שוקל אותה |
| --- | --- |
| `text-embedding-ada-002` | בסיס ישן יותר באירוח שצץ בהרבה מדריכים מתקופת 2023. לא הייתי בוחר בו כברירת מחדל למדריך חדש היום. |
| `text-embedding-3-small` | ברירת המחדל המודרנית כשאני רוצה איזון טוב בין עלות/ביצועים ואינני צריך הטמעות מקומיות בלבד. |
| `text-embedding-3-large` | אפשרות מאוחסנת כשהאיכות של האחזור חשובה יותר מגודל הוקטור או מחיר ההטמעה. |
| `BAAI/bge-small-en-v1.5` | בסיס מקומי קל באנגלית למדריכים, אב-טיפוסים וניסויים נוחים ל-CPU. |
| `BAAI/bge-base-en-v1.5` או `BAAI/bge-large-en-v1.5` | מודלים מקומיים גדולים יותר באנגלית כשאני רוצה איכות אחזור טובה יותר ויכול להרשות יותר חישוב. |
| `BAAI/bge-m3` | אחזור רב-לשוני או הקשר ארוך, במיוחד כשמסמכים אינם רק באנגלית. |
| `sentence-transformers/all-MiniLM-L6-v2` | בסיס חיפוש סמנטי קטן ומהיר מאוד. שימושי כשמהירות ופשטות הם העיקר. |
| `nomic-embed-text-v1.5` | אפשרות הטמעות מקומית קהילתית ששווה לבדוק למערכות עם הקשר ארוך או תכנון לניידות. |

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

ואז כל חתיכה מקבלת הטמעה:

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

## 6. אחסן וקטורים במצב מקומי של Qdrant

כעת ניצור אוסף Qdrant בזיכרון ונכנס את החתיכות עם מטא-נתונים של המטען.

> [!NOTE]
> במדריך של 2023 השתמשתי ב-FAISS כי זו הייתה דרך פשוטה ופופולרית להדגים חיפוש דמיון וקטורי מקומי עם LangChain. FAISS עדיין שימושי לניסויים מהירים מקומיים. בגרסה הזו של 2026 אני משתמש ב-Qdrant כי אני רוצה שהמדריך ירגיש קרוב יותר למערכת RAG בייצור. Qdrant מאפשר לי לאחסן וקטורים יחד עם מטא-נתונים של המטען כמו קובץ מקור, כותרת קטע, גרסת מסמך והרשאות. זה מקל על האחזור ונותן דוגמה לסינון, לציטוטים, ולפריסה עתידית מתמשכת או מבוססת שרת.

FAISS מעולה להדגמת חיפוש דמיון וקטורי. Qdrant טוב יותר להצגת שכבת אחזור RAG קטנה אך מכוונת ייצור.

כמה חלופות מעשיות:

| מחסן וקטורים / שכבת חיפוש | מתי הייתי שוקל אותה |
| --- | --- |
| Qdrant | אב-טיפוסים מקומיים, סינון מטא-נתונים, חיפוש וקטורים ידידותי לייצור, וזרם עבודה פשוט ב-Python. |
| Chroma | ניסויים מהירים מקומיים למערכת RAG ומחברות שבהן פשטות היא העיקר. |
| FAISS | חיפוש וקטורי מקומי קל ונוח כשאני צריך רק חיפוש דמיון ויכול לנהל מטא-נתונים בנפרד. |
| Milvus | חיפוש וקטורי בקנה מידה גדול קהילתי כשהצוות מוכן לנהל מסד וקטורי ייעודי. |
| Weaviate | חיפוש וקטורי עם סכמה, מטא-נתונים, חיפוש משולב, ואפשרויות פריסה מנוהלות או בדיקה עצמית. |
| Azure AI Search | RAG ארגוני על Azure כשאני רוצה חיפוש לפי מילת מפתח, חיפוש וקטורי, אחזור משולב, דירוג סמנטי, סינון, אבטחה ופעולות מנוהלות בשכבת חיפוש אחת. |
| PostgreSQL + pgvector | צוותים שכבר משתמשים ב-PostgreSQL ורוצים חיפוש וקטורי קרוב לנתוני האפליקציה. |

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

ואז מכניסים את הנקודות:

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

בהרצה שלי, האוסף הכניס 8 וקטורים.

 כאן מערכת ה-RAG מתחילה להיות ניתנת לבחינה. מסד הנתונים הווקטורי לא רק מאחסן וקטורים; הוא מאחסן את טקסט הראיות ואת המטא-נתונים הנדרשים לציטוטים.

## 7. אחזר חתיכות מועמדות

כעת אנחנו שואלים את השאלה ומאחזר חתיכות מועמדות.

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

כאן אני מדפיס את החתיכות שהוחזרו לפני יצירת תשובה. זה חשוב. אם האחזור שגוי, הייצור יסתיר את הבעיה מאחורי טקסט שוטף.

## 8. הוסף דירוג מחדש קל

כשהתחלתי לבדוק את נתיב האחזור, דמיון וקטורי לבדו מצא תוכן מדיניות רלוונטי, אבל הקטע המדויק ביותר לא תמיד היה בראש.

אז הוספתי דירוג מחדש מקומי קטן. הוא נותן משקל נוסף כשמונחי השאלה חופפים לכותרת הקטע ולתוכן.

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

אחרי דירוג מחדש, התוצאה העליונה הייתה:

```text
school_ai_policy.md / Final Assignments
```

זו הייתה הקטע המצופה לשאלה שבדקנו.

זו הייתה הלקח הכי חשוב מהמימוש הראשון. אפילו בדוגמה מקומית קטנה, איכות האחזור השתפרה כשהשוויתי דמיון וקטורי עם אות נוספת.

## 9. הרכב תשובה מקומית מבוססת

לנתיב ברירת המחדל אני משתמש בהרכב תשובה מקומי שקוף במקום LLM.

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

זה לא מיועד להיות מנגנון יצירת תשובה סופי. זהו כלי דיבוג. הוא מוכיח שאחזור, מטא-נתונים וחיבור ציטוטים עובדים לפני הוספת שונות מודלי.

## 10. צור תשובה מקומית עם Ollama ו-Phi-4-mini

ברגע שאחזור עובד, המחברת יכולה להחליף רק את שלב יצירת התשובה הסופי עם Ollama ו-`phi4-mini:3.8b`.

> [!NOTE]
> Ollama צריך להחליף רק את שלב יצירת התשובה הסופי. טעינת המסמכים, החלקה, אחסון הוקטורים, האחזור, הדירוג מחדש וחיבור הציטוטים צריכים להישאר אותו דבר.

ראשית, המחברת בונה בקשת ראיות מהחתיכות שהוחזרו:

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

למדריך הזה, אני ממליץ על משפחת Phi-4-mini של Microsoft דרך Ollama כאפשרות ברירת מחדל ליצירה מקומית. המחברת השתמשה בשם המודל:

```powershell
ollama pull phi4-mini:3.8b
```

אפשר במהירות לבדוק שהמודל זמין:

```powershell
ollama list
```

ואז להגדיר את המשתנים האלה:

```powershell
Copy-Item .env.example .env
```

פתח `.env` והסר את ההערה מהערכים של Ollama בסדרה 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

המחברת טוענת את `.env` משורש המאגר עם `python-dotenv`, ואז שולחת את אותו בקשת ראיות לנקודת הקצה המקומית `/api/chat` של Ollama עם הזרמה מושבתת. אם Ollama לא רצה או ש-`SERIES2_OLLAMA_MODEL` חסר, מסלול זה מדולג.

> [!NOTE]
> במכונה הזו, `phi4-mini:3.8b` הוריד כ-2.49GB של קבצי מודל. במהלך האינפרנציה, Ollama דיווח על גודל מודל טעון של 3.3GB והשתמש ב-GPU RTX 3060 Laptop.

זה נותן למדריך שני רמות:

1. מנגנון הרכבת תשובה דטרמיניסטי CPU בלבד.
2. יצירת תשובה מקומית עם Ollama ו-Phi-4-mini.

זרם האחזור נשאר זהה בשתי הרמות.

## 11. תוצאת אימות

הרצתי את המחברת מקומית ב-Windows עם Python 3.12.6.

חבילות מותקנות:

| חבילה | גרסה |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

הרצת המחברת:

- מחברת: `notebooks/series-2-open-source-rag.ipynb`
- תוצאת הרצה: עברה עם `nbclient`
- מסמכים נטענו: 2
- חתיכות שנוצרו: 8
- אוסף Qdrant: `school_policy_local`
- וקטורים מוזנו: 8
- מודל הטמעות: `BAAI/bge-small-en-v1.5`
- גודל הטמעה: 384
- שאלה לשליפה: "האם ניתן להשתמש בבינה מלאכותית יוצרת עבור המטלה הסופית שלי?"
- מסלול מיון מחדש: מיון מחדש לקסיקלי מקומי קל משקל
- מקור ראשי שזוהה לאחר מיון מחדש: `school_ai_policy.md`
- קטע ראשי שזוהה לאחר מיון מחדש: `מטלות סופיות`
- מסלול ברירת מחדל למענה: מחבר תשובות שקוף מקומי
- מסלול יצירת אולאמה: הושלם עם `phi4-mini:3.8b`
- גודל קובץ הדגם של אולאמה: 2.49GB בדיסק
- גודל דגם אולאמה שטען: 3.3GB כפי שדווח על ידי `ollama ps`
- הפרדת GPU: 100% GPU כפי שדווח על ידי `ollama ps`
- זיכרון GPU שנצפה לאחר יצירה: כ-3.5GB מתוך 6GB בשימוש על RTX 3060 Laptop GPU
- ביצוע פנקס הערות עם דגם FastEmbed שמור ויצירת אולאמה מופעלת: עבר בכ-34 שניות דרך סקריפט האימות

התשובה שנוצרה על ידי אולאמה הייתה:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

לא הייתי קורא לתשובה זו מושלמת. היא עונה ממקור הראיות הנכון, אך שורת המקור הסופית פחות מדויקת מפורמט הציטוט הדטרמיניסטי. זה שימושי להראות בטיוטוריאל כי זה מבהיר את השאלה ההנדסית הבאה: יצירת תשובות גם צריכה הערכה, לא רק השליפה.

העיקר שלמדתי בזמן האימות הוא שיש לבדוק את איכות השליפה לפני יצירת התשובה. תוצאת האמבדינג הייתה שימושית כבר, ומיין מחדש הקל משקל גרם לכך שקטע מדיניות הצפוי הופיע אמין ראשון. זה בדיוק סוג ההתנהגות הקטנה של המערכת שאני רוצה שהטיוטוריאל יחשוף במקום להסתיר.

## 12. מה הלאה

השיפור הבא הוא להשוות את ההתקנה המקומית הזו עם גרסה מנוהלת של Azure של אותו תרחיש עוזר מדיניות בית ספר. שמירת התרחיש קבוע תקל על זיהוי הפשרות: מורכבות ההתקנה, בקרות השליפה, אינטגרציית זהות, בעלות תפעולית ועלות.

## 13. מקורות

- [מדריך מהיר ללקוח Python של Qdrant](https://python-client.qdrant.tech/quickstart.html)
- [מאגר GitHub של לקוח Qdrant](https://github.com/qdrant/qdrant-client)
- [דגמים נתמכים של FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [מדריך אמבדינג של OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [כרטיס דגם BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [כרטיס דגם BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [כרטיס דגם sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [דף דגם Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [תיעוד Ollama ל-Windows](https://docs.ollama.com/windows)
- [תיעוד API סטרימינג של Ollama](https://docs.ollama.com/api/streaming)
- [כרטיס דגם Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [סקירת LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [מבוא ל-RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

הקודם: [סדרה 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->