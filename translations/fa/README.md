# آموزش هوش مصنوعی برای پاسخ به سوالات بر اساس اسناد شما

این مخزن مجموعه‌ای از یک سری بلاگ‌های سال ۲۰۲۶ درباره ساخت سیستم‌های هوش مصنوعی مبتنی بر اسناد با RAG، خدمات هوش مصنوعی آزور، جایگزین‌های متن‌باز و جریان‌های کاری مبتنی بر ارزیابی است.

## پیش‌زمینه

در سال ۲۰۲۳، من روی دو آموزش در مورد آموزش ChatGPT برای پاسخ به سوالات از اسناد PDF با استفاده از Azure AI Search و Azure OpenAI کار کردم. ایده «ChatGPT روی داده‌های شما» آن زمان هنوز نو بود و هدف نمایش یک جریان کاری عملی بود: ذخیره اسناد، فهرست‌بندی آنها، بازیابی محتوای مرتبط و تولید پاسخ از آن متن بازیابی‌شده.

در سال ۲۰۲۶، اکوسیستم RAG بسیار بزرگتر شده است. Azure AI Search الگوهای بازیابی برداری و ترکیبی مدرن را پشتیبانی می‌کند، Azure OpenAI بخشی از اکوسیستم گسترده‌تر مدل‌های Foundry مایکروسافت است و ابزارهای متن‌باز مانند LangGraph، LlamaIndex، Haystack، Qdrant، Milvus، Weaviate، Chroma، Ollama و vLLM به انتخاب‌هایی عملی برای سیستم‌های واقعی تبدیل شده‌اند.

به همین دلیل خواستم دوباره به این موضوع بپردازم. سؤال دیگر فقط «چگونه RAG بسازم؟» نیست. حالا راه‌های متعددی برای ساخت آن وجود دارد و سؤال مهم‌تر این است که «کدام معماری برای شرایط من مناسب‌تر است؟»

این سری از همان لایه تصمیم‌گیری آغاز می‌شود. پیش از رفتن به عمق پیاده‌سازی، به این می‌پردازد که چرا خدمات هوش مصنوعی به بازیابی نیاز دارند، کی خدمات مدیریت شده مبتنی بر آزور منطقی است، کی جایگزین‌های متن‌باز مناسب‌ترند و جایی که آموزش دقیق جای می‌گیرد.

## مقالات

۱. [سری ۱: RAG، آزور در مقابل جایگزین‌های متن‌باز، و زمانی که آموزش دقیق معنادار است](./series-1-rag-azure-open-source-fine-tuning.md)

## پشتیبانی چندزبانه

### پشتیبانی شده توسط مترجم همکار (خودکار و همیشه به‌روز)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](./README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ترجیح می‌دهید به صورت محلی کلون کنید؟**
>
> این مخزن شامل بیش از ۵۰ ترجمه زبان است که به طور قابل توجهی حجم دانلود را افزایش می‌دهد. برای کلون بدون ترجمه‌ها از sparse checkout استفاده کنید:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (ویندوز):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> این به شما همه چیز لازم برای گذراندن دوره با دانلود بسیار سریع‌تر را می‌دهد.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان مادری خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما در قبال هرگونه سوء تفاهم یا برداشت نادرست ناشی از استفاده از این ترجمه مسئولیتی نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->