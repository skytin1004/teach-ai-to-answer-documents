# Scripts

This folder contains repository verification scripts.

## `verify_notebooks.py`

Validates local Markdown links, notebook JSON, notebook output cleanliness, and high-risk secret patterns:

```powershell
python scripts\verify_notebooks.py
```

Executes all public local-safe notebooks:

```powershell
python scripts\verify_notebooks.py --execute
```

The GitHub Actions workflow uses the same script.

Draft material under `drafts/` is skipped until it is ready for the public index.
