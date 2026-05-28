# Kontrolní seznam pro publikování

Použijte tento seznam před tím, než provedete commit nebo push veřejných aktualizací.

## Bezpečnost

- Potvrďte, že v Markdown souborech, poznámkových blozcích, ukázkových datech nebo skriptech nejsou zapsány žádné API klíče, tokeny, hesla nebo soukromé koncové body.
- Ukládejte přihlašovací údaje do proměnných prostředí nebo spravované identity, ne do commitovaných souborů.
- Necommittujte `.env` soubory ani výstupy spuštěných poznámkových bloků.
- Soubor `.env.example` nechte pouze s ukázkovými hodnotami.

## Ověření

Spusťte skript pro ověření repozitáře:

```powershell
python scripts\verify_notebooks.py
```

Před publikací změn implementace proveďte kompletní bezpečné lokální spuštění poznámkového bloku:

```powershell
python scripts\verify_notebooks.py --execute
```

Očekávané kontroly:

- lokální odkazy v Markdown projdou
- validace JSON poznámkových bloků projde
- poznámkové bloky neobsahují uložené výstupy ani počty spuštění
- kontrola vzorů vysoce rizikových tajných údajů projde
- veřejné poznámkové bloky se spustí lokálně
- návrhy pod `drafts/` jsou úmyslně vynechány

## Revize

- Potvrďte, že odkazy v článku README vedou na zamýšlené soubory.
- Potvrďte, že každý článek má navigaci v repozitáři a odkazy na související poznámkové bloky.
- Potvrďte, že návrhy nejsou odkazovány z veřejných indexů, pokud nejsou připraveny k publikaci.
- Potvrďte, že šablony GitHub issue a pull request stále odpovídají workflow repozitáře.
- Potvrďte, že výsledky ověření v článku odpovídají nejnovějšímu výstupu poznámkového bloku.
- Potvrďte, že GitHub Actions workflow se očekává po pushi.
- Potvrďte, že `CHANGELOG.md` odráží právě publikovanou aktualizaci.
- Potvrďte, že `CONTRIBUTING.md` stále odpovídá workflow repozitáře.

## Git

- Prohlédněte si `git status --short --branch`.
- Prohlédněte si `git diff --stat`.
- Commitujte a pushujte pouze tehdy, když jste explicitně připraveni.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->