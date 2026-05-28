# నోట్‌బుక్స్

ఈ నోట్‌బుక్స్ ఆర్టికల్ సిరీస్‌ను ఆచరణాత్మక ఉదాహరణలతో మద్దతు ఇస్తాయి.

| నోట్‌బుక్ | ఆర్టికల్ | ఉద్దేశ్యం |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [సిరీస్ 2](../articles/series-2-open-source-rag-end-to-end.md) | ఫాస్ట్‌ఎంబెడ్, క్యూడ్రాంట్ లోకల్ మోడ్, రిట్రీవల్, రీరాంకింగ్, ఐచ్ఛిక ఒల్లామా జనరేషన్, మరియు సోర్స్ సూచనలతో ఓపెన్-సోర్స్ RAG |

## స్థానికంగా ఇది నడపండి

నీయొక్క నోట్‌బుక్ నడపడానికి అవసరమైన ఆకాంక్షలను ఇన్‌స్టాల్ చెయ్యండి:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

లేదా అన్ని డిపెండెన్సీలను ఇన్‌స్టాల్ చేయండి:

```powershell
python -m pip install -r requirements\all.txt
```

## ధృవీకరించండి

రిపాజిటరీ రూట్ నుండి:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

సిరీస్ 2 ఒక రిపాజిటరీ-రూట్ `.env` ఫైల్ నుండి ఒల్లామా కాన్ఫిగరేషన్‌ను చదవగలదు. సిరీస్ ఆధారంగా గుంపుగా ఉన్న [../.env.example](../../../.env.example) నుండి ప్రారంభించండి.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్వీకరణ**:
ఈ పత్రం AI అనువాద సేవ [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నిస్తున్నప్పటికీ, ఆటోమేటెడ్ అనువాదాలు తప్పులు లేదా అసమగ్రతలను కలిగి ఉండవచ్చు. దాని స్వదేశ భాషలో ఉన్న అసలు పత్రాన్ని అధికారం కలిగిన మూలంగా పరిగణించాలి. కీలకమైన సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదాన్ని సిఫారసు చేస్తాము. ఈ అనువాదం ఉపయోగం వల్ల కలిగే ఏవైనా అపార్థాలు లేదా తప్పుదారులు కోసం మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->