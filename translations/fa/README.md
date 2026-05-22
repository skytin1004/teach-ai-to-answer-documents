# آموزش هوش مصنوعی برای پاسخ به سوالات بر اساس اسناد شما

![نمای کلی سیستم هوش مصنوعی مبتنی بر سند RAG](../../assets/images/readme-hero.svg)

این مخزن مجموعه‌ای از سری مقالات سال ۲۰۲۶ درباره ساخت سیستم‌های هوش مصنوعی مبتنی بر سند با RAG، سرویس‌های Azure AI، جایگزین‌های متن‌باز و گردش‌های کاری ارزیابی‌محور را جمع‌آوری می‌کند.

## پیش‌زمینه

در سال ۲۰۲۳، کاری روی دو آموزش درباره آموزش ChatGPT برای پاسخ به سوالات از اسناد PDF با استفاده از Azure AI Search و Azure OpenAI انجام دادم. ایده «ChatGPT روی داده‌های شما» هنوز تازه به نظر می‌رسید و هدف نمایش یک گردش کاری عملی بود: ذخیره اسناد، نمایه‌سازی آنها، بازیابی محتوای مرتبط و تولید پاسخ از متن بازیابی‌شده.

در سال ۲۰۲۶، اکوسیستم RAG بسیار بزرگ‌تر شده است. Azure AI Search از الگوهای بازیابی مدرن برداری و ترکیبی پشتیبانی می‌کند، Azure OpenAI بخشی از اکوسیستم گسترده‌تر مدل‌های Microsoft Foundry است، و ابزارهای متن‌باز مانند LangGraph، LlamaIndex، Haystack، Qdrant، Milvus، Weaviate، Chroma، Ollama و vLLM به گزینه‌های عملی برای سیستم‌های واقعی تبدیل شده‌اند.

به همین دلیل خواستم دوباره به این موضوع بپردازم. سوال دیگر فقط «چگونه RAG بسازم؟» نیست. حالا راه‌های زیادی برای ساخت آن وجود دارد و سوال مهم‌تر این است که «کدام معماری برای شرایط من مناسب است؟»

این سری از لایه تصمیم‌گیری شروع می‌کند و سپس آن را به آموزش‌های عملی تبدیل می‌کند. مسیر پیاده‌سازی اول یک سیستم RAG متن‌باز محلی می‌سازد که هر کسی می‌تواند با داده نمونه، Qdrant، Ollama و Phi-4-mini اجرا کند.

## مقالات

برای فهرست مقالات به [articles/README.md](./articles/README.md) مراجعه کنید.

1. [سری ۱: RAG، Azure در برابر جایگزین‌های متن‌باز، و زمانی که تنظیم دقیق منطقی است](./articles/series-1-rag-azure-open-source-fine-tuning.md)  
2. [سری ۲: ساخت سیستم RAG متن‌باز محلی از ابتدا تا انتها](./articles/series-2-open-source-rag-end-to-end.md)

مقرره‌های بعدی:  

- بازسازی همان سیستم RAG با Azure AI Search و Azure OpenAI.  
- افزودن بررسی‌های ارزیابی و رگرسیون فراتر از پاسخ نمایشی.

## دفترچه یادداشت‌ها

مقالات پیاده‌سازی از دفترچه یادداشت‌ها استفاده می‌کنند تا مراحل بازیابی و ارزیابی به‌صورت مستقیم قابل بررسی باشند. راهنمایی سطح پوشه را در [notebooks/README.md](./notebooks/README.md) ببینید.

> [!TIP]
> اگر دنبال سریع‌ترین مسیر هستید، از سری ۲ شروع کنید. این سری به صورت محلی با داده نمونه، جاسازی‌های سازگار با CPU، حالت محلی Qdrant و بدون نیاز به اعتبارنامه‌های ابری اجرا می‌شود.

| سری | دفترچه یادداشت | نیازمندی‌ها | تایید محلی |
| --- | --- | --- | --- |
| سری ۲ | [دفترچه یادداشت RAG متن‌باز](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | حالت محلی Qdrant، بازیابی، رتبه‌بندی مجدد و اتصال منابع تایید شده است |

برای اجرای یک دفترچه یادداشت به صورت محلی، یک محیط مجازی بسازید و فایل نیازمندی‌های مربوطه را نصب کنید. برای مثال:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```
  
## داده نمونه

دفترچه یادداشت‌ها از یک مجموعه کوچک محلی در [sample_data](../../sample_data) استفاده می‌کنند تا مثال‌ها بتوانند بدون اسناد شخصی یا اعتبارنامه‌های ابری اجرا شوند. جزئیات در [sample_data/README.md](./sample_data/README.md) آمده است.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)  
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)  

## خلاصه تایید محلی

نتایج تایید در هر مقاله و در [SERIES_PLAN.md](./SERIES_PLAN.md) ثبت شده‌اند.

| حوزه | نتیجه |
| --- | --- |
| مسیر متن‌باز سری ۲ | FastEmbed جاسازی‌های محلی با ۳۸۴ بعد تولید کرد، مجموعه درون‌حافظه‌ای Qdrant هشت بردار وارد کرد، رتبه‌بندی مجدد سبک بخش مورد انتظار را بازیابی کرد؛ تولید اختیاری Ollama با `phi4-mini:3.8b` کامل شد |

دفترچه یادداشت محلی عمداً از رازهای کدگذاری‌شده سخت خودداری می‌کند.

## تولید محلی Ollama

دفترچه یادداشت سری ۲ به طور پیش‌فرض امن برای اجرای محلی است. برای فعال‌سازی تولید محلی Ollama، فایل [.env.example](../../.env.example) را به `.env` کپی کرده و مقادیر سری ۲ را پر کنید.

برای تولید Ollama سری ۲، بخش زیر را فعال کنید:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```
  
دفترچه یادداشت سری ۲ به طور خودکار `.env` را از ریشه مخزن با استفاده از `python-dotenv` بارگذاری می‌کند.

> [!IMPORTANT]
> فایل‌های `.env`، کلیدهای API، نقاط انتهایی خصوصی یا مقادیر منحصر به مستاجر را کامیت نکنید. مخزن عمداً اسرار را از فایل‌های Markdown و دفترچه یادداشت‌ها دور نگه می‌دارد.

فایل‌های نیازمندی در [requirements/README.md](./requirements/README.md) مستند شده‌اند.

برای ارزیابی لینک‌ها، ساختار دفترچه یادداشت، تمیزی خروجی دفترچه یادداشت، و الگوهای رمز عبور با ریسک بالا:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```
  
اسکریپت‌های تایید در [scripts/README.md](./scripts/README.md) مستندسازی شده‌اند.

برای اجرای همه دفترچه یادداشت‌های امن محلی در یک محیط:

```powershell
python scripts\verify_notebooks.py --execute
```
  
همین جریان تایید در GitHub Actions هنگام پوش، درخواست کشش و اجرای دستی گردش کار اجرا می‌شود. مقالات و دفترچه‌های یادداشت پیش‌نویس عمداً از مسیر تایید عمومی حذف شده‌اند.

قبل از انتشار به‌روزرسانی‌ها، از [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) استفاده کنید.

خلاصه تغییرات منتشر نشده فعلی را در [CHANGELOG.md](./CHANGELOG.md) ببینید.

برای دستورالعمل‌های مشارکت و بهداشت دفترچه یادداشت به [CONTRIBUTING.md](./CONTRIBUTING.md) مراجعه کنید.

## پشتیبانی چندزبان

### پشتیبانی شده از طریق مترجم همکار (خودکار و همیشه به‌روز)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[عربی](../ar/README.md) | [بنگالی](../bn/README.md) | [بلغاری](../bg/README.md) | [برمه‌ای (میانمار)](../my/README.md) | [چینی (ساده‌سازی شده)](../zh-CN/README.md) | [چینی (سنتی، هنگ‌کنگ)](../zh-HK/README.md) | [چینی (سنتی، ماکائو)](../zh-MO/README.md) | [چینی (سنتی، تایوان)](../zh-TW/README.md) | [کرواسی](../hr/README.md) | [چکی](../cs/README.md) | [دانمارکی](../da/README.md) | [هلندی](../nl/README.md) | [استونیایی](../et/README.md) | [فنلاندی](../fi/README.md) | [فرانسوی](../fr/README.md) | [آلمانی](../de/README.md) | [یونانی](../el/README.md) | [عبری](../he/README.md) | [هندی](../hi/README.md) | [مجارستانی](../hu/README.md) | [اندونزیایی](../id/README.md) | [ایتالیایی](../it/README.md) | [ژاپنی](../ja/README.md) | [کانادایی](../kn/README.md) | [خمری](../km/README.md) | [کره‌ای](../ko/README.md) | [لیتوانیایی](../lt/README.md) | [مالایی](../ms/README.md) | [مالایالامی](../ml/README.md) | [مراتی](../mr/README.md) | [نپالی](../ne/README.md) | [پیدگین نیجریه‌ای](../pcm/README.md) | [نروژی](../no/README.md) | [فارسی (دری)](./README.md) | [لهستانی](../pl/README.md) | [پرتغالی (برزیل)](../pt-BR/README.md) | [پرتغالی (پرتغال)](../pt-PT/README.md) | [پنجابی (گورموخی)](../pa/README.md) | [رومانیایی](../ro/README.md) | [روسی](../ru/README.md) | [صربی (سیریلیک)](../sr/README.md) | [اسلواک](../sk/README.md) | [اسلوونیایی](../sl/README.md) | [اسپانیایی](../es/README.md) | [سواحیلی](../sw/README.md) | [سوئدی](../sv/README.md) | [تاگالوگ (فیلیپینی)](../tl/README.md) | [تامیل](../ta/README.md) | [تلوگو](../te/README.md) | [تایلندی](../th/README.md) | [ترکی](../tr/README.md) | [اوکراینی](../uk/README.md) | [اردو](../ur/README.md) | [ویتنامی](../vi/README.md)

> **ترجیح می‌دهید به صورت محلی کلون کنید؟**  
>  
> این مخزن بیش از ۵۰ ترجمه زبان دارد که حجم دانلود را به طور قابل توجهی افزایش می‌دهد. برای کلون کردن بدون ترجمه‌ها، از sparse checkout استفاده کنید:  
>  
> **Bash / مک‌اواس / لینوکس:**  
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
> این به شما همه چیز لازم برای تکمیل دوره را با دانلودی بسیار سریع‌تر می‌دهد.  
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان مادری خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما در قبال هرگونه سوء تفاهم یا برداشت نادرست ناشی از استفاده از این ترجمه مسئولیتی نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->