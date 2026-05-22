# Scripts

Denna mapp innehåller skript för verifiering av repository.

## `verify_notebooks.py`

Verifierar lokala Markdown-länkar, notebook JSON, notebook-utdata rengöring och mönster för hög risk av hemligheter:

```powershell
python scripts\verify_notebooks.py
```

Kör alla offentliga lokalt-säkra notebooks:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions-arbetsflödet använder samma skript.

Utkastsmaterial i `drafts/` hoppas över tills det är redo för den offentliga indexen.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->