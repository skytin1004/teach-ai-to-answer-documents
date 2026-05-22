# Scripts

Questa cartella contiene script di verifica del repository.

## `verify_notebooks.py`

Convalida i link Markdown locali, il JSON dei notebook, la pulizia dell'output dei notebook e i modelli di segreti ad alto rischio:

```powershell
python scripts\verify_notebooks.py
```

Esegue tutti i notebook pubblici e locali sicuri:

```powershell
python scripts\verify_notebooks.py --execute
```

Il workflow di GitHub Actions utilizza lo stesso script.

Il materiale in bozza nella cartella `drafts/` viene saltato fino a quando non è pronto per l'indice pubblico.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->