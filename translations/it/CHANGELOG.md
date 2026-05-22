# Changelog

## Non rilasciato

Ambito del rilascio pubblico iniziale per **Insegnare all'IA a Rispondere alle Domande Basate sui Tuoi Documenti**.

### Aggiunto

- Articolo della Serie 1 sulle decisioni architetturali RAG, compromessi Azure vs open-source e dove si colloca il fine-tuning.
- Articolo e notebook della Serie 2 per un workflow RAG open-source locale usando la modalità locale Qdrant, i embeddings locali FastEmbed, il reranking leggero, Ollama e Phi-4-mini.
- Formato tutorial passo dopo passo end-to-end della Serie 2 con snippet Python e note di verifica dal notebook eseguito.
- Percorso opzionale di generazione delle risposte della Serie 2 con Ollama e Phi-4-mini mantenendo come predefinito il recupero locale CPU-friendly.
- Verifica locale Ollama per la Serie 2 usando `phi4-mini:3.8b` su RTX 3060 Laptop GPU.
- Dati di esempio per la politica scolastica e la guida AI ai corsi.
- File dei requisiti per il notebook pubblico e la verifica a livello di repository.
- Script di verifica del repository per i link Markdown locali e la validazione/esecuzione del notebook.
- Workflow GitHub Actions per la verifica del notebook.
- `.env.example` per configurazione opzionale di generazione Ollama locale senza impegnare la configurazione locale.
- File README a livello di cartella per articoli, notebook, requisiti, dati di esempio e script.
- Lista di controllo per la pubblicazione per sicurezza pubblica e verifica.
- Area di lavoro bozza per futuri contenuti Azure e di valutazione.

### Verificato

- Validazione dei link Markdown locali superata.
- Il notebook Serie 2 si convalida con successo.
- Il notebook Serie 2 si esegue con successo nell'ambiente di verifica locale.
- I file del notebook sono mantenuti senza output salvati o conteggi di esecuzione.
- Nessun segreto reale è stato impegnato.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->