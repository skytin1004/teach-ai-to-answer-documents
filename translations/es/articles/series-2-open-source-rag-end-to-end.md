# Enseña a la IA a Responder Preguntas Basadas en Tus Documentos
## Serie 2: Construir un Sistema RAG Local y Open Source de Extremo a Extremo

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Este artículo convierte la discusión de arquitectura de la Serie 1 en un tutorial ejecutable local de RAG. El objetivo es construir primero el flujo de trabajo completo con datos de ejemplo, sin cuenta en la nube y sin secretos, para luego usar esa línea base funcional para tomar mejores decisiones de arquitectura.

El sistema que construiremos es un asistente de políticas escolares pequeño. Uso dos documentos Markdown locales como base de conocimiento, luego recorro todo el pipeline RAG: fragmentación, embeddings locales, almacenamiento vectorial Qdrant, recuperación, reranking, composición de respuesta con conocimiento de la fuente y generación local opcional con Ollama y Phi-4-mini.

Navegación de la serie: [Inicio del repositorio](../README.md) | Anterior: [Serie 1 - RAG, Azure vs Alternativas Open Source, y Cuándo Tiene Sentido Afinar](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Requisitos: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Este es el mejor punto de partida si quieres entender el pipeline RAG antes de crear recursos en la nube. El camino por defecto se ejecuta localmente con embeddings amigables para CPU y sin secretos.

## 1. Qué Estamos Construyendo

En el tutorial de 2023, comencé con Azure porque el objetivo era mostrar cómo Azure AI Search y Azure OpenAI podían responder preguntas a partir de documentos PDF.

Para esta serie 2026, quiero empezar un nivel más abajo.

Antes de usar servicios gestionados, quiero construir un pequeño sistema RAG localmente y hacer visible cada paso: cargar documentos, fragmentar texto, almacenar vectores, recuperar evidencias, reranking de resultados y devolver una respuesta con conocimiento de la fuente.

El escenario de ejemplo es un asistente de políticas escolares. El usuario pregunta:

```text
Can I use generative AI for my final assignment?
```

El sistema no debe responder desde la memoria general del modelo. Debe recuperar la sección relevante de la política y responder basándose en esa evidencia.

La versión ejecutable completa está en [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). El código a continuación muestra los pasos principales para que el artículo pueda leerse como un tutorial.

## 2. Instalar las Dependencias Locales

Crea un entorno virtual e instala los requisitos de la Serie 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

La primera versión usa el modo local de Qdrant y FastEmbed. El cliente Python de Qdrant soporta un modo local en memoria con `QdrantClient(":memory:")`, útil para tutoriales locales y verificación estilo CI. FastEmbed nos da un modelo de embedding real local sin requerir clave API en la nube.

El archivo de requisitos también incluye `python-dotenv` porque el notebook puede leer opcionalmente el nombre de un modelo Ollama desde `.env`. No se requiere clave API de Azure OpenAI ni OpenAI para este tutorial local.

## 3. Cargar los Documentos de Ejemplo

El corpus de ejemplo es intencionalmente pequeño:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

En el notebook, cargo todos los archivos Markdown de `sample_data/`:

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

Cuando ejecuté el notebook, cargó 2 documentos. Eso es lo suficientemente pequeño para inspeccionarlo manualmente, lo cual es útil al construir la primera versión de un pipeline RAG.

## 4. Fragmentar por Encabezados Markdown

El siguiente paso es dividir los documentos en fragmentos.

Para este tutorial, uso los encabezados Markdown como la señal de estructura. El título del documento viene de `#`, y cada fragmento de sección de `##`.

> [!NOTE]
> La fragmentación no es una solución única para todos. En este tutorial, uso encabezados Markdown porque los documentos de ejemplo tienen clara estructura `#` y `##`. Para PDFs, documentos Word, diapositivas, tickets o páginas web, una mejor estrategia puede usar límites de página, información de diseño, secciones semánticas, límites de tokens, tablas o metadatos. Lo importante es elegir una estrategia de fragmentación que preserve el significado y la trazabilidad de la fuente para tus documentos.

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

Luego lo aplico a cada documento:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Esto creó 8 fragmentos en mi ejecución local.

Lo que me gustó de este paso es que los metadatos ya son útiles. Cada fragmento sabe su `source`, `sectionHeading`, `documentVersion` y un marcador `permissions`. Incluso en un tutorial pequeño, esto facilita razonar sobre citas y la recuperación con conciencia de permisos después.

## 5. Crear Embeddings Locales

Para la primera versión pública, uso `BAAI/bge-small-en-v1.5` a través de FastEmbed.

Esto mantiene el tutorial local y amigable para CPU, pero usa un modelo real de embedding en lugar de una función vectorial genérica. La primera ejecución descarga los pesos del modelo. Luego, el notebook puede reutilizar la caché local.

> [!NOTE]
> Uso `BAAI/bge-small-en-v1.5` porque es un modelo de embedding en inglés ligero que funciona bien con FastEmbed y Qdrant para un tutorial local. Crea vectores de 384 dimensiones, lo que mantiene el ejemplo rápido y barato para ejecutar localmente. No es la única buena opción. En 2023, muchos tutoriales usaban modelos de embedding alojados como `text-embedding-ada-002`. Hoy, opciones alojadas más nuevas como OpenAI `text-embedding-3-small` y `text-embedding-3-large`, y opciones open source como BGE, E5, MiniLM, Nomic Embed y modelos multilingües como `BAAI/bge-m3` son todas opciones razonables según la carga de trabajo. En producción, el modelo de embedding correcto debe seleccionarse a través de evaluación de recuperación con tus propios documentos.

Algunas alternativas prácticas:

| Familia de modelo | Cuándo la consideraría |
| --- | --- |
| `text-embedding-ada-002` | Línea base alojada antigua que apareció en muchos tutoriales de la era 2023. No la elegiría como predeterminada para un tutorial nuevo hoy. |
| `text-embedding-3-small` | Predeterminada moderna alojada cuando quiero un buen balance costo/rendimiento y no necesito embeddings sólo locales. |
| `text-embedding-3-large` | Opción alojada cuando la calidad de recuperación importa más que el tamaño vectorial o costo de embedding. |
| `BAAI/bge-small-en-v1.5` | Línea base local ligera en inglés para tutoriales, prototipos y experimentos amigables para CPU. |
| `BAAI/bge-base-en-v1.5` o `BAAI/bge-large-en-v1.5` | Modelos locales en inglés más grandes cuando quiero mejor calidad de recuperación y puedo permitir más cómputo. |
| `BAAI/bge-m3` | Recuperación multilingüe o para contextos más largos, especialmente cuando los documentos no son solo en inglés. |
| `sentence-transformers/all-MiniLM-L6-v2` | Línea base de búsqueda semántica muy pequeña y rápida. Útil cuando la velocidad y simplicidad son lo más importante. |
| `nomic-embed-text-v1.5` | Opción local abierta de embedding que vale la pena probar para contextos más largos o configuraciones enfocadas en portabilidad. |

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

Luego, cada fragmento obtiene un embedding:

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

## 6. Almacenar Vectores en Modo Local Qdrant

Ahora creamos una colección Qdrant en memoria e insertamos los fragmentos con metadatos en el payload.

> [!NOTE]
> En el tutorial de 2023, usé FAISS porque era una forma simple y popular de demostrar búsqueda local por similitud vectorial con LangChain. FAISS sigue siendo útil para experimentos locales rápidos. En esta versión 2026, uso Qdrant porque quiero que el tutorial se sienta más cercano a un sistema RAG productivo. Qdrant me permite almacenar vectores junto con metadatos del payload como archivo fuente, encabezado de sección, versión del documento y permisos. Eso facilita inspeccionar la recuperación y prepara el ejemplo para filtrado, citas y despliegue futuro persistente o en servidor.

FAISS es genial para mostrar búsqueda por similitud vectorial. Qdrant es mejor para mostrar una capa de recuperación RAG pequeña pero con forma de producción.

Algunas alternativas prácticas:

| Almacén de vectores / capa de búsqueda | Cuándo la consideraría |
| --- | --- |
| Qdrant | Prototipos locales, filtrado por metadatos, búsqueda vectorial amigable para producción y un flujo sencillo en Python. |
| Chroma | Experimentos rápidos locales RAG y notebooks donde la simplicidad es lo más importante. |
| FAISS | Búsqueda vectorial ligera local cuando solo necesito búsqueda por similitud y puedo gestionar metadatos por separado. |
| Milvus | Búsqueda vectorial open source a escala más grande cuando el equipo está listo para operar una base de datos vectorial dedicada. |
| Weaviate | Búsqueda vectorial con esquema, metadatos, búsqueda híbrida y opciones gestionadas o auto hospedadas. |
| Azure AI Search | RAG empresarial en Azure cuando quiero búsqueda por palabra clave, vectorial, recuperación híbrida, ranking semántico, filtrado, seguridad y operaciones gestionadas en una sola capa de búsqueda. |
| PostgreSQL + pgvector | Equipos que ya usan PostgreSQL y quieren búsqueda vectorial cerca de los datos de la aplicación. |

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

Luego insertamos los puntos:

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

En mi ejecución, la colección insertó 8 vectores.

Aquí es donde el sistema RAG empieza a ser inspeccionable. La base de datos vectorial no sólo almacena vectores; también almacena el texto de evidencia y los metadatos necesarios para las citas.

## 7. Recuperar Fragmentos Candidatos

Ahora hacemos la pregunta y recuperamos fragmentos candidatos.

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

En este punto, imprimo los fragmentos recuperados antes de generar una respuesta. Esto es importante. Si la recuperación falla, la generación sólo ocultará el problema tras un texto fluido.

## 8. Añadir un Reranker Ligero

Cuando probé por primera vez la ruta de recuperación, la similitud vectorial sola encontró contenido de política relacionado, pero la sección más precisa no siempre estaba en primer lugar.

Así que añadí un pequeño reranker local. Da peso extra cuando los términos de la pregunta se superponen con el encabezado de la sección y el contenido.

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

Después del reranking, el resultado principal fue:

```text
school_ai_policy.md / Final Assignments
```

Esa fue la sección esperada para la pregunta de prueba.

Esta fue la lección más útil de la primera implementación. Incluso en un ejemplo local pequeño, la calidad de recuperación mejoró cuando combiné la similitud vectorial con otra señal.

## 9. Componer una Respuesta Local Fundamentada

Para el camino por defecto, uso un compositor de respuestas local transparente en lugar de un LLM.

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

Esto no está pensado como un generador de respuestas final. Es una herramienta de depuración. Demuestra que recuperación, metadatos y enlace a citas funcionan antes de añadir variabilidad del modelo.

## 10. Generar una Respuesta Local con Ollama y Phi-4-mini

Una vez que la recuperación funciona, el notebook puede reemplazar sólo el paso final de respuesta con Ollama y `phi4-mini:3.8b`.

> [!NOTE]
> Ollama debe reemplazar sólo el paso final de generación de respuesta. La carga de documentos, fragmentación, almacenamiento vectorial, recuperación, reranking y enlace a citas deben mantenerse igual.

Primero, el notebook construye un prompt de evidencia a partir de los fragmentos recuperados:

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

Para este tutorial, recomiendo la familia Phi-4-mini de Microsoft a través de Ollama como opción local predeterminada para generación. En Ollama, el nombre del modelo que probé es:

```powershell
ollama pull phi4-mini:3.8b
```

Puedes verificar rápidamente que el modelo está disponible:

```powershell
ollama list
```

Luego configura estas variables:

```powershell
Copy-Item .env.example .env
```

Abre `.env` y descomenta los valores de Ollama de la Serie 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

El notebook carga `.env` desde la raíz del repositorio con `python-dotenv`, luego envía el mismo prompt de evidencia al endpoint local `/api/chat` de Ollama con streaming desactivado. Si Ollama no está corriendo o falta `SERIES2_OLLAMA_MODEL`, esta ruta se omite.

> [!NOTE]
> En esta máquina, `phi4-mini:3.8b` descargó alrededor de 2.49GB de archivos de modelo. Durante la inferencia, Ollama reportó un tamaño cargado de modelo de 3.3GB y usó la GPU RTX 3060 Laptop.

Esto da al tutorial dos niveles:

1. Compositor de respuestas determinista solo CPU.
2. Generación de respuestas local con Ollama y Phi-4-mini.

El pipeline de recuperación se mantiene igual en ambos.

## 11. Resultado de Verificación

Ejecuté el notebook localmente en Windows con Python 3.12.6.

Paquetes instalados:

| Paquete | Versión |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Ejecución del notebook:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Resultado de ejecución: aprobado con `nbclient`
- Documentos cargados: 2
- Fragmentos creados: 8
- Colección Qdrant: `school_policy_local`
- Vectores insertados: 8
- Modelo de embedding: `BAAI/bge-small-en-v1.5`
- Tamaño del embedding: 384
- Pregunta de recuperación: "¿Puedo usar IA generativa para mi trabajo final?"
- Ruta de reordenamiento: reordenamiento léxico local ligero
- Fuente superior recuperada después del reordenamiento: `school_ai_policy.md`
- Sección superior recuperada después del reordenamiento: `Final Assignments`
- Ruta de respuesta predeterminada: compositor de respuestas transparente local
- Ruta de generación Ollama: completada con `phi4-mini:3.8b`
- Tamaño del archivo del modelo Ollama: 2.49GB en disco
- Tamaño del modelo Ollama cargado: 3.3GB reportado por `ollama ps`
- Descarga a GPU: 100% GPU reportado por `ollama ps`
- Memoria GPU observada después de la generación: aproximadamente 3.5GB de 6GB usados en RTX 3060 Laptop GPU
- Ejecución del notebook con modelo FastEmbed en caché y generación Ollama habilitada: pasada en aproximadamente 34 segundos mediante el script de verificación

La respuesta generada por Ollama fue:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

No llamaría perfecta a esta respuesta. Responde desde la evidencia correcta, pero la línea final de la fuente es menos precisa que el formato de cita determinista. Eso es útil mostrarlo en el tutorial porque hace obvia la siguiente pregunta de ingeniería: la generación de respuestas también necesita evaluación, no solo la recuperación.

Lo principal que aprendí mientras verificaba esto es que la calidad de la recuperación debería revisarse antes de la generación de respuestas. El resultado del embedding ya era útil, y el reordenador ligero hizo que la sección de política esperada apareciera primero de manera confiable. Ese es exactamente el tipo de comportamiento pequeño del sistema que quiero que el tutorial exponga en lugar de ocultar.

## 12. Qué Sigue

La siguiente mejora es comparar esta configuración local con una versión gestionada en Azure del mismo escenario del asistente de políticas escolares. Mantener el escenario fijo debería facilitar ver las compensaciones: complejidad de la configuración, controles de recuperación, integración de identidad, propiedad operativa y costo.

## 13. Referencias

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Repositorio GitHub del cliente Qdrant](https://github.com/qdrant/qdrant-client)
- [Modelos soportados por FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Guía de embeddings de OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Ficha técnica del modelo BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Ficha técnica del modelo BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Ficha técnica del modelo sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Página del modelo Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Documentación de Ollama para Windows](https://docs.ollama.com/windows)
- [Documentación de streaming de la API de Ollama](https://docs.ollama.com/api/streaming)
- [Ficha técnica del modelo Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Resumen de LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Introducción a RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Anterior: [Serie 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->