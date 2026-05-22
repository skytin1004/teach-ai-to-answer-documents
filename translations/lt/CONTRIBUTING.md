# Prisidėjimas

Šis saugykla yra suorganizuota kaip tinklaraščio serija su vykdomais užrašų pavyzdžiais.

## Prieš atidarant pakeitimų užklausą

Paleiskite vietinį tikrinimo scenarijų:

```powershell
python scripts\verify_notebooks.py
```

Dėl įgyvendinimo ar užrašų pakeitimų paleiskite vietoje saugų užrašų vykdymą:

```powershell
python scripts\verify_notebooks.py --execute
```

## Užrašų gairės

- Laikykite užrašus skaitomus ir orientuotus į susijusį straipsnį.
- Nekomentuokite išsaugotų užrašų rezultatų ar vykdymo skaičių.
- Naudokite mažus pavyzdžių duomenis iš `sample_data/`, jei straipsnis nereikalauja konkretaus išorinio šaltinio.
- Patvirtinimo rezultatus įrašykite į susijusį straipsnį, kai keičiasi elgsena.

## Slapti duomenys ir prisijungimo duomenys

- Nekomentuokite API raktų, žetonų, slaptažodžių, privačių galinių taškų ar `.env` failų.
- Naudokite `.env.example` tik vietoje rezervuotų reikšmių.
- Naudokite aplinkos kintamuosius pasirenkamiems vietiniams Ollama eksperimentams.

## Dokumentacija

- Laikykite straipsnių navigacijos nuorodas atnaujintas.
- Atnaujinkite `README.md`, kai pridedate naują straipsnį, užrašą, priklausomybių failą ar pavyzdinių duomenų failą.
- Atnaujinkite `CHANGELOG.md` prieš skelbdami matomą saugyklos atnaujinimą.

## Patvirtinimas

GitHub Actions darbo eiga vykdoma:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Juodraščių medžiaga aplanke `drafts/` nepaisoma saugyklos patikrų, kol ji nėra paruošta viešam indeksavimui.

## Problemos

Naudokite straipsnių atsiliepimų šabloną straipsnių taisymams ir užrašų problemų šabloną užrašų vykdymo problemoms.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->