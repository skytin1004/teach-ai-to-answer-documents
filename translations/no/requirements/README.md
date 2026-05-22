# Krav

Hver implementeringsartikkel har en fokusert kravfil.

| Fil | Brukt av |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Serie 2 åpen kildekode RAG-notatbok, inkludert valgfrie Ollama genereringshjelpere |
| [all.txt](../../../requirements/all.txt) | Bekreftelse og CI på repositorienivå |

Bruk den fokuserte filen når du kjører én notatbok. Bruk `all.txt` når du validerer hele repositoriet.

`open-source-rag.txt` og `all.txt` inkluderer `fastembed` for lokale innebygginger og `python-dotenv` slik at Serie 2 valgfritt kan aktivere Ollama-generering fra `.env` uten å endre gjenfinningspipen.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->