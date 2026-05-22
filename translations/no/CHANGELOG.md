# Endringslogg

## Uutgitt

Første offentlige utgivelsesomfang for **Lær AI å svare på spørsmål basert på dokumentene dine**.

### Lagt til

- Serie 1-artikkel om RAG-arkitekturvalg, Azure vs åpen kildekode-kompromisser, og hvor fintuning passer inn.
- Serie 2-artikkel og notatbok for en lokal åpen kildekode RAG-arbeidsflyt med Qdrant lokal modus, FastEmbed lokale embeddinger, lettvekts omrangering, Ollama og Phi-4-mini.
- Serie 2 steg-for-steg ende-til-ende opplæringsformat med Python-snutter og verifiseringsnotater fra den kjørte notatboken.
- Valgfri Serie 2 svar-genereringsbane med Ollama og Phi-4-mini samtidig som lokal CPU-vennlig henting beholdes som standardbane.
- Lokal Ollama-verifisering for Serie 2 ved hjelp av `phi4-mini:3.8b` på RTX 3060 Laptop GPU.
- Eksempeldata for skolepolitikk og kurs AI-veiledning.
- Kravfiler for den offentlige notatboken og depotnivåverifisering.
- Repositorium verifiseringsskript for lokale Markdown-lenker og notatbokvalidering/utførelse.
- GitHub Actions arbeidsflyt for notatbokverifisering.
- `.env.example` for valgfri lokal Ollama-genereringsoppsett uten å comitte lokal konfigurasjon.
- Mappespesifikke README-filer for artikler, notatbøker, krav, eksempeldata og skript.
- Publiseringssjekkliste for offentlig sikkerhet og verifisering.
- Utkast til arbeidsområde for fremtidig Azure- og evalueringsinnhold.

### Verifisert

- Lokal validering av Markdown-lenker er bestått.
- Serie 2 notatbok valideres vellykket.
- Serie 2 notatbok kjøres vellykket i det lokale verifiseringsmiljøet.
- Notatbokfiler beholdes uten lagrede utdata eller kjøreantall.
- Ingen ekte hemmeligheter er comittet.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->