# دفاتر الملاحظات

تدعم هذه الدفاتر سلسلة المقالات مع أمثلة قابلة للتشغيل.

| دفتر الملاحظات | المقال | الغرض |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [السلسلة 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG مفتوح المصدر مع FastEmbed، وضع Qdrant المحلي، الاسترجاع، إعادة الترتيب، التوليد الاختياري باستخدام Ollama، ومراجع المصدر |

## التشغيل محليًا

قم بتثبيت المتطلبات لدفتر الملاحظات الذي تريد تشغيله:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

أو قم بتثبيت جميع التبعيات:

```powershell
python -m pip install -r requirements\all.txt
```

## التحقق

من جذر المستودع:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

يمكن للسلسلة 2 قراءة تكوين Ollama من ملف `.env` في جذر المستودع. ابدأ من [../.env.example](../../../.env.example)، والذي يتم تنظيمه حسب السلسلة.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**تنويه**:
تمت ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والمعتمد. للمعلومات الهامة، يُنصح بالاستعانة بترجمة بشرية محترفة. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->