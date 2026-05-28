# Învățați AI să răspundă la întrebări pe baza documentelor dvs. - Planul seriei

Acest plan urmărește lansarea publică a Seriei 1 și Seriei 2. Ulterior, lucrările Azure și evaluarea sunt păstrate ca ciorne până când exemplele sunt complet end-to-end și verificate.

Nu efectuați commit sau push la modificări până nu primiți instrucțiuni explicite.

## Domeniul public

Lansarea publică curentă:

- Articol Seria 1: decizii de arhitectură RAG, compromisuri Azure vs open-source și unde se potrivește fine-tuning-ul.
- Articol Seria 2: tutorial local RAG open-source.
- Notebook Seria 2: laborator RAG local executabil cu FastEmbed, Qdrant, Ollama și Phi-4-mini.
- Date de probă: fișiere Markdown cu politica școlii și ghidul AI pentru cursuri.

Ciorne redactate, dar încă neindexate public:

- Reconstrucția Azure AI Search și Azure OpenAI.
- Evaluarea RAG și verificări de regresie.

## Scenariul tutorialului

Scenariul partajat este un asistent pentru politica școlii.

Asistentul răspunde la această întrebare din documentele locale:

```text
Can I use generative AI for my final assignment?
```


Comportamentul așteptat este:

1. Încărcarea documentelor Markdown locale.
2. Parsarea și fragmentarea lor după titluri.
3. Crearea de embedding-uri locale și stocarea reprezentărilor căutabile cu metadate.
4. Recuperarea secțiunii relevante din politică.
5. Reclasarea când este necesar.
6. Generarea sau compunerea unui răspuns fundamentat.
7. Returnarea citărilor.
8. Înregistrarea rezultatelor verificării.

## Structura publică curentă

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


Materialul în ciornă este stocat în `drafts/` și este omis de verificarea depozitului până când este gata pentru indexare publică.

## Verificarea Seriei 2

Verificat pe Windows cu Python 3.12.6.

- Instalare cu succes a `requirements/open-source-rag.txt`.
- Execuție `notebooks/series-2-open-source-rag.ipynb` cu `nbclient`.
- Verificare locală reușită: 2 documente de probă încărcate, 8 fragmente create, FastEmbed a generat embedding-uri locale de 384 dimensiuni, colecția în memorie Qdrant inițializată și 8 vectori inserați.
- Întrebarea de test: "Pot folosi AI generativ pentru tema mea finală?"
- Sursele de top recuperate după reclasare ușoară: `school_ai_policy.md`.
- Secțiunea de top recuperată după reclasare ușoară: `Final Assignments`.
- Cale implicită de răspuns: compozitor local de răspunsuri transparente.
- Ollama instalat prin winget; `phi4-mini:3.8b` tras cu succes.
- Cale de generare răspuns Ollama: finalizată cu `phi4-mini:3.8b`.
- Dimensiunea fișierului model Ollama: circa 2.49GB pe disc.
- Dimensiunea modelului încărcat Ollama: 3.3GB raportat de `ollama ps`.
- Descărcare GPU: 100% GPU raportat de `ollama ps` pe RTX 3060 Laptop GPU.
- Memorie GPU observată după generare: circa 3.5GB din 6GB.
- Execuția notebook-ului cu model FastEmbed în cache și generarea Ollama activată a trecut în circa 34 de secunde prin scriptul de verificare.
- Observație: o primă trecere de încărcare documente a inclus accidental `sample_data/README.md`; acum notebook-ul încarcă explicit doar cele două documente de probă intenționate.

## Verificarea depozitului

- `scripts/verify_notebooks.py` validează linkuri locale Markdown, JSON-ul notebook-ului, curățenia output-ului notebook-ului și modele de secrete cu risc ridicat.
- `scripts/verify_notebooks.py --execute` rulează notebook-urile publice din rădăcina depozitului.
- Materialul în ciornă din `drafts/` este omis intenționat.

## Lucrările următoare

- Reconstruirea aceluiași scenariu cu Azure AI Search și Azure OpenAI ca parte a unei serii viitoare.
- Adăugarea evaluării recuperării și a răspunsului după ce implementările locale și Azure sunt ambele stabile.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->