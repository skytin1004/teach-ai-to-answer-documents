# अपने दस्तावेज़ों के आधार पर AI को प्रश्नों के उत्तर देने के लिए शिक्षित करें

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

यह संग्रह एक 2026 की ब्लॉग श्रृंखला है जो दस्तावेज़-आधारित AI सिस्टम बनाने के बारे में RAG, Azure AI सेवाओं, ओपन-सोर्स विकल्पों, और मूल्यांकन-उन्मुख वर्कफ़्लो के साथ है।

## पृष्ठभूमि

2023 में, मैंने Azure AI Search और Azure OpenAI का उपयोग करके PDF दस्तावेज़ों से प्रश्नों के उत्तर देने के लिए ChatGPT को शिक्षित करने के बारे में दो ट्यूटोरियल पर काम किया। "आपके डेटा पर ChatGPT" का विचार तब भी नया महसूस होता था, और उद्देश्य एक व्यावहारिक वर्कफ़्लो दिखाना था: दस्तावेज़ संग्रहित करें, उन्हें सूचीबद्ध करें, संबंधित सामग्री पुनः प्राप्त करें, और उस पुनः प्राप्त संदर्भ से उत्तर उत्पन्न करें।

2026 में, RAG पारिस्थितिकी तंत्र बहुत बड़ा हो गया है। Azure AI Search आधुनिक वेक्टर और हाइब्रिड पुनर्प्राप्ति पैटर्न का समर्थन करता है, Azure OpenAI व्यापक Microsoft Foundry Models पारिस्थितिकी तंत्र का हिस्सा है, और LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, और vLLM जैसे ओपन-सोर्स टूल वास्तविक सिस्टम के लिए व्यावहारिक विकल्प बन गए हैं।

इसीलिए मैं इस विषय को फिर से देखना चाहता था। सवाल अब केवल "मैं RAG कैसे बनाऊं?" नहीं है। अब इसे बनाने के कई तरीके हैं, और सबसे महत्वपूर्ण सवाल है "मेरी स्थिति के लिए कौन सा आर्किटेक्चर चुनना चाहिए?"

यह श्रृंखला इस निर्णय-लेने वाली परत से शुरू होती है, फिर इसे व्यावहारिक ट्यूटोरियल में बदल देती है। पहला कार्यान्वयन पथ एक स्थानीय ओपन-सोर्स RAG सिस्टम बनाता है जिसे कोई भी नमूना डेटा, Qdrant, Ollama, और Phi-4-mini के साथ चला सकता है।

## लेख

लेख सूची के लिए देखे [articles/README.md](./articles/README.md)।

1. [श्रृंखला 1: RAG, Azure बनाम ओपन-सोर्स विकल्प, और जब फाइन-ट्यूनिंग समझ में आती है](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [श्रृंखला 2: एक स्थानीय ओपन-सोर्स RAG सिस्टम शुरुआत से अंत तक बनाएं](./articles/series-2-open-source-rag-end-to-end.md)

आगामी:

- उसी RAG सिस्टम को Azure AI Search और Azure OpenAI के साथ पुनर्निर्माण करें।
- डेमो उत्तर के परे मूल्यांकन और प्रतिगमन जांच जोड़ें।

## नोटबुक

कार्यान्वयन लेख नोटबुक्स का उपयोग करते हैं ताकि पुनर्प्राप्ति और मूल्यांकन चरणों को सीधे निरीक्षित किया जा सके। फोल्डर-स्तर मार्गदर्शन के लिए देखें [notebooks/README.md](./notebooks/README.md)।

> [!TIP]
> यदि आप सबसे तेज़ मार्ग चाहते हैं तो श्रृंखला 2 से शुरू करें। यह नमूना डेटा, CPU-फ्रेंडली एम्बेडिंग्स, Qdrant स्थानीय मोड, और बिना क्लाउड प्रमाणपत्रों के स्थानीय रूप से चलता है।

| श्रृंखला | नोटबुक | आवश्यकताएँ | स्थानीय सत्यापन |
| --- | --- | --- | --- |
| श्रृंखला 2 | [ओपन-सोर्स RAG नोटबुक](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant स्थानीय मोड, पुनर्प्राप्ति, पुनः रैंकिंग, और स्रोत वायरिंग सत्यापित |

स्थानीय रूप से नोटबुक चलाने के लिए, एक वर्चुअल वातावरण बनाएं और मिलते-जुलते आवश्यकताएँ फ़ाइल स्थापित करें। उदाहरण के लिए:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## नमूना डेटा

नोटबुक्स [sample_data](../../sample_data) में एक छोटा स्थानीय कॉर्पस उपयोग करते हैं ताकि उदाहरण निजी दस्तावेज़ों या क्लाउड प्रमाणपत्रों के बिना चल सके। विवरण के लिए देखें [sample_data/README.md](./sample_data/README.md)।

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## स्थानीय सत्यापन सारांश

सत्यापन परिणाम प्रत्येक लेख में और [SERIES_PLAN.md](./SERIES_PLAN.md) में रिकॉर्ड किए गए हैं।

| क्षेत्र | परिणाम |
| --- | --- |
| श्रृंखला 2 ओपन-सोर्स पथ | FastEmbed द्वारा 384-आयामी स्थानीय एम्बेडिंग जनरेट हुई, Qdrant इन-मेमोरी संग्रह में 8 वेक्टर डाले गए, हल्की पुनः रैंकिंग ने अपेक्षित अनुभाग पुनः प्राप्त किया; वैकल्पिक Ollama जनरेशन `phi4-mini:3.8b` के साथ पूरा हुआ |

स्थानीय नोटबुक जानबूझकर हार्डकोडेड सीक्रेट्स से बचता है।

## स्थानीय Ollama जनरेशन

श्रृंखला 2 नोटबुक डिफ़ॉल्ट रूप से स्थानीय-सुरक्षित है। स्थानीय Ollama जनरेशन सक्षम करने के लिए, [.env.example](../../.env.example) को `.env` में कॉपी करें और श्रृंखला 2 के मान भरें।

श्रृंखला 2 Ollama जनरेशन के लिए, अनकॉमेंट करें:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

श्रृंखला 2 नोटबुक स्वतः ही रिपोजिटरी रूट से `.env` को `python-dotenv` का उपयोग करके लोड करता है।

> [!IMPORTANT]
> `.env` फाइल, API कुंजी, निजी एंडपॉइंट, या टेनेंट-विशिष्ट मान कमिट न करें। रिपोजिटरी जानबूझकर Markdown फाइलों और नोटबुक्स से गुप्त जानकारी बाहर रखता है।

आवश्यकताएँ फ़ाइलें [requirements/README.md](./requirements/README.md) में प्रलेखित हैं।

लिंक, नोटबुक संरचना, नोटबुक आउटपुट की सफाई, और उच्च-जोखिम वाले गुप्त पैटर्नों को सत्यापित करने के लिए:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

सत्यापन स्क्रिप्ट [scripts/README.md](./scripts/README.md) में प्रलेखित हैं।

सभी स्थानीय-सुरक्षित नोटबुक्स को एक ही वातावरण में चलाने के लिए:

```powershell
python scripts\verify_notebooks.py --execute
```

वहीं सत्यापन फ़्लो GitHub Actions में पुश, पुल अनुरोध, और मैन्युअल वर्कफ़्लो डिस्पैच पर चलता है। ड्राफ्ट लेख और नोटबुक्स जानबूझकर सार्वजनिक सत्यापन पथ से बाहर रखे गए हैं।

अपडेट प्रकाशित करने से पहले, [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) का उपयोग करें।

वर्तमान अप्रकाशित परिवर्तन सारांश के लिए देखें [CHANGELOG.md](./CHANGELOG.md)।

योगदान और नोटबुक सफाई दिशानिर्देशों के लिए देखें [CONTRIBUTING.md](./CONTRIBUTING.md)।

## बहुभाषी समर्थन

### Co-op Translator द्वारा समर्थित (स्वचालित और हमेशा अपडेटेड)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](./README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानीय रूप से क्लोन करना पसंद है?**
>
> यह रिपोजिटरी 50+ भाषा अनुवाद शामिल करता है जो डाउनलोड आकार को काफी बढ़ा देता है। अनुवादों के बिना क्लोन करने के लिए sparse checkout का उपयोग करें:
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
> यह आपको कोर्स पूरा करने के लिए आवश्यक सब कुछ देगा, लेकिन बहुत तेज डाउनलोड के साथ।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
इस दस्तावेज़ का अनुवाद AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->