# ללמד בינה מלאכותית לענות על שאלות בהתבסס על המסמכים שלך

מאגר זה אוסף סדרת בלוגים משנת 2026 על בניית מערכות בינה מלאכותית מבוססות מסמכים עם RAG, שירותי Azure AI, חלופות קוד פתוח, וזרימות עבודה מוכוונות הערכה.

## רקע

בשנת 2023 עבדתי על זוג מדריכים ללימוד ChatGPT לענות על שאלות מתוך מסמכי PDF באמצעות Azure AI Search ו-Azure OpenAI. רעיון "ChatGPT על הנתונים שלך" עדיין הרגיש חדש אז, והמטרה הייתה להראות זרימת עבודה מעשית: לאחסן מסמכים, לאינדקס אותם, למצוא תוכן רלוונטי, וליצור תשובות מהקשר שנמצא.

בשנת 2026, סביבת RAG גדולה הרבה יותר. Azure AI Search תומך בתבניות אחזור מודרניות וקטוריות והיברידיות, Azure OpenAI הוא חלק מהאקוסיסטם הרחב יותר של Microsoft Foundry Models, וכלים בקוד פתוח כגון LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, ו-vLLM הפכו לבחירות מעשיות למערכות אמיתיות.

לכן רציתי לחזור לנושא זה. השאלה כבר אינה רק "איך לבנות RAG?" יש כיום דרכים רבות לבנות אותו, והשאלה החשובה יותר היא "איזה ארכיטקטורה כדאי לבחור למצב שלי?"

סדרה זו מתחילה משכבת קבלת ההחלטות הזו. לפני שנכנסים לעומק היישום, היא מתבוננת מדוע שירותי בינה מלאכותית צריכים אחזור, מתי שירותים מנוהלים מבוססי Azure הגיוניים, מתי חלופות קוד פתוח מתאימות יותר, ואיפה פיין-טיונינג משתלב.

## מאמרים

1. [סדרה 1: RAG, Azure מול חלופות קוד פתוח, ומתי פיין-טיונינג הגיוני](./series-1-rag-azure-open-source-fine-tuning.md)

## תמיכה רב-לשונית

### נתמכת באמצעות Co-op Translator (אוטומטי ותמיד מעודכן)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[ערבית](../ar/README.md) | [בנגלית](../bn/README.md) | [בולגרית](../bg/README.md) | [בירמזית (מיאנמר)](../my/README.md) | [סינית (מפושטת)](../zh-CN/README.md) | [סינית (מסורתית, הונג קונג)](../zh-HK/README.md) | [סינית (מסורתית, מקאו)](../zh-MO/README.md) | [סינית (מסורתית, טייוואן)](../zh-TW/README.md) | [קרואטית](../hr/README.md) | [צ'כית](../cs/README.md) | [דנית](../da/README.md) | [הולנדית](../nl/README.md) | [אסטונית](../et/README.md) | [פינית](../fi/README.md) | [צרפתית](../fr/README.md) | [גרמנית](../de/README.md) | [יוונית](../el/README.md) | [עברית](./README.md) | [הודית](../hi/README.md) | [הונגרית](../hu/README.md) | [אינדונזית](../id/README.md) | [איטלקית](../it/README.md) | [יפנית](../ja/README.md) | [קאנדה](../kn/README.md) | [חמרית](../km/README.md) | [קוריאנית](../ko/README.md) | [ליטאית](../lt/README.md) | [מלאית](../ms/README.md) | [מלאלאית](../ml/README.md) | [מרטהית](../mr/README.md) | [נפאלית](../ne/README.md) | [פיג'ין ניגרי](../pcm/README.md) | [נורווגית](../no/README.md) | [פרסית (פרסי)](../fa/README.md) | [פולנית](../pl/README.md) | [פורטוגזית (ברזיל)](../pt-BR/README.md) | [פורטוגזית (פורטוגל)](../pt-PT/README.md) | [פונג'אבית (גורמוכי)](../pa/README.md) | [רומנית](../ro/README.md) | [רוסית](../ru/README.md) | [סרבית (קירילית)](../sr/README.md) | [סלובקית](../sk/README.md) | [סלובנית](../sl/README.md) | [ספרדית](../es/README.md) | [סוואהילי](../sw/README.md) | [שוודית](../sv/README.md) | [טגלוג (פיליפינית)](../tl/README.md) | [טמילית](../ta/README.md) | [טלוגו](../te/README.md) | [תאית](../th/README.md) | [טורקית](../tr/README.md) | [אוקראינית](../uk/README.md) | [אורדו](../ur/README.md) | [וייטנאמית](../vi/README.md)

> **עדיף לשכפל מקומית?**
>
> מאגר זה כולל למעלה מ-50 תרגומים, מה שמגדיל משמעותית את גודל ההורדה. לשכפול ללא תרגומים, השתמש ב-sparse checkout:
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
> זה נותן לך את כל מה שאתה צריך כדי להשלים את הקורס עם הורדה מהירה יותר.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->