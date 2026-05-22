# သင့်စာရွက်စာတမ်းများအပေါ် အခြေခံ၍ AI ကို မေးခွန်းများကို ဖြေဆိုနိုင်ရန် သင်ကြားပါ
## စီးရီး 2: အပြည့်အစုံ အတွင်း ဒေသတွင်း Open-Source RAG စနစ် တည်ဆောက်ခြင်း

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> အဆိုပါဆောင်းပါးသည် စီးရီး 1 ၏ ဂေါ်ဖြစ်ပုံဆွေးနွေးချက်ကို ဒေသတွင်း RAG သင်ခန်းစာ အဖြစ် ပြောင်းလဲထားသည်။ ရည်ရွယ်ချက်မှာ နမူနာဒေတာဖြင့် ပထမဦးစွာ အပြည့်အစုံလုပ်ဆောင်မှုကို တည်ဆောက်ခြင်းဖြစ်ပြီး၊ မိုးကောင်းကင်အကောင့်မလိုအပ်ဘဲ ၊ လျှိုင်းလျှော်ချက်မပါဘဲ အလုပ်လုပ်စေပြီး ထိုအခြေခံကို စနစ်ပိုင်းဆိုင်ရာ ဆုံးဖြတ်ချက်များ လုပ်နိုင်ရန်ဖြစ်သည်။

ကျွန်ုပ်တို့ တည်ဆောက်မည့် စနစ်မှာ ကျောင်းမူဝါဒ အကူအညီဖြစ်သည်။ ဒေသတွင်း Markdown စာရွက်စာတမ်း ၂ ခုကို အသုံးပြုကာ နောက်ထပ် RAG စနစ် လုံးဝလမ်းကြောင်းကို လိုက်ပါမည် - ချန်က်၊ ဒေသစွဲ အထည်ဖော်ခြင်း၊ Qdrant vector သိုလှောင်မှု၊ ရယူခြင်း၊ ပြန်စီခြင်း၊ အရင်းအမြစ် သိရှိမှု ဖြေဆိုချက် စပ်ဆိုင်မှုနှင့် စိတ်ကြိုက် ဒေသတွင်း စက်မှုလုပ်ငန်း ဒေါင်လိုဒ်ဖြင့် Ollama နှင့် Phi-4-mini အသုံးပြုပြီး ထုတ်လုပ်ခြင်း။

စီးရီးလမ်းကြောင်း: [Repository home](../README.md) | ယခင်: [Series 1 - RAG, Azure vs Open-Source Alternatives, and When Fine-Tuning Makes Sense](./series-1-rag-azure-open-source-fine-tuning.md)

စုစုပေါင်းအကြောင်းအရာ: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | လိုအပ်ချက်များ: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> မိုးကောင်းကင်အရင်းအမြစ် မဟုတ်ဘဲ RAG လမ်းကြောင်းကို နားလည်လိုသူများအတွက် အကောင်းဆုံး စတင်ပုံဖြစ်သည်။ ပုံမှန်လမ်းကြောင်းမှာ ဒေသတွင်း (local) CPU-ကိုဖြစ်ဖွယ် Embedding များနှင့် လျှိုင်းလျှော်ချက် မပါဘဲ လုပ်ဆောင်မည်ဖြစ်သည်။

## 1. ကျွန်ုပ်တို့ တည်ဆောက်မည့် အရာ

2023 သင်ခန်းစာတွင် Azure မှ စတင်ခဲ့သည်။ ရည်ရွယ်ချက်မှာ Azure AI Search နှင့် Azure OpenAI က PDF စာရွက်စာတမ်းမှ မေးခွန်းများကို ဖြေဆိုပုံကို ပြသရန်ဖြစ်သည်။

2026 စီးရီးအတွက် ဤအလွှာ များထပ်ရုပ်၍ စတင်လိုသည်။

စီမံခန့်ခွဲထားသော ဝန်ဆောင်မှုများအသုံးမပြုမီ၊ ငါသည် ဂျပန် RAG စနစ်တစ်ခုကို ဒေသတွင်းသပ်ရပ်စွာ တည်ဆောက်၍ အဆင့်တိုင်းကို မြင်ရစေချင်သည် - စာရွက်စာတမ်းများကို ဖွင့်၍ ၊ စာသား ချန်က်ခြင်း၊ ဗက်တာများကို သိုလှောင်ခြင်း၊ သက်သေ ရယူခြင်း၊ ပြန်စီခြင်းနှင့် အရင်းအမြစ်အပေါ်အခြေခံ ဖြေဆိုချက် ပြန်ပေးခြင်း။

နမူနာ အခြေအနေမှာ ကျောင်းမူဝါဒအကူအညီဖြစ်သည်။ အသုံးပြုသူ မေးမြန်းသည်-

```text
Can I use generative AI for my final assignment?
```

စနစ်သည် ယေဘုယျ မော်ဒယ်မှတ်ဉာဏ်မှ မဖြေဆိုရ။ သက်ဆိုင်ရာ မူဝါဒ အခန်းပိုင်းကို ရယူ၍ ထိုသက်သေအောက်မှ ဖြေကြားရမည်။

လုံးဝ လုပ်ဆောင်နိုင်သည့် ဗားရှင်းမှာ [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) တွင် ရှိသည်။ အောက်ပါကုဒ်မှာ အဓိကအဆင့်များကို ဖော်ပြထားပြီး ဆောင်းပါးကို သင်ခန်းစာတစ်ခုအဖြစ် ဖတ်ရှုနိုင်သည်။

## 2. ဒေသတွင်းလိုအပ်ချက်များထည့်သွင်းခြင်း

 virtual environment တစ်ခု ဖန်တီးကာ စီးရီး 2 လိုအပ်ချက်များကို ထည့်သွင်းပါ-

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

ပထမဦးဆုံးဗားရှင်းတွင် Qdrant ဒေသတွင်း mode နှင့် FastEmbed ကို အသုံးပြုသည်။ Qdrant ၏ Python client သည် `QdrantClient(":memory:")` ဖြင့် memory-based local mode ကိုထောက်ပံ့ပြီး ဒေသတွင်း သင်ခန်းစာနှင့် CI စတိုင် စစ်ဆေးမှုအတွက် အသုံးဝင်သည်။ FastEmbed မှ cloud API ကီးမလိုဘဲ ပရောဂျက်အား တကယ်တမ်းဒေသတွင်း embedding မော်ဒယ်ကိုပေးသည်။

လိုအပ်ချက်ဖိုင်တွင် `python-dotenv` ပါဝင်သည်၊ ဒါဟာ Notebook မှ Ollama မော်ဒယ်နာမည်ကို `.env` မှအလိုအလျောက်ဖတ်ရန်သုံးသည်။ Azure OpenAI သို့မဟုတ် OpenAI API ကီးမလိုအပ်ဘဲ ဒေသတွင်း သင်ခန်းစာအတွက် ဖြစ်သည်။

## 3. နမူနာစာရွက်စာတမ်းများကို ဖတ်ယူခြင်း

နမူနာ စာစုသည် ရည်ရွယ်ချက်ဖြင့် သေးငယ်။-

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Notebook တွင် `sample_data/` မှ Markdown ဖိုင်များအားလုံးကို ဖတ်ယူသည်-

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

Notebook ကို ကြောင့် ကျွန်ုပ် ၂ ဖိုင် စာရွက်ဖတ်ပါသည်။ ဒါဟာ လက်ထဲကြည့်ရှုရန် သင့်လျော်သည်။ RAG ပိုင်း၏ ပထမထုတ်လုပ်မှု တည်ဆောက်စဉ်တွင် အသုံးဝင်သည်။

## 4. Markdown ခေါင်းစဉ်များဖြင့် ချန်က်ခြင်း

နောက်တစ်ဆင့်မှာ စာရွက်စာတမ်းများကို ချန်က်ခြင်းဖြစ်သည်။

ဒီသင်ခန်းစာတွင် သတ်မှတ်ဖော်ပြချက်ဖြစ်သော Markdown ခေါင်းစဉ်များကို တည်ဆောက်မှု အချက်အလက်အဖြစ် အသုံးပြုသည်။ စာရွက်၏ ခေါင်းစဉ်သည် `#` မှ ရယူပြီး၊ အပိုင်းတိုင်း chunk မှ `##` မှရသည်။

> [!NOTE]
> ချန်က်ခြင်းသည် အားလုံးအတွက် တူညီမှုမရှိပါ။ ဤသင်ခန်းစာတွင် Markdown ခေါင်းစဉ်များကို အသုံးပြုသောအကြောင်းမှာ နမူနာစာရွက်များတွင် `#` နှင့် `##` တိကျသော တည်ဆောက်မှုရှိသည့်အတွက်ဖြစ်သည်။ PDF၊ Word စာရွက်စာတမ်း၊ slide၊ ပွဲတင်ပေးခြင်း Ticket များ သို့မဟုတ် ဝဘ်စာမျက်နှာများတွင် စာမျက်နှာ နယ်နိမိတ်များ၊ အပြင်အဆင်၊ အဓိပ္ပါယ်နယ်ပယ်၊ token ကန့်သတ်ချက်များ၊ ဇယားများ သို့မဟုတ် metadata အသုံးပြုမှု စသဖြင့် ပိုမိုသင့်တော်သည်။ အရေးကြီးတာက သင့်စာရွက်စာတမ်းများအတွက် အဓိပ္ပါယ်နှင့် အရင်းအမြစ် တိကျမှုကို ထိန်းသိမ်းနေသော ချန်က်နည်းလမ်းကို ရွေးချယ်ခြင်းဖြစ်သည်။

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

ထို့နောက် တစ်စိတ်တစ်ပိုင်း အားလုံးကို လျှောက်ထားသည်-

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

ကျွန်ုပ် ဒေသတွင်း လည်ပတ်မှုတွင် ၈ ချန်က် ဖန်တီးခဲ့သည်။

ဤအဆင့်တွင်Metadata သည် ဝိသေသလက္ခဏာရှိသည်။ တစ်စိတ်တစ်ပိုင်းချင်းစီသည် `source`, `sectionHeading`, `documentVersion`, နှင့် အစားထိုး `permissions` ကို သိသည်။ သေးငယ်သော်လည်း သင်ခန်းစာတစ်ခုတွင် ဒါဟာ ရည်ညွှန်းချက်များနှင့် နောက်ပိုင်းခွင့်ပြုချက် သိရှိရန် မျှော်လင့်အောင် အလွယ်တကူဖြစ်စေသည်။

## 5. ဒေသတွင်း Embeddings ဖန်တီးခြင်း

ပထမ ဗားရှင်းအတွက် `BAAI/bge-small-en-v1.5` ကို FastEmbed ဖြင့်သုံးသည်။

ဒါက သင်ခန်းစာကို ဒေသတွင်းနဲ့ CPU-သင့်လုပ်ဆောင်မှုရှိစေပါသည်၊ ဒါပေမယ့် နမူနာ vector function မဟုတ်ပဲ တကယ်တမ်း embedding မော်ဒယ်ကို အသုံးပြုသည်။ ပထမ run မှာ မော်ဒယ်အလေးချိန်များ ဒေါင်းလုပ်လုပ်ပါမည်။ နောက်မှ Notebook မှ ဒေသတွင်း cache ကို ပြန်အသုံးပြုနိုင်သည်။

> [!NOTE]
> ငါသည် `BAAI/bge-small-en-v1.5` ကို သုံးသည့်အကြောင်းမှာ ဒေသတွင်း သင်ခန်းစာအတွက် FastEmbed နဲ့ Qdrant နှင့် လိုက်ဖက်သည့် ပေါ့ပါးသော အင်္ဂလိပ် embedding မော်ဒယ် ဖြစ်သောကြောင့် ဖြစ်သည်။ ၃၈၄-မျှတို dimension vector များ ပြုလုပ်သည်၊ သက်သာမြန်ဆန်စေ။ ဤဟာတစ်ခုတည်းကောင်းမွန်သော ရွေးချယ်မှု မဟုတ်ပါ။ ၂၀၂၃ တွင် စက်တင်အမျိုးမျိုးသည် hosted embedding မော်ဒယ်များ `text-embedding-ada-002` စသဖြင့် အသုံးပြုခဲ့သည်။ ယနေ့တွင် အပိုမိုနောက်ဆုံး Hosted ရွေးချယ်မှုများဖြစ်သော OpenAI `text-embedding-3-small`, `text-embedding-3-large` နဲ့ BGE, E5, MiniLM, Nomic Embed နှင့် နိုင်ငံပေါင်းစုံ မော်ဒယ်များ `BAAI/bge-m3` စသော ရွေးချယ်စရာများ ရှိသည်။ ထုတ်လုပ်မှုတွင် embedding မော်ဒယ်သင့်တော်မှုကို ကိုယ်ပိုင် စာရွက်စာတမ်းများပေါ်တွင် ရယူမှန်းကောက်ခြင်းဖြင့် သတ်မှတ်ပေးသင့်သည်။

အချို့ အကောင်းဆုံးလမ်းကြောင်းများ-

| မော်ဒယ် အုပ်စု | ဘယ်အချိန်တွင် ယူဆမည် |
| --- | --- |
| `text-embedding-ada-002` | ၂၀၂၃ အတွင်း သင်ခန်းစာများတွင် အသုံးပြုသောဟောင်းကောင်းဝါ baseline တစ်ခု။ ယနေ့သစ် သင်ခန်းစာအတွက် မပေးရွေးလိုပါ။ |
| `text-embedding-3-small` | လုပ်ဆောင်မှုနှင့် ကုန်ကျစရိတ်ချိန်ကို ထိန်းချုပ်ရန် ပြည့်စုံသော hosted default သုံးချင်သည့်အခါ။ ဒေသတွင်း embedding မလိုအပ်ပါ။ |
| `text-embedding-3-large` | အသံမြင့်သော ရယူမှုအရည်အသွေး လိုအပ်သော အခါ Hosted option ဖြစ်သည်။ |
| `BAAI/bge-small-en-v1.5` | သင်ခန်းစာ၊ နမူနာများနှင့် CPU-friendly စမ်းသပ်မှုများအတွက် ပေါ့ပါးသော ဒေသတွင်း အင်္ဂလိပ် baseline ဖြစ်ပါတယ်။ |
| `BAAI/bge-base-en-v1.5` သို့မဟုတ် `BAAI/bge-large-en-v1.5` | ကောင်းမွန်သော ရယူမှုအရည်အသွေးလိုမည့်အခါ နှင့် စွမ်းဆောင်ရည် ပိုလိုအပ်သောအခါ အကြီးစား ဒေသတွင်း အင်္ဂလိပ် မော်ဒယ်များ။ |
| `BAAI/bge-m3` | နိုင်ငံတကာ များစွာသုံးဆောင်သော မော်ဒယ်များ သို့မဟုတ် နောက်ခံ context ကြီး များစွာ လိုအပ်သောအခါ။ |
| `sentence-transformers/all-MiniLM-L6-v2` | အလွန်သေးငယ်ပြီး မြန်ဆန်သော semantic ရှာဖွေရေး baseline ဖြစ်သည်။ မြန်နှုန်းနှင့် ရိုးရှင်းမှုအလွန်အရေးကြီးသည့်အခါ အသုံးဝင်သည်။ |
| `nomic-embed-text-v1.5` | ဘေးပတ်ဝန်းကျင်များ အစဉ်အလာ မရှိသော်လည်း ပြင်ပ ဒေသတွင်း embedding ရွေးချယ်မှုအတွက် စမ်းသပ်ရန်အသုံးပြုနိုင်သည်။ |

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

ထို့နောက် တစ်စိတ်တစ်ပိုင်းစီတွင် embedding သတ်မှတ်သည်-

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

## 6. Qdrant ဒေသတွင်း mode တွင် ဗက်တာများ သိုလှောင်ခြင်း

ယခု in-memory Qdrant collection တည်ဆောက်၍ တစ်စိတ်တစ်ပိုင်းများကို payload metadata အတူ မြှပ်နှံပါ။

> [!NOTE]
> ၂၀၂၃ သင်ခန်းစာတွင် FAISS ကိုသုံးခဲ့သည်။ LangChain နှင့် ဒေသတွင်း vector similarity ရှာဖွေမှုကို ပြသရန် ပေါ့ပါးနဲ့ လူကြိုက်များသောနည်းလမ်းဖြစ်သည်။ FAISS သည် ဒေသတွင်း မြန်ဆန်သော စမ်းသပ်မှုများတွင် ကျေနပ်စရာဖြစ်သည်။ ၂၀၂၆ ဗားရှင်းတွင် ငါ Qdrant ကိုသုံးသည်။ ထိုသင်ခန်းစာသည် ထုတ်လုပ်မှု RAG စနစ်နီးပါး အခြေအနေနိုင်ရှိစေသည်။ Qdrant သည် vector များကို source ဖိုင်၊ section heading, document version, permissions လို payload metadata တို့နှင့်အတူ သိုလှောင်နိုင်စေသည်။ ထိုသို့ရသည်မှာ ရယူမှု စစ်ဆေးရန် လွယ်ကူစေပြီး ဖျတ်အုပ်၊ ရည်ညွှန်းချက်နှင့် အနာဂတ် တစ်နေရာတည်း သို့မဟုတ် ဆာဗာအခြေပြု တပ်ဆင်ခြင်းမရှိသော system များအတွက် အဆင်ပြေစေရန်ဖြစ်သည်။

FAISS သည် vector similarity ရှာဖွေမှုကို ပြသရာတွင် အထူးကောင်းမွန်သည်။ Qdrant သည် အသေးစား ဒါပေမဲ့ ထုတ်လုပ်ပြင်ဆင်ထားသော RAG ရယူမှုအလွှာကို ပြသရာတွင် ပိုမို ကောင်းမွန်သည်။

အချို့ လုပ်ဆောင်နိုင်သော ရွေးချယ်စရာများ-

| Vector store / ရှာဖွေမှု အလွှာ | ဘယ်အချိန် ယူဆမည် |
| --- | --- |
| Qdrant | ဒေသတွင်း ပရိုတိုတိုက်၊ metadata စစ်ထုတ်မှု၊ ထုတ်လုပ်ရန်သင့်တော်သော vector ရှာဖွေမှု၊ Python workflow ရိုးရှင်းမှု။ |
| Chroma | မြန်ဆန်သော ဒေသတွင်း RAG စမ်းသပ်မှုများ၊ အလွန် ရိုးရှင်းသော notebook များတွင် အသုံးပြုရန်။ |
| FAISS | vector similarity ရှာဖွေမှုသာ လိုအပ်ပြီး metadata ကို မိမိစီမံထိန်းသိမ်းနိုင်သည့် သေးငယ်သော ဒေသတွင်း vector ရှာဖွေမှု။ |
| Milvus | အသင်းအသုံးပြု၍ သီးခြား vector ဒေတာအချက်အလက် ထိန်းသိမ်းသည့် များပြားသော open-source vector ရှာဖွေမှု။ |
| Weaviate | schema၊ metadata၊ ဟြိုက်ဘရစ် ရှာဖွေမှုများနှင့် စီမံခန့်ခွဲခြင်း သို့မဟုတ် ကိုယ်ပိုင်ထိန်းသိမ်း သတ်မှတ်ခြင်းများပါဝင်သည့် vector ရှာဖွေမှု။ |
| Azure AI Search | Azure တွင် Enterprise RAG၊ စကားလုံးရှာဖွေမှု၊ vector ရှာဖွေမှု၊ ဟြိုက်ဘရစ် ရယူမှု၊ semantic ရွေးချယ်မှု၊ စစ်ထုတ်မှု၊ လုံခြုံမှုနှင့် စီမံခန့်ခွဲမှုကို တစ်နေရာတည်းတွင်။ |
| PostgreSQL + pgvector | PostgreSQL ကို အသုံးပြုနေသော အသင်းများအတွက် vector ရှာဖွေမှုကို အချက်အလက်ဒေတာနဲ့ အနီးကပ်လိုချင်သည်။ |

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

နောက်တော်တော် insert points -

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

ကျွန်ုပ်၏ လည်ပတ်မှုတွင် စုစည်းမှု ၈ ဗက်တာထည့်သွင်းခဲ့သည်။

ဒီမှာ RAG စနစ်သည် စတင်ကြည့်ရှုနိုင်ထိုက်သည်။ ဗက်တာဒေတာဘေ့စ်သည် ဗက်တာများသာ မဟုတ်ပဲ သက်သေစာသားနှင့် ရည်ညွှန်းချက် metadata ကိုလည်း ထည့်သွင်းသိမ်းဆည်းသည်။

## 7. မျှော်မှန်းထားသော ချန်က်များ ရယူခြင်း

ယခု မေးခွန်းကိုမေးပြီး မျှော်မှန်းထားသော ချန်က်များကို ရယူပါ။

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

ဤအချိန်တွင် ငါ မျှော်မှန်းထားသော ချန်က်များကို စာပေါ်ကြည့်ရုံကျော်မဟုတ်ဘဲ ဖြေဆိုချက် ထုတ်လုပ်မှသာမက စောင့်ကြည့်ပေးသည်။ ရယူမှုမှားမှ ရိုက်ထုတ်မှုမှ အမှားကိုသာ မြင်နိုင်ပြီး စာသားချောမွေ့၍ ပြဿနာကို ဖုံးကွယ်မည်ဖြစ်သည်။

## 8. ပေါ့ပါးသော ပြန်စီဖော်သူ ထည့်သွင်းခြင်း

ပထမဆုံး ရယူမှု လမ်းကြောင်းကို စမ်းသပ်သောအခါ၊ vector similarity တစ်ခုတည်းဖြင့် ဆက်စပ်သော မူဝါဒ အကြောင်းအရာများကို ရှာဖွေသော်လည်း အတိအကျဆုံး အပိုင်းသည် အမြဲတမ်း ထိပ်ဆုံးမဖြစ်ပါ။

ဒါကြောင့် ဒေသတွင်း ပြန်စီဖော်သူက ရှိပေးပါသည်။ မေးခွန်းစကားလုံးများနှင့် အပိုင်း ခေါင်းစဉ် နှင့် အကြောင်းအရာမှ တစ်ကျော့ကျော့ တစ်ခု ကျော်ရှိမှသာ ပိုပြီး အလေးထားပေးသည်။

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

ပြန်စီပြီးနောက်၊ ထိပ်ဆုံးရလဒ်မှာ

```text
school_ai_policy.md / Final Assignments
```

စမ်းသပ်မေးခွန်းအတွက် မျှော်မှန်းထားသော အပိုင်း ဖြစ်သည်။

ဒါဟာ ပထမဆုံး အကောင်အထည်ဖော်မှုမှ အရမ်းကိုအသုံးဝင်သော သင်ခန်းစာဖြစ်သည်။ သေးငယ်သော ဒေသတွင်း ဥပမာတစ်ခု ဖြစ်သော်လည်း vector similarity နှင့် အခြား အချက်အလက္ခဏာပေါင်းစည်းသည်နှင့်အတူ ရယူမှုအရည်အသွေး တိုးတက်ခဲ့သည်။

## 9. နေရာကျ စက်ရုံဖြေရှင်းချက် တည်ဆောက်ခြင်း

ပုံမှန်လမ်းကြောင်းအတွက် LLM မဟုတ်ဘဲ ဖျော်ဖြေရှင်းချက် စက်တည်ဆောက်ကူညီရေးကို အသုံးပြုသည်-

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

ဒါက နောက်ဆုံးထုတ်ကုန်ဖြေရှင်းသူ မဟုတ်ပါ။ အားတစ်ခုဖြစ်သည်။ ရယူမှု၊ metadata နှင့် ရည်ညွှန်းချက်ကြိုးပမ်းမှု မော်ဒယ်မတည့်ခင် စမ်းသပ်နိုင်ရန် ဖြစ်သည်။

## 10. Ollama နှင့် Phi-4-mini ဖြင့် ဒေသတွင်း ဖြေရှင်းချက် ထုတ်လုပ်ခြင်း

ရယူမှုအဆင်ပြေနေသောအချိန်တွင် Notebook မှ ဖြေဆိုခြင်းအဆင့်ကို Ollama နှင့် `phi4-mini:3.8b` ဖြင့် ပြောင်းလဲနိုင်သည်။

> [!NOTE]
> Ollama သည် ဖြေဆိုခြင်းအဆုံး အဆင့်၌သာ အစားထိုးသင့်သည်။ စာရွက်ဖတ်ခြင်း၊ ချန်က်ခြင်း၊ vector သိုလှောင်ခြင်း၊ ရယူခြင်း၊ ပြန်စီခြင်းနှင့် ရည်ညွှန်းပေးခြင်းတို့သည်တူညီနေသင့်သည်။

ပထမဆုံး Notebook မှ ရယူထားသော ချန်က်များမှ သက်သေ prompt တည်ဆောက်သည်-

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

ဤသင်ခန်းစာအတွက် လုပ်ဆောင်ရန် Microsoft ၏ Phi-4-mini မော်ဒယ်ကို Ollama မှ တခြားနမူနာ ဒေသတွင်း မော်ဒယ်ရွေးချယ်မှု အဖြစ် အကြံပြုသည်။ Ollama တွင် စမ်းသပ်သော မော်ဒယ်အမည်မှာ -

```powershell
ollama pull phi4-mini:3.8b
```

မော်ဒယ် ရရှိနိုင်ကြောင်း မြန်မြန်စစ်ဆေးနိုင်သည်-

```powershell
ollama list
```

ထို့နောက် အတိအကျ variables များကို သတ်မှတ်သည်-

```powershell
Copy-Item .env.example .env
```

`.env` ဖိုင်ကို ဖွင့်၍ စီးရီး ၂ Ollama တန်ဖိုးတွေကို uncomment လုပ်ပါ-

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook သည် အမှတ်အသားဖြစ်သော `.env` ကို repository ရှင်းမှ python-dotenv နှင့် ဖတ်ယူပြီး၊ ထိုသက်သေ prompt ကို Ollama ၏ ဒေသတွင်း `/api/chat` အဆုံး‌မှာ ပို့သည်၊ streaming ကို ပိတ်ထားသည်။ Ollama မရှိပါက သို့မဟုတ် `SERIES2_OLLAMA_MODEL` မရှိပါက ဒီနည်းလမ်းကို ဖျက်ပစ်မည်။

> [!NOTE]
> ဤစက်ပေါ်တွင် `phi4-mini:3.8b` ဟာ 2.49GB မော်ဒယ်ဖိုင်များကိုဒေါင်းလုပ်ထားသည်။ Inference လုပ်စဉ်မှာ Ollama က 3.3GB loaded model အရွယ်အစားနှင့် RTX 3060 Laptop GPU ကိုသုံးသည်။

ဒါနဲ့ သင်ခန်းစာမှာ နှစ်ခုသောအဆင့်ရှိသည်-

1. CPU မှသာ ဖွဲ့စည်းချက်ဖြေရှင်းသူ။
2. Ollama နှင့် Phi-4-mini ဖြင့် ဒေသတွင်း ဖြေရှင်းချက် ထုတ်လုပ်မှု။

ရယူမှု လမ်းကြောင်းတွင် LLM ထောက်ပံ့မှုမရှိဘဲ တူညီနေသည်။

## 11. စစ်ဆေးမှုရလဒ်

ကျွန်ုပ်က Notebook ကို Windows ပတ်လမ်းမှာ Python 3.12.6 ဖြင့် လည်ပတ်ခဲ့သည်။

တပ်ထားသော ကုဒ်ရင်းများ-

| Package | ဗားရှင်း |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Notebook လည်ပတ်မှု-

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- လည်ပတ်စမ်းသပ်မှုရလဒ်: nbclient ဖြင့် ဖြတ်သန်းပြီး
- စာရွက်စာတမ်းများ ဖတ်ယူထားမှု: 2
- ချန်က်ဖန်တီးမှု: 8
- Qdrantစုစည်းမှု: `school_policy_local`
- ဗက်တာထည့်သွင်းမှု: 8
- Embedding မော်ဒယ်: `BAAI/bge-small-en-v1.5`
- Embedding အရွယ်အစား: 384
- Retrieval question: "ကျွန်ုပ်၏နောက်ဆုံးအပ်ဒ်လိုက်တာအတွက် generative AI ကို အသုံးပြုနိုင်မလား?"
- Reranking path: အလေးချိန် မျက်နှာသာ နှင့် ဒေသခံ စကားလုံးအခြေပြု ပြန်သီးခြားခြင်း
- Top retrieved source after reranking: `school_ai_policy.md`
- Top retrieved section after reranking: `Final Assignments`
- Default answer path: ဒေသခံ ထင်ရှားသော အဖြေဖန်တီးသူ
- Ollama generation path: ပြီးစီးခဲ့ပြီး `phi4-mini:3.8b`
- Ollama model file size: ဒစ်စ်ပေါ်မှာ 2.49GB
- Ollama loaded model size: `ollama ps` မှာ 3.3GB အစီရင်ခံထားသည်
- GPU offload: `ollama ps` မှာ 100% GPU ဖြင့် သတင်းပို့ထားသည်
- GPU memory observed after generation: RTX 3060 Laptop GPU မှာ 6GB အနက် 3.5GB အသုံးပြုနေသည်
- Notebook execution with cached FastEmbed model and Ollama generation enabled: အတည်ပြုရေး စာမျက်နှာဖြင့် 34 စက္ကန့်ခန့်ကြာ ပြီးဆုံးခဲ့သည်

Ollama ဖြင့် ထုတ်လုပ်ထားသော အဖြေမှာ -

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

ဤအဖြေကို သေချာပြည့်စုံသည် မဟုတ်ကြောင်း ပြောနိုင်မှာဖြစ်သည်။ သက်သေများမှမှန်ကန်စွာ တုံ့ပြန်ထားသော်လည်း နောက်ဆုံးအရင်းအမြစ်ပိုင်းနည်းနည်းတင်းကျပ်မှုမရှိပါ။ သင်ကြားမှုတွင် ပြသရန် အမျိုးအစားအဖြေများ ထုတ်လုပ်ရာမှ နှုတ်ဆက်အဆင့်ကို ထိထိရောက်ရောက်ပြသနိုင်စေသည်။ ထိုကဲ့သို့ဖြစ်စေခြင်းအားဖြင့် အဖြေထုတ်လုပ်ခြင်းကို ရှေးစစ်သင့်သည်ဟု စိတ်ခွန်အား ပေးသည်။

ကျွန်ုပ်စစ်ဆေးသည့်အချိန်တွင် အဓိက သင်ယူရသည်မှာ စုံစမ်းခြင်းအရည်အသွေးကို အဖြေထုတ်လုပ်မှုမတိုင်မှီ စစ်ဆေးသင့်သည်ဟု ဖြစ်သည်။ embedding ရလဒ်မှာ အကျိုးရှိပြီး ၎င်း၏ အလေးချိန်နည်းသော ပြန်သီးခြားမှုမှ မျှော်မှန်းထားသော မူဝါဒအပိုင်းကို ပထမဆုံး ပြသနိုင်ခဲ့သည်။ ၎င်းသည် သင်ကြားမှုအတွက် ဖုံးကွယ်မထားလိုသော စနစ်ပြသမှု အမျိုးအစားဖြစ်သည်။

## 12. နောက်တစ်ဆင့်ကဘာလဲ

နောက်တစ်ခုတိုးတက်မှုမှာ ဒေသခံစနစ်နှင့် ပိုင်ဆိုင်မှုရှိသော Azure ဗားရှင်းကို အရင်းအမြစ်ခိုင်မာမှု၊ ရှာဖွေရေးထိန်းချုပ်မှု၊ ကိုယ်စားလှယ်ပေါင်းစည်းမှု၊ လည်ပတ်မှုအပေါ် ပိုင်ဆိုင်မှုနှင့် ကုန်ကျစရိတ်တို့ကို ရှင်းလင်းစွာ မျှတစွာ ကြည့်ရှုနိုင်ရန် စစ်ဆေးမှုလိမ့်မည်။

## 13. မှတ်စုများ

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

ယခင်: [စီးရီး 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ပြောကြားချက်**
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းနေသော်လည်း၊ စက်ကိရိယာဘာသာပြန်ခြင်းများတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် လိုအပ်ပါသည်။ မူလစာတမ်းကို မူရင်းဘာသာဖြင့်သာ ယုံကြည်စိတ်ချရသော အချက်အလက်အဖြစ် သတ်မှတ်သင့်သည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုကွာခြားမှုများ သို့မဟုတ် မမှန်ကန်သော အသုံးပြုမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မခံပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->