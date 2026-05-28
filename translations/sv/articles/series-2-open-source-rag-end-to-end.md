# Lär AI att besvara frågor baserat på dina dokument
## Serie 2: Bygg ett lokalt open-source RAG-system från början till slut

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Den här artikeln omvandlar diskussionen om arkitektur i Serie 1 till en körbar lokal RAG-guide. Målet är att först bygga hela arbetsflödet med exempeldatum, utan molnkonto och utan hemligheter, och sedan använda den fungerande baslinjen för att fatta bättre arkitekturval senare.

Systemet vi kommer att bygga är en liten assistent för skolpolicy. Jag använder två lokala Markdown-dokument som kunskapsbas, och går sedan igenom hela RAG-pipelinen: uppdelning i delar, lokala inbäddningar, Qdrant-vektorlager, hämtning, omrankning, källmedveten svarskomposition och valfri lokal generering med Ollama och Phi-4-mini.

Serie-navigering: [Repository hem](../README.md) | Föregående: [Serie 1 - RAG, Azure vs Open-Source-alternativ, och när finjustering är meningsfullt](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Krav: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Detta är den bästa startpunkten om du vill förstå RAG-pipelinen innan du skapar molnresurser. Standardvägen körs lokalt med CPU-vänliga inbäddningar och utan hemligheter.

## 1. Vad vi bygger

I tutorialen 2023 började jag med Azure eftersom målet var att visa hur Azure AI Search och Azure OpenAI kunde besvara frågor från PDF-dokument.

För denna serie 2026 vill jag börja ett steg lägre.

Innan jag använder hanterade tjänster vill jag bygga ett litet RAG-system lokalt och göra varje steg synligt: ladda dokument, dela upp text, lagra vektorer, hämta bevis, rangordna om resultaten och returnera ett källmedvetet svar.

Exemplet är en assistent för skolpolicy. Användaren frågar:

```text
Can I use generative AI for my final assignment?
```

Systemet ska inte svara utifrån allmän modellminne. Det ska hämta den relevanta policydelen och svara baserat på det beviset.

Den fullständiga körbara versionen finns i [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Koden nedan visar huvudsakliga steg så artikeln kan läsas som en guide.

## 2. Installera lokala beroenden

Skapa en virtuell miljö och installera Serie 2-kraven:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Första versionen använder Qdrant i lokalt läge och FastEmbed. Qdrants Python-klient stöder ett lokalt läge i minnet med `QdrantClient(":memory:")`, vilket är användbart för lokala tutorials och CI-verifiering. FastEmbed ger oss en äkta lokal inbäddningsmodell utan krav på moln-API-nyckel.

Kravfilen inkluderar även `python-dotenv` eftersom notebooken valfritt kan läsa in ett Ollama-modellnamn från `.env`. Ingen Azure OpenAI eller OpenAI API-nyckel krävs för denna lokala tutorial.

## 3. Ladda exempeldokument

Exempelkorpuset är avsiktligt litet:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

I notebooken laddar jag alla Markdown-filer från `sample_data/`:

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

När jag körde notebooken laddade den 2 dokument. Det är tillräckligt litet för att inspekteras manuellt, vilket är användbart när man bygger den första versionen av en RAG-pipeline.

## 4. Dela upp efter Markdown-rubriker

Nästa steg är att dela upp dokumenten i bitar.

För denna tutorial använder jag Markdown-rubriker som strukturmarkör. Dokumenttiteln kommer från `#`, och varje avsnittsklump kommer från `##`.

> [!NOTE]
> Uppdelning är inte en lösning för alla. I denna tutorial använder jag Markdown-rubriker eftersom exempeldokumenten har tydlig `#` och `##`-struktur. För PDF, Word-dokument, presentationsbilder, ticketar eller webbsidor kan en bättre strategi användas såsom sidgränser, layoutinformation, semantiska avsnitt, tokenbegränsningar, tabeller eller metadata. Det viktiga är att välja en uppdelningsstrategi som bevarar betydelse och källspårbarhet för dina dokument.

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

Sedan tillämpar jag det på varje dokument:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Detta skapade 8 klumpar i min lokala körning.

Vad jag gillade med detta steg är att metadata redan är användbar. Varje klump vet sin `source`, `sectionHeading`, `documentVersion` och platshållarskopia för `permissions`. Även i en liten tutorial gör detta citat och senare källmedveten hämtning enklare att resonera kring.

## 5. Skapa lokala inbäddningar

För den första publika versionen använder jag `BAAI/bge-small-en-v1.5` via FastEmbed.

Det håller tutorialen lokal och CPU-vänlig, men använder ändå en riktig inbäddningsmodell istället för en platshållarvektorfunktion. Första körningen laddar ner modellvikterna. Därefter kan notebooken återanvända den lokala cachén.

> [!NOTE]
> Jag använder `BAAI/bge-small-en-v1.5` eftersom det är en lättviktig engelsk inbäddningsmodell som fungerar bra med FastEmbed och Qdrant för en lokal tutorial. Den skapar 384-dimensionella vektorer, vilket håller exemplet snabbt och billigt att köra lokalt. Detta är inte det enda bra valet. År 2023 använde många tutorials hostade inbäddningsmodeller som `text-embedding-ada-002`. Idag är nyare hostade alternativ som OpenAI `text-embedding-3-small` och `text-embedding-3-large`, och open-source alternativ som BGE, E5, MiniLM, Nomic Embed och flerspråkiga modeller som `BAAI/bge-m3` alla rimliga val beroende på arbetsbelastningen. I produktion bör rätt inbäddningsmodell väljas utifrån utvärdering av hämtning på dina egna dokument.

Några praktiska alternativ:

| Modellfamilj | När jag skulle överväga den |
| --- | --- |
| `text-embedding-ada-002` | Äldre hostad baslinje som förekom i många tutorials från 2023. Jag skulle inte välja den som standard för en ny tutorial idag. |
| `text-embedding-3-small` | Modern hostad standard när jag vill ha bra balans mellan kostnad/prestanda och inte behöver endast lokala inbäddningar. |
| `text-embedding-3-large` | Hostat alternativ när hämtningens kvalitet är viktigare än vektorstorlek eller inbäddningskostnad. |
| `BAAI/bge-small-en-v1.5` | Lättviktig lokal engelsk baslinje för tutorials, prototyper och CPU-vänliga experiment. |
| `BAAI/bge-base-en-v1.5` eller `BAAI/bge-large-en-v1.5` | Större lokala engelska modeller för bättre hämtning när jag har mer datorkraft att tillgå. |
| `BAAI/bge-m3` | Flerspråkig eller längre kontexthämtning, särskilt när dokument inte bara är på engelska. |
| `sentence-transformers/all-MiniLM-L6-v2` | Mycket liten och snabb semantisk sökbaslinje. Användbar när hastighet och enkelhet är viktigast. |
| `nomic-embed-text-v1.5` | Öppen lokal inbäddningsoption värd att testa för längre kontext eller portabilitetsfokuserade lösningar. |

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

Sedan får varje klump en inbäddning:

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

## 6. Lagra vektorer i Qdrant lokalt läge

Nu skapar vi en Qdrant-samling i minnet och lägger in klumparna med metadata som payload.

> [!NOTE]
> I tutorialen 2023 använde jag FAISS eftersom det var ett enkelt och populärt sätt att demonstrera lokal vektorsökningslikhet med LangChain. FAISS är fortfarande användbart för snabba lokala experiment. I denna 2026-version använder jag Qdrant eftersom jag vill att tutorialen ska kännas närmare ett produktions-RAG-system. Qdrant låter mig lagra vektorer tillsammans med metadata som källfil, avsnittsrubrik, dokumentversion och rättigheter. Det gör hämtningen lättare att inspektera och förbereder exemplet för filtrering, citat och framtida ihållande eller serverbaserad utrullning.

FAISS är bra för att visa vektorsökningslikhet. Qdrant är bättre för att visa ett litet men produktionslikt RAG-hämtlager.

Några praktiska alternativ:

| Vektorlager / söklager | När jag skulle överväga det |
| --- | --- |
| Qdrant | Lokala prototyper, metadatafiltrering, produktionsvänlig vektorsökning och enkelt Python-flöde. |
| Chroma | Snabba lokala RAG-experiment och notebooks där enkelhet är högsta prioritet. |
| FAISS | Lättviktig lokal vektorsökning när jag bara behöver likhetssökning och kan hantera metadata separat. |
| Milvus | Open-source vektorsökning i större skala när teamet är redo att driva en dedikerad vektordatabas. |
| Weaviate | Vektorsökning med schema, metadata, hybrid-sökning samt hanterade eller självhostade alternativ. |
| Azure AI Search | Företags-RAG på Azure när jag vill ha nyckelordssökning, vektorsökning, hybrid-hämtning, semantisk rankning, filtrering, säkerhet och hanterade operationer i ett söklager. |
| PostgreSQL + pgvector | Team som redan använder PostgreSQL och vill ha vektorsök nära applikationsdata. |

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

Sedan lägger vi in punkterna:

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

I min körning matades 8 vektorer in i samlingen.

Här börjar RAG-systemet bli inspekterbart. Vektordatabasen lagrar inte bara vektorer; den lagrar bevistext och metadata som behövs för citat.

## 7. Hämta kandidatklumpar

Nu ställer vi frågan och hämtar kandidatklumpar.

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

Vid det här laget skriver jag ut de hämtade klumparna innan jag genererar ett svar. Det är viktigt. Om hämtningen är fel, kommer genereringen bara att dölja problemet bakom flytande text.

## 8. Lägg till en lättvikts-omrankare

När jag först testade hämtvägen, hittade vektorskillnad liknande policyn innehåll, men det mest precisa avsnittet låg inte alltid överst.

Så jag lade till en liten lokal omrankare. Den ger extra vikt när frågetermen överlappar med avsnitts-rubriken och innehållet.

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

Efter omrankning blev toppresultatet:

```text
school_ai_policy.md / Final Assignments
```

Det var det förväntade avsnittet för testfrågan.

Det var den mest användbara lärdomen från första implementationen. Även i ett litet lokalt exempel förbättrades hämtkvaliteten när jag kombinerade vektorskillnad med en annan signal.

## 9. Sätt ihop ett förankrat lokalt svar

För standardvägen använder jag en transparent lokal svarskompositör istället för en LLM.

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

Det här är inte tänkt som en slutprodukt för svarsgenerering. Det är ett felsökningsverktyg. Det bevisar att hämtning, metadata och citatkoppling fungerar innan man lägger till modellvariation.

## 10. Generera ett lokalt svar med Ollama och Phi-4-mini

När hämtningen fungerar kan notebooken ersätta endast sista svarssteg med Ollama och `phi4-mini:3.8b`.

> [!NOTE]
> Ollama bör endast ersätta det sista steget för svarsgenerering. Dokumentladdning, uppdelning, vektorlager, hämtning, omrankning och citatkoppling ska vara desamma.

Först bygger notebooken en bevis-prompt från de hämtade klumparna:

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

För denna tutorial rekommenderar jag Microsofts Phi-4-mini-familj via Ollama som standard för lokal generering. I Ollama är modellnamnet jag testade:

```powershell
ollama pull phi4-mini:3.8b
```

Du kan snabbt kontrollera att modellen är tillgänglig:

```powershell
ollama list
```

Sedan sätter du dessa variabler:

```powershell
Copy-Item .env.example .env
```

Öppna `.env` och avkommentera Serie 2:s Ollama-värden:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebooken laddar `.env` från repository-root med `python-dotenv`, och skickar sedan samma bevis-prompt till Ollamas lokala `/api/chat`-endpoint med strömning avstängd. Om Ollama inte körs eller `SERIES2_OLLAMA_MODEL` saknas, hoppar den över detta spår.

> [!NOTE]
> På denna maskin laddade `phi4-mini:3.8b` ner cirka 2,49 GB modellfiler. Under inferens rapporterade Ollama en modellstorlek på 3,3 GB och använde RTX 3060 Laptop GPU.

Det ger tutorialen två nivåer:

1. CPU-endast deterministisk svarskompositör.
2. Lokal svarsgenerering med Ollama och Phi-4-mini.

Hämtningspipelinen är densamma i båda.

## 11. Verifieringsresultat

Jag körde notebooken lokalt i Windows med Python 3.12.6.

Installerade paket:

| Paket | Version |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Notebook-körning:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Körningsresultat: godkänd med `nbclient`
- Dokument laddade: 2
- Klumpar skapade: 8
- Qdrant-samling: `school_policy_local`
- Vektorer insatta: 8
- Inbäddningsmodell: `BAAI/bge-small-en-v1.5`
- Inbäddningsstorlek: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Jag skulle inte kalla detta svar perfekt. Det svarar från rätt bevis, men den sista källraden är mindre exakt än det deterministiska citeringsformatet. Det är användbart att visa i handledningen eftersom det gör nästa teknikfråga uppenbar: svarsgenerering behöver också utvärderas, inte bara återvinning.

Det viktigaste jag lärde mig vid verifieringen är att återvinningskvaliteten bör kontrolleras innan svarsgenereringen. Inbäddningsresultatet var redan användbart, och den lätta omsorteraren gjorde att den förväntade policydelen pålitligt dök upp först. Det är just den typen av små systembeteenden jag vill att handledningen ska exponera istället för att dölja.

## 12. Vad kommer härnäst

Nästa förbättring är att jämföra denna lokala installation med en hanterad Azure-version av samma skolpolicyassistentscenario. Att hålla scenariot fast bör göra avvägningarna lättare att se: installationskomplexitet, återvinningskontroller, identitetsintegrering, operativt ägarskap och kostnad.

## 13. Referenser

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

Föregående: [Serie 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->