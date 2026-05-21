# Turuan ang AI na Sagutin ang mga Tanong Batay sa Iyong mga Dokumento

Kinokolekta ng repositoryong ito ang isang serye ng blog noong 2026 tungkol sa pagbuo ng mga document-grounded AI system gamit ang RAG, Azure AI services, open-source na mga alternatibo, at mga evaluation-oriented na workflow.

## Background

Noong 2023, nagtrabaho ako sa isang pares ng mga tutorial tungkol sa pagtuturo sa ChatGPT na sumagot ng mga tanong mula sa mga PDF na dokumento gamit ang Azure AI Search at Azure OpenAI. Ang ideya ng "ChatGPT sa iyong data" ay tila bago pa noon, at ang layunin ay ipakita ang isang praktikal na workflow: mag-imbak ng mga dokumento, i-index ang mga ito, kunin ang mga kaugnay na nilalaman, at bumuo ng mga sagot mula sa nakuha na konteksto.

Noong 2026, mas malaki na ang ecosystem ng RAG. Sinusuportahan ng Azure AI Search ang mga modernong vector at hybrid retrieval pattern, bahagi ng mas malawak na Microsoft Foundry Models ecosystem ang Azure OpenAI, at naging mga praktikal na pagpipilian para sa mga tunay na sistema ang mga open-source tool tulad ng LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, at vLLM.

Kaya gusto kong balikan ang paksang ito. Hindi na lamang tanong ang "Paano ako gumawa ng RAG?" Ngayon, maraming paraan na para gawin ito, at ang mas mahalagang tanong ay "Anong arkitektura ang dapat kong piliin para sa aking sitwasyon?"

Nagsisimula ang seryeng ito mula sa layer na paggawa ng desisyon. Bago pumasok sa malalim na implementasyon, tinitingnan nito kung bakit kailangan ng AI services ng retrieval, kailan angkop ang mga Azure-based managed services, kailan mas angkop ang mga open-source na alternatibo, at saan pumapasok ang fine-tuning.

## Mga Artikulo

1. [Serye 1: RAG, Azure vs mga Open-Source na Alternatibo, at Kailan Angkop ang Fine-Tuning](./series-1-rag-azure-open-source-fine-tuning.md)

## Suporta sa Maramihang Wika

### Sinusuportahan sa pamamagitan ng Co-op Translator (Awtomatikong at Laging Napapanahon)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](./README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Mas gusto mo bang I-clone Locally?**
>
> Kasama sa repositoryong ito ang 50+ na pagsasalin ng wika na malaki ang pinapataas sa laki ng pag-download. Para mag-clone nang walang mga pagsasalin, gamitin ang sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Bibigyan ka nito ng lahat ng kailangan mo upang tapusin ang kurso nang mas mabilis ang pag-download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->