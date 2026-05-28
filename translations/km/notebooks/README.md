# សៀវភៅកំណត់ត្រា

សៀវភៅកំណត់ត្រាទាំងនេះគាំទ្រប្រភេទអត្ថបទជាមួយឧទាហរណ៍អាចដំណើរការ។

| សៀវភៅកំណត់ត្រា | អត្ថបទ | គោលបំណង |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG កេលើក្បាលមុខទូទៅជាមួយ FastEmbed, របៀប Qdrant នៅក្នុងម៉ាស៊ីនមូលដ្ឋាន, ការទាញយក, ការរៀបចំឡើងវិញ, ជម្រើសបង្កើត Ollama, និងឯកសារឧទាហរណ៍ |

## ដំណើរការនៅក្នុងម៉ាស៊ីនផ្ទាល់ខ្លួន

ដំឡើងអ្វីដែលត្រូវការ​សម្រាប់​សៀវភៅកំណត់ត្រាដែលអ្នកចង់ដំណើរការ៖

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

ឬដំឡើង dependency ទាំងអស់៖

```powershell
python -m pip install -r requirements\all.txt
```

## ផ្ទៀងផ្ទាត់

ចេញពីឫសរ៉េប៉ូស៊ីតូរី៖

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Series 2 អាចអានការកំណត់រចនាសម្ព័ន្ធ Ollama ពីឯកសារ `.env` នៅឫសរ៉េប៉ូស៊ីតូរី។ ចាប់ផ្តើមពី [../.env.example](../../../.env.example) ដែលត្រូវបានចែកតាមប្រភេទ។

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**:
ឯកសារនេះត្រូវបានបម្លែងភាសា ដោយប្រើសេវាបម្លែងភាសា AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ទោះយើងខ្ញុំមានក្តីប្រាថ្នាឱ្យបានច្បាស់លាស់ តែសូមយល់ដឹងថាការបម្លែងដោយស្វ័យប្រវត្តិក៏អាចមានកំហុសឬភាពមិនត្រឹមត្រូវ។ ឯកសារដើមជាភាសាទីតាំងគួរត្រូវបានគេប្រើជាប្រភពច្បាស់លាស់។ សម្រាប់ព័ត៌មានសំខាន់ៗ សូមណែនាំឱ្យប្រើប្រាស់ការប្រែដោយមនុស្សជំនាញ។ យើងខ្ញុំមិនទទួលខុសត្រូវចំពោះការយល់ច្រឡំ ឬការបកស្រាយខុសបន្ទាប់ពីការប្រើប្រាស់ការបម្លែងនេះនោះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->