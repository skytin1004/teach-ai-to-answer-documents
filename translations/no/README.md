# Lær AI å svare på spørsmål basert på dokumentene dine

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

Dette depotet samler en bloggserie fra 2026 om å bygge dokumentbaserte AI-systemer med RAG, Azure AI-tjenester, åpne kildealternativer og evalueringsorienterte arbeidsflyter.

## Bakgrunn

I 2023 arbeidet jeg med et par veiledninger om å lære ChatGPT å svare på spørsmål fra PDF-dokumenter ved bruk av Azure AI Search og Azure OpenAI. Ideen om "ChatGPT på dine data" føltes fortsatt ny da, og målet var å vise en praktisk arbeidsflyt: lagre dokumenter, indeksere dem, hente relevant innhold, og generere svar fra denne hentede konteksten.

I 2026 er RAG-økosystemet mye større. Azure AI Search støtter moderne vektor- og hybridgjenfinningsmønstre, Azure OpenAI er en del av det bredere Microsoft Foundry Models-økosystemet, og åpne kildeverktøy som LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama og vLLM har blitt praktiske valg for ekte systemer.

Derfor ønsket jeg å ta opp dette temaet på nytt. Spørsmålet er ikke lenger bare "Hvordan bygger jeg RAG?" Det finnes nå mange måter å bygge det på, og det viktigere spørsmålet er "Hvilken arkitektur bør jeg velge for min situasjon?"

Denne serien starter fra det beslutningslaget, og gjør det deretter om til praktiske veiledninger. Den første implementeringsveien bygger et lokalt åpen kilde RAG-system som alle kan kjøre med eksempeldata, Qdrant, Ollama og Phi-4-mini.

## Artikler

Se [articles/README.md](./articles/README.md) for artikkelindeks.

1. [Serie 1: RAG, Azure vs Åpne Kilde-alternativer, og Når Finjustering Gir Mening](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serie 2: Bygg et Lokalt Åpen Kilde RAG-System fra Start til Slutt](./articles/series-2-open-source-rag-end-to-end.md)

Kommende:

- Bygg samme RAG-system med Azure AI Search og Azure OpenAI.
- Legg til evaluering og regresjonskontroller utover et demo-svar.

## Notatbøker

Implementasjonsartiklene bruker notatbøker slik at henting og evalueringssteg kan inspiseres direkte. Se [notebooks/README.md](./notebooks/README.md) for veiledning på mappenivå.

> [!TIP]
> Start med Serie 2 hvis du ønsker den raskeste veien. Den kjører lokalt med eksempeldata, CPU-vennlige innebygginger, Qdrant i lokal modus, og uten sky-legitimasjon.

| Serie | Notatbok | Krav | Lokal verifisering |
| --- | --- | --- | --- |
| Serie 2 | [Åpen kilde RAG-notatbok](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant lokal modus, henting, om-rangering og kildewiring verifisert |

For å kjøre en notatbok lokalt, opprett et virtuelt miljø og installer den matchende kravfilen. For eksempel:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Eksempeldata

Notatbøkene bruker en liten lokal korpus i [sample_data](../../sample_data) slik at eksemplene kan kjøres uten private dokumenter eller sky-legitimasjon. Se [sample_data/README.md](./sample_data/README.md) for detaljer.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Lokal Verifiseringsoppsummering

Verifiseringsresultater registreres i hver artikkel og i [SERIES_PLAN.md](./SERIES_PLAN.md).

| Område | Resultat |
| --- | --- |
| Serie 2 åpen kilde vei | FastEmbed genererte 384-dimensjonale lokale innebygginger, Qdrant inn-memory samling satte inn 8 vektorer, lettvekts om-rangering hentet forventet seksjon; valgfri Ollama-generering fullført med `phi4-mini:3.8b` |

Den lokale notatboken unngår bevisst hardkodede hemmeligheter.

## Lokal Ollama-generering

Serie 2-notatboken er som standard lokal-sikker. For å aktivere lokal Ollama-generering, kopier [.env.example](../../.env.example) til `.env` og fyll inn verdiene for Serie 2.

For Ollama-generering i Serie 2, fjern kommentaren på:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Serie 2-notatboken laster automatisk `.env` fra depotets rot ved bruk av `python-dotenv`.

> [!IMPORTANT]
> Ikke legg inn `.env`-filer, API-nøkler, private endepunkter eller leietaker-spesifikke verdier i kildekoden. Depotet holder bevisst hemmeligheter utenfor Markdown-filer og notatbøker.

Kravfilene dokumenteres i [requirements/README.md](./requirements/README.md).

For å validere lenker, notatbøkkstrukturen, notatbok-utdataenes renhet, og høyrisiko hemmelighetsmønstre:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Verifiseringsskriptene dokumenteres i [scripts/README.md](./scripts/README.md).

For å kjøre alle lokal-sikre notatbøker i samme miljø:

```powershell
python scripts\verify_notebooks.py --execute
```

Den samme verifiseringsflyten kjører i GitHub Actions ved pushes, pull requests og manuelle workflow-dispatcher. Utkast-artikler og notatbøker er bevisst ekskludert fra den offentlige verifikasjonsveien.

Før oppdateringer publiseres, bruk [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Se [CHANGELOG.md](./CHANGELOG.md) for den nåværende upubliserte endringsoversikten.

For retningslinjer for bidrag og notatbokhygiene, se [CONTRIBUTING.md](./CONTRIBUTING.md).

## Flerspråklig støtte

### Støttes via Co-op Translator (Automatisk og Alltid Oppdatert)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabisk](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarsk](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Kinesisk (Forenklet)](../zh-CN/README.md) | [Kinesisk (Tradisjonell, Hong Kong)](../zh-HK/README.md) | [Kinesisk (Tradisjonell, Macau)](../zh-MO/README.md) | [Kinesisk (Tradisjonell, Taiwan)](../zh-TW/README.md) | [Kroatisk](../hr/README.md) | [Tsjekkisk](../cs/README.md) | [Dansk](../da/README.md) | [Nederlandsk](../nl/README.md) | [Estisk](../et/README.md) | [Finsk](../fi/README.md) | [Fransk](../fr/README.md) | [Tysk](../de/README.md) | [Gresk](../el/README.md) | [Hebraisk](../he/README.md) | [Hindi](../hi/README.md) | [Ungarsk](../hu/README.md) | [Indonesisk](../id/README.md) | [Italiensk](../it/README.md) | [Japansk](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreansk](../ko/README.md) | [Litauisk](../lt/README.md) | [Malayisk](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigeriansk pidgin](../pcm/README.md) | [Norsk](./README.md) | [Persisk (Farsi)](../fa/README.md) | [Polsk](../pl/README.md) | [Portugisisk (Brasil)](../pt-BR/README.md) | [Portugisisk (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumensk](../ro/README.md) | [Russisk](../ru/README.md) | [Serbisk (Kyrillisk)](../sr/README.md) | [Slovakisk](../sk/README.md) | [Slovensk](../sl/README.md) | [Spansk](../es/README.md) | [Swahili](../sw/README.md) | [Svensk](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Tyrkisk](../tr/README.md) | [Ukrainsk](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamesisk](../vi/README.md)

> **Foretrekker du å klone lokalt?**
>
> Dette depotet inkluderer over 50 språkoversettelser som betydelig øker nedlastingsstørrelsen. For å klone uten oversettelser, bruk sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Dette gir deg alt du trenger for å fullføre kurset med en mye raskere nedlastning.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->