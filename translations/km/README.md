# បង្រៀន AI ឲ្យឆ្លើយសំនួរតាមឯកសាររបស់អ្នក

ឃ្លាំងនេះប្រមូលផ្តុំពីសេរីប្លក់ឆ្នាំ 2026 អំពីការបង្កើតប្រព័ន្ធ AI ដែលផ្អែកលើឯកសារជាមួយ RAG សេវាកម្ម Azure AI ជំនួសចំហ និងដំណើរការវាយតម្លៃ។

## ប្រវត្តិសាស្ត្រ

នៅឆ្នាំ 2023 ខ្ញុំបានបង្កើតមេរៀនគូពីរអំពីការបង្រៀន ChatGPT ឲ្យឆ្លើយសំនួរពីឯកសារ PDF ដោយប្រើ Azure AI Search និង Azure OpenAI គំនិត "ChatGPT លើទិន្នន័យរបស់អ្នក" នៅពេលនោះនៅតែមើលទៅថ្មី ហើយគោលបំណងគឺបង្ហាញផ្លូវការរបស់ការងារជាក់ស្តែង៖ រក្សាទុកឯកសារ រៀបចំ​បញ្ជី​សន្ទស្សន៍ ទាញយកមាតិកាសមរម្យ ហើយបង្កើតចម្លើយពីបរិបទដែលបានទាញយក។

នៅឆ្នាំ 2026 ប្រព័ន្ធ RAG ធំជាងមុន។ Azure AI Search គាំទ្ររបៀបទាញយកវ៉ិចទ័រ និងទាយការណ៍ចំរុះ វិធីសាស្ត្រ Azure OpenAI ជាផ្នែកមួយនៃប្រព័ន្ធ Microsoft Foundry Models ហើយឧបករណ៍ចំហដូចជា LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, និង vLLM បានក្លាយជជ្រើសរើសជាក់ស្តែងសម្រាប់ប្រព័ន្ធពិត។

នេះជាហេតុផលដែលខ្ញុំចង់ត្រឡប់មកពិភាក្សាពីប្រធានបទនេះម្តងទៀត។ សំនួរឥឡូវនេះមិនត្រឹមតែ "តើខ្ញុំនឹងបង្កើត RAG យ៉ាងដូចម្តេច?" ទេ។ មានវិធីជាច្រើនសម្រាប់បង្កើតវា ហើយសំនួរសំខាន់បំផុតគឺ "តើខ្ញុំនឹងជ្រើសរើសស្ថาปัตยกรรมណាសម្រាប់ស្ថានភាពរបស់ខ្ញុំ?"

សេរីនេះចាប់ផ្តើមពីស្រទាប់ការសម្រេចចិត្តនោះ មុននឹងចូលទៅកាន់ការអនុវត្ត វាអំពាវនាវមើលថា ហេតុអ្វី AI សេវាកម្មត្រូវការតាមដាន ទៀតពេលណា សេវាកម្មគ្រប់គ្រងដោយ Azure មានអត្ថន័យពេលណា ជំនួសចំហអាចសមរម្យនៅពេលណា ក៏ដូចជាកន្លែងដែលការបង្វឹកលម្អគួរតែទៅ។

## លិខិតប្រកាស

1. [សេរី ១៖ RAG, Azure នឹងជំនួសចំហ និងពេលណាការបង្វឹកលម្អមានអត្ថន័យ](./series-1-rag-azure-open-source-fine-tuning.md)

## ការគាំទ្រភាសាច្រើន

### គាំទ្រដោយ Co-op Translator (ស្វ័យក្រីយ និងធ្វើបច្ចុប្បន្នភាពជានិច្ច)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[អារ៉ាប៊ី](../ar/README.md) | [បង់ក្លា](../bn/README.md) | [ប៊ុលហ្គារី](../bg/README.md) | [ភូមា (មីយ៉ាន់ម៉ា)](../my/README.md) | [ចិន (សាមៀល)](../zh-CN/README.md) | [ចិន (ប្រពៃណី, ហុងកុង)](../zh-HK/README.md) | [ចិន (ប្រពៃណី, ម៉ាកាវ)](../zh-MO/README.md) | [ចិន (ប្រពៃណី, តៃវ៉ាន់)](../zh-TW/README.md) | [ក្រូអាត](../hr/README.md) | [ឆែក](../cs/README.md) | [ឌាណ្មាស](../da/README.md) | [ហូឡង់](../nl/README.md) | [អេស្តូនី](../et/README.md) | [ហ្វាំងឡង់](../fi/README.md) | [បារាំង](../fr/README.md) | [អាល្លឺម៉ង់](../de/README.md) | [ហ្គ្រីក](../el/README.md) | [ហេប្រ៊ូ](../he/README.md) | [ហินឌី](../hi/README.md) | [ហុងការ](../hu/README.md) | [ឥណ្ឌូណេស៊ី](../id/README.md) | [អ៊ីតាលី](../it/README.md) | [ជប៉ុន](../ja/README.md) | [កណាដា](../kn/README.md) | [ខ្មែរ](./README.md) | [កូរ៉េ](../ko/README.md) | [លីទុយអានី](../lt/README.md) | [ម៉ាឡេស៊ី](../ms/README.md) | [ម៉ាឡាយ៉ាលាំ](../ml/README.md) | [ម៉ារាធី](../mr/README.md) | [នេប៉ាល់](../ne/README.md) | [ភីលីពីនយ៉ាងនាយ៉េ](../pcm/README.md) | [ន័រវែស](../no/README.md) | [ភាសាអ៊ីរ៉ង់ (ផាស៊ី)](../fa/README.md) | [ប៉ូឡូញ](../pl/README.md) | [ព័រទុយហ្គាល់ (ប្រេស៊ីល)](../pt-BR/README.md) | [ព័រទុយហ្គាល់ (ប្រទេសព័រទុយហ្គាល់)](../pt-PT/README.md) | [ភាសាពន្ធជាបុរស (Gurmukhi)](../pa/README.md) | [រូម៉ានី](../ro/README.md) | [រុស្ស៊ី](../ru/README.md) | [សឺប៊ី (ស៊ីរីលិក)](../sr/README.md) | [ស្លូវ៉ាគី](../sk/README.md) | [ស្លូវែនី](../sl/README.md) | [អេស្បាញ](../es/README.md) | [ស្វាហ៊ីលី](../sw/README.md) | [ស្វីដិន](../sv/README.md) | [តាហ្គាឡូ (ហ្វីលីពីន)](../tl/README.md) | [តាមីល](../ta/README.md) | [តេលូហ្គូ](../te/README.md) | [ថៃ](../th/README.md) | [ទួគ្រី](../tr/README.md) | [អ៊ុយក្រែន](../uk/README.md) | [អ៊ឺដូ](../ur/README.md) | [វៀតណាម](../vi/README.md)

> **ចូលចិត្តចម្លងផ្ទាល់មែនទេ?**
>
> ឃ្លាំងនេះមានការប្រែជាភាសាច្រើនជាង ៥០ ដែលបង្កើនទំហំទាញយកយ៉ាងខ្លាំង។ ដើម្បីចម្លងដោយគ្មានការប្រែភាសា សូមប្រើ sparse checkout៖
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
> នេះនឹងផ្ដល់អ្វីៗដែលអ្នកត្រូវការដើម្បីបញ្ចប់វគ្គសិក្សាមួយដោយទាញយកបានលឿនជាងមុន។
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**:
ឯកសារនេះត្រូវបានបម្លែងភាសា ដោយប្រើសេវាបម្លែងភាសា AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ទោះយើងខ្ញុំមានក្តីប្រាថ្នាឱ្យបានច្បាស់លាស់ តែសូមយល់ដឹងថាការបម្លែងដោយស្វ័យប្រវត្តិក៏អាចមានកំហុសឬភាពមិនត្រឹមត្រូវ។ ឯកសារដើមជាភាសាទីតាំងគួរត្រូវបានគេប្រើជាប្រភពច្បាស់លាស់។ សម្រាប់ព័ត៌មានសំខាន់ៗ សូមណែនាំឱ្យប្រើប្រាស់ការប្រែដោយមនុស្សជំនាញ។ យើងខ្ញុំមិនទទួលខុសត្រូវចំពោះការយល់ច្រឡំ ឬការបកស្រាយខុសបន្ទាប់ពីការប្រើប្រាស់ការបម្លែងនេះនោះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->