# Mga Kinakailangan

Bawat implementasyon ng artikulo ay may nakatuon na file ng mga kinakailangan.

| File | Ginagamit ni |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Series 2 na open-source RAG notebook, kabilang ang mga opsyonal na Ollama generation helpers |
| [all.txt](../../../requirements/all.txt) | Pag-verify sa antas ng repositoryo at CI |

Gamitin ang nakatuong file kapag nagpapagana ng isang notebook. Gamitin ang `all.txt` kapag nagva-validate sa buong repositoryo.

Kasama sa `open-source-rag.txt` at `all.txt` ang `fastembed` para sa lokal na embeddings at `python-dotenv` upang maaaring opsyonal na paganahin ng Series 2 ang Ollama generation mula sa `.env` nang hindi binabago ang retrieval pipeline.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->