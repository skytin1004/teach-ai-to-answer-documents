# اپنی دستاویزات کی بنیاد پر سوالات کے جواب دینے کے لیے AI کو تربیت دیں

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

یہ ریپوزیٹری 2026 کے بلاگ سیریز کو جمع کرتی ہے جو RAG، Azure AI سروسز، اوپن سورس متبادلات، اور جائزہ لینے والے ورک فلو کے ذریعے دستاویز پر مبنی AI سسٹمز بنانے کے بارے میں ہے۔

## پس منظر

2023 میں، میں نے Azure AI سرچ اور Azure OpenAI استعمال کرتے ہوئے PDF دستاویزات سے سوالات کے جواب دینے کے لیے ChatGPT کو تربیت دینے کے بارے میں دو ٹیوٹوریلز پر کام کیا۔ "آپ کے ڈیٹا پر ChatGPT" کا خیال تب بھی نیا محسوس ہوتا تھا، اور مقصد ایک عملی ورک فلو دکھانا تھا: دستاویزات ذخیرہ کریں، انڈیکس کریں، متعلقہ مواد بازیافت کریں، اور بازیافت شدہ سیاق و سباق سے جوابات تیار کریں۔

2026 میں، RAG ایکو سسٹم بہت بڑا ہو چکا ہے۔ Azure AI سرچ جدید ویکٹر اور ہائبرڈ بازیافت کے پیٹرنز کی حمایت کرتا ہے، Azure OpenAI مائیکروسافٹ Foundry ماڈلز کے وسیع تر ایکو سسٹم کا حصہ ہے، اور LangGraph، LlamaIndex، Haystack، Qdrant، Milvus، Weaviate، Chroma، Ollama، اور vLLM جیسے اوپن سورس ٹولز حقیقت پسندانہ نظاموں کے لیے عملی انتخاب بن چکے ہیں۔

اسی وجہ سے میں نے اس موضوع کو دوبارہ دیکھنے کی خواہش کی۔ اب سوال صرف "میں RAG کیسے بناؤں؟" نہیں رہا۔ اب اسے بنانے کے کئی طریقے ہیں، اور اہم سوال یہ ہے "میرے حالات کے لیے کونسی ساخت منتخب کرنی چاہیے؟"

یہ سیریز اس فیصلہ سازی کی پرت سے شروع ہوتی ہے، پھر اسے عملی ٹیوٹوریلز میں تبدیل کرتی ہے۔ پہلی امپلیمنٹیشن راستہ ایک مقامی اوپن سورس RAG نظام بناتا ہے جسے کوئی بھی نمونہ ڈیٹا، Qdrant، Ollama، اور Phi-4-mini کے ساتھ چلا سکتا ہے۔

## مضامین

مضمون کی فہرست کے لیے دیکھیں [articles/README.md](./articles/README.md)۔

1. [سیریز 1: RAG، Azure بمقابلہ اوپن سورس متبادل، اور جب فائن-ٹیوننگ معنی رکھتی ہے](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [سیریز 2: ایک مقامی اوپن سورس RAG نظام ابتدا سے آخر تک بنائیں](./articles/series-2-open-source-rag-end-to-end.md)

آنے والا:

- وہی RAG نظام Azure AI سرچ اور Azure OpenAI کے ساتھ دوبارہ بنائیں۔
- ایک ڈیمو جواب سے آگے جائزہ اور ریگریشن چیکس شامل کریں۔

## نوٹ بکس

عمل درآمد مضامین نوٹ بکس استعمال کرتے ہیں تاکہ بازیافت اور جائزہ مراحل کو براہ راست جانچا جا سکے۔ فولڈر سطح کی رہنمائی کے لیے دیکھیں [notebooks/README.md](./notebooks/README.md)۔

> [!TIP]
> اگر آپ تیز ترین راستہ چاہتے ہیں تو سیریز 2 سے شروع کریں۔ یہ مقامی طور پر نمونہ ڈیٹا، CPU دوستانہ ایمبیڈنگز، Qdrant مقامی موڈ، اور کوئی کلاؤڈ اسناد کے بغیر چلتا ہے۔

| سیریز | نوٹ بک | ضروریات | مقامی تصدیق |
| --- | --- | --- | --- |
| سیریز 2 | [اوپن سورس RAG نوٹ بک](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant مقامی موڈ، بازیافت، ری رینکنگ، اور ماخذ وائرنگ کی تصدیق شدہ |

نوٹ بک مقامی طور پر چلانے کے لیے، ایک ورچوئل ماحول بنائیں اور مماثل ضروریات فائل انسٹال کریں۔ مثال کے طور پر:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## نمونہ ڈیٹا

نوٹ بکس ایک چھوٹے مقامی مجموعہ [sample_data](../../sample_data) میں استعمال کرتے ہیں تاکہ مثالیں نجی دستاویزات یا کلاؤڈ اسناد کے بغیر چل سکیں۔ تفصیلات کے لیے دیکھیں [sample_data/README.md](./sample_data/README.md)۔

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## مقامی تصدیق کا خلاصہ

تصدیق کے نتائج ہر مضمون اور [SERIES_PLAN.md](./SERIES_PLAN.md) میں ریکارڈ کیے جاتے ہیں۔

| علاقہ | نتیجہ |
| --- | --- |
| سیریز 2 اوپن سورس راستہ | FastEmbed نے 384-بعد کا مقامی ایمبیڈنگ تیار کیا، Qdrant نے میموری میں 8 ویکٹرز کا مجموعہ شامل کیا، ہلکی پھلکی ری رینکنگ نے متوقع سیکشن بازیافت کیا؛ اختیاری Ollama جنریشن `phi4-mini:3.8b` کے ساتھ مکمل ہوا |

مقامی نوٹ بک جان بوجھ کر ہارڈ کوڈڈ رازوں سے بچتی ہے۔

## مقامی Ollama جنریشن

سیریز 2 نوٹ بک بذات خود مقامی محفوظ ہے۔ مقامی Ollama جنریشن کو فعال کرنے کے لیے، [.env.example](../../.env.example) کو `.env` میں کاپی کریں اور سیریز 2 کے اقدار بھریں۔

سیریز 2 Ollama جنریشن کے لیے، ان کومنٹ کریں:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

سیریز 2 نوٹ بک خود بخود `python-dotenv` استعمال کرکے مخزن کی جڑ سے `.env` لوڈ کرتی ہے۔

> [!IMPORTANT]
> `.env` فائلز، API کیز، نجی اینڈ پوائنٹس، یا مخصوص کرایہ دار کی قدریں کمیٹ نہ کریں۔ ریپوزیٹری جان بوجھ کر رازوں کو Markdown فائلز اور نوٹ بکس سے باہر رکھتی ہے۔

ضروریات کی فائلیں [requirements/README.md](./requirements/README.md) میں دستاویزی ہیں۔

لنکس کی جانچ پڑتال، نوٹ بک کی ساخت، نوٹ بک کی صفائی، اور خطرناک رازوں کے پیٹرنز کی تصدیق کے لیے:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

تصدیقی اسکرپٹس [scripts/README.md](./scripts/README.md) میں دستاویزی ہیں۔

تمام مقامی محفوظ نوٹ بکس کو ایک ہی ماحول میں چلانے کے لیے:

```powershell
python scripts\verify_notebooks.py --execute
```

وہی تصدیقی عمل GitHub Actions میں pushes، pull requests، اور دستی ورک فلو dispatches پر چلتا ہے۔ مسودہ مضامین اور نوٹ بکس جان بوجھ کر عوامی تصدیقی راستے سے خارج کیے گئے ہیں۔

اپ ڈیٹس شائع کرنے سے پہلے [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) استعمال کریں۔

موجودہ غیر شائع شدہ تبدیلی کا خلاصہ [CHANGELOG.md](./CHANGELOG.md) میں دیکھیں۔

حصہ داری اور نوٹ بک صفائی کی رہنمائی کے لیے دیکھیں [CONTRIBUTING.md](./CONTRIBUTING.md)۔

## کثیراللسانی سپورٹ

### Co-op Translator کے ذریعے سپورٹ شدہ (خودکار اور ہمیشہ تازہ ترین)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](./README.md) | [Vietnamese](../vi/README.md)

> **ترجیح ہے کہ مقامی طور پر کلون کریں؟**
>
> یہ ریپوزیٹری 50+ زبانوں کے تراجم شامل کرتی ہے جو ڈاؤن لوڈ سائز کو بہت بڑھا دیتی ہے۔ تراجم کے بغیر کلون کرنے کے لیے sparse checkout استعمال کریں:
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
> اس سے آپ کو کورس مکمل کرنے کے لیے سب کچھ مل جائے گا، اور ڈاؤن لوڈ بہت تیز ہوگا۔
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->