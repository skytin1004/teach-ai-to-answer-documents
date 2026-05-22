# Lær AI at besvare spørgsmål baseret på dine dokumenter - Serieplan

Denne plan sporer den offentlige udgivelse af Serie 1 og Serie 2. Senere arbejde med Azure og evaluering holdes som kladder, indtil eksemplerne er fuldt gennemgående og verificeret.

Foretag ikke commit eller push af ændringer, medmindre det udtrykkeligt er instrueret.

## Offentlig rækkevidde

Nuværende offentlige udgivelse:

- Serie 1 artikel: RAG-arkitektur beslutninger, Azure vs open-source afvejninger, og hvor finjustering passer ind.
- Serie 2 artikel: lokal open-source RAG vejledning.
- Serie 2 notesbog: kørbar lokal RAG-lab med FastEmbed, Qdrant, Ollama og Phi-4-mini.
- Eksempeldatasæt: skolepolitik og kursus AI-vejlednings Markdown-filer.

Udarbejdet, men endnu ikke i det offentlige indeks:

- Azure AI Search og Azure OpenAI genopbygning.
- RAG evaluering og regressionskontroller.

## Vejledningsscenario

Det delte scenario er en skolepolitikassistent.

Assistenten besvarer dette spørgsmål ud fra lokale dokumenter:

```text
Can I use generative AI for my final assignment?
```
  
Den forventede adfærd er:

1. Indlæs lokale Markdown-dokumenter.  
2. Analyser og del dem op efter overskrifter.  
3. Opret lokale embeddings og opbevar søgbare repræsentationer med metadata.  
4. Hent den relevante politiksektion.  
5. Omlister efter behov.  
6. Generer eller sammensæt et funderet svar.  
7. Returner kildehenvisninger.  
8. Registrer verificeringsresultater.

## Nuværende offentlige struktur

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
  
Udkastsmateriale gemmes under `drafts/` og ignoreres af repository-verifikation, indtil det er klar til offentlig indeksering.

## Serie 2 Verifikation

Verificeret på Windows med Python 3.12.6.

- `requirements/open-source-rag.txt` blev installeret succesfuldt.  
- `notebooks/series-2-open-source-rag.ipynb` blev kørt med `nbclient`.  
- Lokal verifikation bestået: 2 eksempeldokumenter indlæst, 8 chunks oprettet, FastEmbed genererede 384-dimensionelle lokale embeddings, Qdrant in-memory samling initialiseret, og 8 vektorer indsat.  
- Testspørgsmål: "Kan jeg bruge generativ AI til min afsluttende opgave?"  
- Top hentet kilde efter let omlistning: `school_ai_policy.md`.  
- Top hentet sektion efter let omlistning: `Final Assignments`.  
- Standard svarsti: lokal transparent svar-komponist.  
- Ollama installeret via winget; `phi4-mini:3.8b` hentet succesfuldt.  
- Ollama svar-genereringssti: gennemført med `phi4-mini:3.8b`.  
- Ollama modelstørrelse: ca. 2.49GB på disk.  
- Ollama indlæst modelstørrelse: 3.3GB rapporteret af `ollama ps`.  
- GPU-aflastning: 100% GPU rapporteret af `ollama ps` på RTX 3060 Laptop GPU.  
- Observeret GPU-hukommelse efter generering: ca. 3.5GB af 6GB.  
- Notesbogsudførelse med cachet FastEmbed-model og Ollama-generering aktiveret bestået på ca. 34 sekunder via verifikationsscript.  
- Observation: et tidligt dokumentindlæsningspass inkluderede utilsigtet `sample_data/README.md`; notesbogen indlæser nu kun eksplicit de to tiltænkte eksempeldokumenter.

## Repository verifikation

- `scripts/verify_notebooks.py` validerer lokale Markdown-links, notesbog JSON, renhed af notesbog output og højrisiko hemmelige mønstre.  
- `scripts/verify_notebooks.py --execute` kører offentlige notesbøger fra repository-roden.  
- Udkastsmateriale under `drafts/` er bevidst udeladt.

## Næste arbejde

- Genopbygge samme scenario med Azure AI Search og Azure OpenAI som en fremtidig del af serien.  
- Tilføje opslag og svar-evaluering når både lokal og Azure-implementering er stabile.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->