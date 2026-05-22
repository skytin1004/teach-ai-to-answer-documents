# Teach AI to Answer Questions Based on Your Documents

![Document-grounded AI RAG system overview](./assets/images/readme-hero.svg)

This repository collects a 2026 blog series about building document-grounded AI systems with RAG, Azure AI services, open-source alternatives, and evaluation-oriented workflows.

## Background

In 2023, I worked on a pair of tutorials about teaching ChatGPT to answer questions from PDF documents using Azure AI Search and Azure OpenAI. The idea of "ChatGPT on your data" still felt new then, and the goal was to show a practical workflow: store documents, index them, retrieve relevant content, and generate answers from that retrieved context.

In 2026, the RAG ecosystem is much larger. Azure AI Search supports modern vector and hybrid retrieval patterns, Azure OpenAI is part of the broader Microsoft Foundry Models ecosystem, and open-source tools such as LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, and vLLM have become practical choices for real systems.

That is why I wanted to revisit this topic. The question is no longer only "How do I build RAG?" There are now many ways to build it, and the more important question is "Which architecture should I choose for my situation?"

This series starts from that decision-making layer, then turns it into hands-on tutorials. The first implementation path builds a local open-source RAG system that anyone can run with sample data, Qdrant, Ollama, and Phi-4-mini.

## Articles

See [articles/README.md](./articles/README.md) for the article index.

1. [Series 1: RAG, Azure vs Open-Source Alternatives, and When Fine-Tuning Makes Sense](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Series 2: Build a Local Open-Source RAG System End to End](./articles/series-2-open-source-rag-end-to-end.md)

Coming next:

- Rebuild the same RAG system with Azure AI Search and Azure OpenAI.
- Add evaluation and regression checks beyond a demo answer.

## Notebooks

The implementation articles use notebooks so the retrieval and evaluation steps can be inspected directly. See [notebooks/README.md](./notebooks/README.md) for folder-level guidance.

> [!TIP]
> Start with Series 2 if you want the fastest path. It runs locally with sample data, CPU-friendly embeddings, Qdrant local mode, and no cloud credentials.

| Series | Notebook | Requirements | Local verification |
| --- | --- | --- | --- |
| Series 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](./requirements/open-source-rag.txt) | Qdrant local mode, retrieval, reranking, and source wiring verified |

To run a notebook locally, create a virtual environment and install the matching requirements file. For example:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Sample Data

The notebooks use a small local corpus in [sample_data](./sample_data/) so the examples can run without private documents or cloud credentials. See [sample_data/README.md](./sample_data/README.md) for details.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Local Verification Summary

Verification results are recorded in each article and in [SERIES_PLAN.md](./SERIES_PLAN.md).

| Area | Result |
| --- | --- |
| Series 2 open-source path | FastEmbed generated 384-dimension local embeddings, Qdrant in-memory collection inserted 8 vectors, lightweight reranking retrieved the expected section; optional Ollama generation completed with `phi4-mini:3.8b` |

The local notebook intentionally avoids hardcoded secrets.

## Local Ollama Generation

The Series 2 notebook is local-safe by default. To enable local Ollama generation, copy [.env.example](./.env.example) to `.env` and fill in the Series 2 values.

For Series 2 Ollama generation, uncomment:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

The Series 2 notebook automatically loads `.env` from the repository root by using `python-dotenv`.

> [!IMPORTANT]
> Do not commit `.env` files, API keys, private endpoints, or tenant-specific values. The repository intentionally keeps secrets out of Markdown files and notebooks.

Requirements files are documented in [requirements/README.md](./requirements/README.md).

To validate links, notebook structure, notebook output cleanliness, and high-risk secret patterns:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Verification scripts are documented in [scripts/README.md](./scripts/README.md).

To execute all local-safe notebooks in the same environment:

```powershell
python scripts\verify_notebooks.py --execute
```

The same verification flow runs in GitHub Actions on pushes, pull requests, and manual workflow dispatches. Draft articles and notebooks are intentionally excluded from the public verification path.

Before publishing updates, use [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

See [CHANGELOG.md](./CHANGELOG.md) for the current unpublished change summary.

For contribution and notebook hygiene guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Multi-Language Support

### Supported via Co-op Translator (Automated and Always Up-to-Date)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](./translations/ar/README.md) | [Bengali](./translations/bn/README.md) | [Bulgarian](./translations/bg/README.md) | [Burmese (Myanmar)](./translations/my/README.md) | [Chinese (Simplified)](./translations/zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](./translations/zh-HK/README.md) | [Chinese (Traditional, Macau)](./translations/zh-MO/README.md) | [Chinese (Traditional, Taiwan)](./translations/zh-TW/README.md) | [Croatian](./translations/hr/README.md) | [Czech](./translations/cs/README.md) | [Danish](./translations/da/README.md) | [Dutch](./translations/nl/README.md) | [Estonian](./translations/et/README.md) | [Finnish](./translations/fi/README.md) | [French](./translations/fr/README.md) | [German](./translations/de/README.md) | [Greek](./translations/el/README.md) | [Hebrew](./translations/he/README.md) | [Hindi](./translations/hi/README.md) | [Hungarian](./translations/hu/README.md) | [Indonesian](./translations/id/README.md) | [Italian](./translations/it/README.md) | [Japanese](./translations/ja/README.md) | [Kannada](./translations/kn/README.md) | [Khmer](./translations/km/README.md) | [Korean](./translations/ko/README.md) | [Lithuanian](./translations/lt/README.md) | [Malay](./translations/ms/README.md) | [Malayalam](./translations/ml/README.md) | [Marathi](./translations/mr/README.md) | [Nepali](./translations/ne/README.md) | [Nigerian Pidgin](./translations/pcm/README.md) | [Norwegian](./translations/no/README.md) | [Persian (Farsi)](./translations/fa/README.md) | [Polish](./translations/pl/README.md) | [Portuguese (Brazil)](./translations/pt-BR/README.md) | [Portuguese (Portugal)](./translations/pt-PT/README.md) | [Punjabi (Gurmukhi)](./translations/pa/README.md) | [Romanian](./translations/ro/README.md) | [Russian](./translations/ru/README.md) | [Serbian (Cyrillic)](./translations/sr/README.md) | [Slovak](./translations/sk/README.md) | [Slovenian](./translations/sl/README.md) | [Spanish](./translations/es/README.md) | [Swahili](./translations/sw/README.md) | [Swedish](./translations/sv/README.md) | [Tagalog (Filipino)](./translations/tl/README.md) | [Tamil](./translations/ta/README.md) | [Telugu](./translations/te/README.md) | [Thai](./translations/th/README.md) | [Turkish](./translations/tr/README.md) | [Ukrainian](./translations/uk/README.md) | [Urdu](./translations/ur/README.md) | [Vietnamese](./translations/vi/README.md)

> **Prefer to Clone Locally?**
>
> This repository may include many language translations over time, which can significantly increase the download size. To clone without translations, use sparse checkout:
>
> **Bash / macOS / Linux:**
>
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
>
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> This gives you the main articles with a faster download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->
