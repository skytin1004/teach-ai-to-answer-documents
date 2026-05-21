# اپنی دستاویزات کی بنیاد پر سوالات کے جوابات دینے کے لیے AI کو تربیت دیں

یہ مخزن 2026 کی ایک بلاگ سیریز جمع کرتا ہے جو RAG، Azure AI خدمات، اوپن سورس متبادلات، اور جائزہ مرکوز ورک فلو کے ساتھ دستاویز پر مبنی AI نظام بنانے کے بارے میں ہے۔

## پس منظر

2023 میں، میں نے ChatGPT کو PDF دستاویزات سے سوالات کے جواب دینے کی تربیت دینے کے بارے میں Azure AI Search اور Azure OpenAI کا استعمال کرتے ہوئے دو ٹیوٹوریلز پر کام کیا۔ "آپ کے ڈیٹا پر ChatGPT" کا تصور اس وقت ابھی نیا محسوس ہوتا تھا، اور مقصد ایک عملی ورک فلو دکھانا تھا: دستاویزات کو اسٹور کریں، ان کا انڈیکس بنائیں، متعلقہ مواد بازیافت کریں، اور اس بازیافت شدہ سیاق و سباق سے جوابات تیار کریں۔

2026 میں، RAG ماحولیاتی نظام بہت بڑا ہو چکا ہے۔ Azure AI Search جدید ویکٹر اور ہائبرڈ بازیافت کے نمونوں کی حمایت کرتا ہے، Azure OpenAI مائیکروسافٹ Foundry Models کے وسیع تر ماحولیاتی نظام کا حصہ ہے، اور اوپن سورس ٹولز جیسے LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, اور vLLM حقیقی نظاموں کے لیے عملی انتخاب بن چکے ہیں۔

اسی لیے میں نے اس موضوع کو دوبارہ دیکھنے کا ارادہ کیا۔ سوال اب صرف "میں RAG کیسے بناؤں؟" نہیں رہا۔ اب اسے بنانے کے بہت سے طریقے ہیں، اور اہم سوال یہ ہے کہ "میرے حالات کے لیے کون سا فن تعمیر منتخب کروں؟"

یہ سیریز اس فیصلہ سازی کی پرت سے شروع ہوتی ہے۔ نفاذ میں گہرائی میں جانے سے پہلے، یہ دیکھتی ہے کہ AI خدمات کو بازیافت کیوں درکار ہے، کب Azure پر مبنی منظم خدمات معنی رکھتی ہیں، کب اوپن سورس متبادلات بہتر ہیں، اور جہاں fine-tuning کی جگہ ہے۔

## مضامین

1. [سیریز 1: RAG، Azure بمقابلہ اوپن سورس متبادلات، اور کب فائن ٹیوننگ معنی رکھتی ہے](./series-1-rag-azure-open-source-fine-tuning.md)

## کثیراللسانی سپورٹ

### Co-op Translator کے ذریعے سپورٹ کیا گیا (خودکار اور ہمیشہ تازہ ترین)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](./README.md) | [Vietnamese](../vi/README.md)

> **کیا آپ مقامی طور پر کلون کرنا پسند کریں گے؟**
>
> اس مخزن میں 50+ زبانوں کے تراجم شامل ہیں جو ڈاؤن لوڈ سائز کو نمایاں طور پر بڑھاتے ہیں۔ بغیر تراجم کے کلون کرنے کے لیے sparse checkout استعمال کریں:
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
> یہ آپ کو کورس مکمل کرنے کے لیے ضروری تمام کچھ فراہم کرتا ہے بہت تیز تر ڈاؤن لوڈ کے ساتھ۔
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->