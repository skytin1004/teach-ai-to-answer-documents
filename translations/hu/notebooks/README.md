# Jegyzetfüzetek

Ezek a jegyzetfüzetek futtatható példákkal támogatják a cikkek sorozatát.

| Jegyzetfüzet | Cikk | Cél |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [2. sorozat](../articles/series-2-open-source-rag-end-to-end.md) | Nyílt forráskódú RAG FastEmbed-del, Qdrant helyi módban, visszakereséssel, átrendezéssel, opcionális Ollama generálással és forrás hivatkozásokkal |

## Helyi futtatás

Telepítse a kívánt jegyzetfüzet futtatásához szükséges követelményeket:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Vagy telepítsen minden függőséget:

```powershell
python -m pip install -r requirements\all.txt
```

## Ellenőrzés

A tároló gyökérkönyvtárából:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

A 2. sorozat képes az Ollama konfigurációját a tároló gyökérkönyvtárában lévő `.env` fájlból olvasni. Kezdje a [../.env.example](../../../.env.example) fájllal, amely sorozatok szerint van csoportosítva.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->