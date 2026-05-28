# तपाईँका कागजातहरूमा आधारित प्रश्नहरूको उत्तर दिन AI सिकाउनुहोस्

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

यो भण्डारले RAG, Azure AI सेवाहरू, खुला-स्रोत विकल्पहरू, र मूल्यांकन-केन्द्रित कार्यप्रवाहहरूसँग कागजात-आधारित AI प्रणालीहरू निर्माण गर्ने बारे 2026 को ब्लग श्रृंखला सङ्कलन गर्दछ।

## पृष्ठभूमि

2023 मा, मैले Azure AI Search र Azure OpenAI प्रयोग गरेर PDF कागजातहरूबाट प्रश्नहरूको उत्तर दिन ChatGPT सिकाउने दुई ट्यूटोरियलहरूमा काम गरेँ। "तपाईंको डाटा मा ChatGPT" को विचार त्यतिबेला अझै नयाँ लाग्थ्यो, र लक्ष्य व्यावहारिक कार्यप्रवाह देखाउनु थियो: कागजातहरू भण्डारण गर्नुहोस्, तिनीहरूलाई सूचकांक गर्नुहोस्, सान्दर्भिक सामग्री पुनःप्राप्त गर्नुहोस्, र त्यो पुनःप्राप्त सन्दर्भबाट उत्तरहरू उत्पन्न गर्नुहोस्।

2026 मा, RAG ईकोसिस्टम धेरै ठूलो भइसकेको छ। Azure AI Search ले आधुनिक भेक्टर र संयोजन पुनःप्राप्ति ढाँचाहरू समर्थन गर्दछ, Azure OpenAI व्यापक Microsoft Foundry Models ईकोसिस्टमको हिस्सा हो, र LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, र vLLM जस्ता खुला-स्रोत उपकरणहरू वास्तविक प्रणालीहरूको लागि व्यावहारिक विकल्प बनेका छन्।

त्यसैले मैले यो विषयमा पुनः ध्यान दिन चाहँथेँ। अब प्रश्न मात्रै "म कसरि RAG निर्माण गर्ने?" होइन। त्यहाँ यसलाई निर्माण गर्ने धेरै तरिकाहरू छन्, र अझ महत्वपूर्ण प्रश्न हो "मेरो स्थिति अनुसार कुन वास्तुकला रोज्ने?"

यो श्रृंखला त्यो निर्णय-निर्माण तहबाट सुरु हुन्छ, अनि त्यसलाई व्यावहारिक ट्यूटोरियलहरूमा परिणत गर्छ। पहिलो कार्यान्वयन मार्गले स्थानीय खुला-स्रोत RAG प्रणाली बनाउँछ जुन कुनै पनि ले नमूना डाटा, Qdrant, Ollama, र Phi-4-mini सँग चलाउन सक्छ।

## लेखहरू

लेख सूचीको लागि [articles/README.md](./articles/README.md) हेर्नुहोस्।

1. [श्रृंखला १: RAG, Azure बनाम खुला-स्रोत विकल्पहरू, र कहिले Fine-Tuning बान्छनीय हुन्छ](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [श्रृंखला २: स्थानीय खुला-स्रोत RAG प्रणाली अन्त्यदेखि अन्त्यसम्म निर्माण गर्नुहोस्](./articles/series-2-open-source-rag-end-to-end.md)

आउँदैछ:

- Azure AI Search र Azure OpenAI सँग त्यो समान RAG प्रणाली पुनर्निर्माण गर्नु।
- डेमो उत्तर भन्दा पर मूल्यांकन र रिग्रेसन जाँचहरू थप्नु।

## नोटबुकहरू

कार्यान्वयन लेखहरूले नोटबुकहरू प्रयोग गर्छन् ताकि पुनःप्राप्ति र मूल्यांकन चरणहरू प्रत्यक्ष निरीक्षण गर्न सकियोस्। फोल्डर स्तरीय मार्गनिर्देशनको लागि [notebooks/README.md](./notebooks/README.md) हेर्नुहोस्।

> [!TIP]
> सबैभन्दा छिटो मार्ग चाहनुहुन्छ भने श्रृंखला २ बाट सुरु गर्नुहोस्। यो स्थानीय रूपमा नमूना डाटा, CPU-अनुकूल एम्बेडिङ्स, Qdrant स्थानीय मोड र कुनै क्लाउड प्रमाणपत्र बिना चल्छ।

| श्रृंखला | नोटबुक | आवश्यकताहरू | स्थानीय प्रमाणिकरण |
| --- | --- | --- | --- |
| श्रृंखला २ | [खुला-स्रोत RAG नोटबुक](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant स्थानीय मोड, पुनःप्राप्ति, पुनर्मूल्याङ्कन, र स्रोत वायरिङ प्रमाणित गरिएको |

नोटबुक स्थानीय रूपमा चलाउन, भर्चुअल वातावरण सिर्जना गरी मिल्दोजुल्दो आवश्यकताहरू फाइल स्थापना गर्नुहोस्। उदाहरण:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## नमूना डाटा

नोटबुकहरूले साना स्थानीय सम्वाहिक डाटासेट [sample_data](../../sample_data) प्रयोग गर्दछन् ताकि उदाहरणहरू निजी कागजात वा क्लाउड प्रमाणपत्र बिना चलाउन सकियोस्। विवरणका लागि [sample_data/README.md](./sample_data/README.md) हेर्नुहोस्।

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## स्थानीय प्रमाणिकरण सारांश

प्रमाणिकरण परिणामहरू प्रत्येक लेखमा र [SERIES_PLAN.md](./SERIES_PLAN.md) मा रेकर्ड गरिएको छ।

| क्षेत्र | परिणाम |
| --- | --- |
| श्रृंखला २ खुला-स्रोत मार्ग | FastEmbed ले ३८४-आयाम स्थानीय एम्बेडिङ्स उत्पन्न गर्‍यो, Qdrant मेमोरीमा ८ भेक्टरहरू सम्मिलित गर्‍यो, हल्का पुनर्मूल्याङ्कनले अपेक्षित सेक्षन पुनःप्राप्त गर्‍यो; वैकल्पिक Ollama उत्पादन `phi4-mini:3.8b` सँग पूरा भयो |

स्थानीय नोटबुक जानाजानी गोप्य जानकारी समावेश गर्नबाट बच्छ।

## स्थानीय Ollama उत्पादन

श्रृंखला २ नोटबुक डिफल्ट रूपमा स्थानीय सुरक्षित छ। स्थानीय Ollama उत्पादन सक्षम गर्न, [.env.example](../../.env.example) लाई `.env` मा कपी गरेर श्रृंखला २ का मानहरू भर्नुहोस्।

श्रृंखला २ Ollama उत्पादनका लागि, यसलाई अनकमेन्ट गर्नुहोस्:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

श्रृंखला २ नोटबुकले `python-dotenv` मार्फत भण्डारको मूलबाट `.env` स्वचालित रूपमा लोड गर्छ।

> [!IMPORTANT]
> `.env` फाइलहरू, API कुञ्जीहरू, निजी अन्तबिन्दुहरू, वा टेनेन्ट-विशेष मानहरू कमिट नगर्नुहोस्। यो भण्डार जानाजानी Markdown फाइलहरू र नोटबुकहरूबाट गोप्यताहरूलाई बाहिर राख्छ।

आवश्यकताहरू फाइलहरूको कागजात [requirements/README.md](./requirements/README.md) मा छ।

लिङ्कहरू, नोटबुक संरचना, नोटबुकको सफाइ अनुसार नतिजा, र उच्च जोखिम गोप्य ढाँचाहरूको मान्यता गर्न:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

प्रमाणिकरण स्क्रिप्टहरूको कागजात [scripts/README.md](./scripts/README.md) मा छ।

सबै स्थानीय-सुरक्षित नोटबुकहरू एउटै वातावरणमा चलाउन:

```powershell
python scripts\verify_notebooks.py --execute
```

त्यसै प्रमाणिकरण प्रक्रिया GitHub Actions मा पुस, पुल अनुरोध, र म्यानुअल वर्कफ्लो डिस्प्याचहरूमा चल्छ। मस्यौदा लेखहरू र नोटबुकहरू जानाजानी सार्वजनिक प्रमाणिकरण मार्गबाट बाहिर राखिएका छन्।

अपडेटहरू प्रकाशन गर्नु अघि [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) प्रयोग गर्नुहोस्।

हालको अप्रकाशित परिवर्तन सारांशका लागि [CHANGELOG.md](./CHANGELOG.md) हेर्नुहोस्।

योगदान र नोटबुक स्वच्छता मार्गनिर्देशनका लागि [CONTRIBUTING.md](./CONTRIBUTING.md) हेर्नुहोस्।

## बहुभाषी समर्थन

### सहकारी अनुवादक मार्फत समर्थित (स्वचालित र सदैव अद्यावधिक)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](./README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानीय रूपमा क्लोन गर्न मन छ?**
>
> यस भण्डारले ५०+ भाषा अनुवादहरू समावेश गर्छ जुन डाउनलोड साइज निकै बढाउँछ। अनुवादहरू बिना क्लोन गर्न sparse checkout प्रयोग गर्नुहोस्:
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
> यसले तपाईंलाई धेरै छिटो डाउनलोडको साथ कोर्स पूरा गर्न आवश्यक सबै कुरा दिन्छ।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी सही हुन प्रयास गर्छौं, तर कृपया जानकार हुनुस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छन्। मूल दस्तावेज़ यसको मूल भाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलत बुझाइ वा त्रुटिको लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->