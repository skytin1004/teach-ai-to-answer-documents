# Scripts

See kaust sisaldab hoidla kontrollskripte.

## `verify_notebooks.py`

Kontrollib kohalikke Markdowni linke, märkmiku JSON-i, märkmiku väljundi puhtust ja kõrge riskiga saladusmustreid:

```powershell
python scripts\verify_notebooks.py
```

Käivitab kõik avalikud kohalikud-turvalised märkmikud:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions töövoog kasutab sama skripti.

Eelnõu materjali kaustas `drafts/` vahele jäetakse kuni see on avaliku indeksi jaoks valmis.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->