# Обучите ИИ отвечать на вопросы на основе ваших документов

![Обзор системы документ-ориентированного ИИ RAG](../../assets/images/readme-hero.svg)

Этот репозиторий собирает серию блогов 2026 года о создании документ-ориентированных ИИ-систем с использованием RAG, Azure AI сервисов, открытых альтернатив и ориентированных на оценку рабочих процессов.

## Введение

В 2023 году я работал над парой учебных материалов о том, как обучить ChatGPT отвечать на вопросы из PDF-документов с использованием Azure AI Search и Azure OpenAI. Тогда идея «ChatGPT на ваших данных» казалась новой, и цель заключалась в демонстрации практического рабочего процесса: хранить документы, индексировать их, получать релевантный контент и генерировать ответы на базе извлечённого контекста.

В 2026 году экосистема RAG значительно расширилась. Azure AI Search поддерживает современные векторные и гибридные шаблоны поиска, Azure OpenAI является частью более широкой экосистемы моделей Microsoft Foundry, а открытые инструменты, такие как LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama и vLLM, стали практичным выбором для реальных систем.

Именно поэтому я хотел вернуться к этой теме. Теперь вопрос уже не просто «Как построить RAG?». Теперь существует много способов построения, а более важный вопрос — «Какую архитектуру выбрать в моей ситуации?»

Этот сериал начинается с этого слоя принятия решений, а затем превращается в практические учебные материалы. Первый путь реализации строит локальную RAG-систему с открытым исходным кодом, которую каждый может запустить с примерами данных, Qdrant, Ollama и Phi-4-mini.

## Статьи

См. [articles/README.md](./articles/README.md) для индекса статей.

1. [Серия 1: RAG, Azure и открытые альтернативы, а также когда имеет смысл тонкая настройка](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Серия 2: Постройте локальную RAG-систему с открытым исходным кодом от начала до конца](./articles/series-2-open-source-rag-end-to-end.md)

Скоро выйдет:

- Перестроить ту же RAG-систему с Azure AI Search и Azure OpenAI.
- Добавить оценку и регрессионные проверки сверх демонстрационных ответов.

## Ноутбуки

В статьях реализации используются ноутбуки, чтобы можно было непосредственно проверить этапы поиска и оценки. См. [notebooks/README.md](./notebooks/README.md) для руководства по папке.

> [!TIP]
> Начинайте с Серии 2, если хотите самый быстрый путь. Она запускается локально с примерными данными, CPU-дружественными встраиваниями, локальным режимом Qdrant и без облачных учётных данных.

| Серия | Ноутбук | Требования | Локальная проверка |
| --- | --- | --- | --- |
| Серия 2 | [Ноутбук с открытым RAG](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Локальный режим Qdrant, поиск, переоценка и подключение источников проверены |

Чтобы запустить ноутбук локально, создайте виртуальное окружение и установите соответствующий файл требований. Например:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Пример данных

Ноутбуки используют небольшой локальный корпус в [sample_data](../../sample_data), чтобы примеры могли запускаться без приватных документов и облачных учётных данных. Смотрите [sample_data/README.md](./sample_data/README.md) для подробностей.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Итог локальной проверки

Результаты проверки фиксируются в каждой статье и в [SERIES_PLAN.md](./SERIES_PLAN.md).

| Область | Результат |
| --- | --- |
| Серия 2 — путь с открытым исходным кодом | FastEmbed сгенерировал локальные встраивания размером 384, в коллекцию Qdrant в памяти было вставлено 8 векторов, лёгкая переоценка вернула ожидаемый раздел; дополнительный генератор Ollama с `phi4-mini:3.8b` успешно выполнен |

Локальный ноутбук специально не содержит жестко зашитых секретов.

## Локальная генерация Ollama

Ноутбук из Серии 2 по умолчанию безопасен для локального запуска. Чтобы включить локальную генерацию Ollama, скопируйте [.env.example](../../.env.example) в `.env` и заполните значения для Серии 2.

Для генерации Ollama из Серии 2 раскомментируйте:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Ноутбук Серии 2 автоматически загружает `.env` из корня репозитория с помощью `python-dotenv`.

> [!IMPORTANT]
> Не коммитьте файлы `.env`, API-ключи, приватные конечные точки или значения, связанные с конкретным тенантом. Репозиторий специально держит секреты вне Markdown-файлов и ноутбуков.

Файлы требований документированы в [requirements/README.md](./requirements/README.md).

Чтобы проверить ссылки, структуру ноутбука, чистоту вывода ноутбука и модели секретов с высоким риском:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Скрипты проверки описаны в [scripts/README.md](./scripts/README.md).

Чтобы выполнить все безопасные локально ноутбуки в одной среде:

```powershell
python scripts\verify_notebooks.py --execute
```

Та же проверка запускается в GitHub Actions при пушах, пулл-реквестах и ручных вызовах рабочих процессов. Черновики статей и ноутбуков намеренно исключены из публичного пути проверки.

Перед публикацией обновлений пользуйтесь [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Смотрите [CHANGELOG.md](./CHANGELOG.md) для текущего непродвинутого списка изменений.

Для рекомендаций по участию и гигиене ноутбуков см. [CONTRIBUTING.md](./CONTRIBUTING.md).

## Многоязычная поддержка

### Поддерживается через Co-op Translator (автоматически и всегда актуально)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](./README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Предпочитаете клонировать локально?**
>
> Этот репозиторий включает более 50 переводов на разные языки, что значительно увеличивает размер загрузки. Чтобы клонировать без переводов, используйте sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Это даст вам всё необходимое для прохождения курса с намного более быстрой загрузкой.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->