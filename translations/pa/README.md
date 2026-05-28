# ਆਪਣੀ ਦਸਤਾਵੇਜ਼ਾਂ ਦੇ ਆਧਾਰ 'ਤੇ ਪ੍ਰਸ਼ਨਾਂ ਦੇ ਜਵਾਬ ਦੇਣ ਲਈ AI ਨੂੰ ਸਿੱਖਾਓ

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

ਇਹ ਰਿਪੋਜ਼ਿਟਰੀ 2026 ਦੀ ਇੱਕ ਬਲੌਗ ਸੀਰੀਜ਼ ਇਕੱਠੀ ਕਰਦੀ ਹੈ ਜੋ RAG, Azure AI ਸੇਵਾਵਾਂ, ਖੁੱਲ੍ਹੇ ਸ્રੋਤ ਵਿਕਲਪਾਂ ਅਤੇ ਮੂਲਾਂਕਣ-ਕੇਂਦਰਿਤ ਵਰਕਫਲੋਜ਼ ਦੇ ਨਾਲ ਦਸਤਾਵੇਜ਼-ਆਧਾਰਿਤ AI ਸਿਸਟਮ ਬਣਾਉਣ ਬਾਰੇ ਹੈ।

## ਪਿਛੋਕੜ

2023 ਵਿੱਚ, ਮੈਂ Azure AI Search ਅਤੇ Azure OpenAI ਦੀ ਵਰਤੋਂ ਕਰਕੇ PDF ਦਸਤਾਵੇਜ਼ਾਂ ਤੋਂ ਪ੍ਰਸ਼ਨਾਂ ਦੇ ਜਵਾਬ ਦੇਣ ਲਈ ChatGPT ਸਿੱਖਾਉਣ ਬਾਰੇ ਇੱਕ ਜੋੜਾ ਟਿਊਟੋਰਿਅਲ 'ਤੇ ਕੰਮ ਕੀਤਾ। "ਤੁਹਾਡੇ ਡੇਟਾ ਉੱਤੇ ChatGPT" ਦਾ ਵਿਚਾਰ ਉਸ ਸਮੇਂ ਨਵਾਂ ਲੱਗਦਾ ਸੀ, ਅਤੇ ਲਕੜੀ ਇਹ ਸੀ ਕਿ ਇੱਕ ਪ੍ਰਯੋਗਿਕ ਵਰਕਫਲੋ ਦਿਖਾਇਆ ਜਾਵੇ: ਦਸਤਾਵੇਜ਼ਾਂ ਨੂੰ ਸਟੋਰ ਕਰਨਾ, ਉਨ੍ਹਾਂ ਨੂੰ ਇੰਡੈਕਸ ਕਰਨਾ, ਸਬੰਧਤ ਸਮੱਗਰੀ ਨੂੰ ਪ੍ਰਾਪਤ ਕਰਨਾ ਅਤੇ ਉਸ ਪ੍ਰਾਪਤ ਸੰਦਰਭ ਤੋਂ ਜਵਾਬ ਬਣਾਉਣਾ।

2026 ਵਿੱਚ, RAG ਪਰਿਭਾਸ਼ਾ ਕਾਫੀ ਵੱਡੀ ਹੋ ਗਈ ਹੈ। Azure AI Search ਆਧੁਨਿਕ ਵੈਕਟਰ ਅਤੇ ਹਾਇਬ੍ਰਿਡ ਰੀਟਰੀਵਲ ਪੈਟਰਨਾਂ ਨੂੰ ਸਮਰਥਨ ਦਿੰਦਾ ਹੈ, Azure OpenAI Microsoft Foundry ਮਾਡਲ ਸਾਮਰਾਜ ਦਾ ਹਿੱਸਾ ਹੈ, ਅਤੇ ਹੋਰ ਖੁੱਲ੍ਹੇ ਸ੍ਰੋਤ ਦੇ ਟੂਲ ਜਿਵੇਂ LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, ਅਤੇ vLLM ਹਕੀਕਤੀ ਸਿਸਟਮਾਂ ਲਈ ਵਰਤੋਂਯੋਗ ਚੋਣਾਂ ਬਨ ਗਏ ਹਨ।

ਇਸ ਲਈ ਮੈਂ ਇਸ ਵਿਸ਼ੇ ਨੂੰ ਦੁਬਾਰਾ ਦੇਖਣਾ ਚਾਹੁੰਦਾ ਹਾਂ। ਪ੍ਰਸ਼ਨ ਹੁਣ ਸਿਰਫ਼ "ਮੈਂ RAG ਕਿਵੇਂ ਬਣਾਵਾਂ?" ਨਹੀਂ ਰਹ ਗਿਆ। ਹੁਣ ਕਈ ਤਰੀਕੇ ਹਨ ਇਸਨੂੰ ਬਣਾਉਣ ਦੇ, ਅਤੇ ਸਭ ਤੋਂ ਜਰੂਰੀ ਹੈ "ਮੇਰੇ ਹਾਲਾਤ ਲਈ ਕਿਹੜਾ ਆਰਕੀਟੈਕਚਰ ਚੁਣਨਾ ਚਾਹੀਦਾ ਹੈ?"

ਇਹ ਸੀਰੀਜ਼ ਇਸ ਫੈਸਲੇ ਦੇਤਰ ਤੋਂ ਸ਼ੁਰੂ ਹੁੰਦੀ ਹੈ, ਅਤੇ ਫਿਰ ਇਸਨੂੰ ਹੈਂਡਜ਼-ਆਨ ਟਿਊਟੋਰਿਅਲਾਂ ਵਿੱਚ ਬਦਲਦੀ ਹੈ। ਪਹਿਲਾ ਇੰਪਲੀਮੈਂਟੇਸ਼ਨ ਰਸਤਾ ਇੱਕ ਲੋਕਲ ਖੁੱਲ੍ਹਾ ਸ੍ਰੋਤ RAG ਸਿਸਟਮ ਬਣਾਉਂਦਾ ਹੈ ਜੋ ਕੋਈ ਵੀ ਨਮੂਨਾ ਡੇਟਾ, Qdrant, Ollama, ਅਤੇ Phi-4-mini ਨਾਲ ਚਲਾ ਸਕਦਾ ਹੈ।

## ਲੇਖ

ਲੇਖਾਂ ਦੀ ਸੂਚੀ ਲਈ ਵੇਖੋ [articles/README.md](./articles/README.md)।

1. [ਸੀਰੀਜ਼ 1: RAG, Azure ਵਿਰੁੱਧ ਖੁੱਲ੍ਹਾ-ਸ੍ਰੋਤ ਵਿਕਲਪ, ਅਤੇ ਜਦੋਂ ਫਾਈਨ-ਟਿਊਨਿੰਗ ਸਮਝਦਾਰ ਹੁੰਦੀ ਹੈ](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [ਸੀਰੀਜ਼ 2: ਇੱਕ ਲੋਕਲ ਖੁੱਲ੍ਹਾ-ਸ੍ਰੋਤ RAG ਸਿਸਟਮ ਮੁਕੰਮਲ ਤੌਰ 'ਤੇ ਬਣਾਓ](./articles/series-2-open-source-rag-end-to-end.md)

ਅਗਲਾ ਆਉਣ ਵਾਲਾ:

- ਉਸੇ RAG ਸਿਸਟਮ ਨੂੰ Azure AI Search ਅਤੇ Azure OpenAI ਨਾਲ ਮੁੜ ਬਣਾਓ।
- ਡੈਮੋ ਜਵਾਬ ਤੋਂ ਅੱਗੇ ਮੂਲਾਂਕਣ ਅਤੇ ਰਿਗ੍ਰੈਸ਼ਨ ਚੈੱਕ ਸ਼ਾਮਲ ਕਰੋ।

## ਨੋਟਬੁੱਕ

ਇੰਪਲੀਮੈਂਟੇਸ਼ਨ ਲੇਖਾਂ ਵਿੱਚ ਨੋਟਬੁੱਕ ਵਰਤੇ ਜਾਂਦੇ ਹਨ ਤਾਂ ਜੋ ਰੀਟਰੀਵਲ ਅਤੇ ਮੂਲਾਂਕਣ ਦੇ ਕਦਮ ਸਿੱਧਾ ਨਿਰੀਖਣ ਕੀਤਾ ਜਾ ਸਕੇ। ਫੋਲਡਰ-ਸਤਰ ਦੀ ਮਦਦ ਲਈ ਵੇਖੋ [notebooks/README.md](./notebooks/README.md)।

> [!TIP]
> ਜੇ ਤੁਸੀਂ ਸਭ ਤੋਂ ਤੇਜ਼ ਰਸਤਾ ਚਾਹੁੰਦੇ ਹੋ ਤਾਂ ਸੀਰੀਜ਼ 2 ਨਾਲ ਸ਼ੁਰੂ ਕਰੋ। ਇਹ ਨਮੂਨਾ ਡੇਟਾ, CPU-ਮਿਤਰ ਕੈਂਪਿੰਗ, Qdrant ਲੋਕਲ ਮੋਡ ਅਤੇ ਕੋਈ ਕਲਾਉਡ ਸੰਦਰਭ ਨਹੀਂ ਮਿਲਾਉਂਦਾ।

| ਸੀਰੀਜ਼ | ਨੋਟਬੁੱਕ | ਲੋੜੀਂਦੇ | ਲੋਕਲ ਪ੍ਰਮਾਣਿਕਤਾ |
| --- | --- | --- | --- |
| ਸੀਰੀਜ਼ 2 | [ਖੁੱਲ੍ਹਾ-ਸ੍ਰੋਤ RAG ਨੋਟਬੁੱਕ](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant ਲੋਕਲ ਮੋਡ, ਰੀਟਰੀਵਲ, ਰੀਰੈਂਕਿੰਗ ਅਤੇ ਸਰੋਤ ਵਾਇਰਿੰਗ ਪ੍ਰਮਾਣਿਤ |

ਲੋਕਲੀ ਨੋਟਬੁੱਕ ਚਲਾਉਣ ਲਈ, ਇੱਕ ਵਰਚੁਅਲ ਐਨਵਾਇਰਨਮੈਂਟ ਬਣਾਓ ਅਤੇ ਮੇਲ ਖਾਂਦਾ ਲੋੜੀਂਦਾ ਫਾਈਲ ਇੰਸਟਾਲ ਕਰੋ। ਉਦਾਹਰਣ ਵਜੋਂ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## ਨਮੂਨਾ ਡੇਟਾ

ਨੋਟਬੁੱਕ ਇੱਕ ਛੋਟਾ ਲੋਕਲ ਕੋਰਪਸ [sample_data](../../sample_data) ਵਿੱਚ ਵਰਤਦਾ ਹੈ ਤਾਂ ਜੋ ਉਦਾਹਰਣ ਨਿੱਜੀ ਦਸਤਾਵੇਜ਼ਾਂ ਜਾਂ ਕਲਾਉਡ ਸੰਦਰਭਾਂ ਦੇ ਬਿਨਾਂ ਚੱਲ ਸਕਣ। ਵੇਖੋ [sample_data/README.md](./sample_data/README.md) ਵਿਸਥਾਰ ਲਈ।

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## ਲੋਕਲ ਪ੍ਰਮਾਣਿਕਤਾ ਸੰਖੇਪ

ਪ੍ਰਮਾਣਿਕਤਾ ਦੇ ਨਤੀਜੇ ਹਰ ਲੇਖ ਵਿੱਚ ਅਤੇ [SERIES_PLAN.md](./SERIES_PLAN.md) ਵਿੱਚ ਦਰਜ ਹਨ।

| ਖੇਤਰ | ਨਤੀਜਾ |
| --- | --- |
| ਸੀਰੀਜ਼ 2 ਖੁੱਲ੍ਹਾ-ਸ੍ਰੋਤ ਰਸਤਾ | FastEmbed ਨੇ 384-ਡਾਈਮੇੰਸ਼ਨ ਲੋਕਲ ਕੈਂਪਿੰਗ ਬਣਾਈ, Qdrant ਨੇ ਮੈਮੋਰੀ ਕਲੇਕਸ਼ਨ ਵਿੱਚ 8 ਵੈਕਟਰ ਸ਼ਾਮਲ ਕੀਤੇ, ਹਲਕੀ-ਫੁਲਕੀ ਰੀਰੈਂਕਿੰਗ ਨੇ ਉਮੀਦਵਾਰ ਸੈਕਸ਼ਨ ਲੱਭਿਆ; ਵਿਕਲਪਤ Ollama ਬਣਾਉਣ `phi4-mini:3.8b` ਨਾਲ ਸਿੱਟਾ ਮੁਕੰਮਲ ਹੋਇਆ |

ਲੋਕਲ ਨੋਟਬੁੱਕ ਜਾਣ-ਪਛਾਣ ਵਾਲੇ ਗੁਪਤ ਸੂਤਰਾਂ ਤੋਂ ਬਚਦਾ ਹੈ।

## ਲੋਕਲ Ollama ਬਣਾਉਣ

ਸੀਰੀਜ਼ 2 ਨੋਟਬੁੱਕ ਡੀਫਾਲਟ ਵਜੋਂ ਲੋਕਲ-ਸੁਰੱਖਿਅਤ ਹੈ। ਲੋਕਲ Ollama ਬਣਾਉਣ ਲਈ, [.env.example](../../.env.example) ਨੂੰ `.env` ਵਜੋਂ ਕਾਪੀ ਕਰੋ ਅਤੇ ਸੀਰੀਜ਼ 2 ਦੇ ਮੁੱਲ ਭਰੋ।

ਸੀਰੀਜ਼ 2 Ollama ਬਣਾਉਣ ਲਈ, ਅਣਕਮੈਂਟ ਕਰੋ:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

ਸੀਰੀਜ਼ 2 ਨੋਟਬੁੱਕ ਰਿਪੋਜ਼ਿਟਰੀ ਬੇਸ ਤੋਂ `.env` ਸਵੈਚਾਲਿਤ ਤੌਰ 'ਤੇ ਲੋਡ ਕਰਦਾ ਹੈ `python-dotenv` ਦੀ ਵਰਤੋਂ ਕਰਕੇ।

> [!IMPORTANT]
> `.env` ਫਾਈਲਾਂ, API ਚਾਬੀਆਂ, ਨਿੱਜੀ ਐਂਡਪੌਇੰਟ ਜਾਂ ਕਿਰਾਏਦਾਰ-ਵਿਸ਼ੇਸ਼ ਮੁੱਲਾਂ ਨੂੰ ਕਮਿਟ ਨਾ ਕਰੋ। ਰਿਪੋਜ਼ਿਟਰੀ ਜਾਨਬੂਝ ਕੇ ਗੁਪਤ ਸੂਤਰਾਂ ਨੂੰ ਮਾਰਕਡਾਊਨ ਫਾਈਲਾਂ ਅਤੇ ਨੋਟਬੁੱਕਾਂ ਵਿੱਚੋਂ ਬਾਹਰ ਰੱਖਦੀ ਹੈ।

ਲੋੜੀਂਦੇ ਫਾਈਲਾਂ [requirements/README.md](./requirements/README.md) ਵਿੱਚ ਦਸਤਾਵੇਜ਼ਬੱਧ ਹਨ।

ਲਿੰਕਾਂ, ਨੋਟਬੁੱਕ ਢਾਂਚਾ, ਨੋਟਬੁੱਕ ਆਉਟਪੁੱਟ ਦੀ ਸਾਫ਼-ਸੁਥਰਤਾ ਅਤੇ ਉੱਚ-ਖਤਰੇ ਗੁਪਤ ਪੈਟਰਨਾਂ ਦੀ ਪੁਸ਼ਟੀ ਲਈ:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

ਪੁਸ਼ਟੀਕਰਨ ਸਕ੍ਰਿਪਟ [scripts/README.md](./scripts/README.md) ਵਿੱਚ ਦਸਤਾਵੇਜ਼ਬੱਧ ਹਨ।

ਸਾਰੇ ਲੋਕਲ-ਸੁਰੱਖਿਅਤ ਨੋਟਬੁੱਕਾਂ ਨੂੰ ਇੱਕੋ ਐਨਵਾਇਰਨਮੈਂਟ ਵਿੱਚ ਚਲਾਉਣ ਲਈ:

```powershell
python scripts\verify_notebooks.py --execute
```

ਇਹੋ ਵਰਗਾ ਪੁਸ਼ਟੀਕਰਨ ਪ੍ਰਕਿਰਿਆ GitHub Actions ਵਿੱਚ ਪੁਸ਼, ਪੁਲ ਰਿਕਵੈਸਟ ਅਤੇ ਹੱਥੋਂ-ਵਰਕਫਲੋ ਡਿਸਪੈਚ ਤੇ ਚੱਲਦੀ ਹੈ। ਡ੍ਰਾਫਟ ਲੇਖਾਂ ਅਤੇ ਨੋਟਬੁੱਕਾਂ ਨੂੰ ਜਾਨਬੂਝ ਕੇ ਪਬਲਿਕ ਪੁਸ਼ਟੀ ਰਸਤੇ ਤੋਂ ਬਾਹਰ ਰੱਖਿਆ ਗਿਆ ਹੈ।

ਅਪਡੇਟ ਪ੍ਰਕਾਸ਼ਿਤ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ, [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) ਵਰਤੋਂ।

ਮੌਜੂਦਾ ਗੈਰ-ਪ੍ਰਕਾਸ਼ਿਤ ਸਵਾਲ ਸੰਖੇਪ ਲਈ ਵੇਖੋ [CHANGELOG.md](./CHANGELOG.md)।

ਯੋਗਦਾਨ ਅਤੇ ਨੋਟਬੁੱਕ ਸਫ਼ਾਈ ਲਈ ਨਿਰਦੇਸ਼ਾਂ ਲਈ, [CONTRIBUTING.md](./CONTRIBUTING.md) ਵੇਖੋ।

## ਬਹੁ-ਭਾਸ਼ਾ ਸਹਾਇਤਾ

### ਕੋ-ਆਪ ਟ੍ਰਾਂਸਲੇਟਰ ਰਾਹੀਂ ਸਮਰਥਿਤ (ਆਟੋਮੇਟਿਕ ਅਤੇ ਹਮੇਸ਼ਾ ਅੱਪ-ਟੂ-ਡੇਟ)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](./README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ਕੀ ਤੁਸੀਂ ਲੋਕਲ ਕਲੋਨ ਕਰਨਾ ਪਸੰਦ ਕਰਦੇ ਹੋ?**
>
> ਇਸ ਰਿਪੋਜ਼ਿਟਰੀ ਵਿੱਚ 50+ ਭਾਸ਼ਾ ਅਨੁਵਾਦ ਸ਼ਾਮਲ ਹਨ ਜੋ ਡਾਊਨਲੋਡ ਦਾ ਆਕਾਰ ਕਾਫੀ ਵਧਾਉਂਦੇ ਹਨ। ਬਿਨਾਂ ਅਨੁਵਾਦਾਂ ਦੇ ਕਲੋਨ ਕਰਨ ਲਈ sparse checkout ਵਰਤੋਂ:
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
> ਇਸ ਨਾਲ ਤੁਹਾਨੂੰ ਕੋਰਸ ਪੂਰਾ ਕਰਨ ਲਈ ਸਾਰਾ ਕੁਝ ਮਿਲਦਾ ਹੈ ਅਤੇ ਡਾਊਨਲੋਡ ਤੇਜ਼ ਹੁੰਦਾ ਹੈ।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਪਣ**:
ਇਸ ਦਸਤਾਵੇਜ਼ ਦਾ ਅਨੁਵਾਦ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾਵਾਂ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮੱਤਿਆਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੇ ਉਪਯੋਗ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆਵਾਂ ਲਈ ਜਵਾਬਦੇਹ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->