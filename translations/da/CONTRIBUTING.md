# Bidrag

Dette repository er organiseret som en blogserie plus kørbare notebook-eksempler.

## Før du åbner en Pull Request

Kør det lokale valideringsscript:

```powershell
python scripts\verify_notebooks.py
```

For implementerings- eller notebook-ændringer, kør den lokale sikre notebook-kørsel:

```powershell
python scripts\verify_notebooks.py --execute
```

## Notebook-retningslinjer

- Hold notebooks læselige og fokuserede på den relaterede artikel.
- Commit ikke gemte notebook-resultater eller eksekveringsantal.
- Brug små prøve-data fra `sample_data/` medmindre artiklen kræver en specifik ekstern ressource.
- Registrer verifikationsresultater i den relaterede artikel, når adfærden ændres.

## Hemmeligheder og legitimationsoplysninger

- Commit ikke API-nøgler, tokens, passwords, private endepunkter eller `.env`-filer.
- Brug kun `.env.example` til pladsholder-værdier.
- Brug miljøvariabler til valgfrie lokale Ollama-eksperimenter.

## Dokumentation

- Hold artikel-navigation links opdaterede.
- Opdater `README.md` når du tilføjer en ny artikel, notebook, krav-fil eller prøve-datafil.
- Opdater `CHANGELOG.md` før offentliggørelse af en synlig repository-opdatering.

## Verifikation

GitHub Actions workflow kører:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Udkastsmateriale under `drafts/` springes over ved repository-verifikation indtil det er klar til offentlig indeksering.

## Issues

Brug artikel-feedback skabelonen til artikelfejl og notebook-issue skabelonen til notebook-udførelsesproblemer.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->