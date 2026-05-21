# आपके दस्तावेज़ों के आधार पर प्रश्नों का उत्तर देने के लिए AI को सिखाएं

यह रिपॉजिटरी 2026 की एक ब्लॉग श्रृंखला को संग्रहित करती है जो RAG, Azure AI सेवाओं, ओपन-सोर्स विकल्पों, और मूल्यांकन-केंद्रित वर्कफ़्लो के साथ दस्तावेज़-आधारित AI सिस्टम बनाने के बारे में है।

## पृष्ठभूमि

2023 में, मैंने Azure AI Search और Azure OpenAI का उपयोग करके PDF दस्तावेज़ों से प्रश्नों का उत्तर देने के लिए ChatGPT को सिखाने पर दो ट्यूटोरियल बनाए। "अपने डेटा पर ChatGPT" का विचार तब भी नया था, और उद्देश्य एक व्यावहारिक वर्कफ़्लो दिखाना था: दस्तावेज़ संग्रहीत करना, उन्हें अनुक्रमित करना, प्रासंगिक सामग्री को पुनः प्राप्त करना, और उस पुनः प्राप्त संदर्भ से उत्तर उत्पन्न करना।

2026 में, RAG पारिस्थितिकी तंत्र काफी बड़ा हो गया है। Azure AI Search आधुनिक वेक्टर और हाइब्रिड पुनः प्राप्ति पैटर्न का समर्थन करता है, Azure OpenAI व्यापक Microsoft Foundry Models पारिस्थितिकी तंत्र का हिस्सा है, और LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, और vLLM जैसे ओपन-सोर्स टूल वास्तविक सिस्टमों के लिए व्यावहारिक विकल्प बन गए हैं।

इसीलिए मैं इस विषय को फिर से देखना चाहता था। अब सवाल केवल "मैं RAG कैसे बनाऊं?" नहीं है। अब इसे बनाने के कई तरीके हैं, और सबसे महत्वपूर्ण सवाल यह है कि "मेरी स्थिति के लिए कौन सा आर्किटेक्चर चुनना चाहिए?"

यह श्रृंखला उस निर्णय-निर्माण लेयर से शुरू होती है। कार्यान्वयन में गहराई से जाने से पहले, यह देखती है कि AI सेवाओं को पुनः प्राप्ति क्यों आवश्यक है, कब Azure आधारित प्रबंधित सेवाएं मायने रखती हैं, कब ओपन-सोर्स विकल्प बेहतर होते हैं, और फाइन-ट्यूनिंग कहां फिट होती है।

## लेख

1. [श्रृंखला 1: RAG, Azure बनाम ओपन-सोर्स विकल्प, और कब फाइन-ट्यूनिंग उपयुक्त है](./series-1-rag-azure-open-source-fine-tuning.md)

## बहुभाषी समर्थन

### को-ऑप ट्रांसलेटर के माध्यम से समर्थित (स्वचालित और हमेशा अद्यतित)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](./README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानीय रूप से क्लोन करना पसंद करते हैं?**
>
> इस रिपॉजिटरी में 50+ भाषा अनुवाद शामिल हैं जो डाउनलोड आकार को काफी बढ़ा देते हैं। अनुवादों के बिना क्लोन करने के लिए, sparse checkout का उपयोग करें:
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
> यह आपको कोर्स पूरा करने के लिए आवश्यक सभी सामग्री तेजी से डाउनलोड करने देता है।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
इस दस्तावेज़ का अनुवाद AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->