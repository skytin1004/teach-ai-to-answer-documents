# ਆਪਣੀਆਂ ਦਸਤਾਵੇਜ਼ਾਂ ਦੇ ਆਧਾਰ 'ਤੇ AI ਨੂੰ ਪ੍ਰਸ਼ਨਾਂ ਦੇ ਜਵਾਬ ਦੇਣਾ ਸਿਖਾਓ

ਇਹ ਰਿਪੋਜ਼ਿਟਰੀ 2026 ਦੀ ਇੱਕ ਬਲੌਗ ਸੀਰੀਜ਼ ਇਕੱਠੀ ਕਰਦੀ ਹੈ ਜੋ RAG, Azure AI ਸਰਵਿਸਿਜ਼, ਖੁੱਲ੍ਹੇ ਸਰੋਤ ਵਿਕਲਪਾਂ, ਅਤੇ ਮੁਲਾਂਕਣ-ਕੇਂਦਰਿਤ ਵਰਕਫਲੋ ਨਾਲ ਦਸਤਾਵੇਜ਼-ਆਧਾਰਿਤ AI ਸਿਸਟਮ ਬਣਾਉਣ ਬਾਰੇ ਹੈ।

## ਪਿਛੋਕੜ

2023 ਵਿੱਚ, ਮੈਂ Azure AI Search ਅਤੇ Azure OpenAI ਦੀ ਵਰਤੋਂ ਕਰਕੇ PDF ਦਸਤਾਵੇਜ਼ਾਂ ਤੋਂ ਪ੍ਰਸ਼ਨਾਂ ਦੇ ਜਵਾਬ ਦੇਣ ਲਈ ChatGPT ਨੂੰ ਸਿਖਾਉਣ ਬਾਰੇ ਦੋ ਟਿਊਟੋਰਿਅਲਜ਼ 'ਤੇ ਕੰਮ ਕੀਤਾ। "ਆਪਣੇ ਡੇਟਾ ਤੇ ChatGPT" ਦਾ ਵਿਚਾਰ ਉਸ ਸਮੇਂ ਨਵਾਂ ਮਹਿਸੂਸ ਹੁੰਦਾ ਸੀ, ਅਤੇ ਮਕਸਦ ਇਹ ਪ੍ਰਦਰਸ਼ਿਤ ਕਰਨਾ ਸੀ ਕਿ ਇੱਕ ਪ੍ਰਯੋਗਕਾਰੀ ਵਰਕਫਲੋ ਕਿਵੇਂ ਬਣਾਈ ਜਾ ਸਕਦੀ ਹੈ: ਦਸਤਾਵੇਜ਼ ਸਟੋਰ ਕਰੋ, ਉਹਨਾਂ ਦਾ ਇੰਡੈਕਸ ਬਣਾਓ, ਸੰਬੰਧਿਤ ਸਮੱਗਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਅਤੇ ਉਸ ਪ੍ਰਾਪਤ ਸੰਦਰਭ ਤੋਂ ਜਵਾਬ ਤਿਆਰ ਕਰੋ।

2026 ਵਿੱਚ, RAG ਪਰਿਸਰ ਬਹੁਤ ਵੱਡਾ ਹੋ ਚੁੱਕਾ ਹੈ। Azure AI Search ਆਧੁਨਿਕ ਵੇਕਟਰ ਅਤੇ ਹਾਈਬਰਿਡ ਰੀਟਰੀਵਲ ਪੈਟਰਨਜ਼ ਨੂੰ ਸਹਿਯੋਗ ਦਿੰਦਾ ਹੈ, Azure OpenAI Microsoft Foundry Models ਪਰਿਸਰ ਦਾ ਹਿੱਸਾ ਹੈ, ਅਤੇ LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, ਅਤੇ vLLM ਵਰਗੇ ਖੁੱਲ੍ਹੇ ਸਰੋਤ ਸੰਦ ਅਸਲੀ ਸਿਸਟਮਾਂ ਲਈ ਵਰਤਣਯੋਗ ਚੋਣ ਬਣ ਚੁੱਕੇ ਹਨ।

ਇਸ ਲਈ ਮੈਂ ਇਸ ਵਿਸ਼ੇ ਨੂੰ ਮੁੜ ਵੇਖਣਾ ਚਾਹੁੰਦਾ ਸੀ। ਹੁਣ ਸਵਾਲ ਸਿਰਫ "ਮੈਂ RAG ਕਿਵੇਂ ਬਣਾਵਾਂ?" ਨਹੀਂ ਹੈ। ਹੁਣ ਇਹ ਬਣਾਉਣ ਦੇ ਕਈ ਤਰੀਕੇ ਹਨ, ਅਤੇ ਅਹੰਕਾਰਕ ਸਵਾਲ ਇਹ ਹੈ "ਮੇਰੇ ਸਥਿਤੀ ਲਈ ਕਿਹੜੀ ਆਰਕੀਟੈਕਚਰ ਚੁਣੀ ਜਾਵੇ?"

ਇਹ ਸੀਰੀਜ਼ ਉਸ ਫੈਸਲਾ ਕਰਨ ਵਾਲੀ ਪਰਤ ਤੋਂ ਸ਼ੁਰੂ ਹੁੰਦੀ ਹੈ। ਲਾਗੂ ਕਰਨ ਵਿੱਚ ਗਹਿਰਾਈ ਵਿੱਚ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ, ਇਹ ਵੇਖਦੀ ਹੈ ਕਿ ਕਿਉਂ AI ਸਰਵਿਸਿਜ਼ ਨੂੰ ਰੀਟਰੀਵਲ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ, ਕਦੋਂ Azure-ਅਧਾਰਤ ਪ੍ਰਬੰਧਿਤ ਸਰਵਿਸਿਜ਼ ਸਹੀ ਹੁੰਦੀਆਂ ਹਨ, ਕਦੋਂ ਖੁੱਲ੍ਹੇ ਸਰੋਤ ਵਿਕਲਪ ਬਿਹਤਰ ਹੁੰਦੇ ਹਨ, ਅਤੇ ਫਾਈਨ-ਟਿਊਨਿੰਗ ਕਿੱਥੇ ਫਿੱਟ ਹੁੰਦੀ ਹੈ।

## ਲੇਖ

1. [ਸੀਰੀਜ਼ 1: RAG, Azure ਅਤੇ ਖੁੱਲ੍ਹੇ ਸਰੋਤ ਵਿਕਲਪ, ਅਤੇ ਫਾਈਨ-ਟਿਊਨਿੰਗ ਕਦੋਂ ਯੋਗ ਹੈ](./series-1-rag-azure-open-source-fine-tuning.md)

## ਬਹੁ-ਭਾਸ਼ਾਈ ਸਹਾਇਤਾ

### ਕੋ-ਆਪ ਟ੍ਰਾਂਸਲੇਟਰ (ਆਟੋਮੇਟਿਡ ਅਤੇ ਹਮੇਸ਼ਾਂ ਅਪਡੇਟ ਰਹਿਣ ਵਾਲਾ) ਰਾਹੀਂ ਸਹਾਇਤਾ ਪ੍ਰਦਾਨ

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](./README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ਕੀ ਤੁਸੀਂ ਸਥਾਨਕ ਤੌਰ ’ਤੇ ਕਲੋਨ ਕਰਨਾ ਪਸੰਦ ਕਰਦੇ ਹੋ?**
>
> ਇਸ ਰਿਪੋਜ਼ਿਟਰੀ ਵਿੱਚ 50+ ਭਾਸ਼ਾਈ ਅਨੁਵਾਦ ਸ਼ਾਮਲ ਹਨ ਜੋ ਡਾਊਨਲੋਡ ਸਾਈਜ਼ ਨੂੰ ਕਾਫੀ ਵਧਾਉਂਦੇ ਹਨ। ਅਨੁਵਾਦਾਂ ਤੋਂ ਬਿਨਾਂ ਕਲੋਨ ਕਰਨ ਲਈ sparse checkout ਦੀ ਵਰਤੋਂ ਕਰੋ:
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
> ਇਸ ਨਾਲ ਤੁਹਾਨੂੰ ਕੋਰਸ ਪੂਰਾ ਕਰਨ ਲਈ ਜਰੂਰੀ ਸਾਰਾ ਕੁੱਝ ਤੇਜ਼ ਡਾਊਨਲੋਡ ਨਾਲ ਮਿਲਦਾ ਹੈ।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਪਣ**:
ਇਸ ਦਸਤਾਵੇਜ਼ ਦਾ ਅਨੁਵਾਦ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾਵਾਂ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮੱਤਿਆਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੇ ਉਪਯੋਗ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆਵਾਂ ਲਈ ਜਵਾਬਦੇਹ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->