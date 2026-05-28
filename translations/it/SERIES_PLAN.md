# Insegnare all'AI a Rispondere alle Domande Basandosi sui Tuoi Documenti - Piano della Serie

Questo piano traccia il rilascio pubblico della Serie 1 e Serie 2. Successivamente il lavoro su Azure e la valutazione verranno mantenuti come bozze finché gli esempi non saranno completamente end-to-end e verificati.

Non effettuare commit o push delle modifiche fino a quando non viene esplicitamente istruito.

## Ambito Pubblico

Rilascio pubblico attuale:

- Articolo della Serie 1: decisioni sull'architettura RAG, compromessi tra Azure e open-source, e dove si inserisce il fine-tuning.
- Articolo della Serie 2: tutorial RAG open-source locale.
- Notebook della Serie 2: laboratorio RAG locale eseguibile con FastEmbed, Qdrant, Ollama e Phi-4-mini.
- Dati di esempio: file Markdown con politica scolastica e guida all'uso dell'IA nei corsi.

Bozze create ma non ancora nell'indice pubblico:

- Ricostruzione di Azure AI Search e Azure OpenAI.
- Valutazione RAG e controlli di regressione.

## Scenario del Tutorial

Lo scenario condiviso è un assistente per la politica scolastica.

L'assistente risponde a questa domanda da documenti locali:

```text
Can I use generative AI for my final assignment?
```

Il comportamento previsto è:

1. Caricare documenti Markdown locali.
2. Analizzarli e suddividerli in sezioni per intestazioni.
3. Creare embedding locali e memorizzare rappresentazioni ricercabili con metadati.
4. Recuperare la sezione di politica rilevante.
5. Riorganizzare i risultati se necessario.
6. Generare o comporre una risposta fondata.
7. Restituire le citazioni.
8. Registrare i risultati della verifica.

## Struttura Pubblica Attuale

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```

Il materiale in bozza è archiviato sotto `drafts/` ed è saltato dalla verifica del repository finché non è pronto per l'indicizzazione pubblica.

## Verifica della Serie 2

Verificato su Windows con Python 3.12.6.

- Installati con successo i requisiti in `requirements/open-source-rag.txt`.
- Eseguito `notebooks/series-2-open-source-rag.ipynb` con `nbclient`.
- Verifica locale superata: caricati 2 documenti di esempio, create 8 sezioni, FastEmbed ha generato embedding locali a 384 dimensioni, inizializzata la collezione in memoria di Qdrant, inseriti 8 vettori.
- Domanda di prova: "Posso usare l'IA generativa per il mio compito finale?"
- Fonte principale recuperata dopo un leggero riordino: `school_ai_policy.md`.
- Sezione principale recuperata dopo un leggero riordino: `Compiti Finali`.
- Percorso di risposta predefinito: compositore di risposte locale e trasparente.
- Ollama installato tramite winget; `phi4-mini:3.8b` scaricato con successo.
- Percorso di generazione risposta con Ollama: completato con `phi4-mini:3.8b`.
- Dimensione file modello Ollama: circa 2,49GB su disco.
- Dimensione modello caricata da Ollama: 3,3GB riportati da `ollama ps`.
- Scarico su GPU: 100% GPU riportato da `ollama ps` su RTX 3060 Laptop GPU.
- Memoria GPU osservata dopo la generazione: circa 3,5GB su 6GB.
- Esecuzione notebook con modello FastEmbed in cache e generazione Ollama abilitata superata in circa 34 secondi tramite lo script di verifica.
- Osservazione: un passaggio iniziale di caricamento documenti ha incluso accidentalmente `sample_data/README.md`; il notebook ora carica esplicitamente solo i due documenti di esempio previsti.

## Verifica del Repository

- `scripts/verify_notebooks.py` valida collegamenti Markdown locali, JSON del notebook, pulizia dell'output del notebook e pattern di segreti ad alto rischio.
- `scripts/verify_notebooks.py --execute` esegue i notebook pubblici dalla radice del repository.
- Il materiale in bozza sotto `drafts/` è intenzionalmente saltato.

## Lavori Futuri

- Ricostruire lo stesso scenario con Azure AI Search e Azure OpenAI come parte futura della serie.
- Aggiungere la valutazione del recupero e della risposta una volta che le implementazioni locali e Azure sono entrambe stabili.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->