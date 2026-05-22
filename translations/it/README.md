# Insegnare all'IA a Rispondere alle Domande Basandosi sui Tuoi Documenti

![Panoramica del sistema AI RAG basato su documenti](../../assets/images/readme-hero.svg)

Questo repository raccoglie una serie di blog del 2026 riguardo la costruzione di sistemi AI basati su documenti con RAG, servizi Azure AI, alternative open-source e flussi di lavoro orientati alla valutazione.

## Contesto

Nel 2023, ho lavorato su una coppia di tutorial su come insegnare a ChatGPT a rispondere a domande da documenti PDF utilizzando Azure AI Search e Azure OpenAI. L'idea di "ChatGPT sui tuoi dati" all'epoca sembrava ancora nuova, e l'obiettivo era mostrare un flusso di lavoro pratico: memorizzare documenti, indicizzarli, recuperare contenuti rilevanti e generare risposte da quel contesto recuperato.

Nel 2026, l'ecosistema RAG è molto più ampio. Azure AI Search supporta pattern moderni di recupero vettoriale e ibrido, Azure OpenAI fa parte del più ampio ecosistema Microsoft Foundry Models, e strumenti open-source come LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama e vLLM sono diventate scelte pratiche per sistemi reali.

Ecco perché ho voluto rivedere questo argomento. La domanda non è più solo "Come costruisco RAG?" Ora ci sono molti modi per costruirlo, e la domanda più importante è "Quale architettura dovrei scegliere per la mia situazione?"

Questa serie parte da quel livello decisionale, poi lo trasforma in tutorial pratici. Il primo percorso di implementazione costruisce un sistema RAG open-source locale che chiunque può eseguire con dati di esempio, Qdrant, Ollama e Phi-4-mini.

## Articoli

Vedi [articles/README.md](./articles/README.md) per l'indice degli articoli.

1. [Serie 1: RAG, Azure vs alternative Open-Source e Quando ha senso il Fine-Tuning](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serie 2: Costruisci un sistema RAG open-source locale end-to-end](./articles/series-2-open-source-rag-end-to-end.md)

In arrivo:

- Ricostruire lo stesso sistema RAG con Azure AI Search e Azure OpenAI.
- Aggiungere valutazioni e controlli regressivi oltre a una risposta demo.

## Notebook

Gli articoli di implementazione utilizzano notebook in modo che i passi di recupero e valutazione possano essere ispezionati direttamente. Vedi [notebooks/README.md](./notebooks/README.md) per una guida a livello di cartella.

> [!TIP]
> Parti dalla Serie 2 se vuoi il percorso più veloce. Funziona localmente con dati di esempio, embedding CPU-friendly, modalità locale di Qdrant e senza credenziali cloud.

| Serie | Notebook | Requisiti | Verifica locale |
| --- | --- | --- | --- |
| Serie 2 | [Notebook RAG open-source](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Modalità locale Qdrant, recupero, riordinamento ed instradamento fonte verificati |

Per eseguire un notebook localmente, crea un ambiente virtuale e installa il file requisiti corrispondente. Per esempio:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Dati di esempio

I notebook usano un piccolo corpus locale in [sample_data](../../sample_data) così gli esempi possono essere eseguiti senza documenti privati o credenziali cloud. Vedi [sample_data/README.md](./sample_data/README.md) per dettagli.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Sintesi Verifica Locale

I risultati della verifica sono registrati in ogni articolo e in [SERIES_PLAN.md](./SERIES_PLAN.md).

| Area | Risultato |
| --- | --- |
| Percorso open-source Serie 2 | FastEmbed ha generato embedding locali a 384 dimensioni, la collezione in-memory di Qdrant ha inserito 8 vettori, il leggero riordinamento ha recuperato la sezione attesa; la generazione opzionale di Ollama è stata completata con `phi4-mini:3.8b` |

Il notebook locale evita intenzionalmente segreti codificati.

## Generazione Locale con Ollama

Il notebook della Serie 2 è di default sicuro per l'uso locale. Per abilitare la generazione locale con Ollama, copia [.env.example](../../.env.example) in `.env` e inserisci i valori della Serie 2.

Per la generazione Ollama della Serie 2, decommenta:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Il notebook della Serie 2 carica automaticamente `.env` dalla radice del repository utilizzando `python-dotenv`.

> [!IMPORTANT]
> Non commettere file `.env`, chiavi API, endpoint privati o valori specifici del tenant. Il repository tiene intenzionalmente i segreti fuori dai file Markdown e notebook.

I file requisiti sono documentati in [requirements/README.md](./requirements/README.md).

Per convalidare i link, la struttura del notebook, la pulizia dell'output e le pattern di segreti ad alto rischio:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Gli script di verifica sono documentati in [scripts/README.md](./scripts/README.md).

Per eseguire tutti i notebook locali sicuri nello stesso ambiente:

```powershell
python scripts\verify_notebooks.py --execute
```

Lo stesso flusso di verifica viene eseguito in GitHub Actions su push, pull request e avvii manuali dei workflow. Articoli e notebook in bozza sono intenzionalmente esclusi dal percorso pubblico di verifica.

Prima di pubblicare aggiornamenti, usa [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Vedi [CHANGELOG.md](./CHANGELOG.md) per il sommario delle modifiche non ancora pubblicate.

Per linee guida su contributi e igiene dei notebook, vedi [CONTRIBUTING.md](./CONTRIBUTING.md).

## Supporto Multilingue

### Supportato tramite Co-op Translator (Automatizzato e Sempre Aggiornato)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabo](../ar/README.md) | [Bengalese](../bn/README.md) | [Bulgaro](../bg/README.md) | [Birmano (Myanmar)](../my/README.md) | [Cinese (Semplificato)](../zh-CN/README.md) | [Cinese (Tradizionale, Hong Kong)](../zh-HK/README.md) | [Cinese (Tradizionale, Macau)](../zh-MO/README.md) | [Cinese (Tradizionale, Taiwan)](../zh-TW/README.md) | [Croato](../hr/README.md) | [Ceco](../cs/README.md) | [Danese](../da/README.md) | [Olandese](../nl/README.md) | [Estone](../et/README.md) | [Finlandese](../fi/README.md) | [Francese](../fr/README.md) | [Tedesco](../de/README.md) | [Greco](../el/README.md) | [Ebraico](../he/README.md) | [Hindi](../hi/README.md) | [Ungherese](../hu/README.md) | [Indonesiano](../id/README.md) | [Italiano](./README.md) | [Giapponese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malese](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalese](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Norvegese](../no/README.md) | [Persiano (Farsi)](../fa/README.md) | [Polacco](../pl/README.md) | [Portoghese (Brasile)](../pt-BR/README.md) | [Portoghese (Portogallo)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumeno](../ro/README.md) | [Russo](../ru/README.md) | [Serbo (Cirillico)](../sr/README.md) | [Slovacco](../sk/README.md) | [Sloveno](../sl/README.md) | [Spagnolo](../es/README.md) | [Swahili](../sw/README.md) | [Svedese](../sv/README.md) | [Tagalog (Filippino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thailandese](../th/README.md) | [Turco](../tr/README.md) | [Ucraino](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **Preferisci Clonare Localmente?**
>
> Questo repository include oltre 50 traduzioni linguistiche, il che aumenta significativamente la dimensione del download. Per clonare senza traduzioni, usa il checkout sparso:
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
> Questo ti fornisce tutto ciò che ti serve per completare il corso con un download molto più veloce.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->