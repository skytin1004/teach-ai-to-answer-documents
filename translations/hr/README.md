# Naučite AI odgovarati na pitanja na temelju vaših dokumenata

Ovaj repozitorij prikuplja seriju blogova iz 2026. godine o izgradnji AI sustava utemeljenih na dokumentima pomoću RAG-a, Azure AI servisa, open-source alternativa i workflowa usmjerenih na evaluaciju.

## Pozadina

Godine 2023. radio sam na paru tutorijala o podučavanju ChatGPT-a da odgovara na pitanja iz PDF dokumenata koristeći Azure AI Search i Azure OpenAI. Ideja "ChatGPT-a na vašim podacima" tada je još bila nova, a cilj je bio pokazati praktičan workflow: spremiti dokumente, indeksirati ih, dohvatiti relevantan sadržaj i generirati odgovore iz tog dohvaćenog konteksta.

Godine 2026. RAG ekosustav je mnogo veći. Azure AI Search podržava moderne načine dohvaćanja vektora i hibridnih modela, Azure OpenAI dio je šireg Microsoft Foundry Models ekosustava, a open-source alati poput LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama i vLLM postali su praktični izbori za stvarne sustave.

Zato sam želio ponovno obraditi ovu temu. Pitanje više nije samo "Kako gradim RAG?" Sada postoji mnogo načina za izgradnju, a važnije pitanje je "Koju arhitekturu trebam odabrati za svoju situaciju?"

Ova serija počinje od te razine donošenja odluka. Prije nego se duboko upustimo u implementaciju, istražuje zašto AI servisi trebaju dohvat, kada ima smisla koristiti Azure upravljane servise, kada su open-source alternative prikladnije i gdje se uklapa fino podešavanje.

## Članci

1. [Serija 1: RAG, Azure naspram Open-Source Alternativa i Kada Je Fino Podešavanje Razumno](./series-1-rag-azure-open-source-fine-tuning.md)

## Podrška za više jezika

### Podržano putem Co-op Translatora (automatizirano i uvijek ažurirano)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](./README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Preferirate li klonirati lokalno?**
>
> Ovaj repozitorij uključuje prijevode na više od 50 jezika što znatno povećava veličinu preuzimanja. Za kloniranje bez prijevoda, koristite sparse checkout:
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
> Ovo vam daje sve što vam treba za završetak tečaja s puno bržim preuzimanjem.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->