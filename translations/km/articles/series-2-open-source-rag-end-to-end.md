# បង្រៀន AI ឲ្យឆ្លើយសំណួរតាមឯកសាររបស់អ្នក
## ស៊េរី 2: បង្កើតប្រព័ន្ធ RAG តំបន់មូលដ្ឋានបើកអាចប្រើបានចាប់ពីដើមដល់ចប់

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> អាយអត្ថបទនេះបំលែងការពិភាក្សាស្ថាបត្យកម្មនៅក្នុងស៊េរី 1 ទៅជាបទបង្ហាញ RAG តំបន់មូលដ្ឋានអាចបើកហើយអាចដំណើរការ។ គោលបំណងគឺបង្កើតលំហូរការងារពេញលេញជាមុនជាមួយទិន្នន័យគំរូ ដោយគ្មានគណនីមេឃ និងគ្មានសម្ងាត់ បន្ទាប់មកប្រើបន្ទាត់មូលដ្ឋានដែលដំណើរការបាននោះ ដើម្បីធ្វើការសម្រេចចិត្តស្ថាបត្យកម្មល្អប្រសើរជាងមុន។

ប្រព័ន្ធដែលយើងនឹងបង្កើតគឺជាជំនួយការទ្រឹស្តីសាលាខ្នាតតូច។ ខ្ញុំប្រើឯកសារ Markdown រងពីរ ដែលជាគ្រឹះចំណេះដឹង បន្ទាប់មកដើរឆ្ពោះតាមលំហូរ RAG ពេញលេញ៖ ការបំបែកប្លុកខ្លឹមសារ បង្កើត embedding បែបតំបន់មូលដ្ឋាន ការផ្ទុកទិន្នន័យ Qdrant vector ការទាញយក ការរៀបចំឡើងវិញ តម្លើងចម្លើយដោយយោងឯកសារ និងការបង្កើតចម្លើយជាគ្រាប់អង្ករ ជាជម្រើសជាមួយ Ollama និង Phi-4-mini។

ការរុករកស៊េរី: [ទំព័រដើមស្ទុកកូដ](../README.md) | មុននេះ៖ [ស៊េរី 1 - RAG, Azure ប្រៀបធៀបជាមួយជម្រើសបើកប្រភព និងពេលណាដើម្បី fine-tune ដែលមានអត្ថប្រយោជន៍](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | តម្រូវការ: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> នេះជាចំណុចចាប់ផ្តើមល្អបំផុត ប្រសិនបើអ្នកចង់យល់ពីលំហូរ RAG មុនពេលបង្កើតធនធានមេឃ។ ផ្លូវផ្ទាល់មុខដំណើរការនេះដំណើរការបែននៅលើកុំព្យូទ័រផ្ទាល់ ជាមួយ embedding ដែលសម្រួល CPU និងគ្មានសម្ងាត់។

## 1. អ្វីដែលយើងកំពុងបង្កើត

នៅក្នុងមេរៀនឆ្នាំ 2023 ខ្ញុំចាប់ផ្តើមពី Azure ព្រោះគោលបំណងគឺបង្ហាញពីរបៀបដែល Azure AI Search និង Azure OpenAI អាចឆ្លើយសំណួរពីឯកសារ PDF។

សម្រាប់ស៊េរីឆ្នាំ 2026 នេះ ខ្ញុំចង់ចាប់ផ្តើមពីកម្រិតខ្នាតតូចជាងនេះមួយជាន់។

មុនប្រើសេវាដំណោះស្រាយដែលគ្រប់គ្រង ខ្ញុំចង់បង្កើតប្រព័ន្ធ RAG តំបន់មូលដ្ឋានតូចមួយហើយបង្ហាញគ្រប់ជំហាន៖ ការបញ្ចូលឯកសារ ការបំបែកខ្លឹមសារ ការផ្ទុកវ៉ិចទ័រ ការទាញយកភស្តុតាង ការរៀបចំឡើងវិញ ចម្លើយដែលយោងឯកសារបាន និងជម្រើសបង្កើតចម្លើយតាមតំបន់ភាពជាមួយ Ollama និង Phi-4-mini។

សញ្ញាឧទាហរណ៍គឺជាជំនួយការប្រព័ន្ធទ្រឹស្តីសាលា។ អ្នកប្រើសួរ៖

```text
Can I use generative AI for my final assignment?
```

ប្រព័ន្ធមិនគួរឆ្លើយពីចំណាំម៉ូដែលទូទៅទេ។ វាត្រូវតែទាញយកផ្នែកគោលនយោបាយដែលពាក់ព័ន្ធ ហើយឆ្លើយពីភស្តុតាងនោះ។

កំណែដំណើរការពេញលេញមាននៅក្នុង [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)។ កូដខាងក្រោមបង្ហាញជំហានសំខាន់ៗ ដើម្បីអត្ថបទនេះអាចអានជាមេរៀនបាន។

## 2. ដំឡើងអាស្រ័យភាពតំបន់មូលដ្ឋាន

បង្កើតបរិយាកាសវេរ៉ូខ្វាល់ ហើយដំឡើងតម្រូវការស៊េរី 2៖

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

កំណែដំបូងប្រើម៉ូដ Qdrant តំបន់មូលដ្ឋាន និង FastEmbed។ ឧបករណ៍ Python របស់ Qdrant គាំទ្រម៉ូដតំបន់មូលដ្ឋានក្នុងចំណោមម៉emory ជាមួយ `QdrantClient(":memory:")` ដែលមានប្រយោជន៍សម្រាប់មេរៀនតំបន់មូលដ្ឋាន និងការត្រួតពិនិត្យព стиле CI ។ FastEmbed ផ្តល់ម៉ូដែល embedding តំបន់មូលដ្ឋានពិតដោយគ្មានការទាមទារកូនសោ API មេឃ។

ឯកសារតម្រូវការនេះរួមបញ្ចូល `python-dotenv` ដោយសារតែ notebook អាចអានឈ្មោះម៉ូដែល Ollama ពី `.env` ។ គ្មានតម្រូវកូនសោ API Azure OpenAI ឬ OpenAI សម្រាប់មេរៀននេះទេ។

## 3. ផ្ទុកឯកសារគំរូ

គម្រូងគំរូតិចតួចដោយចេតនាចង់តូច៖

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

នៅក្នុង notebook ខ្ញុំផ្ទុកឯកសារ Markdown ទាំងអស់ពី `sample_data/`៖

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

ពេលខ្ញុំរត់ notebook វាបានផ្ទុកឯកសារ 2 ហើយ។ នេះតិចគ្រប់គ្រាន់ដល់ការត្រួតពិនិត្យដោយដៃដែលមានប្រយោជន៍នៅពេលបង្កើតកំណែ RAG ដំបូង។

## 4. បំបែកតាមក្បាល Markdown

ជំហានបន្ទាប់គឺបំបែកឯកសារ ទៅជាប្លុកខ្លឹមសារ។

សម្រាប់មេរៀននេះ ខ្ញុំប្រើក្បាល Markdown ជាសញ្ញាសំណុំរចនាសម្ព័ន្ធ។ចំណងជើងឯកសារមកពី `#` ហើយប្លុកផ្នែកមួយមកពី `##` ។

> [!NOTE]
> ការបំបែកមិនមែនសម្រួលតែមួយទេទៅគ្រប់ករណី។ ក្នុងមេរៀននេះ ខ្ញុំប្រើក្បាល Markdown ព្រោះឯកសារគំរូមានរចនាសម្ព័ន្ធ `#` និង `##` ច្បាស់លាស់។ សម្រាប់ PDF, ឯកសារ Word, ស្លាយ, សំបុត្រ ឬគេហទំព័រ យន្តការល្អប្រសើរអាចប្រើព្រំដែនទំព័រ ឬព័ត៌មានរចនាសម្ព័ន្ធ ផ្នែកមានអត្ថន័យ ទំហំ token តារាង ឬ metadata ។ ចំណុចសំខាន់គឺជ្រើសយុទ្ធសាស្ត្របំបែកដែលរក្សាទុកអត្ថន័យ និងអាចតាមដានប្រភពឯកសារបាន។

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

បន្ទាប់ហើយដាក់អនុវត្តនៅលើឯកសារទាំងអស់៖

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

នេះបានបង្កើតប្លុក 8 នៅក្នុងការរត់តំបន់មូលដ្ឋានរបស់ខ្ញុំ។

អ្វីដែលខ្ញុំចូលចិត្តអំពីជំហាននេះគឺ metadata មានប្រយោជន៍រួចទៅហើយ។ ប្លុកនីមួយៗដឹង `source`, `sectionHeading`, `documentVersion` និង placeholder `permissions` របស់ខ្លួន។ ទោះបីជាមេរៀនតិចតួចក៏ដោយ វា ធ្វើឲ្យករណីយោង និងការទាញយកដោយគិតពីសិទ្ធិ នៅពេលក្រោយងាយស្រួលឡើង។

## 5. បង្កើត Embeddings តំបន់មូលដ្ឋាន

សម្រាប់កំណែសាធារណៈដំបូង ខ្ញុំប្រើ `BAAI/bge-small-en-v1.5` តាមរយៈ FastEmbed។

នេះរក្សាមេរៀននៅតំបន់មូលដ្ឋាន និងសម្រួល CPU ប៉ុន្តែមិនមែនជាការប្រើម៉ូដែល embedding មួយគូតទទេ។ ការរត់ដំបូងទាញយកទម្ងន់ម៉ូដែល។ បន្ទាប់មក notebook អាចប្រើតាមកម្សាន្តជាតំបន់មូលដ្ឋានម្តងទៀត។

> [!NOTE]
> ខ្ញុំប្រើ `BAAI/bge-small-en-v1.5` ព្រោះវាជាម៉ូដែល embedding ភាសាអង់គ្លេសស្រាលដែលដំណើរការល្អជាមួយ FastEmbed និង Qdrant សម្រាប់មេរៀនតំបន់មូលដ្ឋាន។ វាបង្កើតវ៉ិចទ័រប្រវែង 384 ប៉ារ៉ាម៉ែត្រ ដែលរក្សាដំណើរការដោយលឿន និងថ្លៃតិចសម្រាប់រត់ក្នុងតំបន់មូលដ្ឋាន។ វាមិនមែនជាជម្រើសល្អតែមួយទេ។ នៅឆ្នាំ 2023 មេរៀនជាច្រើនបានប្រើម៉ូដែល embeddingដែលភ្ជាប់ជាមួយ cloud ដូចជា `text-embedding-ada-002`។ នៅពេលនេះ ជម្រើសថ្មីៗមានដូចជា OpenAI `text-embedding-3-small` និង `text-embedding-3-large` និងជម្រើសបើកប្រភពដូចជា BGE, E5, MiniLM, Nomic Embed និងម៉ូដែលមួយចំនួន multilingual ដូចជា `BAAI/bge-m3` ដោយស្រាប់តែជ្រើសយ៉ាងហោចណាស់តាមបរិមាណធនធាន។ ក្នុងការផលិត យ៉ាងណាក៏ដោយ ម៉ូដែល embedding ដែលត្រឹមត្រូវគួរត្រូវបានជ្រើសតាមតម្លៃការពិនិត្យការទាញយកលើឯកសាររបស់អ្នក។

ជម្រើសនៃផ្សេងទៀតដែលប្រើបាន៖

| គ្រួសារម៉ូដែល | ពេលដែលខ្ញុំចង់ពិចារណា |
| --- | --- |
| `text-embedding-ada-002` | ស្ថាបត្យកម្មបម្រុងដ៏ចាស់ ដែលបានប្រើនៅមេរៀនណែនាំជាច្រើនក្នុងឆ្នាំ 2023។ ខ្ញុំមិននឹងជ្រើសវាជាលំនាំដើមសម្រាប់មេរៀនថ្មីនៅថ្ងៃនេះទេ។ |
| `text-embedding-3-small` | លំនាំដើមសាកល្បង ដែលមានតុល្យភាពថ្លៃ/ប្រសិទ្ធភាពខ្លាំងពេលខ្ញុំមិនចាំបាច់មាន embedding តំបន់មូលដ្ឋានតែប៉ុណ្ណោះ។ |
| `text-embedding-3-large` | ជម្រើសដែលអ្នកផ្សាយពាណិជ្ជកម្មពេលដែលគុណភាពការទាញយកសំខាន់ជាងទំហំវ៉ិចទ័រ ឬថ្លៃ embedding។ |
| `BAAI/bge-small-en-v1.5` | ម៉ូដែល embedding ភាសាអង់គ្លេសស្រាល តំបន់មូលដ្ឋាន សម្រាប់មេរៀន ប្រភ័ន្ធគំរូ និងការពិសោធន៍សម្រួល CPU។ |
| `BAAI/bge-base-en-v1.5` ឬ `BAAI/bge-large-en-v1.5` | ម៉ូដែល embedding អង់គ្លេសធំជាងសម្រាប់ការទាញយកល្អប្រសើរ នឹងអាចងាយសល់ថវិកា CPU ពីរចនាសម្ព័ន្ធក្រោយ។ |
| `BAAI/bge-m3` | វិធីទាញយកបានច្រើនភាសា ឬបរិបទវែង ជាពិសេសពេលឯកសារមិនមែនមានតែលើភាសាអង់គ្លេសទេ។ |
| `sentence-transformers/all-MiniLM-L6-v2` | ម៉ូដែល semantic search តូច និងលឿន ដែលមានប្រយោជន៍ពេលល្បឿន និងភាពសាមញ្ញមានសារៈសំខាន់។ |
| `nomic-embed-text-v1.5` | ជម្រើស embedding តំបន់មូលដ្ឋានបើកប្រភព ដែលគួរតេស្តសម្រាប់បរិបទវែង ឬការដំឡើងដែលអាចចល័តបាន។ |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

បន្ទាប់ពីនេះ ឆ្នែកគ្រប់ប្លុកជាមួយ embedding:

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. ផ្ទុកវ៉ិចទ័រនៅម៉ូដ Qdrant តំបន់មូលដ្ឋាន

ឥឡូវនេះ យើងបង្កើតស្រង់ Qdrant ដែលស្ថិតក្នុងចំណោមម៉emory ហើយបញ្ចូលប្លុកជាមួយ metadata ទាញសំណុំ។

> [!NOTE]
> នៅក្នុងមេរៀនឆ្នាំ 2023 ខ្ញុំបានប្រើ FAISS ព្រោះវាជាវិធីសាមញ្ញ ហើយពេញនិយមសម្រាប់បង្ហាញការស្វែងរកវ៉ិចទ័រតំបន់មូលដ្ឋានជាមួយ LangChain។ FAISS នៅតែមានប្រយោជន៍សម្រាប់ការពិសោធរហ័សនៅតំបន់មូលដ្ឋាន។ នៅកំណែឆ្នាំ 2026 នេះ ខ្ញុំប្រើ Qdrant ព្រោះចង់ឲ្យមេរៀនមានអារម្មណ៍ជិតប្រព័ន្ធ RAG ផលិតកម្មកាន់តែច្រើន។ Qdrant អនុញ្ញាតឲ្យផ្ទុកវ៉ិចទ័រជាមួយ metadata ដូចជាឯកសារប្រភព ក្បាលផ្នែក កំណែឯកសារ និងសិទ្ធិ។ វាធ្វើឲ្យការទាញយកងាយស្រួលត្រួតផង ហើយរៀបចំបរិស្ថានឧទាហរណ៍សម្រាប់តម្រង ការយោង និងការបញ្ចូលក្នុងការដំឡើងវេទិកាចក្រ ឬម៉ាស៊ីនមេនៅពេលក្រោយ។

FAISS ល្អសម្រាប់បង្ហាញការស្វែងរកវ៉ិចទ័រដូចគ្នា។ Qdrant ល្អសម្រាប់បង្ហាញជាន់ស្រទាប់ RAG តូចដែលមានសមាសភាពផលិតកម្ម។

ជម្រើសផ្សេងទៀត៖

| កន្លែងផ្ទុកវ៉ិចទ័រ / ជាន់ស្វែងរក | ពេលដែលខ្ញុំចង់ពិចារណា |
| --- | --- |
| Qdrant | ការសាកល្បងតំបន់មូលដ្ឋាន ការតម្រង metadata ស្វែងរកវ៉ិចទ័រដែលសមរម្យក្នុងផលិតកម្ម និងលំហូរការងារ Python ដែលសាមញ្ញ។ |
| Chroma | ការសាកល្បង RAG តំបន់មូលដ្ឋានរហ័ស និង notebook ដែលភាពសាមញ្ញសំខាន់បំផុត។ |
| FAISS | ការស្វែងរកវ៉ិចទ័រតំបន់មូលដ្ឋានស្រាល ពេលខ្ញុំត្រូវការស្វែងរកដូចគ្នាទេ ហើយអាចគ្រប់គ្រង metadata ផ្សេងទៀតបាន។ |
| Milvus | ស្វែងរកវ៉ិចទ័រចម្រុះតំបន់មូលដ្ឋានកំណិនធំ ពេលក្រុមហ៊ុនត្រៀមខ្លួនដំណើរការទិន្នន័យវ៉ិចទ័រផ្តាច់មុខ។ |
| Weaviate | ស្វែងរកវ៉ិចទ័រជាមួយស្កីម៉ា, metadata, ស្វែង hybrid និងជម្រើសដំឡើងគ្រប់គ្រង ឬដំឡើងដោយខ្លួនឯង។ |
| Azure AI Search | RAG សហគ្រាសនៅលើ Azure ពេលខ្ញុំចង់បានការស្វែងរកពាក្យគន្លឹះ ស្វែងរកវ៉ិចទ័រ ស្វែង hybrid, ចំណាត់ថ្នាក់ល្បឿន, តម្រង, សុវត្ថិភាព និងដំណើរការគ្រប់គ្រងក្នុងជាន់ស្វែងរកតែមួយ។ |
| PostgreSQL + pgvector | ក្រុមដែលមានប្រើ PostgreSQL រួចហើយ ហើយចង់បានស្វែងរកវ៉ិចទ័របន្តិចជិតទិន្នន័យកម្មវិធី។ |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

បន្ទាប់បញ្ចូលចំណុច:

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

ក្នុងការរត់របស់ខ្ញុំ ស្រង់បានបញ្ចូលវ៉ិចទ័រ 8។

នេះជាចន្លោះដែលប្រព័ន្ធ RAG ចាប់ផ្តើមអាចត្រូវបានពិនិត្យបាន។ ឃ្លាំងទិន្នន័យវ៉ិចទ័រមិនត្រឹមតែផ្ទុកវ៉ិចទ័រទេ តែផ្ទុកអត្ថបទភស្តុតាង និង metadata ដែលចាំបាច់សម្រាប់ការយោង។

## 7. ទាញយកប្លុកជម្រើស

ឥឡូវនេះ យើងសួរសំណួរ ហើយទាញយកប្លុកជម្រើស។

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

នៅចំណុចនេះ ខ្ញុំបោះពុម្ពប្លុកដែលបានទាញមកមុនបង្កើតចម្លើយ។ នេះសំខាន់។ ប្រសិនបើការទាញយកខុស ចម្លើយនឹងលាក់បញ្ហា តែមានអត្ថបទដែលហាមឃាត់។

## 8. បន្ថែមកម្មវិធីរៀបចំឡើងវិញស្រាល

ពេលខ្ញុំបានសាកល្បងផ្លូវទាញយកដំបូង ការស្រដៀងវ៉ិចទ័រតែប៉ុណ្ណោះបានរកមាតិការគោលនយោបាយដែលពាក់ព័ន្ធ ប៉ុន្តែផ្នែកដ៏ត្រឹមត្រូវមិនអាចស្ថិតនៅលំដាប់ខ្ពស់ជានិច្ច។

ដូច្នេះ ខ្ញុំបានបន្ថែមកម្មវិធីរៀបចំឡើងវិញតំបន់មូលដ្ឋានតូចមួយ។ វាផ្តល់ទំងន់បន្ថែមពេលពាក្យសំណួរចម្រុះជាមួយក្បាលផ្នែក និងខ្លឹមសារ។

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

បន្ទាប់ពីរៀបចំឡើងវិញ លទ្ធផលលំដាប់ដំបូងកើតឡើង៖

```text
school_ai_policy.md / Final Assignments
```

នេះជាផ្នែកដែលរំពឹងទុកសម្រាប់សំណួរតេស្ត។

នេះជាបទពិសោធន៍មានប្រយោជន៍បំផុតពីការអនុវត្តដំបូង។ ទោះបីជាគំរូតំបន់មូលដ្ឋានតូចមួយ ការទាញយកមានគុណភាពកាន់តែប្រសើរនៅពេលខ្ញុំបញ្ចូលការស្រដៀងវ៉ិចទ័រជាមួយសញ្ញាផ្សេងទៀត។

## 9. លាយចម្លើយតំបន់មូលដ្ឋានដែលមានមូលដ្ឋានយ៉ាងច្បាស់

សម្រាប់ផ្លូវលំនាំដើម ខ្ញុំប្រើកម្មវិធីលាយចម្លើយតំបន់មូលដ្ឋានតែស្រស់មិនប្រើ LLM។

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

នេះគឺមិនមែនជាឧបករណ៍បង្កើតចម្លើយផលិតផលចុងក្រោយទេ។ វាអាចជួយកែកំហុស។ វាបញ្ជាក់ថាការទាញយក, metadata និងការយោងដំណើរការល្អ មុនពេលបន្ថែមស្រទាប់ចម្លើយម៉ូដែល។

## 10. បង្កើតចម្លើយតំបន់មូលដ្ឋានជាមួយ Ollama និង Phi-4-mini

ខណៈពេលការទាញយកដំណើរការបាន notebook អាចជំនួស​តែកំហ៊ានចម្លើយចុងក្រោយជាមួយ Ollama និង `phi4-mini:3.8b` ។

> [!NOTE]
> Ollama គួរជំនួសតែកំហ៊ានបង្កើតចម្លើយចុងក្រោយប៉ុណ្ណោះ។ ការផ្ទុកឯកសារ ការបំបែក ខ្ទង់វ៉ិចទ័រ ការទាញយក ការរៀបចំឡើងវិញ និងការយោងគួរតែរក្សាដូចដើម។

ដំបូង notebook បង្កើត prompt ភស្តុតាងពីប្លុកដែលបានទាញយក៖

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

សម្រាប់មេរៀននេះ ខ្ញុំផ្តល់អនុសាសន៍គ្រួសារម៉ូដែល Phi-4-mini របស់ Microsoft តាមរយៈ Ollama ជាជម្រើសបង្កើតចម្លើយតំបន់មូលដ្ឋានលំនាំដើម។ នៅ Ollama ម៉ូដែលដែលខ្ញុំបានសាកល្បងគឺ៖

```powershell
ollama pull phi4-mini:3.8b
```

អ្នកអាចពិនិត្យឆាប់ថាម៉ូដែលមានទេ៖

```powershell
ollama list
```

បន្ទាប់មកកំណត់អថេរទាំងនេះ៖

```powershell
Copy-Item .env.example .env
```

បើក `.env` ហើយដកស្ដោតតម្លៃ Ollama ស៊េរី 2៖

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

notebook អាន `.env` ពីឫសស្ទុកកូដជាមួយ `python-dotenv` បន្ទាប់ចេញផ្ញើ prompt ផ្ទាំងភស្តុតាងទៅ Ollama តាមរយៈ endpoint `/api/chat` នៅតំបន់មូលដ្ឋានហើយបិទការចាក់ចម្រាសការផ្ទាល់। ប្រសិនបើ Ollama មិនដំណើរការឬ `SERIES2_OLLAMA_MODEL` បាត់បង់ត្រាប់វាគឺខ្វះចេញ។

> [!NOTE]
> នៅលើម៉ាស៊ីននេះ `phi4-mini:3.8b` ទាញយកឯកសារម៉ូដែលប្រមាណ 2.49GB។ ខណៈពេលសម្រួល Ollama រាយការណ៍ទម្ងន់ម៉ូដែលបានដោនឡើង 3.3GB និងប្រើ GPU RTX 3060 Laptop។

នេះផ្តល់មេរៀនពីកម្រិត ២៖

1. កម្មវិធីលាយចម្លើយសម្ងាត់ CPU តែមួយ។
2. បង្កើតចម្លើយតំបន់មូលដ្ឋានជាមួយ Ollama និង Phi-4-mini។

លំហូរការទាញយកនៅដដែលទាំងពីរ។

## 11. លទ្ធផលបញ្ជាក់

ខ្ញុំបានរត់ notebook នៅតំបន់មូលដ្ឋានលើ Windows ជាមួយ Python 3.12.6។

ចំណតដែលបានដំឡើង៖

| កញ្ចប់ | កំណែ |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

ការប្រតិបត្ដិ notebook៖

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- លទ្ធផលប្រតិបត្ដិ: ត្រូវបានកំណត់ជាមួយ `nbclient`
- ឯកសារ ត្រូវបានផ្ទុក: 2
- ប្លុកបានបង្កើត: 8
- ក្រុមពី Qdrant: `school_policy_local`
- វ៉ិចទ័របញ្ចូល: 8
- ម៉ូដែល embedding: `BAAI/bge-small-en-v1.5`
- ទំហំ embedding: 384
- Retrieval question: "តើខ្ញុំអាចប្រើប្រាស់ AI បង្កើតសម្រាប់ការងារផ្ទាល់ខ្លួនចុងក្រោយរបស់ខ្ញុំបានទេ?"
- Reranking path: ការរៀបចំឡើងវិញភាសាដំណាក់កាលតាមបំណែកក្នុងស្រុក
- Top retrieved source after reranking: `school_ai_policy.md`
- Top retrieved section after reranking: `Final Assignments`
- Default answer path: local transparent answer composer
- Ollama generation path: completed with `phi4-mini:3.8b`
- Ollama model file size: 2.49GB on disk
- Ollama loaded model size: 3.3GB reported by `ollama ps`
- GPU offload: 100% GPU reported by `ollama ps`
- GPU memory observed after generation: about 3.5GB of 6GB used on RTX 3060 Laptop GPU
- Notebook execution with cached FastEmbed model and Ollama generation enabled: passed in about 34 seconds through the verification script

The Ollama-generated answer was:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

ខ្ញុំមិនចាត់ទុកចម្លើយនេះថាល្អបំផុតទេ។ វាឆ្លើយតបពីភស្តុតាងត្រឹមត្រូវ ប៉ុន្តែខ្សែប្រភពចុងក្រោយមិនច្បាស់លាស់ដូចទ្រង់ទ្រាយយោងតាមការបញ្ជាក់ដោយច្បាស់លាស់ទេ។ វាមានប្រយោជន៍ក្នុងការបង្ហាញនៅក្នុងមេរៀនដោយសារវាធ្វើឱ្យសំណួរបច្ចេកទេសបន្ទាប់ក្លាយទៅជាប្រសិទ្ធភាព: ការបង្កើតចម្លើយត្រូវការការវាយតម្លៃផងដែរ មិនមែនត្រឹមតែការទាញយកទេ។

អ្វីដែលខ្ញុំបានរៀនរបស់កំឡុងពេលបញ្ចាក់នេះគឺថាគុណភាពការទាញយកគួរត្រូវបានពិនិត្យមុនការបង្កើតចម្លើយ។ លទ្ធផល embedding មានប្រយោជន៍រួចហើយ និងកម្មវិធីរៀបចំឡើងវិញភាសាដំបូងបានធ្វើឲ្យវាលំបាកក្នុងការបង្ហាញផ្នែកគោលនយោបាយដែលរំពឹងទុកឡើងជាលើកដំបូង។ នេះជាការប្រព្រឹត្តន៍ប្រព័ន្ធតូចដែល​ខ្ញុំ​ចង់ឲ្យមេរៀនបង្ហាញជំនួសការលាក់បាំង។

## ១២. តើអ្វីជាមុខដែលនៅមុខ

ការកែលម្អបន្ទាប់គឺប្រៀបធៀបការតំឡើងក្នុងស្រុកនេះជាមួយនឹងកំណែ Azure ដែលគ្រប់គ្រងរបស់ស្ថានការណ៍ជំនួយគោលនយោបាយសាលាប្រភេទដូចគ្នា។ ការរក្សាស្ថានការណ៍អោយទៀងទាត់គួរធ្វើឲ្យការប្រៀបធៀបលម្អងឡើង្នូវងាយស្រួល: ភាពស្មុគស្មាញនៃការដំឡើង ការត្រួតពិនិត្យការទាញយក ការចូលរួមរបស់អត្តសញ្ញាណ ការទទួលខុសត្រូវប្រតិបត្តិការ និងថ្លៃដើម។

## ១៣. ឲ្យយោង

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub repository](https://github.com/qdrant/qdrant-client)
- [FastEmbed supported models](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 model card](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 model card](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini model page](https://ollama.com/library/phi4-mini)
- [Ollama Windows documentation](https://docs.ollama.com/windows)
- [Ollama API streaming documentation](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct model card](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph)
- [Introduction to RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Previous: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**:
ឯកសារនេះត្រូវបានបម្លែងភាសា ដោយប្រើសេវាបម្លែងភាសា AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ទោះយើងខ្ញុំមានក្តីប្រាថ្នាឱ្យបានច្បាស់លាស់ តែសូមយល់ដឹងថាការបម្លែងដោយស្វ័យប្រវត្តិក៏អាចមានកំហុសឬភាពមិនត្រឹមត្រូវ។ ឯកសារដើមជាភាសាទីតាំងគួរត្រូវបានគេប្រើជាប្រភពច្បាស់លាស់។ សម្រាប់ព័ត៌មានសំខាន់ៗ សូមណែនាំឱ្យប្រើប្រាស់ការប្រែដោយមនុស្សជំនាញ។ យើងខ្ញុំមិនទទួលខុសត្រូវចំពោះការយល់ច្រឡំ ឬការបកស្រាយខុសបន្ទាប់ពីការប្រើប្រាស់ការបម្លែងនេះនោះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->