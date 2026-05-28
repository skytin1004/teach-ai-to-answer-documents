# Lær AI at Besvare Spørgsmål baseret på Dine Dokumenter
## Serie 2: Byg et Lokalt Open-Source RAG System fra Start til Slut

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Denne artikel omdanner Serie 1's arkitektur-diskussion til en kørbar lokal RAG tutorial. Målet er først at bygge hele workflowet med prøve-data, uden sky-konto og uden hemmeligheder, og derefter bruge den fungerende baseline til at træffe bedre arkitekturvalg senere.

Systemet vi vil bygge, er en lille skolepolitik-assistent. Jeg bruger to lokale Markdown dokumenter som vidensbase og gennemgår derefter hele RAG pipeline: chunking, lokale embeddings, Qdrant vektor opslag, retrieval, reranking, kilde-ansvarlig svarcomponering og valgfri lokal generering med Ollama og Phi-4-mini.

Serie navigation: [Repository hjem](../README.md) | Forrige: [Serie 1 - RAG, Azure vs Open-Source Alternativer, og Hvornår Fine-Tuning Giver Mening](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Krav: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Dette er det bedste udgangspunkt, hvis du vil forstå RAG pipelinen inden oprettelse af skyeressourcer. Standardvejen kører lokalt med CPU-venlige embeddings og uden hemmeligheder.

## 1. Hvad Vi Bygger

I 2023 tutorialen startede jeg med Azure, fordi målet var at vise, hvordan Azure AI Search og Azure OpenAI kunne besvare spørgsmål fra PDF-dokumenter.

For denne 2026 serie ønsker jeg at starte et lag dybere.

Inden brug af managed services, vil jeg bygge et lille RAG system lokalt og gøre hvert trin synligt: indlæsning af dokumenter, chunking af tekst, lagring af vektorer, hentning af beviser, reranking af resultater, og returnering af et kilde-ansvarligt svar.

Det eksemplariske scenarie er en skolepolitik-assistent. Brugeren spørger:

```text
Can I use generative AI for my final assignment?
```

Systemet må ikke svare ud fra generel modellhukommelse. Det skal hente den relevante politiksektion og svare ud fra det bevis.

Den fulde kørbare version findes i [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Koden herunder viser hovedtrinene, så artiklen kan læses som en tutorial.

## 2. Installer de Lokale Afhængigheder

Opret et virtuelt miljø og installer Serie 2 kravene:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Den første version bruger Qdrant i lokal tilstand og FastEmbed. Qdrants Python klient understøtter en in-memory lokal tilstand med `QdrantClient(":memory:")`, som er nyttig til lokale tutorials og CI-lignende verifikation. FastEmbed giver os en ægte lokal embedding-model uden krav om sky-API nøgle.

Kravfilen inkluderer også `python-dotenv`, fordi notebooken valgfrit kan læse et Ollama modelnavn fra `.env`. Ingen Azure OpenAI eller OpenAI API-nøgle er nødvendig for denne lokale tutorial.

## 3. Indlæs Prøvedokumenterne

Prøvekorpuset er bevidst lille:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

I notebooken indlæser jeg alle Markdown filer fra `sample_data/`:

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

Da jeg kørte notebooken, indlæste den 2 dokumenter. Det er småt nok til manuel inspektion, hvilket er nyttigt, når man bygger den første version af en RAG pipeline.

## 4. Chunk ved Markdown Overskrifter

Næste trin er at opdele dokumenter i chunks.

Til denne tutorial bruger jeg Markdown overskrifter som struktur-signal. Dokumenttitlen kommer fra `#`, og hver sektionschunk kommer fra `##`.

> [!NOTE]
> Chunking er ikke one-size-fits-all. I denne tutorial bruger jeg Markdown overskrifter, fordi prøve-dokumenterne har klare `#` og `##` strukturer. For PDF’er, Word dokumenter, slides, tickets eller websider kan en bedre strategi bruge sidegrænser, layoutinformation, semantiske sektioner, token-grænser, tabeller eller metadata. Det vigtige er at vælge en chunking-strategi, der bevarer mening og kilde-sporbarhed i dine dokumenter.

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

Så anvender jeg det på hvert dokument:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Dette skabte 8 chunks i mit lokale run.

Det, jeg kunne lide ved dette trin, er, at metadataene allerede er nyttige. Hver chunk kender sin `source`, `sectionHeading`, `documentVersion` og pladsholder `permissions`. Selv i en lille tutorial gør dette citations- og senere tilladelses-bevidst hentning lettere at forstå.

## 5. Opret Lokale Embeddings

Til den første offentlige version bruger jeg `BAAI/bge-small-en-v1.5` via FastEmbed.

Dette holder tutorialen lokal og CPU-venlig, men benytter stadig en ægte embedding-model i stedet for en pladsholder vektorfunktion. Første kørsel downloader modelvægtene. Derefter kan notebooken genbruge lokal cache.

> [!NOTE]
> Jeg bruger `BAAI/bge-small-en-v1.5`, fordi det er en letvægts engelsk embedding-model, der fungerer godt med FastEmbed og Qdrant til en lokal tutorial. Den skaber 384-dimensionelle vektorer, hvilket holder eksemplet hurtigt og billigt at køre lokalt. Dette er ikke det eneste gode valg. I 2023 brugte mange tutorials hosted embedding-modeller som `text-embedding-ada-002`. I dag er nyere hosted muligheder som OpenAI `text-embedding-3-small` og `text-embedding-3-large`, samt open-source muligheder som BGE, E5, MiniLM, Nomic Embed og flersprogede modeller som `BAAI/bge-m3` alle rimelige valg afhængigt af arbejdsbyrden. I produktion bør den rigtige embedding-model vælges gennem retrieval evaluering på dine egne dokumenter.

Nogle praktiske alternativer:

| Modellfamilie | Hvornår jeg ville overveje det |
| --- | --- |
| `text-embedding-ada-002` | Ældre hosted baseline, der optrådte i mange tutorials fra 2023-æraen. Jeg ville ikke vælge den som standard til en ny tutorial i dag. |
| `text-embedding-3-small` | Moderne hosted standard, når jeg vil have en stærk pris/præstations-balance og ikke behøver kun lokale embeddings. |
| `text-embedding-3-large` | Hosted mulighed, når hentningskvalitet er vigtigere end vektor-størrelse eller embedding-omkostning. |
| `BAAI/bge-small-en-v1.5` | Letvægts lokal engelsk baseline til tutorials, prototyper og CPU-venlige eksperimenter. |
| `BAAI/bge-base-en-v1.5` eller `BAAI/bge-large-en-v1.5` | Større lokale engelske modeller, når jeg vil have bedre hentningskvalitet og kan tillade mere beregning. |
| `BAAI/bge-m3` | Flersproglig eller længere-kontekst hentning, især når dokumenterne ikke kun er engelske. |
| `sentence-transformers/all-MiniLM-L6-v2` | Meget små og hurtige semantiske søgebasemodeller. Nyttig når hastighed og simpelhed er vigtigst. |
| `nomic-embed-text-v1.5` | Open lokal embedding mulighed, værd at teste til længere-kontekst eller portabilitetsfokuserede setups. |

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

Så får hver chunk en embedding:

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

## 6. Gem Vektorer i Qdrant Lokal Tilstand

Nu opretter vi en in-memory Qdrant samling og indsætter chunks med payload metadata.

> [!NOTE]
> I 2023 tutorialen brugte jeg FAISS, fordi det var en simpel og populær måde at demonstrere lokal vektorlignende søgning med LangChain. FAISS er stadig nyttigt til hurtige lokale eksperimenter. I denne 2026 version bruger jeg Qdrant, fordi jeg vil have tutorialen til at føles tættere på et produktions-RAG system. Qdrant lader mig gemme vektorer sammen med payload metadata som kildefil, sektionsoverskrift, dokumentversion og tilladelser. Det gør hentningen lettere at inspicere og forbereder eksemplet på filtrering, citationer og fremtidig persistent eller serverbaseret deployment.

FAISS er fantastisk til at vise vektorlignende søgning. Qdrant er bedre til at vise et lille men produktionsformet RAG hentningslag.

Nogle praktiske alternativer:

| Vektorlager / søgelag | Hvornår jeg ville overveje det |
| --- | --- |
| Qdrant | Lokale prototyper, metadatafiltrering, produktionsvenlig vektorsøgning, og et simpelt Python workflow. |
| Chroma | Hurtige lokale RAG eksperimenter og notebooks hvor simpelhed er vigtigst. |
| FAISS | Letvægts lokal vektorsøgning når jeg kun behøver lignende søgning og kan håndtere metadata separat. |
| Milvus | Større åbent-source vektorsøgning når teamet er klar til at drive en dedikeret vektordatabase. |
| Weaviate | Vektorsøgning med skema, metadata, hybrid søgning og managed eller egen-hostede deploymentsmuligheder. |
| Azure AI Search | Enterprise RAG på Azure, når jeg ønsker nøgleordsøgning, vektorsøgning, hybrid hentning, semantisk rangering, filtrering, sikkerhed og managed drift i ét søgelag. |
| PostgreSQL + pgvector | Teams der allerede bruger PostgreSQL og ønsker vektorsøgning tæt på applikationsdata. |

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

Indsæt derefter punkterne:

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

I mit run indsatte samlingen 8 vektorer.

Her begynder RAG systemet at blive muligt at inspicere. Vektordatabasen gemmer ikke kun vektorer; den gemmer tekstbeviser og de metadata, der er nødvendige til citationer.

## 7. Hent Kandidatchunks

Nu stiller vi spørgsmålet og henter kandidatchunks.

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

Her printer jeg de hentede chunks inden generering af svaret. Det er vigtigt. Hvis hentningen er forkert, vil genereringen kun skjule problemet bag flydende tekst.

## 8. Tilføj en Letvægts Reranker

Da jeg først testede hentningsstien, fandt vektorlignende søgning alene relateret politikindhold, men den mest præcise sektion var ikke altid øverst.

Så tilføjede jeg en lille lokal reranker. Den giver ekstra vægt, når spørgsmålets termer overlapper sektionsoverskriften og indholdet.

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

Efter reranking blev det øverste resultat:

```text
school_ai_policy.md / Final Assignments
```

Det var den forventede sektion til testspørgsmålet.

Dette var den mest nyttige lektion fra første implementering. Selv i et lille lokalt eksempel forbedredes hentningskvaliteten, når jeg kombinerede vektorlignende søgning med et andet signal.

## 9. Sammenstil et Jordbundet Lokalt Svar

Til standardvejen bruger jeg en transparent lokal svarcomponist i stedet for en LLM.

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

Dette er ikke ment som en endelig produkt-svargenerator. Det er et fejlfindingsværktøj. Det beviser, at hentning, metadata og citationssammenkædning virker, før man tilføjer model-varians.

## 10. Generer et Lokalt Svar med Ollama og Phi-4-mini

Når hentningen fungerer, kan notebooken erstatte kun det sidste svartrin med Ollama og `phi4-mini:3.8b`.

> [!NOTE]
> Ollama bør kun erstatte det sidste svargenereringstrin. Dokumentindlæsning, chunking, vektorlagring, hentning, reranking og citationssammenkædning bør forblive det samme.

Først bygger notebooken en bevisprompt fra de hentede chunks:

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

Til denne tutorial anbefaler jeg Microsofts Phi-4-mini familie gennem Ollama som standard lokal generationsmulighed. Modellen jeg testede i Ollama er:

```powershell
ollama pull phi4-mini:3.8b
```

Du kan hurtigt tjekke, at modellen er tilgængelig:

```powershell
ollama list
```

Sæt derefter disse variabler:

```powershell
Copy-Item .env.example .env
```

Åbn `.env` og fjern kommentaren fra Serie 2 Ollama værdierne:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebooken loader `.env` fra repository-roden med `python-dotenv`, og sender derefter samme bevisprompt til Ollamas lokale `/api/chat` endpoint med streaming slået fra. Hvis Ollama ikke kører eller `SERIES2_OLLAMA_MODEL` mangler, springes dette spor over.

> [!NOTE]
> På denne maskine downloadede `phi4-mini:3.8b` cirka 2,49GB model-filer. Under inferens rapporterede Ollama en indlæst modelstørrelse på 3,3GB og brugte RTX 3060 Laptop GPU.

Dette giver tutorialen to niveauer:

1. CPU-only deterministisk svarcomponist.
2. Lokal svar-generering med Ollama og Phi-4-mini.

Hentningspipen forbliver den samme i begge.

## 11. Verifikationsresultat

Jeg kørte notebooken lokalt på Windows med Python 3.12.6.

Installerede pakker:

| Pakke | Version |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Notebook-udførelse:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Kørsel resultat: bestået med `nbclient`
- Dokumenter indlæst: 2
- Chunks oprettet: 8
- Qdrant samling: `school_policy_local`
- Vektorer indsat: 8
- Embedding-model: `BAAI/bge-small-en-v1.5`
- Embedding-størrelse: 384
- Hentningsspørgsmål: "Kan jeg bruge generativ AI til min afsluttende opgave?"
- Omrankeringsvej: letvægts lokal leksikal omrangering
- Bedst hentede kilde efter omrangering: `school_ai_policy.md`
- Bedst hentede afsnit efter omrangering: `Final Assignments`
- Standard svarvej: lokal transparent svarkomponist
- Ollama genereringsvej: fuldført med `phi4-mini:3.8b`
- Ollama modelfilstørrelse: 2,49 GB på disk
- Ollama indlæst modelstørrelse: 3,3 GB rapporteret af `ollama ps`
- GPU aflastning: 100% GPU rapporteret af `ollama ps`
- GPU hukommelse observeret efter generering: omkring 3,5 GB af 6 GB brugt på RTX 3060 Laptop GPU
- Notebook eksekvering med cachet FastEmbed model og Ollama generering aktiveret: bestået på omkring 34 sekunder gennem verifikationsscriptet

Det Ollama-genererede svar var:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Jeg vil ikke kalde dette svar perfekt. Det svarer ud fra den rette evidens, men den sidste kildeangivelseslinje er mindre præcis end det deterministiske citationsformat. Det er nyttigt at vise i tutorialen, fordi det gør det næste ingeniørspørgsmål åbenlyst: svar generering kræver også evaluering, ikke kun hentning.

Det vigtigste, jeg lærte under verifikationen, er, at kvaliteten af hentningen bør kontrolleres før svar generering. Embedding-resultatet var allerede brugbart, og den lette omrangering fik forventet politikafsnit til pålideligt at fremstå først. Det er præcis den slags små systemadfærd, jeg ønsker, at tutorialen skal eksponere i stedet for at skjule.

## 12. Hvad kommer herefter

Den næste forbedring er at sammenligne denne lokale opsætning med en administreret Azure-version af samme skolepolitikassistent-scenarie. At bevare scenariet fastgjort bør gøre kompromiserne lettere at se: opsætningskompleksitet, hentningskontroller, identitetsintegration, operationelt ejerskab og omkostninger.

## 13. Referencer

- [Qdrant Python klient quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant klient GitHub repository](https://github.com/qdrant/qdrant-client)
- [FastEmbed understøttede modeller](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 modelkort](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 modelkort](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 modelkort](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini modelside](https://ollama.com/library/phi4-mini)
- [Ollama Windows dokumentation](https://docs.ollama.com/windows)
- [Ollama API streaming dokumentation](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct modelkort](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph oversigt](https://docs.langchain.com/oss/python/langgraph)
- [Introduktion til RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Forrige: [Serie 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->