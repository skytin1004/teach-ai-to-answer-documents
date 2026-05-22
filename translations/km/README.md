# សិក្សាបង្រៀន AI ដើម្បីឆ្លើយសំណួរដោយផ្អែកលើឯកសាររបស់អ្នក

![រូបភាពសង្ខេបប្រព័ន្ធ AI RAG ដែលផ្អែកលើឯកសារ](../../assets/images/readme-hero.svg)

ឃ្លាំងនេះប្រមូលបណ្ដុំអត្ថបទប្លុកឆ្នាំ 2026 អំពីការបង្កើតប្រព័ន្ធ AI ដែលផ្អែកលើឯកសារជាមួយ RAG សេវាកម្ម Azure AI ជំនួសបើកចំហ និងផ្លូវការត្រួតពិនិត្យផ្តោតលើការវាយតម្លៃ។

## ផ្ទៃដែនផ្ទាល់ខ្លួន

ក្នុងឆ្នាំ 2023 ខ្ញុំបានធ្វើការលើសTutorials ខ្នាតពីរអំពីការបង្រៀន ChatGPT ឱ្យឆ្លើយសំណួរពីឯកសារ PDF ដោយប្រើ Azure AI Search និង Azure OpenAI។ គំនិត "ChatGPT លើទិន្នន័យរបស់អ្នក" នៅតែមានអារម្មណ៍ថាថ្មីនៅពេលនោះ ហើយគោលបំណងគឺបង្ហាញលំហូរការងារជាក់ស្តែង៖ រក្សាទុកឯកសារ តួលេខវា ស្វែងរកខ្លឹមសារដែលប្រសើរ និងបង្កើតចម្លើយពីបរិបទដែលបានស្វែងរកនោះ។

នៅឆ្នាំ 2026 អេកូស៊ីសធ៌ម RAG កាន់តែធំជាងមុន។ Azure AI Search គាំទ្រទំនាញបត់បែនវ៉ិចទ័រថ្មី និងការស្វែងរកប្រភេទផ្សំ Azure OpenAI ជាផ្នែកមួយនៃប្រព័ន្ធ Microsoft Foundry Models ជាសកល ហើយឧបករណ៍បើកចំហដូចជា LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama និង vLLM បានក្លាយជាជម្រើសពិតប្រាកដសម្រាប់ប្រព័ន្ធពិតប្រាកដ។

នេះហើយហេតុផលដែលខ្ញុំចង់ត្រឡប់មកពិចារណាប្រធាននេះម្តងទៀត។ សំណួរឥឡូវនេះមិនមែនគ្រាន់តែ "តើធ្វើដូចម្តេចដើម្បីបង្កើត RAG?" ទេ ប៉ុន្តែមានវិធីជាច្រើនក្នុងការបង្កើតវា ហើយសំណួរសំខាន់ជាងគេសម្រាប់ស្ថានភាពរបស់ខ្ញុំគឺ "តើខ្ញុំគួរជ្រើសរចនាសម្ព័ន្ធណាសម្រាប់ស្ថានភាពរបស់ខ្ញុំ?"

ស៊េរីនេះចាប់ផ្តើមពីស្រទាប់ការទិញចំណុចនោះ បន្ទាប់មកប្តូរវាទៅជាតូរីលៗ។ ផ្លូវអនុវត្តដំបូងគឺបង្កើតប្រព័ន្ធ RAG បើកចំហក្នុងតំបន់ដែលនរណាក៏អាចដំណើរការជាមួយទិន្នន័យគំរូ Qdrant Ollama និង Phi-4-mini។

## អត្ថបទ

មើល [articles/README.md](./articles/README.md) សម្រាប់សន្ទស្សន៍អត្ថបទ។

1. [ស៊េរី 1៖ RAG, Azure ប្រឆាំងជាមួយ ជម្រើសបើកចំហ និង កាល​បរិច្ឆេទ Fine-Tuning ដែលមានអត្ថិភាព](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [ស៊េរី 2៖ បង្កើតប្រព័ន្ធ RAG បើកចំហក្នុងតំបន់ចប់ពីដើមដល់ចុង](./articles/series-2-open-source-rag-end-to-end.md)

អ្វីដែលនឹងមកបន្ទាប់៖

- បង្កើតប្រព័ន្ធ RAG ដដែលជាមួយ Azure AI Search និង Azure OpenAI។
- បន្ថែមការវាយតម្លៃ និងពិនិត្យប្រៀបធៀបលើសខ្លះនៃចម្លើយសម្ដែង។

## កំណត់ត្រា

អត្ថបទអនុវត្តន៍ប្រើកំណត់ត្រាដើម្បីអនុញ្ញាតឱ្យមើលដំណើរការស្វែងរក និងវាយតម្លៃបានដោយផ្ទាល់។ មើល [notebooks/README.md](./notebooks/README.md) សម្រាប់ការណែនាំកម្រិតថត។

> [!TIP]
> ចាប់ផ្ដើមជាមួយស៊េរី 2 ប្រសិនបើអ្នកចង់បានផ្លូវលឿនជាងគេ។ វាដំណើរការក្នុងតំបន់ជាមួយទិន្នន័យគំរូ ការបញ្ចូលដែលឆ្លុះបញ្ចាំងCPU ចុង Qdrant នៅម៉ូដតំបន់ និងគ្មានឯកសារផ្ទាល់ខ្លួនក្រោមពពកទេ។

| ស៊េរី | កំណត់ត្រា | តម្រូវការ | ការផ្ទៀងផ្ទាត់ក្នុងតំបន់ |
| --- | --- | --- | --- |
| ស៊េរី 2 | [កំណត់ត្រា RAG បើកចំហ](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | ម៉ូដ Qdrant តំបន់ ស្វែងរក ការតម្រៀបឡើងវិញ និងការតភ្ជាប់ប្រភពត្រូវបានផ្ទៀងផ្ទាត់ |

ដើម្បីដំណើរការកំណត់ត្រានៅក្នុងតំបន់ បង្កើតបរិយាកាសវ៉ិរុឌហ្សួទៅហើយដំឡើងឯកសារតម្រូវការដូចគ្នា។ ដូចក្នុងឧទាហរណ៍៖

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## ទិន្នន័យគំរូ

កំណត់ត្រាអនុវត្តប្រើសំណុំឯកសារតូចមួយនៅក្នុង [sample_data](../../sample_data) ដើម្បីឱ្យតំរូវឯកសារស៊ីជម្រៅឯកជនឬពាក្យសម្ងាត់ក្រោមពពក។ មើល [sample_data/README.md](./sample_data/README.md) សម្រាប់ពិពណ៌នាបន្ថែម។

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## សង្ខេបការផ្ទៀងផ្ទាត់ក្នុងតំបន់

លទ្ធផលការផ្ទៀងផ្ទាត់ត្រូវបានកត់ត្រានៅក្នុងអត្ថបទនីមួយៗ និងក្នុង [SERIES_PLAN.md](./SERIES_PLAN.md)។

| ផ្នែក | លទ្ធផល |
| --- | --- |
| ផ្លូវ RAG បើកចំហ ស៊េរី 2 | FastEmbed បង្កើតការបញ្ចូលមាត្រដ្ឋាន 384 ទំហឹម ក្នុងតំបន់ Qdrant in-memory collection បានបញ្ចូលវ៉ិចទ័រ 8, ការតម្រៀបឡើងវិញប្រក្រតីបានយកផ្នែកដែលបានរំពឹង; ជម្រើសបង្កើត Ollama បានចប់ជាមួយ `phi4-mini:3.8b` |

កំណត់ត្រានៅក្នុងតំបន់នេះចៀសវាងកូដសម្ងាត់ដែលបានធ្វើឡើងដោយដៃ។

## ការបង្កើត Ollama នៅក្នុងតំបន់

កំណត់ត្រាស៊េរី 2 សុវត្ថិភាពក្នុងតំបន់ដោយលំនាំដើម។ ដើម្បីអនុញ្ញាតឱ្យបង្កើត Ollama ក្នុងតំបន់ ចម្លង [.env.example](../../.env.example) ទៅ .env ហើយបញ្ចូលតម្លៃសម្រាប់ស៊េរី 2។

សម្រាប់បង្កើត Ollama ស៊េរី 2 ផ្ដាច់វាគឺ៖

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

កំណត់ត្រាស៊េរី 2 ផ្ទុក `.env` ពីផ្នែកដើមឃ្លាំងដោយស្វ័យប្រវត្តិ ដោយប្រើ `python-dotenv`។

> [!IMPORTANT]
> កុំបញ្ជូនឯកសារ `.env` កើម្បីចូលចិត្តកូន API ចំណុចបញ្ចប់ឯកជន ឬតម្លៃជាក់លាក់ tenant។ ឃ្លាំងនេះបានរក្សារសម្ងាត់នៅក្រៅឯកសារ Markdown និងកំណត់ត្រា។

ឯកសារតម្រូវការត្រូវបានរាយការណ៍នៅក្នុង [requirements/README.md](./requirements/README.md)។

ដើម្បីផ្ទៀងផ្ទាត់តំណភ្ជាប់ រចនាសម្ព័ន្ធកំណត់ត្រា ការស្អាតនៃលទ្ធផលកំណត់ត្រា និងលំនាំសម្ងាត់មានហានិភ័យខ្ពស់៖

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

ស្គ្រីបផ្ទៀងផ្ទាត់ត្រូវបានរាយការណ៍នៅ [scripts/README.md](./scripts/README.md)។

ដើម្បីអនុវត្តន៍កំណត់ត្រទាំងអស់ដែលសុវត្ថិភាពក្នុងតំបន់ជាមួយបរិយាកាសតែមួយ៖

```powershell
python scripts\verify_notebooks.py --execute
```

ដំណើរការផ្ទៀងផ្ទាត់ដូចគ្នាត្រូវបានដំណើរការនៅ GitHub Actions នៅពេលដាក់លទ្ធផលនៅ pushed, pull requests និងដំណើរការដោយដៃ។ អត្ថបទដែលនៅជារចនាសម្ព័ន្ធ និងកំណត់ត្រាត្រូវបានច្រានចោលនៅផ្លូវផ្ទៀងផ្ទាត់សាធារណៈ។

មុនផ្សាយការអាប់ដេត ប្រើ [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)។

មើល [CHANGELOG.md](./CHANGELOG.md) សម្រាប់សង្ខេបផ្លាស់ប្តូរដែលមិនទាន់ផ្សាយ។

សម្រាប់មគ្គុទេសក៍អំពីការរួមចំណែក និងសុភាពភាពកំណត់ត្រា សូមមើល [CONTRIBUTING.md](./CONTRIBUTING.md)។

## គាំទ្រភាសាច្រើន

### គាំទ្រដោយ Co-op Translator (ស្វ័យកាល និងធ្វើអាប់ដេតជានិច្ច)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[អារ៉ាប់](../ar/README.md) | [បង់ក្លាឡា](../bn/README.md) | [ប៊ុលហ្គារី](../bg/README.md) | [ភាសាជាតិមួយម៉ានទី](../my/README.md) | [ចិន (អក្សរប្រែសម្រុក)](../zh-CN/README.md) | [ចិន (អក្សរបុរាណ, ហុងកុង)](../zh-HK/README.md) | [ចិន (អក្សរបុរាណ, ម៉ាកាវ)](../zh-MO/README.md) | [ចិន (អក្សរបុរាណ, តៃវ៉ាន់)](../zh-TW/README.md) | [ក្រូអាស៊ី](../hr/README.md) | [ចែក](../cs/README.md) | [ដាណីស](../da/README.md) | [ហូលង់](../nl/README.md) | [អេស្តូនី](../et/README.md) | [ហ្វាំងឡង់](../fi/README.md) | [បារាំង](../fr/README.md) | [ជर्मាន](../de/README.md) | [ក្រិច](../el/README.md) | [ហេប្រ៊ួ](../he/README.md) | [ហិណ្ឌា](../hi/README.md) | [ហុងគ្រី](../hu/README.md) | [ឥណ្ឌូនេស៊ី](../id/README.md) | [អ៊ីតាឡ៊ី](../it/README.md) | [ជប៉ុន](../ja/README.md) | [កណាដា](../kn/README.md) | [ខ្មែរ](./README.md) | [កូរ៉េខាងត្បូង](../ko/README.md) | [លីទុយអានី](../lt/README.md) | [ម៉ាឡៃ](../ms/README.md) | [ម៉ាឡាលាម](../ml/README.md) | [ម៉ារ៉ាធី](../mr/README.md) | [នេប៉ាល់](../ne/README.md) | [ភីឌជិន នៃនីហ្សេរ៉ា](../pcm/README.md) | [ន័រវែច](../no/README.md) | [ប៉ែ្ស្យែន (ហ្វាស៊ី)](../fa/README.md) | [ប៉ូឡូញ](../pl/README.md) | [ព័រទុយហ្គាល់ (ប្រែល)](../pt-BR/README.md) | [ព័រទុយហ្គាល់ (ប្រទេសប៉ូរទុយហ្គាល់)](../pt-PT/README.md) | [ប៊ុយជេ (Gurmukhi)](../pa/README.md) | [រ៉ូម៉ានី](../ro/README.md) | [រុស្ស៊ី](../ru/README.md) | [ស៊ែប៊ី (ស៊ីរីលិក)](../sr/README.md) | [ស្លូវ៉ាក់](../sk/README.md) | [ស្លូវេនី](../sl/README.md) | [អេស្ប៉ាញ](../es/README.md) | [ស្វាហ៊ីលី](../sw/README.md) | [ស៊ុយអែត](../sv/README.md) | [តាឡាហ្គោ (ហ្វីលីពីន)](../tl/README.md) | [តាម៉ីល](../ta/README.md) | [តេលូហ្គូ](../te/README.md) | [ថៃ](../th/README.md) | [ទួរគី](../tr/README.md) | [អ៊ុយក្រែន](../uk/README.md) | [អ៊ួដូ](../ur/README.md) | [វៀតណាម](../vi/README.md)

> **ចូលចិត្តចម្លងនៅក្នុងតំបន់មែនទេ?**
>
> ឃ្លាំងនេះមានការប្រែប្រាស់ភាសា​ជាង 50 ដែលបន្ថែមទំហំទាញយកយ៉ាងសំខាន់។ ដើម្បីចម្លងដោយគ្មានការប្រែប្រាស់ ប្រើ sparse checkout៖
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
> នេះផ្តល់ឱ្យអ្នកនូវអ្វីគ្រប់យ៉ាងដែលត្រូវការសម្រាប់បញ្ចប់វគ្គនេះជាមួយការទាញយកលឿនជាងមុន។
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**:
ឯកសារនេះត្រូវបានបម្លែងភាសា ដោយប្រើសេវាបម្លែងភាសា AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ទោះយើងខ្ញុំមានក្តីប្រាថ្នាឱ្យបានច្បាស់លាស់ តែសូមយល់ដឹងថាការបម្លែងដោយស្វ័យប្រវត្តិក៏អាចមានកំហុសឬភាពមិនត្រឹមត្រូវ។ ឯកសារដើមជាភាសាទីតាំងគួរត្រូវបានគេប្រើជាប្រភពច្បាស់លាស់។ សម្រាប់ព័ត៌មានសំខាន់ៗ សូមណែនាំឱ្យប្រើប្រាស់ការប្រែដោយមនុស្សជំនាញ។ យើងខ្ញុំមិនទទួលខុសត្រូវចំពោះការយល់ច្រឡំ ឬការបកស្រាយខុសបន្ទាប់ពីការប្រើប្រាស់ការបម្លែងនេះនោះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->