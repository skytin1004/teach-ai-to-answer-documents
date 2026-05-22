# Poznámkové bloky

Tieto poznámkové bloky podporujú sériu článkov s spustiteľnými príkladmi.

| Poznámkový blok | Článok | Účel |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Séria 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG s FastEmbed, Qdrant lokálny režim, vyhľadávanie, pretriedenie, voliteľná Ollama generácia a odkazy na zdroje |

## Spustenie lokálne

Nainštalujte požiadavky pre poznámkový blok, ktorý chcete spustiť:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Alebo nainštalujte všetky závislosti:

```powershell
python -m pip install -r requirements\all.txt
```

## Overenie

Z koreňového adresára repozitára:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Séria 2 môže načítať konfiguráciu Ollama zo súboru `.env` v koreňovom adresári repozitára. Začnite od [../.env.example](../../../.env.example), ktorý je rozdelený podľa sérií.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->