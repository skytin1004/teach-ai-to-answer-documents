# Publishing Checklist

Use this checklist before committing or pushing public updates.

## Safety

- Confirm no API keys, tokens, passwords, or private endpoints are written into Markdown files, notebooks, sample data, or scripts.
- Keep credentials in environment variables or managed identity, not in committed files.
- Do not commit `.env` files or executed notebook output files.
- Keep `.env.example` placeholder-only.

## Verification

Run the repository verification script:

```powershell
python scripts\verify_notebooks.py
```

Run the full local-safe notebook execution before publishing implementation changes:

```powershell
python scripts\verify_notebooks.py --execute
```

Expected checks:

- local Markdown links pass
- notebook JSON validation passes
- notebooks do not contain saved outputs or execution counts
- high-risk secret pattern scan passes
- public notebooks execute locally
- draft material under `drafts/` is intentionally skipped

## Review

- Confirm README article links point to the intended files.
- Confirm each article has repository navigation and related notebook links.
- Confirm drafts are not linked from public indexes unless they are ready to publish.
- Confirm GitHub issue and pull request templates still match the repository workflow.
- Confirm verification results in the article match the latest notebook output.
- Confirm GitHub Actions workflow is expected to run after push.
- Confirm `CHANGELOG.md` reflects the update being published.
- Confirm `CONTRIBUTING.md` still matches the repository workflow.

## Git

- Review `git status --short --branch`.
- Review `git diff --stat`.
- Commit and push only when explicitly ready.
