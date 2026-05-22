# Lær AI å svare på spørsmål basert på dine dokumenter
## Serie 2: Bygg et lokalt åpne-kildekode RAG-system fra start til slutt

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Denne artikkelen gjør Series 1 sin arkitekturdiskusjon om til en kjørbar lokal RAG-opplæring. Målet er å bygge hele arbeidsflyten først med eksempeldata, uten skylagringskonto eller hemmeligheter, og så bruke denne fungerende basisen til å ta bedre arkitekturvalg senere.

Systemet vi skal bygge er en liten skolepolitikkassistent. Jeg bruker to lokale Markdown-dokumenter som kunnskapsbase, og går deretter gjennom hele RAG-pipelinen: oppdeling i deler, lokale embeddings, Qdrant vektorlagring, henting, omrangering, kildebevisst svarkomposisjon og valgfri lokal generering med Ollama og Phi-4-mini.

Serienavigasjon: [Repository hjem](../README.md) | Forrige: [Serie 1 - RAG, Azure vs åpne-kildekodealternativer, og når finjustering gir mening](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Krav: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Dette er det beste utgangspunktet hvis du vil forstå RAG-pipelinen før du oppretter skytjenester. Standardscenariet kjører lokalt med CPU-vennlige embeddings og uten hemmeligheter.

## 1. Hva vi bygger

I 2023-opplæringen startet jeg med Azure fordi målet var å vise hvordan Azure AI Search og Azure OpenAI kunne svare på spørsmål ut fra PDF-dokumenter.

For denne 2026-serien ønsker jeg å starte et lag lavere.

Før jeg bruker administrerte tjenester, ønsker jeg å bygge et lite RAG-system lokalt og gjøre hvert steg synlig: laste dokumenter, dele opp tekst, lagre vektorer, hente bevis, omrangere resultater og returnere et kildebevisst svar.

Eksempel-scenarioet er en skolepolitikkassistent. Brukeren spør:

```text
Can I use generative AI for my final assignment?
```

Systemet skal ikke svare fra generell modellhukommelse. Det skal hente relevant policy-seksjon og svare basert på det beviset.

Den fullstendige kjørbare versjonen er i [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Koden nedenfor viser hovedstegene slik at artikkelen kan leses som en opplæring.

## 2. Installer lokale avhengigheter

Lag et virtuelt miljø og installer kravene for Serie 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Den første versjonen bruker Qdrant i lokal modus og FastEmbed. Qdrants Python-klient støtter en minnebasert lokal modus med `QdrantClient(":memory:")`, som er nyttig for lokale opplæringer og CI-lignende verifisering. FastEmbed gir oss en ekte lokal embedding-modell uten krav om sky-API-nøkkel.

Kravfilen inkluderer også `python-dotenv` fordi notebooken kan valgfritt lese modellnavn for Ollama fra `.env`. Ingen Azure OpenAI- eller OpenAI-API-nøkkel kreves for denne lokale opplæringen.

## 3. Last inn eksempel-dokumentene

Eksempelkorpuset er med vilje lite:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

I notebooken laster jeg alle Markdown-filer fra `sample_data/`:

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

Da jeg kjørte notebooken, lastet den inn 2 dokumenter. Det er lite nok til å inspisere manuelt, noe som er nyttig ved bygging av første RAG-pipeline-versjon.

## 4. Del opp etter Markdown-overskrifter

Neste steg er å splitte dokumentene opp i biter.

I denne opplæringen bruker jeg Markdown-overskrifter som strukturindikator. Dokumenttittelen kommer fra `#`, og hver seksjon fra `##`.

> [!NOTE]
> Oppdeling er ikke en løsning for alle tilfeller. I denne opplæringen bruker jeg Markdown-overskrifter fordi eksempel-dokumentene har tydelig `#` og `##` struktur. For PDF-filer, Word-dokumenter, lysbilder, tickets eller nettsider kan en bedre strategi bruke sideskift, layoutinformasjon, semantiske seksjoner, tokenbegrensninger, tabeller eller metadata. Det viktige er å velge en oppdelingsstrategi som bevarer mening og sporbarhet for dokumentene dine.

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

Deretter bruker jeg den på hvert dokument:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Dette skapte 8 biter i min lokale kjøring.

Det jeg likte med dette steget er at metadata allerede er nyttige. Hver bit kjenner sin `source`, `sectionHeading`, `documentVersion` og plassholder for `permissions`. Selv i en liten opplæring gjør dette sitater og senere tilgangsrettighetsbevisst henting lettere å forstå.

## 5. Lag lokale embeddings

For første offentlige versjon bruker jeg `BAAI/bge-small-en-v1.5` via FastEmbed.

Dette holder opplæringen lokal og CPU-vennlig, men bruker fortsatt en ekte embeddingmodell i stedet for en plassholder-vektorfunksjon. Første kjøring laster ned modellvektene. Deretter kan notebooken gjenbruke lokal buffer.

> [!NOTE]
> Jeg bruker `BAAI/bge-small-en-v1.5` fordi det er en lett engelsk embeddingmodell som fungerer godt med FastEmbed og Qdrant for lokal opplæring. Den lager 384-dimensjonale vektorer, som gjør eksempelet raskt og rimelig å kjøre lokalt. Dette er ikke det eneste gode valget. I 2023 brukte mange opplæringer hostede embeddingmodeller som `text-embedding-ada-002`. I dag er nyere hostede alternativer som OpenAI `text-embedding-3-small` og `text-embedding-3-large`, og åpne alternativer som BGE, E5, MiniLM, Nomic Embed og flerspråklige modeller som `BAAI/bge-m3` alle rimelige valg avhengig av arbeidsmengde. I produksjon bør riktig embeddingmodell velges gjennom vurdering av gjenfinning på dine egne dokumenter.

Noen praktiske alternativer:

| Modell-familie | Når jeg vil vurdere den |
| --- | --- |
| `text-embedding-ada-002` | Eldre hostet baseline som dukket opp i mange 2023-opplæringer. Ville ikke valgt som standard i en ny opplæring i dag. |
| `text-embedding-3-small` | Moderne hostet standard når jeg ønsker god balanse mellom kostnad og ytelse og ikke trenger kun lokal embedding. |
| `text-embedding-3-large` | Hostet alternativ når gjenfinningskvalitet er viktigere enn vektor-størrelse eller embedding-kostnad. |
| `BAAI/bge-small-en-v1.5` | Lett lokal engelsk baseline for opplæringer, prototyper og CPU-vennlige eksperimenter. |
| `BAAI/bge-base-en-v1.5` eller `BAAI/bge-large-en-v1.5` | Større lokale engelske modeller når jeg ønsker bedre gjenfinningskvalitet og kan bruke mer regnekraft. |
| `BAAI/bge-m3` | Flerspråklig eller gjenfinning med lengre kontekst, spesielt når dokumentene ikke bare er på engelsk. |
| `sentence-transformers/all-MiniLM-L6-v2` | Veldig liten og rask semantisk søk-baseline. Nyttig når hastighet og enkelhet er viktigst. |
| `nomic-embed-text-v1.5` | Åpent lokalt embedding-alternativ verdt å teste for lengre kontekster eller oppsett fokusert på portabilitet. |

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

Deretter får hver bit en embedding:

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

## 6. Lagre vektorer i Qdrant lokal modus

Nå lager vi en minnebasert Qdrant-samling og setter inn biter med metadata som laste.

> [!NOTE]
> I 2023-opplæringen brukte jeg FAISS fordi det var en enkel og populær måte å demonstrere lokal vektorlignbarhetssøk med LangChain. FAISS er fortsatt nyttig for raske lokale eksperimenter. I denne 2026-versjonen bruker jeg Qdrant fordi jeg ønsker at opplæringen skal føles nærmere et produksjons-RAG-system. Qdrant lar meg lagre vektorer sammen med metadata som kildefil, seksjonsoverskrift, dokumentversjon og rettigheter. Det gjør hentingen lettere å inspisere og forbereder eksempelet for filtrering, sitater og fremtidig vedvarende eller serverbasert distribusjon.

FAISS er glimrende for å vise vektorlignbarhetssøk. Qdrant er bedre for å vise et lite men produksjonsformet RAG-hentingslag.

Noen praktiske alternativer:

| Vektorlagring / søkelag | Når jeg vil vurdere det |
| --- | --- |
| Qdrant | Lokale prototyper, metadatfiltrering, produksjonsvennlig vektorsøk og enkel Python-arbeidsflyt. |
| Chroma | Raske lokale RAG-eksperimenter og notebooks der enkelhet er viktigst. |
| FAISS | Lettvekts lokal vektorsøk når jeg bare trenger likhetssøk og kan håndtere metadata separat. |
| Milvus | Større åpen-kildekode vektorsøk når teamet er klart for å drifte en dedikert vektordatabase. |
| Weaviate | Vektorsøk med skjema, metadata, hybridsøk og administrerte eller selvhostede distribusjonsalternativer. |
| Azure AI Search | Enterprise-RAG på Azure når jeg ønsker nøkkelordssøk, vektorsøk, hybrid gjenfinning, semantisk rangering, filtrering, sikkerhet og administrerte operasjoner i ett søkelag. |
| PostgreSQL + pgvector | Team som allerede bruker PostgreSQL og ønsker vektorsøk nær applikasjonsdata. |

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

Sett deretter inn punktene:

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

I min kjøring satte samlingen inn 8 vektorer.

Her begynner RAG-systemet å bli inspiserbart. Vektordatabasen lagrer ikke bare vektorer; den lagrer bevistekst og metadata som trengs for sitater.

## 7. Hent kandidatdeler

Nå stiller vi spørsmålet og henter kandidatdeler.

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

På dette tidspunktet skriver jeg ut de hentede delene før jeg genererer svar. Dette er viktig. Hvis hentingen er feil, vil genereringen bare skjule problemet bak flytende tekst.

## 8. Legg til en lettvekts omrangering

Da jeg først testet hentesporet, fant vektorlignbarhet alene relatert policy-innhold, men den mest presise seksjonen var ikke alltid øverst.

Så la jeg til en liten lokal omrangering. Den gir ekstra vekt når spørsmålstermene overlapper med seksjonsoverskriften og innholdet.

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

Etter omrangering ble toppresultatet:

```text
school_ai_policy.md / Final Assignments
```

Det var den forventede seksjonen for testspørsmålet.

Dette var den mest nyttige lærdomen fra første implementasjon. Selv i et lite lokalt eksempel forbedret hentekvaliteten seg når jeg kombinerte vektorlignbarhet med et annet signal.

## 9. Komponer et godt fundert lokalt svar

For standardløypen bruker jeg en transparent lokal svar-komponist i stedet for en LLM.

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

Dette er ikke ment som en sluttprodukt-svar-generator. Det er et feilsettingsverktøy. Det beviser at henting, metadata og siteringer fungerer før modellvariasjon legges til.

## 10. Generer et lokalt svar med Ollama og Phi-4-mini

Når henting fungerer, kan notebooken erstatte bare det siste svaretappunktet med Ollama og `phi4-mini:3.8b`.

> [!NOTE]
> Ollama bør kun erstatte den siste svargenereringsfasen. Dokumentlasting, oppdeling, vektorlagring, henting, omrangering og siteringskobling bør forbli uendret.

Først bygger notebooken en bevis-prompt fra hentede biter:

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

For denne opplæringen anbefaler jeg Microsofts Phi-4-mini-familie via Ollama som standard lokalt genereringsvalg. Modellen jeg testet i Ollama er:

```powershell
ollama pull phi4-mini:3.8b
```

Du kan raskt sjekke at modellen er tilgjengelig:

```powershell
ollama list
```

Deretter setter du disse variablene:

```powershell
Copy-Item .env.example .env
```

Åpne `.env` og fjern kommentaren fra Serie 2 Ollama-verdier:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebooken laster `.env` fra repository-roten med `python-dotenv`, og sender deretter samme bevis-prompt til Ollamas lokale `/api/chat` endepunkt med streaming deaktivert. Hvis Ollama ikke kjører eller `SERIES2_OLLAMA_MODEL` mangler, blir denne løypen hoppet over.

> [!NOTE]
> På denne maskinen lastet `phi4-mini:3.8b` ned cirka 2,49 GB med modellfiler. Under inferens rapporterte Ollama 3,3 GB lastet modellstørrelse og brukte RTX 3060 Laptop GPU.

Dette gir opplæringen to nivåer:

1. Kun CPU deterministisk svarkomponist.
2. Lokal svar-generering med Ollama og Phi-4-mini.

Hentepipelinen forblir den samme i begge.

## 11. Verifiseringsresultat

Jeg kjørte notebooken lokalt på Windows med Python 3.12.6.

Installerte pakker:

| Pakke | Versjon |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Notebook-kjøring:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Kjøringsresultat: bestått med `nbclient`
- Dokumenter lastet: 2
- Deler opprettet: 8
- Qdrant-samling: `school_policy_local`
- Vektorer satt inn: 8
- Embedding-modell: `BAAI/bge-small-en-v1.5`
- Embedding-størrelse: 384
- Hentingsspørsmål: "Kan jeg bruke generativ AI for min avsluttende oppgave?"
- Omrangeringsvei: lettvekts lokal leksikalsk omrangering
- Topp hentet kilde etter omrangering: `school_ai_policy.md`
- Topp hentet seksjon etter omrangering: `Final Assignments`
- Standard svarvei: lokal gjennomsiktig svarkomponist
- Ollama genereringsvei: fullført med `phi4-mini:3.8b`
- Ollama modelfilstørrelse: 2,49GB på disk
- Ollama lastet modellstørrelse: 3,3GB rapportert av `ollama ps`
- GPU avlastning: 100% GPU rapportert av `ollama ps`
- GPU-minne observert etter generering: omtrent 3,5GB av 6GB brukt på RTX 3060 Laptop GPU
- Notebook-eksekvering med bufret FastEmbed-modell og Ollama-generering aktivert: bestått på omtrent 34 sekunder gjennom verifiseringsskriptet

Det Ollama-genererte svaret var:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Jeg vil ikke kalle dette svaret perfekt. Det svarer fra riktig bevis, men den siste kildelinjen er mindre presis enn det deterministiske sitatformatet. Det er nyttig å vise i veiledningen fordi det gjør det neste ingeniørspørsmålet åpenbart: svar-generering trenger også evaluering, ikke bare henting.

Det viktigste jeg lærte mens jeg verifiserte dette, er at hentekvalitet bør sjekkes før svar-generering. Innebyggingsresultatet var allerede nyttig, og den lettvekts omrangereren fikk den forventede policyseksjonen til å vises først pålitelig. Det er akkurat den typen små systemoppførsler jeg ønsker at veiledningen skal avdekke i stedet for å skjule.

## 12. Hva Kommer Neste

Den neste forbedringen er å sammenligne denne lokale oppsettet med en administrert Azure-versjon av samme skolepolicy assistentscenario. Å holde scenariet fast bør gjøre avveiningene enklere å se: oppsettskompleksitet, hentekontroller, identitetsintegrasjon, operasjonelt eierskap og kostnad.

## 13. Referanser

- [Qdrant Python klient kjappstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant klient GitHub-repositorium](https://github.com/qdrant/qdrant-client)
- [FastEmbed støttede modeller](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 modellkort](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 modellkort](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 modellkort](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini modellside](https://ollama.com/library/phi4-mini)
- [Ollama Windows dokumentasjon](https://docs.ollama.com/windows)
- [Ollama API streaming dokumentasjon](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct modellkort](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph oversikt](https://docs.langchain.com/oss/python/langgraph)
- [Introduksjon til RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Forrige: [Serie 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->