# Požiadavky

Každý článok o implementácii má súbor zameraných požiadaviek.

| Súbor | Používa |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Série 2 open-source RAG notebook, vrátane voliteľných pomocníkov na generovanie Ollama |
| [all.txt](../../../requirements/all.txt) | Overenie na úrovni repozitára a CI |

Použite zameraný súbor pri spustení jedného notebooku. Použite `all.txt` pri overovaní celého repozitára.

`open-source-rag.txt` a `all.txt` obsahujú `fastembed` pre lokálne embedovania a `python-dotenv`, takže Série 2 môže voliteľne povoliť generovanie Ollama zo súboru `.env` bez zmeny pipeline pre získavanie.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->