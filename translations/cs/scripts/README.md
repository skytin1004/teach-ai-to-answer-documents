# Skripty

Tato složka obsahuje skripty pro ověření repozitáře.

## `verify_notebooks.py`

Ověřuje místní odkazy v Markdownu, JSON notebooků, čistotu výstupů notebooků a vzory vysoce rizikových tajných údajů:

```powershell
python scripts\verify_notebooks.py
```

Spouští všechny veřejné místně bezpečné notebooky:

```powershell
python scripts\verify_notebooks.py --execute
```

Pracovní postup GitHub Actions používá stejný skript.

Konceptový materiál ve `drafts/` je přeskočen, dokud není připraven pro veřejný index.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->