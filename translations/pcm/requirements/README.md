# Requirements

Each implementation article get one focused requirements file.

| File | Used by |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Series 2 open-source RAG notebook, including optional Ollama generation helpers |
| [all.txt](../../../requirements/all.txt) | Repository-level verification and CI |

Use di focused file when you dey run one notebook. Use `all.txt` wen you wan check di whole repository.

`open-source-rag.txt` and `all.txt` get `fastembed` for local embeddings and `python-dotenv` so Series 2 fit optionally enable Ollama generation from `.env` without changing di retrieval pipeline.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->