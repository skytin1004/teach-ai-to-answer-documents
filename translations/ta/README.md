# உங்கள் ஆவணங்களின் அடிப்படையில் AI க்கு கேள்விகளுக்குப் பதிலளிப்பதை கற்பிக்கவும்

இந்த ரெப்பொசிடரி 2026ம் ஆண்டிற்கான ஒரு பிளாக் தொடர் சேர்க்கிறது, இது RAG, Azure AI சேவைகள், திறந்த மூல மாற்றுகள் மற்றும் மதிப்பீடு சார்ந்த வேலைநிரல்களுடன் ஆவணம் தீவிரமான AI கணினித் திட்டங்களை உருவாக்குவதைக் குறிக்கிறது.

## பின்னணி

2023 ஆம் ஆண்டில், PDF ஆவணங்களில் உள்ள கேள்விகளுக்கு பதிலளிக்க ChatGPT-ஐ Azure AI Search மற்றும் Azure OpenAI பயன்படுத்தி கற்பிப்பதற்கான இரண்டு பாடநெறிகள் உருவாக்கினேன். "உங்கள் தரவை அடிப்படையாக கொண்டு ChatGPT" என்ற எண்ணம் அந்நேரத்தில் புதிதாகவே எண்ணப்பட்டது, மற்றும் நோக்கம் ஒரு நடைமுறை வேலைநிரலைக் காட்டுவது: ஆவணங்களை சேமிக்கவும், அவற்றை அடையாளம் காணவும், தொடர்புடைய உள்ளடக்கத்தை பெறவும், பின்னர் அந்தக் கொண்டன்ட்டிலிருந்து பதில்கள் உருவாக்கவும்.

2026 ஆம் ஆண்டில், RAG சூழல் மிகவும் விரிவடைந்துள்ளது. Azure AI Search சமகால வெக்டர் மற்றும் குழைத்தல் மறுபயன்பாட்டுத் திட்டங்களை ஆதரிக்கிறது, Azure OpenAI மைக்ரோசாஃப்ட் Foundry Models சூழலில் பங்குபெறுகிறது, மற்றும் LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, மற்றும் vLLM போன்ற திறந்த மூல கருவிகள் உண்மையான திட்டங்களுக்கு நடைமுறையாக உள்ளன.

இதழ் காரணமாக, இந்த தலைப்பை மீண்டும் பார்க்க விரும்பினேன். கேள்வி இப்போது "நான் RAG-ஐ எப்படி உருவாக்குவது?" மட்டுமல்ல. அதை உருவாக்க பல வழிகளும் உள்ளன, மேலும் முக்கியமான கேள்வி "என் சூழலுக்கான கட்டமைப்பை நான் எதைத் தேர்வு செய்ய வேண்டும்?" ஆகிவிட்டது.

இந்த தொடர் அந்த முடிவு எடுக்கும் அடுக்கிலிருந்து துவங்குகிறது. செயல்பாட்டு அமலாக்கத்திற்கு ஆழமாக செல்லுமுன், ஏன் AI சேவைகளுக்கு மறுபயன்பாடு தேவை, Azure அடிப்படையிலான மேலாண்மை சேவைகள் எப்போது பொருந்தும், திறந்த மூல மாற்றுகள் எப்போது சிறந்தவை, மற்றும் fine-tuning எங்கே பொருந்துகிறது என்பவற்றை ஆராய்கிறது.

## கட்டுரைகள்

1. [தொடர் 1: RAG, Azure மற்றும் திறந்த மூல மாற்றுகள், மற்றும் fine-tuning எப்போது பொருந்துகிறது](./series-1-rag-azure-open-source-fine-tuning.md)

## பன்மொழி ஆதரவு

### கூட்டமைப்பு மொழிபெயர்ப்புக் கருவி மூலம் ஆதரவு (தானாகவும் எப்போதும் சமீபத்தியதாகவும்)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](./README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **உள்ளூர் கிளோன் செய்ய விரும்புகிறீர்களா?**
>
> இந்த ரெப்பொசிடரி 50+ மொழி மொழிபெயர்ப்புகளைக் கொண்டுள்ளது, இது பதிவிறக்க அளவை மிகப் பெரியதாக்குகிறது. மொழிபெயர்ப்புகள் இல்லாமல் கிளோன் செய்ய, sparse checkout பயன்படுத்தவும்:
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
> இது பாடநெறியை நிறைவு செய்ய தேவையான எல்லாவற்றையும் மிகவும் விரைவான பதிவிறக்கத்துடன் வழங்கும்.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**மறுப்பு**:
இந்த ஆவணம் AI மொழிபெயர்ப்பு சேவை [Co-op Translator](https://github.com/Azure/co-op-translator) பயன்படுத்தி மொழிபெயர்க்கப்பட்டுள்ளது. நாங்கள் துல்லியத்திற்காக முயற்சி செய்துள்ளோம், ஆனால் தானாக செய்யப்படும் மொழிபெயர்ப்புகளில் பிழைகள் அல்லது தவறுகள் இருக்கலாம் என்பதை கவனத்தில் கொள்ளவும். அசல் ஆவணம் அதன் தாய்மொழியில் அதிகாரப்பூர்வ ஆதாரமாக கருதப்பட வேண்டும். முக்கியமான தகவல்களுக்கு, தொழில்நுட்பமான மனித மொழிபெயர்ப்பு பரிந்துரைக்கப்படுகிறது. இந்த மொழிபெயர்ப்பைப் பயன்படுத்துவதால் ஏற்படும் எந்த தவறான புரிதல்கள் அல்லது தவறான விளக்கத்திற்கும் நாங்கள் பொறுப்பில்வில்லை.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->