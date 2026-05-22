# Scripts

Ang folder na ito ay naglalaman ng mga script para sa beripikasyon ng repositoryo.

## `verify_notebooks.py`

Nivavalida ang mga lokal na Markdown link, notebook JSON, kalinisan ng output ng notebook, at mga pattern ng high-risk secret:

```powershell
python scripts\verify_notebooks.py
```

Isinasagawa ang lahat ng pampublikong local-safe na mga notebook:

```powershell
python scripts\verify_notebooks.py --execute
```

Ginagamit ng workflow ng GitHub Actions ang parehong script.

Ang mga draft na materyal sa ilalim ng `drafts/` ay nilalaktawan hanggang ito ay handa na para sa pampublikong indeks.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->