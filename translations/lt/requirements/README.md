# Reikalavimai

Kiekvienas įgyvendinimo straipsnis turi susikoncentravusį reikalavimų failą.

| Failas | Naudojamas |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Serija 2 atviro kodo RAG užrašų knygelė, įskaitant pasirenkamus Ollama generavimo pagalbininkus |
| [all.txt](../../../requirements/all.txt) | Saugyklos lygmens tikrinimas ir CI |

Naudokite susikoncentravusį failą paleisdami vieną užrašų knygelę. Naudokite `all.txt`, kai tikrinate visą saugyklą.

`open-source-rag.txt` ir `all.txt` įtraukia `fastembed` vietiniams įterpimams ir `python-dotenv`, kad Serija 2 galėtų pasirenkamai įgalinti Ollama generavimą iš `.env` nekeisdama sugriebimo grandinės.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->