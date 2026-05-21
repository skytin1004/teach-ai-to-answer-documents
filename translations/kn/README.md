# ನಿಮ್ಮ ದಾಖಲೆಗಳ ಆಧಾರದ ಮೇಲೆ AIಗೆ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸುವುದನ್ನು ಬೋಧಿಸಿ

ಈ ರೆಪೊಸಿಟರಿ RAG, ಅಜ್ಯೂರ್ AI ಸೇವೆಗಳು, ಮುಕ್ತ ಆವರಣ ಪರ್ಯಾಯಗಳು ಮತ್ತು ಮೌಲ್ಯಮಾಪನ-ಕೇಂದ್ರೀಕೃತ ಕೆಲಸದ ಪ್ರವಾಹಗಳೊಂದಿಗೆ ದಾಖಲೆ ಆಧಾರಿತ AI ವ್ಯವಸ್ಥೆಗಳನ್ನು ನಿರ್ಮಿಸುವ ಬಗ್ಗೆ 2026ರ ಬ್ಲಾಗ್ ಸರಣಿಯನ್ನು ಸಂಗ್ರಹಿಸುತ್ತದೆ.

## ಹಿನ್ನೆಲೆ

2023 ರಲ್ಲಿ, ನಾನು ಅಜ್ಯೂರ್ AI ಸರ್ಚ್ ಮತ್ತು ಅಜ್ಯೂರ್ ಓಪನ್AI ಬಳಸಿಕೊಂಡು PDF ದಾಖಲೆಗಳಿಂದ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಲು ChatGPT ಅನ್ನು ಬೋಧಿಸುವ ಬಗ್ಗೆ ಜೋಡಿ ಟ್ಯುಟೋರಿಯಲ್‌ಗಳಲ್ಲಿ ಕೆಲಸ ಮಾಡಿದೆ. "ನಿಮ್ಮ ಡೇಟಾದ ಮೇಲೆ ChatGPT" ಎಂಬ ಕಲ್ಪನೆ ಅದನ್ನೇನುಳಿದಾಗಲೂ ಹೊಸದಾಗಿ ಅನಿಸಿದವು, ಮತ್ತು ಗುರಿ عملي ಕಾರ್ಯಪ್ರವಾಹವೊಂದನ್ನು ತೋರಿಸುವುದು: ದಾಖಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ, ಸ_INDೆಕ್ ಮಾಡಿ, ಸಂಬಂಧಿತ ವಿಷಯವನ್ನು ಪಡೆದ ನಂತರ, ಆ ಸ್ಥಿತಿಯಿಂದ ಉತ್ತರಗಳನ್ನು ರಚಿಸುವುದು.

2026 ರಲ್ಲಿ, RAG ಪರಿಸರತಂತ್ರಾನು ಬಹಳ ದೊಡ್ಡದಾಗಿದೆ. ಅಜ್ಯೂರ್ AI ಸರ್ಚ್ ಆಧುನಿಕ ವೆಕ್ಟರ್ ಮತ್ತು ಸಂಯುಕ್ತ ಸೇರಿಸಿಕೊಳ್ಳುವ ಮಾದರಿಗಳನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ, ಅಜ್ಯೂರ್ ಓಪನ್AI Microsoft Foundry Models ಪರಿಸರತಂತ್ರದ ಭಾಗವಾಗಿದೆ, ಮತ್ತು LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, ಮತ್ತು vLLM ಮುಂತಾದ ಮುಕ್ತ ಮೂಲ ಸಾಧನಗಳು ವ್ಯವಹಾರಿಕ ವ್ಯವಸ್ಥೆಗಳಿಗೆ ಪ್ರಾಯೋಗಿಕ ಆಯ್ಕೆಗಳಾಗಿವೆ.

ಅದೇ ಕಾರಣಕ್ಕಾಗಿ ನಾನು ಈ ವಿಷಯವನ್ನು ಮರು ನೋಡುವ ಕುತೂಹಲ ಹೊಂದಿದ್ದೇನೆ. ಪ್ರಶ್ನೆ ಈಗ "ನಾನು RAG ಅನ್ನು ಹೇಗೆ ನಿರ್ಮಿಸುವುದು?" ಮಾತ್ರವಲ್ಲ. ಈಗ ಅದನ್ನು ನಿರ್ಮಿಸುವ ಅನೇಕ ಮಾರ್ಗಗಳಿವೆ, ಮತ್ತು ಹೆಚ್ಚಿನ ಪ್ರಮುಖ ಪ್ರಶ್ನೆ "ನನ್ನ ಪರಿಸ್ಥಿತಿಗೆ ಯಾವ ವಿನ್ಯಾಸವನ್ನು ಆಯ್ಕೆ ಮಾಡಬೇಕು?" ಎಂಬುದು.

ಈ ಸರಣಿ ಆ ನಿರ್ಧಾರಮಾಡುವ ಪದರದಿಂದ ಪ್ರಾರಂಭವಾಗುತ್ತದೆ. ಅನುಷ್ಠಾನದಲ್ಲಿ ಆಳವಾಗಿ ಹೋಗುವ ಮೊದಲು, ಏಕೆ AI ಸೇವೆಗಳಿಗೆ ಸೇರಿಸುವಿಕೆ ಅಗತ್ಯವಿದೆ, ಅಜ್ಯೂರ್ ಆಧಾರಿತ ನಿರ್ವಹಿಸಲ್ಪಟ್ಟ ಸೇವೆಗಳು ಯಾವಾಗ ಅರ್ಥಪೂರ್ಣವಾಗುತ್ತವೆ, ಮುಕ್ತ ಮೂಲ ಪರ್ಯಾಯಗಳು ಯಾವಾಗ ಉತ್ತಮ ಹೊಂದಿಕೆಯಾಗುತ್ತವೆ, ಮತ್ತು ಸೂಕ್ಷ್ಮ-ಶಿಕ್ಷಣ ಎಲ್ಲಿಗೆ ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ ಎಂಬುದನ್ನು ನೋಡುವದು.

## ಲೇಖನಗಳು

1. [ಸರಣಿ 1: RAG, ಅಜ್ಯೂರ್ ವಿರುದ್ಧ ಮುಕ್ತ ಮೂಲ ಪರ್ಯಾಯಗಳು, ಮತ್ತು ಸೂಕ್ಷ್ಮ-ಶಿಕ್ಷಣ ನಂಬಲು ಯಾಕೆ](./series-1-rag-azure-open-source-fine-tuning.md)

## ಬಹು-ಭಾಷಾ ಬೆಂಬಲ

### ಸಹ-ಆದರ್ಶಕ ಅನುವಾದಕಾರ ಮೂಲಕ ಬೆಂಬಲಿತ (ಸ್ವಯಂಚಾಲಿತವಾಗಿದ್ದು ಸದಾ تازه)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](./README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ಸ್ಥಳೀಯವಾಗಿ ಕ್ಲೋನ್ ಮಾಡಬೇಕೆಂದು ಇಷ್ಟಪಡುತ್ತೀರಾ?**
>
> ಈ ರೆಪೊಸಿಟರಿಯಲ್ಲಿ 50+ ಭಾಷಾ ಅನುವಾದಗಳು ಒಳಗೊಂಡಿದ್ದು, ಡೌನ್ಲೋಡ್ ಗಾತ್ರವನ್ನು ಬಹಳಷ್ಟು ಹೆಚ್ಚಿಸುತ್ತದೆ. ಅನುವಾದಗಳಿಲ್ಲದೆ ಕ್ಲೋನ್ ಮಾಡಲು, sparse checkout ಅನ್ನು ಬಳಸಿ:
>
> **ಬ್ಯಾಶ್ / macOS / ಲಿನಕ್ಸ್ನಲ್ಲಿ:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (ವಿಂಡೋಸ್):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> ಇದರಿಂದ ನೀವು ಕೋರ್ಸ್ ಪೂರ್ಣಗೊಳಿಸಲು ಅಗತ್ಯವಿರುವ ಎಲ್ಲವನ್ನೂ ಹೆಚ್ಚು ತ್ವರಿತ ಡೌನ್ಲೋಡ್‌ನಿಂದ ಪಡೆಯುತ್ತೀರಿ.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ಅಸ್ವೀಕಾರ**:
ಈ ದಸ್ತಾವೇಜು AI ಅನುವಾದ ಸೇವೆ [Co-op Translator](https://github.com/Azure/co-op-translator) ಬಳಸಿ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ನಿಖರತೆಯನ್ನು ಸಾಧಿಸಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದರೂ, ದಯವಿಟ್ಟು ಗಮನಿಸಿ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ದೋಷಗಳು ಅಥವಾ ಅಸಡ್ಡೆಗಳು ಇರಬಹುದು. ಮೂಲ ಭಾಷೆಯಲ್ಲಿರುವ ಮೂಲ ದಸ್ತಾವೇಜು ಪ್ರಾಮಾಣಿಕ ಮೂಲವೆಂದು ಪರಿಗಣಿಸಬೇಕು. ಪ್ರಮುಖ ಮಾಹಿತಿಗಾಗಿ, ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ. ಈ ಅನುವಾದವನ್ನು ಬಳಸುವ ಮೂಲಕ ಉಂಟಾಗುವ ಯಾವುದೇ ತಪ್ಪು ಅರ್ಥಗಳ ಅಥವಾ ತಪ್ಪು ವ್ಯಾಖ್ಯಾನಗಳ ಬಗ್ಗೆ ನಾವು ಹೊಣೆಗಾರರಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->