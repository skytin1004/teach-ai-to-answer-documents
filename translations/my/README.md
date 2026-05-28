# သင့်စာရွက်စာတမ်းများအခြေခံပြီး AI ကိုမေးခွန်းများကိုဖြေဆိုရန်သင်ကြားပါ

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

ဒီ repository မှာ 2026 ခုနှစ်တွင် RAG၊ Azure AI ဝန်ဆောင်မှုများ၊ open-source နည်းလမ်းများနှင့် အကဲဖြတ်မှုနှင့်ဆိုင်သော workflow များဖြင့် စာရွက်စာတမ်းမှ AI စနစ်များကိုတည်ဆောက်ခြင်းအကြောင်း 2026 ခုနှစ် blog စီးရီးကိုစုစုပေါင်းထားသည်။

## အခင်းအကျမ်း

2023 ခုနှစ်တွင်၊ မင်းက ChatGPT ကို Azure AI Search နှင့် Azure OpenAI ကိုသုံးဆွဲ၍ PDF စာရွက်များမှ မေးခွန်းများကို ဖြေဆိုခြင်း သင်ကြားပေးသည့် tutorial နှစ်ခုအပေါ် လုပ်ခဲ့သည်။ "သင်၏ဒေတာအပေါ် ChatGPT" ဆိုသောအယူအဆသည် အဲဒီအချိန်မှာ မကြာသေးသေးသောအရာ ဖြစ်သလို၊ ရည်ရွယ်ချက်မှာ လက်တွေ့ အသုံးပြုနိုင်သည့် workflow ကိုပြသခြင်းဖြစ်သည်။ စာရွက်စာတမ်းများကို သိမ်းဆည်းပြီး၊ ဒါတွေကို indexing လုပ်ပြီး၊ သင့်တော်သော အကြောင်းအရာများကို ရယူပြီး၊ ရယူထားသောအကြောင်းအရာမှ ဖြေချင်သော ဖြေကြားချက်ကို အဆင့်ဆင့်ဖန်တီးခြင်း ဖြစ်သည်။

2026 ခုနှစ်တွင် RAG ဒီဇိုင်းစနစ်များပို၍ ကျယ်ပြန့်သွားသည်။ Azure AI Search မှ  စနစ်အသစ်များဖြစ်သည့် ကျောတင်ပြီး ရွေးချယ်ထုတ်ယူမှု ပုံစံများကို ထောက်ပံ့ပေးသည်၊ Azure OpenAI သည် Microsoft Foundry Models ပိုင်းဆိုင်ရာ ecosystem ၏ တစ်စိတ်တစ်ပိုင်းဖြစ်ပြီး၊ LangGraph၊ LlamaIndex၊ Haystack၊ Qdrant၊ Milvus၊ Weaviate၊ Chroma၊ Ollama နှင့် vLLM ကဲ့သို့သော open-source tools များသည် အမှန်တကယ် အသုံးပြုလို့ရသော ရွေးချယ်မှုများဖြစ်လာသည်။

ဒါကြောင့် ဤခေါင်းစဉ်ကို ထပ်မံလေ့လာလိုခဲ့သည်။ မေးခွန်းမှာ "RAG ကို လုပ်ဆောင်သည့် အကြောင်းအရာ ဘယ်လိုလုပ်မလဲ" ဟူသော တည့်တည့်မဟုတ်တော့ပါ။ အခုတော့ RAG ကို တည်ဆောက်နည်းစုံများ ရှိပြီး၊ အရေးပါတဲ့ မေးခွန်းမှာတော့ "ငါ့ အခြေအနေအတွက် ဘယ် architecture ကို ရွေးချယ်သင့်သလဲ" ဖြစ်လာသည်။

ဒီစီးရီးဟာ ဤဆုံးဖြတ်ချက်အလွှာမှ စတင်ပြီး၊ အလျင်အမြန် လက်တွေ့ လုပ်ဆောင်ရန် tutorial များအဖြစ်ပြောင်းလဲပေးသွားမှာ ဖြစ်သည်။ ပထမဆုံးလုပ်ငန်းအဆင့်မှာ Qdrant, Ollama နှင့် Phi-4-mini တို့ဖြင့် မည်သူမဆို ဆောင်ရွက်နိုင်မည့် ဒေသန္တရ open-source RAG စနစ်တစ်ခုကို တည်ဆောက်ပေးပါမည်။

## ဆောင်းပါးများ

ဆောင်းပါးများ အညွှန်းအတွက် [articles/README.md](./articles/README.md) ကို ကြည့်ပါ။

1. [စီးရီး 1: RAG, Azure နှင့် Open-Source အစားထိုးများ၊ Fine-Tuning မည်သို့သင့်တော်သည်](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [စီးရီး 2: ဒေသန္တရ Open-Source RAG စနစ်တစ်ခု အစမှအဆုံး တည်ဆောက်ခြင်း](./articles/series-2-open-source-rag-end-to-end.md)

လာမည့်အချက်များ -

- Azure AI Search နှင့် Azure OpenAI ဖြင့် တူညီသော RAG စနစ်ကို ထပ်မံတည်ဆောက်မည်။
- မူလဖြေချင်းမှ ပိုမိုတိုးတက်သော အကဲဖြတ်ခြင်းနှင့် regression စစ်ဆေးမှုများ ထည့်သွင်းမည်။

## Notebook များ

လုပ်ဆောင်ချက်ဆောင်းပါးများတွင် notebook များကို အသုံးပြုသည်။ ထို့ကြောင့် ရွေးချယ်ထုတ်ယူခြင်းနှင့် အကဲဖြတ်ခြင်း အဆင့်များကို တိုက်ရိုက် စစ်ဆေးနိုင်ပြီး [notebooks/README.md](./notebooks/README.md) တွင် ဖိုင်ဖွဲ့စည်းမှု လမ်းညွှန်ချက်များကို ကြည့်ရှုနိုင်ပါသည်။

> [!TIP]
> အရှိန်အဟုန်မြန်ဆုံးလမ်းကိုလိုချင်ရင် စီးရီး 2 နဲ့ စတင်ပါ။ ဒေသန္တရ၊ နမူနာဒေတာ၊ CPU လိုအပ်ချက်နည်းသော embedding များ၊ Qdrant ဒေသန္တရ mode နှင့် cloud credentials မလိုအပ်။

| စီးရီး | Notebook | လိုအပ်ချက်များ | ဒေသန္တရ စစ်ဆေးမှု |
| --- | --- | --- | --- |
| စီးရီး 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant ဒေသန္တရ mode, ရွေးချယ်ထုတ်ယူမှု, သတ်မှတ်သည့် ပြန်လည်သုံးသပ်ခြင်းနှင့် ရင်းမြစ် ဆက်သွယ်မှု စစ်ဆေးပြီး |

notebook ကို ဒေသန္တရတွင် ဖွင့်ရန်၊ virtual environment တည်ဆောက်ပြီး လိုက်ဖက်သော ပိုင်းအစိတ်အပိုင်း ဖိုင်များကို 설치လုပ်ပါ။ ဥပမာ -

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## နမူနာဒေတာ

notebook များသည် [sample_data](../../sample_data) ထဲရှိ ဒေသန္တရ corpus သေးငယ်တစ်ခုကိုအသုံးပြုပါသည်။ အထူးအစီအစဉ်များမရှိဘဲ private စာရွက်စာတမ်းများ သို့မဟုတ် cloud ခံယူခွင့်မလိုအပ်ဘဲ အလုပ်လုပ်စေပါသည်။ အသေးစိတ်အချက်အလက်များအတွက် [sample_data/README.md](./sample_data/README.md) ကို ကြည့်ပါ။

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## ဒေသန္တရ စစ်ဆေးမှု အကျဉ်းချုပ်

စစ်ဆေးမှုရလဒ်ကို ဆောင်းပါးတိုင်းတွင် နေရာယူပြီး [SERIES_PLAN.md](./SERIES_PLAN.md) မှာလည်း မှတ်တမ်းတင်ထားသည်။

| နေရာ | ရလဒ် |
| --- | --- |
| စီးရီး 2 open-source လမ်း | FastEmbed ကနေ 384-အတိုင်းအတာ ဒေသန္တရ embedding များ ဖန်တီး၊ Qdrant in-memory collection သို့ 8 vectors ထည့်သွင်းပြီး၊ ပေါ့ပါးတဲ့ reranking က မျှော်မှန်းထားသော အပိုင်းရွေးချယ်မှု ပြီးဆုံးပြီး; ကျွမ်းကျင်သော Ollama ရလဒ်ကို `phi4-mini:3.8b` ဖြင့် ပြီးမြောက်စေသည် |

ဒေသန္တရ notebook မှာ အမှားသုံး စကားဝှက်များ မပါဝင်ရန် ရည်ရွယ်ထားသည်။

## ဒေသန္တရ Ollama ဖန်တီးခြင်း

စီးရီး 2 notebook သည် အလိုအလျောက် ဒေသန္တရ နေရာတွင် လုံခြုံစွာ အလုပ်လုပ်သည်။ ဒေသန္တရ Ollama ဖန်တီးမှုကို အသုံးပြုလိုပါက [.env.example](../../.env.example) ကို `.env` မှာကူးယူပြီး စီးရီး 2 အတွက် အချက်အလက်များဖြည့်စွက်ပါ။

စီးရီး 2 Ollama ဖန်တီးမှုအတွက် အောက်ပါကိစ္စကို remark ပြုလုပ်ပါ-

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

စီးရီး 2 notebook သည် repository ရဲ့ ဒဏ်ရာ root မှ `.env` ကို `python-dotenv` ဖြင့် အလိုအလျောက် ဖတ်ယူသည်။

> [!IMPORTANT]
> `.env` ဖိုင်များ၊ API key များ၊ ကိုယ်ပိုင် endpoint များ သို့မဟုတ် tenant-specific တန်ဖိုးများကို commit မပြုလုပ်ရ။ repository သည် Markdown ဖိုင်များနှင့် notebook များထဲတွင် လျှို့ဝှက်ချက် မပါဝင်အောင် သတိထားသည်။

လိုအပ်ချက် ဖိုင်များကို [requirements/README.md](./requirements/README.md) တွင် မှတ်တမ်းတင်ထားသည်။

link များ၊ notebook ဖွဲ့စည်းမှု၊ notebook အထွက် ထားမှု သန့်ရှင်းမှုနှင့် အန္တရာယ်အလွန်များသော လျှို့ဝှက်ချက် ပုံစံများကို စစ်ဆေးရန် -

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

စစ်ဆေးမှု script များကို [scripts/README.md](./scripts/README.md) တွင် ဖော်ပြထားသည်။

ဒေသန္တရ seguridad အလုပ်လုပ်နိုင်တဲ့ notebooks အားလုံးကို တစ်ပြိုင်နက်မှာ ကြပ်မတ်ရန် -

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions တွင် push, pull request, manual workflow များတွင် ဤသို့စစ်ဆေးမှု တွဲဖက်ကာ ဖွင့်လှစ်ပြီး ဖြစ်သည်။ နမူနာဆောင်းပါးများ၊ notebooks များကို အာမခံဖို့ ရက်စွဲမတင်သေးသော verification လမ်းကြောင်းမှ ဖြုတ်ထားသည်။

အသစ်ထုတ်ဖော်မည့် အချက်အလက်များ အားဖြင့် [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) ကို အသုံးပြုပါ။

လက်ရှိမထုတ်ဝေခင် အပြောင်းအလဲအကျဉ်းကို [CHANGELOG.md](./CHANGELOG.md) မှာ တွေ့နိုင်သည်။

ပါဝင်ဆောင်ရွက်မှုများနှင့် notebook စနစ်သန့်ရှင်းရေးညွှန်ကြားချက်များ အတွက် [CONTRIBUTING.md](./CONTRIBUTING.md) ကို ကြည့်ပါ။

## ဘာသာစကားများ အများအပြား ထောက်ပံ့မှု

### Co-op Translator ဖြင့် ထောက်ပံ့ထား (အလိုအလျောက်နဲ့ ဖော်ပြမှု အမြဲအသစ်ဖြစ်)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](./README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ဒေသန္တရ များကို ကိုယ်တိုင် clone မယ့်သူတွေအတွက်**
>
> ဒီ repository မှာ ဘာသာစကား 50 ကျော်ဖော်ပြထားပြီး ဒါကြောင့် ဒေါင်းလုပ် အရွယ်အစား တိုးလာပါတယ်။ ဘာသာပြန်ချက်တွေမပါဘဲ clone လုပ်ချင်ရင် sparse checkout ကိုသုံးပါ။
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
> ဒါနဲ့ သင်အလိုရှိတဲ့ ဘာသာရပ်များကို အမြန်ဆုံးပြီးစီးနိုင်ပါတယ်။
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ပြောကြားချက်**
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းနေသော်လည်း၊ စက်ကိရိယာဘာသာပြန်ခြင်းများတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် လိုအပ်ပါသည်။ မူလစာတမ်းကို မူရင်းဘာသာဖြင့်သာ ယုံကြည်စိတ်ချရသော အချက်အလက်အဖြစ် သတ်မှတ်သင့်သည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုကွာခြားမှုများ သို့မဟုတ် မမှန်ကန်သော အသုံးပြုမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မခံပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->