# Publiceringschecklista

Använd denna checklista innan du committar eller pushar offentliga uppdateringar.

## Säkerhet

- Bekräfta att inga API-nycklar, tokens, lösenord eller privata endpoints är skrivna i Markdown-filer, notebooks, exempeldatan eller skript.
- Håll referenser i miljövariabler eller hanterad identitet, inte i committade filer.
- Committa inte `.env`-filer eller körda notebook-utdatafiler.
- Håll `.env.example` endast som platshållare.

## Verifiering

Kör verifikationsskriptet för repositoryt:

```powershell
python scripts\verify_notebooks.py
```

Kör den fullständiga lokala-säkra notebookkörningen innan implementeringsändringar publiceras:

```powershell
python scripts\verify_notebooks.py --execute
```

Förväntade kontroller:

- lokala Markdown-länkar fungerar
- notebook JSON-validering godkänns
- notebooks innehåller inte sparade utdata eller exekveringsräkningar
- sökning efter hög-risk hemlig mönster godkänns
- publika notebooks körs lokalt
- utkastsmaterial under `drafts/` hoppas över med avsikt

## Granskning

- Bekräfta att README-artikellänkar pekar på avsedda filer.
- Bekräfta att varje artikel har repository-navigering och relaterade notebook-länkar.
- Bekräfta att utkast inte länkas från offentliga index såvida de inte är redo att publiceras.
- Bekräfta att GitHub-issues och pull request-mallar fortfarande överensstämmer med repositoryflödet.
- Bekräfta att verifieringsresultaten i artikeln matchar senaste notebook-utdata.
- Bekräfta att GitHub Actions-flöde förväntas köras efter push.
- Bekräfta att `CHANGELOG.md` speglar den uppdatering som publiceras.
- Bekräfta att `CONTRIBUTING.md` fortfarande matchar repositoryflödet.

## Git

- Granska `git status --short --branch`.
- Granska `git diff --stat`.
- Commit och pusha bara när det uttryckligen är redo.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->