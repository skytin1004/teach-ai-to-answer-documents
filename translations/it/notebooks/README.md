# Notebooks

Questi notebook supportano la serie di articoli con esempi eseguibili.

| Notebook | Articolo | Scopo |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serie 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG open-source con FastEmbed, modalità locale Qdrant, recupero, riorganizzazione, generazione opzionale Ollama e riferimenti alle fonti |

## Esegui in locale

Installa i requisiti per il notebook che vuoi eseguire:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Oppure installa tutte le dipendenze:

```powershell
python -m pip install -r requirements\all.txt
```

## Verifica

Dalla radice del repository:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

La serie 2 può leggere la configurazione Ollama da un file `.env` nella radice del repository. Parti da [../.env.example](../../../.env.example), che è organizzato per serie.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->