# Notebooks

ဤ notebooks များသည် အဆောင်းအရာစီးရီးနှင့်အတူ ပြေးနိုင်သော နမူနာများကို ထောက်ပံ့သည်။

| Notebook | ဆောင်းပါး | ရည်ရွယ်ချက် |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | FastEmbed၊ Qdrant ဒေသစီးကွက်၊ ရှာဖွေရေး၊ ပြန်လည်ခေါ်ယူခြင်း၊ ရွေးချယ်မှု Ollama ထုတ်လုပ်မှုနှင့် အရင်းအမြစ် ရည်ညွှန်းချက်များပါဝင်သည့် Open-source RAG |

## ဒေသတွင်းတွင် ပြေးရန်

သင်ပြေးလိုသော notebook အတွက် လိုအပ်ချက်များကို တပ်ဆင်ပါ။

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

သို့မဟုတ် အားလုံးသော လိုအပ်ချက်များကို တပ်ဆင်ပါ။

```powershell
python -m pip install -r requirements\all.txt
```

## အတည်ပြုရန်

repository ရှေ့ဆုံးမှ စ၍ -

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Series 2 သည် repository ရှေ့ဆုံးရှိ `.env` ဖိုင်မှ Ollama ဖွဲ့စည်းတည်ဆောက်မှုကို ဖတ်နိုင်သည်။ series အလိုက် အုပ်စုဖွဲ့ထားသော [../.env.example](../../../.env.example) မှ စတင်ပါ။

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ပြောကြားချက်**
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းနေသော်လည်း၊ စက်ကိရိယာဘာသာပြန်ခြင်းများတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် လိုအပ်ပါသည်။ မူလစာတမ်းကို မူရင်းဘာသာဖြင့်သာ ယုံကြည်စိတ်ချရသော အချက်အလက်အဖြစ် သတ်မှတ်သင့်သည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုကွာခြားမှုများ သို့မဟုတ် မမှန်ကန်သော အသုံးပြုမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မခံပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->