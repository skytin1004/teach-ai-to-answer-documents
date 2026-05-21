# علِّم الذكاء الاصطناعي الإجابة عن الأسئلة بناءً على مستنداتك

يجمع هذا المستودع سلسلة مدونات لعام 2026 حول بناء أنظمة ذكاء اصطناعي ترتكز على المستندات باستخدام RAG، وخدمات Azure AI، والبدائل مفتوحة المصدر، وسير العمل المرتكز على التقييم.

## الخلفية

في عام 2023، عملت على زوج من البرامج التعليمية حول تعليم ChatGPT للإجابة على الأسئلة من مستندات PDF باستخدام Azure AI Search وAzure OpenAI. كانت فكرة "ChatGPT على بياناتك" لا تزال جديدة آنذاك، والهدف كان عرض سير عمل عملي: تخزين المستندات، فهرستها، استرجاع المحتوى ذي الصلة، وتوليد الإجابات من السياق المسترجع.

في عام 2026، أصبح نظام RAG أكبر بكثير. يدعم Azure AI Search أنماط الاسترجاع الحديثة النقطية والهجينة، وأصبح Azure OpenAI جزءًا من نظام Microsoft Foundry Models الأوسع، وتحوّلت الأدوات مفتوحة المصدر مثل LangGraph وLlamaIndex وHaystack وQdrant وMilvus وWeaviate وChroma وOllama وvLLM إلى خيارات عملية للأنظمة الحقيقية.

لهذا أردت إعادة النظر في هذا الموضوع. لم يعد السؤال فقط "كيف أبني RAG؟" بل هناك الآن العديد من الطرق لبنائه، والسؤال الأكثر أهمية هو "أي بنية يجب أن أختارها لحالتي؟"

تبدأ هذه السلسلة من طبقة اتخاذ القرار تلك. قبل التعمق في التنفيذ، تبحث في سبب حاجة خدمات الذكاء الاصطناعي للاسترجاع، ومتى تكون الخدمات المدارة على Azure مناسبة، ومتى تكون البدائل مفتوحة المصدر أفضل ملاءمة، وأين يناسب التخصيص الدقيق.

## المقالات

1. [السلسلة 1: RAG، Azure مقابل البدائل مفتوحة المصدر، ومتى يكون التخصيص الدقيق مناسبًا](./series-1-rag-azure-open-source-fine-tuning.md)

## الدعم متعدد اللغات

### مدعوم عبر Co-op Translator (آلي ومحدث دائمًا)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[العربية](./README.md) | [البنغالية](../bn/README.md) | [البلغارية](../bg/README.md) | [اللغة البورمية (ميانمار)](../my/README.md) | [الصينية (المبسطة)](../zh-CN/README.md) | [الصينية (التقليدية، هونغ كونغ)](../zh-HK/README.md) | [الصينية (التقليدية، ماكاو)](../zh-MO/README.md) | [الصينية (التقليدية، تايوان)](../zh-TW/README.md) | [الكرواتية](../hr/README.md) | [التشيكية](../cs/README.md) | [الدانماركية](../da/README.md) | [الهولندية](../nl/README.md) | [الإستونية](../et/README.md) | [الفنلندية](../fi/README.md) | [الفرنسية](../fr/README.md) | [الألمانية](../de/README.md) | [اليونانية](../el/README.md) | [العبرية](../he/README.md) | [الهندية](../hi/README.md) | [الهنغارية](../hu/README.md) | [الإندونيسية](../id/README.md) | [الإيطالية](../it/README.md) | [اليابانية](../ja/README.md) | [الكانادية](../kn/README.md) | [الخميرية](../km/README.md) | [الكورية](../ko/README.md) | [الليتوانية](../lt/README.md) | [المالايوية](../ms/README.md) | [الملالياية](../ml/README.md) | [الماراثية](../mr/README.md) | [النيبالية](../ne/README.md) | [البيجن النيجيري](../pcm/README.md) | [النرويجية](../no/README.md) | [الفارسية (اللغة الفارسية)](../fa/README.md) | [البولندية](../pl/README.md) | [البرتغالية (البرازيل)](../pt-BR/README.md) | [البرتغالية (البرتغال)](../pt-PT/README.md) | [البنجابية (Gurmukhi)](../pa/README.md) | [الرومانية](../ro/README.md) | [الروسية](../ru/README.md) | [الصربية (السيليزية)](../sr/README.md) | [السلوفاكية](../sk/README.md) | [السلوفينية](../sl/README.md) | [الإسبانية](../es/README.md) | [السواحيلية](../sw/README.md) | [السويدية](../sv/README.md) | [التاغالوغ (الفلبينية)](../tl/README.md) | [التاميلية](../ta/README.md) | [التيلجو](../te/README.md) | [التايلاندية](../th/README.md) | [التركية](../tr/README.md) | [الأوكرانية](../uk/README.md) | [الأردية](../ur/README.md) | [الفيتنامية](../vi/README.md)

> **تفضل النسخ محليًا؟**
>
> يتضمن هذا المستودع أكثر من 50 ترجمة لغوية مما يزيد بشكل كبير من حجم التنزيل. للاستنساخ بدون الترجمات، استخدم السحب الجزئي:
>
> **Bash / macOS / Linux:**
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