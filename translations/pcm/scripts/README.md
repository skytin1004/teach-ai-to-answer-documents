# Scripts

Dis folder get repository verification scripts.

## `verify_notebooks.py`

E dey check local Markdown links, notebook JSON, notebook output cleanliness, and high-risk secret patterns:

```powershell
python scripts\verify_notebooks.py
```

E go run all public local-safe notebooks:

```powershell
python scripts\verify_notebooks.py --execute
```

The GitHub Actions workflow dey use the same script.

Draft material wey dey under `drafts/` no dey run until e don ready for the public index.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->