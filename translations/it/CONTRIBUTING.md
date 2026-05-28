# Contributing

Questo repository è organizzato come una serie di blog più esempi di notebook eseguibili.

## Before Opening a Pull Request

Esegui lo script di validazione locale:

```powershell
python scripts\verify_notebooks.py
```

Per modifiche di implementazione o del notebook, esegui l'esecuzione del notebook sicura locale:

```powershell
python scripts\verify_notebooks.py --execute
```

## Notebook Guidelines

- Mantieni i notebook leggibili e focalizzati sull'articolo correlato.
- Non effettuare il commit di output salvati o conteggi di esecuzione del notebook.
- Usa piccoli dati di esempio da `sample_data/` a meno che l'articolo non richieda una risorsa esterna specifica.
- Registra i risultati di verifica nell'articolo correlato quando il comportamento cambia.

## Secrets and Credentials

- Non effettuare il commit di chiavi API, token, password, endpoint privati o file `.env`.
- Usa `.env.example` solo per valori segnaposto.
- Usa variabili d'ambiente per esperimenti locali opzionali con Ollama.

## Documentation

- Mantieni aggiornati i link di navigazione degli articoli.
- Aggiorna `README.md` quando aggiungi un nuovo articolo, notebook, file requirements o file dati di esempio.
- Aggiorna `CHANGELOG.md` prima di pubblicare un aggiornamento visibile del repository.

## Verification

Il workflow di GitHub Actions esegue:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Il materiale di bozza sotto `drafts/` viene ignorato dalla verifica del repository finché non è pronto per l'indicizzazione pubblica.

## Issues

Usa il template di feedback per articoli per correzioni degli articoli e il template di problema notebook per problemi di esecuzione del notebook.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->