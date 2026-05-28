# Scripts

Šiame aplanke yra saugyklos patikros scenarijai.

## `verify_notebooks.py`

Patikrinti vietinius Markdown nuorodas, užrašų knygelių JSON, užrašų išvesties švarumą ir didelės rizikos slaptųjų modelių šablonus:

```powershell
python scripts\verify_notebooks.py
```

Vykdo visas viešas vietinėms saugioms užrašų knygelėms:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions darbotvarkė naudoja tą patį scenarijų.

Juodraščių medžiaga, esanti `drafts/`, yra praleidžiama, kol nėra paruošta viešajam indeksui.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->