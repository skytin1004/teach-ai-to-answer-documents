# Popis za provjeru prije objave

Koristite ovaj popis prije nego što izvršite commit ili push javnih ažuriranja.

## Sigurnost

- Potvrdite da u Markdown datotekama, radnim bilježnicama, uzorcima podataka ili skriptama nisu napisani API ključevi, tokeni, lozinke ili privatni endpointi.
- Držite vjerodajnice u varijablama okoline ili upravljanoj identifikaciji, a ne u commitanim datotekama.
- Nemojte commitati `.env` datoteke ili izlaze izvršenih radnih bilježnica.
- `.env.example` neka sadrži samo rezervirane oznake.

## Verifikacija

Pokrenite skriptu za verifikaciju repozitorija:

```powershell
python scripts\verify_notebooks.py
```

Prije objave promjena implementacije pokrenite potpuno lokalno sigurno izvršavanje radne bilježnice:

```powershell
python scripts\verify_notebooks.py --execute
```

Očekivane provjere:

- lokalni Markdown linkovi prolaze
- validacija JSON radne bilježnice prolazi
- radne bilježnice ne sadrže spremljene izlaze ili brojeve izvršenja
- skeniranje uzoraka visokorizičnih tajni prolazi
- javne radne bilježnice se izvršavaju lokalno
- materijal u `drafts/` se namjerno preskače

## Pregled

- Potvrdite da linkovi u README člancima vode do namijenjenih datoteka.
- Potvrdite da svaki članak ima navigaciju repozitorija i povezane linkove na radne bilježnice.
- Potvrdite da draftovi nisu povezani iz javnih indeksa osim ako nisu spremni za objavu.
- Potvrdite da GitHub predlošci za issue i pull request još uvijek odgovaraju tijeku rada repozitorija.
- Potvrdite da rezultati verifikacije u članku odgovaraju najnovijem izlazu radne bilježnice.
- Potvrdite da se GitHub Actions workflow očekuje nakon pushanja.
- Potvrdite da `CHANGELOG.md` odražava aktualno objavljivanje.
- Potvrdite da `CONTRIBUTING.md` još uvijek odgovara tijeku rada repozitorija.

## Git

- Pregledajte `git status --short --branch`.
- Pregledajte `git diff --stat`.
- Commitajte i pushajte samo kada ste eksplicitno spremni.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->