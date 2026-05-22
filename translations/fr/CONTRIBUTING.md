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
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->