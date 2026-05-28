# Publikavimo kontrolinis sąrašas

Prieš įsipareigodami ar siųsdami viešus atnaujinimus, naudokite šį kontrolinį sąrašą.

## Saugumas

- Patikrinkite, ar nėra API raktų, žetonų, slaptažodžių ar privačių galinių taškų įrašytų į Markdown failus, užrašų knygeles, pavyzdinius duomenis ar scenarijus.
- Kredencialus laikykite aplinkos kintamuosiuose arba valdomos tapatybės srityje, o ne įsipareigotose bylose.
- Neišsipareigokite `.env` failų ar vykdytų užrašų knygelių išeigos failų.
- `.env.example` laikykite tik kaip rezervinio šablono failą.

## Patikra

Paleiskite saugumo patikros skriptą saugykloje:

```powershell
python scripts\verify_notebooks.py
```

Prieš publikuodami implementacijos pakeitimus, pilnai ir saugiai vietoje vykdykite užrašų knygeles:

```powershell
python scripts\verify_notebooks.py --execute
```

Laukiami patikrinimai:

- praėjo vietiniai Markdown nuorodų testai
- praėjo užrašų knygelių JSON validacija
- užrašų knygelėse nėra išsaugotų išeigos ar vykdymo skaičių
- praėjo aukštos rizikos slaptų duomenų paieška
- viešos užrašų knygelės vykdomos vietoje
- medžiaga po `drafts/` sąmoningai praleidžiama

## Peržiūra

- Patikrinkite, ar README straipsnių nuorodos rodo į numatytus failus.
- Patikrinkite, ar kiekviename straipsnyje yra nuorodos į saugyklos navigaciją ir susijusias užrašų knygeles.
- Patikrinkite, ar juodraščiai nėra susieti iš viešų indeksų, nebent jie paruošti publikuoti.
- Patikrinkite, ar GitHub problemų ir pull request šablonai atitinka saugyklos darbų eigą.
- Patikrinkite, ar straipsnyje pateikti patikros rezultatai atitinka naujausią užrašų knygelės išeigą.
- Patikrinkite, ar po įkėlimo turėtų veikti GitHub Actions darbų eiga.
- Patikrinkite, ar `CHANGELOG.md` atspindi skelbiamą atnaujinimą.
- Patikrinkite, ar `CONTRIBUTING.md` vis dar atitinka saugyklos darbų eigą.

## Git

- Peržiūrėkite `git status --short --branch`.
- Peržiūrėkite `git diff --stat`.
- Įsipareigokite ir siųskite tik tada, kai esate aiškiai pasirengę.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->