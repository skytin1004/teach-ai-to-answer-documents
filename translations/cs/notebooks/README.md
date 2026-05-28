# Poznámkové bloky

Tyto poznámkové bloky podporují sérii článků s spustitelnými příklady.

| Poznámkový blok | Článek | Účel |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Série 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG s FastEmbed, lokálním režimem Qdrant, vyhledáváním, přeřazením, volitelnou generací Ollama a odkazy na zdroje |

## Spuštění lokálně

Nainstalujte požadavky pro poznámkový blok, který chcete spustit:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Nebo nainstalujte všechny závislosti:

```powershell
python -m pip install -r requirements\all.txt
```

## Ověření

Ze kořenového adresáře repozitáře:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Série 2 může číst konfiguraci Ollama ze souboru `.env` v kořenovém adresáři repozitáře. Začněte ze souboru [../.env.example](../../../.env.example), který je rozčleněný podle sérií.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->