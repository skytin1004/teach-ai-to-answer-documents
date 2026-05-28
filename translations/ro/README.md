# Învățați AI să Răspundă la Întrebări Bazate pe Documentele Dumneavoastră

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

Acest depozit colectează o serie de bloguri din 2026 despre construirea sistemelor AI bazate pe documente cu RAG, serviciile Azure AI, alternative open-source și fluxuri de lucru orientate spre evaluare.

## Context

În 2023, am lucrat la o pereche de tutoriale despre cum să înveți ChatGPT să răspundă la întrebări din documente PDF folosind Azure AI Search și Azure OpenAI. Ideea de „ChatGPT pe datele tale” părea încă nouă atunci, iar scopul era să arăt un flux de lucru practic: stocarea documentelor, indexarea lor, recuperarea conținutului relevant și generarea răspunsurilor pornind de la contextul extras.

În 2026, ecosistemul RAG este mult mai mare. Azure AI Search suportă modelele moderne de recuperare vectorială și hibridă, Azure OpenAI face parte din ecosistemul mai larg Microsoft Foundry Models, iar unelte open-source precum LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama și vLLM au devenit opțiuni practice pentru sisteme reale.

De aceea am vrut să revin asupra acestui subiect. Întrebarea nu mai este doar „Cum construiesc RAG?” Acum există multe moduri de a-l construi, iar întrebarea mai importantă este „Ce arhitectură ar trebui să aleg pentru situația mea?”

Această serie pornește de la acel strat decizional, apoi îl transformă în tutoriale practice. Primul drum de implementare construiește un sistem RAG open-source local pe care oricine îl poate rula cu date de probă, Qdrant, Ollama și Phi-4-mini.

## Articole

Consultați [articles/README.md](./articles/README.md) pentru indexul articolelor.

1. [Seria 1: RAG, alternative Azure vs open-source și când are sens fine-tuning-ul](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Seria 2: Construiește un sistem RAG open-source local de la început până la sfârșit](./articles/series-2-open-source-rag-end-to-end.md)

Urmează:

- Reconstruirea aceluiași sistem RAG cu Azure AI Search și Azure OpenAI.
- Adăugarea evaluării și verificărilor regresive dincolo de un răspuns demo.

## Notebook-uri

Articolele de implementare folosesc notebook-uri pentru ca pașii de recuperare și evaluare să poată fi inspectați direct. Consultați [notebooks/README.md](./notebooks/README.md) pentru orientări la nivel de folder.

> [!TIP]
> Începeți cu Seria 2 dacă doriți calea cea mai rapidă. Rulează local cu date de probă, embedding-uri prietenoase cu CPU, modul local Qdrant și fără credențiale cloud.

| Serie | Notebook | Cerințe | Verificare locală |
| --- | --- | --- | --- |
| Seria 2 | [Notebook RAG open-source](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Modul local Qdrant, recuperare, reranking și conexiune sursă verificate |

Pentru a rula un notebook local, creați un mediu virtual și instalați fișierul de cerințe corespunzător. De exemplu:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Date de probă

Notebook-urile folosesc un corpus local mic în [sample_data](../../sample_data) pentru ca exemplele să poată rula fără documente private sau credențiale cloud. Consultați [sample_data/README.md](./sample_data/README.md) pentru detalii.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Rezumat verificare locală

Rezultatele verificării sunt înregistrate în fiecare articol și în [SERIES_PLAN.md](./SERIES_PLAN.md).

| Domeniu | Rezultat |
| --- | --- |
| Drumul open-source din Seria 2 | FastEmbed a generat embedding-uri locale de 384 dimensiuni, colecția în memorie Qdrant a inserat 8 vectori, reranking-ul ușor a recuperat secțiunea așteptată; generarea opțională cu Ollama s-a finalizat folosind `phi4-mini:3.8b` |

Notebook-ul local evită intenționat secretele codificate direct.

## Generare locală Ollama

Notebook-ul din Seria 2 este implicit sigur pentru rulare locală. Pentru a activa generarea locală Ollama, copiați [.env.example](../../.env.example) în `.env` și completați valorile pentru Seria 2.

Pentru generarea Ollama din Seria 2, decomentați:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook-ul din Seria 2 încarcă automat `.env` din rădăcina depozitului folosind `python-dotenv`.

> [!IMPORTANT]
> Nu comiteți fișiere `.env`, chei API, endpoint-uri private sau valori specifice tenant-ului. Depozitul evită intenționat să păstreze secrete în fișiere Markdown sau notebook-uri.

Fișierele de cerințe sunt documentate în [requirements/README.md](./requirements/README.md).

Pentru a valida linkurile, structura notebook-ului, curățenia output-ului și tiparele de secrete cu risc ridicat:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Scripturile de verificare sunt documentate în [scripts/README.md](./scripts/README.md).

Pentru a executa toate notebook-urile sigure local în același mediu:

```powershell
python scripts\verify_notebooks.py --execute
```

Același flux de verificare rulează în GitHub Actions la push-uri, pull requests și porniri manuale de workflow. Articolele și notebook-urile în stadiu draft sunt excluse intenționat din fluxul public de verificare.

Înainte de a publica actualizări, folosiți [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Consultați [CHANGELOG.md](./CHANGELOG.md) pentru rezumatul curent al schimbărilor nepublicate.

Pentru ghiduri privind contribuțiile și igiena notebook-urilor, vedeți [CONTRIBUTING.md](./CONTRIBUTING.md).

## Suport multilingv

### Suportat prin Co-op Translator (automatizat și mereu actualizat)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabă](../ar/README.md) | [Bengaleză](../bn/README.md) | [Bulgară](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chineză (simplificată)](../zh-CN/README.md) | [Chineză (tradițională, Hong Kong)](../zh-HK/README.md) | [Chineză (tradițională, Macau)](../zh-MO/README.md) | [Chineză (tradițională, Taiwan)](../zh-TW/README.md) | [Croată](../hr/README.md) | [Cehă](../cs/README.md) | [Daneză](../da/README.md) | [Olandeză](../nl/README.md) | [Estonă](../et/README.md) | [Finlandeză](../fi/README.md) | [Franceză](../fr/README.md) | [Germană](../de/README.md) | [Greacă](../el/README.md) | [Ebraică](../he/README.md) | [Hindi](../hi/README.md) | [Maghiară](../hu/README.md) | [Indoneziană](../id/README.md) | [Italiană](../it/README.md) | [Japoneză](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coreeană](../ko/README.md) | [Lituaniană](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepaleză](../ne/README.md) | [Pidgin nigerian](../pcm/README.md) | [Norvegiană](../no/README.md) | [Persană (Farsi)](../fa/README.md) | [Poloneză](../pl/README.md) | [Portugheză (Brazilia)](../pt-BR/README.md) | [Portugheză (Portugalia)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Română](./README.md) | [Rusă](../ru/README.md) | [Sârbă (chirilică)](../sr/README.md) | [Slovac](../sk/README.md) | [Slovenă](../sl/README.md) | [Spaniolă](../es/README.md) | [Swahili](../sw/README.md) | [Suedeză](../sv/README.md) | [Tagalog (Filipineză)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thailandeză](../th/README.md) | [Turcă](../tr/README.md) | [Ucraineană](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnameză](../vi/README.md)

> **Preferi să clonezi local?**
>
> Acest depozit include peste 50 de traduceri în limbi diferite, ceea ce crește semnificativ mărimea descărcării. Pentru a clona fără traduceri, folosește sparse checkout:
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
> Astfel obții tot ce ai nevoie pentru a finaliza cursul cu o descărcare mult mai rapidă.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->