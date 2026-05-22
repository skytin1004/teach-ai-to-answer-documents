# உங்கள் ஆவணங்களின் அடிப்படையில் கேள்விகளுக்கு பதிலளிக்க கற்பிக்க AI

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

இந்த தொகுப்பு RAG, Azure AI சேவைகள், திறந்த மூல மாற்றிகள் மற்றும் மதிப்பீடு நோக்கிட்ட வேலைப்பாடுகளுடன் ஆவணம்-அடிப்படை AI அமைப்புகளை கட்டியெழுப்பும் 2026 வலைப்பதிவு தொடர் ஒன்றை சேகரித்துள்ளது.

## பின்னணி

2023ல், நான் Azure AI Search மற்றும் Azure OpenAI பயன்படுத்தி PDF ஆவணங்களிலிருந்து கேள்விகளுக்கு பதிலளிக்க ChatGPT கற்பிப்பதற்கான இரண்டு பயிற்சி பதிவுகளை உருவாக்கினேன். "உங்கள் தரவின் மேல் ChatGPT" என்ற கருது அப்போது இன்னும் புதியதிதான் என்று உணர்ந்தேன், மற்றும் குறிக்கோள் ஒரு பயனுள்ள வேலைப்பாட்டை காட்டுவதற்காக இருந்தது: ஆவணங்களை சேமிக்க, குறியிட, சம்பந்தப்பட்ட உள்ளடக்கத்தை மீட்டெடுக்க, அந்த மீட்டெடுத்த உள்ளடக்கத்திலிருந்து பதில்களை உருவாக்க.

2026ல், RAG சூழல் மிகவும் விரிவடைந்துள்ளது. Azure AI Search நவீன வெக்டர் மற்றும் கலவையான மீட்டெடுப்பு பரிசுரங்குகளை ஆதரிக்கிறது, Azure OpenAI மைக்ரோசாஃப்ட் Foundry Models இன் பெரியச் சூழலின் ஒரு பகுதியாக உள்ளது, மற்றும் திறந்த மூல கருவிகள் LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, மற்றும் vLLM போன்றவை உண்மையான அமைப்புகளுக்கு நடைமுறை தேர்வுகளாக மாறி விட்டன.

அதனால் இந்த தலைப்புக்கு மீண்டும் திரும்ப விரும்பினேன். கேள்வி இப்போது "நான் எப்படி RAG கட்டுவேன்?" என்பதுதான் இல்லை. இப்போது அதை கட்ட பல வழிகள் உள்ளன, மேலும் முக்கியமான கேள்வி "எந்த கட்டமைப்பை நான் என் சூழலுக்குச் தேர்ந்தெடுக்க வேண்டும்?" என்பதுதான்.

இந்த தொடரின் துவக்கம் அந்த முடிவெடுக்கும் அடியில் இருந்து, பின்னர் அதை நடைமுறைப் பயிற்சிகளாக மாற்றுகிறது. முதல் அமலாக்க பாதை உள்ளூர் திறந்த மூல RAG அமைப்பை கட்ட முனைவோம், இது எவரும் எடுத்துக்காட்டான தரவுடன், Qdrant, Ollama, மற்றும் Phi-4-mini பயன்படுத்தி இயங்கலாம்.

## கட்டுரைகள்

கட்டுரை குறியீட்டிற்கு [articles/README.md](./articles/README.md) ஐ பார்க்கவும்.

1. [தொடர் 1: RAG, Azure vs திறந்த மூல மாற்றிகள், மற்றும் எப்பொழுது நுண்மையாக்கம் பொருந்தும்](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [தொடர் 2: ஒருங்கிணைந்த உள்ளூர் திறந்த மூல RAG அமைப்பை கட்டும்](./articles/series-2-open-source-rag-end-to-end.md)

அடுத்ததாக வரவிருக்கும்:

- அதே RAG அமைப்பை Azure AI Search மற்றும் Azure OpenAI கொண்டு மறுவமைக்க.
- ஒரு டெமோ பதிலுக்கு மேலாக மதிப்பீடு மற்றும் பின்வழிச் சோதனைகளைச் சேர்க்க.

## நோட்புக்குகள்

அமைப்புச் கட்டுரைகள் நோட்புக்குகளை பயன்படுத்துகின்றன, அதனால் மீட்டெடுப்பு மற்றும் மதிப்பீடு படிகளைக் நேரடியாக பரிசோதிக்கலாம். கோப்பக நிலை வழிகாட்டிக்கு [notebooks/README.md](./notebooks/README.md) பார்க்கவும்.

> [!TIP]
> மிகவும் விரைவு பாதையை விரும்பினால் தொடர் 2 முதல் தொடங்கவும். இது எடுத்துக்காட்டான தரவுடன் உள்ளூர் இயங்குகிறது, CPU-அணுகுமுறை உடைய எம்பெடிங்க்களை பயன்படுத்துகிறது, Qdrant உள்ளூர் முறையில் இயங்குகிறது, மற்றும் மேக அங்கீகாரங்கள் தேவையில்லை.

| தொடர் | நோட்புக் | தேவைகள் | உள்ளூர் சரிபார்த்தல் |
| --- | --- | --- | --- |
| தொடர் 2 | [திறந்த மூல RAG நோட்புக்](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant உள்ளூர் முறை, மீட்டெடுத்தல், மறுஐர்வாகம், மற்றும் மூல இணைப்புகள் சரிபார்க்கப்பட்டவை |

உள்ளூரில் நோட்புக் ஓட, ஒரு நித்திய சூழல் உருவாக்கி பொருந்தும் தேவைகள் கோப்பைப் பதித்து நிறுவவும். உதாரணமாக:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## எடுத்துக்காட்டான தரவு

நோட்புக்குகள் [sample_data](../../sample_data) என்ற சிறிய உள்ளூர் தொகுதியைப் பயன்படுத்துகின்றன, இதனால் எடுத்துக்காட்டுகள் தனிப்பட்ட ஆவணங்கள் அல்லது மேக அங்கீகாரங்கள் இல்லாமல் இயங்கலாம். விவரங்களுக்கு [sample_data/README.md](./sample_data/README.md) ஐ பார்க்கவும்.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## உள்ளூர் சரிபார்ப்பு சுருக்கம்

சரிபார்ப்பு முடிவுகள் ஒவ்வொரு கட்டுரையிலும் மற்றும் [SERIES_PLAN.md](./SERIES_PLAN.md) லிலும் பதிவு செய்யப்பட்டுள்ளன.

| பகுதி | முடிவு |
| --- | --- |
| தொடர் 2 திறந்த மூல பாதை | FastEmbed 384-பரிமாண உள்ளூர் எம்பெடிங்க்களை உருவாக்கியது, Qdrant நினைவக சேகரிப்பில் 8 வெக்டர்களைக் சேர்த்தது, எளிமையான மறுஐர்வாகம் எதிர்பார்க்கப்படும் பகுதியை மீட்டெடுத்தது; விருப்பமான Ollama உருவாக்கம் `phi4-mini:3.8b` உடன் முடிந்தது |

உள்ளூர் நோட்புக் இருக்கும் இரகசியங்கள் கடுமையாகக் குறியாக்கம் செய்யப்பட்டுள்ளன.

## உள்ளூர் Ollama உருவாக்கம்

தொடர் 2 நோட்புக் இயல்பாக உள்ளூர் பாதுகாப்பானது. உள்ளூர Ollama உருவாக்கத்துக்கு, [.env.example](../../.env.example) ஐ `.env` ஆக நகலெடுத்து தொடர் 2 மதிப்புகளை நிரப்பவும்.

தொடர் 2 Ollama உருவாக்கத்துக்கு, இந்த கோப்பின் பின்னருள்ள பகுதியை செயல்படுத்தவும்:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

தொடர் 2 நோட்புக் தானாகவே `python-dotenv` பயன்படுத்தி `.env` ஐ கிடைத்த இடத்தில் இருந்து ஏற்றுகிறது.

> [!IMPORTANT]
> `.env` கோப்புகள், API விசைகள், தனிப்பட்ட முடிச்சுகள் அல்லது வாடிக்கையாளர்-குறைந்த மதிப்புகள் மூலம் கொடுப்பதைத் தவிர்க்கவும். தொகுப்பு குறியீட்டில் மற்றும் நோட்புக்குகளில் இரகசியங்களை முரண்படாமல் வைத்துள்ளது.

தேவைகள் கோப்புகள் [requirements/README.md](./requirements/README.md) இல் பதிவு செய்யப்பட்டுள்ளன.

இணைப்புகள், நோட்புக் அமைப்பு, நோட்புக் வெளியீட்டு சுத்தமாக்கல், மற்றும் மிகப்பெரிய ஆபத்துள்ள இரகசிய நடைமுறைகளை சரிபார்க்க:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

சரிபார்ப்பு ஸ்கிரிப்ட்கள் [scripts/README.md](./scripts/README.md) இல் பதிவுசெய்யப்பட்டுள்ளன.

அனைத்து உள்ளூர்-பாதுகாப்பான நோட்புக்குகளை ஒரே சூழலில் இயக்க:

```powershell
python scripts\verify_notebooks.py --execute
```

அதே சரிபார்ப்பு நடைமுறை GitHub Actions இல் புஷ், புல் கோரிக்கைகள், மற்றும் கைமுறையா வேலைப்பாடுகளை இயக்கும்போது இயங்கும். வரைவு கட்டுரைகள் மற்றும் நோட்புக்குகள் பொதுச் சரிபார்ப்பு பாதையில் இருந்து குறுவிக்கப்பட்டுள்ளன.

புதுப்பிப்புகளை வெளியிடுவதற்கு முன், [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) ஐப் பயன்படுத்தவும்.

தற்போதைய வெளியிடப்படாத மாற்ற சுருக்கத்திற்காக [CHANGELOG.md](./CHANGELOG.md) பார்க்கவும்.

பங்களிப்பு மற்றும் நோட்புக் பராமரிப்பு வழிகாட்டிகளுக்கு [CONTRIBUTING.md](./CONTRIBUTING.md) ஐ பாருங்க.

## பலமொழி ஆதரவு

### கூட்டாண்மை மொழிபெயர்த்தால் ஆதரவு (தானாக இயங்கும் மற்றும் எப்போதும் புதுப்பிக்கும்)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](./README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **உள்ளூரில் நகலெடுக்க விரும்புகிறீர்களா?**
>
> இந்த தொகுப்பில் 50க்கும் மேற்பட்ட மொழி மொழிபெயர்ப்புகள் உள்ளன, இது பதிவிறக்க அளவை குறிப்பிடத்தக்கவாறு அதிகரிக்கிறது. மொழிபெயர்ப்புகளை இல்லாமல் கிளோன் செய்ய sparse checkout பயன்படுத்தவும்:
>
> **Bash / macOS / லினக்ஸ்:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (விண்டோஸ்):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> இப்படியான முறையில், பயிற்சியை முடிக்க தேவையான அனைத்தும் மிக வேகமான பதிவிறக்கத்துடன் உங்களுக்கு கிடைக்கும்.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**மறுப்பு**:
இந்த ஆவணம் AI மொழிபெயர்ப்பு சேவை [Co-op Translator](https://github.com/Azure/co-op-translator) பயன்படுத்தி மொழிபெயர்க்கப்பட்டுள்ளது. நாங்கள் துல்லியத்திற்காக முயற்சி செய்துள்ளோம், ஆனால் தானாக செய்யப்படும் மொழிபெயர்ப்புகளில் பிழைகள் அல்லது தவறுகள் இருக்கலாம் என்பதை கவனத்தில் கொள்ளவும். அசல் ஆவணம் அதன் தாய்மொழியில் அதிகாரப்பூர்வ ஆதாரமாக கருதப்பட வேண்டும். முக்கியமான தகவல்களுக்கு, தொழில்நுட்பமான மனித மொழிபெயர்ப்பு பரிந்துரைக்கப்படுகிறது. இந்த மொழிபெயர்ப்பைப் பயன்படுத்துவதால் ஏற்படும் எந்த தவறான புரிதல்கள் அல்லது தவறான விளக்கத்திற்கும் நாங்கள் பொறுப்பில்வில்லை.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->