# Turuan ang AI na Sumagot ng Mga Tanong Batay sa Iyong Mga Dokumento

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

Ang repositoryong ito ay nangongolekta ng serye ng blog sa taong 2026 tungkol sa pagbuo ng mga document-grounded AI system gamit ang RAG, Azure AI services, mga open-source na alternatibo, at mga workflow na nakatuon sa pagsusuri.

## Background

Noong 2023, nagtrabaho ako sa isang pares ng mga tutorial tungkol sa pagtuturo sa ChatGPT na sumagot ng mga tanong mula sa mga PDF dokumento gamit ang Azure AI Search at Azure OpenAI. Ang ideya ng "ChatGPT sa iyong data" ay tila bago noon, at ang layunin ay ipakita ang isang praktikal na workflow: i-imbak ang mga dokumento, i-index ang mga ito, kunin ang kaugnay na nilalaman, at bumuo ng mga sagot mula sa nakuha na konteksto.

Noong 2026, mas malaki na ang ekosistema ng RAG. Sinusuportahan ng Azure AI Search ang mga modernong vector at hybrid retrieval pattern, bahagi ang Azure OpenAI ng mas malawak na Microsoft Foundry Models ecosystem, at ang mga open-source na tool tulad ng LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, at vLLM ay naging mga praktikal na pagpipilian para sa mga totoong sistema.

Kaya't gusto kong balikan ang paksa na ito. Hindi na lang tanong ngayon ang "Paano ba ako magtatayo ng RAG?" Maraming paraan na ngayon upang itayo ito, at ang mas mahalagang tanong ay "Anong arkitektura ang dapat kong piliin para sa aking sitwasyon?"

Nagsisimula ang seryeng ito mula sa layer ng pagpapasya, pagkatapos ay gawing mga hands-on na tutorial. Ang unang landas ng implementasyon ay nagtayo ng lokal na open-source RAG system na maaaring patakbuhin ng kahit sino gamit ang sample data, Qdrant, Ollama, at Phi-4-mini.

## Mga Artikulo

Tingnan ang [articles/README.md](./articles/README.md) para sa index ng mga artikulo.

1. [Serye 1: RAG, Azure kumpara sa Open-Source na mga Alternatibo, at Kailan Mahusay ang Fine-Tuning](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serye 2: Bumuo ng Lokal na Open-Source RAG System Mula Simula](./articles/series-2-open-source-rag-end-to-end.md)

Darating na susunod:

- Muling buuin ang parehong RAG system gamit ang Azure AI Search at Azure OpenAI.
- Magdagdag ng pagsusuri at regression checks lampas sa demo na sagot.

## Mga Notebook

Gumagamit ang mga implementation article ng mga notebook upang direktang masuri ang mga hakbang ng retrieval at pagsusuri. Tingnan ang [notebooks/README.md](./notebooks/README.md) para sa gabay sa folder.

> [!TIP]
> Simulan sa Serye 2 kung gusto mo ng pinakamabilis na landas. Patakbo ito nang lokal gamit ang sample data, CPU-friendly embeddings, Qdrant local mode, at walang cloud credentials.

| Serye | Notebook | Mga Kinakailangan | Lokal na beripikasyon |
| --- | --- | --- | --- |
| Serye 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Naberipikang Qdrant local mode, retrieval, reranking, at source wiring |

Para magpatakbo ng notebook nang lokal, gumawa ng virtual environment at i-install ang tumutugmang requirements file. Halimbawa:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```


## Sample Data

Gumagamit ang mga notebook ng maliit na lokal na korpus sa [sample_data](../../sample_data) kaya pwedeng patakbuhin ang mga halimbawa nang walang pribadong dokumento o cloud credentials. Tingnan ang [sample_data/README.md](./sample_data/README.md) para sa mga detalye.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Lokal na Buod ng Beripikasyon

Itinatala ang mga resulta ng beripikasyon sa bawat artikulo at sa [SERIES_PLAN.md](./SERIES_PLAN.md).

| Lugar | Resulta |
| --- | --- |
| Serye 2 open-source path | Nakabuo ng FastEmbed ng 384-dimension na lokal na embeddings, nag-insert ng 8 vectors ang Qdrant na in-memory collection, na-retrieve ang inaasahang seksyon gamit ang lightweight reranking; ang opsyonal na Ollama generation ay natapos gamit ang `phi4-mini:3.8b` |

Sadyang iniiwasan ng lokal na notebook ang mga hardcoded na sikreto.

## Lokal na Ollama Generation

Ang Serye 2 notebook ay lokal-safe bilang default. Para paganahin ang lokal na Ollama generation, kopyahin ang [.env.example](../../.env.example) papuntang `.env` at punan ang mga value ng Serye 2.

Para sa Serye 2 Ollama generation, i-uncomment:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```


Awtomatikong niloload ng Serye 2 notebook ang `.env` mula sa root ng repository gamit ang `python-dotenv`.

> [!IMPORTANT]
> Huwag mag-commit ng `.env` files, API keys, private endpoints, o tenant-specific na mga value. Sadyang iniiwasan ng repository ang magsama ng mga sikreto sa mga Markdown file at mga notebook.

Ang mga requirements file ay dokumentado sa [requirements/README.md](./requirements/README.md).

Para i-validate ang mga link, istruktura ng notebook, kalinisan ng output ng notebook, at mga high-risk na pattern ng sikreto:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```


Ang mga verification script ay dokumentado sa [scripts/README.md](./scripts/README.md).

Para patakbuhin ang lahat ng lokal-safe na notebook sa iisang environment:

```powershell
python scripts\verify_notebooks.py --execute
```


Ang parehong daloy ng beripikasyon ay tumatakbo sa GitHub Actions sa mga push, pull request, at manual workflow dispatch. Ang mga draft na artikulo at notebook ay sadyang hindi isinama sa public verification path.

Bago mag-publish ng mga update, gamitin ang [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Tingnan ang [CHANGELOG.md](./CHANGELOG.md) para sa kasalukuyang hindi pa nailalathalang buod ng mga pagbabago.

Para sa mga panuntunan sa kontribusyon at kalinisan ng notebook, tingnan ang [CONTRIBUTING.md](./CONTRIBUTING.md).

## Multi-Language Support

### Sinusuportahan sa pamamagitan ng Co-op Translator (Awtomatik at Laging Napapanahon)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](./README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Mas Gusto Mo Bang I-clone Nang Lokal?**
>
> Kasama sa repositoryong ito ang mahigit 50 na pagsasalin ng wika na nagpapa-taas nang malaki sa laki ng pag-download. Para mag-clone nang walang mga pagsasalin, gamitin ang sparse checkout:
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
> Bibigyan ka nito ng lahat ng kailangan mo para matapos ang kurso nang mas mabilis ang pag-download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->