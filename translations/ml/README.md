# നിങ്ങളുടെ ഡോക്യുമെന്റുകളുടെ അടിസ്ഥാനത്തിൽ ചോദ്യങ്ങൾക്ക് ഉത്തരം നൽകാൻ AI-നെ പഠിപ്പിക്കുക

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

ഈ റിപ്പോസിറ്ററി ഡോക്യുമെന്റ്-അധിഷ്ഠിത AI സംവിധാനങ്ങൾ RAG, Azure AI സർവീസുകൾ, ഓപ്പൺ-സോഴ്‌സ് ആൽട്ടർനേറ്റീവുകൾ, വിലയിരുത്തൽമുഖപ്പെട്ട വർക്ക്‌ഫ്ലോകൾ എന്നിവ ഉപയോഗിച്ച് നിർമ്മിക്കുന്നതിനെ കുറിച്ചുള്ള 2026 ബ്ലോഗ് പരമ്പര ശേഖരിക്കുന്നു.

## പശ്ചാത്തലം

2023-ൽ, ഞാൻ Azure AI Search-ഉം Azure OpenAI-ഉം ഉപയോഗിച്ച് PDF ഡോക്യുമെന്റുകളിൽ നിന്നുള്ള ചോദ്യങ്ങൾക്ക് ChatGPT-നെ മറുപടി നൽകാൻ പഠിപ്പിക്കുന്ന കുറെ ട്യൂട്ടോറിയലുകൾ തയ്യാറാക്കി. "നിങ്ങളുടെ ഡേറ്റയിൽ ChatGPT" എന്ന ആശയം അപ്പോൾ പുതിയതായി തോന്നിയിരുന്നു, ലക്ഷ്യം പ്രായോഗിക ഒരു വർക്ക്‌ഫ്ലോ കാണിച്ചതായിരുന്നു: ഡോക്യുമെന്റുകൾ സംഭരിക്കുക, അവ ഇൻഡക്സ് ചെയ്യുക, ബന്ധപ്പെട്ട ഉള്ളടക്കം തിരിച്ചു കിട്ടുക, അതിലെ контекстിൽ നിന്നുള്ള മറുപടി സൃഷ്ടിക്കുക.

2026-നോട്, RAG ഇക്കോസിസ്റ്റം വളരെ വലുതായി വളർന്നു. Azure AI Search ആധുനിക വെക്റ്റർ, ഹൈബ്രിഡ് റിട്രീവൽ മാതൃകകൾ പിന്തുണയ്‌ക്കുന്നു, Azure OpenAI മാസ്തിരോഫ്റ്റ് Fosundry Models ഇക്കോസിസ്റ്റത്തിന്റെ ഭാഗമാണ്, LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, vLLM പോലുള്ള ഓപ്പൺ-സോഴ്‌സ് ഉപകരണങ്ങൾ യാഥാർത്ഥ്യ സംവിധാനങ്ങൾക്ക് പ്രായോഗികമായ തിരഞ്ഞെടുപ്പുകൾ ആയി മാറിയിട്ടുണ്ട്.

അതിനാൽ ഈ വിഷയം വീണ്ടും പരിശോധിക്കാൻ ഞാൻ ആഗ്രഹിച്ചു. ചോദ്യമിനോ ഇനി "എങ്ങനെ RAG നിർമ്മിക്കാം?" മാത്രമല്ല. ഇതിനെ നിർമ്മിക്കാൻ നൂറു വഴികളുണ്ട്, ഇതിലൂടെ "എന്ത് ആർക്കിടെക്ചർ എന്റെ സാഹചര്യത്തിനു ഏറ്റവും അനുയോജ്യമാണ്?" എന്നതാണു ഏറ്റവും പ്രധാനപ്പെട്ട ചോദ്യം.

ഈ പരമ്പരം ആ തീരുമാനമെടുക്കൽ ഘട്ടത്തിൽ നിന്നാണ് ആരംഭിക്കുന്നത്, തുടർന്ന് ആദ്ധ്യാപനപരമായ ട്യൂട്ടോറിയലുകളാക്കി മാറ്റുന്നു. ആദ്യം പ്രവർത്തന വഴിപാടാണ് ആരും സാമ്പിൾ ഡാറ്റ ഉപയോഗിച്ച് Qdrant, Ollama, Phi-4-mini ഉപയോഗിച്ച് ഓപ്പൺ-സോഴ്‌സ് RAG സിസ്റ്റം ലൊക്കലായി പ്രവർത്തിപ്പിക്കാം.

## ലേഖനങ്ങൾ

ലേഖന സൂപ്രധാനത്തിന് [articles/README.md](./articles/README.md) കാണുക.

1. [പരമ്പരം 1: RAG, Azure vs ഓപ്പൺ-സോഴ്‌സ് ആൽട്ടർനേറ്റീവുകൾ, ഫൈൻ-ട്യൂണിംഗ് എപ്പോഴാണ് പ്രായോഗികം](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [പരമ്പരം 2: ഒരു ലൊക്കൽ ഓപ്പൺ-സോഴ്‌സ് RAG സിസ്റ്റം തുടക്കം മുതൽ അവസാനം വരെ നിർമ്മിക്കൽ](./articles/series-2-open-source-rag-end-to-end.md)

അടുത്തതായി വരുന്നത്:

- Azure AI Search-ഉം Azure OpenAI-ഉം ഉപയോഗിച്ച് അതേ RAG സിസ്റ്റം പുനർനിർമ്മിക്കുക.
- ഡെമോ മറുപടിയിൽ മുകളിൽ വിലയിരുത്തലും റിഗ്രഷൻ പരിശോധനകളും ചേർക്കുക.

## നോട്ട്‌ബുക്കുകൾ

പ്രവർത്തന ലേഖനങ്ങൾ നോട്ട്‌ബുക്കുകൾ ഉപയോഗിക്കുന്നു, അതുകൊണ്ട് റിട്രീവൽ, വിലയിരുത്തൽ ഘട്ടങ്ങൾ നേരിട്ട് പരിശോധിക്കാം. ഫോൾഡർ-ലെവൽ മാർഗ്ഗദർശനത്തിന് [notebooks/README.md](./notebooks/README.md) കാണുക.

> [!TIP]
> ഏറ്റവും വേഗത്തിൽ എത്താൻ പരമ്പരം 2 ആരംഭിക്കുക. ഇത് ലൊക്കലായി സാമ്പിൾ ഡാറ്റ, CPU-സൗഹൃദ എംബെഡ്ഡിംഗ്സ്, Qdrant ലൊക്കൽ മോഡ് എന്നിവ ഉപയോഗിച്ച് പ്രവർത്തിക്കുന്നു; ക്ലൗഡ് ക്രെഡൻഷ്യലുകൾ വേണ്ട.

| പരമ്പരം | നോട്ട്‌ബുക്ക് | ആവശ്യകതകൾ | ലൊക്കൽ പരിശോധന |
| --- | --- | --- | --- |
| പരമ്പരം 2 | [ഓപ്പൺ-സോഴ്‌സ് RAG നോട്ട്‌ബുക്ക്](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant ലൊക്കൽ മോഡ്, റിട്രീവൽ, റീ-റാങ്കിങ്ങ്, സോഴ്സ് വയറിംഗ് പരിശോധിച്ചു |

ലൊക്കലായി നോട്ട്‌ബുക്ക് പ്രവർത്തിപ്പിക്കാൻ, ഒരു വെർച്ച്വൽ എൻവയോൺമെന്റ് സൃഷ്ടിച്ച് അവയ്ക്ക് ആവശ്യമായ ഫയൽ ഇൻസ്റ്റാൾ ചെയ്യുക. ഉദാഹരണത്തിന്:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## സാമ്പിൾ ഡാറ്റ

നോട്ട്‌ബുക്കുകൾ [sample_data](../../sample_data) എന്ന ചെറിയ ലൊക്കൽ കോർപ്പസ് ഉപയോഗിക്കുന്നു, അതിനാൽ ഉദാഹരണങ്ങൾ സ്വകാര്യ ഡോക്യുമെന്റുകളും ക്ലൗഡ് ക്രെഡൻഷ്യലുകളും വേണ്ടാതെ പ്രവർത്തിക്കും. വിശദാംശങ്ങൾക്ക് [sample_data/README.md](./sample_data/README.md) കാണുക.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## ലൊക്കൽ പരിശോധന സമാരി

പരിശോധനാ ഫലങ്ങൾ ഓരോ ലേഖനത്തിലും [SERIES_PLAN.md](./SERIES_PLAN.md) ൽ രേഖപ്പെടുത്തുന്നു.

| മേഖല | ഫലം |
| --- | --- |
| പരമ്പരം 2 ഓപ്പൺ-സോഴ്‌സ് വഴി | FastEmbed ഉപയോഗിച്ച് 384-ഡൈമെൻഷൻ ലൊക്കൽ എംബെഡ്ഡിങ്സ് സൃഷ്ടിച്ചു, Qdrant ഇൻ-മെമ്മറി കൂട്ടത്തിൽ 8 വെക്റ്ററുകൾ ചേർത്തു, ലൈറ്റ്‌വെയിറ്റ് റീ-റാങ്കിങ്ങ് പ്രതീക്ഷിച്ച സെക്ഷൻ തിരിച്ച് നൽകി; ഓപ്ഷണൽ Ollama ജനरेशन `phi4-mini:3.8b` ഉപയോഗിച്ച് പൂർത്തിയായി |

ലൊക്കൽ നോട്ട്‌ബുക്ക് ഹാർഡ്‌കോഡു ചെയ്ത രഹസ്യങ്ങൾ അറിയാതെ ഡീസൈൻ ചെയ്തിരിക്കുന്നു.

## ലൊക്കൽ Ollama ജനറേഷൻ

പരമ്പരം 2 നോട്ട്‌ബുക്ക് ലൊക്കൽ-സേഫ് ആയി ഡিফോൾട്ടാണ്. ലൊക്കൽ Ollama ജനറേഷൻ സാധ്യമാക്കാൻ [.env.example](../../.env.example) ജാൾ `.env` ആയി കോപ്പി ചെയ്ത് പരമ്പരം 2 വാല്യൂസ് പൂരിപ്പിക്കുക.

പരമ്പരം 2 Ollama ജനറേഷൻ പ്രവർത്തിപ്പിക്കാൻ, പ്രതിഷേധിക്കുക:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

പരമ്പരം 2 നോട്ട്‌ബുക്ക് റിപോസിറ്ററി റൂട്ട് മാർഗ്ഗം നിൽക്കുന്നതായി `python-dotenv` ഉപയോഗിച്ച് `.env` സ്വയം ലോഡു ചെയ്യും.

> [!IMPORTANT]
> `.env` ഫയലുകൾ, API കീകൾ, സ്വകാര്യ എൻഡ്പോയിന്റുകൾ, ടെന്നന്റ്-സ്പെസിഫിക് വാല്യൂകൾ നൽകാതെ വച്ചോളൂ. Markdown ഫയലുകളിലും നോട്ട്‌ബുക്കുകളിലും രഹസ്യങ്ങൾ മാറ്റിവയ്ക്കാതിരിക്കാൻ repositories കർശനമാണ്.

ആവശ്യകത ഫയലുകൾ [requirements/README.md](./requirements/README.md) ൽ രേഖപ്പെടുത്തിയിരിക്കുന്നു.

ലിങ്കുകൾ, നോട്ട്‌ബുക്ക് ഘടന, നോട്ട്‌ബുക്ക് ഔട്ട്പുട്ടിന്റെ ശുചിത്വം, ഉയർന്ന അപകടമുള്ള രഹസ്യ മാതൃകകൾ പരിശോധിക്കാൻ:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

പരിശോധനാ സ്ക്രിപ്റ്റുകൾ [scripts/README.md](./scripts/README.md) ൽ രേഖപ്പെടുത്തിയിരിക്കുന്നു.

അല്ലെങ്കിൽ ലോകൽ-സേഫ് നോട്ട്‌ബുക്കുകൾ ഒരേ എൻവയോൺമെന്റിൽ പ്രവർത്തിപ്പിക്കാൻ:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub ആക്ഷനുകളിൽ പുഷ്, പുൾ റിക്വസ്റ്റ്, മാനുവൽ വർക്ക്‌ഫ്ലോ ഡിസ്പാച്ചുകളിൽ ഈ പരിശോധന പ്രവാഹം പ്രവർത്തിക്കും. ഡ്രാഫ്റ്റ് ലേഖനങ്ങളും നോട്ട്‌ബുക്കുകളും പൊതു പരിശോധന പാതയിൽ ഉൾപ്പെടുത്തിയിട്ടില്ല.

പുതുക്കലുകൾ പുറത്തുവെക്കുന്നതിനു മുമ്പ് [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) ഉപയോഗിക്കുക.

ഇപ്പോഴുള്ള പ്രസിദ്ധീകരിക്കാത്ത മാറ്റങ്ങളുടെ സംക്ഷേപം കാണാൻ [CHANGELOG.md](./CHANGELOG.md) കാണുക.

കോണ്ട്രിബ്യൂഷൻ, നോട്ട്‌ബുക്ക് ശുചിത്വ മാർഗ്ഗരേഖകൾക്കായി [CONTRIBUTING.md](./CONTRIBUTING.md) കാണുക.

## ബഹുഭാഷാ പിന്തുണ

### Co-op Translator ഉപയോഗിച്ച് (ഓട്ടോമേറ്റഡ്, എല്ലായ്പ്പോഴും അപ്‌ടുഡേറ്റ് ഉണ്ട്)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](./README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **പ്രിയം, ലോക്കലായി ക്ലോൺ ചെയ്യാൻ ആഗ്രഹിക്കുന്നുണ്ടോ?**
>
> ഈ റിപ്പോസിറ്ററിയിൽ 50+ ഭാഷാ വിവർത്തനങ്ങൾ ഉൾക്കൊള്ളുന്നതാണ്, ഇതുവഴി ഡൗൺലോഡ് വലുതാകും. വിവർത്തനങ്ങൾ ഇല്ലാതെ ക്ലോൺ ചെയ്യാൻ സ്പാർസ് ചെക്ക്ഔട്ട് ഉപയോഗിക്കുക:
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
> കോഴ്സ് പൂർത്തിയാക്കാനായി ആവശ്യമുള്ള എല്ലാം വളരെ വേഗം ഡൗൺലോഡ് ചെയ്യപ്പെടും.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**അറിയിപ്പ്**:
ഈ രേഖ AI പരിഭാഷാ സേവനം [Co-op Translator](https://github.com/Azure/co-op-translator) ഉപയോഗിച്ച് പരിഭാഷപ്പെടുത്തിയതാണ്. ഞങ്ങൾ കൃത്യതയ്ക്കായി ശ്രമിക്കുന്നുവെങ്കിലും, ഓട്ടോമേറ്റഡ് പരിഭാഷകളിൽ പിഴവുകൾ അല്ലെങ്കിൽ തെറ്റായ വിവരങ്ങൾ ഉണ്ടാകാൻ സാധ്യതയുണ്ട്. അതിന്റെ സ്വാഭാവിക ഭാഷയിലുള്ള അസൽ രേഖയാണ് പ്രാമാണികമായ ഉറവിടമായി പരിഗണിക്കേണ്ടത്. നിർണായകമായ വിവരങ്ങൾക്ക്, പ്രൊഫഷണൽ മനുഷ്യ പരിഭാഷ ശുപാർശ ചെയ്യുന്നു. ഈ പരിഭാഷ ഉപയോഗിച്ച് ഉണ്ടാകുന്ന തെറ്റിദ്ധാരണകൾ അല്ലെങ്കിൽ തെറ്റായ വ്യാഖ്യാനങ്ങൾക്കായി ഞങ്ങൾ ഉത്തരവാദികളല്ല.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->