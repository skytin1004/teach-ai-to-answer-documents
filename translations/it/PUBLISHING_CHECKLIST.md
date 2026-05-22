# Lista di controllo per la pubblicazione

Usa questa lista di controllo prima di eseguire il commit o il push di aggiornamenti pubblici.

## Sicurezza

- Conferma che non siano presenti chiavi API, token, password o endpoint privati scritti in file Markdown, notebook, dati di esempio o script.
- Conserva le credenziali nelle variabili d'ambiente o nell'identità gestita, non nei file sottoposti a commit.
- Non eseguire commit di file `.env` o file di output dei notebook eseguiti.
- Mantieni `.env.example` solo con segnaposto.

## Verifica

Esegui lo script di verifica del repository:

```powershell
python scripts\verify_notebooks.py
```

Esegui l'esecuzione completa sicura in locale del notebook prima di pubblicare modifiche all'implementazione:

```powershell
python scripts\verify_notebooks.py --execute
```

Controlli previsti:

- i link Markdown locali sono validi
- la validazione JSON del notebook passa
- i notebook non contengono output salvati o conteggi di esecuzione
- la scansione per pattern segreti ad alto rischio passa
- i notebook pubblici si eseguono localmente
- il materiale in bozza sotto `drafts/` viene saltato intenzionalmente

## Revisione

- Conferma che i link agli articoli nel README puntino ai file previsti.
- Conferma che ogni articolo abbia la navigazione del repository e link ai notebook correlati.
- Conferma che le bozze non siano linkate dagli indici pubblici a meno che non siano pronte per la pubblicazione.
- Conferma che i template per issue e pull request di GitHub corrispondano ancora al flusso di lavoro del repository.
- Conferma che i risultati della verifica nell'articolo corrispondano all'ultimo output del notebook.
- Conferma che il workflow di GitHub Actions si avvii come previsto dopo il push.
- Conferma che `CHANGELOG.md` rifletta l'aggiornamento che si sta pubblicando.
- Conferma che `CONTRIBUTING.md` corrisponda ancora al flusso di lavoro del repository.

## Git

- Revisiona `git status --short --branch`.
- Revisiona `git diff --stat`.
- Esegui commit e push solo quando esplicitamente pronto.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->