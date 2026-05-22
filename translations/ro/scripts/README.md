# Scripts

Acest folder conține scripturi de verificare a depozitului.

## `verify_notebooks.py`

Validează link-urile locale din Markdown, JSON-ul notebook-urilor, curățenia output-ului notebook-urilor și modele de secrete cu risc ridicat:

```powershell
python scripts\verify_notebooks.py
```

Execută toate notebook-urile publice și locale sigure:

```powershell
python scripts\verify_notebooks.py --execute
```

Fluxul de lucru GitHub Actions folosește același script.

Materialul în curs de redactare din `drafts/` este sărit până când este gata pentru indexul public.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->