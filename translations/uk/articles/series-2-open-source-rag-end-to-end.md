# Навчіть ШІ відповідати на запитання на основі ваших документів
## Серія 2: Побудова локальної RAG-системи з відкритим кодом від початку до кінця

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Ця стаття перетворює обговорення архітектури Серії 1 у виконуваний локальний навчальний посібник з RAG. Мета полягає в тому, щоб спочатку побудувати повний робочий процес із прикладними даними, без облікового запису в хмарі та секретів, а потім використати цей робочий базовий рівень для кращих архітектурних рішень у майбутньому.

Система, яку ми побудуємо, — це невеликий помічник із політики школи. Я використовую два локальні документи Markdown як базу знань, а потім проходжу повний конвеєр RAG: розбиття на фрагменти, локальні ембедінги, векторне сховище Qdrant, витяг, повторне ранжування, формування відповіді з урахуванням джерела та опціональне локальне генерування з Ollama і Phi-4-mini.

Навігація серії: [Домашня сторінка репозиторію](../README.md) | Попередня: [Серія 1 - RAG, Azure vs альтернативи з відкритим кодом і коли корисне донавчання](./series-1-rag-azure-open-source-fine-tuning.md)

Ноутбук: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Вимоги: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Це найкраща точка старту, якщо ви хочете зрозуміти конвеєр RAG перед створенням хмарних ресурсів. За замовчуванням запускається локально з CPU-дружніми ембедінгами та без секретів.

## 1. Що ми будуємо

У підручнику 2023 року я починав з Azure, бо мета була показати, як Azure AI Search та Azure OpenAI можуть відповідати на запитання з PDF-документів.

Для цієї серії 2026 року я хочу почати на один рівень нижче.

Перед використанням керованих сервісів я хочу побудувати невелику RAG-систему локально і зробити кожен крок видимим: завантаження документів, розбиття тексту на фрагменти, зберігання векторів, витяг доказів, повторне ранжування результатів і повернення відповіді з урахуванням джерела.

Приклад сценарію — помічник із шкільної політики. Користувач запитує:

```text
Can I use generative AI for my final assignment?
```

Система не повинна відповідати на базі загальної пам'яті моделі. Вона повинна знаходити відповідний розділ політики та відповідати, базуючись на цих доказах.

Повна виконувана версія у [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Наведений код показує основні кроки, щоб статтю можна було прочитати як посібник.

## 2. Встановлення локальних залежностей

Створіть віртуальне середовище та встановіть вимоги Серії 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Перша версія використовує локальний режим Qdrant і FastEmbed. Python-клієнт Qdrant підтримує локальний режим в оперативній пам’яті з `QdrantClient(":memory:")`, що корисно для локальних навчальних посібників та перевірок у стилі CI. FastEmbed дає нам справжню локальну модель ембедінгів без потреби в ключі API хмари.

Файл вимог також містить `python-dotenv`, бо ноутбук може вибірково зчитувати ім'я моделі Ollama з `.env`. Для цього локального підручника ключі Azure OpenAI чи OpenAI API не потрібні.

## 3. Завантаження прикладних документів

Прикладний корпус навмисно маленький:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

У ноутбуці я завантажую всі файли Markdown із `sample_data/`:

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

Коли я запускав ноутбук, він завантажив 2 документи. Це достатньо мало, щоб інспектувати вручну, що корисно під час побудови першої версії конвеєра RAG.

## 4. Розбиття за заголовками Markdown

Наступний крок — розбити документи на фрагменти.

Для цього підручника я використовую заголовки Markdown як сигнал структури. Назва документа береться з `#`, а кожен розділ — з `##`.

> [!NOTE]
> Розбиття не універсальне. В цьому підручнику я використовую заголовки Markdown, бо прикладні документи мають чітку структуру `#` і `##`. Для PDF, Word-документів, слайдів, тікетів чи веб-сторінок кращою стратегією можуть бути межі сторінок, інформація про макет, семантичні секції, ліміти токенів, таблиці чи метадані. Важливо обрати стратегію розбиття, яка зберігає значення та слідкуваність джерела у ваших документах.

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

Потім я застосовую це до кожного документа:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

У моєму локальному запуску це створило 8 фрагментів.

Мені подобається, що у цьому кроці метадані вже корисні. Кожен фрагмент знає свій `source`, `sectionHeading`, `documentVersion` і заповнювач `permissions`. Навіть у маленькому прикладі це спрощує цитування та пізніше врахування дозволів під час отримання даних.

## 5. Створення локальних ембедінгів

Для першої публічної версії я використовую `BAAI/bge-small-en-v1.5` через FastEmbed.

Це зберігає підручник локальним і дружнім до CPU, але все ще використовує справжню модель ембедінгів замість функції заповнювача векторів. Перший запуск завантажує ваги моделі. Надалі ноутбук може повторно використовувати локальний кеш.

> [!NOTE]
> Я використовую `BAAI/bge-small-en-v1.5`, бо це легка модель ембедінгів англійською, яка добре працює з FastEmbed і Qdrant для локального підручника. Вона створює вектори розмірністю 384, що робить приклад швидким і недорогим для запуску локально. Це не єдина добра опція. У 2023 році багато підручників використовували хостовані ембедінги типу `text-embedding-ada-002`. Сьогодні більш нові хостовані варіанти, такі як OpenAI `text-embedding-3-small` і `text-embedding-3-large`, а також відкриті рішення, як BGE, E5, MiniLM, Nomic Embed і багатомовні моделі на кшталт `BAAI/bge-m3`, є розумним вибором залежно від навантаження. В продакшні правильна модель ембедінгів вибирається через оцінку витягування на ваших документах.

Деякі практичні альтернативи:

| Родина моделей | Коли я розглядаю варіант |
| --- | --- |
| `text-embedding-ada-002` | Старіший хостований базовий варіант, який з’являвся у багатьох підручниках 2023 року. Сьогодні я не обрав би його за замовчуванням для нового підручника. |
| `text-embedding-3-small` | Сучасний хостований варіант за замовчуванням, коли потрібен хороший баланс вартості та продуктивності і не потрібні виключно локальні ембедінги. |
| `text-embedding-3-large` | Хостована опція, коли якість витягування важливіша за розмір вектора або вартість ембедінгів. |
| `BAAI/bge-small-en-v1.5` | Легка локальна англомовна базова модель для підручників, прототипів і CPU-дружніх експериментів. |
| `BAAI/bge-base-en-v1.5` або `BAAI/bge-large-en-v1.5` | Великі локальні англомовні моделі, коли хочеться кращої якості витягування і можна дозволити більше обчислень. |
| `BAAI/bge-m3` | Багатомовне або довший контекст витягування, особливо якщо документи не лише англійською. |
| `sentence-transformers/all-MiniLM-L6-v2` | Дуже маленька і швидка базова модель семантичного пошуку. Корисна, коли найважливіша швидкість і простота. |
| `nomic-embed-text-v1.5` | Відкрита локальна модель ембедінгів, варта тестування для довшоконтекстних або орієнтованих на портативність налаштувань. |

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

Потім кожному фрагменту призначається ембедінг:

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

## 6. Зберігання векторів у локальному режимі Qdrant

Тепер створюємо колекцію Qdrant в оперативній пам’яті та вставляємо фрагменти з метаданими.

> [!NOTE]
> У підручнику 2023 року я використовував FAISS, бо це був простий і популярний спосіб показати локальний пошук за схожістю векторів з LangChain. FAISS досі корисний для швидких локальних експериментів. У цій версії 2026 року я використовую Qdrant, бо хочу, щоб підручник більше нагадував виробничу RAG-систему. Qdrant дозволяє зберігати вектори разом з метаданими, такими як файл-джерело, заголовок секції, версія документа та дозволи. Це полегшує огляд витягування і підготуває приклад для фільтрації, цитування та майбутнього постійного чи серверного розгортання.

FAISS добре показує пошук за векторною схожістю. Qdrant краще для демонстрації невеликого, але виробничо орієнтованого рівня витягування для RAG.

Деякі практичні альтернативи:

| Векторне сховище / шар пошуку | Коли я розглядаю варіант |
| --- | --- |
| Qdrant | Локальні прототипи, фільтрація за метаданими, виробничо орієнтований векторний пошук та простий робочий процес на Python. |
| Chroma | Швидкі локальні RAG-експерименти та ноутбуки, де важлива максимальна простота. |
| FAISS | Легкий локальний векторний пошук, якщо потрібен лише пошук за схожістю і метадані керуються окремо. |
| Milvus | Відкритий векторний пошук великого масштабу, коли команда готова запускати спеціалізовану базу векторів. |
| Weaviate | Векторний пошук із схемою, метаданими, гібридним пошуком, варіанти керованого або самостійного розгортання. |
| Azure AI Search | Корпоративний RAG на Azure, коли потрібен пошук за ключовими словами, векторами, гібридне витягування, семантичне ранжування, фільтрація, безпека та керовані операції в одному пошуковому шарі. |
| PostgreSQL + pgvector | Команди, що вже використовують PostgreSQL і хочуть векторний пошук поруч із даними додатку. |

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

Потім вставляємо точки:

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

У моєму запуску колекція вставила 8 векторів.

Це момент, коли система RAG починає ставати інспектованою. Векторна база даних зберігає не лише вектори, а й текст доказів та метадані, потрібні для цитування.

## 7. Витягування кандидатів-фрагментів

Тепер ставимо запитання і витягаємо кандидатів.

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

На цьому етапі я виводжу знайдені фрагменти перед генерацією відповіді. Це важливо. Якщо витягування неправильне, генерація просто сховає проблему за плавним текстом.

## 8. Додавання легкого повторного ранжування

Коли я вперше тестував шлях витягування, лише схожість векторів знаходила пов’язаний політичний контент, але найточніший розділ не завжди був на вершині.

Тож я додав невеликий локальний повторний ранжувач. Він дає додаткову вагу, коли терміни запитання збігаються із заголовком і вмістом секції.

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

Після повторного ранжування найвищим результатом став:

```text
school_ai_policy.md / Final Assignments
```

Це був очікуваний розділ для тестового запитання.

Це був найкорисніший урок із першої реалізації. Навіть у крихітному локальному прикладі якість витягування покращилась, коли я поєднав схожість векторів із іншим сигналом.

## 9. Формування обґрунтованої локальної відповіді

Для шляху за замовчуванням я використовую прозорий локальний конструктор відповіді замість LLM.

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

Це не призначено бути кінцевим генератором відповідей. Це інструмент відладки. Він доводить, що витягування, метадані і зв’язування цитат працюють перед додаванням варіативності моделі.

## 10. Генерація локальної відповіді з Ollama і Phi-4-mini

Коли витягування працює, ноутбук може замінити лише останній крок відповіді на Ollama і `phi4-mini:3.8b`.

> [!NOTE]
> Ollama повинен замінювати лише фінальний крок генерації відповіді. Завантаження документів, розбиття на фрагменти, збереження векторів, витягування, повторне ранжування і зв’язування цитат повинні залишатися без змін.

Спочатку ноутбук створює підказку доказів із витягнутих фрагментів:

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

Для цього підручника я рекомендую сімейство Microsoft Phi-4-mini через Ollama як опцію за замовчуванням для локальної генерації. У Ollama ім’я моделі, яку я тестував:

```powershell
ollama pull phi4-mini:3.8b
```

Ви можете швидко перевірити, що модель доступна:

```powershell
ollama list
```

Потім встановлюємо такі змінні:

```powershell
Copy-Item .env.example .env
```

Відкрийте `.env` і розкоментуйте значення Ollama для Серії 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Ноутбук завантажує `.env` з кореня репозиторію за допомогою `python-dotenv` і відсилає ту ж підказку доказів до локальної кінцевої точки Ollama `/api/chat` з відключеним стрімінгом. Якщо Ollama не запущено або `SERIES2_OLLAMA_MODEL` відсутній, цей шлях пропускається.

> [!NOTE]
> На цьому комп’ютері `phi4-mini:3.8b` завантажив близько 2.49 ГБ файлів моделі. Під час висновку Ollama повідомляв про 3.3 ГБ завантаженої моделі і використовував RTX 3060 Laptop GPU.

Це дає підручнику два рівні:

1. Детермінований конструктор відповіді виключно на CPU.
2. Локальна генерація відповіді з Ollama і Phi-4-mini.

Конвеєр витягування залишається однаковим в обох.

## 11. Результат перевірки

Я запускав ноутбук локально на Windows з Python 3.12.6.

Встановлені пакети:

| Пакет | Версія |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Виконання ноутбука:

- Ноутбук: `notebooks/series-2-open-source-rag.ipynb`
- Результат виконання: пройшов з `nbclient`
- Документів завантажено: 2
- Фрагментів створено: 8
- Колекція Qdrant: `school_policy_local`
- Векторів вставлено: 8
- Модель ембедінгів: `BAAI/bge-small-en-v1.5`
- Розмір ембедінгів: 384
- Питання для пошуку: "Чи можу я використовувати генеративний ШІ для мого фінального завдання?"
- Шлях повторного ранжування: легке локальне лексичне повторне ранжування
- Найкраще отримане джерело після повторного ранжування: `school_ai_policy.md`
- Найкращий отриманий розділ після повторного ранжування: `Final Assignments`
- Шлях формування стандартної відповіді: локальний прозорий композитор відповіді
- Шлях генерації Ollama: завершено з `phi4-mini:3.8b`
- Розмір файлу моделі Ollama: 2.49GB на диску
- Завантажений розмір моделі Ollama: 3.3GB за даними `ollama ps`
- Використання GPU: 100% GPU за даними `ollama ps`
- Використання пам’яті GPU після генерації: близько 3.5GB з 6GB на RTX 3060 Laptop GPU
- Виконання ноутбука з закешованою моделлю FastEmbed і ввімкненою генерацією Ollama: пройшло приблизно за 34 секунди через скрипт перевірки

Відповідь, згенерована Ollama:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Я не назвав би цю відповідь ідеальною. Вона відповідає на основі правильних доказів, але останній рядок джерела менш точний, ніж детермінований формат цитування. Це корисно показати в навчальному посібнику, бо це робить очевидним наступне інженерне питання: генерація відповіді також потребує оцінки, а не лише пошук.

Головне, що я зрозумів під час перевірки, це те, що якість пошуку слід перевіряти перед генерацією відповіді. Результат вбудовування вже був корисним, і легкий повторний ранжувальник надійно розміщував очікуваний розділ політики першим. Саме такого роду поведінка системи мені хочеться, щоб посібник виявляв, замість того, щоб її приховувати.

## 12. Що далі

Наступним покращенням буде порівняння цього локального налаштування з керованою версією Azure тієї ж самої ситуації з шкільним помічником політик. Збереження сценарію фіксованим має полегшити розуміння компромісів: складність налаштування, керування пошуком, інтеграція ідентичності, оперативне володіння та вартість.

## 13. Посилання

- [Швидкий старт з Qdrant Python клієнтом](https://python-client.qdrant.tech/quickstart.html)
- [GitHub репозиторій клієнта Qdrant](https://github.com/qdrant/qdrant-client)
- [Підтримувані моделі FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Посібник з вбудов OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Картка моделі BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Картка моделі BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Картка моделі sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Сторінка моделі Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Документація Ollama для Windows](https://docs.ollama.com/windows)
- [Документація Ollama API потокової передачі](https://docs.ollama.com/api/streaming)
- [Картка моделі Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Огляд LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Вступ до RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Попередня: [Серія 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:
Цей документ було перекладено за допомогою сервісу штучного інтелекту для перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->