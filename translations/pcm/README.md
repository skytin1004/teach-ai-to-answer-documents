# Teach AI to Answer Questions Based on Your Documents

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

Dis repository dey collect one 2026 blog series about how to build document-grounded AI systems wit RAG, Azure AI services, open-source alternatives, and workflows wey dey focus on evaluation.

## Background

For 2023, I work on two tutorials wey teach how ChatGPT fit answer questions from PDF documents using Azure AI Search and Azure OpenAI. The idea of "ChatGPT for your data" still be new den, and the aim na to show practical workflow: store documents, index dem, find relevant content, and generate answers from the context wey dem retrieve.

For 2026, the RAG ecosystem don big well-well. Azure AI Search dey support modern vector and hybrid retrieval patterns, Azure OpenAI be part of the bigger Microsoft Foundry Models ecosystem, and open-source tools like LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, and vLLM don become practical choices for real systems.

Na why I want make we revisit this topic. The question no be just "How I go build RAG?" again. Now, plenty ways dey to build am, and the important question na "Which architecture suppose I choose for my situation?"

Dis series go start from the decision-making layer, then turn am into hands-on tutorials. The first implementation path go build one local open-source RAG system wey anybody fit run wit sample data, Qdrant, Ollama, and Phi-4-mini.

## Articles

See [articles/README.md](./articles/README.md) for the article index.

1. [Series 1: RAG, Azure vs Open-Source Alternatives, and When Fine-Tuning Makes Sense](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Series 2: Build a Local Open-Source RAG System End to End](./articles/series-2-open-source-rag-end-to-end.md)

Wetin dey come next:

- Rebuild the same RAG system wit Azure AI Search and Azure OpenAI.
- Add evaluation and regression checks pass one demo answer.

## Notebooks

The implementation articles dey use notebooks so that den retrieval and evaluation steps fit dey inspected directly. Check [notebooks/README.md](./notebooks/README.md) for folder-level guidance.

> [!TIP]
> Start wit Series 2 if you want the fastest path. E dey run locally wit sample data, CPU-friendly embeddings, Qdrant local mode, and no cloud credentials.

| Series | Notebook | Requirements | Local verification |
| --- | --- | --- | --- |
| Series 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant local mode, retrieval, reranking, and source wiring verified |

To run notebook locally, create virtual environment and install the matching requirements file. For example:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Sample Data

The notebooks dey use small local corpus for [sample_data](../../sample_data) so dat examples fit run without private documents or cloud credentials. See [sample_data/README.md](./sample_data/README.md) for details.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Local Verification Summary

Verification results dey recorded for each article and for [SERIES_PLAN.md](./SERIES_PLAN.md).

| Area | Result |
| --- | --- |
| Series 2 open-source path | FastEmbed generate 384-dimension local embeddings, Qdrant in-memory collection insert 8 vectors, lightweight reranking retrieve the expected section; optional Ollama generation complete wit `phi4-mini:3.8b` |

The local notebook purposely no use hardcoded secrets.

## Local Ollama Generation

The Series 2 notebook be local-safe by default. To enable local Ollama generation, copy [.env.example](../../.env.example) to `.env` and fill the Series 2 values.

For Series 2 Ollama generation, remove comment:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

The Series 2 notebook automatically load `.env` from repository root using `python-dotenv`.

> [!IMPORTANT]
> No commit `.env` files, API keys, private endpoints, or tenant-specific values. The repository purposely keep secrets out of Markdown files and notebooks.

Requirements files dey documented for [requirements/README.md](./requirements/README.md).

To validate links, notebook structure, notebook output cleanliness, and high-risk secret patterns:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Verification scripts dey documented for [scripts/README.md](./scripts/README.md).

To run all local-safe notebooks in one environment:

```powershell
python scripts\verify_notebooks.py --execute
```

The same verification flow dey run for GitHub Actions on pushes, pull requests, and manual workflow dispatches. Draft articles and notebooks purposely no dey inside the public verification path.

Before you update for publishing, use [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

See [CHANGELOG.md](./CHANGELOG.md) for current unpublished change summary.

For contribution and notebook hygiene guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Multi-Language Support

### Supported via Co-op Translator (Automated and Always Up-to-Date)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](./README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **You wan Clone am Locally?**
>
> Dis repository get 50+ language translations wey dey make download size big well. To clone without translations, use sparse checkout:
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
> Dis go give you everything wey you need to finish the course with faster download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->