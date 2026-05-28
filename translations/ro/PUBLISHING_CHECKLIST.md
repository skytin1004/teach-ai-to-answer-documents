# Lista de verificare pentru publicare

Folosește această listă de verificare înainte de a face commit sau push pentru actualizările publice.

## Siguranță

- Confirmă că nu există chei API, token-uri, parole sau endpoint-uri private scrise în fișiere Markdown, notebook-uri, date de exemplu sau scripturi.
- Păstrează acreditările în variabile de mediu sau identitate gestionată, nu în fișiere comise.
- Nu face commit la fișiere `.env` sau la fișiere de output pentru notebook-uri executate.
- Păstrează fișierul `.env.example` doar cu substituenți.

## Verificare

Rulează scriptul de verificare a depozitului:

```powershell
python scripts\verify_notebooks.py
```

Rulează execuția completă a notebook-ului în mod local și sigur înainte de a publica modificările de implementare:

```powershell
python scripts\verify_notebooks.py --execute
```

Verificările așteptate:

- link-urile locale Markdown sunt funcționale
- validarea JSON a notebook-urilor trece
- notebook-urile nu conțin output-uri salvate sau numere de execuție
- scanarea după modele de secrete cu risc ridicat trece
- notebook-urile publice se execută local
- materialul în ciornă din `drafts/` este intenționat sărit

## Revizuire

- Confirmă că link-urile din README duc către fișierele intenționate.
- Confirmă că fiecare articol are navigare în depozit și link-uri către notebook-urile aferente.
- Confirmă că ciornele nu sunt legate din indexurile publice decât dacă sunt gata de publicare.
- Confirmă că template-urile de issues și pull requests din GitHub se potrivesc în continuare cu fluxul de lucru al depozitului.
- Confirmă că rezultatele de verificare din articol corespund cu ultimul output al notebook-ului.
- Confirmă că workflow-ul GitHub Actions este setat să ruleze după push.
- Confirmă că `CHANGELOG.md` reflectă actualizarea ce urmează a fi publicată.
- Confirmă că `CONTRIBUTING.md` corespunde în continuare fluxului de lucru al depozitului.

## Git

- Verifică `git status --short --branch`.
- Verifică `git diff --stat`.
- Fă commit și push doar când ești explicit pregătit.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->