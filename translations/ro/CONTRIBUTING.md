# Contribuții

Acest depozit este organizat ca o serie de bloguri plus exemple de notebook-uri rulabile.

## Înainte de a deschide un Pull Request

Rulați scriptul local de validare:

```powershell
python scripts\verify_notebooks.py
```

Pentru implementări sau modificări în notebook, rulați execuția locală sigură a notebook-ului:

```powershell
python scripts\verify_notebooks.py --execute
```

## Ghid pentru Notebook-uri

- Păstrați notebook-urile lizibile și concentrate pe articolul aferent.
- Nu comiteți output-urile salvate ale notebook-ului sau numerele de execuție.
- Folosiți date mici de eșantion din `sample_data/`, cu excepția cazului în care articolul necesită o resursă externă specifică.
- Înregistrați rezultatele verificării în articolul aferent când comportamentul se schimbă.

## Secrete și Credențiale

- Nu comiteți chei API, token-uri, parole, endpoint-uri private sau fișiere `.env`.
- Folosiți `.env.example` doar pentru valori de substituție.
- Folosiți variabile de mediu pentru experimentele locale opționale cu Ollama.

## Documentație

- Mențineți link-urile de navigare ale articolelor actualizate.
- Actualizați `README.md` când adăugați un nou articol, notebook, fișier de cerințe sau fișier de date de eșantion.
- Actualizați `CHANGELOG.md` înainte de a publica o actualizare vizibilă a depozitului.

## Verificare

Workflow-ul GitHub Actions rulează:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Materialul în stadiu de proiect din `drafts/` este omis de verificarea depozitului până când este gata pentru indexare publică.

## Probleme

Utilizați șablonul de feedback al articolului pentru corecturi ale articolului și șablonul de probleme pentru notebook pentru probleme de execuție ale notebook-ului.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->