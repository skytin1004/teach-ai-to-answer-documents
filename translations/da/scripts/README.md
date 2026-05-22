# Scripts

Denne mappe indeholder repositories verifikationsscripts.

## `verify_notebooks.py`

Validerer lokale Markdown-links, notebook JSON, notebook output-renhed og højrisiko hemmelighedsmønstre:

```powershell
python scripts\verify_notebooks.py
```

Eksekverer alle offentlige lokale-sikre notebooks:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions workflow bruger samme script.

Udkastsmateriale under `drafts/` springes over, indtil det er klar til den offentlige indeks.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->