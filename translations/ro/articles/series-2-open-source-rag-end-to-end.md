# Învățați AI să răspundă la întrebări pe baza documentelor dvs.
## Seria 2: Construirea unui sistem local RAG open-source de la început până la sfârșit

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Acest articol transformă discuția despre arhitectura din Seria 1 într-un tutorial local RAG executabil. Scopul este de a construi mai întâi întregul flux de lucru cu date de probă, fără cont în cloud și fără secrete, apoi de a folosi acest punct de referință funcțional pentru a lua decizii mai bune de arhitectură ulterior.

Sistemul pe care îl vom construi este un mic asistent pentru politica școlii. Folosesc două documente locale Markdown ca bază de cunoștințe, apoi parcurg întregul flux RAG: împărțirea în bucăți, încorporări locale, stocare vectorială Qdrant, regăsire, rerangare, compunerea răspunsurilor conștiente de sursă și generare locală opțională cu Ollama și Phi-4-mini.

Navigare serie: [Pagina principală a depozitului](../README.md) | Anterior: [Seria 1 - RAG, Azure vs alternative open-source și când are sens ajustarea fină](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Cerințe: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Acesta este cel mai bun punct de plecare dacă doriți să înțelegeți fluxul RAG înainte de a crea resurse în cloud. Calea implicită rulează local cu încorporări prietenoase cu CPU și fără secrete.

## 1. Ce construim

În tutorialul din 2023, am început de la Azure pentru că scopul era să arăt cum Azure AI Search și Azure OpenAI pot răspunde la întrebări din documente PDF.

Pentru această serie din 2026, vreau să pornesc de un nivel mai jos.

Înainte de a folosi servicii gestionate, vreau să construiesc un mic sistem RAG local și să fac fiecare pas vizibil: încărcarea documentelor, împărțirea textului în bucăți, stocarea vectorilor, regăsirea probelor, rerangarea rezultatelor și întoarcerea unui răspuns conștient de sursă.

Scenariul de probă este un asistent pentru politica școlii. Utilizatorul întreabă:

```text
Can I use generative AI for my final assignment?
```

Sistemul nu trebuie să răspundă din memoria generală a modelului. Trebuie să recupereze secțiunea relevantă a politicii și să răspundă pe baza acelei dovezi.

Versiunea completă executabilă este în [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Codul de mai jos arată pașii principali pentru ca articolul să poată fi citit ca un tutorial.

## 2. Instalați dependențele locale

Creați un mediu virtual și instalați cerințele Seriei 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Prima versiune folosește modul local Qdrant și FastEmbed. Clientul Python Qdrant suportă un mod local în memorie cu `QdrantClient(":memory:")`, care este util pentru tutoriale locale și verificări de tip CI. FastEmbed ne oferă un model real local de încorporare fără a necesita o cheie API de cloud.

Fișierul de cerințe include și `python-dotenv` pentru că notebook-ul poate opțional să citească un nume de model Ollama din `.env`. Nu este necesară o cheie Azure OpenAI sau OpenAI API pentru acest tutorial local.

## 3. Încărcați documentele de probă

Corpusul de probă este intenționat mic:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

În notebook, încarc toate fișierele Markdown din `sample_data/`:

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

Când am rulat notebook-ul, a încărcat 2 documente. Aceasta este suficient de mic pentru a inspecta manual, ceea ce este util la construirea primei versiuni a unui flux RAG.

## 4. Împărțiți după titlurile Markdown

Pasul următor este să împărțim documentele în bucăți.

Pentru acest tutorial, folosesc titlurile Markdown ca semnal de structură. Titlul documentului vine de la `#`, iar fiecare secțiune vine de la `##`.

> [!NOTE]
> Împărțirea în bucăți nu este un proces universal. În acest tutorial folosesc titluri Markdown deoarece documentele de probă au o structură clară `#` și `##`. Pentru PDF-uri, documente Word, slide-uri, bilete sau pagini web, o strategie mai bună poate folosi limite de pagină, informații de layout, secțiuni semantice, limite de tokeni, tabele sau metadate. Important este să alegi o strategie de împărțire care păstrează semnificația și trasabilitatea sursei pentru documentele tale.

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

Apoi o aplic pe fiecare document:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Acest lucru a creat 8 bucăți în rularea mea locală.

Ce mi-a plăcut la acest pas este că metadatele sunt deja utile. Fiecare bucată știe sursa (`source`), titlul secțiunii (`sectionHeading`), versiunea documentului (`documentVersion`) și permisiunile reprezentate printr-un substituent (`permissions`). Chiar și într-un tutorial mic, asta face citările și regăsirea ulterioară conștientă de permisiuni mai ușor de gestionat.

## 5. Creați încorporări locale

Pentru prima versiune publică, folosesc `BAAI/bge-small-en-v1.5` prin FastEmbed.

Acest lucru menține tutorialul local și prietenos cu CPU, dar folosește încă un model real de încorporare în loc de o funcție vector placeholder. Prima rulare descarcă greutățile modelului. După aceea, notebook-ul poate reutiliza cache-ul local.

> [!NOTE]
> Folosesc `BAAI/bge-small-en-v1.5` pentru că este un model de încorporare ușor în limba engleză care funcționează bine cu FastEmbed și Qdrant pentru un tutorial local. Creează vectori cu 384 dimensiuni, ceea ce menține exemplul rapid și ieftin pentru rularea locală. Aceasta nu este singura alegere bună. În 2023, multe tutoriale foloseau modele gazduite de încorporare, precum `text-embedding-ada-002`. Astăzi, opțiuni mai noi găzduite, cum ar fi OpenAI `text-embedding-3-small` și `text-embedding-3-large`, și opțiuni open-source precum BGE, E5, MiniLM, Nomic Embed și modele multilingve precum `BAAI/bge-m3` sunt toate alegeri rezonabile în funcție de sarcină. În producție, modelul de încorporare potrivit ar trebui selectat prin evaluarea regăsirii pe propriile documente.

Câteva alternative practice:

| Familie model | Când aș lua în considerare |
| --- | --- |
| `text-embedding-ada-002` | Referință mai veche găzduită care a apărut în multe tutoriale din 2023. Nu aș alege-o ca implicită pentru un tutorial nou astăzi. |
| `text-embedding-3-small` | Implicit modern găzduit când vreau un echilibru puternic cost/performance și nu am nevoie de încorporări doar locale. |
| `text-embedding-3-large` | Opțiune găzduită când calitatea regăsirii contează mai mult decât dimensiunea vectorului sau costul încorporării. |
| `BAAI/bge-small-en-v1.5` | Referință locală ușoară în engleză pentru tutoriale, prototipuri și experimente prietenoase cu CPU. |
| `BAAI/bge-base-en-v1.5` sau `BAAI/bge-large-en-v1.5` | Modele locale în engleză mai mari când vreau calitate mai bună la regăsire și pot permite resurse mai mari. |
| `BAAI/bge-m3` | Regăsire multilingvă sau de context mai lung, în special când documentele nu sunt doar în engleză. |
| `sentence-transformers/all-MiniLM-L6-v2` | Referință semantică foarte mică și rapidă pentru căutare. Utilă când viteza și simplitatea contează cel mai mult. |
| `nomic-embed-text-v1.5` | Opțiune locală open embedding care merită testată pentru contexte mai lungi sau configurații orientate pe portabilitate. |

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

Apoi fiecare bucată primește o încorporare:

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

## 6. Stocați vectorii în modul local Qdrant

Acum creăm o colecție Qdrant în memorie și inserăm bucățile cu metadate în payload.

> [!NOTE]
> În tutorialul din 2023, am folosit FAISS deoarece era o metodă simplă și populară pentru a demonstra căutarea locală vectorială similară cu LangChain. FAISS este încă util pentru experimente locale rapide. În această versiune 2026, folosesc Qdrant deoarece vreau ca tutorialul să se simtă mai aproape de un sistem RAG pentru producție. Qdrant permite stocarea vectorilor împreună cu metadatele payload, cum ar fi fișierul sursă, titlul secțiunii, versiunea documentului și permisiunile. Asta face căutarea mai ușor de inspectat și pregătește exemplul pentru filtrare, citări și implementări viitoare persistente sau bazate pe server.

FAISS este grozav pentru demonstrarea căutării vectoriale după similitudine. Qdrant este mai bun pentru a arăta un strat mic, dar modelat pentru producție, de regăsire RAG.

Câteva alternative practice:

| Magazin vector / strat de căutare | Când aș lua în considerare |
| --- | --- |
| Qdrant | Prototipuri locale, filtrare metadata, căutare vectorială prietenoasă cu producția și flux de lucru Python simplu. |
| Chroma | Experimente locale rapide RAG și notebook-uri unde simplitatea contează cel mai mult. |
| FAISS | Căutare locală vectorială ușoară când am nevoie doar de căutare după similaritate și pot gestiona separat metadatele. |
| Milvus | Căutare vectorială open-source la scară mai mare când echipa este pregătită să opereze o bază de date vectorială dedicată. |
| Weaviate | Căutare vectorială cu schemă, metadate, căutare hibridă și opțiuni de implementare gestionată sau auto-găzduită. |
| Azure AI Search | RAG enterprise pe Azure când vreau căutare pe cuvinte cheie, căutare vectorială, regăsire hibridă, rang semantic, filtrare, securitate și operații gestionate într-un singur strat de căutare. |
| PostgreSQL + pgvector | Echipe care folosesc deja PostgreSQL și doresc căutare vectorială aproape de datele aplicației. |

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

Apoi inserăm punctele:

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

În rularea mea, colecția a inserat 8 vectori.

Aici începe sistemul RAG să devină inspectabil. Baza de date vectorială nu stochează doar vectori; stochează textul de dovezi și metadatele necesare pentru citări.

## 7. Regăsiți bucățile candidate

Acum punem întrebarea și regăsim bucățile candidate.

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

În acest punct, afișez bucățile regăsite înainte de generarea răspunsului. Acest lucru este important. Dacă regăsirea este greșită, generarea va ascunde problema în spatele unui text fluent.

## 8. Adăugați un reranker ușor

Când am testat prima dată calea de regăsire, similitudinea vectorială singură găsea conținut de politică legat, dar secțiunea cea mai precisă nu era întotdeauna prima pe listă.

Așa că am adăugat un mic reranker local. Acesta oferă greutate suplimentară când termenii întrebării se suprapun cu titlul secțiunii și conținutul acesteia.

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

După rerangare, rezultatul de top a devenit:

```text
school_ai_policy.md / Final Assignments
```

Aceasta a fost secțiunea așteptată pentru întrebarea de test.

Aceasta a fost lecția cea mai utilă din prima implementare. Chiar și într-un exemplu local mic, calitatea regăsirii a îmbunătățit când am combinat similitudinea vectorială cu un alt semnal.

## 9. Compuneți un răspuns local fundamentat

Pentru calea implicită, folosesc un compozitor transparent local de răspunsuri în loc de un LLM.

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

Acesta nu este menit să fie un generator final de răspunsuri. Este un instrument de depanare. Demonstrează că regăsirea, metadatele și legăturile de citare funcționează înainte de a adăuga variabilitate modelului.

## 10. Generați un răspuns local cu Ollama și Phi-4-mini

Odată ce regăsirea funcționează, notebook-ul poate înlocui doar pasul final de generare a răspunsului cu Ollama și `phi4-mini:3.8b`.

> [!NOTE]
> Ollama trebuie să înlocuiască doar pasul final de generare a răspunsului. Încărcarea documentelor, împărțirea în bucăți, stocarea vectorilor, regăsirea, rerangarea și legăturile de citare trebuie să rămână la fel.

Mai întâi, notebook-ul construiește un prompt de dovezi din bucățile regăsite:

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

Pentru acest tutorial, recomand familia Phi-4-mini de la Microsoft prin Ollama ca opțiune implicită locală de generare. În Ollama, numele modelului pe care l-am testat este:

```powershell
ollama pull phi4-mini:3.8b
```

Puteți verifica rapid că modelul este disponibil:

```powershell
ollama list
```

Apoi setați aceste variabile:

```powershell
Copy-Item .env.example .env
```

Deschideți `.env` și debifați valorile Seriei 2 Ollama:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook-ul încarcă `.env` din rădăcina depozitului cu `python-dotenv`, apoi trimite același prompt de dovezi către endpoint-ul local `/api/chat` al Ollama cu streaming dezactivat. Dacă Ollama nu rulează sau `SERIES2_OLLAMA_MODEL` lipsește, această cale este omisă.

> [!NOTE]
> Pe această mașină, `phi4-mini:3.8b` a descărcat circa 2.49GB de fișiere model. În timpul inferenței, Ollama a raportat o dimensiune încărcată a modelului de 3.3GB și a folosit GPU-ul RTX 3060 Laptop.

Aceasta oferă tutorialului două niveluri:

1. Compozitor de răspunsuri determinist doar CPU.
2. Generare locală de răspuns cu Ollama și Phi-4-mini.

Fluxul de regăsire rămâne același în ambele.

## 11. Rezultatul verificării

Am rulat notebook-ul local pe Windows cu Python 3.12.6.

Pachetele instalate:

| Pachet | Versiune |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Executarea notebook-ului:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Rezultatul execuției: trecut cu `nbclient`
- Documente încărcate: 2
- Bucăți create: 8
- Colecția Qdrant: `school_policy_local`
- Vectori inserați: 8
- Model de încorporare: `BAAI/bge-small-en-v1.5`
- Dimensiune încorporare: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Nu aș numi acest răspuns perfect. Răspunde pe baza dovezii corecte, dar linia finală a sursei este mai puțin precisă decât formatul determinist de citare. Acest lucru este util să fie arătat în tutorial deoarece face evidentă următoarea întrebare de inginerie: generarea răspunsului trebuie evaluată, nu doar preluarea.

Principala lecție pe care am învățat-o în timpul verificării este că calitatea preluării trebuie verificată înainte de generarea răspunsului. Rezultatul embeddingului a fost deja util, iar rerank-atorul ușor a făcut ca secțiunea de politică așteptată să apară fiabil prima. Acesta este exact tipul de comportament mic al sistemului pe care vreau ca tutorialul să îl expună în loc să îl ascundă.

## 12. Ce Urmează

Următoarea îmbunătățire este să compar acest setup local cu o versiune gestionată Azure a aceluiași scenariu asistent politicii școlii. Menținând scenariul fix ar trebui să facă compromisurile mai ușor de observat: complexitatea configurării, controalele preluării, integrarea identității, proprietatea operațională și costul.

## 13. Referințe

- [Introducere rapidă în clientul Python Qdrant](https://python-client.qdrant.tech/quickstart.html)
- [Depozitul GitHub al clientului Qdrant](https://github.com/qdrant/qdrant-client)
- [Modele suportate FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Ghid embedding-uri OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Fișa modelului BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Fișa modelului BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Fișa modelului sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Pagina modelului Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Documentație Ollama Windows](https://docs.ollama.com/windows)
- [Documentație API Ollama streaming](https://docs.ollama.com/api/streaming)
- [Fișa modelului Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Prezentare LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Introducere în RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Anterior: [Seria 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->