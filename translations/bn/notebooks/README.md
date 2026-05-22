# নোটবুক

এই নোটবুকগুলি আর্টিকেল সিরিজের সাথে রানযোগ্য উদাহরণসমূহ সমর্থন করে।

| নোটবুক | আর্টিকেল | উদ্দেশ্য |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [সিরিজ ২](../articles/series-2-open-source-rag-end-to-end.md) | ফাস্টএম্বেড, কিউড্রান্ট লোকাল মোড, রিট্রিভাল, রির্যাঙ্কিং, ঐচ্ছিক অললামা জেনারেশন, এবং উৎস রেফারেন্সসহ ওপেন-সোর্স RAG |

## লোকালি রান করুন

যে নোটবুকটি চালাতে চান তার জন্য প্রয়োজনীয়তাসমূহ ইনস্টল করুন:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

অথবা সব ডিপেন্ডেন্সি ইনস্টল করুন:

```powershell
python -m pip install -r requirements\all.txt
```

## যাচাই করুন

রিপোজিটোরির মূল ফোল্ডার থেকে:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

সিরিজ ২ একটি রিপোজিটোরি-রুট `.env` ফাইল থেকে অললামা কনফিগারেশন পড়তে পারে। [../.env.example](../../../.env.example) থেকে শুরু করুন, যা সিরিজ অনুযায়ী গুচ্ছবদ্ধ।

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা শুদ্ধতার জন্য চেষ্টা করি, অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার স্বভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে প্রয়োজনীয় ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়বদ্ধ নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->