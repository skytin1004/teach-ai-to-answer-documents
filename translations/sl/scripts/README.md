# Skripte

Ta mapa vsebuje skripte za preverjanje skladišča.

## `verify_notebooks.py`

Preverja lokalne Markdown povezave, JSON zvezkov, čistost izhoda zvezkov in vzorce tveganih skrivnosti:

```powershell
python scripts\verify_notebooks.py
```

Izvede vse javne lokalno-varne zvezke:

```powershell
python scripts\verify_notebooks.py --execute
```

Potek dela GitHub Actions uporablja enako skripto.

Zasnove gradiv pod `drafts/` so preskočene, dokler niso pripravljene za javni indeks.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->