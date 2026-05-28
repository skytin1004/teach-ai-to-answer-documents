# Научете AI да отговаря на въпроси въз основа на вашите документи
## Серия 2: Изграждане на локална отворена RAG система от край до край

![Локална отворена RAG учебна линия](../../../assets/images/series-2-local-rag.svg)

> Тази статия превръща дискусията за архитектурата от Серия 1 в изпълнима локална RAG учебна програма. Целта е първо да се изгради пълният работен процес с примерни данни, без облачен акаунт и без тайни, а след това да се използва тази работеща основа за вземане на по-добри архитектурни решения по-късно.

Системата, която ще изградим, е малък асистент за училищна политика. Използвам два локални документа в Markdown като база знания, след което преминавам през пълната RAG линия: разделяне на парчета, локални embedding-и, съхранение на вектори в Qdrant, извличане, повторно класиране, съставяне на отговор с позоваване на източника и опционално локално генериране с Ollama и Phi-4-mini.

Навигация в серията: [Начална страница на репозитория](../README.md) | Предишна: [Серия 1 - RAG, Azure срещу отвoрени алтернативи и кога има смисъл фина настройка](./series-1-rag-azure-open-source-fine-tuning.md)

Бележник: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Изисквания: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Това е най-добрата отправна точка, ако искате да разберете RAG линията, преди да създавате облачни ресурси. По подразбиране работи локално с CPU-приятелски embedding-и и без тайни.

## 1. Какво изграждаме

В учебното ръководство от 2023 започнах от Azure, защото целта беше да покажа как Azure AI Search и Azure OpenAI могат да отговарят на въпроси от PDF документи.

За тази серия 2026 искам да започна една стъпка по-ниско.

Преди да използвам управлявани услуги, искам да изградя малка RAG система локално и да направя всяка стъпка видима: зареждане на документи, разделяне на текст, съхраняване на вектори, извличане на доказателства, повторно класиране и връщане на отговор с позоваване на източника.

Примерният сценарий е училищен асистент за политика. Потребителят пита:

```text
Can I use generative AI for my final assignment?
```

Системата не трябва да отговаря от общата памет на модела. Тя трябва да извлече релевантния раздел от политиката и да отговори въз основа на този доказателствен материал.

Пълната изпълнима версия е в [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Кодът по-долу показва основните стъпки, за да може статията да се чете като учебник.

## 2. Инсталиране на локалните зависимости

Създайте виртуална среда и инсталирайте изискванията на Серия 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Първата версия използва Qdrant в локален режим и FastEmbed. Qdrant Python клиентът поддържа локален режим в паметта с `QdrantClient(":memory:")`, което е полезно за локални учебници и CI-стил проверка. FastEmbed ни дава истински локален embedding модел без нужда от облачен API ключ.

Във файла с изискванията е включен и `python-dotenv`, защото бележникът може опционално да чете име на Ollama модел от `.env`. За този локален учебник не е необходим Azure OpenAI или OpenAI API ключ.

## 3. Зареждане на примерните документи

Примерният корпус е умишлено малък:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

В бележника зареждам всички Markdown файлове от `sample_data/`:

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

Когато пуснах бележника, бяха заредени 2 документа. Това е достатъчно малко за ръчна проверка, което е полезно при изграждането на първата версия на RAG линия.

## 4. Разделяне по заглавия на Markdown

Следващата стъпка е да се разделят документите на парчета.

За този учебник използвам заглавията в Markdown като структурен сигнал. Заглавието на документа идва от `#`, а всяко параграфно парче идва от `##`.

> [!NOTE]
> Разделянето не е универсално. В този учебник използвам заглавия от Markdown, защото примерните документи имат ясна структура с `#` и `##`. За PDF, Word документи, слайдове, билети или уеб страници, по-добрата стратегия може да използва граници на страници, информация за оформление, семантични секции, лимити на токени, таблици или метаданни. Важното е да изберете стратегия за разделяне, която запазва значението и възможността за проследяване на източника за вашите документи.

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

След това го прилагам за всеки документ:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Това създаде 8 парчета при локално изпълнение.

Това, което ми хареса в тази стъпка, е че метаданните вече са полезни. Всяко парче знае своя `source`, `sectionHeading`, `documentVersion` и заслонен `permissions`. Дори в малък учебник това улеснява позоваванията и по-късното извличане с внимание към разрешения.

## 5. Създаване на локални embedding-и

За първата публична версия използвам `BAAI/bge-small-en-v1.5` чрез FastEmbed.

Това поддържа учебната програма локална и CPU-приятелска, но все пак използва реален embedding модел, а не демонстративна векторна функция. Първото пускане изтегля теглата на модела. След това бележникът може да използва локалния кеш.

> [!NOTE]
> Използвам `BAAI/bge-small-en-v1.5`, защото е лек английски embedding модел, който работи добре с FastEmbed и Qdrant за локален учебник. Той създава 384-измерни вектори, което държи примера бърз и евтин за локално изпълнение. Това не е единственият добър избор. През 2023 много учебници използваха хоствани embedding модели като `text-embedding-ada-002`. Днес по-нови хоствани опции като OpenAI `text-embedding-3-small` и `text-embedding-3-large`, както и отворени варианти като BGE, E5, MiniLM, Nomic Embed и многоезични модели като `BAAI/bge-m3` са разумен избор в зависимост от натоварването. В продукция правилният embedding модел трябва да се избира чрез оценка на извличането върху вашите собствени документи.

Някои практични алтернативи:

| Семейство модели | Кога бих го разгледал |
| --- | --- |
| `text-embedding-ada-002` | Стар хостван базов модел, който се появяваше в много учебници от 2023. Днес не бих го избрал като подразбиране за нов учебник. |
| `text-embedding-3-small` | Модерен хостван стандарт, когато искам добро съотношение цена/производителност и не ми трябват само локални embedding-и. |
| `text-embedding-3-large` | Хостван вариант, когато качеството на извличане е по-важно от размера на вектора или цената на embedding-а. |
| `BAAI/bge-small-en-v1.5` | Лек локален английски модел за учебници, прототипи и CPU-приятелски експерименти. |
| `BAAI/bge-base-en-v1.5` или `BAAI/bge-large-en-v1.5` | По-големи локални английски модели за по-добро качество на извличане, ако мога да си позволя повече изчисления. |
| `BAAI/bge-m3` | Многоезично или извличане с по-дълъг контекст, особено когато документите не са само на английски. |
| `sentence-transformers/all-MiniLM-L6-v2` | Много малък и бърз семантичен базов модел за търсене. Полезен, когато скоростта и простотата са най-важни. |
| `nomic-embed-text-v1.5` | Отворен локален embedding вариант, който си струва да бъде изпробван за по-дълъг контекст или настройки, ориентирани към преносимост. |

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

След това всяко парче получава embedding:

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

## 6. Съхраняване на вектори в Qdrant локален режим

Сега създаваме колекция в паметта на Qdrant и вмъкваме парчетата с метаданни за натоварване.

> [!NOTE]
> В учебника от 2023 използвах FAISS, защото беше прост и популярен начин да демонстрирам локално търсене по векторна прилика с LangChain. FAISS е все още полезен за бързи локални експерименти. В тази версия 2026 използвам Qdrant, защото искам учебникът да се усеща по-близо до продукционна RAG система. Qdrant ми позволява да съхранявам вектори заедно с метаданни като източников файл, заглавие на секция, версия на документа и разрешения. Това прави извличането по-лесно за преглед и подготвя примера за филтриране, цитиране и бъдещи персистентни или сървърно-базирани внедрявания.

FAISS е отличен за показване на търсене по векторна прилика. Qdrant е по-добър за демонстриране на малък, но продукционно оформен слой за извличане в RAG.

Някои практични алтернативи:

| Векторна база / търсещ слой | Кога бих го разгледал |
| --- | --- |
| Qdrant | Локални прототипи, филтриране по метаданни, продукционно приятелско векторно търсене и прост Python работен процес. |
| Chroma | Бързи локални RAG експерименти и бележници, където простотата е най-важна. |
| FAISS | Леко локално търсене по вектори, когато ми трябва само търсене по прилика и мога да управлявам метаданните отделно. |
| Milvus | По-голямо отворено векторно търсене, когато екипът е готов да оперира с посветена векторна база данни. |
| Weaviate | Векторно търсене със схема, метаданни, хибридно търсене и възможности за управлявани или самостоятелно хоствани внедрявания. |
| Azure AI Search | Корпоративен RAG в Azure, когато искам ключово търсене, векторно търсене, хибридно извличане, семантично ранжиране, филтриране, сигурност и управлявани операции в един слой за търсене. |
| PostgreSQL + pgvector | Екипи, които вече използват PostgreSQL и искат векторно търсене близо до данните на приложението. |

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

След това вмъкнете точките:

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

В моя случай колекцията вмъкна 8 вектора.

Тук RAG системата започва да става инспекционна. Векторната база данни не съхранява само вектори, а и доказателствения текст и необходимите метаданни за цитиране.

## 7. Извличане на кандидат-парчета

Сега задаваме въпроса и извличаме кандидат-парцели.

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

В този момент отпечатвам извлечените парчета преди генериране на отговор. Това е важно. Ако извличането е грешно, генерирането само ще скрие проблема зад течен текст.

## 8. Добавяне на лек reranker

Когато първоначално тествах пътя на извличане, само векторната прилика намираше свързано съдържание на политиката, но най-прецизният раздел не винаги беше на върха.

Затова добавих малък локален повторен класификатор. Той дава допълнително тегло, когато термините от въпроса се припокриват със заглавието на секцията и съдържанието.

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

След повторното класиране топ резултатът беше:

```text
school_ai_policy.md / Final Assignments
```

Това беше очакваният раздел за тестовия въпрос.

Това беше най-полезният урок от първото внедряване. Дори в малък локален пример качеството на извличане се подобри, когато комбинирах векторната прилика с друг сигнал.

## 9. Съставяне на локален отговор с доказателства

За подразбиращия се път използвам прозрачен локален композитор на отговори вместо LLM.

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

Това не е предназначено да бъде генератор на окончателни отговори. Това е инструмент за отстраняване на грешки. Той доказва, че извличането, метаданните и свързването с цитирания работят преди да се добави вариабилност на модела.

## 10. Генериране на локален отговор с Ollama и Phi-4-mini

Когато извличането работи, бележникът може да замени само крайната стъпка за отговор с Ollama и `phi4-mini:3.8b`.

> [!NOTE]
> Ollama трябва да замества само крайната стъпка за генериране на отговор. Зареждането на документи, разделянето на парчета, съхранението на вектори, извличането, повторното класиране и свързването с цитатите трябва да останат същите.

Първо бележникът изгражда подсещане за доказателствата от извлечените парчета:

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

За този учебник препоръчвам семейството Phi-4-mini на Microsoft чрез Ollama като опция по подразбиране за локално генериране. В Ollama, тестваният модел е:

```powershell
ollama pull phi4-mini:3.8b
```

Бързо можете да проверите дали моделът е наличен:

```powershell
ollama list
```

След това задайте тези променливи:

```powershell
Copy-Item .env.example .env
```

Отворете `.env` и премахнете коментара на стойностите за Ollama в Серия 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Бележникът зарежда `.env` от корена на репозитория с `python-dotenv`, след което изпраща същото подсещане за доказателства до локалната крайна точка `/api/chat` на Ollama с изключено стриймване. Ако Ollama не работи или `SERIES2_OLLAMA_MODEL` липсва, този път се пропуска.

> [!NOTE]
> На този компютър `phi4-mini:3.8b` изтегли около 2.49GB моделни файлове. По време на инференция Ollama докладва за 3.3GB зареден модел и използване на RTX 3060 Laptop GPU.

Това дава два слоя на учебника:

1. Детеминиран композитор на отговори, изцяло на CPU.
2. Локално генериране на отговори с Ollama и Phi-4-mini.

Линията за извличане остава една и съща и в двата варианта.

## 11. Резултат от проверката

Пуснах бележника локално на Windows с Python 3.12.6.

Инсталирани пакети:

| Пакет | Версия |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Изпълнение на бележника:

- Бележник: `notebooks/series-2-open-source-rag.ipynb`
- Резултат от изпълнението: успешен с `nbclient`
- Заредени документи: 2
- Създадени парчета: 8
- Qdrant колекция: `school_policy_local`
- Вмъкнати вектори: 8
- Модел за embedding: `BAAI/bge-small-en-v1.5`
- Размер на embedding: 384
- Въпрос за извличане: "Мога ли да използвам генеративен AI за моята крайна задача?"
- Път за преподреждане: леко локално лексикално преподреждане
- Най-добър извлечен източник след преподреждането: `school_ai_policy.md`
- Най-добър извлечен раздел след преподреждането: `Final Assignments`
- Стандартен път за отговор: локален прозрачен композитор на отговори
- Път на генериране с Ollama: завършен с `phi4-mini:3.8b`
- Размер на модела Ollama на диска: 2.49GB
- Размер на заредения модел Ollama: 3.3GB според `ollama ps`
- Офлоуд на GPU: 100% GPU според `ollama ps`
- Използвана памет на GPU след генериране: около 3.5GB от 6GB използвани на RTX 3060 Laptop GPU
- Изпълнение на ноутбука с кеширан модел FastEmbed и разрешено генериране с Ollama: успешно за около 34 секунди чрез скрипта за проверка

Отговорът, генериран от Ollama, беше:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Не бих нарекъл този отговор перфектен. Той отговаря въз основа на правилните доказателства, но последният ред източник е по-малко прецизен от детерминистичния формат за цитиране. Това е полезно да се покаже в урока, защото прави следващия инженеринг въпрос очевиден: генерирането на отговора също се нуждае от оценка, а не само извличането.

Основното нещо, което научих при проверката, е, че качеството на извличане трябва да се проверява преди генерирането на отговор. Резултатът от вграждането вече беше полезен, а лекото преподреждане надеждно направи очаквания раздел на политиката да се появи първо. Това е точно видът малко поведение на системата, който искам урокът да разкрие вместо да го крие.

## 12. Какво следва

Следващото подобрение е да се сравни тази локална настройка с управлявана версия в Azure на същия сценарий за помощник с училищна политика. Запазването на сценариото фиксирано трябва да направи по-лесно видими компромисите: сложност на настройката, контрол на извличането, интеграция на идентичността, експлоатационна собственост и разходи.

## 13. Източници

- [Бърз старт с Qdrant Python клиент](https://python-client.qdrant.tech/quickstart.html)
- [GitHub хранилище на Qdrant клиента](https://github.com/qdrant/qdrant-client)
- [Поддържани модели на FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Ръководство за вгражданията на OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Картичка на модела BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Картичка на модела BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Картичка на модела sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Страница на модела Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Документация на Ollama за Windows](https://docs.ollama.com/windows)
- [Документация за Ollama API за стрийминг](https://docs.ollama.com/api/streaming)
- [Картичка на модела Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Преглед на LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Въведение в RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Предишна: [Серия 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:
Този документ е преведен с помощта на AI преводачески услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да е недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->