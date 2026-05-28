# علّم الذكاء الاصطناعي الإجابة على الأسئلة بناءً على مستنداتك

![نظرة عامة على نظام RAG القائم على الوثائق للذكاء الاصطناعي](../../assets/images/readme-hero.svg)

يجمع هذا المستودع سلسلة مدونات لعام 2026 حول بناء أنظمة ذكاء اصطناعي قائمة على الوثائق باستخدام RAG، وخدمات Azure AI، والبدائل مفتوحة المصدر، وسير العمل الموجه نحو التقييم.

## الخلفية

في عام 2023، عملت على زوج من البرامج التعليمية حول تعليم ChatGPT الإجابة على الأسئلة من مستندات PDF باستخدام Azure AI Search وAzure OpenAI. كانت فكرة "ChatGPT على بياناتك" لا تزال جديدة آنذاك، وكان الهدف هو عرض سير عمل عملي: تخزين المستندات، فهرستها، استرجاع المحتوى ذي الصلة، وتوليد الإجابات من ذلك السياق المسترجع.

في عام 2026، أصبح نظام RAG أكبر بكثير. يدعم Azure AI Search أنماط الاسترجاع الحديثة القائمة على المتجهات والهجينة، وأصبح Azure OpenAI جزءًا من نظام Microsoft Foundry Models الأوسع، وأدوات المصدر المفتوح مثل LangGraph وLlamaIndex وHaystack وQdrant وMilvus وWeaviate وChroma وOllama وvLLM أصبحت خيارات عملية للأنظمة الحقيقية.

لهذا السبب أردت إعادة زيارة هذا الموضوع. لم يعد السؤال فقط "كيف أبني RAG؟" بل توجد الآن العديد من الطرق لبنائه، والسؤال الأكثر أهمية هو "أي بنية ينبغي أن أختار لحالتي؟"

تبدأ هذه السلسلة من طبقة اتخاذ القرار تلك، ثم تتحول إلى دروس عملية. المسار الأول للتنفيذ يبني نظام RAG مفتوح المصدر محلي يمكن لأي شخص تشغيله باستخدام بيانات نموذجية، Qdrant، Ollama، وPhi-4-mini.

## المقالات

انظر [articles/README.md](./articles/README.md) لفهرس المقالات.

1. [السلسلة 1: RAG، بدائل Azure مقابل مفتوحة المصدر، ومتى يكون الضبط الدقيق منطقيًا](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [السلسلة 2: بناء نظام RAG مفتوح المصدر محلي من البداية إلى النهاية](./articles/series-2-open-source-rag-end-to-end.md)

القادم بعد ذلك:

- إعادة بناء نفس نظام RAG باستخدام Azure AI Search وAzure OpenAI.
- إضافة التقييم وفحوصات الانحدار بالإضافة إلى إجابة العرض التوضيحي.

## دفاتر الملاحظات

تستخدم مقالات التنفيذ دفاتر ملاحظات بحيث يمكن فحص خطوات الاسترجاع والتقييم مباشرة. انظر [notebooks/README.md](./notebooks/README.md) لإرشادات على مستوى المجلد.

> [!TIP]
> ابدأ بالسلسلة 2 إذا أردت المسار الأسرع. تعمل محليًا باستخدام بيانات نموذجية، تضمين صديق للمعالج، وضع Qdrant المحلي، وبدون بيانات اعتماد سحابية.

| السلسلة | دفتر الملاحظات | المتطلبات | التحقق المحلي |
| --- | --- | --- | --- |
| السلسلة 2 | [دفتر ملاحظات RAG مفتوح المصدر](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | تحقق من وضع Qdrant المحلي، الاسترجاع، إعادة الترتيب، وربط المصدر |

لتشغيل دفتر ملاحظات محليًا، أنشئ بيئة افتراضية وثبت ملف المتطلبات المطابق. على سبيل المثال:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## بيانات نموذجية

تستخدم دفاتر الملاحظات مجموعة محلية صغيرة في [sample_data](../../sample_data) حتى يمكن تشغيل الأمثلة بدون مستندات خاصة أو بيانات اعتماد سحابية. انظر [sample_data/README.md](./sample_data/README.md) للتفاصيل.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## ملخص التحقق المحلي

يتم تسجيل نتائج التحقق في كل مقال وفي [SERIES_PLAN.md](./SERIES_PLAN.md).

| المجال | النتيجة |
| --- | --- |
| مسار السلسلة 2 مفتوح المصدر | أنشأ FastEmbed تضمينات محلية بأبعاد 384، وأدرج Qdrant مجموعة في الذاكرة بها 8 متجهات، واسترجع إعادة الترتيب الخفيفة القسم المتوقع؛ وتم الانتهاء اختياريًا من التوليد عبر Ollama مع `phi4-mini:3.8b` |

يتجنب دفتر الملاحظات المحلي عن عمد الأسرار المشفرة الثابتة.

## التوليد المحلي لـ Ollama

دفتر ملاحظات السلسلة 2 آمن محليًا افتراضيًا. لتمكين التوليد المحلي لـ Ollama، انسخ [.env.example](../../.env.example) إلى `.env` واملأ قيم السلسلة 2.

للتوليد عبر Ollama في السلسلة 2، قم بإلغاء تعليق:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

يحمّل دفتر ملاحظات السلسلة 2 `.env` تلقائيًا من جذر المستودع باستخدام `python-dotenv`.

> [!IMPORTANT]
> لا تُخطِر ملفات `.env` أو مفاتيح API أو نقاط النهاية الخاصة أو القيم الخاصة بالمستأجر. يحافظ المستودع عن عمد على سرية المعلومات خارج ملفات Markdown ودفاتر الملاحظات.

تُوثّق ملفات المتطلبات في [requirements/README.md](./requirements/README.md).

للتأكد من الروابط، هيكل دفتر الملاحظات، نظافة إخراج دفتر الملاحظات، ونمط الأسرار عالية الخطورة:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

تُوثّق سكربتات التحقق في [scripts/README.md](./scripts/README.md).

لتنفيذ جميع دفاتر الملاحظات الآمنة محليًا في نفس البيئة:

```powershell
python scripts\verify_notebooks.py --execute
```

يتم تشغيل نفس تدفق التحقق في GitHub Actions عند الدفع، طلبات السحب، وتنفيذ سير العمل يدويًا. تستثنى المقالات ودفاتر الملاحظات المسودة عمدًا من مسار التحقق العام.

قبل نشر التحديثات، استخدم [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

انظر [CHANGELOG.md](./CHANGELOG.md) لملخص التغييرات غير المنشورة الحالية.

لتوجيهات المساهمة ونظافة دفاتر الملاحظات، انظر [CONTRIBUTING.md](./CONTRIBUTING.md).

## دعم لغات متعددة

### مدعوم عبر مترجم التعاونية (آلي ومحدث دائمًا)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[العربية](./README.md) | [البنغالية](../bn/README.md) | [البلغارية](../bg/README.md) | [البرمية (ميانمار)](../my/README.md) | [الصينية (المبسطة)](../zh-CN/README.md) | [الصينية (التقليدية، هونغ كونغ)](../zh-HK/README.md) | [الصينية (التقليدية، ماكاو)](../zh-MO/README.md) | [الصينية (التقليدية، تايوان)](../zh-TW/README.md) | [الكرواتية](../hr/README.md) | [التشيكية](../cs/README.md) | [الدنماركية](../da/README.md) | [الهولندية](../nl/README.md) | [الإستونية](../et/README.md) | [الفنلندية](../fi/README.md) | [الفرنسية](../fr/README.md) | [الألمانية](../de/README.md) | [اليونانية](../el/README.md) | [العبرية](../he/README.md) | [الهندية](../hi/README.md) | [الهنغارية](../hu/README.md) | [الإندونيسية](../id/README.md) | [الإيطالية](../it/README.md) | [اليابانية](../ja/README.md) | [الكانادية](../kn/README.md) | [الخميرية](../km/README.md) | [الكورية](../ko/README.md) | [الليتوانية](../lt/README.md) | [الماليزية](../ms/README.md) | [الماليالامية](../ml/README.md) | [الماراثية](../mr/README.md) | [النيبالية](../ne/README.md) | [البيدجين النيجيرية](../pcm/README.md) | [النرويجية](../no/README.md) | [الفارسية (اللغة)](../fa/README.md) | [البولندية](../pl/README.md) | [البرتغالية (البرازيل)](../pt-BR/README.md) | [البرتغالية (البرتغال)](../pt-PT/README.md) | [البنجابية (جورموخي)](../pa/README.md) | [الرومانية](../ro/README.md) | [الروسية](../ru/README.md) | [الصربية (السيريلية)](../sr/README.md) | [السلوفاكية](../sk/README.md) | [السلوفينية](../sl/README.md) | [الإسبانية](../es/README.md) | [السواحلية](../sw/README.md) | [السويدية](../sv/README.md) | [التاجالوج (الفلبينية)](../tl/README.md) | [التاميلية](../ta/README.md) | [التيلوجو](../te/README.md) | [التايلاندية](../th/README.md) | [التركية](../tr/README.md) | [الأوكرانية](../uk/README.md) | [الأردية](../ur/README.md) | [الفيتنامية](../vi/README.md)

> **هل تفضل الاستنساخ محليًا؟**
>
> يشمل هذا المستودع أكثر من 50 ترجمة لغوية مما يزيد بشكل كبير حجم التنزيل. لاستنساخ بدون الترجمات، استخدم sparse checkout:
>
> **باش / macOS / لينكس:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (ويندوز):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> هذا يمنحك كل ما تحتاجه لإكمال الدورة مع تنزيل أسرع بكثير.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**تنويه**:
تمت ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والمعتمد. للمعلومات الهامة، يُنصح بالاستعانة بترجمة بشرية محترفة. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->