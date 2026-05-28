# Contributing

Ang repositoryong ito ay inayos bilang isang serye ng blog kasama ang mga runnable na halimbawa ng notebook.

## Bago Magbukas ng Pull Request

Patakbuhin ang lokal na validation script:

```powershell
python scripts\verify_notebooks.py
```

Para sa mga pagbabago sa implementasyon o notebook, patakbuhin ang lokal-safe na pagpapatakbo ng notebook:

```powershell
python scripts\verify_notebooks.py --execute
```

## Mga Panuntunan sa Notebook

- Panatilihing nababasa at nakatuon sa kaugnay na artikulo ang mga notebook.
- Huwag i-commit ang mga naka-save na output ng notebook o bilang ng pagpapatupad.
- Gumamit ng maliit na sample data mula sa `sample_data/` maliban kung ang artikulo ay nangangailangan ng isang partikular na panlabas na resource.
- Irekord ang mga resulta ng beripikasyon sa kaugnay na artikulo kapag may mga pagbabago sa asal.

## Mga Sekreto at Kredensyal

- Huwag i-commit ang mga API key, token, password, pribadong endpoints, o `.env` files.
- Gamitin ang `.env.example` para lamang sa mga placeholder na halaga.
- Gumamit ng mga environment variable para sa mga opsyonal na lokal na eksperimento sa Ollama.

## Dokumentasyon

- Panatilihing updated ang mga link ng pag-navigate sa artikulo.
- I-update ang `README.md` kapag nagdagdag ng bagong artikulo, notebook, requirements file, o sample data file.
- I-update ang `CHANGELOG.md` bago maglathala ng nakikitang update sa repositoryo.

## Beripikasyon

Pinapatakbo ng GitHub Actions workflow:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Ang mga draft na materyales sa ilalim ng `drafts/` ay hindi isinasaalang-alang sa beripikasyon ng repositoryo hanggang ito ay handa na para sa pampublikong pag-index.

## Mga Isyu

Gamitin ang template ng feedback ng artikulo para sa mga pagwawasto sa artikulo at ang notebook issue template para sa mga problema sa pagpapatakbo ng notebook.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->