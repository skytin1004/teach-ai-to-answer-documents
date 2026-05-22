# Contributing

Dis repository dey organized as blog series plus runnable notebook examples.

## Before Opening a Pull Request

Run di local validation script:

```powershell
python scripts\verify_notebooks.py
```

For implementation or notebook changes, run di local-safe notebook execution:

```powershell
python scripts\verify_notebooks.py --execute
```

## Notebook Guidelines

- Make sure say di notebooks dey readable and e focus on di related article.
- No dey commit saved notebook outputs or execution counts.
- Use small sample data from `sample_data/` unless di article require specific external resource.
- Record verification results for di related article if behavior don change.

## Secrets and Credentials

- No dey commit API keys, tokens, passwords, private endpoints, or `.env` files.
- Use `.env.example` only for placeholder values.
- Use environment variables for optional local Ollama experiments.

## Documentation

- Keep article navigation links updated.
- Update `README.md` when you add new article, notebook, requirements file, or sample data file.
- Update `CHANGELOG.md` before you publish visible repository update.

## Verification

Di GitHub Actions workflow dey run:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Draft material under `drafts/` no dey included for repository verification until e ready for public indexing.

## Issues

Use di article feedback template for article corrections and di notebook issue template for notebook execution problems.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->