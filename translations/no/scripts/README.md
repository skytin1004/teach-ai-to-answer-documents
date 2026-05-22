# Scripts

Denne mappen inneholder skript for verifisering av repositoriet.

## `verify_notebooks.py`

Validerer lokale Markdown-lenker, notebook JSON, renhet i notebook-utdata og mønstre for høy-risiko hemmeligheter:

```powershell
python scripts\verify_notebooks.py
```

Kjører alle offentlige lokal-sikre notebooks:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions-arbeidsflyten bruker det samme skriptet.

Utkastsmateriale under `drafts/` blir hoppet over inntil det er klart for den offentlige indeksen.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->