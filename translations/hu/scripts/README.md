# Scripts

Ez a mappa a tároló ellenőrző szkriptjeit tartalmazza.

## `verify_notebooks.py`

Érvényesíti a helyi Markdown hivatkozásokat, a jegyzetfüzet JSON-ját, a jegyzetfüzet kimenetének tisztaságát és a nagy kockázatú titkos mintákat:

```powershell
python scripts\verify_notebooks.py
```

Futtatja az összes nyilvános helyi biztonságos jegyzetfüzetet:

```powershell
python scripts\verify_notebooks.py --execute
```

A GitHub Actions munkafolyamat ugyanazt a szkriptet használja.

A `drafts/` alatt található vázlat anyagokat kihagyja, amíg nem készen állnak a nyilvános index számára.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->