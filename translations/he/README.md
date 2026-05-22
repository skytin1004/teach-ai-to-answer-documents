# ללמד בינה מלאכותית לענות על שאלות בהתבסס על המסמכים שלך

![סקירת מערכת RAG מבוססת מסמכים](../../assets/images/readme-hero.svg)

מאגר הקוד הזה אוסף סדרת בלוגים משנת 2026 אודות בניית מערכות בינה מלאכותית מבוססות מסמכים עם RAG, שירותי בינה מלאכותית של Azure, חלופות קוד פתוח, וזרמי עבודה מונחי הערכה.

## רקע

בשנת 2023, עבדתי על זוג מדריכים בנושא ללמד את ChatGPT לענות על שאלות מתוך מסמכי PDF באמצעות Azure AI Search ו-Azure OpenAI. הרעיון של "ChatGPT על הנתונים שלך" עדיין הרגיש חדש אז, והמטרה הייתה להראות זרימת עבודה מעשית: לאחסן מסמכים, לאנדקס אותם, לשלוף תוכן רלוונטי, וליצור תשובות מההקשר שנשלף.

ב-2026, מערכת RAG רחבה בהרבה. Azure AI Search תומך בדפוסי שליפה מודרניים של וקטורים והיברידיים, Azure OpenAI הוא חלק ממערכת Microsoft Foundry Models הרחבה, וכלי קוד פתוח כמו LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, ו-vLLM הפכו לבחירות מעשיות למערכות אמיתיות.

זו הסיבה שרציתי לחזור לנושא הזה. השאלה כבר איננה רק "איך בונים RAG?" אלא ישנן כיום דרכים רבות לבנות אותה, והשאלה החשובה יותר היא "איזה ארכיטקטורה לבחור לסיטואציה שלי?"

סדרה זו מתחילה משכבת קבלת ההחלטות הזו, ואז הופכת אותה למדריכים מעשיים. מסלול היישום הראשון בונה מערכת RAG קוד פתוח מקומית שכל אחד יכול להריץ עם נתוני דוגמה, Qdrant, Ollama, ו-Phi-4-mini.

## מאמרים

ראה [articles/README.md](./articles/README.md) לאינדקס המאמרים.

1. [סדרה 1: RAG, Azure מול חלופות קוד פתוח, ומתי כדאי כוונון עדין](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [סדרה 2: בניית מערכת RAG קוד פתוח מקומית מקצה לקצה](./articles/series-2-open-source-rag-end-to-end.md)

בקרוב:

- לבנות מחדש את אותה מערכת RAG עם Azure AI Search ו-Azure OpenAI.
- להוסיף הערכה ובדיקות רגרסיה מעבר לתשובת הדמו.

## מחברות

מאמרי היישום משתמשים במחברות (notebooks) כדי שניתן יהיה לבדוק את שלבי השליפה וההערכה ישירות. ראה [notebooks/README.md](./notebooks/README.md) להנחיות כלליות לתיקיה.

> [!TIP]
> התחילו בסדרה 2 אם אתם רוצים את המסלול המהיר ביותר. היא רצה מקומית עם נתוני דוגמה, הטמעות יעילות למעבד, מצב מקומי של Qdrant, וללא אישורי ענן.

| סידרה | מחברת | דרישות | אימות מקומי |
| --- | --- | --- | --- |
| סידרה 2 | [מחברת RAG קוד פתוח](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | מצב מקומי של Qdrant, שליפה, מיון מחדש ואימות חיווט מקור |

להריץ מחברת מקומית, צרו סביבה וירטואלית והתקינו את קובץ הדרישות התואם. לדוגמה:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## נתוני דוגמה

המחברות משתמשות בקורפוס קטן מקומי ב-[sample_data](../../sample_data) כדי שהדוגמאות יכולות לרוץ ללא מסמכים פרטיים או אישורי ענן. ראה [sample_data/README.md](./sample_data/README.md) לפרטים.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## סיכום אימות מקומי

תוצאות האימות מתועדות בכל מאמר וב-[SERIES_PLAN.md](./SERIES_PLAN.md).

| תחום | תוצאה |
| --- | --- |
| מסלול קוד פתוח בסידרה 2 | FastEmbed יצר הטמעות מקומיות בממד 384, אוסף בזיכרון של Qdrant הכניס 8 וקטורים, מיון קל משקל שלף את הקטע הצפוי; יצירת Ollama אופציונלית הושלמה עם `phi4-mini:3.8b` |

המחברת המקומית נמנעת בכוונה מסודות מקודדים.

## יצירת Ollama מקומית

מחברת הסידרה 2 בטוחה לשימוש מקומי כברירת מחדל. כדי לאפשר יצירת Ollama מקומית, העתק את הקובץ [.env.example](../../.env.example) ל- `.env` ומלא את הערכים של הסידרה 2.

ליצירה בסידרה 2 עם Ollama, הסר את ההערה:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

מחברת הסידרה 2 טוענת אוטומטית את `.env` מתיקיית השורש של המאגר באמצעות `python-dotenv`.

> [!IMPORTANT]
> אל תכללו קבצי `.env`, מפתחות API, נקודות קצה פרטיות, או ערכים ספציפיים לשוכר. המאגר שומר בכוונה סודות מחוץ לקבצי Markdown ולמחברות.

קבצי הדרישות מתועדים ב-[requirements/README.md](./requirements/README.md).

כדי לאמת קישורים, מבנה המחברת, ניקיון הפלט ודפוסי סודות בסיכון גבוה:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

סקריפטי האימות מתועדים ב-[scripts/README.md](./scripts/README.md).

להריץ את כל המחברות הבטוחות בסביבה המקומית:

```powershell
python scripts\verify_notebooks.py --execute
```

זרם האימות אותו מריץ GitHub Actions בלחיצות, בקשות משיכה והפעלות ידניות. מאמרים ומחברות טיוטה לא נכללים בכוונה במסלול האימות הציבורי.

לפני פרסום עדכונים, השתמש ב-[PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

ראה [CHANGELOG.md](./CHANGELOG.md) עבור סיכום השינויים הלא מפורסם.

לקווי הנחייה לתרומה ולתחזוקת מחברות, ראה [CONTRIBUTING.md](./CONTRIBUTING.md).

## תמיכה בריבוי שפות

### נתמכת באמצעות Co-op Translator (אוטומטי ותמיד מעודכן)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[ערבית](../ar/README.md) | [בנגלית](../bn/README.md) | [בולגרית](../bg/README.md) | [בורמאית (מיאנמר)](../my/README.md) | [סינית (מפושטת)](../zh-CN/README.md) | [סינית (מסורתית, הונג קונג)](../zh-HK/README.md) | [סינית (מסורתית, מקאו)](../zh-MO/README.md) | [סינית (מסורתית, טייוואן)](../zh-TW/README.md) | [קרואטית](../hr/README.md) | [צ'כית](../cs/README.md) | [דנית](../da/README.md) | [הולנדית](../nl/README.md) | [אסטונית](../et/README.md) | [פינית](../fi/README.md) | [צרפתית](../fr/README.md) | [גרמנית](../de/README.md) | [יוונית](../el/README.md) | [עברית](./README.md) | [הינדי](../hi/README.md) | [הונגרית](../hu/README.md) | [אינדונזית](../id/README.md) | [איטלקית](../it/README.md) | [יפנית](../ja/README.md) | [קנאדה](../kn/README.md) | [חמרית](../km/README.md) | [קוריאנית](../ko/README.md) | [ליטאית](../lt/README.md) | [מלאית](../ms/README.md) | [מלאיאלאם](../ml/README.md) | [מרעי](../mr/README.md) | [נפאלית](../ne/README.md) | [ניגרית פידג׳ין](../pcm/README.md) | [נורווגית](../no/README.md) | [פרסית (פרסי)](../fa/README.md) | [פולנית](../pl/README.md) | [פורטוגזית (ברזיל)](../pt-BR/README.md) | [פורטוגזית (פורטוגל)](../pt-PT/README.md) | [פנג'אבי (גורמוכי)](../pa/README.md) | [רומנית](../ro/README.md) | [רוסית](../ru/README.md) | [סרבית (קירילית)](../sr/README.md) | [סלובקית](../sk/README.md) | [סלובנית](../sl/README.md) | [ספרדית](../es/README.md) | [סוואהילי](../sw/README.md) | [שוודית](../sv/README.md) | [טגלוג (פיליפינית)](../tl/README.md) | [טמילית](../ta/README.md) | [טלוגו](../te/README.md) | [תאית](../th/README.md) | [טורקית](../tr/README.md) | [אוקראינית](../uk/README.md) | [אורדו](../ur/README.md) | [וייטנאמית](../vi/README.md)

> **מעדיפים לשכפל מקומית?**
>
> מאגר זה כולל תרגומים ל-50+ שפות שמגדילים משמעותית את גודל ההורדה. כדי לשכפל ללא תרגומים, השתמשו בספרס צ'קאאוט:
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
> זה נותן לכם את כל הדרוש כדי להשלים את הקורס עם הורדה הרבה יותר מהירה.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->