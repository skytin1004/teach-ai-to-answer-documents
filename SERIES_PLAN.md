# Teach AI to Answer Questions Based on Your Documents - Series Plan

This plan tracks the public Series 1 and Series 2 release. Later Azure and evaluation work is being kept as drafts until the examples are fully end-to-end and verified.

Do not commit or push changes until explicitly instructed.

## Public Scope

Current public release:

- Series 1 article: RAG architecture decisions, Azure vs open-source tradeoffs, and where fine-tuning fits.
- Series 2 article: local open-source RAG tutorial.
- Series 2 notebook: runnable local RAG lab with FastEmbed, Qdrant, Ollama, and Phi-4-mini.
- Sample data: school policy and course AI guidance Markdown files.

Drafted but not in the public index yet:

- Azure AI Search and Azure OpenAI rebuild.
- RAG evaluation and regression checks.

## Tutorial Scenario

The shared scenario is a school policy assistant.

The assistant answers this question from local documents:

```text
Can I use generative AI for my final assignment?
```

The expected behavior is:

1. Load local Markdown documents.
2. Parse and chunk them by headings.
3. Create local embeddings and store searchable representations with metadata.
4. Retrieve the relevant policy section.
5. Rerank when needed.
6. Generate or compose a grounded answer.
7. Return citations.
8. Record verification results.

## Current Public Structure

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

Draft material is stored under `drafts/` and is skipped by repository verification until it is ready for public indexing.

## Series 2 Verification

Verified on Windows with Python 3.12.6.

- Installed `requirements/open-source-rag.txt` successfully.
- Executed `notebooks/series-2-open-source-rag.ipynb` with `nbclient`.
- Local verification passed: 2 sample documents loaded, 8 chunks created, FastEmbed generated 384-dimension local embeddings, Qdrant in-memory collection initialized, and 8 vectors inserted.
- Test question: "Can I use generative AI for my final assignment?"
- Top retrieved source after lightweight reranking: `school_ai_policy.md`.
- Top retrieved section after lightweight reranking: `Final Assignments`.
- Default answer path: local transparent answer composer.
- Ollama installed through winget; `phi4-mini:3.8b` pulled successfully.
- Ollama answer-generation path: completed with `phi4-mini:3.8b`.
- Ollama model file size: about 2.49GB on disk.
- Ollama loaded model size: 3.3GB reported by `ollama ps`.
- GPU offload: 100% GPU reported by `ollama ps` on RTX 3060 Laptop GPU.
- GPU memory observed after generation: about 3.5GB of 6GB.
- Notebook execution with cached FastEmbed model and Ollama generation enabled passed in about 34 seconds through the verification script.
- Observation: an early document-loading pass accidentally included `sample_data/README.md`; the notebook now loads only the two intended sample documents explicitly.

## Repository Verification

- `scripts/verify_notebooks.py` validates local Markdown links, notebook JSON, notebook output cleanliness, and high-risk secret patterns.
- `scripts/verify_notebooks.py --execute` runs public notebooks from the repository root.
- Draft material under `drafts/` is intentionally skipped.

## Next Work

- Rebuild the same scenario with Azure AI Search and Azure OpenAI as a future series part.
- Add retrieval and answer evaluation once the local and Azure implementations are both stable.
