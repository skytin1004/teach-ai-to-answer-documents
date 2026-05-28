# Leer AI om vragen te beantwoorden op basis van uw documenten

![Document-gebaseerd AI RAG systeem overzicht](../../assets/images/readme-hero.svg)

Deze repository verzamelt een blogserie uit 2026 over het bouwen van document-gebaseerde AI-systemen met RAG, Azure AI-diensten, open-source alternatieven en evaluatiegerichte workflows.

## Achtergrond

In 2023 heb ik gewerkt aan een paar tutorials over het aanleren van ChatGPT om vragen te beantwoorden uit PDF-documenten met behulp van Azure AI Search en Azure OpenAI. Het idee van "ChatGPT op uw data" voelde toen nog nieuw aan, en het doel was om een praktische workflow te tonen: documenten opslaan, indexeren, relevante inhoud ophalen en antwoorden genereren vanuit die opgehaalde context.

In 2026 is het RAG-ecosysteem veel groter. Azure AI Search ondersteunt moderne vector- en hybride ophaalpatronen, Azure OpenAI maakt deel uit van het bredere Microsoft Foundry Models-ecosysteem, en open-source tools zoals LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, en vLLM zijn praktische keuzes geworden voor echte systemen.

Daarom wilde ik dit onderwerp opnieuw bekijken. De vraag is niet langer alleen "Hoe bouw ik RAG?" Er zijn nu veel manieren om het te bouwen, en de belangrijkere vraag is "Welke architectuur moet ik kiezen voor mijn situatie?"

Deze serie begint bij die beslissingslaag en zet die vervolgens om in hands-on tutorials. Het eerste implementatietraject bouwt een lokaal open-source RAG-systeem dat iedereen kan draaien met voorbeeldgegevens, Qdrant, Ollama en Phi-4-mini.

## Artikelen

Zie [articles/README.md](./articles/README.md) voor de artikelindex.

1. [Serie 1: RAG, Azure vs Open-Source Alternatieven, en Wanneer Fijn-afstemming Zinvol Is](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serie 2: Bouw een Lokaal Open-Source RAG-systeem van Begin tot Eind](./articles/series-2-open-source-rag-end-to-end.md)

Komt binnenkort:

- Bouw hetzelfde RAG-systeem opnieuw met Azure AI Search en Azure OpenAI.
- Voeg evaluatie- en regressiecontroles toe naast een demo-antwoord.

## Notebooks

De implementatie-artikelen maken gebruik van notebooks zodat de ophaal- en evaluatiestappen direct kunnen worden bekeken. Zie [notebooks/README.md](./notebooks/README.md) voor mapniveau richtlijnen.

> [!TIP]
> Begin met Serie 2 als je het snelste pad wilt. Het draait lokaal met voorbeelddata, CPU-vriendelijke embeddings, Qdrant lokale modus, en geen cloudreferenties.

| Serie | Notebook | Vereisten | Lokale verificatie |
| --- | --- | --- | --- |
| Serie 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant lokale modus, ophalen, herordenen, en bronkoppeling geverifieerd |

Om een notebook lokaal te draaien, maak een virtuele omgeving aan en installeer het bijpassende requirements-bestand. Bijvoorbeeld:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Voorbeeldgegevens

De notebooks gebruiken een kleine lokale corpus in [sample_data](../../sample_data) zodat de voorbeelden kunnen draaien zonder privé-documenten of cloudreferenties. Zie [sample_data/README.md](./sample_data/README.md) voor details.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Samenvatting Lokale Verificatie

Verificatieresultaten worden vastgelegd in elk artikel en in [SERIES_PLAN.md](./SERIES_PLAN.md).

| Gebied | Resultaat |
| --- | --- |
| Serie 2 open-source pad | FastEmbed genereerde 384-dimensionale lokale embeddings, Qdrant in-memory collectie voegde 8 vectoren toe, lichte herordening haalde het verwachte gedeelte op; optionele Ollama generatie voltooid met `phi4-mini:3.8b` |

De lokale notebook vermijdt opzettelijk hardcoded geheimen.

## Lokale Ollama Generatie

De Serie 2 notebook is standaard lokaal veilig. Om lokale Ollama-generatie in te schakelen, kopieer [.env.example](../../.env.example) naar `.env` en vul de Serie 2 waarden in.

Voor Series 2 Ollama-generatie, haal de commentaartekens weg bij:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

De Serie 2 notebook laadt automatisch `.env` vanuit de repository root met behulp van `python-dotenv`.

> [!IMPORTANT]
> Voeg geen `.env` bestanden, API-sleutels, privé endpoints, of tenant-specifieke waarden toe aan commits. De repository houdt opzettelijk geheimen buiten Markdown-bestanden en notebooks.

Vereisten-bestanden zijn gedocumenteerd in [requirements/README.md](./requirements/README.md).

Om links, notebook-structuur, netheid van notebookoutput, en hoog-risico geheimpatronen te valideren:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Verificatiescripts zijn gedocumenteerd in [scripts/README.md](./scripts/README.md).

Om alle lokale veilige notebooks in dezelfde omgeving uit te voeren:

```powershell
python scripts\verify_notebooks.py --execute
```

Dezelfde verificatiestroom wordt uitgevoerd in GitHub Actions bij pushes, pull requests en handmatig starten van workflows. Concept-artikelen en notebooks worden opzettelijk uitgesloten van het openbare verificatiepad.

Gebruik voor het publiceren van updates [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Zie [CHANGELOG.md](./CHANGELOG.md) voor de huidige niet-gepubliceerde wijzigingssamenvatting.

Voor richtlijnen over bijdragen en notebookhygiëne, zie [CONTRIBUTING.md](./CONTRIBUTING.md).

## Meertalige Ondersteuning

### Ondersteund via Co-op Translator (Geautomatiseerd en Altijd Up-to-Date)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabisch](../ar/README.md) | [Bengaals](../bn/README.md) | [Bulgaars](../bg/README.md) | [Birmaans (Myanmar)](../my/README.md) | [Chinees (Vereenvoudigd)](../zh-CN/README.md) | [Chinees (Traditioneel, Hong Kong)](../zh-HK/README.md) | [Chinees (Traditioneel, Macau)](../zh-MO/README.md) | [Chinees (Traditioneel, Taiwan)](../zh-TW/README.md) | [Kroatisch](../hr/README.md) | [Tsjechisch](../cs/README.md) | [Deens](../da/README.md) | [Nederlands](./README.md) | [Ests](../et/README.md) | [Fins](../fi/README.md) | [Frans](../fr/README.md) | [Duits](../de/README.md) | [Grieks](../el/README.md) | [Hebreeuws](../he/README.md) | [Hindi](../hi/README.md) | [Hongaars](../hu/README.md) | [Indonesisch](../id/README.md) | [Italiaans](../it/README.md) | [Japans](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreaans](../ko/README.md) | [Litouws](../lt/README.md) | [Maleis](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalees](../ne/README.md) | [Nigeriaans Pidgin](../pcm/README.md) | [Noors](../no/README.md) | [Perzisch (Farsi)](../fa/README.md) | [Pools](../pl/README.md) | [Portugees (Brazilië)](../pt-BR/README.md) | [Portugees (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Roemeens](../ro/README.md) | [Russisch](../ru/README.md) | [Servisch (Cyrillisch)](../sr/README.md) | [Slowaaks](../sk/README.md) | [Sloveens](../sl/README.md) | [Spaans](../es/README.md) | [Swahili](../sw/README.md) | [Zweeds](../sv/README.md) | [Tagalog (Filipijns)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turks](../tr/README.md) | [Oekraïens](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamees](../vi/README.md)

> **Liever lokaal klonen?**
>
> Deze repository bevat meer dan 50 taalvertalingen, wat de downloadgrootte aanzienlijk vergroot. Om zonder vertalingen te klonen, gebruik sparse checkout:
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
> Dit geeft je alles wat je nodig hebt om de cursus te voltooien met een veel snellere download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->