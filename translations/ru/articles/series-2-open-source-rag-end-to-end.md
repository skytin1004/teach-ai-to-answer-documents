# Обучите ИИ отвечать на вопросы на основе ваших документов
## Серия 2: Полное создание локальной RAG-системы с открытым исходным кодом

![Локальный учебный конвейер RAG с открытым исходным кодом](../../../assets/images/series-2-local-rag.svg)

> Эта статья превращает обсуждение архитектуры из Серии 1 в исполняемый локальный учебник по RAG. Цель — сначала построить полный рабочий процесс с примерными данными, без облачного аккаунта и секретов, а затем использовать эту рабочую базу для более обоснованных архитектурных решений в дальнейшем.

Система, которую мы построим, — это небольшой помощник по школьной политике. Я использую два локальных документа в формате Markdown в качестве базы знаний, а затем прохожу весь конвейер RAG: разбиение на части, локальные эмбеддинги, векторное хранилище Qdrant, извлечение, переоценку, создание ответа с учётом источника и опциональную локальную генерацию с Ollama и Phi-4-mini.

Навигация по серии: [Домашняя страница репозитория](../README.md) | Предыдущая: [Серия 1 - RAG, Azure против альтернатив с открытым исходным кодом и когда уместна дообучение](./series-1-rag-azure-open-source-fine-tuning.md)

Тетрадь: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Требования: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Это лучшая отправная точка, если вы хотите понять конвейер RAG до создания облачных ресурсов. По умолчанию всё запускается локально с CPU-дружественными эмбеддингами и без секретов.

## 1. Что мы строим

В учебнике 2023 года я начал с Azure, потому что целью было показать, как Azure AI Search и Azure OpenAI могут отвечать на вопросы из PDF-документов.

Для этой серии 2026 года я хочу начать на один уровень ниже.

Прежде чем использовать управляемые сервисы, я хочу локально построить небольшую RAG-систему и сделать каждый шаг видимым: загрузка документов, разбиение текста на части, хранение векторов, извлечение доказательств, переоценка результатов и возврат ответа с учётом источника.

Примерный сценарий — помощник по школьной политике. Пользователь спрашивает:

```text
Can I use generative AI for my final assignment?
```

Система не должна отвечать на основе общей памяти модели. Она должна извлечь соответствующий раздел политики и ответить, используя эти доказательства.

Полная исполняемая версия находится в [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Код ниже показывает основные шаги, чтобы статья читалась как учебник.

## 2. Установка локальных зависимостей

Создайте виртуальное окружение и установите требования Серии 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Первая версия использует локальный режим Qdrant и FastEmbed. Python-клиент Qdrant поддерживает локальный режим в памяти через `QdrantClient(":memory:")`, что полезно для локальных учебников и проверки в стиле CI. FastEmbed даёт нам реальную локальную модель эмбеддингов без необходимости ключа облачного API.

Файл требований также включает `python-dotenv`, потому что тетрадь может опционально читать имя модели Ollama из `.env`. Для этого локального учебника ключи Azure OpenAI или OpenAI API не требуются.

## 3. Загрузка примерных документов

Примерный корпус намеренно небольшой:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

В тетради я загружаю все файлы Markdown из `sample_data/`:

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

Когда я запускал тетрадь, она загрузила 2 документа. Это достаточно мало, чтобы проверить вручную, что полезно при создании первой версии конвейера RAG.

## 4. Разбиение по заголовкам Markdown

Следующий шаг — разделить документы на части.

В этом учебнике я использую заголовки Markdown как сигнал структуры. Заголовок документа берётся из `#`, а каждый раздел — из `##`.

> [!NOTE]
> Разбиение не универсально. В этом учебнике я использую заголовки Markdown, потому что примерные документы имеют чёткую структуру `#` и `##`. Для PDF, Word-документов, слайдов, тикетов или веб-страниц лучшая стратегия может использовать границы страниц, информацию о раскладке, семантические разделы, лимиты по токенам, таблицы или метаданные. Главное — выбрать стратегию разбиения, которая сохраняет смысл и прослеживаемость источника для ваших документов.

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

Затем я применяю это к каждому документу:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

В моём локальном запуске это создало 8 частей.

Что мне понравилось на этом шаге, так это то, что метаданные уже полезны. Каждая часть знает свой `source`, `sectionHeading`, `documentVersion` и заполнитель `permissions`. Даже в маленьком учебнике это облегчает ссылки и позднее извлечение с учётом разрешений.

## 5. Создание локальных эмбеддингов

Для первой публичной версии я использую `BAAI/bge-small-en-v1.5` через FastEmbed.

Это сохраняет учебник локальным и CPU-дружественным, но всё ещё использует реальную модель эмбеддингов вместо подставной функции векторов. При первом запуске веса модели загружаются. После этого тетрадь может повторно использовать локальный кэш.

> [!NOTE]
> Я использую `BAAI/bge-small-en-v1.5`, потому что это лёгкая английская модель эмбеддингов, которая хорошо работает с FastEmbed и Qdrant для локального учебника. Она создаёт 384-мерные векторы, что делает пример быстрым и недорогим для локального запуска. Это не единственный хороший выбор. В 2023 году многие учебники использовали размещённые модели эмбеддингов, такие как `text-embedding-ada-002`. Сегодня более новые размещённые варианты, такие как OpenAI `text-embedding-3-small` и `text-embedding-3-large`, а также открытые варианты, такие как BGE, E5, MiniLM, Nomic Embed и многоязычные модели вроде `BAAI/bge-m3`, все являются разумными вариантами в зависимости от нагрузки. В производстве правильная модель эмбеддингов должна выбираться на основе оценки извлечения по вашим собственным документам.

Практические альтернативы:

| Семейство моделей | Когда я бы рассматривал |
| --- | --- |
| `text-embedding-ada-002` | Старый размещённый базовый вариант, который встречался во многих учебниках 2023 года. Я бы не выбрал его по умолчанию для нового учебника сегодня. |
| `text-embedding-3-small` | Современный размещённый вариант по умолчанию, когда нужен хороший баланс цена/качество и не обязательны только локальные эмбеддинги. |
| `text-embedding-3-large` | Размещённый вариант, когда качество извлечения важнее размера вектора или стоимости эмбеддинга. |
| `BAAI/bge-small-en-v1.5` | Лёгкий локальный английский базовый вариант для учебников, прототипов и CPU-дружественных экспериментов. |
| `BAAI/bge-base-en-v1.5` или `BAAI/bge-large-en-v1.5` | Более крупные локальные английские модели, когда нужно лучшее качество извлечения и достаточно вычислительных ресурсов. |
| `BAAI/bge-m3` | Многоязычный или для работы с более длинным контекстом, особенно если документы не только на английском. |
| `sentence-transformers/all-MiniLM-L6-v2` | Очень маленький и быстрый базовый вариант семантического поиска. Полезен, когда важна скорость и простота. |
| `nomic-embed-text-v1.5` | Открытый локальный вариант эмбеддинга, который стоит протестировать для более длинного контекста или портативных настроек. |

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

Затем каждой части присваивается эмбеддинг:

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

## 6. Хранение векторов в локальном режиме Qdrant

Теперь создаём коллекцию Qdrant в памяти и вставляем части с метаданными в полезной нагрузке.

> [!NOTE]
> В учебнике 2023 года я использовал FAISS, потому что это был простой и популярный способ показать локальный поиск векторов по сходству с LangChain. FAISS всё ещё полезен для быстрых локальных экспериментов. В этой версии 2026 года я использую Qdrant, потому что хочу, чтобы учебник был ближе к производственной системе RAG. Qdrant позволяет хранить векторы вместе с метаданными полезной нагрузки, такими как исходный файл, заголовок раздела, версия документа и разрешения. Это облегчает инспекцию извлечения и подготавливает пример к фильтрации, ссылкам и будущему постоянному или серверному развертыванию.

FAISS отлично подходит для демонстрации поиска по сходству векторов. Qdrant лучше для демонстрации небольшого, но приближенного к производству слоя извлечения RAG.

Практические альтернативы:

| Векторное хранилище / слой поиска | Когда я бы рассматривал |
| --- | --- |
| Qdrant | Локальные прототипы, фильтрация по метаданным, производительный векторный поиск и простой Python-воркфлоу. |
| Chroma | Быстрые локальные эксперименты RAG и тетради, где важна простота. |
| FAISS | Лёгкий локальный векторный поиск, если нужен только поиск по сходству и можно отдельно управлять метаданными. |
| Milvus | Векторы большого масштаба с открытым исходным кодом, когда команда готова управлять выделенной векторной базой данных. |
| Weaviate | Векторный поиск со схемой, метаданными, гибридным поиском и вариантами управляемого или самостоятельного развертывания. |
| Azure AI Search | Корпоративный RAG на Azure, когда нужны поиск по ключевым словам, векторный поиск, гибридное извлечение, семантический рейтинг, фильтрация, безопасность и управляемые операции в одном слое поиска. |
| PostgreSQL + pgvector | Команды, которые уже используют PostgreSQL и хотят векторный поиск рядом с данными приложения. |

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

Затем вставляем точки:

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

В моём запуске коллекция вставила 8 векторов.

Здесь RAG-система становится более обозримой. Векторная база данных хранит не только векторы, но и текст доказательств с метаданными, необходимыми для ссылок.

## 7. Извлечение кандидатных частей

Теперь задаём вопрос и извлекаем кандидатные части.

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

На этом этапе я вывожу извлечённые части перед генерацией ответа. Это важно. Если извлечение неверно, генерация просто скроет проблему за плавным текстом.

## 8. Добавление лёгкого повторного ранжирования

Когда я впервые тестировал путь извлечения, только векторное сходство находило связанный контент политики, но самый точный раздел не всегда был сверху.

Поэтому я добавил небольшой локальный повторный ранжировщик. Он даёт дополнительный вес, если термины вопроса пересекаются с заголовком раздела и содержимым.

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

После повторного ранжирования топ-результат стал:

```text
school_ai_policy.md / Final Assignments
```

Это был ожидаемый раздел для тестового вопроса.

Это был самый полезный урок из первой реализации. Даже в маленьком локальном примере качество извлечения улучшалось, когда я комбинировал векторное сходство с другим сигналом.

## 9. Составление обоснованного локального ответа

По умолчанию я использую прозрачный локальный композитор ответа вместо LLM.

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

Это не предназначено быть генератором финального ответа. Это инструмент отладки. Он доказывает, что извлечение, метаданные и связь по цитатам работают перед добавлением вариативности модели.

## 10. Генерация локального ответа с Ollama и Phi-4-mini

Когда извлечение работает, тетрадь может заменить только последний шаг ответа на Ollama и `phi4-mini:3.8b`.

> [!NOTE]
> Ollama должен заменять только финальный шаг генерации ответа. Загрузка документов, разбиение, хранение векторов, извлечение, переоценка и связь по цитатам должны оставаться без изменений.

Сначала тетрадь собирает подсказку с доказательствами из извлечённых частей:

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

Для этого учебника я рекомендую семейство Phi-4-mini компании Microsoft через Ollama в качестве варианта локальной генерации по умолчанию. В Ollama модель, которую я тестировал, называется:

```powershell
ollama pull phi4-mini:3.8b
```

Вы можете быстро проверить доступность модели:

```powershell
ollama list
```

Затем установите эти переменные:

```powershell
Copy-Item .env.example .env
```

Откройте `.env` и раскомментируйте значения Ollama для Серии 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Тетрадь загружает `.env` из корня репозитория с помощью `python-dotenv`, затем отправляет ту же подсказку с доказательствами в локальный эндпоинт Ollama `/api/chat` с отключённой трансляцией. Если Ollama не запущена или отсутствует `SERIES2_OLLAMA_MODEL`, этот путь пропускается.

> [!NOTE]
> На этой машине `phi4-mini:3.8b` загрузил примерно 2.49 ГБ файлов модели. При инференсе Ollama сообщила о размере загруженной модели 3.3 ГБ и использовала GPU RTX 3060 Laptop.

Это даёт учебнику два уровня:

1. Только CPU, детерминированный композитор ответа.
2. Локальная генерация ответа с Ollama и Phi-4-mini.

Конвейер извлечения остаётся одинаковым в обоих.

## 11. Результат проверки

Я запускал тетрадь локально на Windows с Python 3.12.6.

Установленные пакеты:

| Пакет | Версия |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Исполнение тетради:

- Тетрадь: `notebooks/series-2-open-source-rag.ipynb`
- Результат выполнения: успешно с использованием `nbclient`
- Загружено документов: 2
- Создано частей: 8
- Коллекция Qdrant: `school_policy_local`
- Векторов вставлено: 8
- Модель эмбеддинга: `BAAI/bge-small-en-v1.5`
- Размер эмбеддинга: 384
- Вопрос по поиску: «Могу ли я использовать генеративный ИИ для моего итогового задания?»
- Путь переоценки: лёгкая локальная лексическая переоценка
- Лучший полученный источник после переоценки: `school_ai_policy.md`
- Лучший полученный раздел после переоценки: `Final Assignments`
- Путь ответа по умолчанию: локальный прозрачный составитель ответов
- Путь генерации Ollama: выполнено с `phi4-mini:3.8b`
- Размер модели Ollama в файле: 2.49GB на диске
- Загруженный размер модели Ollama: 3.3GB по данным `ollama ps`
- Выгрузка на GPU: 100% на GPU по данным `ollama ps`
- Используемая память GPU после генерации: около 3.5GB из 6GB на RTX 3060 Laptop GPU
- Выполнение ноутбука с кэшированной моделью FastEmbed и включённой генерацией Ollama: прошло за примерно 34 секунды через скрипт проверки

Ответ, сгенерированный Ollama, был:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Я бы не назвал этот ответ идеальным. Он даёт ответ на основе правильных доказательств, но окончательная строка источника менее точна, чем детерминированный формат цитирования. Это полезно показать в руководстве, поскольку это делает следующий вопрос по инженерии очевидным: генерация ответов тоже нуждается в оценке, а не только поиск.

Главное, что я узнал при проверке этого, — это то, что качество поиска следует проверять до генерации ответов. Результат встраивания уже был полезен, а лёгкий переоценщик сделал так, что ожидаемый раздел политики надёжно появился первым. Именно такого рода мелкое поведение системы я хочу, чтобы руководство показывало, а не скрывало.

## 12. Что дальше

Следующее улучшение — сравнить эту локальную настройку с управляемой версией Azure для того же сценария помощника школьной политики. Сохранение сценария фиксированным должно облегчить понимание компромиссов: сложность настройки, управление поиском, интеграция идентификации, операционное владение и стоимость.

## 13. Ссылки

- [Быстрый старт с клиентом Qdrant на Python](https://python-client.qdrant.tech/quickstart.html)
- [Репозиторий клиента Qdrant на GitHub](https://github.com/qdrant/qdrant-client)
- [Поддерживаемые модели FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Руководство по встраиваниям OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 модельная карточка](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 модельная карточка](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 модельная карточка](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Страница модели Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Документация Ollama для Windows](https://docs.ollama.com/windows)
- [Документация по потоковому API Ollama](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct модельная карточка](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Обзор LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Введение в RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Предыдущий: [Серия 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->