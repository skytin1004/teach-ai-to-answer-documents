# Märkmikud

Need märkmikud toetavad artiklisarja käivitatavate näidetega.

| Märkmik | Artikkel | Eesmärk |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Seeria 2](../articles/series-2-open-source-rag-end-to-end.md) | Avatud lähtekoodiga RAG FastEmbedi, Qdranti lokaalses režiimis, päringu, ümberjärjestamise, valikulise Ollama genereerimise ja allikaviidetega |

## Käivita lokaalselt

Paigalda nõuded märkmikule, mida soovid käivitada:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Või paigalda kõik sõltuvused:

```powershell
python -m pip install -r requirements\all.txt
```

## Kontrolli

Hoonejuurest:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Seeria 2 võib lugeda Ollama konfiguratsiooni hoidla juurest `.env` failist. Alusta failist [../.env.example](../../../.env.example), mis on grupeeritud sarja järgi.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->