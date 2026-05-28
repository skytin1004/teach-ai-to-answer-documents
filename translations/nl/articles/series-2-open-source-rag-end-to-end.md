# Leer AI vragen beantwoorden op basis van uw documenten
## Serie 2: Bouw een lokale open-source RAG-systeem van begin tot eind

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Dit artikel zet de architectuurdiscussie uit Serie 1 om in een uitvoerbare lokale RAG-tutorial. Het doel is om eerst de volledige workflow te bouwen met voorbeeldgegevens, zonder cloudaccount en zonder geheimen, en vervolgens die werkende basislijn te gebruiken om later betere architectuurbeslissingen te nemen.

Het systeem dat we gaan bouwen is een kleine assistent voor schoolbeleid. Ik gebruik twee lokale Markdown-documenten als kennisbasis en loop vervolgens de volledige RAG-pijplijn door: opdelen in stukken, lokale embeddings, vectoropslag met Qdrant, ophalen, herordenen, bronbewuste samenstelling van antwoorden en optionele lokale generatie met Ollama en Phi-4-mini.

Navigatie serie: [Repository home](../README.md) | Vorige: [Serie 1 - RAG, Azure vs Open-Source Alternatieven, en Wanneer Fine-Tuning Zinvol Is](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Vereisten: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Dit is het beste startpunt als u de RAG-pijplijn wilt begrijpen voordat u cloudresources aanmaakt. Het standaardpad draait lokaal met CPU-vriendelijke embeddings en zonder geheimen.

## 1. Wat we bouwen

In de tutorial van 2023 begon ik vanuit Azure omdat het doel was te laten zien hoe Azure AI Search en Azure OpenAI vragen konden beantwoorden uit PDF-documenten.

Voor deze serie in 2026 wil ik één laag lager beginnen.

Voordat ik beheerde diensten gebruik, wil ik lokaal een klein RAG-systeem bouwen en elke stap zichtbaar maken: documenten laden, tekst opdelen, vectors opslaan, bewijs ophalen, herordenen van resultaten en een bronbewust antwoord teruggeven.

Het voorbeeldscenario is een assistent voor schoolbeleid. De gebruiker vraagt:

```text
Can I use generative AI for my final assignment?
```

Het systeem mag niet antwoorden vanuit de algemene modelgeheugen. Het moet de relevante beleidssectie ophalen en van dat bewijs antwoorden.

De volledige uitvoerbare versie staat in [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). De code hieronder toont de hoofdlijnen zodat het artikel als tutorial gelezen kan worden.

## 2. Installeer de lokale afhankelijkheden

Maak een virtuele omgeving aan en installeer de vereisten van Serie 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

De eerste versie gebruikt Qdrant in lokale modus en FastEmbed. De Python-client van Qdrant ondersteunt een in-memory lokale modus met `QdrantClient(":memory:")`, wat nuttig is voor lokale tutorials en CI-achtige verificatie. FastEmbed geeft ons een echt lokaal embeddingmodel zonder een cloud-API-sleutel te vereisen.

Het requirements-bestand bevat ook `python-dotenv` omdat de notebook optioneel een Ollama-modelnaam kan lezen vanuit `.env`. Voor deze lokale tutorial is geen Azure OpenAI- of OpenAI-API-sleutel nodig.

## 3. Laad de voorbeelddocumenten

De voorbeeldcorpus is bewust klein:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

In de notebook laad ik alle Markdown-bestanden uit `sample_data/`:

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

Toen ik de notebook draaide, werden er 2 documenten geladen. Dat is klein genoeg om handmatig te inspecteren, wat nuttig is bij het bouwen van de eerste versie van een RAG-pijplijn.

## 4. Opdelen op basis van Markdown-koppen

De volgende stap is documenten opdelen in stukken.

Voor deze tutorial gebruik ik Markdown-koppen als structuurgegeven. De titel van het document komt van `#`, en elk sectiestuk van `##`.

> [!NOTE]
> Chunking is niet één-op-één toepasbaar. In deze tutorial gebruik ik Markdown-koppen omdat de voorbeelddocumenten een duidelijke `#` en `##` structuur hebben. Voor PDF's, Word-documenten, slides, tickets of webpagina's kan een betere strategie gebruik maken van pagina-grenzen, lay-outinformatie, semantische secties, tokenlimieten, tabellen of metadata. Het belangrijkste is een chunking-strategie te kiezen die betekenis en brontraceerbaarheid van je documenten behoudt.

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

Daarna pas ik het toe op elk document:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Dit resulteerde in 8 stukken in mijn lokale uitvoering.

Wat ik prettig vond aan deze stap is dat de metadata al nuttig is. Elk stuk kent zijn `source`, `sectionHeading`, `documentVersion` en tijdelijke `permissions`. Zelfs in een kleine tutorial maakt dit het makkelijker om citaten en later toestemming-gebaseerde ophalen te begrijpen.

## 5. Maak lokale embeddings

Voor de eerste openbare versie gebruik ik `BAAI/bge-small-en-v1.5` via FastEmbed.

Dit houdt de tutorial lokaal en CPU-vriendelijk, maar gebruikt nog steeds een echt embeddingmodel in plaats van een placeholder-vectorfunctie. De eerste keer downloadt het de modelgewichten. Daarna kan de notebook de lokale cache hergebruiken.

> [!NOTE]
> Ik gebruik `BAAI/bge-small-en-v1.5` omdat het een lichtgewicht Engels embeddingmodel is dat goed werkt met FastEmbed en Qdrant voor een lokale tutorial. Het creëert 384-dimensionale vectors, wat het voorbeeld snel en goedkoop maakt om lokaal uit te voeren. Dit is niet de enige goede keuze. In 2023 gebruikten veel tutorials gehoste embeddingmodellen zoals `text-embedding-ada-002`. Tegenwoordig zijn nieuwere gehoste opties zoals OpenAI `text-embedding-3-small` en `text-embedding-3-large`, en open-source opties zoals BGE, E5, MiniLM, Nomic Embed, en meertalige modellen zoals `BAAI/bge-m3` allemaal redelijke keuzes afhankelijk van de workload. In productie hoort het juiste embeddingmodel geselecteerd te worden via retrieval-evaluatie op je eigen documenten.

Enkele praktische alternatieven:

| Modelfamilie | Wanneer ik het zou overwegen |
| --- | --- |
| `text-embedding-ada-002` | Oudere gehoste baseline die in veel tutorials rond 2023 voorkwam. Ik zou het niet standaard kiezen voor een nieuwe tutorial vandaag. |
| `text-embedding-3-small` | Moderne gehoste standaard wanneer ik een goede kosten/prestatie-balans wil en geen strikt lokale embeddings nodig heb. |
| `text-embedding-3-large` | Gehoste optie wanneer retrievalkwaliteit belangrijker is dan vectorgrootte of embeddingkosten. |
| `BAAI/bge-small-en-v1.5` | Lichtgewicht lokaal Engels basismodel voor tutorials, prototypes en CPU-vriendelijke experimenten. |
| `BAAI/bge-base-en-v1.5` of `BAAI/bge-large-en-v1.5` | Grotere lokale Engelse modellen wanneer ik betere retrievalkwaliteit wil en meer rekenkracht kan veroorloven. |
| `BAAI/bge-m3` | Meertalig of retrieval met langere context, vooral wanneer documenten niet alleen Engels zijn. |
| `sentence-transformers/all-MiniLM-L6-v2` | Zeer klein en snel basismodel voor semantische zoektoepassingen. Handig als snelheid en eenvoud het belangrijkst zijn. |
| `nomic-embed-text-v1.5` | Open lokale embeddingoptie die het waard is te testen voor setups met langere context of draagbaarheid. |

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

Dan krijgt elk stuk een embedding:

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

## 6. Vectors opslaan in Qdrant lokale modus

Nu maken we een in-memory Qdrant-collectie en voegen we de stukken toe met payload-metadata.

> [!NOTE]
> In de tutorial van 2023 gebruikte ik FAISS omdat het een eenvoudige en populaire manier was om lokale vector-similariteitszoektocht met LangChain te demonstreren. FAISS is nog steeds nuttig voor snelle lokale experimenten. In deze 2026-versie gebruik ik Qdrant omdat ik wil dat de tutorial dichter bij een productie-RAG-systeem aanleunt. Qdrant laat me vectors opslaan samen met payload-metadata zoals bronbestand, sectiekop, documentversie en toestemmingen. Dat maakt ophalen makkelijker te inspecteren en bereidt het voorbeeld voor op filtering, citaties en toekomstige persistente of servergebaseerde implementaties.

FAISS is geweldig voor het tonen van vector-similarity search. Qdrant is beter voor het tonen van een kleine maar productie-achtige RAG-ophaallaag.

Enkele praktische alternatieven:

| Vectoropslag / zoeklaag | Wanneer ik het zou overwegen |
| --- | --- |
| Qdrant | Lokale prototypes, metadata-filtering, productievriendelijke vectorzoektocht en een simpele Python-workflow. |
| Chroma | Snelle lokale RAG-experimenten en notebooks waar eenvoud het belangrijkst is. |
| FAISS | Lichtgewicht lokale vectorzoektocht wanneer ik alleen similarity search nodig heb en metadata apart kan beheren. |
| Milvus | Grootschalige open-source vectorzoektocht wanneer het team klaar is om een dedicated vectordatabase te beheren. |
| Weaviate | Vectorsearch met schema, metadata, hybride zoektoepassingen en beheerde of zelf-gehoste implementaties. |
| Azure AI Search | Enterprise-RAG op Azure wanneer ik zoekwoordenzoektocht, vectorsearch, hybride retrieval, semantische ranking, filtering, beveiliging en beheerde operaties in één laag wil. |
| PostgreSQL + pgvector | Teams die al PostgreSQL gebruiken en vectorsearch dicht bij applicatiedata willen. |

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

Dan voegen we de punten toe:

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

In mijn uitvoering voegde de collectie 8 vectors in.

Hier begint het RAG-systeem inspecteerbaar te worden. De vectordatabase slaat niet alleen vectors op; hij slaat ook de bewijsttekst en de metadata die nodig zijn voor citaties.

## 7. Kandidatenstukken ophalen

Nu stellen we de vraag en halen we kandidaatstukken op.

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

Op dit punt print ik de opgehaalde stukken voordat ik een antwoord genereer. Dit is belangrijk. Als het ophalen fout is, zal de generatie het probleem alleen verbergen achter vloeiende tekst.

## 8. Voeg een lichte herordening toe

Toen ik het retrievalpad voor het eerst testte, vond vectorsimilariteit gerelateerde beleidsinhoud, maar stond de meest precieze sectie niet altijd bovenaan.

Dus voegde ik een kleine lokale herordening toe. Deze geeft extra gewicht als de vragenwoorden overlappen met de sectiekop en inhoud.

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

Na herordening werd het topresultaat:

```text
school_ai_policy.md / Final Assignments
```

Dat was de verwachte sectie voor de testvraag.

Dit was de meest bruikbare les uit de eerste implementatie. Zelfs in een klein lokaal voorbeeld verbeterde de kwaliteit van retrieval wanneer ik vectorsimilariteit combineerde met een andere signaal.

## 9. Stel een gegrond lokaal antwoord samen

Voor het standaardpad gebruik ik een transparante lokale antwoordcomponist in plaats van een LLM.

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

Dit is niet bedoeld als een definitieve antwoordgenerator. Het is een debuggingtool. Het bewijst dat retrieval, metadata en citaatverbindingen werken voordat modelvariabiliteit wordt toegevoegd.

## 10. Genereer een lokaal antwoord met Ollama en Phi-4-mini

Als het ophalen werkt, kan de notebook alleen de laatste antwoordstap vervangen door Ollama en `phi4-mini:3.8b`.

> [!NOTE]
> Ollama zou alleen de laatste antwoordgeneratiestap moeten vervangen. Document laden, chunking, vectoropslag, ophalen, herordenen en citaatverbindingen blijven hetzelfde.

Eerst bouwt de notebook een bewijsprompt op basis van de opgehaalde stukken:

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

Voor deze tutorial raad ik Microsofts Phi-4-mini familie aan via Ollama als standaard lokale generatieoptie. In Ollama is het model dat ik testte:

```powershell
ollama pull phi4-mini:3.8b
```

U kunt snel controleren of het model beschikbaar is:

```powershell
ollama list
```

Daarna stelt u deze variabelen in:

```powershell
Copy-Item .env.example .env
```

Open `.env` en haal de commentaartekens weg bij de Serie 2 Ollama-waarden:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

De notebook laadt `.env` vanuit de root van de repository met `python-dotenv`, en verzendt dan dezelfde bewijsprompt naar Ollama’s lokale `/api/chat` endpoint met streaming uitgeschakeld. Als Ollama niet draait of `SERIES2_OLLAMA_MODEL` ontbreekt, wordt dit pad overgeslagen.

> [!NOTE]
> Op deze machine downloadde `phi4-mini:3.8b` ongeveer 2,49GB aan modelbestanden. Tijdens inference meldde Ollama een geladen modelgrootte van 3,3GB en gebruikte de RTX 3060 Laptop GPU.

Dit geeft de tutorial twee niveaus:

1. CPU-only deterministische antwoordcomponist.
2. Lokale antwoordgeneratie met Ollama en Phi-4-mini.

De retrieval-pijplijn blijft in beide gelijk.

## 11. Verificatie resultaat

Ik heb de notebook lokaal gedraaid op Windows met Python 3.12.6.

Geïnstalleerde pakketten:

| Pakket | Versie |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Notebook-uitvoering:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Uitvoeringsresultaat: geslaagd met `nbclient`
- Documenten geladen: 2
- Aangemaakte stukken: 8
- Qdrant-collectie: `school_policy_local`
- Ingevoegde vectors: 8
- Embeddingmodel: `BAAI/bge-small-en-v1.5`
- Embeddinggrootte: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Ik zou dit antwoord niet perfect noemen. Het beantwoordt vanuit het juiste bewijs, maar de laatste bronregel is minder precies dan het deterministische citeringsformaat. Dat is nuttig om in de tutorial te laten zien omdat het de volgende engineeringvraag duidelijk maakt: antwoordgeneratie heeft ook evaluatie nodig, niet alleen ophalen.

Het belangrijkste wat ik heb geleerd tijdens het verifiëren, is dat de kwaliteit van het ophalen gecontroleerd moet worden vóór de antwoordgeneratie. Het embeddingresultaat was al nuttig, en de lichtgewicht herorderaar zorgde ervoor dat de verwachte beleidssectie betrouwbaar als eerste verscheen. Dat is precies het soort klein systeemgedrag dat ik met de tutorial wil blootleggen in plaats van verbergen.

## 12. Wat volgt hierna

De volgende verbetering is om deze lokale opzet te vergelijken met een beheerde Azure-versie van hetzelfde schoolbeleid-assistent-scenario. Het scenario vasthouden zou het gemakkelijker moeten maken om de afwegingen te zien: complexiteit van de opzet, retrieval-controles, identiteitsintegratie, operationeel eigenaarschap en kosten.

## 13. Referenties

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub repository](https://github.com/qdrant/qdrant-client)
- [FastEmbed ondersteunde modellen](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embeddings gids](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 modelkaart](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 modelkaart](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 modelkaart](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini modelpagina](https://ollama.com/library/phi4-mini)
- [Ollama Windows documentatie](https://docs.ollama.com/windows)
- [Ollama API streaming documentatie](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct modelkaart](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph overzicht](https://docs.langchain.com/oss/python/langgraph)
- [Introductie tot RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Vorige: [Serie 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->