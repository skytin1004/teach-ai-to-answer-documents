# Panustamine

See hoidla on organiseeritud blogiseeria ja käivitatavate märkmiku näidete kujul.

## Enne Pull Requesti avamist

Käivita kohalik valideerimisskript:

```powershell
python scripts\verify_notebooks.py
```

Rakenduse või märkmiku muudatuste puhul käivita kohalik ohutu märkmiku täideviimine:

```powershell
python scripts\verify_notebooks.py --execute
```

## Märkmike suunised

- Hoia märkmikud loetavad ja seotud artiklile keskendunud.
- Ära kinnita salvestatud märkmiku väljundeid ega täitmise loendeid.
- Kasuta väikseid näitedatafaile kaustast `sample_data/`, välja arvatud juhul, kui artikkel nõuab konkreetset välist ressursi.
- Käsitle kinnitustulemusi seotud artiklis, kui käitumine muutub.

## Saladused ja volitused

- Ära kinnita API võtmeid, märke, paroole, privaatseid lõpp-punkte ega `.env` faile.
- Kasuta ainult `.env.example` kohatäidetena.
- Kasuta keskkonnamuutujaid valikuliste kohalike Ollama katsete jaoks.

## Dokumentatsioon

- Hoia artikli navigeerimislingid ajakohased.
- Uuenda `README.md`, kui lisad uue artikli, märkmiku, nõuete faili või näitedataa faili.
- Uuenda `CHANGELOG.md` enne nähtava hoidla uuenduse avaldamist.

## Kinnitamine

GitHub Actions töövoog käivitatakse:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Mustandmaterjal kaustas `drafts/` jäetakse hoidla kinnitamisel kõrvale, kuni see on avalikuks indekseerimiseks valmis.

## Tõrked

Kasuta artikli tagasiside malli artikli paranduste jaoks ja märkmiku tõrke malli märkmiku täitmise probleemide jaoks.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->