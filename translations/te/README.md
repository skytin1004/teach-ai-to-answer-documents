# మీ డాక్యుమెంట్ల ఆధారంగా ప్రశ్నలకు సమాధానం చెప్పేందుకు AIని పాఠం చెప్పండి

![డాక్యుమెంట్-గ్రౌండెడ్ AI RAG సిస్టమ్ అవలోకనం](../../assets/images/readme-hero.svg)

ఈ రీపోజిటరీ 2026 బ్లాగ్ సిరీస్‌ను సేకరిస్తుంది, ఇది RAG, Azure AI సర్వీసులు, ఓపెన్-సోర్స్ ప్రత్యామ్నాయాలు మరియు మూల్యాంకన-ఆధారిత వర్క్‌ఫ్లోలతో డాక్యుమెంట్-గ్రౌండెడ్ AI సిస్టమ్లను నిర్మించే గురించి.

## నేపథ్యం

2023లో, నేను Azure AI Search మరియు Azure OpenAI ఉపయోగించి PDF డాక్యుమెంట్ల నుండి ప్రశ్నలకు సమాధానం చెప్పడానికి ChatGPTని సికిందాలి నేర్పించే రెండు పాఠాలపై పని చేశాను. "మీ డేటాపై ChatGPT" అనే ఆలోచన అప్పటికీ కొత్తగా అనిపించింది, మరియు లక్ష్యం ప్రాక్టికల్ వర్క్‌ఫ్లోను చూపించడం: డాక్యుమెంట్లను నిల్వ చేయడం, వాటిని ఇండెక్స్ చేయడం, సంబంధిత కంటెంట్‌ను తీసుకురావడం మరియు ఆ తీసుకువచ్చిన సందర్భం నుండి సమాధానాలు సృష్టించడం.

2026లో, RAG పర్యావరణం చాలా పెద్దది అయింది. Azure AI Search సమకాలీన వెక్టర్ మరియు హైబ్రిడ్ రిట్రీవల్ మోడల్స్‌కు మద్దతు ఇస్తుంది, Azure OpenAI Microsoft Foundry Models పర్యావరణంలో భాగంగా ఉంది, మరియు LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, మరియు vLLM వంటి ఓపెన్-సోర్స్ టూల్స్ వాస్తవిక సిస్టమ్స్ కోసం ప్రాక్టికల్ ఎంపికలుగా మారాయి.

అందుకే ఈ విషయం మీద తిరిగి చూడదల్చుకున్నాను. ఇప్పుడు ప్రశ్న "నేను RAG ఎలా నిర్మించాలి?" మాత్రమే కాదు. నిర్మించే అనేక మార్గాలు ఉన్నాయి మరియు మరికొద్ది ముఖ్యమైన ప్రశ్న "నా పరిస్థితికి ఏ ఆర్కిటెక్చర్‌ను ఎంచుకోవాలి?" అనేది.

ఈ సిరీస్ ఆ నిర్ణయం తీసుకునే పొర నుండి మొదలవుతుంది, ఆ తరువాత దాన్ని హ్యాండ్స్-ఆన్ ట్యుటోరియల్స్‌గా మార్చుతుంది. మొదటి అమలు మార్గం ప్రత్యామ్నాయకంగా ఓపెన్-సోర్స్ RAG సిస్టమ్‌ను నిర్మిస్తుంది, దీన్ని ఎవరు కావచ్చైతే నమూనా డేటాతో, Qdrant, Ollama మరియు Phi-4-mini తో నడపవచ్చు.

## వ్యాసాలు

వ్యాస సూచిక కోసం [articles/README.md](./articles/README.md) చూడండి.

1. [సిరీస్ 1: RAG, Azure మరియు ఓపెన్-సోర్స్ ప్రత్యామ్నాయాలు, మరియు ఫైన్-ట్యూన్‌డ్ అవసరం ఎప్పుడు](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [సిరీస్ 2: ఒక లోకల్ ఓపెన్-సోర్స్ RAG సిస్టమ్ నంతస్థం నిర్మించండి](./articles/series-2-open-source-rag-end-to-end.md)

ఇప్పటికే రాబోతున్నవి:

- అదే RAG సిస్టమ్‌ను Azure AI Search మరియు Azure OpenAIతో తిరిగి నిర్మించండి.
- డెమో సమాధానంతో పాటు మూల్యాంకన మరియు రిగ్రెషన్ చెక్‌లను జోడించండి.

## నోటుబుక్స్

అమలు వ్యాసాలు నోటుబుక్స్ ఉపయోగిస్తాయి, కాబట్టి రిట్రీవల్ మరియు మూల్యాంకన దశలను నేరుగా పరిశీలించవచ్చు. ఫోల్డర్ స్థాయి గైడన్స్ కోసం [notebooks/README.md](./notebooks/README.md) చూడండి.

> [!TIP]
> మీరు వేగవంతమైన మార్గం కావాలంటే, సిరీస్ 2 తో మొదలు పెట్టండి. ఇది లోకల్‌గా నమూనా డేటాతో, CPU-స్నేహపూర్వక ఎంబెడ్డింగ్స్, Qdrant లోకల్ మోడ్, మరియు క్లౌడ్ క్రెడెన్షియల్స్ లేకుండా నడుస్తుంది.

| సిరీస్ | నోటుబుక్ | అవసరాలు | లోకల్ వెరిఫికేషన్ |
| --- | --- | --- | --- |
| సిరీస్ 2 | [ఓపెన్-సోర్స్ RAG నోటుబుక్](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant లోకల్ మోడ్, రిట్రీవల్, రీరాంకింగ్ మరియు సోర్స్ వైర్యింగ్ ధృవీకరించబడింది |

లోకల్‌గా నోటుబుక్ నడపడానికి, వర్చువల్ ఎన్విరోన్మెంట్ సృష్టించి సరిపోయే అవసరాలు ఫైల్‌ను ఇన్‌స్టాల్ చేయండి. ఉదాహరణకు:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## నమూనా డేటా

నోటుబుక్స్ చిన్న లోకల్ కార్పస్ను [sample_data](../../sample_data)లో ఉపయోగిస్తాయి, అందువల్ల ఉదాహరణలు ప్రైవేట్ డాక్యుమెంట్లు లేదా క్లౌడ్ క్రెడెన్షియల్స్ లేకుండా పనిచేస్తాయి. వివరాలకు [sample_data/README.md](./sample_data/README.md) చూడండి.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## లోకల్ వెరిఫికేషన్ సారాంశం

ధృవీకరణ ఫలితాలు ప్రతి వ్యాసంలో మరియు [SERIES_PLAN.md](./SERIES_PLAN.md)లో నమోదు చేయబడ్డాయి.

| ప్రాంతం | ఫలితం |
| --- | --- |
| సిరీస్ 2 ఓపెన్-సోర్స్ మార్గం | FastEmbed సహాయంతో 384-డైమెన్షన్ లోకల్ ఎంబెడ్డింగ్స్ సృష్టించబడ్డాయి, Qdrant మెమొరీలో 8 వెక్టర్లు చేర్చబడ్డాయి, లైట్వెయిట్ రీరాంకింగ్ ఆశించిన సెక్షన్ తీసుకొచ్చింది; ఐచ్ఛికంగా Ollama జనరేషన్ `phi4-mini:3.8b`తో పూర్తిచేయబడింది |

లోకల్ నోటుబుక్ చటుక్కైన రహస్యాలను ముట్టుకోదు.

## లోకల్ Ollama జనరేషన్

సిరీస్ 2 నోటుబుక్ డిఫాల్ట్‌గా లోకల్-సురక్షితంగా ఉంటుంది. లోకల్ Ollama జనరేషన్‌ను ఎనేబుల్ చేయడానికి, [.env.example](../../.env.example)ని `.env`కి కాపీ చేసి సిరీస్ 2 విలువలు పూరించండి.

సిరీస్ 2 Ollama జనరేషన్ కోసం, అనుమతించండి:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

సిరీస్ 2 నోటుబుక్ ఆటోమేటిగ్గా డిపాజిటరీ రూట్ నుండి `.env` ని `python-dotenv` ఉపయోగించి లోడ్ చేస్తుంది.

> [!IMPORTANT]
> `.env` ఫైళ్లను, API కీలు, ప్రైవేట్ ఎండ్పాయింట్లు లేదా టెనెంట్-ప్రత్యేక విలువలను కమిట్ చేయవద్దు. రీపోజిటరీ కలర్, మార్క్డౌన్ ఫైళ్లు మరియు నోటుబుక్స్ నుండి రహస్యాలను అవగాహనపూర్వకంగా దూరంగా ఉంచుతుంది.

అవసరాలైన ఫైళ్లను [requirements/README.md](./requirements/README.md)లో డాక్యుమెంట్ చేశారు.

లింకులు, నోటుబుక్ నిర్మాణం, నోటుబుక్ అవుట్పుట్ శుద్ధి మరియు హై-రిస్క్ రహస్య నమూనాల్ని ధ్రువీకరించడానికి:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

ధృవీకరణ స్క్రిప్ట్‌లు [scripts/README.md](./scripts/README.md)లో పేర్కొనబడ్డాయి.

అన్ని లోకల్-సురక్షిత నోటుబుక్స్‌ను ఒకే ఎన్విరోన్మెంట్‌లో అమలు చేసేందుకు:

```powershell
python scripts\verify_notebooks.py --execute
```

అదే ధృవీకరణ వర్క్‌ఫ్లో GitHub Actionsలో PUSHES, PULL REQUESTS, మరియు మ్యాన్యువల్ వర్క్‌ఫ్లో డిస్‌ప్యాచెస్‌పై నడుస్తుంది. డ్రాఫ్ట్ వ్యాసాలు, నోటుబుక్స్ పబ్లిక్ ధృవీకరణ మార్గం నుండి తప్పవేసినవి.

అప్డేట్లు ప్రచురించడానికి ముందు, [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) ఉపయోగించండి.

ప్రస్తుత ప్రచురించని మార్పుల సారాంశం కోసం [CHANGELOG.md](./CHANGELOG.md) చూడండి.

కాంట్రిబ్యూషన్ మరియు నోటుబుక్ అనుకూలత మార్గదర్శకాలకు [CONTRIBUTING.md](./CONTRIBUTING.md) చూడండి.

## బహుభాషా మద్దతు

### కో-ఆప్ ట్రాన్స్లేటర్ ద్వారా మద్దతు (ఆటోమేటెడ్ మరియు ఎప్పటికప్పుడు నవీకరించబడుతుంది)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](./README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **స్థానికంగా క్లోన్ చేయడం ఇష్టమా?**
>
> ఈ రీపోజిటరీ 50+ భాషా అనువాదాలను కలిగి ఉంది, ఇది డౌన్లోడ్ పరిమాణాన్ని గణనీయంగా పెంచుతుంది. అనువాదాలు లేకుండా క్లోన్ చేయడానికి, స్పార్స్ చెకౌట్ ఉపయోగించండి:
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
> ఇది కోర్సు పూర్తి చేసుకోవడానికి మీరు అవసరమైన అన్నింటినీ ఒక వేగవంతమైన డౌన్లోడ్‌తో ఇస్తుంది.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్వీకరణ**:
ఈ పత్రం AI అనువాద సేవ [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నిస్తున్నప్పటికీ, ఆటోమేటెడ్ అనువాదాలు తప్పులు లేదా అసమగ్రతలను కలిగి ఉండవచ్చు. దాని స్వదేశ భాషలో ఉన్న అసలు పత్రాన్ని అధికారం కలిగిన మూలంగా పరిగణించాలి. కీలకమైన సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదాన్ని సిఫారసు చేస్తాము. ఈ అనువాదం ఉపయోగం వల్ల కలిగే ఏవైనా అపార్థాలు లేదా తప్పుదారులు కోసం మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->