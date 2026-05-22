# Skripty

Táto zložka obsahuje skripty na overenie repozitára.

## `verify_notebooks.py`

Overuje lokálne Markdown odkazy, JSON notebooky, čistotu výstupu notebookov a vzory vysoko rizikových tajomstiev:

```powershell
python scripts\verify_notebooks.py
```

Spúšťa všetky verejné bezpečné lokálne notebooky:

```powershell
python scripts\verify_notebooks.py --execute
```

Workflow GitHub Actions používa ten istý skript.

Návrhový materiál v `drafts/` je preskočený, kým nie je pripravený pre verejný index.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->