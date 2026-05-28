# Prispievanie

Tento repozitár je organizovaný ako séria blogov plus spustiteľné príklady v notebookoch.

## Pred otvorením Pull Requestu

Spustite lokálny validačný skript:

```powershell
python scripts\verify_notebooks.py
```

Pre implementačné alebo zmeny v notebooku spustite lokálne bezpečnú exekúciu notebooku:

```powershell
python scripts\verify_notebooks.py --execute
```

## Návody pre notebooky

- Udržiavajte notebooky čitateľné a zamerané na súvisiaci článok.
- Nezaväzujte uložené výstupy alebo počty spustení notebookov.
- Používajte malé ukážkové dáta z `sample_data/`, pokiaľ článok nevyžaduje konkrétny externý zdroj.
- Zaznamenajte výsledky overenia v súvisiacom článku, keď sa správanie mení.

## Tajomstvá a prihlasovacie údaje

- Nezaväzujte API kľúče, tokeny, heslá, súkromné koncové body alebo súbory `.env`.
- Používajte `.env.example` iba pre zástupné hodnoty.
- Používajte premenné prostredia pre voliteľné lokálne experimenty Ollama.

## Dokumentácia

- Udržiavajte odkazy na navigáciu v článkoch aktuálne.
- Aktualizujte `README.md` pri pridávaní nového článku, notebooku, požiadavkového súboru alebo súboru vzorových dát.
- Aktualizujte `CHANGELOG.md` pred zverejnením viditeľnej aktualizácie repozitára.

## Overenie

GitHub Actions workflow spúšťa:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Koncepty materiálov v priečinku `drafts/` sú pri overovaní repozitára ignorované, kým nie sú pripravené na verejné indexovanie.

## Problémy

Používajte šablónu spätnej väzby k článkom na opravy článkov a šablónu pre problémy s notebookmi na problémy s vykonávaním notebooku.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->