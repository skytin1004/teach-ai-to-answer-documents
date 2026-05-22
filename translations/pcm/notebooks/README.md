# Notebooks

Dem notebooks dey support di article series wit runnable examples.

| Notebook | Article | Purpose |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG wit FastEmbed, Qdrant local mode, retrieval, reranking, optional Ollama generation, an source references |

## Run Locally

Install di requirements for di notebook wey you want run:

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

From di repository root:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Series 2 fit read Ollama configuration from a repository-root `.env` file. Start from [../.env.example](../../../.env.example), wey dem group by series.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->