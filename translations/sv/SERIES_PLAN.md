# Lär AI att Svara på Frågor Baserat på Dina Dokument - Serieplan

Denna plan spårar den offentliga Serien 1 och Serien 2 lanseringen. Senare arbete med Azure och utvärdering hålls som utkast tills exemplen är fullt end-to-end och verifierade.

Gör inga commit eller push ändringar förrän det uttryckligen anges.

## Offentlig Omfattning

Nuvarande offentliga lansering:

- Serie 1 artikel: RAG arkitekturval, Azure vs öppen källkod avvägningar, och var finjustering passar in.
- Serie 2 artikel: lokal öppen källkod RAG handledning.
- Serie 2 anteckningsbok: körbar lokal RAG-labb med FastEmbed, Qdrant, Ollama och Phi-4-mini.
- Exempeldatat: skolpolicy och kurs AI väglednings Markdown-filer.

Utkast men inte i det offentliga indexet än:

- Azure AI Search och Azure OpenAI ombyggnad.
- RAG utvärdering och regressionskontroller.

## Handledning Scenario

Det delade scenariot är en skolpolicyassistent.

Assistanten svarar på denna fråga från lokala dokument:

```text
Can I use generative AI for my final assignment?
```

Det förväntade beteendet är:

1. Ladda lokala Markdown-dokument.
2. Pars och dela upp dem efter rubriker.
3. Skapa lokala inbäddningar och lagra sökbara representationer med metadata.
4. Hämta relevant policydel.
5. Omrankera vid behov.
6. Generera eller komponera ett grundat svar.
7. Returnera källhänvisningar.
8. Registrera verifieringsresultat.

## Nuvarande Offentliga Struktur

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

Utkastsmaterial lagras under `drafts/` och hoppas över av repository-verifiering tills det är redo för offentligt index.

## Serie 2 Verifiering

Verifierad på Windows med Python 3.12.6.

- Installerade `requirements/open-source-rag.txt` framgångsrikt.
- Körde `notebooks/series-2-open-source-rag.ipynb` med `nbclient`.
- Lokal verifiering godkänd: 2 exempeldokument laddades, 8 delar skapades, FastEmbed genererade 384-dimensionella lokala inbäddningar, Qdrant minneskollektion initierades och 8 vektorer infogades.
- Testfråga: "Kan jag använda generativ AI för mitt slutuppdrag?"
- Topp hämtad källa efter lättvikts omrangering: `school_ai_policy.md`.
- Topp hämtad sektion efter lättvikts omrangering: `Final Assignments`.
- Standard svarsväg: lokal transparent svarskompositör.
- Ollama installerad genom winget; `phi4-mini:3.8b` draget framgångsrikt.
- Ollama svarsgenereringsväg: slutförd med `phi4-mini:3.8b`.
- Ollama modelfilstorlek: cirka 2.49GB på disk.
- Ollama laddad modellstorlek: 3.3GB rapporterat av `ollama ps`.
- GPU avlastning: 100% GPU rapporterat av `ollama ps` på RTX 3060 Laptop GPU.
- GPU-minne observerat efter generering: cirka 3.5GB av 6GB.
- Anteckningsbok körning med cachelagrat FastEmbed-modell och Ollama-generation aktiverad klarade sig på cirka 34 sekunder via verifieringsskriptet.
- Observation: ett tidigt dokumentladdningspass inkluderade av misstag `sample_data/README.md`; anteckningsboken laddar nu endast de två avsedda exempeldokumenten uttryckligen.

## Repository Verifiering

- `scripts/verify_notebooks.py` validerar lokala Markdown-länkar, notebook JSON, notebook utgångsrensning och högriskmönster för hemligheter.
- `scripts/verify_notebooks.py --execute` kör offentliga notebooks från repository-roten.
- Utkastsmaterial under `drafts/` hoppas över avsiktligt.

## Nästa Arbete

- Bygga om samma scenario med Azure AI Search och Azure OpenAI som del av framtida serie.
- Lägga till hämtning och svarsvärdering när både lokal och Azure-implementationer är stabila.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->