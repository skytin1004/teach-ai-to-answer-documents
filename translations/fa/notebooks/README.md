# دفترچه‌های یادداشت

این دفترچه‌های یادداشت از مجموعه مقاله‌ها با مثال‌های قابل اجرا پشتیبانی می‌کنند.

| دفترچه یادداشت | مقاله | هدف |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [سری ۲](../articles/series-2-open-source-rag-end-to-end.md) | RAG متن باز با FastEmbed، حالت محلی Qdrant، بازیابی، رتبه‌بندی مجدد، تولید اختیاری Ollama، و مراجع به منابع |

## اجرای محلی

وابستگی‌های مورد نیاز دفترچه‌ای که می‌خواهید اجرا کنید را نصب کنید:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

یا همه وابستگی‌ها را نصب کنید:

```powershell
python -m pip install -r requirements\all.txt
```

## تایید

از ریشه مخزن:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

سری ۲ می‌تواند پیکربندی Ollama را از فایل `.env` در ریشه مخزن بخواند. از [../.env.example](../../../.env.example) شروع کنید که بر اساس سری‌ها گروه‌بندی شده است.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان مادری خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما در قبال هرگونه سوء تفاهم یا برداشت نادرست ناشی از استفاده از این ترجمه مسئولیتی نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->