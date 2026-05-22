# Publiceringscheckliste

Brug denne checkliste før du committer eller pusher offentlige opdateringer.

## Sikkerhed

- Bekræft at der ikke er skrevet API-nøgler, tokens, adgangskoder eller private endpoints i Markdown-filer, notebooks, eksempeldata eller scripts.
- Opbevar legitimationsoplysninger i miljøvariable eller managed identity, ikke i committede filer.
- Commit ikke `.env`-filer eller outputfiler fra kørte notebooks.
- Hold `.env.example` som udelukkende pladsholder.

## Verifikation

Kør repository-verifikationsscriptet:

```powershell
python scripts\verify_notebooks.py
```

Kør den fulde lokale sikre notebook-eksekvering før publicering af implementeringsændringer:

```powershell
python scripts\verify_notebooks.py --execute
```

Forventede checks:

- lokale Markdown-links godkendes
- notebook JSON-validering godkendes
- notebooks indeholder ikke gemte output eller eksekveringstællinger
- scanning for højrisiko hemmelige mønstre godkendes
- offentlige notebooks kører lokalt
- kladder under `drafts/` springes bevidst over

## Gennemgang

- Bekræft at README-artikellinks peger på de tilsigtede filer.
- Bekræft at hver artikel har repository-navigation og relaterede notebook-links.
- Bekræft at kladder ikke er linket fra offentlige indekser medmindre de er klar til publicering.
- Bekræft at GitHub issue- og pull request-skabeloner stadig matcher repository-workflowen.
- Bekræft at verifikationsresultater i artiklen matcher det seneste notebook-output.
- Bekræft at GitHub Actions workflow forventes at køre efter push.
- Bekræft at `CHANGELOG.md` afspejler den opdatering, der skal publiceres.
- Bekræft at `CONTRIBUTING.md` stadig matcher repository-workflowen.

## Git

- Gennemgå `git status --short --branch`.
- Gennemgå `git diff --stat`.
- Commit og push kun når du udtrykkeligt er klar.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->