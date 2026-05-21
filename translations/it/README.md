# Insegna all'IA a Rispondere alle Domande Basate sui Tuoi Documenti

Questo repository raccoglie una serie di blog del 2026 sulla costruzione di sistemi di IA basati su documenti con RAG, servizi Azure AI, alternative open-source e flussi di lavoro orientati alla valutazione.

## Contesto

Nel 2023, ho lavorato a un paio di tutorial su come insegnare a ChatGPT a rispondere a domande da documenti PDF utilizzando Azure AI Search e Azure OpenAI. L'idea di "ChatGPT sui tuoi dati" sembrava ancora nuova allora, e l'obiettivo era mostrare un flusso di lavoro pratico: memorizzare i documenti, indicizzarli, recuperare contenuti rilevanti e generare risposte da quel contesto recuperato.

Nel 2026, l'ecosistema RAG è molto più ampio. Azure AI Search supporta modelli di recupero vettoriale e ibrido moderni, Azure OpenAI è parte del più ampio ecosistema Microsoft Foundry Models, e strumenti open-source come LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama e vLLM sono diventati scelte pratiche per sistemi reali.

Ecco perché ho voluto rivedere questo argomento. La domanda non è più solo "Come costruisco RAG?" Ora ci sono molti modi per costruirlo, e la domanda più importante è "Quale architettura dovrei scegliere per la mia situazione?"

Questa serie parte da quel livello decisionale. Prima di entrare nel dettaglio dell'implementazione, si esamina perché i servizi di IA necessitano di recupero, quando i servizi gestiti basati su Azure hanno senso, quando le alternative open-source sono una scelta migliore, e dove si colloca il fine-tuning.

## Articoli

1. [Serie 1: RAG, Azure vs Alternative Open-Source, e Quando il Fine-Tuning ha Senso](./series-1-rag-azure-open-source-fine-tuning.md)

## Supporto Multilingue

### Supportato tramite Co-op Translator (Automatizzato e Sempre Aggiornato)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](./README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Preferisci Clonare Localmente?**
>
> Questo repository include traduzioni in più di 50 lingue, il che aumenta significativamente la dimensione del download. Per clonare senza traduzioni, usa il sparse checkout:
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
> Questo ti dà tutto il necessario per completare il corso con un download molto più veloce.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->