# Lär AI att Svara på Frågor Baserade på Dina Dokument

![Dokumentbaserat AI RAG-systemöversikt](../../assets/images/readme-hero.svg)

Detta repository samlar en bloggserie från 2026 om att bygga dokumentbaserade AI-system med RAG, Azure AI-tjänster, open-source-alternativ och evalueringsorienterade arbetsflöden.

## Bakgrund

År 2023 arbetade jag med ett par handledningar om att lära ChatGPT att svara på frågor från PDF-dokument med hjälp av Azure AI Search och Azure OpenAI. Idén med "ChatGPT på dina data" kändes fortfarande ny då, och målet var att visa ett praktiskt arbetsflöde: lagra dokument, indexera dem, hämta relevant innehåll och generera svar utifrån den hämtade kontexten.

År 2026 är RAG-ekosystemet mycket större. Azure AI Search stödjer moderna vektor- och hybridhämtningmönster, Azure OpenAI är en del av det bredare Microsoft Foundry Models-ekosystemet, och open-source-verktyg som LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama och vLLM har blivit praktiska val för riktiga system.

Det är därför jag ville återbesöka detta ämne. Frågan är inte längre bara "Hur bygger jag RAG?" Det finns nu många sätt att bygga det, och den viktigare frågan är "Vilken arkitektur ska jag välja för min situation?"

Denna serie börjar från det beslutsfattande lagret och gör det sedan till praktiska handledningar. Den första implementationsvägen bygger ett lokalt open-source RAG-system som vem som helst kan köra med exempeldata, Qdrant, Ollama och Phi-4-mini.

## Artiklar

Se [articles/README.md](./articles/README.md) för artikelindex.

1. [Serie 1: RAG, Azure vs Open-Source-alternativ och när finjustering är meningsfullt](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serie 2: Bygg ett lokalt open-source RAG-system från början till slut](./articles/series-2-open-source-rag-end-to-end.md)

Kommande:

- Bygg om samma RAG-system med Azure AI Search och Azure OpenAI.
- Lägg till utvärdering och regressionstester utöver ett demosvar.

## Notebooks

Implementationsartiklarna använder notebooks så att hämtning och utvärderingssteg kan inspekteras direkt. Se [notebooks/README.md](./notebooks/README.md) för mappnivåvägledning.

> [!TIP]
> Börja med Serie 2 om du vill ha snabbast väg. Den körs lokalt med exempeldata, CPU-vänliga embeddings, Qdrant i lokal läge och inga molnbehörigheter.

| Serie | Notebook | Krav | Lokal verifiering |
| --- | --- | --- | --- |
| Serie 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant i lokal läge, hämtning, omrankning och koppling av källa verifierade |

För att köra en notebook lokalt, skapa en virtuell miljö och installera motsvarande kravfil. Till exempel:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Exempeldata

Notebooks använder en liten lokal samling i [sample_data](../../sample_data) så exemplen kan köras utan privata dokument eller molnbehörigheter. Se [sample_data/README.md](./sample_data/README.md) för detaljer.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Sammanfattning av Lokal Verifiering

Verifieringsresultat dokumenteras i varje artikel och i [SERIES_PLAN.md](./SERIES_PLAN.md).

| Område | Resultat |
| --- | --- |
| Serie 2 open-source-väg | FastEmbed genererade 384-dimensionella lokala embeddings, Qdrant in-memory-kollektion infogade 8 vektorer, lättviktig omrankning hämtade förväntad sektion; valfri Ollama-generering slutfördes med `phi4-mini:3.8b` |

Den lokala notebooken undviker medvetet hårdkodade hemligheter.

## Lokal Ollama-generering

Serie 2 notebook är default säker för lokalt bruk. För att aktivera lokal Ollama-generering, kopiera [.env.example](../../.env.example) till `.env` och fyll i Serie 2-värdena.

För Ollama-generering i Serie 2, avkommentera:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Serie 2 notebook laddar automatiskt `.env` från repositoryrötterna genom att använda `python-dotenv`.

> [!IMPORTANT]
> Lämna inte in `.env`-filer, API-nycklar, privata endpoints eller hyresgästs-specifika värden. Repositoryt håller medvetet hemligheter ute från Markdown-filer och notebooks.

Kravfiler dokumenteras i [requirements/README.md](./requirements/README.md).

För att validera länkar, notebookstruktur, notebookens resultatrensning och högriskhemlighetsmönster:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Verifieringsskript dokumenteras i [scripts/README.md](./scripts/README.md).

För att köra alla lokalt säkra notebooks i samma miljö:

```powershell
python scripts\verify_notebooks.py --execute
```

Samma verifieringsflöde körs i GitHub Actions vid pushar, pull-requests och manuella arbetsflödesutlösningar. Utkast till artiklar och notebooks är medvetet exkluderade från den publika verifieringsvägen.

Innan du publicerar uppdateringar, använd [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Se [CHANGELOG.md](./CHANGELOG.md) för aktuell opublicerad ändringssammanfattning.

För bidrags- och notebookvårdsriktlinjer, se [CONTRIBUTING.md](./CONTRIBUTING.md).

## Flerspråkigt Stöd

### Stöds via Co-op Translator (Automatiserat och Alltid Uppdaterat)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabiska](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgariska](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Kinesiska (Förenklad)](../zh-CN/README.md) | [Kinesiska (Traditionell, Hongkong)](../zh-HK/README.md) | [Kinesiska (Traditionell, Macao)](../zh-MO/README.md) | [Kinesiska (Traditionell, Taiwan)](../zh-TW/README.md) | [Kroatiska](../hr/README.md) | [Tjeckiska](../cs/README.md) | [Danska](../da/README.md) | [Nederländska](../nl/README.md) | [Estniska](../et/README.md) | [Finska](../fi/README.md) | [Franska](../fr/README.md) | [Tyska](../de/README.md) | [Grekiska](../el/README.md) | [Hebreiska](../he/README.md) | [Hindi](../hi/README.md) | [Ungerska](../hu/README.md) | [Indonesiska](../id/README.md) | [Italienska](../it/README.md) | [Japanska](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreanska](../ko/README.md) | [Litauiska](../lt/README.md) | [Malayiska](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalesiska](../ne/README.md) | [Nigeriansk Pidgin](../pcm/README.md) | [Norska](../no/README.md) | [Persiska (Farsi)](../fa/README.md) | [Polska](../pl/README.md) | [Portugisiska (Brasilien)](../pt-BR/README.md) | [Portugisiska (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumänska](../ro/README.md) | [Ryska](../ru/README.md) | [Serbiska (Kyrilliska)](../sr/README.md) | [Slovakiska](../sk/README.md) | [Slovenska](../sl/README.md) | [Spanska](../es/README.md) | [Swahili](../sw/README.md) | [Svenska](./README.md) | [Tagalog (Filippinska)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thailändska](../th/README.md) | [Turkiska](../tr/README.md) | [Ukrainska](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamesiska](../vi/README.md)

> **Föredrar du att klona lokalt?**
>
> Detta repository inkluderar 50+ språköversättningar vilket kraftigt ökar nedladdningsstorleken. För att klona utan översättningar, använd sparsamt uttag:
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
> Detta ger dig allt du behöver för att slutföra kursen med en mycket snabbare nedladdning.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->