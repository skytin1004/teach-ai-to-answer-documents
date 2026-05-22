# פנקסי הערות

פנקסי הערות אלה תומכים בסדרת המאמרים עם דוגמאות שניתן להריץ.

| פנקס הערות | מאמר | מטרה |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [סדרה 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG בקוד פתוח עם FastEmbed, מצב מקומי של Qdrant, שליפה, סידור מחדש, יצירת Ollama אופציונלית, והפניות למקורות |

## הרצה מקומית

התקן את הדרישות עבור פנקס ההערות שברצונך להריץ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

או התקן את כל התלויות:

```powershell
python -m pip install -r requirements\all.txt
```

## אימות

משורש המאגר:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

סדרה 2 יכולה לקרוא תצורת Ollama מקובץ `.env` בשורש המאגר. התחל מ-[../.env.example](../../../.env.example), שממוין לפי סדרות.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->