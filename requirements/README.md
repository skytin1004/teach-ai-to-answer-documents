# Requirements

Each implementation article has a focused requirements file.

| File | Used by |
| --- | --- |
| [open-source-rag.txt](./open-source-rag.txt) | Series 2 open-source RAG notebook, including optional Ollama generation helpers |
| [all.txt](./all.txt) | Repository-level verification and CI |

Use the focused file when running one notebook. Use `all.txt` when validating the whole repository.

`open-source-rag.txt` and `all.txt` include `fastembed` for local embeddings and `python-dotenv` so Series 2 can optionally enable Ollama generation from `.env` without changing the retrieval pipeline.
