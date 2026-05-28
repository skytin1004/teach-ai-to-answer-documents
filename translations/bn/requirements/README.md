# Requirements

Each implementation article has a focused requirements file.

| File | Used by |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | সিরিজ ২ ওপেন-সোর্স RAG নোটবুক, অপশনাল Ollama উৎপাদন সহায়ক সহ |
| [all.txt](../../../requirements/all.txt) | রিপোসিটরি-স্তরের যাচাই ও CI |

একটি নোটবুক চালানোর সময় ফোকাসড ফাইল ব্যবহার করুন। পুরো রিপোজিটরি যাচাই করার সময় `all.txt` ব্যবহার করুন।

`open-source-rag.txt` এবং `all.txt` স্থানীয় এম্বেডিংয়ের জন্য `fastembed` এবং সিরিজ ২ থেকে `.env` থেকে Ollama উৎপাদন অপশনে সক্ষম করার জন্য `python-dotenv` অন্তর্ভুক্ত করে, যা পুনরুদ্ধার পাইপলাইনে পরিবর্তন ছাড়াই করা যায়।

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা শুদ্ধতার জন্য চেষ্টা করি, অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার স্বভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে প্রয়োজনীয় ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়বদ্ধ নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->