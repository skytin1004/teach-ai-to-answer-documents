# Bidra

Dette depotet er organisert som en bloggserie pluss kjørbare notatbokeksempler.

## Før du åpner en Pull Request

Kjør det lokale valideringsskriptet:

```powershell
python scripts\verify_notebooks.py
```

For implementerings- eller notatbokendringer, kjør den lokale sikre notatbokkjøringen:

```powershell
python scripts\verify_notebooks.py --execute
```

## Retningslinjer for notatbøker

- Hold notatbøkene lesbare og fokusert på den tilknyttede artikkelen.
- Ikke legg inn lagrede notatbokutdata eller kjøringsantall i commit.
- Bruk små prøve-data fra `sample_data/` med mindre artikkelen krever en spesifikk ekstern ressurs.
- Registrer verifiseringsresultater i den tilknyttede artikkelen når oppførselen endres.

## Hemmeligheter og legitimasjon

- Ikke legg inn API-nøkler, tokens, passord, private endepunkter eller `.env` filer.
- Bruk kun `.env.example` for plassholderverdier.
- Bruk miljøvariabler for valgfrie lokale Ollama-eksperimenter.

## Dokumentasjon

- Hold navigasjonslenkene for artikler oppdatert.
- Oppdater `README.md` ved tillegg av en ny artikkel, notatbok, kravfil eller prøve-datafil.
- Oppdater `CHANGELOG.md` før publisering av synlig depotoppdatering.

## Verifisering

GitHub Actions-arbeidsflyten kjører:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Utkastsmateriale under `drafts/` ignoreres av depotverifisering til det er klart for offentlig indeksering.

## Problemer

Bruk artikkelformularet for tilbakemelding ved artikkelrettelser og notatbokproblem-skjemaet for problemer med notatbokkjøring.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->