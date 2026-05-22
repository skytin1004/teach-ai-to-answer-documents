# Kontrolni seznam za objavo

Uporabite ta kontrolni seznam pred potrditvijo ali potiskom javnih posodobitev.

## Varnost

- Potrdite, da v Markdown datotekah, zvezkih, vzorčnih podatkih ali skriptah niso zapisani nobeni API ključi, žetoni, gesla ali zasebni končni točki.
- Shranjujte poverilnice v spremenljivkah okolja ali upravljani identiteti, ne v potrjenih datotekah.
- Ne potrjujte `.env` datotek ali izvedenih izhodnih datotek zvezkov.
- Naj bo `.env.example` samo z mesta za vnos.

## Preverjanje

Zaženite skripto za preverjanje repozitorija:

```powershell
python scripts\verify_notebooks.py
```

Pred objavo sprememb implementacije zaženite popolno lokalno varno izvajanje zvezka:

```powershell
python scripts\verify_notebooks.py --execute
```

Pričakovane kontrole:

- lokalne Markdown povezave so uspešne
- veljavnost JSON zvezkov je potrjena
- zvezki ne vsebujejo shranjenih izhodov ali štetij izvajanja
- skeniranje vzorcev visoko tveganih skrivnosti je uspešno
- javni zvezki se izvajajo lokalno
- material v mapi `drafts/` je namerno preskočen

## Pregled

- Potrdite, da povezave v člankih README kažejo na ustrezne datoteke.
- Potrdite, da ima vsak članek navigacijo po repozitoriju in povezave do sorodnih zvezkov.
- Potrdite, da osnutki niso povezani z javnih indeksov, razen če so pripravljeni za objavo.
- Potrdite, da predloge za GitHub issue in pull request še vedno ustrezajo delovnemu toku repozitorija.
- Potrdite, da rezultati preverjanja v članku sovpadajo z najnovejšim izhodom zvezka.
- Potrdite, da se poteza GitHub Actions pričakuje po pritisku.
- Potrdite, da `CHANGELOG.md` odraža objavljeno posodobitev.
- Potrdite, da `CONTRIBUTING.md` še vedno ustreza delovnemu toku repozitorija.

## Git

- Preglejte `git status --short --branch`.
- Preglejte `git diff --stat`.
- Potrdite in pošljite le, ko ste izrecno pripravljeni.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->