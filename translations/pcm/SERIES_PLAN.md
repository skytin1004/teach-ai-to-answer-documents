# Teach AI to Answer Questions Based on Your Documents - Series Plan

Dis plan dey track the public Series 1 and Series 2 release. Later Azure and evaluation work dey kept as drafts until the examples don complete end-to-end and verified.

No make you commit or push changes until person talk make you do am.

## Public Scope

Current public release:

- Series 1 article: RAG architecture decisions, Azure vs open-source tradeoffs, and where fine-tuning fit.
- Series 2 article: local open-source RAG tutorial.
- Series 2 notebook: runnable local RAG lab with FastEmbed, Qdrant, Ollama, and Phi-4-mini.
- Sample data: school policy and course AI guidance Markdown files.

Drafted but no dey public index yet:

- Azure AI Search and Azure OpenAI rebuild.
- RAG evaluation and regression checks.

## Tutorial Scenario

The shared scenario na school policy assistant.

The assistant go answer dis question from local documents:

```text
Can I use generative AI for my final assignment?
```

The expected behaviour na:

1. Load local Markdown documents.
2. Parse and chunk dem by headings.
3. Create local embeddings and store searchable representations with metadata.
4. Retrieve the relevant policy section.
5. Rerank when e need.
6. Generate or compose grounded answer.
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

Draft material dey under `drafts/` and dem no dey check am for repository verification until e ready for public indexing.

## Series 2 Verification

Verified on Windows with Python 3.12.6.

- Installed `requirements/open-source-rag.txt` successful.
- Run `notebooks/series-2-open-source-rag.ipynb` with `nbclient`.
- Local verification pass: 2 sample documents loaded, 8 chunks created, FastEmbed generate 384-dimension local embeddings, Qdrant in-memory collection initialize, and 8 vectors insert.
- Test question: "Can I use generative AI for my final assignment?"
- Top retrieved source after lightweight reranking: `school_ai_policy.md`.
- Top retrieved section after lightweight reranking: `Final Assignments`.
- Default answer path: local transparent answer composer.
- Ollama install through winget; `phi4-mini:3.8b` pull successful.
- Ollama answer-generation path: complete with `phi4-mini:3.8b`.
- Ollama model file size: about 2.49GB for disk.
- Ollama loaded model size: 3.3GB reported by `ollama ps`.
- GPU offload: 100% GPU reported by `ollama ps` on RTX 3060 Laptop GPU.
- GPU memory wey dem observe after generation: about 3.5GB of 6GB.
- Notebook run with cached FastEmbed model and Ollama generation enabled pass in about 34 seconds through the verification script.
- Observation: early document-loading pass accidentally include `sample_data/README.md`; the notebook now load only the two intended sample documents explicitly.

## Repository Verification

- `scripts/verify_notebooks.py` validate local Markdown links, notebook JSON, notebook output cleanliness, and high-risk secret patterns.
- `scripts/verify_notebooks.py --execute` run public notebooks from the repository root.
- Draft material under `drafts/` dey intentionally skip.

## Next Work

- Rebuild the same scenario with Azure AI Search and Azure OpenAI as future series part.
- Add retrieval and answer evaluation once local and Azure implementations dey stable.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->