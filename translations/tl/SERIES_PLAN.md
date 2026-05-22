# Turuan ang AI na Sumagot ng mga Tanong Batay sa Iyong Mga Dokumento - Plano ng Serye

Ang planong ito ay sumusubaybay sa pampublikong paglabas ng Serye 1 at Serye 2. Ang mga susunod na gawain sa Azure at pagsusuri ay inilalagay muna bilang mga draft hanggang sa ang mga halimbawa ay ganap na end-to-end at beripikado.

Huwag mag-commit o mag-push ng mga pagbabago hangga't hindi hayagang iniutos.

## Pampublikong Saklaw

Kasalukuyang pampublikong paglabas:

- Artikulo sa Serye 1: Mga desisyon sa arkitektura ng RAG, kalakasan at kahinaan ng Azure laban sa open-source, at kung saan kasya ang fine-tuning.
- Artikulo sa Serye 2: lokal na open-source na RAG na tutorial.
- Notebook sa Serye 2: tumatakbong lokal na RAG lab kasama ang FastEmbed, Qdrant, Ollama, at Phi-4-mini.
- Halimbawang data: mga Markdown file ng patakaran ng paaralan at gabay sa AI ng kurso.

I-draft na ngunit hindi pa nasa pampublikong index:

- Azure AI Search at Azure OpenAI rebuild.
- Pagsusuri at pagsusuri sa regression ng RAG.

## Senaryo ng Tutorial

Ang pinagsasaluhang senaryo ay isang katulong sa patakaran ng paaralan.

Sinusagot ng katulong ang tanong na ito mula sa mga lokal na dokumento:

```text
Can I use generative AI for my final assignment?
```

Ang inaasahang kilos ay:

1. I-load ang mga lokal na Markdown na dokumento.
2. Ihati at hatiin ang mga ito batay sa mga heading.
3. Gumawa ng lokal na embeddings at iimbak ang mga searchable na representasyon kasabay ang metadata.
4. Kunin ang kaugnay na seksyon ng patakaran.
5. Muling i-ranggo kung kinakailangan.
6. Bumuo o lumikha ng grounded na sagot.
7. Ibalik ang mga sipi.
8. Irekord ang mga resulta ng beripikasyon.

## Kasalukuyang Pampublikong Estruktura

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```

Ang materyal na draft ay nakaimbak sa ilalim ng `drafts/` at nilalaktawan sa beripikasyon ng repositoryo hanggang ito ay handa na para sa pampublikong pag-index.

## Beripikasyon ng Serye 2

Naberedeng patakbuhin sa Windows gamit ang Python 3.12.6.

- Matagumpay na na-install ang `requirements/open-source-rag.txt`.
- Napatakbo ang `notebooks/series-2-open-source-rag.ipynb` gamit ang `nbclient`.
- Lumampas sa lokal na beripikasyon: 2 sample na dokumento ang na-load, 8 chunks ang ginawa, FastEmbed ang lumikha ng 384-dimension na lokal na embeddings, na-initialize ang Qdrant in-memory na koleksyon, at 8 vectors ang naipasok.
- Pagsubok na tanong: "Maaari ko bang gamitin ang generative AI para sa aking huling asignatura?"
- Nangungunang nakuha na mapagkukunan pagkatapos ng magaan na muling pag-ranggo: `school_ai_policy.md`.
- Nangungunang nakuha na seksyon pagkatapos ng magaan na muling pag-ranggo: `Final Assignments`.
- Default na path ng sagot: lokal na transparent na tagabuo ng sagot.
- Na-install ang Ollama sa pamamagitan ng winget; matagumpay na nakuha ang `phi4-mini:3.8b`.
- Natapos ang Ollama na path ng pagbuo ng sagot gamit ang `phi4-mini:3.8b`.
- Laki ng modelong Ollama na file: humigit-kumulang 2.49GB sa disk.
- Laki ng na-load na Ollama na modelo: 3.3GB ang naulat ng `ollama ps`.
- GPU offload: 100% GPU ang naulat ng `ollama ps` sa RTX 3060 Laptop GPU.
- Naobserbahan ang GPU memory pagkatapos ng pagbuo: humigit-kumulang 3.5GB ng 6GB.
- Ang pagpapatakbo ng notebook gamit ang cached na FastEmbed model at payagan ang Ollama generation ay pumasa sa halos 34 na segundo sa pamamagitan ng verification script.
- Obserbasyon: isang maagang pag-load ng dokumento ay aksidenteng naisama ang `sample_data/README.md`; ngayon ang notebook ay naglo-load lamang ng dalawang intensiyonal na mga sample na dokumento nang tahasang.

## Beripikasyon ng Repositoryo

- Ang `scripts/verify_notebooks.py` ay nagpapatunay sa mga lokal na Markdown link, JSON ng notebook, kalinisan ng output ng notebook, at mga high-risk na pattern ng sikreto.
- Ang `scripts/verify_notebooks.py --execute` ay nagpapatakbo ng mga pampublikong notebook mula sa root ng repositoryo.
- Ang materyal na draft sa ilalim ng `drafts/` ay sinasadyang nilalaktawan.

## Susunod na Gawain

- Muling itayo ang parehong senaryo gamit ang Azure AI Search at Azure OpenAI bilang bahagi ng hinaharap na serye.
- Magdagdag ng retrieval at pagsusuri ng sagot kapag ang parehong lokal at Azure na implementasyon ay matatag na.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->