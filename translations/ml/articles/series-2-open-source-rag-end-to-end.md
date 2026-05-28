# നിങ്ങളുടെ പ്രമാണങ്ങളെ അടിസ്ഥാനമാക്കി AI-ന് ചോദ്യങ്ങൾക്ക് മറുപടി പറയാൻ പഠിപ്പിക്കുക  
## 2nd സീരീസ്: ഒരു ലോക്കൽ ഓപ്പൺ-സോഴ്‌സ് RAG സിസ്റ്റം എండ్ ടു എണ്ട് നിർമ്മിക്കുക

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> ഈ ലേഖനം സീരീസ് 1 ആർക്കിടെക്ചർ ചർച്ചയെ ഒരു പ്രവർത്തനക്ഷമമായ ലോക്കൽ RAG ട്യൂട്ടോറിയലായി മാറ്റുന്നു. ലക്ഷ്യം സാമ്പിൾ ഡാറ്റ ഉപയോഗിച്ച്, ക്ലൗഡ് അക്കൗണ്ട് ഇല്ലാതെ, രഹസ്യങ്ങൾ ഇല്ലാതെ ആദ്യം മുഴുവൻ വർക്ക്ഫ്ലോ നിർമ്മിക്കുക, പിന്നീട് ആ പ്രവർത്തനക്ഷമമായ അടിസ്ഥാനത്തെ അധരിച്ച് മികച്ച ആർക്കിടെക്ചർ തീരുമാനങ്ങൾ എടുക്കുക.

നാം നിർമ്മിക്കാനുദ്ദേശിക്കുന്ന സിസ്റ്റം ഒരു ചെറു സ്‌കൂൾ നയം അസിസ്റ്റന്റാണ്. ഞാൻ രണ്ട് ലോക്കൽ മാർക്ക്ഡൗൺ പ്രമാണങ്ങൾ അറിവ് ആധാരമായി ഉപയോഗിച്ച്, RAG പൈപ്പ്ലൈൻ മുഴുവൻ വഴി നടക്കും: chunks-ആകൽ, ലോക്കൽ embeddings, Qdrant വെക്റ്റർ സ്റ്റോറേജ്, വീണ്ടെടുക്കൽ, റീ-റാങ്കിംഗ്, സോഴ്‌സ്-അവേർ ഉത്തരം നിർമ്മാണം, ഒപ്പം ഐച്ഛികമായ ലോക്കൽ ജനറേഷൻ ഓള്ളാമയും Phi-4-mini-ഉം ഉപയോഗിച്ച്.

സീരീസ് നാവിഗേഷൻ: [Repository home](../README.md) | മുമ്പത്തെത്: [സീരീസ് 1 - RAG, Azure vs ഓപ്പൺ-സോഴ്‌സ് പകരങ്ങൾ, ഫൈൻ-ട്യൂണിംഗ് മുന്നോക്കുന്നത് എപ്പോൾ ഉചിതം](./series-1-rag-azure-open-source-fine-tuning.md)

നോട്ട്ബുക്ക്: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | ആവശ്യക്കഴിവുകൾ: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]  
> ക്ലൗഡ് റിസോഴ്‌സുകൾ സൃഷ്ടിക്കുന്നതിനു മുമ്പ് RAG പൈപ്പ്ലൈൻ മനസ്സിലാക്കാനാഗ്രഹിക്കുന്നുവെങ്കിൽ ഇത് മികച്ച ആരംഭ ബിന്ദുവാണ്. ഡിഫോൾട്ട് മാർഗ്ഗം CPU-നുയോജ്യമായ embeddings-ഉം രഹസ്യങ്ങളില്ലാതെ ലോക്കലായാണ് പ്രവർത്തിക്കുന്നത്.

## 1. നാം നിർമ്മിക്കുന്നത് എന്താണ്

2023-ലെ ട്യൂട്ടോറിയലിൽ, Azure AI Search, Azure OpenAI എന്നിവ PDF-പ്രമാണങ്ങളിൽ നിന്ന് ചോദ്യങ്ങൾക്ക് ഉത്തരം പറയുകയാണ് എങ്ങനെ കാണിക്കാനെന്ന ലക്ഷ്യത്തോടെ Azure-ലാണ് തുടക്കം.

2026 സീരീസിനായി ഞാൻ ഒരു ലയറ് താഴേക്ക് തുടക്കമിടാൻ ആഗ്രഹിക്കുന്നു.

മാനേജുചെയ്യപ്പെടുന്ന സേവനങ്ങൾ ഉപയോഗിക്കും മുമ്പ്, ഒരു ചെറു RAG സിസ്റ്റം ലോക്കലായി നിർമ്മിച്ച് എല്ലാ ഘട്ടങ്ങളും ദൃശ്യമാകണം: പ്രമാണങ്ങൾ ലോഡ് ചെയ്യൽ, ടെക്സ്റ്റ് ചങ്ക് ചെയ്യൽ, വെക്റ്ററുകൾ സംഭരിക്കൽ, തെളിവ് വീണ്ടെടുക്കൽ, റീ-റാങ്കിംഗ്, സോഴ്‌സ്-അവേർ ഉത്തരം തിരുത്തൽ.

സാമ്പിൾ പരിസ്ഥിതി ഒരു സ്‌കൂൾ നയം സഹായി ആണ്. ഉപയോഗിക്കുന്നവൻ ചോദിക്കുന്നു:

```text
Can I use generative AI for my final assignment?
```
  
സിസ്റ്റം സാധാരണ മോഡൽ മെമ്മറിയിൽ നിന്ന് മറുപടി നൽകരുത്. അനുയോജ്യമായ നയം വിഭാഗം വീണ്ടെടുക്കുകയും അതിൽ നിന്ന് മറുപടി നൽകും.

മൊത്തം പ്രവർത്തനക്ഷമമായ പതിപ്പ് [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)-ൽ കാണാം. താഴെ കൊടുത്തിരിക്കുന്ന കോഡ് പ്രധാന ഘട്ടങ്ങൾ göstermektedir, അതിനാൽ ലേഖനം ട്യൂട്ടോറിയലായി വായിക്കാവുന്നതാണ്.

## 2. ലോക്കൽ ആശ്രിതങ്ങൾ ഇൻസ്റ്റാൾ ചെയ്യുക

ഒരു virtual environment സൃഷ്ടിച്ച് സീരീസ് 2 ആവശ്യകതകൾ ഇൻസ്റ്റാൾ ചെയ്യുക:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```
  
ആദ്യ പതിപ്പ് Qdrant ലോക്കൽ മോഡ്, FastEmbed എന്നിവ ഉപയോഗിക്കുന്നു. Qdrant-ന്റെ Python ക്ലയന്റ് in-memory ലോക്കൽ മോഡിനായി `QdrantClient(":memory:")` പിന്തുണയ്ക്കുന്നു, ഇത് ലോക്കൽ ട്യൂട്ടോറിയലുകൾക്കും CI-ശൈലിയിൽ പരിശോധനയ്ക്കും സഹായകരമാണ്. FastEmbed ഒരു ക്ലൗഡ് API കീ വേണ്ടാതെ യഥാർത്ഥ ലോക്കൽ embedding മോഡൽ നൽകുന്നു.

ആവശ്യകത ഫയലിൽ `python-dotenv` ഉൾപ്പെടുത്തിയിട്ടുണ്ട്, കാരണം നോട്ട്ബുക്ക് ഓള്ളാമ മോഡൽ നാമം `.env`-ൽ നിന്ന് ഐച്ഛികമായി വായിക്കാം. ഈ ലോക്കൽ ട്യൂട്ടോറിയലിനായി Azure OpenAI അല്ലെങ്കിൽ OpenAI API കികൾ ആവശ്യമില്ല.

## 3. സാമ്പിൾ പ്രമാണങ്ങൾ ലോഡ് ചെയ്യുക

സാമ്പിൾ കോർപ്പസ് ഉദ്ദേശപൂർവ്വം ചെറുതാണ്:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)  
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)  

നോട്ട്ബുക്കിൽ `sample_data/`-ൽ നിന്നുള്ള എല്ലാ മാർക്ക്ഡൗൺ ഫയലുകളും ലോഡ് ചെയ്യുന്നു:

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
  
നോട്ട്‌ബുക്ക് ഓടിക്കുമ്പോൾ 2 പ്രമാണങ്ങൾ ലോഡ് ചെയ്തു. ആദ്യ RAG പൈപ്പ്ലൈൻ നിർമ്മിക്കുമ്പോൾ കൈയാലോചനയ്ക്ക് ഇത്ര ചെറുതായിരിക്കുന്നു.

## 4. മാർക്ക്ഡൗൺ തലക്കെട്ടുകൾ പ്രകാരം ചങ്ക് ചെയ്യുക

അടുത്ത ഘട്ടം പ്രമാണങ്ങളെ ചങ്കുകളാക്കി വിഭജിക്കുക.

 ഈ ട്യൂട്ടോറിയലിൽ, മാർക്ക്ഡൗൺ തലക്കെട്ടുകൾ ഘടനാ സൂചനയായി ഉപയോഗിക്കുന്നു. ഡോക്യുമെന്റ് തലക്കെട്ട് `#`-ൽ നിന്നുള്ളതായിരിക്കും, ഓരോ സെക്ഷൻ ചങ്കും `##`-നിന്നുള്ളതായിരിക്കും.

> [!NOTE]  
> ചങ്ക് ചെയ്യൽ ഒരൊറ്റ രീതി എല്ലാ സാഹചര്യങ്ങൾക്കും അനുയോജ്യതയുള്ളതല്ല. ഈ ട്യൂട്ടോറിയലിൽ സാമ്പിൾ പ്രമാണങ്ങളിലെ വ്യക്തമായ `#` , `##` ഘടന ഉപയോഗിക്കുന്നു. PDF, Word പ്രമാണങ്ങൾ, സ്ലൈഡ്, ടിക്കറ്റ്, വെബ് പേജുകൾ ഉൾപ്പെടെയുള്ളവയിലെ പേജ് അതിരുകൾ, ലേയൌട്ട് വിവരങ്ങൾ, സെമാന്റിക് സെക്ഷനുകൾ, ടോക്കൺ പരിധി, പട്ടികകൾ, മെടാഡേറ്റ തുടങ്ങിയവ ഉപയോഗിക്കുന്ന മെച്ചപ്പെട്ട രീതി ആശ്രയിക്കാം. പ്രധാനതെങ്കിൽ നിങ്ങളുടെ പ്രമാണങ്ങൾക്ക് അർത്ഥവും സോഴ്‌സ് ട്രേസബിലിറ്റിയും സൂക്ഷിക്കുന്ന ചങ്ക് രീതി തിരഞ്ഞെടുക്കുക.

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
  
പിന്നീട് ഇത് ഓരോ പ്രമാണത്തിനും പ്രയോഗിക്കുന്നു:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```
  
ഇത് എന്റെ ലോക്കൽ പ്രവർത്തനത്തിൽ 8 ചങ്കുകൾ സൃഷ്ടിച്ചു.

ഈ ഘട്ടത്തിൽ എനിക്ക് ഇഷ്ടമായ കാര്യം മെടാഡേറ്റ ഉള്ളടക്കം തന്നെ ഉപയോഗപ്രദമായിരുക്കുന്നുണ്ട്. ഓരോ chunk-നും അതിന്റെ `source`, `sectionHeading`, `documentVersion`, `permissions` പ്ലേസ്‌ഹോൾഡർ അറിയാം. ചെറുചെറു ട്യൂട്ടോറിയലിലും ഇത് റഫറൻസിലും പിന്നീട് അനുവാദം-അവേർ വീണ്ടെടുക്കലിലും മനസിലാക്കാൻ സഹായിക്കും.

## 5. ലോക്കൽ embeddings സൃഷ്ടിക്കുക

ആദ്യ പൊതുജന പതിപ്പിന്, FastEmbed വഴി `BAAI/bge-small-en-v1.5` ഉപയോഗിക്കുന്നു.

ഇത് ട്യൂട്ടോറിയൽ ലോക്കലും CPU-സൗഹാർദവുമാകുന്നു, എന്നാൽ പ്ലേസ്‌ഹോൾഡർ വെക്റ്റർ ഫങ്ഷനിനു പകരം യഥാർത്ഥ embedding മോഡൽ ഉപയോഗിക്കുന്നു. ആദ്യം റൺ ചെയ്യുമ്പോൾ മോഡൽ ഭാരം ഡൗൺലോഡ് ചെയ്യും. അതിനുശേഷം സ്മൃതിഗധി പുനർവിനിയോഗിക്കാം.

> [!NOTE]  
> `BAAI/bge-small-en-v1.5` എങ്കിൽ ലളിതവും എളുപ്പത്തിൽ FastEmbed, Qdrant-ഉം ഉപയോഗിക്കാവുന്ന ഇംഗ്ലീഷ് embedding മോഡലാണ്. 384-ആയിരിക്കും വക്ടർ ഡിമെൻഷൻ, കാരണം ഉദാഹരണം വേഗത്തിലും കുറഞ്ഞ ചെലവിൽ ലോക്കൽ ഓടികാനാകും. ഇത് ഒറ്റ മാർഗ്ഗമല്ല. 2023-ൽ പല ട്യൂട്ടോറിയലുകളും ഹോസ്റ്റഡ് embedding മോഡലുകൾ പോലുള്ള `text-embedding-ada-002` ഉപയോഗിച്ചിരുന്നു. ഇന്നത്തെ കാലത്ത്, പുതിയ ഹോസ്റ്റഡ് ഓപ്ഷനുകൾ - OpenAI-യുടെ `text-embedding-3-small`, `text-embedding-3-large`, ഉൾപ്പെടെ, ഒപ്പം ഒപ്പൺ സോഴ്‌സ് ഓപ്ഷനുകൾ BGE, E5, MiniLM, Nomic Embed, നിരവധി ഭാഷകളിൽ പ്രവർത്തിക്കുന്ന `BAAI/bge-m3` എന്നിവയും തിരഞ്ഞെടുത്ത ജോലി ഭാരം അനുസരിച്ച് ശരിയായ embedding മോഡൽ തിരഞ്ഞെടുക്കുന്നതിന് മുതിർന്നവർക്ക് ഉത്തമം. പ്രോഡക്ഷനിൽ നിങ്ങളുടെ പ്രമാണങ്ങളിൽ retrieval മൂല്യനിർണയം മുഖാന്തിരം ശരിയായ മോഡൽ തിരഞ്ഞെടുക്കണം.

പ്രായോഗിക മേൽക്കേട്:

| മോഡൽ കുടുംബം | എപ്പോൾ പരിഗണിക്കും |  
| --- | --- |  
| `text-embedding-ada-002` | പഴയ ഹോസ്റ്റഡ് അടിസ്ഥാനമിൽ 2023 കാലഘട്ടത്തിലേയ്ക്കുള്ള പല ട്യൂട്ടോറിയലുകളിലും. ഇന്ന് പുതിയ ട്യൂട്ടോറിയലിന് ഇത് ഡിഫോൾട്ടായിട്ട് ഞാൻ തിരഞ്ഞെടുക്കാറില്ല. |  
| `text-embedding-3-small` | ശക്തമായ ചെലവ്/പ്രദർശന സമതുലനം ആഗ്രഹിക്കുമ്പോഴും ലോക്കൽ മാത്രം ആവശ്യമില്ലാത്തപ്പോൾ ഡിഫോൾട്ട് ആയി പരിഗണിക്കുക. |  
| `text-embedding-3-large` | retrieval ഗുണനിലവാരം വെക്ടർ വലുപ്പം അല്ലെങ്കിൽ embedding ചെലവിനേക്കാൾ പ്രധാനമാകുമ്പോൾ ഹോസ്റ്റഡ് ഓപ്ഷൻ. |  
| `BAAI/bge-small-en-v1.5` | ലളിതവും CPU-സൗഹൃദവും ആയ ലോക്കൽ ഇംഗ്ലീഷ് അടിസ്ഥാന പാതകങ്ങൾ ട്യൂട്ടോറിയലുകൾ, പ്രോട്ടോടൈപ്പ്, പരീക്ഷണങ്ങൾക്ക്. |  
| `BAAI/bge-base-en-v1.5` അല്ലെങ്കിൽ `BAAI/bge-large-en-v1.5` | മെച്ചപ്പെട്ട retrieval ഗുണനിലവാരവും കൂടുതൽ കമ്പ്യൂട്ട് അനുവദിച്ചാൽ വലിയ മോഡലുകൾ. |  
| `BAAI/bge-m3` | ഒന്നിൽ അധികം ഭാഷകളും നീളം കൂടിയ context ഉള്ള retrieval. |  
| `sentence-transformers/all-MiniLM-L6-v2` | വളരെ ചെറിയ വേഗതയുള്ള സെമാന്റിക് søർച്ച് മോഡൽ. വേഗവും ലളിതത്വവും പ്രധാനപ്പെട്ട സാഹചര്യങ്ങളിൽ ഉപയോഗപ്രദം. |  
| `nomic-embed-text-v1.5` | നീളമുള്ള context ഉം പോർട്ടബിലിറ്റിക്ക് അനുയോജ്യമായ ഓപ്പൺ ലോക്കൽ embedding ഓപ്ഷൻ പരिक्षിക്കാൻ പാടുള്ളത്. |

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
  
ഈ ശേഷം ഓരോ chunk-നും embedding കിട്ടും:

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
  
## 6. Qdrant ലോക്കൽ മോഡിൽ വെക്റ്ററുകൾ സംഭരിക്കുക

ഇപ്പോൾ ഒരു in-memory Qdrant collection സൃഷ്ടിച്ച് ചങ്കുകൾ payload മെറ്റാഡേറ്റയോടുകൂടി ചേർക്കുന്നു.

> [!NOTE]  
> 2023-ലെ ട്യൂട്ടോറിയലിൽ LangChain ഉപയോഗിച്ച് ലോക്കൽ വെക്റ്റർ സമാനത തിരച്ചിൽ കാണിക്കാൻ എളുപ്പവും ജനപ്രിയവും ആയ വഴിയായ FAISS-നെ ഉപയോഗിച്ചിരുന്നു. FAISS ഇപ്പോഴും വേഗത്തിലുള്ള ലോക്കൽ പരീക്ഷണങ്ങൾക്ക് നല്ലതാണ്. 2026 പതിപ്പിൽ, പ്രൊഡക്ഷൻ RAG സിസ്റ്റത്തിനോട് കൂടുതല് ആശയത്തിലേക്ക് ട്യൂട്ടോറിയൽ എത്തിക്കാൻ Qdrant ഉപയോഗിക്കുന്നു. Qdrant വെക്റ്ററുകളോട് കൂടെ സോഴ്‌സ് ഫയൽ, സെക്ഷൻ തലക്കെട്ട്, പ്രമാണ പതിപ്പ്, അനുവാദങ്ങൾ പോലുള്ള payload മെറ്റാഡേറ്റയും സംഭരിക്കാൻ സഹായിക്കുന്നു. ഇത് retrievalക്ക് എളുപ്പത്തിൽ പരിശോധിക്കാൻ ഉത്തമവും ഫിൽട്ടറിംഗിനും റഫറൻസിനും ഭാവിയിൽ സ്ഥിരതയ്ക്കും സഹായകവുമാണ്.

FAISS വെക്റ്റർ സമാനത തിരച്ചിൽ കാണിക്കാൻ മികച്ചതാണ്. Qdrant ചെറിയതായും എന്നാൽ പ്രൊഡക്ഷൻ രൂപം ലഭിച്ച RAG retrieval തലസ്ഥാന കാണിക്കാൻ ഉത്തമമാണ്.

പ്രായോഗിക മേൽക്കേട്:

| വെക്ടർ സ്റ്റോർ / തിരച്ചിൽ തലസ്ഥാനം | എപ്പോൾ പരിഗണിക്കും |  
| --- | --- |  
| Qdrant | ലൊക്കൽ പ്രോട്ടോടൈപ്പുകൾ, മെറ്റാഡേറ്റ ഫിൽട്ടറിംഗ്, പ്രൊഡക്ഷൻ-സ്വാഭാവിക വെക്റ്റർ തിരച്ചിൽ, ലളിതമായ പൈതൺ പ്രവർത്തനപ്രവാഹം. |  
| Chroma | ലളിതത്വം പ്രധാനമായുള്ള വേഗത്തിലൊരു ലോക്കൽ RAG പരീക്ഷണങ്ങൾക്കും നോട്ട്ബുക്കുകൾക്കും. |  
| FAISS | വെക്റ്റർ സമാനത തിരച്ചിൽ മാത്രം ആവശ്യമായപ്പോൾ, മെറ്റാഡേറ്റ ഉറപ്പിക്കൽ വേറിട്ടു കൈകാര്യം ചെയ്യാവുന്നതാകുമ്പോൾ. |  
| Milvus | വലിയ സ്കെയിൽ ഓപ്പൺ-സോഴ്‌സ് വെക്റ്റർ തിരച്ചിൽ ലാഭിക്കുമ്പോൾ, സമർപ്പിത വെക്റ്റർ ഡാറ്റാബേസ് പ്രവർത്തിപ്പിക്കാൻ ടീം തയ്യാറുണ്ടെങ്കിൽ. |  
| Weaviate | സ്കീമ, മെറ്റാഡേറ്റ, ഹൈബ്രിഡ് തിരച്ചിൽ കൂടെ വെക്റ്റർ തിരച്ചിൽ, മാനേജുചെയ്തോ സ്വയം ഹോസ്റ്റ് ചെയ്തോ വിന്യസന ഓപ്ഷനുകൾ. |  
| Azure AI Search | എന്റർപ്രൈസ് RAG, കീബോർഡ് തിരച്ചിൽ, വെക്റ്റർ തിരച്ചിൽ, ഹൈബ്രിഡ് വീണ്ടെടുക്കൽ, സെമാന്റിക് റാങ്കിംഗ്, ഫിൽട്ടറിംഗ്, സുരക്ഷ, മാനേജുചെയ്ത പ്രവർത്തനങ്ങൾ ഒരുചോദ്യയിൽ.Azure-ൽ. |  
| PostgreSQL + pgvector | PostgreSQL ഉപയോഗിക്കുന്ന ടീങ്ങൾ, ആപ്ലിക്കേഷൻ ഡാറ്റയോടു അടുത്തായി വെക്റ്റർ തിരച്ചിൽ ആവശ്യമുണ്ടെങ്കിൽ. |

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
  
പിന്നീട് പോയിന്റുകൾ ചേർക്കുക:

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
  
എന്റെ പ്രവർത്തനത്തിൽ, ഈ ശേഖരം 8 വെക്റ്ററുകൾ ചേർന്നു.

ഇത്തിരി ഭാഗം RAG സിസ്റ്റം കാണാനാകുന്ന വിധം ആരംഭിക്കുന്നു. വെക്റ്റർ ഡാറ്റാബേസ് വെക്റ്ററുകൾ മാത്രമല്ല സൂക്ഷിക്കുന്നത്, അതുമായി ബന്ധപ്പെട്ട തെളിവ് ടെക്സ്റ്റും മെറ്റാഡേറ്റയും സിനിമിച്ചുകൊള്ളുന്നു.

## 7. ಅಭ್ಯರ್ಥി ചങ്കുകൾ വീണ്ടെടുക്കുക

അതിനു ശേഷം ചോദ്യമുയർത്തി, അവസരമായ ചങ്കുകൾ വീണ്ടെടുക്കുന്നു.

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
  
ഈ ഘട്ടത്തിൽ retrieval ചെയ്ത ചങ്കുകൾ പ്രിന്റ് ചെയ്യുക. ഇത് നിർണ്ണായകമാണ്. വീണ്ടെടുക്കൽ തെറ്റായാൽ, ജനറേഷൻ എളുപ്പത്തിൽ പിഴവ് മറച്ചുവയ്ക്കും.

## 8. ഒരു ലഘുവായ റീ-റാങ്കർ ചേർക്കുക

പ്രാരംഭത്തിൽ retrieval വഴി വെക്റ്റർ സമാനത മാത്രം ശ്രദ്ധിച്ചപ്പോൾ ബന്ധപ്പെട്ട നയ സംവരണങ്ങൾ കണ്ടെത്തി, എന്നാൽ ഏറ്റവും കൃത്യമായ സെക്ഷൻ ഇടയിൽ എല്ലായ്പ്പോഴും കാണാനാകുന്നില്ല.

അതിനാൽ ചെറിയ ലൊക്കൽ റീ-റാങ്കർ ഏർപ്പെടുത്തി. ചോദ്യത്തിലെ പദങ്ങൾ സെക്ഷൻ തലക്കെട്ടിലും ഉള്ളടക്കത്തിലും ഒത്തുപോകുമ്പോൾ അധിക ഭാരമിട്ടു.

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
  
റീ-റാങ്ക് ചെയ്ത് ശേഷമുള്ള ഉച്ചസ്ഥാനവും:

```text
school_ai_policy.md / Final Assignments
```
  
ഇത് ചോദ്യത്തിന് പ്രതീക്ഷിച്ച സെക്ഷൻ ആയിരുന്നു.

ഇത് ആദ്യ നടപ്പിലാക്കലിൽ ലഭിച്ച ഏറ്റവും പ്രയോജനമുള്ള പാഠമാണ്. ചെറു ലൊക്കൽ ഉദാഹരണത്തിൽ പോലും, റീട്രീവൽ ഗുണമേന്മ വെക്റ്റർ സമാനതയോട് ചേർന്ന മറ്റൊരു സൂചന കൂടിച്ചേർത്തപ്പോൾ മെച്ചപ്പെട്ടു.

## 9. നിസ്സാരമായ ലോക്കൽ ഉത്തരം നിർമ്മിക്കുക

ഡിഫോൾട്ട് മാർഗ്ഗത്തിനായി, LLM ഉപയോഗിക്കാതെ ഒരു പടിഞ്ഞാറൻ ലോക്കൽ ഉത്തരം നിർമ്മാണ ടൂൾ ഉപയോഗിക്കുന്നു.

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
  
ഇത് അന്തിമ ഉത്തരം ജനറേറ്റർ ആയി bedoeld അല്ല. ഇത് ഒരു ഡീബഗ്ഗിംഗ് ഉപകരണം മാത്രമാണ്. retrieval, മെറ്റാഡേറ്റ, റഫറൻസിംഗ് പ്രവർത്തിക്കുന്നുവെന്ന് തെളിയിക്കുന്നു, മോഡൽ വൈവിധ്യത്തിനു മുമ്പ്.

## 10. ഓള്ളാമയും Phi-4-mini-യും ഉപയോഗിച്ച് ലോക്കലായി ഉത്തരം ജനറേറ്റ് ചെയ്യുക

വീണ്ടെടുക്കൽ തീർച്ചയായ ശേഷം, നോട്ട്ബുക്ക് മാത്രം അവസാന ഉത്തരം ഘട്ടം ഓള്ളാമയും `phi4-mini:3.8b` കമ്പൗണ്ട് ഉപയോഗിച്ച് മാറ്റും.

> [!NOTE]  
> ഡോക്യുമെന്റ് ലോഡിംഗ്, ചങ്ക് ചെയ്യൽ, വെക്റ്റർ സംഭരണം, retrieval, റീ-റാങ്കിംഗ്, റഫറൻസിംഗ് ഘടകങ്ങൾ എല്ലാം ഒരുപോലെ തന്നെയായിരിക്കും; ഓള്ളാമ ഉപയോഗം വെറും ഉത്തരം സൃഷ്ടിക്കൽ ഘട്ടം മാത്രമാകും മാറ്റം.

ആദ്യം നോട്ട്ബുക്ക് retrieval ചെയ്ത ചങ്കുകളിൽ നിന്ന് തെളിവ് പ്രോമ്പ്റ്റ് സൃഷ്ടിക്കുന്നു:

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
  
ഈ ട്യൂട്ടോറിയലിൽ, മൈക്രോസോഫ്റ്റ് Phi-4-mini കുടുംബം ഓള്ളമ വഴി ഡിഫോൾട്ടായ ലോക്കൽ ജനറേഷൻ વિકലയായി ശുപാർശ ചെയ്യുന്നു. ഞാൻ പരീക്ഷിച്ചത് ഓള്ളാമയിലെ മോഡൽ:

```powershell
ollama pull phi4-mini:3.8b
```
  
മോഡൽ ലഭ്യമാണ് എങ്കിൽ ഉടൻ പരിശോധിക്കാം:

```powershell
ollama list
```
  
പിന്നീട് ഈ മാറ്റനിലവാരങ്ങൾ സജ്ജമാക്കുക:

```powershell
Copy-Item .env.example .env
```
  
`.env` തുറന്ന് സീരീസ് 2 ഓള്ളാമ മൂല്യങ്ങൾ അണ്‍കമ്മെന്റ് ചെയ്യുക:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```
  
നോട്ട്ബുക്ക് റിപോസിറ്ററി മൂലത്തിൽ നിന്നുള്ള `.env` `python-dotenv` ഉപയോഗിച്ച് വായിക്കുന്നു, പിന്നീട് തെളിവ് പ്രോമ്പ്റ് ഓಳ್ಳാമയുടെ ലോക്കൽ `/api/chat` എൻഡ്‌പോയിന്റിലേക്ക് സ്റ്റ്രീമിംഗ് ഒഴിവാക്കി അയയ്ക്കുന്നു. ഓള്ളാമ പ്രവർത്തിച്ചില്ലെങ്കിൽ അല്ലെങ്കിൽ `SERIES2_OLLAMA_MODEL` കാണാനില്ലെങ്കിൽ ഈ മാർഗ്ഗം ഒഴിവാക്കാം.

> [!NOTE]  
> ഇതാ പിസിയിൽ `phi4-mini:3.8b` ഏകദേശം 2.49GB മോഡൽ ഫയലുകൾ ഡൗൺലോഡ് ചെയ്തു. ഇൻഫറൻസിൽ, ഓള്ളാമ ഏറ്റവുമധികം 3.3GB മോഡൽ വലുപ്പം ലോഡ് ചെയ്ത് RTX 3060 ലാപ്‌ടോപ്പ് GPU ഉപയോഗിച്ചു.

ഈ ട്യൂട്ടോറിയലിന് രണ്ട് നിലകളുണ്ട്:  
1. CPU മാത്രം നിർണ്ണായക ഉത്തരം നിർമ്മിതി.  
2. ഓള്ളാമയും Phi-4-mini-ഉം ഉപയോഗിച്ച് ലോക്കൽ ഉത്തരം സൃഷ്ടിക്കൽ.

റീട്രീവൽ പൈപ്പ്ലൈൻ രണ്ടിലും ഒരുപോലെ തന്നെ.

## 11. പരിശോദന ഫലം

പൈത്തൺ 3.12.6-ഉം Windows-ഉം ഉള്ള എന്റെ ലോക്കൽ പിസിയിൽ നോട്ട്ബുക്ക് ഓടിച്ചു.

ഇൻസ്റ്റാൾ ചെയ്ത പാക്കേജുകൾ:

| പാക്കേജ് | പതിപ്പ് |  
| --- | --- |  
| `qdrant-client` | `1.18.0` |  
| `fastembed` | `0.8.0` |  
| `python-dotenv` | `1.2.2` |  
| `nbclient` | `0.10.4` |  
| `nbformat` | `5.10.4` |  
| `ipykernel` | `7.2.0` |  
| `numpy` | `2.4.6` |

നോട്ട്ബുക്ക് പ്രവൃത്തി:  

- നോട്ട്ബുക്ക്: `notebooks/series-2-open-source-rag.ipynb`  
- പ്രവർത്തനഫലം: `nbclient` ഉപയോഗിച്ചു വിജയിച്ചു  
- ലോഡ് ചെയ്ത പ്രമാണങ്ങൾ: 2  
- സൃഷ്ടിച്ച ചങ്കുകൾ: 8  
- Qdrant ശേഖരം: `school_policy_local`  
- ചേർത്ത വെക്റ്ററുകൾ: 8  
- embedding മോഡൽ: `BAAI/bge-small-en-v1.5`  
- embedding വലുപ്പം: 384
- റിട്രീവൽ ചോദ്യം: "എന്റെ അന്തിമ അസൈൻമെന്റിന് ഞാൻ ജനറേറ്റീവ് എഐ ഉപയോഗിക്കാമോ?"
- പുനഃക്രമീകരണ പാത: ലൈറ്റ്‌വെയിറ്റ് ലോക്കൽ ലെക്സിക്കൽ പുനഃക്രമീകരണം
- പുനഃക്രമീകരണത്തിന് ശേഷം മുകളിൽ കണ്ടെത്തിയ ഉറവിടം: `school_ai_policy.md`
- പുനഃക്രമീകരണത്തിന് ശേഷം മുകളിൽ കണ്ടെത്തിയ വിഭാഗം: `Final Assignments`
- ഡിഫോൾട്ട് ഉത്തരം പാത: ലോക്കൽ ട്രാൻസ്പാരൻറ് ഉത്തരം കമ്പോസർ
- Ollama ജനറേഷൻ പാത: `phi4-mini:3.8b` ഉപയോഗിച്ച് പൂർത്തിയാക്കി
- Ollama മോഡൽ ഫയൽ സൈസ്: 2.49GB ഡിസ്കിൽ
- Ollama ലോഡ് ചെയ്ത മോഡൽ സൈസ്: `ollama ps` പ്രകാരം 3.3GB റിപ്പോർട്ട് ചെയ്യപ്പെട്ടത്
- GPU ഓഫ്‌ലോഡ്: `ollama ps` പ്രകാരം 100% GPU
- ജനറേഷന്ക്ക് ശേഷം GPU മെമ്മറി നിരീക്ഷണം: RTX 3060 ലാപ്ടോപ് GPUയിൽ 6GB ൽ ഏതാണ്ട് 3.5GB ഉപയോഗിച്ചതായി കാണ됨
- കാഷ് ചെയ്ത ഫാസ്റ്റ്‌എംബെഡ് മോഡലും Ollama ജനറേഷനും സജീവമാക്കിയുള്ള നോട്ട്‌ബുക്ക് എക്സിക്യൂഷൻ: സ്ഥിരീകരണ സ്ക്രിപ്റ്റിലൂടെ ഏകദേശം 34 സെക്കന്റിൽ വിജയകരമായി പാസ്സായി

Ollama ജനറേറ്റഡ് ഉത്തരമാണ്:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

ഈ ഉത്തരം പരിപൂർണമെന്ന് ഞാൻ വിളിക്കില്ല. ഇത് ശരിയായ തെളിവുകളിൽ നിന്ന് ഉത്തരം നൽകുന്നു, പക്ഷേ അന്തിമ ഉറവിട ലൈൻ നിർണായകമായ ഉദ്ധരണി ഫോർമാറ്റിന് സമാനമല്ല. ഇത് ട്യൂട്ടോറിയലിൽ കാണിക്കുന്നത് ഉപകാരപ്രദമാണ് കാരണം ഇത് അടുത്ത് വരുന്ന എഞ്ചിനീയറിങ് ചോദ്യത്തെ വ്യക്തമാക്കുന്നു: ഉത്തരം ജനറേഷൻക്കും വിലയിരുത്തൽ ആവശ്യമുണ്ട്, വെറും റിട്രീവൽ മാത്രം അല്ല.

ഈ പരിശോധിക്കൽ ചെയ്തപ്പോൾ ഞാൻ പ്രധാനമായി മനസ്സിലാക്കിയത് ഉത്തരം ജനറേഷൻക്ക് മുമ്പ് റിട്രീവൽ ഗുണമേന്മ പരിശോധിക്കണം എന്നതാണ്. എം‌ബഡ്ഡിംഗ് ഫലം ഇതിനകം ഉപകാരപ്രദമായിരുന്നു, ലഘുലേഖ പുനഃക്രമീകരണ ഉപകരണം പ്രതീക്ഷിച്ചതുപോലെ സംവരണ നയം വിഭാഗം നിഷ്ചിതമായി ആദ്യത്തേതായി പ്രത്യക്ഷപ്പെട്ടു. ട്യൂട്ടോറിയൽ മറച്ചുവെക്കാതെ ഇത്തരത്തിലുള്ള ചെറിയ സിസ്റ്റം പെരുമാറ്റം പുറത്തുകാണിക്കാൻ ഈ സിസ്റ്റം സഹായിക്കുന്നു.

## 12. അടുത്തത് എന്ത് വരും

അടുത്ത മെച്ചപ്പെടുത്തൽ ആയിരിക്കും ഈ ആഭ്യന്തര ക്രമീകരണത്തെ ആസ്യൂർ മാനേജ്ഡ് പതിപ്പുമായി താരതമ്യം ചെയ്യൽ, അതേ സ്കൂൾ നയ സഹായക രംഗം ഉപയോഗിച്ച്. രംഗം സ്ഥിരമായിരിക്കുകയാൽ വാഗ്ദാനം ചെയ്യുന്ന ട്രേഡോഫുകൾ ഏറെയും കാണാനാകും: ക്രമീകരണ സങ്കീർണ്ണത, റിട്രീവൽ നിയന്ത്രണങ്ങൾ, ഐഡന്റിറ്റി ഇന്റഗ്രേഷൻ, പ്രവർത്തന ഉടമസ്ഥാവകാശം, ചെലവ് എന്നിവ.

## 13. റഫറൻസുകൾ

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

മുന്പ്: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**അറിയിപ്പ്**:
ഈ രേഖ AI പരിഭാഷാ സേവനം [Co-op Translator](https://github.com/Azure/co-op-translator) ഉപയോഗിച്ച് പരിഭാഷപ്പെടുത്തിയതാണ്. ഞങ്ങൾ കൃത്യതയ്ക്കായി ശ്രമിക്കുന്നുവെങ്കിലും, ഓട്ടോമേറ്റഡ് പരിഭാഷകളിൽ പിഴവുകൾ അല്ലെങ്കിൽ തെറ്റായ വിവരങ്ങൾ ഉണ്ടാകാൻ സാധ്യതയുണ്ട്. അതിന്റെ സ്വാഭാവിക ഭാഷയിലുള്ള അസൽ രേഖയാണ് പ്രാമാണികമായ ഉറവിടമായി പരിഗണിക്കേണ്ടത്. നിർണായകമായ വിവരങ്ങൾക്ക്, പ്രൊഫഷണൽ മനുഷ്യ പരിഭാഷ ശുപാർശ ചെയ്യുന്നു. ഈ പരിഭാഷ ഉപയോഗിച്ച് ഉണ്ടാകുന്ന തെറ്റിദ്ധാരണകൾ അല്ലെങ്കിൽ തെറ്റായ വ്യാഖ്യാനങ്ങൾക്കായി ഞങ്ങൾ ഉത്തരവാദികളല്ല.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->