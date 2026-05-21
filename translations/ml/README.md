# നിങ്ങളുടെ ഡോക്യുമെന്റുകൾ അടിസ്ഥാനമാക്കി ചോദ്യങ്ങൾക്ക് മറുപടി പറയാൻ AIയെ শেখിക്കുക

ഈ റിപോസിറ്ററി 2026-ലെ ഒരു ബ്ലോഗ് സീരീസിനെ ശേഖരിക്കുന്നു, RAG, അസ്യൂർ AI സേവനങ്ങൾ, ഓപ്പൺ സോഴ്‌സ് പ്രത്യയോക്താക്കൾ, വിലയിരുത്തൽ-കേന്ദ്രമായ പ്രവൃത്തിപദ്ധതികൾ ഉപയോഗിച്ച് ഡോക്യുമെൻറ്-നിര്‍മ്മിത AI സിസ്റ്റങ്ങൾ നിർമ്മിക്കുന്നതിനെക്കുറിച്ചുള്ളത്.

## പശ്ചാത്തലം

2023-ൽ, ഞാൻ PDF ഡോക്യുമെന്റുകളിൽ നിന്നുള്ള ചോദ്യങ്ങൾക്ക് Azure AI Search, Azure OpenAI എന്നിവ ഉപയോഗിച്ച് ChatGPTക്കു പഠിപ്പിക്കുന്നതെക്കുറിച്ചുള്ള രണ്ട് ട്യൂട്ടോറിയലുകളിലേയ്ക്ക് ജോലി ചെയ്തു. "നിങ്ങളുടെ ഡാറ്റയിൽ ChatGPT" എന്ന 아이디어 ആ സമയത്ത് പുതിയതായി തോന്നിയിരുന്നു, പ്രായോഗിക പ്രവൃത്തിപദ്ധതി കാണിക്കുന്നതായിരുന്നു ലക്ഷ്യം: ഡോക്യുമെന്റുകൾ സൂക്ഷിക്കുക, അവ ഇൻഡക്സ് ചെയ്യുക, അനുയോജ്യമായ ഉള്ളടക്കം തിരിച്ച് കണ്ടെത്തുക, ആ തിരഞ്ഞെടുത്ത പരിസരം ഉപയോഗിച്ചു മറുപടികൾ സൃഷ്ടിക്കുക.

2026-ൽ RAG പരിസ്ഥിതിയാണ് വളരെക് വലുത്. അസ്യൂർ AI Search ആധുനിക വെക്ടർ ആൻഡ് ഹൈബ്രിഡ് റിട്ട്രീവൽ പാറ്റേണുകളെ പിന്തുണയ്ക്കുന്നു, അസ്യൂർ OpenAI ബൃഹദ്മൈക്രോസോഫ്‌റ്റ് ഫോണ്ട്രി മോഡലുകൾ പരിസ്ഥിതിയുടെ ഭാഗമാണ്, LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, vLLM പോലുള്ള ഓപ്പൺ സോഴ്‌സ് ഉപകരണങ്ങൾ യഥാർത്ഥ സിസ്റ്റങ്ങളിലേക്ക് പ്രായോഗിക തിരഞ്ഞെടുപ്പുകൾ ആയി മാറിയിട്ടുണ്ട്.

അതിനാലാണ് ഈ വിഷയത്തിന് വീണ്ടുംigirതി നൽകേണ്ടതുണ്ടെന്ന് ഞാൻ കരുതിയത്. ചോദ്യം ഇനി "ഞാൻ എങ്ങനെ RAG നിർമ്മിക്കും?" മാത്രം അല്ല. ഇപ്പോൾ ഇത് നിർമ്മിക്കാൻ നിരവധി മാർഗ്ഗങ്ങൾ ഉണ്ട്, ഏറ്റവും പ്രധാനപ്പെട്ട ചോദ്യം "എനിക്ക് അനുയോജ്യമായ ഈ ഘടന ഏതാണെന്ന് എങ്ങനെ തിരഞ്ഞെടുക്കണം?" എന്നാണ്.

ഈ സീരിസ് ആ തീരുമാനമെടുക്കൽ പാളിയിൽ നിന്നാണ് ആരംഭിക്കുന്നത്. ആഴത്തിൽ നടപ്പിലാക്കുന്നതിന് മുമ്പ്, AI സേവനങ്ങൾക്ക് റിട്രീവലിന്റെ ആവശ്യം എന്തുകൊണ്ട് ഉണ്ടാകുന്നു, അസ്യൂർ അടിസ്ഥാനമാക്കിയ മാനേജ് ചെയ്ത സേവനങ്ങൾ എപ്പോൾ സഹജമാണ്, ഓപ്പൺ സോഴ്‌സ് പ്രത്യായോക്താക്കൾ എപ്പോഴാണ് വലിയ അനുയോജ്യമായത്, ഫൈൻ-ട്യൂണിംഗ് എവിടെയൊക്കെയാണ് കൂടിപ്പോകുന്നത് എന്നവയെ നോക്കുന്നു.

## ലേഖനങ്ങൾ

1. [സീരീസ് 1: RAG, അസ്യൂർ vs ഓപ്പൺ-സോഴ്‌സ് പ്രത്യായോക്താക്കൾ, ഫൈൻ-ട്യൂണിംഗ് എപ്പോൾ ഉപകാരപ്രദമാണ്](./series-1-rag-azure-open-source-fine-tuning.md)

## ബഹുഭാഷാ പിന്തുണ

### കോ-ഓപ് ട്രാൻസ്ലേറ്റർ വഴിയുള്ള പിന്തുണ (സ്വয়മാറ്റവും എപ്പോഴും അപ്-ടു-ഡേറ്റ്)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](./README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **പ്രാദേശികമായി ക്ലോൺ ചെയ്യാൻ ആഗ്രഹിക്കുന്നുണ്ടോ?**
>
> ഈ റിപോസിറ്ററിയിൽ 50+ ഭാഷാ പരിഭാഷകൾ ഉൾപ്പെടുത്തിയിട്ടുണ്ട്, ഇത് ഡൗൺലോഡ് വലിപ്പം ഗണ്യമായി വർദ്ധിപ്പിക്കുന്നു. പരിഭാഷകൾ കൂടാതെ ക്ലോൺ ചെയ്യാൻ sparse checkout ഉപയോഗിക്കുക:
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
> ഇത് കോഴ്സ് പൂർത്തിയാക്കാനുള്ള എല്ലാ പ്രത്യാശകളും നിങ്ങൾക്കു much വേഗത്തിലുള്ള ഡൗൺലോഡോടെ നൽകുന്നു.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**അറിയിപ്പ്**:
ഈ രേഖ AI പരിഭാഷാ സേവനം [Co-op Translator](https://github.com/Azure/co-op-translator) ഉപയോഗിച്ച് പരിഭാഷപ്പെടുത്തിയതാണ്. ഞങ്ങൾ കൃത്യതയ്ക്കായി ശ്രമിക്കുന്നുവെങ്കിലും, ഓട്ടോമേറ്റഡ് പരിഭാഷകളിൽ പിഴവുകൾ അല്ലെങ്കിൽ തെറ്റായ വിവരങ്ങൾ ഉണ്ടാകാൻ സാധ്യതയുണ്ട്. അതിന്റെ സ്വാഭാവിക ഭാഷയിലുള്ള അസൽ രേഖയാണ് പ്രാമാണികമായ ഉറവിടമായി പരിഗണിക്കേണ്ടത്. നിർണായകമായ വിവരങ്ങൾക്ക്, പ്രൊഫഷണൽ മനുഷ്യ പരിഭാഷ ശുപാർശ ചെയ്യുന്നു. ഈ പരിഭാഷ ഉപയോഗിച്ച് ഉണ്ടാകുന്ന തെറ്റിദ്ധാരണകൾ അല്ലെങ്കിൽ തെറ്റായ വ്യാഖ്യാനങ്ങൾക്കായി ഞങ്ങൾ ഉത്തരവാദികളല്ല.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->