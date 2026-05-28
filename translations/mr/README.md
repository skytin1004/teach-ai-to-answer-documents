# आपल्या दस्तऐवजांच्या आधारे प्रश्नांची उत्तरे देण्यासाठी AI शिका

![दस्तऐवज-आधारित AI RAG प्रणालीचा आढावा](../../assets/images/readme-hero.svg)

हा रेपॉझिटरी RAG, Azure AI सेवा, मुक्त स्त्रोत पर्याय आणि मुल्यांकन-केंद्रित कार्यप्रवाहांसह दस्तऐवज-आधारित AI प्रणाली तयार करण्याबाबत 2026 मधील ब्लॉग मालिकाचं संकलन करतो.

## पार्श्वभूमी

2023 मध्ये, मी Azure AI Search आणि Azure OpenAI वापरून PDF दस्तऐवजांमधून प्रश्नांना उत्तरे देण्यासाठी ChatGPT शिकवण्याबाबत दोन ट्युटोरियल्सवर काम केले. "ChatGPT आपल्या डेटावर" ही कल्पना तेव्हा अजून नव्याने वाटत होती, आणि उद्देश एक व्यावहारिक कार्यप्रवाह दाखवायचा होता: दस्तऐवज संग्रहित करा, त्यांचे अनुक्रमण करा, संबंधित सामग्री मिळवा, आणि प्राप्त केलेल्या संदर्भातून उत्तरे तयार करा.

2026 मध्ये, RAG पर्यावरण खूप मोठे झाले आहे. Azure AI Search आधुनिक वेक्टर आणि संकरित पुनर्प्राप्ती पद्धतींना समर्थन देतो, Azure OpenAI ही Microsoft Foundry Models च्या विस्तृत पर्यावरणाचा भाग आहे, आणि LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama आणि vLLM सारखी मुक्त स्त्रोत उपकरणे खऱ्या प्रणालींसाठी व्यावहारिक पर्याय बनली आहेत.

म्हणूनच मला हा विषय पुन्हा पाहायचा होता. प्रश्न आता फक्त "मी RAG कसा तयार करू?" एवढाच नाही. आता ती तयार करण्याचे अनेक मार्ग आहेत, आणि आणखी महत्त्वाचा प्रश्न असा आहे "माझ्या परिस्थितीसाठी कोणती आर्किटेक्चर निवडावी?"

ही मालिका त्या निर्णय-निर्मितीच्या स्तरापासून सुरू होते, नंतर तिला हाताळण्यासाठी ट्युटोरियलमध्ये रूपांतरित करते. पहिला अंमलबजावणी मार्ग स्थानिक मुक्त स्त्रोत RAG प्रणाली तयार करतो ज्याला कोणीही नमुना डेटासह, Qdrant, Ollama, आणि Phi-4-mini वापरून चालवू शकते.

## लेख

लेख निर्देशिका पाहण्यासाठी [articles/README.md](./articles/README.md) पहा.

1. [मालिका 1: RAG, Azure विरुद्ध मुक्त स्त्रोत पर्याय, आणि जेव्हा फाईन-ट्यूनिंगला अर्थ असतो](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [मालिका 2: स्थानिक मुक्त स्त्रोत RAG प्रणाली संपूर्णपणे तयार करा](./articles/series-2-open-source-rag-end-to-end.md)

पुढे येत आहे:

- Azure AI Search आणि Azure OpenAI वापरून त्याच RAG प्रणालीचे पुनर्निर्माण करा.
- डेमो उत्तरांपलीकडील मुल्यांकन आणि विघटन तपासणी जोडा.

## नोटबुक्स

अंमलबजावणी लेखांसाठी नोटबुक्स वापरल्या आहेत ज्यामुळे पुनर्प्राप्ती आणि मुल्यांकन टप्पे थेट तपासता येतील. फोल्डर-स्तरीय मार्गदर्शनासाठी [notebooks/README.md](./notebooks/README.md) पहा.

> [!TIP]
> सर्वात जलद मार्ग हवा असल्यास मालिका 2 पासून सुरू करा. ही प्रणाली स्थानिकरित्या नमुना डेटासह, CPU-लायक एम्बेडिंग्जसह, Qdrant स्थानिक मोडमधील, आणि कोणत्याही क्लाउड क्रेडेन्शियलशिवाय चालते.

| मालिका | नोटबुक | आवश्यकता | स्थानिक पडताळणी |
| --- | --- | --- | --- |
| मालिका 2 | [मुक्त स्त्रोत RAG नोटबुक](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant स्थानिक मोड, पुनर्प्राप्ती, पुनर्रँकिंग आणि स्रोत वायरिंग पडताळलेले |

स्थानिक नोटबुक चालवण्यासाठी, एक व्हर्च्युअल पर्यावरण तयार करा आणि जुळणा-या आवश्यकता फाइल इन्स्टॉल करा. उदाहरणार्थ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## नमुना डेटा

नोटबुक्स एका लहान स्थानिक संग्रहणाचा वापर करतात जो [sample_data](../../sample_data) मध्ये आहे, त्यामुळे उदाहरणे खासगी दस्तऐवज किंवा क्लाउड क्रेडेन्शियलशिवाय चालू शकतात. तपशिलांसाठी [sample_data/README.md](./sample_data/README.md) पहा.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## स्थानिक पडताळणी सारांश

पडताळणी निकाल प्रत्येक लेखात आणि [SERIES_PLAN.md](./SERIES_PLAN.md) मध्ये नोंदवलेले आहेत.

| विभाग | निकाल |
| --- | --- |
| मालिका 2 मुक्त स्त्रोत मार्ग | FastEmbed ने 384-आयामी स्थानिक एम्बेडिंग तयार केली, Qdrant इन्मेमरी संग्रहात 8 वेक्टर घातले, हलकी पुनर्रँकिंग अपेक्षित विभाग आणली; ऐच्छिक Ollama जनरेशन `phi4-mini:3.8b` सह पूर्ण झाले |

स्थानिक नोटबुक जाणूनबुजून हार्डकोड केलेली गुपिते टाळतो.

## स्थानिक Ollama निर्मिती

मालिका 2 नोटबुक डिफॉल्टनुसार स्थानिक सुरक्षित आहे. स्थानिक Ollama निर्मिती सक्षम करण्यासाठी, [.env.example](../../.env.example) ला `.env` म्हणून कॉपी करा आणि मालिका 2 चे मूल्य भरा.

मालिका 2 Ollama निर्मितीसाठी, अनकमेंट करा:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

मालिका 2 नोटबुक आपोआप रेपॉझिटरी रूट मधून `.env` `python-dotenv` वापरून लोड करतो.

> [!IMPORTANT]
> `.env` फाइल्स, API कीज, खासगी एंडपॉइंट्स, किंवा टेनेन्ट-विशिष्ट मूल्ये कमिट करू नका. रेपॉझिटरी जाणूनबुजून Markdown फाइल्स आणि नोटबुक्स मधून गुपिते दूर ठेवते.

आवश्यकतांची फायली [requirements/README.md](./requirements/README.md) मध्ये दस्तऐवजीकृत आहेत.

लिंक्स, नोटबुक संरचना, नोटबुक आउटपुट स्वच्छता, आणि उच्च-धोकादायक गुपित नमुन्यांची तपासणी करण्यासाठी:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

पडताळणी स्क्रिप्ट्स [scripts/README.md](./scripts/README.md) मध्ये दस्तऐवजीकृत आहेत.

सर्व स्थानिक सुरक्षित नोटबुक एकाच पर्यावरणात चालवण्यासाठी:

```powershell
python scripts\verify_notebooks.py --execute
```

तीच पडताळणी प्रक्रिया GitHub Actions मध्ये पुश, पुल रिक्वेस्ट आणि मॅन्युअल वर्कफ्लो डिस्पॅचवर चालते. इष्टतम लेख आणि नोटबुक्स जानूनबुजून सार्वजनिक पडताळणी मार्गातून वगळलेले आहेत.

अपडेट प्रकाशित करण्यापूर्वी [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) वापरा.

सद्य: अप्रकाशित बदलांचा सारांश [CHANGELOG.md](./CHANGELOG.md) मध्ये पहा.

योगदान देणे व नोटबुक स्वच्छतेच्या मार्गदर्शकांसाठी [CONTRIBUTING.md](./CONTRIBUTING.md) पहा.

## बहुभाषिक समर्थन

### सहकार ट्रान्सलेटरने समर्थित (स्वयंचलित व नेहमी अद्ययावत)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](./README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानिक क्लोन करायचा प्राधान्य आहे का?**
>
> हा रेपॉझिटरी ५०+ भाषा अनुवादांसह येतो ज्यामुळे डाउनलोड आकार मोठा होतो. फक्त कोर्स पूर्ण करण्यासाठी अनुवादांशिवाय क्लोन करण्यासाठी sparse checkout वापरा:
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
> हे आपल्याला कोर्स पूर्ण करण्यासाठी भव्य वेगाने डाउनलोड देतो.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून अनुवादित केला आहे. जरी आम्ही अचूकतेसाठी प्रयत्न करतो, तरी कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या मूळ भाषेत अधिकृत स्रोत मानला पाहिजे. महत्त्वाची माहिती असल्यास, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थलावणीसाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->