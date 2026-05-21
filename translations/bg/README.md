# Научете ИИ да Отговаря на Въпроси Въз основа на Вашите Документи

Това хранилище събира серия от блогове от 2026 г. за изграждане на AI системи, базирани на документи, с RAG, Azure AI услуги, алтернативи с отворен код и работни процеси с фокус върху оценката.

## Обзор

През 2023 г. работих върху два урока за това как да научим ChatGPT да отговаря на въпроси от PDF документи, използвайки Azure AI Search и Azure OpenAI. Идеята за „ChatGPT върху вашите данни“ все още изглеждаше нова тогава, а целта беше да се покаже практичен работен процес: съхраняване на документи, индексиране, извличане на релевантно съдържание и генериране на отговори от този извлечен контекст.

През 2026 г. екосистемата RAG е много по-голяма. Azure AI Search поддържа съвременни векторни и хибридни модели за извличане, Azure OpenAI е част от по-голямата екосистема Microsoft Foundry Models, а инструменти с отворен код като LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama и vLLM са станали практични избори за реални системи.

Затова исках да разгледам тази тема отново. Въпросът вече не е само „Как да изградя RAG?“ Има вече много начини да го изградите, а по-важният въпрос е „Коя архитектура да избера за моя случай?“

Тази серия започва от този слой на вземане на решения. Преди да се навлиза дълбоко в имплементацията, тя разглежда защо AI услугите имат нужда от извличане, кога управляемите услуги на Azure са подходящи, кога алтернативите с отворен код са по-добър избор и къде се вписва фината настройка.

## Статии

1. [Серия 1: RAG, Azure срещу Алтернативи с Отворен Код и Кога Фината Настройка Има Смисъл](./series-1-rag-azure-open-source-fine-tuning.md)

## Поддръжка на Множество Езици

### Поддържа се чрез Co-op Translator (Автоматично и Винаги Актуално)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](./README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Предпочитате да клонирате локално?**
>
> Това хранилище включва преводи на 50+ езика, което значително увеличава размера на изтегляне. За да клонирате без преводи, използвайте sparse checkout:
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
> Това ви дава всичко необходимо, за да завършите курса с много по-бързо изтегляне.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:
Този документ е преведен с помощта на AI преводачески услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да е недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->