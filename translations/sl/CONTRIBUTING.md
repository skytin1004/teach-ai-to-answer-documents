# Prispevanje

Ta repozitorij je organiziran kot serija blogov in izvedljivi primeri zvezkov.

## Pred odpiranjem Pull Requesta

Zaženite lokalni skript za preverjanje:

```powershell
python scripts\verify_notebooks.py
```

Za spremembe implementacije ali zvezkov zaženite lokalno varno izvajanje zvezka:

```powershell
python scripts\verify_notebooks.py --execute
```

## Smernice za zvezke

- Ohranjajte zvezke berljive in osredotočene na sorodni članek.
- Ne komitirajte shranjenih izhodov zvezkov ali štetja izvedb.
- Uporabljajte majhne vzorčne podatke iz `sample_data/`, razen če članek zahteva poseben zunanji vir.
- Rezultate preverjanja zabeležite v sorodnem članku, kadar se vedenje spremeni.

## Gesla in poverilnice

- Ne komitirajte API ključev, žetonov, gesel, zasebnih končnih točk ali datotek `.env`.
- Datoteko `.env.example` uporabljajte le za nadomestne vrednosti.
- Za neobvezne lokalne eksperimente z Ollamo uporabite spremenljivke okolja.

## Dokumentacija

- Posodabljajte povezave za navigacijo v člankih.
- Posodobite `README.md` ob dodajanju novega članka, zvezka, datoteke zahtev ali vzorčnih podatkov.
- Posodobite `CHANGELOG.md` pred objavo vidne posodobitve repozitorija.

## Preverjanje

Workflow GitHub Actions izvaja:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Osnutke pod `drafts/` repozitorijska preverjanja preskočijo, dokler niso pripravljeni za javno indeksiranje.

## Težave

Uporabite predlogo za povratne informacije za popravke člankov in predlogo za težave z zvezki za težave pri izvajanju zvezkov.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->