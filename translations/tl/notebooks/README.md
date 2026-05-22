# Notebooks

Sinusuportahan ng mga notebook na ito ang serye ng mga artikulo na may mga maaaring patakbuhin na mga halimbawa.

| Notebook | Artikulo | Layunin |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG gamit ang FastEmbed, Qdrant local mode, retrieval, reranking, optional Ollama generation, at mga sanggunian ng pinagmulan |

## Patakbuhin Nang Lokal

I-install ang mga kinakailangan para sa notebook na nais mong patakbuhin:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

O i-install ang lahat ng dependencies:

```powershell
python -m pip install -r requirements\all.txt
```

## Beripikahin

Mula sa ugat ng repositoryo:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Maaaring basahin ng Series 2 ang konfigurasyon ng Ollama mula sa isang `.env` file sa ugat ng repositoryo. Magsimula mula sa [../.env.example](../../../.env.example), na nakaayos ayon sa serye.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->