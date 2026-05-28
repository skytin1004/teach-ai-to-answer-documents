# Közreműködés

Ez a tároló egy blog sorozatból és futtatható jegyzetfüzet példákból áll.

## Mielőtt Pull Requestet nyitsz

Futtasd a helyi validációs szkriptet:

```powershell
python scripts\verify_notebooks.py
```

Implementáció vagy jegyzetfüzet változtatások esetén futtasd a helyi biztonságos jegyzetfüzet végrehajtást:

```powershell
python scripts\verify_notebooks.py --execute
```

## Jegyzetfüzet irányelvek

- Tartsd a jegyzetfüzeteket olvashatónak és az adott cikkhez kapcsolódónak.
- Ne kötelezz el mentett jegyzetfüzet eredményeket vagy végrehajtási számlálókat.
- Használj kis mintaadatokat a `sample_data/` mappából, kivéve ha a cikk egy adott külső erőforrást igényel.
- Rögzítsd a hitelesítési eredményeket a kapcsolódó cikkben, ha a viselkedés változik.

## Titkok és hitelesítési adatok

- Ne kötelezz el API kulcsokat, tokeneket, jelszavakat, privát végpontokat vagy `.env` fájlokat.
- Csak a `.env.example` fájlt használd helyőrző értékekhez.
- Használj környezeti változókat az opcionális helyi Ollama kísérletekhez.

## Dokumentáció

- Tartsd naprakészen a cikk navigációs linkeket.
- Frissítsd a `README.md` fájlt új cikk, jegyzetfüzet, függőségi fájl vagy mintaadat fájl hozzáadásakor.
- Frissítsd a `CHANGELOG.md` fájlt a látható tároló frissítés kiadása előtt.

## Hitelesítés

A GitHub Actions munkafolyamat futtatja:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

A `drafts/` alatt lévő vázlat anyagokat a tároló hitelesítése átugorja, amíg készen nem állnak a nyilvános indexelésre.

## Hibák

A cikk javításokhoz használd a cikk visszajelzési sablonját, a jegyzetfüzet futtatási problémákhoz pedig a jegyzetfüzet hibabejelentő sablonját.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->