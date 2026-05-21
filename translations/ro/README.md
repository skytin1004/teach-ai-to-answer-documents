# Învățarea AI să Răspundă la Întrebări Bazate pe Documentele Tale

Acest depozit colectează o serie de bloguri din 2026 despre construirea sistemelor AI fundamentate pe documente cu RAG, serviciile Azure AI, alternative open-source și fluxurile de lucru orientate spre evaluare.

## Context

În 2023, am lucrat la o pereche de tutoriale despre cum să înveți ChatGPT să răspundă la întrebări din documente PDF folosind Azure AI Search și Azure OpenAI. Ideea de „ChatGPT pe datele tale” părea încă nouă atunci, iar scopul era să arăt un flux de lucru practic: stocarea documentelor, indexarea lor, recuperarea conținutului relevant și generarea de răspunsuri din contextul recuperat.

În 2026, ecosistemul RAG este mult mai mare. Azure AI Search suportă modele moderne de recuperare vectorială și hibridă, Azure OpenAI face parte din ecosistemul mai larg Microsoft Foundry Models, iar uneltele open-source precum LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama și vLLM au devenit alegeri practice pentru sisteme reale.

De aceea am dorit să revin asupra acestui subiect. Întrebarea nu mai este doar „Cum construiesc RAG?” Acum există multe moduri de a-l construi, iar întrebarea mai importantă este „Ce arhitectură ar trebui să aleg pentru situația mea?”

Această serie începe de la acel strat decizional. Înainte de a intra în implementare, analizează de ce serviciile AI au nevoie de recuperare, când serviciile gestionate Azure au sens, când alternativele open-source sunt o potrivire mai bună și unde se potrivește ajustarea fină.

## Articole

1. [Seria 1: RAG, Azure vs Alternative Open-Source și Când Are Sens Ajustarea Fină](./series-1-rag-azure-open-source-fine-tuning.md)

## Suport Multilingv

### Suportat prin Co-op Translator (Automat și Întotdeauna Actualizat)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](./README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Preferi să Clonezi Local?**
>
> Acest depozit include traduceri în peste 50 de limbi, ceea ce crește semnificativ dimensiunea descărcării. Pentru a clona fără traduceri, folosește sparse checkout:
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
> Acest lucru îți oferă tot ce ai nevoie pentru a finaliza cursul cu o descărcare mult mai rapidă.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->