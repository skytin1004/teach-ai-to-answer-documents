# Notatbøker

Disse notatbøkene støtter artikkelserien med kjørbare eksempler.

| Notatbok | Artikkel | Formål |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serie 2](../articles/series-2-open-source-rag-end-to-end.md) | Åpen kildekode RAG med FastEmbed, Qdrant lokal modus, henting, omrangering, valgfri Ollama-generering og kildehenvisninger |

## Kjør lokalt

Installer kravene for notatboken du vil kjøre:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Eller installer alle avhengigheter:

```powershell
python -m pip install -r requirements\all.txt
```

## Verifiser

Fra depotets rotmappe:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serie 2 kan lese Ollama-konfigurasjon fra en `.env`-fil i depotets rotmappe. Start fra [../.env.example](../../../.env.example), som er gruppert etter serie.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->