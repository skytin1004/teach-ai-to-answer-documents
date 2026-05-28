# نوٹ بکس

یہ نوٹ بکس مضمون سیریز کی حمایت کرتے ہیں جن میں چلانے کے قابل مثالیں شامل ہیں۔

| نوٹ بک | مضمون | مقصد |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [سیریز 2](../articles/series-2-open-source-rag-end-to-end.md) | اوپن سورس RAG بشمول FastEmbed، Qdrant لوکل موڈ، بازیافت، دوبارہ درجہ بندی، اختیاری Ollama جنریشن، اور ماخذ حوالہ جات |

## مقامی طور پر چلائیں

اس نوٹ بک کے لیے ضروریات نصب کریں جسے آپ چلانا چاہتے ہیں:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

یا تمام انحصارات انسٹال کریں:

```powershell
python -m pip install -r requirements\all.txt
```

## تصدیق کریں

رپوزٹری کی جڑ سے:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

سیریز 2 Ollama کی ترتیب رپوزٹری کی جڑ میں `.env` فائل سے پڑھ سکتی ہے۔ [../.env.example](../../../.env.example) سے شروع کریں، جو سیریز کے لحاظ سے گروپ کی گئی ہے۔

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->