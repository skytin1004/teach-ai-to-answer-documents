# Contributing

This repository is organized as a blog series plus runnable notebook examples.

## Before Opening a Pull Request

Run the local validation script:

```powershell
python scripts\verify_notebooks.py
```

For implementation or notebook changes, run the local-safe notebook execution:

```powershell
python scripts\verify_notebooks.py --execute
```

## Notebook Guidelines

- Keep notebooks readable and focused on the related article.
- Do not commit saved notebook outputs or execution counts.
- Use small sample data from `sample_data/` unless the article requires a specific external resource.
- Record verification results in the related article when behavior changes.

## Secrets and Credentials

- Do not commit API keys, tokens, passwords, private endpoints, or `.env` files.
- Use `.env.example` only for placeholder values.
- Use environment variables for optional local Ollama experiments.

## Documentation

- Keep article navigation links up to date.
- Update `README.md` when adding a new article, notebook, requirements file, or sample data file.
- Update `CHANGELOG.md` before publishing a visible repository update.

## Verification

The GitHub Actions workflow runs:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Draft material under `drafts/` is skipped by repository verification until it is ready for public indexing.

## Issues

Use the article feedback template for article corrections and the notebook issue template for notebook execution problems.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->