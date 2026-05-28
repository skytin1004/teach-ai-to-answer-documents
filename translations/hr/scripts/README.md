# Skripte

Ova mapa sadrži skripte za provjeru repozitorija.

## `verify_notebooks.py`

Validira lokalne Markdown veze, JSON bilježnice, čistoću izlaza bilježnice i obrasce visokorizičnih tajni:

```powershell
python scripts\verify_notebooks.py
```

Izvršava sve javne lokalno-sigurne bilježnice:

```powershell
python scripts\verify_notebooks.py --execute
```

Radni tijek GitHub Actions koristi isti skript.

Materijal u nacrtu unutar `drafts/` je preskočen dok nije spreman za javni indeks.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->