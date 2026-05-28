# Kontrolný zoznam pri publikovaní

Použite tento kontrolný zoznam pred potvrdením zmien alebo ich zverejnením.

## Bezpečnosť

- Overte, že v Markdown súboroch, poznámkových blokoch, ukážkových dátach alebo skriptoch nie sú zapísané žiadne API kľúče, tokeny, heslá ani súkromné koncové body.
- Uchovávajte prihlasovacie údaje v premenných prostredia alebo spravovanej identite, nie v potvrdených súboroch.
- Nepotvrdzujte `.env` súbory ani súbory výstupu vykonaných poznámkových blokov.
- Uchovávajte `.env.example` iba ako zástupný súbor.

## Overenie

Spustite skript na overenie úložiska:

```powershell
python scripts\verify_notebooks.py
```

Pred publikovaním zmien v implementácii spustite úplné lokálne bezpečné vykonanie poznámkového bloku:

```powershell
python scripts\verify_notebooks.py --execute
```

Očakávané kontroly:

- lokálne odkazy v Markdown prechádzajú
- validácia JSON poznámkových blokov prechádza
- poznámkové bloky neobsahujú uložené výstupy ani počet vykonaní
- kontrola vzorov vysoko rizikových tajomstiev prechádza
- verejné poznámkové bloky sa vykonávajú lokálne
- materiály v priečinku `drafts/` sú úmyselne vynechané

## Kontrola

- Overte, že odkazy v článku README ukazujú na zamýšľané súbory.
- Overte, že každý článok má navigáciu v repozitári a odkazy na súvisiace poznámkové bloky.
- Overte, že návrhy nie sú prelinkované z verejných indexov, pokiaľ nie sú pripravené na publikovanie.
- Overte, že šablóny issues a pull requestov na GitHube stále zodpovedajú workflow repozitára.
- Overte, že výsledky overenia v článku zodpovedajú najnovšiemu výstupu poznámkového bloku.
- Overte, že GitHub Actions workflow sa očakáva na spustenie po pushnutí.
- Overte, že `CHANGELOG.md` zobrazuje publikovanú aktualizáciu.
- Overte, že `CONTRIBUTING.md` stále zodpovedá workflow repozitára.

## Git

- Prezrite si výstup `git status --short --branch`.
- Prezrite si štatistiky zmien príkazom `git diff --stat`.
- Potvrďte a odošlite zmeny iba vtedy, keď ste výslovne pripravení.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->