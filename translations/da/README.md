# Lær AI at Besvare Spørgsmål Baseret på Dine Dokumenter

![Dokument-understøttet AI RAG system oversigt](../../assets/images/readme-hero.svg)

Dette arkiv samler en blogserie fra 2026 om at bygge dokument-understøttede AI-systemer med RAG, Azure AI-tjenester, open-source alternativer og evalueringsorienterede arbejdsprocesser.

## Baggrund

I 2023 arbejdede jeg på et par vejledninger om at lære ChatGPT at besvare spørgsmål fra PDF-dokumenter ved hjælp af Azure AI Search og Azure OpenAI. Ideen om "ChatGPT på dine data" føltes stadig ny dengang, og målet var at vise en praktisk arbejdsproces: opbevar dokumenter, indekser dem, hente relevant indhold og generere svar ud fra den hentede kontekst.

I 2026 er RAG-økosystemet meget større. Azure AI Search understøtter moderne vektor- og hybride hentemønstre, Azure OpenAI er en del af det bredere Microsoft Foundry Models-økosystem, og open-source værktøjer såsom LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama og vLLM er blevet praktiske valg til reelle systemer.

Derfor ønskede jeg at genbesøge dette emne. Spørgsmålet er ikke længere kun "Hvordan bygger jeg RAG?" Der findes nu mange måder at bygge det på, og det vigtigste spørgsmål er "Hvilken arkitektur skal jeg vælge til min situation?"

Denne serie starter fra det beslutningstagende lag, og forvandler det derefter til praktiske vejledninger. Den første implementationsvej bygger et lokalt open-source RAG-system, som alle kan køre med eksempeldatasæt, Qdrant, Ollama og Phi-4-mini.

## Artikler

Se [articles/README.md](./articles/README.md) for artikelindekset.

1. [Serie 1: RAG, Azure vs Open-Source Alternativer, og Hvornår Finjustering Giver Mening](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serie 2: Byg et Lokalt Open-Source RAG-System Fra Start til Slut](./articles/series-2-open-source-rag-end-to-end.md)

Kommer næste:

- Genbyg det samme RAG-system med Azure AI Search og Azure OpenAI.
- Tilføj evaluering og regressionskontroller ud over et demonstrationssvar.

## Notebooks

Implementeringsartiklerne bruger notebooks, så henter- og evalueringsfaserne kan inspiceres direkte. Se [notebooks/README.md](./notebooks/README.md) for vejledning på mappeniveau.

> [!TIP]
> Start med Serie 2, hvis du ønsker den hurtigste vej. Den kører lokalt med eksempeldatasæt, CPU-venlige embeddings, Qdrant lokaltilstand og ingen cloud-legitimationsoplysninger.

| Serie | Notebook | Krav | Lokal verifikation |
| --- | --- | --- | --- |
| Serie 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant lokaltilstand, hentning, omrangering, og kildeforbindelse verificeret |

For at køre en notebook lokalt, opret et virtuelt miljø og installer den matchende kravfil. For eksempel:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Eksempeldatasæt

Notebooks bruger en lille lokal korpus i [sample_data](../../sample_data) så eksemplerne kan køre uden private dokumenter eller cloud-legitimationsoplysninger. Se [sample_data/README.md](./sample_data/README.md) for detaljer.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Lokal Verifikationsoversigt

Verifikationsresultaterne er registreret i hver artikel og i [SERIES_PLAN.md](./SERIES_PLAN.md).

| Område | Resultat |
| --- | --- |
| Serie 2 open-source vej | FastEmbed genererede 384-dimensionelle lokale embeddings, Qdrant i hukommelses-samling indsatte 8 vektorer, letvægts omrangering hentede den forventede sektion; valgfri Ollama generation blev fuldført med `phi4-mini:3.8b` |

Den lokale notebook undgår bevidst hardcodede hemmeligheder.

## Lokal Ollama Generering

Serie 2 notebook er som standard lokal-sikker. For at aktivere lokal Ollama generering, kopier [.env.example](../../.env.example) til `.env` og udfyld værdierne for Serie 2.

For Serie 2 Ollama generering, fjern kommenteringen af:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Serie 2 notebook indlæser automatisk `.env` fra arkivroden ved brug af `python-dotenv`.

> [!IMPORTANT]
> Indsæt ikke `.env` filer, API-nøgler, private endpoints eller lejer-specifikke værdier i versionsstyring. Arkivet holder bevidst hemmeligheder ude af Markdown-filer og notebooks.

Kravfiler dokumenteres i [requirements/README.md](./requirements/README.md).

For at validere links, notebook struktur, notebook output-renhed og højrisko hemmeligheds-mønstre:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Verifikationsscripts er dokumenteret i [scripts/README.md](./scripts/README.md).

For at køre alle lokal-sikre notebooks i samme miljø:

```powershell
python scripts\verify_notebooks.py --execute
```

Den samme verifikationsproces kører i GitHub Actions ved pushes, pull requests og manuelle workflow-udløsninger. Udkast til artikler og notebooks er bevidst ekskluderet fra den offentlige verifikationsvej.

Før offentliggørelse af opdateringer, brug [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Se [CHANGELOG.md](./CHANGELOG.md) for den aktuelle upublicerede ændringsoversigt.

For retningslinjer om bidrag og notebook-vedligeholdelse, se [CONTRIBUTING.md](./CONTRIBUTING.md).

## Multisprogsunderstøttelse

### Understøttet via Co-op Translator (Automatiseret og Altid Opdateret)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabisk](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarsk](../bg/README.md) | [Burmesisk (Myanmar)](../my/README.md) | [Kinesisk (Forenklet)](../zh-CN/README.md) | [Kinesisk (Traditionel, Hong Kong)](../zh-HK/README.md) | [Kinesisk (Traditionel, Macau)](../zh-MO/README.md) | [Kinesisk (Traditionel, Taiwan)](../zh-TW/README.md) | [Kroatisk](../hr/README.md) | [Tjekkisk](../cs/README.md) | [Dansk](./README.md) | [Hollandsk](../nl/README.md) | [Estisk](../et/README.md) | [Finsk](../fi/README.md) | [Fransk](../fr/README.md) | [Tysk](../de/README.md) | [Græsk](../el/README.md) | [Hebraisk](../he/README.md) | [Hindi](../hi/README.md) | [Ungarsk](../hu/README.md) | [Indonesisk](../id/README.md) | [Italiensk](../it/README.md) | [Japansk](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreansk](../ko/README.md) | [Litauisk](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalesisk](../ne/README.md) | [Nigeriansk Pidgin](../pcm/README.md) | [Norsk](../no/README.md) | [Persisk (Farsi)](../fa/README.md) | [Polsk](../pl/README.md) | [Portugisisk (Brasilien)](../pt-BR/README.md) | [Portugisisk (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumænsk](../ro/README.md) | [Russisk](../ru/README.md) | [Serbisk (Cyrillisk)](../sr/README.md) | [Slovakisk](../sk/README.md) | [Slovensk](../sl/README.md) | [Spansk](../es/README.md) | [Swahili](../sw/README.md) | [Svensk](../sv/README.md) | [Tagalog (Filippinsk)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thailandsk](../th/README.md) | [Tyrkisk](../tr/README.md) | [Ukrainsk](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamesisk](../vi/README.md)

> **Foretrækker du at klone lokalt?**
>
> Dette arkiv inkluderer over 50 sprogoversættelser, hvilket øger downloadstørrelsen betydeligt. For at klone uden oversættelser, brug sparse checkout:
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
> Dette giver dig alt, hvad du behøver for at fuldføre kurset med en meget hurtigere download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->