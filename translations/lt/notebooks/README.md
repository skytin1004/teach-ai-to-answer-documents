# Sąsiuviniai

Šie sąsiuviniai palaiko straipsnių seriją su vykdomais pavyzdžiais.

| Sąsiuvinis | Straipsnis | Paskirtis |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serija 2](../articles/series-2-open-source-rag-end-to-end.md) | Atviro kodo RAG su FastEmbed, Qdrant vietiniu režimu, paieška, perrikiavimu, pasirinktinai Ollama generavimu ir šaltinių nuorodomis |

## Vykdyti vietoje

Įdiekite priklausomybes sąsiuviniui, kurį norite paleisti:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Arba įdiekite visas priklausomybes:

```powershell
python -m pip install -r requirements\all.txt
```

## Patikrinkite

Iš saugyklos šaknies:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serija 2 gali skaityti Ollama konfigūraciją iš saugyklos šaknies `.env` failo. Pradėkite nuo [../.env.example](../../../.env.example), kuris yra sugrupuotas pagal serijas.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->