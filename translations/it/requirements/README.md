# Requisiti

Ogni articolo di implementazione ha un file di requisiti specifico.

| File | Utilizzato da |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Notebook RAG open-source Serie 2, inclusi strumenti opzionali per la generazione con Ollama |
| [all.txt](../../../requirements/all.txt) | Verifica a livello di repository e CI |

Usa il file specifico quando esegui un singolo notebook. Usa `all.txt` quando convalidi l'intero repository.

`open-source-rag.txt` e `all.txt` includono `fastembed` per gli embeddings locali e `python-dotenv` così la Serie 2 può opzionalmente abilitare la generazione con Ollama dal `.env` senza modificare la pipeline di retrieval.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->