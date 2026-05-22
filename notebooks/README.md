# Notebooks

These notebooks support the article series with runnable examples.

| Notebook | Article | Purpose |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG with FastEmbed, Qdrant local mode, retrieval, reranking, optional Ollama generation, and source references |

## Run Locally

Install the requirements for the notebook you want to run:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Or install all dependencies:

```powershell
python -m pip install -r requirements\all.txt
```

## Verify

From the repository root:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Series 2 can read Ollama configuration from a repository-root `.env` file. Start from [../.env.example](../.env.example), which is grouped by series.
