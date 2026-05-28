# Caiete

Aceste caiete susțin seria de articole cu exemple care pot fi rulate.

| Caiet | Articol | Scop |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Seria 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG open-source cu FastEmbed, modul local Qdrant, recuperare, reordonare, generare opțională Ollama și referințe la surse |

## Rulare locală

Instalează cerințele pentru caietul pe care vrei să-l rulezi:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Sau instalează toate dependențele:

```powershell
python -m pip install -r requirements\all.txt
```

## Verificare

Din rădăcina depozitului:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Seria 2 poate citi configurația Ollama dintr-un fișier `.env` aflat în rădăcina depozitului. Pornește de la [../.env.example](../../../.env.example), care este grupat pe serii.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->