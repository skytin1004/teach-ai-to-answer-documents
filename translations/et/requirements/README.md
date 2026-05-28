# Nõuded

Igal rakendusartiklil on konkreetne nõuete fail.

| Fail | Kasutab |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Seeria 2 avatud lähtekoodiga RAG märkmik, sealhulgas valikulised Ollama genereerimise abivahendid |
| [all.txt](../../../requirements/all.txt) | Hoidla taseme kontroll ja CI |

Käivita ühe märkmiku puhul konkreetne fail. Kasuta `all.txt`, kui valideerid kogu hoidlat.

`open-source-rag.txt` ja `all.txt` sisaldavad `fastembed` lokaalsete sisendite jaoks ja `python-dotenv`, et Seeria 2 saaks valikuliselt võimaldada Ollama genereerimist `.env` failist ilma otsingupipeline'i muutmata.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->