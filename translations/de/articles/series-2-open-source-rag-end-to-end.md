# Bringen Sie KI bei, Fragen basierend auf Ihren Dokumenten zu beantworten
## Serie 2: Aufbau eines lokalen Open-Source-RAG-Systems von Anfang bis Ende

![Lokaler Open-Source-RAG-Tutorial-Pipeline](../../../assets/images/series-2-local-rag.svg)

> Dieser Artikel verwandelt die Architektur-Diskussion aus Serie 1 in ein ausführbares lokales RAG-Tutorial. Ziel ist es, zuerst den gesamten Workflow mit Beispieldaten, ohne Cloud-Konto und ohne Geheimnisse aufzubauen und dann diese funktionierende Basis zu nutzen, um später bessere Architekturentscheidungen zu treffen.

Das System, das wir aufbauen werden, ist ein kleiner Schulpolitik-Assistent. Ich nutze zwei lokale Markdown-Dokumente als Wissensbasis und führe dann die komplette RAG-Pipeline durch: Chunking, lokale Embeddings, Qdrant Vektor-Speicherung, Retrieval, Reranking, quellenbewusste Antwortkomposition und optional lokale Generierung mit Ollama und Phi-4-mini.

Serien-Navigation: [Repository-Startseite](../README.md) | Vorherige: [Serie 1 – RAG, Azure vs Open-Source-Alternativen und wann Fine-Tuning Sinn macht](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Anforderungen: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Dies ist der beste Startpunkt, wenn Sie die RAG-Pipeline verstehen möchten, bevor Sie Cloud-Ressourcen einrichten. Der Standardpfad läuft lokal mit CPU-freundlichen Embeddings und ohne Geheimnisse.

## 1. Was wir bauen

Im Tutorial von 2023 habe ich mit Azure begonnen, weil das Ziel war zu zeigen, wie Azure AI Search und Azure OpenAI Fragen aus PDF-Dokumenten beantworten können.

Für diese Serie 2026 möchte ich eine Ebene tiefer starten.

Bevor ich verwaltete Dienste nutze, möchte ich ein kleines RAG-System lokal aufbauen und jeden Schritt sichtbar machen: Dokumente laden, Text chunking, Vektoren speichern, Beweise abrufen, Ergebnisse neu bewerten und quellenbewusste Antworten zurückgeben.

Das Beispiel-Szenario ist ein Schulpolitik-Assistent. Der Nutzer fragt:

```text
Can I use generative AI for my final assignment?
```

Das System soll nicht aus dem allgemeinen Modellgedächtnis antworten. Es soll den relevanten Politikabschnitt abrufen und darauf basierend antworten.

Die vollständige ausführbare Version ist in [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Der Code unten zeigt die Hauptschritte, sodass der Artikel als Tutorial gelesen werden kann.

## 2. Installieren der lokalen Abhängigkeiten

Erstellen Sie eine virtuelle Umgebung und installieren Sie die Anforderungen der Serie 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Die erste Version nutzt Qdrant im lokalen Modus und FastEmbed. Der Qdrant-Python-Client unterstützt einen In-Memory-Lokalmode mit `QdrantClient(":memory:")`, welcher nützlich für lokale Tutorials und CI-ähnliche Überprüfungen ist. FastEmbed gibt uns ein echtes lokales Embedding-Modell ohne Cloud-API-Schlüssel.

Die Requirements-Datei enthält auch `python-dotenv`, da das Notebook optional einen Ollama-Modellnamen aus `.env` lesen kann. Für dieses lokale Tutorial wird kein Azure OpenAI- oder OpenAI API-Schlüssel benötigt.

## 3. Laden der Beispieldokumente

Das Beispielkorpus ist absichtlich klein:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Im Notebook lade ich alle Markdown-Dateien aus `sample_data/`:

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

Als ich das Notebook ausführte, wurden 2 Dokumente geladen. Das ist klein genug, um manuell inspiziert zu werden, was beim Bau der ersten Version einer RAG-Pipeline nützlich ist.

## 4. Chunking nach Markdown-Überschriften

Der nächste Schritt ist, Dokumente in Chunks zu unterteilen.

Für dieses Tutorial nutze ich Markdown-Überschriften als Struktur-Signal. Der Dokumenttitel kommt von `#`, und jeder Abschnitts-Chunk von `##`.

> [!NOTE]
> Chunking ist nicht universell. In diesem Tutorial nutze ich Markdown-Überschriften, da die Beispieldokumente klare `#`- und `##`-Strukturen haben. Für PDFs, Word-Dokumente, Folien, Tickets oder Webseiten kann eine bessere Strategie Seitenbegrenzungen, Layout-Informationen, semantische Abschnitte, Token-Limits, Tabellen oder Metadaten verwenden. Wichtig ist, eine Chunking-Strategie zu wählen, welche die Bedeutung und Quellnachverfolgbarkeit der Dokumente bewahrt.

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

Dann wende ich es auf jedes Dokument an:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Das erzeugte in meinem lokalen Lauf 8 Chunks.

Was mir an diesem Schritt gefallen hat, ist, dass die Metadaten bereits nützlich sind. Jeder Chunk kennt seine `source`, `sectionHeading`, `documentVersion` und Platzhalter-`permissions`. Selbst in einem kleinen Tutorial macht das Zitate und später erlaubnisbewusstes Retrieval leichter nachvollziehbar.

## 5. Erstellen lokaler Embeddings

Für die erste öffentliche Version nutze ich `BAAI/bge-small-en-v1.5` über FastEmbed.

Das hält das Tutorial lokal und CPU-freundlich, verwendet aber trotzdem ein echtes Embedding-Modell statt einer Platzhalter-Vektorfunktion. Der erste Lauf lädt die Modellgewichte herunter. Danach kann das Notebook den lokalen Cache wiederverwenden.

> [!NOTE]
> Ich nutze `BAAI/bge-small-en-v1.5`, weil es ein leichtgewichtiges englisches Embedding-Modell ist, das gut mit FastEmbed und Qdrant für lokale Tutorials funktioniert. Es erstellt 384-dimensionale Vektoren, was das Beispiel schnell und kostengünstig laufen lässt. Das ist nicht die einzige gute Wahl. 2023 nutzten viele Tutorials gehostete Embedding-Modelle wie `text-embedding-ada-002`. Heute sind neuere gehostete Optionen wie OpenAI `text-embedding-3-small` und `text-embedding-3-large` sowie Open-Source-Optionen wie BGE, E5, MiniLM, Nomic Embed und mehrsprachige Modelle wie `BAAI/bge-m3` je nach Anwendungsfall gute Optionen. Im Produktivbetrieb sollte das richtige Embedding-Modell anhand der Retrieval-Evaluation auf eigenen Dokumenten gewählt werden.

Einige praktische Alternativen:

| Modellfamilie | Wann ich es in Betracht ziehen würde |
| --- | --- |
| `text-embedding-ada-002` | Älterer gehosteter Standard, der in vielen Tutorials aus der Zeit 2023 genutzt wurde. Ich würde ihn heute nicht als Standard für ein neues Tutorial wählen. |
| `text-embedding-3-small` | Moderner gehosteter Standard, wenn ich ein gutes Kosten-Leistungs-Verhältnis will und keine rein lokalen Embeddings benötige. |
| `text-embedding-3-large` | Gehostete Option, wenn die Retrieval-Qualität wichtiger ist als Vektorgröße oder Embedding-Kosten. |
| `BAAI/bge-small-en-v1.5` | Leichtgewichtige lokale englische Basis für Tutorials, Prototypen und CPU-freundliche Experimente. |
| `BAAI/bge-base-en-v1.5` oder `BAAI/bge-large-en-v1.5` | Größere lokale englische Modelle, wenn ich bessere Retrieval-Qualität möchte und mehr Rechenleistung einsetzen kann. |
| `BAAI/bge-m3` | Mehrsprachiges oder langkontextiges Retrieval, besonders wenn die Dokumente nicht nur Englisch sind. |
| `sentence-transformers/all-MiniLM-L6-v2` | Sehr kleine und schnelle semantische Such-Basis. Nützlich, wenn Geschwindigkeit und Einfachheit am wichtigsten sind. |
| `nomic-embed-text-v1.5` | Offene lokale Embedding-Option, die sich für längeren Kontext oder portabilitätsfokussierte Setups lohnt zu testen. |

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

Dann bekommt jeder Chunk ein Embedding:

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

## 6. Vektoren im Qdrant-Lokalmode speichern

Jetzt erstellen wir eine In-Memory-Qdrant-Sammlung und fügen die Chunks mit Payload-Metadaten ein.

> [!NOTE]
> Im Tutorial 2023 nutzte ich FAISS, weil es ein einfacher und populärer Weg war, lokale Vektorähnlichkeitssuche mit LangChain zu demonstrieren. FAISS ist immer noch nützlich für schnelle lokale Experimente. In dieser Version 2026 nutze ich Qdrant, weil ich will, dass sich das Tutorial näher an einem produktiven RAG-System anfühlt. Qdrant erlaubt, Vektoren zusammen mit Payload-Metadaten wie Quell-Datei, Abschnittsüberschrift, Dokumentversion und Berechtigungen zu speichern. Das macht Retrieval leichter nachvollziehbar und bereitet das Beispiel für Filterung, Zitierungen und zukünftige persistente oder serverbasierte Deployments vor.

FAISS ist großartig, um Vektorähnlichkeitssuche zu zeigen. Qdrant ist besser, um eine kleine, aber produktionsnahe RAG-Retrieval-Schicht zu zeigen.

Einige praktische Alternativen:

| Vektorspeicher / Suchschicht | Wann ich es in Betracht ziehen würde |
| --- | --- |
| Qdrant | Lokale Prototypen, Metadatenfilterung, produktionsfreundliche Vektorsuche und einfacher Python-Workflow. |
| Chroma | Schnelle lokale RAG-Experimente und Notebooks, wenn Einfachheit am wichtigsten ist. |
| FAISS | Leichtgewichtige lokale Vektorsuche, wenn ich nur Ähnlichkeitssuche brauche und Metadaten separat verwalte. |
| Milvus | Größeres Open-Source-Vektorsuchsystem, wenn das Team bereit ist, eine eigene Vektordatenbank zu betreiben. |
| Weaviate | Vektorsuche mit Schema, Metadaten, Hybridsuche sowie verwaltete oder selbstgehostete Deploymentoptionen. |
| Azure AI Search | Enterprise-RAG auf Azure, wenn ich Schlagwortsuche, Vektorsuche, hybrides Retrieval, semantische Rangfolge, Filterung, Sicherheit und verwaltete Operationen in einer Suche-Schicht möchte. |
| PostgreSQL + pgvector | Teams, die bereits PostgreSQL nutzen und Vektorsuche nahe an den Anwendungsdaten wollen. |

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

Dann die Punkte einfügen:

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

In meinem Lauf fügte die Sammlung 8 Vektoren ein.

Hier beginnt das RAG-System, inspezierbar zu werden. Die Vektordatenbank speichert nicht nur Vektoren, sondern auch den Beweistext und die Metadaten, die für Zitierungen nötig sind.

## 7. Kandidaten-Chunks abrufen

Jetzt stellen wir die Frage und rufen Kandidaten-Chunks ab.

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

An diesem Punkt gebe ich die abgerufenen Chunks aus, bevor ich eine Antwort generiere. Das ist wichtig. Wenn das Retrieval falsch ist, verdeckt die Generierung das Problem nur hinter flüssigem Text.

## 8. Leichten Reranker hinzufügen

Als ich den Retrieval-Pfad das erste Mal testete, fand die reine Vektorähnlichkeit verwandte Politik-Inhalte, aber der präziseste Abschnitt stand nicht immer an der Spitze.

Also fügte ich einen kleinen lokalen Reranker hinzu. Er gibt zusätzlich Gewicht, wenn Fragebegriffe mit Abschnittsüberschrift und Inhalt überlappen.

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

Nach dem Reranking wurde das Top-Ergebnis:

```text
school_ai_policy.md / Final Assignments
```

Das war der erwartete Abschnitt für die Testfrage.

Das war die nützlichste Lektion aus der ersten Implementierung. Selbst in einem kleinen lokalen Beispiel verbesserte sich die Retrieval-Qualität, wenn ich Vektorähnlichkeit mit einem weiteren Signal kombinierte.

## 9. Eine fundierte lokale Antwort zusammensetzen

Für den Standardpfad nutze ich einen transparenten lokalen Antwortkomponisten statt eines LLM.

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

Das soll kein finales Produkt-Antwortgenerator sein. Es ist ein Debugging-Tool. Es beweist, dass Retrieval, Metadaten und Zitierverkettung funktionieren, bevor Modellvariabilität hinzukommt.

## 10. Lokale Antwort mit Ollama und Phi-4-mini generieren

Sobald das Retrieval funktioniert, kann das Notebook nur den finalen Antwortschritt mit Ollama und `phi4-mini:3.8b` ersetzen.

> [!NOTE]
> Ollama sollte nur den letzten Antwortgenerierungsschritt ersetzen. Dokumentladen, Chunking, Vektorspeicherung, Retrieval, Reranking und Zitierverkettung bleiben unverändert.

Zuerst baut das Notebook eine Evidenz-Eingabeaufforderung aus den abgerufenen Chunks:

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

Für dieses Tutorial empfehle ich Microsofts Phi-4-mini-Familie durch Ollama als Standard-Lokal-Generierungsoption. Im Ollama habe ich dieses Modell getestet:

```powershell
ollama pull phi4-mini:3.8b
```

Sie können schnell prüfen, ob das Modell verfügbar ist:

```powershell
ollama list
```

Dann diese Variablen setzen:

```powershell
Copy-Item .env.example .env
```

Öffnen Sie `.env` und kommentieren Sie die Series 2 Ollama-Werte aus:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Das Notebook lädt `.env` aus dem Repository-Root mit `python-dotenv` und sendet dann die gleiche Evidenz-Eingabeaufforderung an Ollamas lokalen `/api/chat`-Endpunkt mit deaktiviertem Streaming. Wenn Ollama nicht läuft oder `SERIES2_OLLAMA_MODEL` fehlt, wird dieser Pfad übersprungen.

> [!NOTE]
> Auf diesem Rechner lud `phi4-mini:3.8b` etwa 2,49GB Modell-Dateien herunter. Während der Inferenz meldete Ollama eine geladene Modellgröße von 3,3GB und nutzte die RTX 3060 Laptop GPU.

Das gibt dem Tutorial zwei Ebenen:

1. CPU-only deterministischer Antwortkomponist.
2. Lokale Antwortgenerierung mit Ollama und Phi-4-mini.

Die Retrieval-Pipeline bleibt in beiden gleich.

## 11. Verifikationsergebnis

Ich führte das Notebook lokal unter Windows mit Python 3.12.6 aus.

Installierte Pakete:

| Paket | Version |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Notebook-Ausführung:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Ausführungsergebnis: bestanden mit `nbclient`
- Geladene Dokumente: 2
- Erstellt Chunks: 8
- Qdrant-Sammlung: `school_policy_local`
- Eingefügte Vektoren: 8
- Embedding-Modell: `BAAI/bge-small-en-v1.5`
- Embedding-Größe: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Ich würde diese Antwort nicht als perfekt bezeichnen. Sie basiert auf den richtigen Belegen, aber die abschließende Quellzeile ist weniger präzise als das deterministische Zitierformat. Das ist nützlich, um es im Tutorial zu zeigen, da es die nächste Ingenieursfrage offensichtlich macht: Auch die Antwortgenerierung muss bewertet werden, nicht nur die Suche.

Das Wichtigste, was ich bei der Überprüfung gelernt habe, ist, dass die Qualität der Suche vor der Antwortgenerierung geprüft werden sollte. Das Einbettungsergebnis war bereits nützlich, und der leichte Neu-Rank-Algorithmus ließ den erwarteten Abschnitt der Richtlinie zuverlässig zuerst erscheinen. Genau diese Art von kleinem Systemverhalten soll das Tutorial offenlegen, anstatt es zu verbergen.

## 12. Was Kommt Als Nächstes

Die nächste Verbesserung ist, dieses lokale Setup mit einer verwalteten Azure-Version desselben Szenarios für den Schulrichtlinien-Assistenten zu vergleichen. Das Festhalten am Szenario sollte die Kompromisse leichter sichtbar machen: Einrichtungskomplexität, Suchkontrollen, Identitätsintegration, operative Verantwortlichkeit und Kosten.

## 13. Referenzen

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

Vorherige: [Serie 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->