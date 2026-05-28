# Publiseringssjekkliste

Bruk denne sjekklisten før du committer eller pusher offentlige oppdateringer.

## Sikkerhet

- Bekreft at ingen API-nøkler, tokens, passord eller private endepunkter er skrevet inn i Markdown-filer, notatbøker, eksempeldatasett eller skript.
- Oppbevar legitimasjon i miljøvariabler eller administrert identitet, ikke i committede filer.
- Ikke committ `.env`-filer eller utførte notatbokutdatafiler.
- Hold `.env.example` kun som plassholder.

## Verifisering

Kjør verifiseringsskriptet for depotet:

```powershell
python scripts\verify_notebooks.py
```

Kjør full lokal sikker notatbokkjøring før publisering av implementasjonsendringer:

```powershell
python scripts\verify_notebooks.py --execute
```

Forventede kontroller:

- lokale Markdown-lenker fungerer
- notatbok-JSON-validering godkjennes
- notatbøker inneholder ikke lagrede utdata eller kjøringsantall
- skanning for høy-risiko hemmelige mønstre er godkjent
- offentlige notatbøker kjører lokalt
- utkastsmateriale under `drafts/` er med vilje utelatt

## Gjennomgang

- Bekreft at README-artikkellinker peker til de tiltenkte filene.
- Bekreft at hver artikkel har navigasjon i depotet og relaterte notatbøker.
- Bekreft at utkast ikke er lenket fra offentlige indekser med mindre de er klare for publisering.
- Bekreft at GitHub-issues og pull request-maler fortsatt samsvarer med depotets arbeidsflyt.
- Bekreft at verifiseringsresultater i artikkelen stemmer med siste notatbokutdata.
- Bekreft at GitHub Actions-arbeidsflyt forventes å kjøre etter push.
- Bekreft at `CHANGELOG.md` gjenspeiler oppdateringen som publiseres.
- Bekreft at `CONTRIBUTING.md` fortsatt samsvarer med depotets arbeidsflyt.

## Git

- Gå gjennom `git status --short --branch`.
- Gå gjennom `git diff --stat`.
- Commit og push kun når det eksplisitt er klart.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->