# Contributing

Ovaj repozitorij je organiziran kao serija blogova plus izvršni primjeri u bilježnicama.

## Prije otvaranja zahtjeva za povlačenje

Pokrenite lokalni skript za provjeru:

```powershell
python scripts\verify_notebooks.py
```

Za promjene implementacije ili bilježnice, pokrenite lokalno sigurno izvršavanje bilježnice:

```powershell
python scripts\verify_notebooks.py --execute
```

## Smjernice za bilježnice

- Držite bilježnice čitljivima i usredotočenima na povezani članak.
- Nemojte upisivati spremljene izlaze bilježnica ili brojače izvršavanja.
- Koristite male primjere podataka iz `sample_data/` osim ako članak ne zahtijeva specifični vanjski resurs.
- Zabilježite rezultate provjere u povezanim člancima kad se ponašanje promijeni.

## Tajne i vjerodajnice

- Nemojte upisivati API ključeve, tokene, lozinke, privatne krajnje točke ili `.env` datoteke.
- Koristite `.env.example` samo za vrijednosti rezerviranih mjesta.
- Koristite varijable okoline za neobavezne lokalne Ollama eksperimente.

## Dokumentacija

- Održavajte veze za navigaciju članaka ažuriranima.
- Ažurirajte `README.md` kada dodajete novi članak, bilježnicu, datoteku zahtjeva ili datoteku primjera podataka.
- Ažurirajte `CHANGELOG.md` prije objave vidljive nadogradnje repozitorija.

## Verifikacija

Radni tijek GitHub Actions izvodi:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Skicirani materijal pod `drafts/` preskače se u provjeri repozitorija dok nije spreman za javno indeksiranje.

## Problemi

Koristite predložak za povratne informacije o članku za ispravke članaka i predložak problema za bilježnice za probleme s izvršavanjem bilježnica.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->