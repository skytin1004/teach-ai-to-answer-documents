# Bilježnice

Ove bilježnice podržavaju seriju članaka s primjerima koje je moguće pokrenuti.

| Bilježnica | Članak | Svrha |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serija 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG s FastEmbed, Qdrant lokalnim načinom rada, dohvaćanjem, ponovnim rangiranjem, opcijskom Ollama generacijom i izvorima referenci |

## Pokreni lokalno

Instalirajte zahtjeve za bilježnicu koju želite pokrenuti:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ili instalirajte sve ovisnosti:

```powershell
python -m pip install -r requirements\all.txt
```

## Potvrdi

Iz korijena repozitorija:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serija 2 može čitati Ollama konfiguraciju iz `.env` datoteke u korijenu repozitorija. Počnite od [../.env.example](../../../.env.example), koja je grupirana po serijama.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->