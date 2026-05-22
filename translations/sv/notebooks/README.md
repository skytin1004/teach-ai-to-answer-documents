# Anteckningsböcker

Dessa anteckningsböcker stödjer artikelserien med körbara exempel.

| Anteckningsbok | Artikel | Syfte |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serie 2](../articles/series-2-open-source-rag-end-to-end.md) | Öppen källkods RAG med FastEmbed, Qdrant lokal läge, hämtning, omrankning, valfri Ollama-generering och källa-referenser |

## Kör lokalt

Installera kraven för anteckningsboken du vill köra:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Eller installera alla beroenden:

```powershell
python -m pip install -r requirements\all.txt
```

## Verifiera

Från repository-roten:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serie 2 kan läsa Ollama-konfiguration från en repository-rot `.env` fil. Börja från [../.env.example](../../../.env.example), som är grupperad per serie.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->