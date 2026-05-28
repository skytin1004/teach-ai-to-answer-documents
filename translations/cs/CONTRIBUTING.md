# Přispívání

Tento repozitář je uspořádán jako série blogových příspěvků plus spustitelné ukázkové notebooky.

## Před otevřením Pull Requestu

Spusťte místní validační skript:

```powershell
python scripts\verify_notebooks.py
```

Pro změny implementace nebo notebooku spusťte lokální bezpečné spuštění notebooku:

```powershell
python scripts\verify_notebooks.py --execute
```

## Pokyny pro notebooky

- Udržujte notebooky čitelné a zaměřené na související článek.
- Nekomitujte uložené výstupy notebooku ani počty spuštění.
- Používejte malá ukázková data z `sample_data/`, pokud článek nevyžaduje konkrétní externí zdroj.
- Zaznamenejte výsledky ověření v souvisejícím článku, pokud se chování změní.

## Tajemství a přihlašovací údaje

- Nekomitujte API klíče, tokeny, hesla, soukromé koncové body ani `.env` soubory.
- Používejte `.env.example` pouze pro zástupné hodnoty.
- Pro volitelné lokální experimenty s Ollamou používejte proměnné prostředí.

## Dokumentace

- Udržujte odkazy na navigaci v článcích aktuální.
- Aktualizujte `README.md` při přidání nového článku, notebooku, souboru požadavků nebo souboru s ukázkovými daty.
- Aktualizujte `CHANGELOG.md` před publikováním viditelné aktualizace repozitáře.

## Ověřování

Workflow GitHub Actions spouští:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Návrhy materiálů ve složce `drafts/` jsou při ověřování repozitáře přeskočeny, dokud nejsou připraveny k veřejnému zaindexování.

## Problémy

Používejte šablonu zpětné vazby k článkům pro opravy článků a šablonu problémů s notebookem pro problémy s jeho spuštěním.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->