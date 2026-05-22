# Publishing Checklist

Gamitin ang checklist na ito bago mag-commit o mag-push ng mga pampublikong update.

## Safety

- Kumpirmahing walang mga API key, token, password, o pribadong endpoints na nakasulat sa mga Markdown file, notebook, sample data, o script.
- Panatilihin ang mga kredensyal sa environment variables o managed identity, hindi sa mga naka-commit na file.
- Huwag mag-commit ng mga `.env` file o mga output file mula sa na-execute na notebook.
- Panatilihin ang `.env.example` na placeholder lamang.

## Verification

Patakbuhin ang repository verification script:

```powershell
python scripts\verify_notebooks.py
```

Patakbuhin ang buong local-safe na pag-execute ng notebook bago i-publish ang mga pagbabago sa implementasyon:

```powershell
python scripts\verify_notebooks.py --execute
```

Inaasahang mga tseke:

- matagumpay ang local Markdown links
- matagumpay ang validation ng notebook JSON
- walang mga saved outputs o execution counts sa mga notebook
- matagumpay ang pag-scan ng high-risk secret pattern
- matagumpay na na-eexecute nang local ang mga pampublikong notebook
- sinasadyaang nilalaktawan ang draft material sa ilalim ng `drafts/`

## Review

- Kumpirmahing ang mga link sa README article ay tumutukoy sa mga tamang file.
- Kumpirmahing ang bawat artikulo ay may repository navigation at mga kaugnay na link sa notebook.
- Kumpirmahing hindi naka-link ang mga draft mula sa mga pampublikong index maliban kung handa na itong i-publish.
- Kumpirmahing ang mga template ng isyu at pull request sa GitHub ay parin tugma sa workflow ng repository.
- Kumpirmahing ang mga resulta ng verification sa artikulo ay tumutugma sa pinakabagong output ng notebook.
- Kumpirmahing ang GitHub Actions workflow ay inaasahang tumakbo pagkatapos ng push.
- Kumpirmahing ang `CHANGELOG.md` ay sumasalamin sa update na ipapublish.
- Kumpirmahing ang `CONTRIBUTING.md` ay nananatiling tumutugma sa workflow ng repository.

## Git

- Suriin ang `git status --short --branch`.
- Suriin ang `git diff --stat`.
- Mag-commit at mag-push lamang kapag handa na talaga.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->