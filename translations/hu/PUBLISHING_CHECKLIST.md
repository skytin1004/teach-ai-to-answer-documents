# Kiadási ellenőrzőlista

Használja ezt az ellenőrzőlistát a közérthető frissítések elkötelezése vagy feltöltése előtt.

## Biztonság

- Győződjön meg arról, hogy nincs API kulcs, token, jelszó vagy privát végpont beírva Markdown fájlokba, jegyzetfüzetekbe, mintaadatokba vagy szkriptekbe.
- A hitelesítő adatokat tartsa környezeti változókban vagy kezelt identitásban, ne elkötelezett fájlokban.
- Ne kötelezze el a `.env` fájlokat vagy futtatott jegyzetfüzet kimeneti fájlokat.
- A `.env.example` fájl legyen csak helyőrző.

## Ellenőrzés

Futtassa a tároló ellenőrző szkriptjét:

```powershell
python scripts\verify_notebooks.py
```

Futtassa a teljes helyi, biztonságos jegyzetfüzet-végrehajtást implementációs változtatások közzététele előtt:

```powershell
python scripts\verify_notebooks.py --execute
```

Elvárt ellenőrzések:

- helyi Markdown linkek érvényesek
- jegyzetfüzet JSON érvényesség átmegy
- a jegyzetfüzetek nem tartalmaznak mentett kimeneteket vagy végrehajtási számlálókat
- magas kockázatú titokminta vizsgálat átmegy
- nyilvános jegyzetfüzetek helyben futtathatók
- a `drafts/` alkönyvtár alatti vázlat anyagok szándékosan ki vannak hagyva

## Áttekintés

- Győződjön meg róla, hogy a README cikk linkjei a szándékolt fájlokra mutatnak.
- Ellenőrizze, hogy minden cikk tartalmaz-e tároló navigációt és kapcsolódó jegyzetfüzet linkeket.
- Győződjön meg arról, hogy a vázlatok nincsenek linkelve a nyilvános indexekből, hacsak nem készek közzétételre.
- Ellenőrizze, hogy a GitHub issue és pull request sablonok még mindig megfelelnek a tároló munkafolyamatának.
- Ellenőrizze, hogy az ellenőrzés eredményei a cikkben megfelelnek a legfrissebb jegyzetfüzet kimenetnek.
- Győződjön meg róla, hogy a GitHub Actions munkafolyamat a push után futni fog.
- Ellenőrizze, hogy a `CHANGELOG.md` tükrözi a közzétett frissítést.
- Ellenőrizze, hogy a `CONTRIBUTING.md` továbbra is megfelel a tároló munkafolyamatának.

## Git

- Tekintse át a `git status --short --branch` kimenetet.
- Tekintse át a `git diff --stat` kimenetet.
- Csak akkor kötelezze el és töltse fel, ha kifejezetten készen áll rá.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->