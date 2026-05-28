# Avaldamise kontrollnimekiri

Kasuta seda kontrollnimekirja enne avalike muudatuste sooritamist või pushimist.

## Turvalisus

- Kinnita, et Markdown-failidesse, märkmikesse, näidandmetesse või skriptidesse ei ole kirjutatud API-võtmeid, tokeneid, paroole ega privaatseid lõpp-punkte.
- Hoia mandaadid keskkonnamuutujates või hallatud identiteedis, mitte versioonihaldusfailides.
- Ära pane koodi `.env` faile ega jooksutatud märkmiku väljundeid.
- Hoia `.env.example` ainult kohatäitajana.

## Kontroll

Käivita hoidla kontrolliskript:

```powershell
python scripts\verify_notebooks.py
```

Käivita kogu kohalikult ohutu märkmiku täitmine enne muudatuste avaldamist:

```powershell
python scripts\verify_notebooks.py --execute
```

Oodatavad kontrollid:

- kohalikud Markdowni lingid töötavad
- märkmiku JSON valideerimine läbitud
- märkmikud ei sisalda salvestatud väljundeid ega täitmise arve
- kõrge riski salajase mustri skaneerimine läbitud
- avalikud märkmikud täidetakse kohapeal
- mustandmaterjal kaustas `drafts/` on teadlikult vahele jäetud

## Ülevaatus

- Kinnita, et README artiklite lingid viitavad soovitud failidele.
- Kinnita, et igal artiklil on hoidla navigeerimise ja seotud märkmike lingid.
- Kinnita, et mustandid ei ole linkidena avalikes indeksites, välja arvatud kui need on avaldamiseks valmis.
- Kinnita, et GitHubi issue ja pull requesti mallid vastavad endiselt hoidla töövoole.
- Kinnita, et artiklis olevate kontrollide tulemused vastavad viimasele märkmiku väljundile.
- Kinnita, et GitHub Actionsi töövoog ootab käivitumist pärast pushi.
- Kinnita, et `CHANGELOG.md` kajastab avaldatavat värskendust.
- Kinnita, et `CONTRIBUTING.md` vastab endiselt hoidla töövoole.

## Git

- Vaata üle `git status --short --branch`.
- Vaata üle `git diff --stat`.
- Tee commit ja pushi ainult siis, kui oled selgelt valmis.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->