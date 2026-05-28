# Lær AI å svare på spørsmål basert på dokumentene dine - Serieplan

Denne planen følger den offentlige utgivelsen av Serie 1 og Serie 2. Senere arbeid med Azure og evaluering holdes som utkast inntil eksemplene er fullt end-to-end og verifisert.

Ikke gjør commit eller push av endringer før det eksplisitt er instruert.

## Offentlig omfang

Nåværende offentlige utgivelse:

- Serie 1 artikkel: RAG arkitekturvalg, Azure vs åpen kildekode kompromisser, og hvor finjustering passer inn.
- Serie 2 artikkel: lokal åpen kildekode RAG veiledning.
- Serie 2 notatbok: kjørbar lokal RAG-lab med FastEmbed, Qdrant, Ollama, og Phi-4-mini.
- Eksempeldatasett: skolepolitikk og kurs AI-veiledning i Markdown-filer.

Utkast, men ikke i det offentlige indekset ennå:

- Azure AI Search og Azure OpenAI gjenoppbygging.
- RAG evaluering og regresjonssjekker.

## Veiledningsscenario

Det delte scenarioet er en skolepolitikkassistent.

Assistenten svarer på dette spørsmålet fra lokale dokumenter:

```text
Can I use generative AI for my final assignment?
```

Forventet oppførsel er:

1. Last inn lokale Markdown-dokumenter.
2. Analyser og del dem opp basert på overskrifter.
3. Lag lokale innebygginger og lagre søkbare representasjoner med metadata.
4. Hent det relevante avsnittet av policyen.
5. Rerank ved behov.
6. Generer eller sett sammen et forankret svar.
7. Returner referanser.
8. Registrer verifiseringsresultater.

## Nåværende offentlige struktur

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```

Utkastsmateriell lagres under `drafts/` og utelates fra repository-verifisering til det er klart for offentlig indeksering.

## Serie 2 Verifisering

Verifisert på Windows med Python 3.12.6.

- Installert `requirements/open-source-rag.txt` uten problemer.
- Kjørte `notebooks/series-2-open-source-rag.ipynb` med `nbclient`.
- Lokal verifisering bestått: 2 eksempel-dokumenter lastet, 8 chunks opprettet, FastEmbed genererte 384-dimensjonale lokale innebygginger, Qdrant in-memory samling initialisert, og 8 vektorer satt inn.
- Testspørsmål: "Kan jeg bruke generativ AI til min avsluttende oppgave?"
- Topp hentet kilde etter lettvekts reranking: `school_ai_policy.md`.
- Topp hentet seksjon etter lettvekts reranking: `Final Assignments`.
- Standard svarvei: lokal transparent svar-komponist.
- Ollama installert via winget; `phi4-mini:3.8b` lastet ned uten problemer.
- Ollama svar-genereringsvei: fullført med `phi4-mini:3.8b`.
- Ollama modellfilstørrelse: ca. 2.49GB på disk.
- Ollama lastet modellstørrelse: 3.3GB rapportert av `ollama ps`.
- GPU avlasting: 100 % GPU brukt rapportert av `ollama ps` på RTX 3060 Laptop GPU.
- GPU-minne observert etter generering: ca. 3.5GB av 6GB.
- Notatbokkjøring med cachet FastEmbed-modell og Ollama-generering aktivert fullførte på ca. 34 sekunder gjennom verifiseringsskriptet.
- Observasjon: et tidlig dokument-lastetrinn inkluderte ved et uhell `sample_data/README.md`; notatboken laster nå bare eksplisitt de to tiltenkte eksempeldokumentene.

## Repository-verifisering

- `scripts/verify_notebooks.py` validerer lokale Markdown-lenker, notatbok-JSON, renhet av notatbok-output, og høyrisiko hemmelige mønstre.
- `scripts/verify_notebooks.py --execute` kjører offentlige notatbøker fra repository-roten.
- Utkastsmateriell under `drafts/` utelates med hensikt.

## Neste arbeid

- Gjenoppbygg samme scenario med Azure AI Search og Azure OpenAI som en fremtidig del av serien.
- Legg til henting og svarevaluering når både lokale og Azure-implementeringer er stabile.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->