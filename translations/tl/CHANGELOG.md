# Changelog

## Unreleased

Paunang pampublikong saklaw ng release para sa **Teach AI to Answer Questions Based on Your Documents**.

### Added

- Artikulo sa Series 1 tungkol sa mga desisyon sa arkitektura ng RAG, mga tradeoff sa Azure kumpara sa open-source, at kung saan pumapasok ang fine-tuning.
- Artikulo at notebook ng Series 2 para sa lokal na open-source RAG workflow gamit ang Qdrant local mode, FastEmbed local embeddings, lightweight reranking, Ollama, at Phi-4-mini.
- Format ng step-by-step end-to-end tutorial ng Series 2 na may mga snippet ng Python at mga tala ng beripikasyon mula sa naisagawang notebook.
- Opsyonal na landas ng pagbuo ng sagot sa Series 2 gamit ang Ollama at Phi-4-mini habang pinananatiling local CPU-friendly retrieval bilang default na landas.
- Lokal na beripikasyon ng Ollama para sa Series 2 gamit ang `phi4-mini:3.8b` sa RTX 3060 Laptop GPU.
- Halimbawang data para sa mga patakaran sa paaralan at patnubay ng kurso AI.
- Mga requirements files para sa pampublikong notebook at beripikasyon sa antas ng repository.
- Script ng beripikasyon ng repository para sa lokal na Markdown links at beripikasyon/pagsasagawa ng notebook.
- Workflow ng GitHub Actions para sa beripikasyon ng notebook.
- `.env.example` para sa opsyonal na lokal na setup ng Ollama generation nang hindi kinokomit ang lokal na konfigurasyon.
- Mga README file sa antas ng folder para sa mga artikulo, notebook, requirements, sample data, at mga script.
- Checklist ng pag-publish para sa pampublikong kaligtasan at beripikasyon.
- Draft workspace para sa mga susunod na nilalaman ng Azure at evaluasyon.

### Verified

- Pumasa sa beripikasyon ng lokal na Markdown link.
- Matagumpay na na-validate ang Series 2 notebook.
- Matagumpay na na-execute ang Series 2 notebook sa lokal na kapaligiran ng beripikasyon.
- Pinananatili ang mga notebook file nang walang naka-save na output o execution counts.
- Walang totoong sikreto ang na-commit.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->