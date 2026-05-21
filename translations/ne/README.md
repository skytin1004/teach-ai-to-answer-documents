# तपाईंको कागजातहरूमा आधार गरि प्रश्नहरूको उत्तर दिन AI सिकाउनुहोस्

यो रिपोजिटरीले RAG, Azure AI सेवाहरू, खुला स्रोत विकल्पहरू, र मूल्यांकन-केंद्रित कार्यप्रवाहहरू सहित कागजात-आधारित AI प्रणालीहरू निर्माण गर्ने सम्बन्धी २०२६ को एक ब्लग श्रृंखला सङ्कलन गरेको छ।

## पृष्ठभूमि

सन् २०२३ मा, मैले Azure AI Search र Azure OpenAI प्रयोग गरी PDF कागजातहरूबाट प्रश्नहरूको उत्तर दिने तरिका सिकाउने दुई ट्युटोरियलहरूमा काम गरेको थिएँ। "तपाईंको डेटामा ChatGPT" को कुरा त्यो बेला अझै नयाँ जस्तो लाग्थ्यो, र लक्ष्य एउटा व्यावहारिक कार्यप्रवाह देखाउनु थियो: कागजातहरू संग्रह गर्नु, तिनीहरूलाई अनुक्रमणिका बनाउनु, सान्दर्भिक सामग्री पुनःप्राप्त गर्नु, र पुनःप्राप्त सन्दर्भबाट उत्तर उत्पादन गर्नु।

सन् २०२६ मा, RAG इकोसिस्टम धेरै ठूलो भइसकेको छ। Azure AI Search ले आधुनिक भेक्टर र हाइब्रिड पुनःप्राप्ति नमूनाहरूलाई समर्थन गर्छ, Azure OpenAI माइक्रोसफ्ट फाउन्ड्री मोडेलहरू इकोसिस्टमको भाग हो, र खुला स्रोत उपकरणहरू जस्तै LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, र vLLM वास्तविक प्रणालीहरूको लागि व्यवहार्य विकल्पहरू बनेका छन्।

त्यसैले मैले यो विषयमा पुनः विचार गर्न चाहन्थेँ। अब प्रश्न मात्र "म RAG कसरी बनाउने?" होइन। अब धेरै तरिकाहरू छन्, र सबैभन्दा महत्वपूर्ण प्रश्न छ "मेरो परिस्थितिका लागि कुन आर्किटेक्चर छनोट गर्ने?"

यो श्रृंखला त्यो निर्णय-लेयरबाट सुरु हुन्छ। कार्यान्वयनमा गहिराइमा जानुअघि, यसले किन AI सेवाहरूलाई पुनःप्राप्ति आवश्यक हुन्छ, कहिले Azure आधारित प्रबन्धित सेवाहरू उपयुक्त हुन्छन्, कहिले खुला स्रोत विकल्पहरू राम्रो हुन्छन्, र फाइन-ट्यूनिङ कहाँ फिट हुन्छ हेर्छ।

## लेखहरू

१. [श्रृंखला १: RAG, Azure र खुला स्रोत विकल्पहरू, र कहिले फाइन-ट्यूनिङ उपयुक्त हुन्छ](./series-1-rag-azure-open-source-fine-tuning.md)

## बहुभाषिक समर्थन

### Co-op Translator मार्फत समर्थन (स्वचालित र सधैं अद्यावधिक)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](./README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानीय रूपमा क्लोन गर्न मन छ?**
>
> यस रिपोजिटरीमा ५०+ भाषा अनुवादहरू समावेश छन् जसले डाउनलोड साइज धेरै बढाउँछ। अनुवादहरू बिना क्लोन गर्न, sparse checkout प्रयोग गर्नुहोस्:
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
> यसले तपाईंलाई छिटो डाउनलोड गरेर कोर्स पूरा गर्न आवश्यक सबै कुरा दिन्छ।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी सही हुन प्रयास गर्छौं, तर कृपया जानकार हुनुस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छन्। मूल दस्तावेज़ यसको मूल भाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलत बुझाइ वा त्रुटिको लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->