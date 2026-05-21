# Lær AI at Besvare Spørgsmål Baseret på Dine Dokumenter

Dette arkiv samler en blogserie fra 2026 om at bygge dokument-baserede AI-systemer med RAG, Azure AI-tjenester, open source-alternativer og evalueringsorienterede arbejdsgange.

## Baggrund

I 2023 arbejdede jeg på et par vejledninger om at lære ChatGPT at besvare spørgsmål fra PDF-dokumenter ved hjælp af Azure AI Search og Azure OpenAI. Ideen om "ChatGPT på dine data" føltes stadig ny dengang, og målet var at vise en praktisk arbejdsgang: gem dokumenter, indekser dem, hent relevant indhold, og generer svar fra den hentede kontekst.

I 2026 er RAG-økosystemet meget større. Azure AI Search understøtter moderne vektor- og hybride hentemønstre, Azure OpenAI er en del af det bredere Microsoft Foundry Models-økosystem, og open source-værktøjer som LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama og vLLM er blevet praktiske valg til reelle systemer.

Derfor ville jeg genbesøge dette emne. Spørgsmålet er ikke længere kun "Hvordan bygger jeg RAG?" Der er nu mange måder at bygge det på, og det vigtigere spørgsmål er "Hvilken arkitektur skal jeg vælge til min situation?"

Denne serie starter fra det beslutningslag. Før den går dybere ind i implementering, ser den på, hvorfor AI-tjenester har brug for hentning, hvornår Azure-baserede styrede tjenester giver mening, hvornår open source-alternativer er et bedre match, og hvor finjustering passer ind.

## Artikler

1. [Serie 1: RAG, Azure vs Open-Source Alternativer, og Hvornår Finjustering Giver Mening](./series-1-rag-azure-open-source-fine-tuning.md)

## Flersproget Support

### Understøttet via Co-op Translator (Automatiseret og Altid Opdateret)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](./README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Foretrækker du at klone lokalt?**
>
> Dette arkiv inkluderer 50+ sprogoversættelser, hvilket øger downloadstørrelsen betydeligt. For at klone uden oversættelser, brug sparse checkout:
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
> Dette giver dig alt, hvad du behøver for at gennemføre kurset med en meget hurtigere download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->