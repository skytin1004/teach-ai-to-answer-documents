# Insegna all’IA a Rispondere alle Domande Basandosi sui Tuoi Documenti
## Serie 2: Costruire un Sistema RAG Open-Source Locale da Zero

![Pipeline del tutorial RAG open-source locale](../../../assets/images/series-2-local-rag.svg)

> Questo articolo trasforma la discussione sull’architettura della Serie 1 in un tutorial RAG locale eseguibile. L’obiettivo è costruire prima l’intero flusso di lavoro con dati di esempio, senza account cloud e senza segreti, quindi utilizzare quella base funzionante per prendere decisioni architetturali migliori in seguito.

Il sistema che costruiremo è un piccolo assistente per le politiche scolastiche. Uso due documenti Markdown locali come base di conoscenza, quindi percorro l’intera pipeline RAG: suddivisione in chunk, embedding locali, archiviazione vettoriale Qdrant, recupero, riordinamento, composizione della risposta con consapevolezza della fonte e generazione locale opzionale con Ollama e Phi-4-mini.

Navigazione della serie: [Home del repository](../README.md) | Precedente: [Serie 1 - RAG, Azure vs alternative open-source e quando ha senso il fine-tuning](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Requisiti: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Questo è il miglior punto di partenza se vuoi capire la pipeline RAG prima di creare risorse cloud. Il percorso predefinito funziona localmente con embedding cpu-friendly e senza segreti.

## 1. Cosa Stiamo Costruendo

Nel tutorial del 2023, sono partito da Azure perché l’obiettivo era mostrare come Azure AI Search e Azure OpenAI potessero rispondere a domande da documenti PDF.

Per questa serie 2026, voglio partire da un livello più basso.

Prima di usare servizi gestiti, voglio costruire un piccolo sistema RAG localmente e rendere ogni passaggio visibile: caricamento documenti, suddivisione in chunk, archiviazione vettoriale, recupero delle evidenze, riordinamento risultati e restituzione di una risposta consapevole della fonte.

Lo scenario di esempio è un assistente per le politiche scolastiche. L’utente chiede:

```text
Can I use generative AI for my final assignment?
```

Il sistema non dovrebbe rispondere dalla memoria generale del modello. Deve recuperare la sezione pertinente della politica e rispondere basandosi su quelle evidenze.

La versione completa eseguibile è in [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Il codice qui sotto mostra i passaggi principali così l’articolo può essere letto come un tutorial.

## 2. Installa le Dipendenze Locali

Crea un ambiente virtuale e installa i requisiti della Serie 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

La prima versione usa la modalità locale Qdrant e FastEmbed. Il client Python di Qdrant supporta una modalità locale in memoria con `QdrantClient(":memory:")`, utile per tutorial locali e verifiche in stile CI. FastEmbed ci offre un modello embedding locale reale senza richiedere una chiave API cloud.

Il file dei requisiti include anche `python-dotenv` perché il notebook può opzionalmente leggere un nome modello Ollama da `.env`. Nessuna chiave API Azure OpenAI o OpenAI è richiesta per questo tutorial locale.

## 3. Carica i Documenti di Esempio

Il corpus di esempio è intenzionalmente piccolo:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Nel notebook carico tutti i file Markdown da `sample_data/`:

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

Quando ho eseguito il notebook, sono stati caricati 2 documenti. È abbastanza piccolo da ispezionare manualmente, cosa utile quando si costruisce la prima versione di una pipeline RAG.

## 4. Suddivisione basata sui Titoli Markdown

Il passaggio successivo è suddividere i documenti in chunk.

Per questo tutorial uso i titoli Markdown come segnale di struttura. Il titolo del documento proviene da `#`, e ogni chunk di sezione da `##`.

> [!NOTE]
> La suddivisione non è “taglia unica”. In questo tutorial uso i titoli Markdown perché i documenti di esempio hanno una struttura chiara `#` e `##`. Per PDF, documenti Word, slide, ticket o pagine web, una strategia migliore può usare confini di pagina, informazioni di layout, sezioni semantiche, limiti di token, tabelle o metadati. Il punto importante è scegliere una strategia di chunking che preservi significato e tracciabilità della fonte per i tuoi documenti.

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

Poi la applico a ogni documento:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Questo ha creato 8 chunk nella mia esecuzione locale.

Quello che mi è piaciuto di questo passaggio è che i metadati sono già utili. Ogni chunk conosce la sua `source`, `sectionHeading`, `documentVersion` e il placeholder `permissions`. Anche in un piccolo tutorial, questo rende più facile ragionare sulle citazioni e sul recupero consapevole delle autorizzazioni.

## 5. Crea Embedding Locali

Per la prima versione pubblica uso `BAAI/bge-small-en-v1.5` attraverso FastEmbed.

Questo mantiene il tutorial locale e cpu-friendly, ma usa comunque un modello embedding reale invece di una funzione vettoriale segnaposto. La prima esecuzione scarica i pesi del modello. Successivamente il notebook può riusare la cache locale.

> [!NOTE]
> Uso `BAAI/bge-small-en-v1.5` perché è un modello embedding leggero per l’inglese che funziona bene con FastEmbed e Qdrant per un tutorial locale. Crea vettori a 384 dimensioni, che mantiene l’esempio veloce ed economico da eseguire localmente. Non è l’unica scelta valida. Nel 2023 molti tutorial usavano modelli embedding ospitati come `text-embedding-ada-002`. Oggi opzioni ospitate più nuove come OpenAI `text-embedding-3-small` e `text-embedding-3-large`, e opzioni open-source come BGE, E5, MiniLM, Nomic Embed e modelli multilingue come `BAAI/bge-m3` sono tutte scelte ragionevoli a seconda del carico di lavoro. In produzione il modello embedding giusto va scelto valutando il recupero sui propri documenti.

Alcune alternative pratiche:

| Famiglia di modelli | Quando la considererei |
| --- | --- |
| `text-embedding-ada-002` | Baseline ospitata più vecchia apparsa in molti tutorial dell’era 2023. Oggi non la sceglierei come default per un nuovo tutorial. |
| `text-embedding-3-small` | Default moderno ospitato quando voglio un buon bilanciamento costo/prestazioni e non necessito embedding solo locali. |
| `text-embedding-3-large` | Opzione ospitata quando la qualità del recupero conta più della dimensione vettoriale o costo embedding. |
| `BAAI/bge-small-en-v1.5` | Baseline locale leggero per l’inglese, utile in tutorial, prototipi ed esperimenti cpu-friendly. |
| `BAAI/bge-base-en-v1.5` o `BAAI/bge-large-en-v1.5` | Modelli locali più grandi per l’inglese quando voglio migliore qualità di recupero e posso permettermi più calcolo. |
| `BAAI/bge-m3` | Recupero multilingue o con contesto più lungo, specialmente quando i documenti non sono solo in inglese. |
| `sentence-transformers/all-MiniLM-L6-v2` | Baseline per ricerca semantica molto piccola e veloce. Utile quando velocità e semplicità sono prioritari. |
| `nomic-embed-text-v1.5` | Opzione embedding locale open-source da testare per contesti più lunghi o set up focalizzati sulla portabilità. |

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

Poi ogni chunk ottiene un embedding:

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

## 6. Archivia i Vettori in Modalità Locale Qdrant

Ora creiamo una collection Qdrant in memoria e inseriamo i chunk con i metadati del payload.

> [!NOTE]
> Nel tutorial 2023 usavo FAISS perché era un modo semplice e popolare per dimostrare la ricerca vettoriale locale di similarità con LangChain. FAISS è ancora utile per esperimenti locali veloci. In questa versione 2026 uso Qdrant perché voglio che il tutorial si senta più vicino a un sistema RAG di produzione. Qdrant permette di archiviare vettori assieme a metadati di payload come file sorgente, titolo sezione, versione documento e permessi. Questo rende il recupero più facile da ispezionare e prepara l’esempio per filtraggio, citazioni e futuri deployment persistenti o server-based.

FAISS va bene per mostrare la ricerca vettoriale di similarità. Qdrant è meglio per mostrare un piccolo strato di retrieval RAG con forma da produzione.

Alcune alternative pratiche:

| Archivio vettori / livello di ricerca | Quando la considererei |
| --- | --- |
| Qdrant | Prototipi locali, filtraggio metadati, ricerca vettoriale adatta alla produzione e workflow Python semplice. |
| Chroma | Esperimenti locali RAG veloci e notebook dove la semplicità è prioritaria. |
| FAISS | Ricerca vettoriale locale leggera quando serve solo search di similarità e posso gestire metadati separatamente. |
| Milvus | Ricerca vettoriale open-source su larga scala quando il team è pronto a gestire un DB vettoriale dedicato. |
| Weaviate | Ricerca vettoriale con schema, metadati, ricerca ibrida e opzioni di deployment gestito o self-hosted. |
| Azure AI Search | RAG enterprise su Azure quando voglio ricerca a parole chiave, ricerca vettoriale, retrieval ibrido, ranking semantico, filtraggio, sicurezza e operazioni gestite in un solo livello di ricerca. |
| PostgreSQL + pgvector | Team già su PostgreSQL che vogliono ricerca vettoriale vicina ai dati applicativi. |

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

Poi inseriamo i punti:

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

Nella mia esecuzione, la collezione ha inserito 8 vettori.

Qui il sistema RAG inizia a diventare ispezionabile. Il database vettoriale non memorizza solo vettori; memorizza il testo delle evidenze e i metadati necessari per le citazioni.

## 7. Recupera i Chunk Candidati

Ora facciamo la domanda e recuperiamo i chunk candidati.

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

A questo punto stampo i chunk recuperati prima di generare una risposta. Questo è importante. Se il recupero è sbagliato, la generazione nasconderà solo il problema dietro un testo fluente.

## 8. Aggiungi un Riordinatore Leggero

Quando ho testato per la prima volta il percorso di recupero, la sola similarità vettoriale trovava contenuti policy correlati, ma la sezione più precisa non era sempre in cima.

Così ho aggiunto un piccolo riordinatore locale. Dà peso extra quando i termini della domanda si sovrappongono con il titolo della sezione e il contenuto.

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

Dopo il riordinamento, il risultato in cima è diventato:

```text
school_ai_policy.md / Final Assignments
```

Quella era la sezione prevista per la domanda di test.

Questa è stata la lezione più utile dalla prima implementazione. Anche in un piccolo esempio locale, la qualità del recupero migliorava combinando similarità vettoriale con un altro segnale.

## 9. Componi una Risposta Locale Fondamentata

Per il percorso predefinito uso un compositore di risposte locale trasparente invece di un LLM.

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

Questo non è pensato come generatore finale di risposte. È uno strumento di debug. Dimostra che recupero, metadati e wiring di citazioni funzionano prima di aggiungere la variabilità del modello.

## 10. Genera una Risposta Locale con Ollama e Phi-4-mini

Una volta che il recupero funziona, il notebook può sostituire solo il passaggio finale di risposta con Ollama e `phi4-mini:3.8b`.

> [!NOTE]
> Ollama dovrebbe sostituire solo il passaggio finale di generazione della risposta. Caricamento documenti, chunking, archiviazione vettori, recupero, riordinamento e wiring delle citazioni dovrebbero rimanere gli stessi.

Prima, il notebook costruisce un prompt di evidenze dai chunk recuperati:

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

Per questo tutorial, raccomando la famiglia Phi-4-mini di Microsoft via Ollama come opzione di generazione locale predefinita. In Ollama il nome modello che ho testato è:

```powershell
ollama pull phi4-mini:3.8b
```

Puoi verificare rapidamente che il modello sia disponibile:

```powershell
ollama list
```

Poi imposta queste variabili:

```powershell
Copy-Item .env.example .env
```

Apri `.env` e decommenta i valori Ollama della Serie 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Il notebook carica `.env` dalla root del repository con `python-dotenv`, quindi invia lo stesso prompt delle evidenze all’endpoint locale `/api/chat` di Ollama con lo streaming disabilitato. Se Ollama non è in esecuzione o `SERIES2_OLLAMA_MODEL` manca, questo passaggio viene saltato.

> [!NOTE]
> Su questa macchina, `phi4-mini:3.8b` ha scaricato circa 2.49GB di file modello. Durante l’inferenza, Ollama ha riportato una dimensione modello caricata di 3.3GB e ha usato la GPU RTX 3060 Laptop.

Questo dà al tutorial due livelli:

1. Compositore di risposte deterministico solo CPU.
2. Generazione locale di risposte con Ollama e Phi-4-mini.

La pipeline di recupero rimane la stessa in entrambi.

## 11. Risultato della Verifica

Ho eseguito il notebook localmente su Windows con Python 3.12.6.

Pacchetti installati:

| Pacchetto | Versione |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Esecuzione notebook:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Esito esecuzione: superato con `nbclient`
- Documenti caricati: 2
- Chunk creati: 8
- Collezione Qdrant: `school_policy_local`
- Vettori inseriti: 8
- Modello embedding: `BAAI/bge-small-en-v1.5`
- Dimensione embedding: 384
- Domanda di recupero: "Posso usare l'IA generativa per il mio compito finale?"
- Percorso di riordino: riordino lessicale locale leggero
- Fonte primaria recuperata dopo il riordino: `school_ai_policy.md`
- Sezione principale recuperata dopo il riordino: `Final Assignments`
- Percorso risposta predefinito: compositore di risposte trasparente locale
- Percorso generazione Ollama: completato con `phi4-mini:3.8b`
- Dimensione file modello Ollama: 2,49GB su disco
- Dimensione modello Ollama caricato: 3,3GB riportati da `ollama ps`
- Scarico GPU: 100% GPU riportato da `ollama ps`
- Memoria GPU osservata dopo la generazione: circa 3,5GB di 6GB usati su RTX 3060 Laptop GPU
- Esecuzione notebook con modello FastEmbed memorizzato nella cache e generazione Ollama abilitata: superata in circa 34 secondi tramite lo script di verifica

La risposta generata da Ollama è stata:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Non definirei questa risposta perfetta. Risponde dalla fonte corretta, ma la riga finale della fonte è meno precisa rispetto al formato di citazione deterministico. Questo è utile mostrarlo nel tutorial perché rende ovvia la prossima domanda di ingegneria: anche la generazione della risposta necessita di una valutazione, non solo il recupero.

La cosa principale che ho imparato durante la verifica è che la qualità del recupero dovrebbe essere controllata prima della generazione della risposta. Il risultato dell'embedding era già utile, e il riordino leggero ha fatto emergere in modo affidabile la sezione della politica prevista come prima. Questo è esattamente il tipo di comportamento di sistema piccolo che voglio che il tutorial esponga anziché nascondere.

## 12. Cosa Viene Dopo

Il prossimo miglioramento è confrontare questa configurazione locale con una versione gestita su Azure dello stesso scenario di assistente politico scolastico. Mantenere fisso lo scenario dovrebbe rendere più evidenti i compromessi: complessità di configurazione, controlli di recupero, integrazione dell'identità, proprietà operativa e costi.

## 13. Riferimenti

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client repository GitHub](https://github.com/qdrant/qdrant-client)
- [Modelli supportati da FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Guida alle embeddings OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Scheda modello BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Scheda modello BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Scheda modello sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Pagina modello Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Documentazione Ollama Windows](https://docs.ollama.com/windows)
- [Documentazione streaming API Ollama](https://docs.ollama.com/api/streaming)
- [Scheda modello Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Panoramica LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Introduzione a RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Precedente: [Serie 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->