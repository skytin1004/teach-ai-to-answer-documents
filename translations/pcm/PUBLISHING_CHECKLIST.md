# Publishing Checklist

Use dis checklist before you commit or push public updates.

## Safety

- Make sure say no API keys, tokens, passwords, or private endpoints dey write for Markdown files, notebooks, sample data, or scripts.
- Keep credentials for environment variables or managed identity, no for committed files.
- No commit `.env` files or executed notebook output files.
- Keep `.env.example` na placeholder only.

## Verification

Run the repository verification script:

```powershell
python scripts\verify_notebooks.py
```

Run the full local-safe notebook execution before you publish implementation changes:

```powershell
python scripts\verify_notebooks.py --execute
```

Expected checks:

- local Markdown links go pass
- notebook JSON validation go pass
- notebooks no get saved outputs or execution counts
- high-risk secret pattern scan go pass
- public notebooks dey execute locally
- draft material under `drafts/` na intentional skip

## Review

- Make sure README article links dey point to the correct files.
- Make sure each article get repository navigation and related notebook links.
- Make sure drafts no dey linked from public indexes unless dem ready to publish.
- Make sure GitHub issue and pull request templates still match the repository workflow.
- Make sure verification results for the article match the latest notebook output.
- Make sure GitHub Actions workflow dey expected to run after push.
- Make sure `CHANGELOG.md` dey reflect the update wey you dey publish.
- Make sure `CONTRIBUTING.md` still dey match the repository workflow.

## Git

- Review `git status --short --branch`.
- Review `git diff --stat`.
- Commit and push only when you really ready.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->