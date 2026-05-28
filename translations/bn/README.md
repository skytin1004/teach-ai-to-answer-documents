# আপনার ডকুমেন্টের উপর ভিত্তি করে AI-কে প্রশ্নের উত্তর দিতে শেখান

![Document-grounded AI RAG system overview](../../assets/images/readme-hero.svg)

এই রিপোজিটরি ২০২৬ সালের এক ব্লগ সিরিজ সংগ্রহ করে যা RAG, Azure AI সার্ভিস, ওপেন-সোর্স বিকল্প এবং মূল্যায়ন-কেন্দ্রিক ওয়ার্কফ্লোর মাধ্যমে ডকুমেন্ট-গ্রাউন্ডেড AI সিস্টেম তৈরি করার বিষয়ে।

## পটভূমি

২০২৩ সালে, আমি Azure AI Search এবং Azure OpenAI ব্যবহার করে PDF ডকুমেন্ট থেকে প্রশ্নের উত্তর দিতে ChatGPT কে শেখানোর একটি টিউটোরিয়াল জোড়া নিয়ে কাজ করেছিলাম। "আপনার ডেটার উপর ChatGPT" ধারণাটি তখনও নতুন মনে হচ্ছিল, এবং লক্ষ্য ছিল একটি বাস্তব ওয়ার্কফ্লো দেখানো: ডকুমেন্টগুলি সংরক্ষণ করা, সেগুলো ইনডেক্স করা, প্রাসঙ্গিক তথ্য পুনরুদ্ধার করা এবং সেই প্রাপ্ত প্রসঙ্গ থেকে উত্তর তৈরি করা।

২০২৬ সালে, RAG ইকোসিস্টেম অনেক বড় হয়েছে। Azure AI Search আধুনিক ভেক্টর এবং হাইব্রিড রিট্রিভাল প্যাটার্ন সমর্থন করে, Azure OpenAI বিস্তৃত Microsoft Foundry Models ইকোসিস্টেমের অংশ, এবং LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, এবং vLLM-এর মতো ওপেন-সোর্স টুলগুলি বাস্তব সিস্টেমের জন্য ব্যবহারযোগ্য পছন্দ হয়ে উঠেছে।

এই কারণে আমি এই বিষয়টি আবার দেখতে চেয়েছি। প্রশ্ন আর শুধুমাত্র "আমি কিভাবে RAG তৈরি করব?" নয়। এখন RAG তৈরি করার অনেক উপায় আছে, এবং সবচেয়ে গুরুত্বপূর্ণ প্রশ্ন হলো "আমার পরিস্থিতির জন্য কোন আর্কিটেকচার বেছে নেব?"

এই সিরিজটি সেই সিদ্ধান্ত নেওয়ার স্তর থেকে শুরু হয়, তারপর সেটিকে হাতেকলমে টিউটোরিয়ালে রূপান্তর করে। প্রথম বাস্তবায়ন পথটি একটি স্থানীয় ওপেন-সোর্স RAG সিস্টেম তৈরি করে যা নমুনা ডেটা, Qdrant, Ollama, এবং Phi-4-mini-এর সাহায্যে যে কেউ চালাতে পারে।

## প্রবন্ধসমূহ

প্রবন্ধের সূচিপত্র দেখতে [articles/README.md](./articles/README.md) দেখুন।

১. [সিরিজ ১: RAG, Azure বনাম ওপেন-সোর্স বিকল্প, এবং কখন ফাইন-টিউনিং কাজ করে](./articles/series-1-rag-azure-open-source-fine-tuning.md)  
২. [সিরিজ ২: সম্পূর্ণ পরিসরে একটি স্থানীয় ওপেন-সোর্স RAG সিস্টেম তৈরি করুন](./articles/series-2-open-source-rag-end-to-end.md)

পরবর্তীকালে আসছে:

- একই RAG সিস্টেম Azure AI Search এবং Azure OpenAI দিয়ে পুনর্নির্মাণ।  
- একটি ডেমো উত্তরের তুলনায় মূল্যায়ন এবং রিগ্রেশন চেক যোগ করা।

## নোটবুকসমূহ

বাস্তবায়ন প্রবন্ধগুলোতে নোটবুক ব্যবহৃত হয় যাতে পুনরুদ্ধার এবং মূল্যায়ন ধাপ সরাসরি পরিদর্শন করা যায়। ফোল্ডার-স্তরের নির্দেশনার জন্য [notebooks/README.md](./notebooks/README.md) দেখুন।

> [!TIP]  
> দ্রুততম পথের জন্য সিরিজ ২ দিয়ে শুরু করুন। এটি স্থানীয়ভাবে নমুনা ডেটা, CPU-সাপেক্ষ এমবেডিংস, Qdrant লোকাল মোড, এবং কোনো ক্লাউড ক্রেডেনশিয়াল ছাড়াই চলে।

| সিরিজ | নোটবুক | প্রয়োজনীয়তা | স্থানীয় যাচাইকরণ |
| --- | --- | --- | --- |
| সিরিজ ২ | [ওপেন-সোর্স RAG নোটবুক](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant লোকাল মোড, রিট্রিভাল, রির্যাঙ্কিং, এবং সোর্স ওয়্যারিং যাচাইকৃত |

একটি নোটবুক স্থানীয়ভাবে চালাতে, একটি ভার্চুয়াল পরিবেশ তৈরি করুন এবং মিল থাকা প্রয়োজনীয়তা ফাইল ইনস্টল করুন। উদাহরণস্বরূপ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```
  
## নমুনা ডেটা

নোটবুকগুলো ছোট একটি স্থানীয় কর্পাস [sample_data](../../sample_data) ব্যবহার করে যাতে উদাহরণগুলো ব্যক্তিগত ডকুমেন্ট বা ক্লাউড ক্রেডেনশিয়াল ছাড়াই চালানো যায়। বিস্তারিত জানতে [sample_data/README.md](./sample_data/README.md) দেখুন।

- [school_ai_policy.md](./sample_data/school_ai_policy.md)  
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)  

## স্থানীয় যাচাইকরণের সারাংশ

যাচাইকরণ ফলাফল প্রতিটি প্রবন্ধে এবং [SERIES_PLAN.md](./SERIES_PLAN.md) এ রেকর্ড করা আছে।

| ক্ষেত্র | ফলাফল |
| --- | --- |
| সিরিজ ২ ওপেন-সোর্স পথ | FastEmbed ৩৮৪-মাপের স্থানীয় এমবেডিং তৈরি করেছে, Qdrant ইন-মেমরি কালেকশনে ৮টি ভেক্টর প্রবেশ করানো হয়েছে, হালকা ওজনের রির্যাঙ্কিং প্রত্যাশিত সেকশনটি উদ্ধার করেছে; ঐচ্ছিক Ollama উৎপাদন `phi4-mini:3.8b` দিয়ে সম্পন্ন হয়েছে |

লোকাল নোটবুক ইচ্ছাকৃতভাবে হার্ডকোড করা গোপনীয় তথ্য এড়ায়।

## স্থানীয় Ollama উৎপাদন

সিরিজ ২ নোটবুক ডিফল্টরূপে স্থানীয়-সুরক্ষা সম্পন্ন। স্থানীয় Ollama উৎপাদন সক্ষম করতে, [.env.example](../../.env.example) `.env` এ কপি করে সিরিজ ২ এর মানগুলি পূরণ করুন।

সিরিজ ২ Ollama উৎপাদনের জন্য মন্তব্য সরান:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```
  
সিরিজ ২ নোটবুক স্বয়ংক্রিয়ভাবে `python-dotenv` ব্যবহার করে রিপোজিটরি রুট থেকে `.env` লোড করে।

> [!IMPORTANT]  
> `.env` ফাইল, API কী, ব্যক্তিগত এন্ডপয়েন্ট, বা টেন্যান্ট-নির্দিষ্ট মানগুলি কমিট করবেন না। রিপোজিটরি ইচ্ছাকৃতভাবে Markdown ফাইল এবং নোটবুক থেকে গোপনীয়তা রাখা হয়েছে।

প্রয়োজনীয়তা ফাইলগুলো [requirements/README.md](./requirements/README.md) এ ডকুমেন্টেড।

লিঙ্ক, নোটবুক স্ট্রাকচার, নোটবুক আউটপুট শুদ্ধতা এবং উচ্চ-ঝুঁকিপূর্ণ গোপনীয়তার প্যাটার্ন যাচাই করতে:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```
  
যাচাইকরণ স্ক্রিপ্টগুলো [scripts/README.md](./scripts/README.md) এ ব্যাখ্যা আছে।

একই পরিবেশে সব স্থানীয়-সুরক্ষিত নোটবুক চালাতে:

```powershell
python scripts\verify_notebooks.py --execute
```
  
একই যাচাইকরণ ফ্লো GitHub Actions-এ push, pull request, এবং ম্যানুয়াল ওয়ার্কফ্লো ডিসপ্যাচে চলে। খসড়া প্রবন্ধ এবং নোটবুকগুলো ইচ্ছাকৃতভাবে পাবলিক যাচাইকরণ পথ থেকে বাদ দেওয়া হয়েছে।

আপডেট প্রকাশের পূর্বে [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) ব্যবহার করুন।

বর্তমান অপাবলিশড পরিবর্তনের সারাংশ জানতে [CHANGELOG.md](./CHANGELOG.md) দেখুন।

অবদান এবং নোটবুক স্বাস্থ্যবিধির নির্দেশনা জন্য [CONTRIBUTING.md](./CONTRIBUTING.md) দেখুন।

## বহুভাষী সমর্থন

### Co-op Translator (স্বয়ংক্রিয় এবং সর্বদা আপ-টু-ডেট) মাধ্যমে সমর্থিত

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](./README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **স্থানীয়ভাবে ক্লোন করতে চান?**  
>  
> এই রিপোজিটরিতে ৫০+ ভাষার অনুবাদ রয়েছে যা ডাউনলোডের আকার অনেক বাড়ায়। অনুবাদ ছাড়া ক্লোন করতে স্পার্স চেকআউট ব্যবহার করুন:  
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
> এটি আপনাকে ক্লাস সম্পন্ন করার জন্য প্রয়োজনীয় সবকিছু অনেক দ্রুত ডাউনলোড দেয়।  
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা শুদ্ধতার জন্য চেষ্টা করি, অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার স্বভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে প্রয়োজনীয় ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়বদ্ধ নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->