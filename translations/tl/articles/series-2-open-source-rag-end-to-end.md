# Turuan ang AI na Sagutin ang mga Tanong Batay sa Iyong mga Dokumento
## Seri 2: Gumawa ng Isang Lokal na Open-Source RAG System Mula Simula Hanggang Wakas

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Ang artikulong ito ay ginagawang isang maipatupad na lokal na RAG tutorial mula sa diskusyon ng arkitektura sa Seri 1. Ang layunin ay buuin muna ang buong workflow gamit ang sample data, walang cloud account, at walang mga sikreto, pagkatapos ay gamitin ang gumaganang baseline na iyon upang makagawa ng mas magagandang desisyon sa arkitektura sa hinaharap.

Ang sistemang ating itatayo ay isang maliit na school policy assistant. Gumamit ako ng dalawang lokal na Markdown na dokumento bilang knowledge base, pagkatapos ay tatahakin ang buong RAG pipeline: chunking, lokal na embeddings, Qdrant vector storage, retrieval, reranking, source-aware answer composition, at opsyonal na lokal na generation gamit ang Ollama at Phi-4-mini.

Navigasyon sa serye: [Repository home](../README.md) | Nakaraan: [Seri 1 - RAG, Azure vs Open-Source Alternatives, at Kailan May Katwiran ang Fine-Tuning](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Mga Kinakailangan: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Ito ang pinakamagandang panimulang punto kung nais mong maunawaan ang RAG pipeline bago gumawa ng cloud resources. Ang default na landas ay tumatakbo nang lokal gamit ang CPU-friendly na mga embedding at walang mga sikreto.

## 1. Ano ang Ating Itatayo

Sa tutorial noong 2023, nagsimula ako sa Azure dahil ang layunin ay ipakita kung paano sumasagot ang Azure AI Search at Azure OpenAI sa mga tanong mula sa mga PDF na dokumento.

Para sa seryeng ito ng 2026, nais kong magsimula sa isang mas mababang antas.

Bago gumamit ng managed services, nais kong bumuo ng isang maliit na RAG system nang lokal at gawin na nakikita ang bawat hakbang: pag-load ng mga dokumento, pagchunk ng teksto, pag-iimbak ng mga vector, pagkuha ng ebidensya, reranking ng mga resulta, at pagbibigay ng sagot na may kaalaman sa pinagmulan.

Ang sample na senaryo ay isang school policy assistant. Tatanungin ng user:

```text
Can I use generative AI for my final assignment?
```

Hindi dapat sumagot ang sistema mula sa pangkalahatang memorya ng modelo. Dapat nitong kunin ang kaugnay na seksyon ng polisiya at sumagot mula sa ebidensyang iyon.

Ang buong maipatupad na bersyon ay nasa [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Ipinapakita ng code sa ibaba ang mga pangunahing hakbang upang mabasa ang artikulo bilang isang tutorial.

## 2. I-install ang mga Lokal na Dependency

Gumawa ng virtual environment at i-install ang mga kinakailangan para sa Seri 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ginagamit ng unang bersyon ang Qdrant local mode at FastEmbed. Sinusuportahan ng Qdrant Python client ang in-memory local mode gamit ang `QdrantClient(":memory:")`, na kapaki-pakinabang para sa mga lokal na tutorial at CI-style na verification. Nagbibigay ang FastEmbed ng tunay na lokal na embedding model nang hindi nangangailangan ng cloud API key.

Kasama rin sa requirements file ang `python-dotenv` dahil maaaring basahin ng notebook nang opsyonal ang pangalan ng Ollama model mula sa `.env`. Hindi kailangan ng Azure OpenAI o OpenAI API key para sa lokal na tutorial na ito.

## 3. I-load ang mga Sample na Dokumento

Sadyang maliit ang sample na corpus:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Sa notebook, niloload ko lahat ng Markdown files mula sa `sample_data/`:

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

Nang patakbuhin ko ang notebook, niload nito ang 2 dokumento. Sapat na itong liit para suriin nang mano-mano, na kapaki-pakinabang kapag bumubuo ng unang bersyon ng RAG pipeline.

## 4. I-chunk Ayon sa Markdown Headings

Susunod na hakbang ay hatiin ang mga dokumento sa mga chunk.

Para sa tutorial na ito, ginamit ko ang mga Markdown heading bilang signal ng istraktura. Ang pamagat ng dokumento ay nagmumula sa `#`, at bawat seksyon na chunk ay nagmumula sa `##`.

> [!NOTE]
> Hindi one-size-fits-all ang chunking. Sa tutorial na ito, ginamit ko ang Markdown headings dahil malinaw ang `#` at `##` na istraktura ng mga sample na dokumento. Para sa mga PDF, Word documents, slides, tickets, o mga web page, maaaring gamitin ang mas mahusay na estratehiya tulad ng mga hangganan ng pahina, impormasyon sa layout, semantic sections, token limits, mga talaan, o metadata. Ang mahalagang punto ay pumili ng estratehiya sa chunking na nagpapreserba ng kahulugan at nasusubaybayan ang pinagmulan para sa iyong mga dokumento.

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

Pagkatapos ay inilapat ko ito sa bawat dokumento:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Nagawa nito ang 8 chunks sa lokal kong pagtakbo.

Ang nagustuhan ko sa hakbang na ito ay ang metadata ay kapaki-pakinabang na agad. Alam ng bawat chunk ang `source`, `sectionHeading`, `documentVersion`, at placeholder na `permissions`. Kahit sa maliit na tutorial, ito ay nagpapadali ng pag-iisip tungkol sa mga citation at pagkuha na may kaalaman sa permiso.

## 5. Gumawa ng Lokal na Embeddings

Para sa unang pampublikong bersyon, ginamit ko ang `BAAI/bge-small-en-v1.5` sa pamamagitan ng FastEmbed.

Pinananatili nitong lokal at CPU-friendly ang tutorial, ngunit gumagamit pa rin ng tunay na embedding model sa halip na placeholder vector function. Ang unang pagtakbo ay nagda-download ng mga weight ng modelo. Pagkatapos noon, maaaring gamitin ng notebook ang lokal na cache.

> [!NOTE]
> Ginamit ko ang `BAAI/bge-small-en-v1.5` dahil ito ay magaan na English embedding model na mahusay sa FastEmbed at Qdrant para sa lokal na tutorial. Gumagawa ito ng 384-dimensional vectors, na nagpapabilis at nagpapababa ng gastos sa lokal na pagpapatakbo. Hindi ito ang nag-iisang magandang pagpipilian. Noong 2023, maraming tutorial ang gumamit ng hosted embedding models tulad ng `text-embedding-ada-002`. Ngayon, mas bagong hosted option tulad ng OpenAI `text-embedding-3-small` at `text-embedding-3-large`, pati na rin ang open-source na mga opsyon tulad ng BGE, E5, MiniLM, Nomic Embed, at multilingual models tulad ng `BAAI/bge-m3` ay makatwirang pagpipilian depende sa workload. Sa produksyon, dapat piliin ang tamang embedding model batay sa retrieval evaluation sa sariling mga dokumento.

Ilang praktikal na alternatibo:

| Pamilya ng Modelo | Kung Kailan Ko Ito Isasaalang-alang |
| --- | --- |
| `text-embedding-ada-002` | Mas matandang hosted baseline na lumabas sa maraming tutorial noong 2023. Hindi ko ito pipiliin bilang default para sa bagong tutorial ngayon. |
| `text-embedding-3-small` | Modernong hosted default kapag gusto ko ng malakas na balanse ng gastos/pagganap at hindi kailangan ng lokal na embeddings lamang. |
| `text-embedding-3-large` | Hosted na opsyon kapag mas mahalaga ang kalidad ng retrieval kaysa sa laki ng vector o gastos ng embedding. |
| `BAAI/bge-small-en-v1.5` | Magaan na lokal na English baseline para sa mga tutorial, prototype, at CPU-friendly na eksperimento. |
| `BAAI/bge-base-en-v1.5` o `BAAI/bge-large-en-v1.5` | Mas malalaking lokal na English na modelo kapag gusto ko ng mas mahusay na kalidad ng retrieval at kaya ng mas mataas na compute. |
| `BAAI/bge-m3` | Multilingual o retrieval na may mas mahaba pang konteksto, lalo na kapag hindi lang English ang mga dokumento. |
| `sentence-transformers/all-MiniLM-L6-v2` | Napakaliit at mabilis na semantic search baseline. Kapaki-pakinabang kapag bilis at pagiging simple ang pinakamahalaga. |
| `nomic-embed-text-v1.5` | Open local embedding option na sulit subukan para sa mas mahahabang konteksto o mga setup na nakatuon sa portability. |

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

Pagkatapos ay binigyan ng embedding ang bawat chunk:

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

## 6. I-store ang mga Vector sa Qdrant Local Mode

Ngayon ay gagawa tayo ng in-memory na Qdrant collection at ipapasok ang mga chunk na may payload metadata.

> [!NOTE]
> Sa tutorial na 2023, ginamit ko ang FAISS dahil ito ay simple at popular na paraan para ipakita ang lokal na vector similarity search gamit ang LangChain. Kapaki-pakinabang pa rin ang FAISS para sa mabilisang lokal na eksperimento. Sa bersyon ng 2026, ginamit ko ang Qdrant dahil gusto ko ang tutorial ay mas malapit sa production RAG system. Pinapahintulutan ako ng Qdrant na mag-imbak ng vectors kasama ang payload metadata gaya ng pinagmulan ng file, section heading, bersyon ng dokumento, at mga permiso. Pinapadali nito ang pag-iinspeksyon ng retrieval at inihahanda ang halimbawa para sa filtering, citations, at hinaharap na persistent o server-based deployment.

Magaling ang FAISS para ipakita ang vector similarity search. Mas maganda ang Qdrant para ipakita ang maliit ngunit production-shaped na RAG retrieval layer.

Ilang praktikal na alternatibo:

| Vector store / search layer | Kung Kailan Ko Ito Isasaalang-alang |
| --- | --- |
| Qdrant | Lokal na prototype, metadata filtering, production-friendly na vector search, at simpleng Python workflow. |
| Chroma | Mabilis na lokal na RAG eksperimento at notebook kung saan mahalaga ang pagiging simple. |
| FAISS | Magaan na lokal na vector search kapag kailangan ko lang ng similarity search at kayang pangasiwaan ang metadata nang hiwalay. |
| Milvus | Mas malakihang open-source vector search kapag handang magpatakbo ng dedikadong vector database ang team. |
| Weaviate | Vector search na may schema, metadata, hybrid search, at may managed o self-hosted na deployment options. |
| Azure AI Search | Enterprise RAG sa Azure kapag gusto ko ng keyword search, vector search, hybrid retrieval, semantic ranking, filtering, seguridad, at managed operations sa isang search layer. |
| PostgreSQL + pgvector | Mga team na gumagamit na ng PostgreSQL at nais ng vector search na malapit sa application data. |

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

Pagkatapos ipasok ang mga puntos:

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

Sa pagtakbo ko, nakapasok ang koleksyon ng 8 vectors.

Dito nagsisimulang maging masusuri ang RAG system. Hindi lang vectors ang iniimbak ng vector database; iniimbak din nito ang ebidensya ng teksto at metadata na kailangan para sa mga citation.

## 7. Kunin ang mga Kandidatong Chunk

Ngayon ay magtatanong tayo at kukunin ang mga kandidatong chunk.

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

Dito, ipiniprint ko ang mga nakuha bago gumawa ng sagot. Mahalaga ito. Kung mali ang retrieval, itatago lang ng generation ang problema sa likod ng maayos na teksto.

## 8. Magdagdag ng Magaan na Reranker

Nang una kong subukan ang retrieval path, nakakita ng may kaugnayang policy content gamit ang vector similarity ngunit hindi palaging nasa taas ang pinaka-tumpak na seksyon.

Kaya nagdagdag ako ng maliit na lokal na reranker. Nagbibigay ito ng dagdag na timbang kapag may overlap ang mga termino sa tanong sa section heading at nilalaman.

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

Pagkatapos ng reranking, ang nangungunang resulta ay naging:

```text
school_ai_policy.md / Final Assignments
```

Ito ang inaasahang seksyon para sa test question.

Ito ang pinakakapaki-pakinabang na aral mula sa unang implementasyon. Kahit sa maliit na lokal na halimbawa, bumuti ang kalidad ng retrieval nang pinagsama ko ang vector similarity at isa pang signal.

## 9. Bumuo ng Batay sa Pinagmulan na Lokal na Sagot

Para sa default na landas, ginamit ko ang transparent na lokal na answer composer sa halip na LLM.

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

Hindi ito nilalayong isang panghuling produkto ng generator ng sagot. Isa itong tool sa pag-debug. Pinatutunayan nito na gumagana ang retrieval, metadata, at wiring ng citation bago idagdag ang variability ng modelo.

## 10. Gumawa ng Lokal na Sagot gamit ang Ollama at Phi-4-mini

Kapag gumagana na ang retrieval, maaaring palitan ng notebook ang huling hakbang ng sagot gamit ang Ollama at `phi4-mini:3.8b`.

> [!NOTE]
> Dapat palitan ng Ollama ang huling hakbang ng pagbuo ng sagot lamang. Ang pag-load ng dokumento, chunking, vector storage, retrieval, reranking, at citation wiring ay dapat manatiling pareho.

Una, bumuo ang notebook ng evidence prompt mula sa nakuha na mga chunk:

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

Para sa tutorial na ito, inirerekomenda ko ang Phi-4-mini family ng Microsoft sa pamamagitan ng Ollama bilang default na opsyon sa lokal na generation. Sa Ollama, ang modelong sinubukan ko ay:

```powershell
ollama pull phi4-mini:3.8b
```

Mabilis mong masusuri kung available ang modelo:

```powershell
ollama list
```

Pagkatapos ay itakda ang mga variable na ito:

```powershell
Copy-Item .env.example .env
```

Buksan ang `.env` at tanggalin ang comment sa mga halaga ng Seri 2 Ollama:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Ilo-load ng notebook ang `.env` mula sa root ng repository gamit ang `python-dotenv`, pagkatapos ay ipapadala ang parehong evidence prompt sa lokal na `/api/chat` endpoint ng Ollama na naka-disable ang streaming. Kung hindi tumatakbo ang Ollama o nawawala ang `SERIES2_OLLAMA_MODEL`, nilalaktawan ang track na ito.

> [!NOTE]
> Sa makinang ito, nag-download ang `phi4-mini:3.8b` ng mga model file na humigit-kumulang 2.49GB. Sa panahon ng inference, iniulat ng Ollama ang 3.3GB na laki ng loaded model at ginamit ang RTX 3060 Laptop GPU.

Nagbibigay ito sa tutorial ng dalawang antas:

1. CPU-only deterministic answer composer.
2. Lokal na pagbuo ng sagot gamit ang Ollama at Phi-4-mini.

Pareho ang retrieval pipeline sa dalawang ito.

## 11. Resulta ng Pag-verify

Patakbuhin ko ang notebook nang lokal sa Windows gamit ang Python 3.12.6.

Mga naka-install na package:

| Package | Bersyon |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Pagtatakbo ng notebook:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Resulta ng pagtakbo: pumasa gamit ang `nbclient`
- Mga dokumentong niload: 2
- Mga chunk na ginawa: 8
- Koleksyon ng Qdrant: `school_policy_local`
- Mga vector na naisama: 8
- Embedding model: `BAAI/bge-small-en-v1.5`
- Laki ng embedding: 384
- Tanong sa pagpapatala: "Maaari ko bang gamitin ang generative AI para sa aking huling takdang-aralin?"
- Landas ng pagsasaayos muli: magaan na lokal na leksikal na pagsasaayos muli
- Nangungunang nakuha na pinagmulan pagkatapos ng pagsasaayos muli: `school_ai_policy.md`
- Nangungunang nakuha na seksyon pagkatapos ng pagsasaayos muli: `Final Assignments`
- Default na landas ng sagot: lokal na transparent na tagagawa ng sagot
- Landas ng Ollama generation: nakumpleto gamit ang `phi4-mini:3.8b`
- Laki ng file ng Ollama model: 2.49GB sa disk
- Laki ng loaded na Ollama model: 3.3GB iniulat ng `ollama ps`
- GPU offload: 100% GPU iniulat ng `ollama ps`
- Memorya ng GPU na naobserbahan pagkatapos ng generation: mga 3.5GB ng 6GB ang nagamit sa RTX 3060 Laptop GPU
- Pagpapatupad ng Notebook gamit ang naka-cache na FastEmbed model at Ollama generation na naka-enable: pumasa sa mga 34 na segundo sa pamamagitan ng verification script

Ang sagot na ginawa ng Ollama ay:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```
  
Hindi ko tatawaging perpekto ang sagot na ito. Sumagot ito mula sa tamang ebidensya, ngunit ang huling linya ng pinagmulan ay hindi kasing tumpak kumpara sa deterministic na format ng pagsipi. Kapaki-pakinabang itong ipakita sa tutorial dahil nagpapalinaw ito ng susunod na tanong sa engineering: kailangan din ng pagsusuri ang paggawa ng sagot, hindi lamang ang pagpapatala.

Ang pangunahing natutunan ko habang sinusuri ito ay dapat munang suriin ang kalidad ng pagpapatala bago ang paggawa ng sagot. Ang resulta ng embedding ay kapaki-pakinabang na, at ang magaan na reranker ay natiyak na unang lumabas ang inaasahang seksyon ng patakaran. Ito ang klase ng maliit na pag-uugali ng sistema na nais kong ipakita sa tutorial sa halip na itago.

## 12. Ano ang Susunod

Ang susunod na pagpapabuti ay ikumpara ang lokal na setup na ito sa isang managed Azure na bersyon ng parehong senaryo ng katulong na patakaran sa paaralan. Ang pagpapanatiling pareho ng senaryo ay dapat gawing mas madali ang pagtingin sa mga tradeoff: maging ang pagiging kumplikado ng setup, mga kontrol sa pagpapatala, integrasyon ng pagkakakilanlan, pagmamay-ari ng pagpapatakbo, at gastos.

## 13. Mga Sanggunian

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

Nakaraan: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->