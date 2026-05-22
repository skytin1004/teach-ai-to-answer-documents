# Tanítsd meg az MI-t kérdések megválaszolására a dokumentumaid alapján
## 2. sorozat: Készíts egy helyi, nyílt forráskódú RAG rendszert az elejétől a végéig

![Helyi nyílt forráskódú RAG oktatócső](../../../assets/images/series-2-local-rag.svg)

> Ez a cikk az 1. sorozat architektúra megbeszélését alakítja futtatható helyi RAG oktatóanyaggá. A cél az, hogy először mintaadatokkal, felhőfiók és titkok nélkül építsük fel a teljes munkafolyamatot, majd ezt a működő alapot felhasználva később jobb architektúra döntéseket hozzunk.

A rendszer, amit építünk, egy kis iskolai irányelmi asszisztens. Két helyi Markdown dokumentumot használok tudásbázisként, majd végigmegyek a teljes RAG csövön: darabolás, helyi embeddingek, Qdrant vektor tárolás, lekérés, újrarendezés, forrás-tudatos válaszkészítés és opcionális helyi generálás Ollama és Phi-4-mini segítségével.

Sorozat navigáció: [Tárház főoldal](../README.md) | Előző: [1. sorozat - RAG, Azure vs Nyílt forráskódú alternatívák és amikor az finomhangolás értelmes](./series-1-rag-azure-open-source-fine-tuning.md)

Jegyzetfüzet: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Követelmények: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Ez a legjobb kiindulópont, ha meg akarod érteni a RAG csövet mielőtt felhő erőforrásokat hozol létre. Az alapértelmezett út helyben fut CPU-barát embeddingekkel és titkok nélkül.

## 1. Amit építünk

A 2023-as oktatóanyagban az Azure-ról indultam, mert a cél az volt, hogy megmutassam, hogyan válaszolhat az Azure AI Search és az Azure OpenAI kérdésekre PDF dokumentumokból.

Ehhez a 2026-os sorozathoz egy réteggel lejjebb akarok kezdeni.

Felügyelt szolgáltatások használata előtt kis helyi RAG rendszert akarok építeni, és minden lépést láthatóvá tenni: dokumentum betöltése, szöveg darabolása, vektorok tárolása, bizonyíték lekérése, eredmények újrarendezése és forrástudatos válasz visszaadása.

A mintaszituáció egy iskolai irányelmi asszisztens. A felhasználó ezt kérdezi:

```text
Can I use generative AI for my final assignment?
```

A rendszer nem válaszolhat a általános modellmemóriából. A releváns irányelvi szakaszt kell lekérni és onnan válaszolni.

A teljes futtatható verzió megtalálható a [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) fájlban. Az alábbi kód a fő lépéseket mutatja, hogy a cikk oktatóanyagként is olvasható legyen.

## 2. Telepítsd a helyi függőségeket

Hozz létre egy virtuális környezetet és telepítsd a 2. sorozat követelményeit:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Az első verzió Qdrant helyi módot és FastEmbed-et használ. A Qdrant Python kliens támogat egy memórián belüli helyi módot `QdrantClient(":memory:")`-vel, ami hasznos helyi oktatóanyagokhoz és CI-stílusú ellenőrzéshez. A FastEmbed valódi helyi embedding modellt ad, felhő API kulcs nélkül.

A követelmény fájlban benne van a `python-dotenv` is, mert a jegyzetfüzet opcionálisan beolvashat Ollama modell nevet `.env`-ből. Ehhez a helyi oktatóanyaghoz nem kell Azure OpenAI vagy OpenAI API kulcs.

## 3. Töltsd be a mintadokumentumokat

A mintakorpuszt szándékosan kicsire vettem:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

A jegyzetfüzetben az összes Markdown fájlt betöltöm a `sample_data/` könyvtárból:

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

Amikor futtattam a jegyzetet, 2 dokumentum töltődött be. Ez kézzel is ellenőrizhetően kicsi, ami hasznos az első RAG cső verzió építésénél.

## 4. Darabolás Markdown címsorok szerint

A következő lépés a dokumentumok darabolása.

Ehhez az oktatóanyaghoz Markdown címsorokat használok struktúra jelzésként. A dokumentum címe a `#`, minden szakasz darabja a `##`-ból jön.

> [!NOTE]
> A darabolás nem egy méret mindnek. Ebben az oktatóanyagban Markdown címsorokat használok, mert a mintadokumentumok világos `#` és `##` struktúrát tartalmaznak. PDF-eknél, Word dokumentumoknál, diáknál, jegyeknél vagy weboldalaknál jobb stratégiák lehetnek oldalhatárok, elrendezés adatok, szemantikai szakaszok, token limit, táblázatok vagy metaadatok használata. A fontos, hogy olyan darabolási stratégiát válassz, ami megőrzi a jelentést és a forráskövethetőséget a dokumentumaid esetén.

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

Majd alkalmazom minden dokumentumra:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Ez a helyi futásommal 8 darabot eredményezett.

Ami tetszett ebben a lépésben, hogy a metaadatok már hasznosak. Minden darab tudja a `source` (forrás), `sectionHeading` (szakaszcím), `documentVersion` (dokumentum verzió), és helyőrző `permissions` értékeket. Még egy kis oktatóanyagnál is ez megkönnyíti a hivatkozásokat és későbbi jogosultságtudatos lekérést.

## 5. Készíts helyi embeddingeket

Az első publikus verzióhoz a `BAAI/bge-small-en-v1.5` modellt használom FastEmbed-en keresztül.

Ez az oktatóanyagot helyi és CPU-barát módon tartja, de valódi embedding modellt használ, nem csak helyőrző vektor függvényt. Az első futás letölti a modell súlyokat. Utána a jegyzetfüzet használhatja a helyi cache-t.

> [!NOTE]
> A `BAAI/bge-small-en-v1.5`-öt használom, mert ez egy könnyű angol embedding modell, ami jól működik FastEmbed-del és Qdrant-tal egy helyi oktatóanyaghoz. 384-dimenziós vektorokat készít, ami gyors és olcsó példafuttatást tesz lehetővé helyben. Ez nem az egyetlen jó választás. 2023-ban sok oktatóanyag használt hosztolt embedding modelleket, mint a `text-embedding-ada-002`. Ma modernebb hosztolt opciók, mint az OpenAI `text-embedding-3-small` és `text-embedding-3-large`, valamint nyílt forráskódú verziók, mint a BGE, E5, MiniLM, Nomic Embed és többnyelvű modellek, mint a `BAAI/bge-m3` mind ésszerű választások terheléstől függően. Éles környezetben a megfelelő embedding modellt saját dokumentumokon végzett lekérés értékelés alapján kell kiválasztani.

Néhány gyakorlati alternatíva:

| Modell család | Mikor gondolnám meg |
| --- | --- |
| `text-embedding-ada-002` | Régi hosztolt alapvonal, ami sok 2023-as oktatóanyagban megjelent. Ma nem választanám alapértelmezettnek új oktatóanyaghoz. |
| `text-embedding-3-small` | Modern hosztolt alapértelmezett, ha jó ár/érték arány kell és nem csak helyi embeddingek. |
| `text-embedding-3-large` | Hosztolt opció, ha a lekérés minősége fontosabb a vektorméret vagy embedding költségnél. |
| `BAAI/bge-small-en-v1.5` | Könnyű helyi angol alapvonal oktatóanyagokhoz, prototípusokhoz és CPU-barát kísérletekhez. |
| `BAAI/bge-base-en-v1.5` vagy `BAAI/bge-large-en-v1.5` | Nagyobb helyi angol modellek, ha jobb lekérés minőséget akarok és több számítást engedhetek meg. |
| `BAAI/bge-m3` | Többnyelvű vagy hosszabb kontextusú lekéréshez, főleg ha nem csak angol dokumentumok vannak. |
| `sentence-transformers/all-MiniLM-L6-v2` | Nagyon kicsi és gyors szemantikus kereső alapvonal. Hasznos ha a sebesség és egyszerűség a legfontosabb. |
| `nomic-embed-text-v1.5` | Nyílt helyi embedding opció, érdemes kipróbálni hosszabb kontextusú vagy hordozhatóságra fókuszáló rendszereknél. |

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

Majd minden darab kap egy embeddinget:

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

## 6. Tárold a vektorokat Qdrant helyi módban

Most létrehozunk egy memórián belüli Qdrant gyűjteményt és beszúrjuk a darabokat metaadatokkal.

> [!NOTE]
> A 2023-as oktatóanyagban FAISS-t használtam, mert az egyszerű és népszerű módja volt helyi hasonlóság alapú vektorkeresést bemutatni LangChain-nel. A FAISS ma is hasznos gyors helyi kísérletekhez. Ebben a 2026-os verzióban Qdrant-ot használok, mert szeretném, ha az oktatóanyag közelebb állna egy éles RAG rendszerhez. A Qdrant lehetővé teszi vektorok tárolását metaadatokkal együtt, mint forrás fájl, szakaszcím, dokumentum verzió és jogosultságok. Ez megkönnyíti a lekérést és előkészíti a példát szűréshez, hivatkozásokhoz és jövőbeni perzisztens vagy szerver-oldali telepítéshez.

A FAISS jó vektoralapú hasonlóság keresés bemutatására. A Qdrant jobb egy kis, de éles formájú RAG lekérő réteg bemutatására.

Néhány gyakorlati alternatíva:

| Vektortár / kereső réteg | Mikor gondolnám meg |
| --- | --- |
| Qdrant | Helyi prototípusokhoz, metaadat szűréshez, élesbarát vektorkereséshez és egyszerű Python munkafolyamathoz. |
| Chroma | Gyors helyi RAG kísérletekhez és jegyzetfüzetekhez, ahol az egyszerűség a legfontosabb. |
| FAISS | Könnyű helyi vektorkereséshez, ha csak hasonlóság keresés kell és külön metaadat kezelést bírok szétszórni. |
| Milvus | Nagyobb léptékű nyílt forráskódú vektorkeresés, ha a csapat hajlandó dedikált vektor adatbázist üzemeltetni. |
| Weaviate | Vektorkeresés sémával, metaadatokkal, hibrid kereséssel és menedzselt vagy önálló telepítési lehetőségekkel. |
| Azure AI Search | Vállalati RAG Azure-on, ha szükségem van kulcsszó keresésre, vektorkeresésre, hibrid lekérésre, szemantikus rangsorolásra, szűrésre, biztonságra és menedzselt működtetésre egy kereső rétegben. |
| PostgreSQL + pgvector | Csapatoknak, akik már PostgreSQL-t használnak, és közel akarják a vektorkeresést az alkalmazás adatokhoz. |

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

Majd beszúrjuk a pontokat:

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

Az én futásomban a gyűjtemény 8 vektort illesztett be.

Itt kezd a RAG rendszer ellenőrizhetővé válni. A vektor adatbázis nem csak vektorokat tárol; tárolja a bizonyíték szöveget és a hivatkozásokhoz szükséges metaadatokat.

## 7. Lekérünk jelölt darabokat

Most felteszem a kérdést és lekérem a jelölt darabokat.

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

Ekkor kiírom a lekért darabokat mielőtt választ generálnék. Ez fontos. Ha a lekérés hibás, a generálás csak elrejti a problémát folyékony szöveg mögé.

## 8. Adjunk hozzá könnyű újrarendezőt

Amikor először teszteltem a lekérési utat, a vektor hasonlóság önmagában megtalálta a kapcsolódó irányelvi tartalmat, de a legpontosabb szakasz nem mindig volt az első.

Így hozzáadtam egy kis helyi újrarendezőt. Ez extra súlyt adott, ha a kérdés szavai átfedik a szakasz címet és tartalmat.

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

Az újrarendezés után a tetején ez lett:

```text
school_ai_policy.md / Final Assignments
```

Ez volt a várt szakasz a teszt kérdéshez.

Ez volt a leghasznosabb tanulság az első megvalósításból. Még egy apró helyi példában is javult a lekérés minősége, amikor a vektor hasonlóságot más jelzéssel kombináltam.

## 9. Alkossunk megalapozott helyi választ

Az alapértelmezett útra egy átlátható helyi válaszkészítőt használok LLM helyett.

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

Ez nem végleges termék válasz generátor. Hibakereső eszköz. Bizonyítja, hogy a lekérés, metaadat és hivatkozás működik, mielőtt a modellvariabilitás bekerül.

## 10. Generálj helyi választ Ollama-val és Phi-4-mini-vel

Amint a lekérés működik, a jegyzetfüzet csak az utolsó válasz lépést cseréli le Ollama-ra és `phi4-mini:3.8b` modellre.

> [!NOTE]
> Az Ollama-nak csak az utolsó válaszgeneráló lépést kellene helyettesítenie. A dokumentum betöltése, darabolás, vektortárolás, lekérés, újrarendezés és hivatkozás összekapcsolás maradjon ugyanaz.

Először a jegyzet összeállít egy bizonyíték promptot a lekért darabokból:

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

Ehhez az oktatóanyaghoz a Microsoft Phi-4-mini családját ajánlom alapértelmezett helyi generálási opcióként Ollama-n keresztül. Az általam tesztelt modell neve Ollamaban:

```powershell
ollama pull phi4-mini:3.8b
```

Gyorsan ellenőrizheted, hogy a modell elérhető-e:

```powershell
ollama list
```

Majd állítsd be ezeket a változókat:

```powershell
Copy-Item .env.example .env
```

Nyisd meg a `.env` fájlt és kapcsold be a 2. sorozat Ollama értékeit:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

A jegyzetfüzet a `python-dotenv` segítségével betölti a `.env`-t a tárház gyökérből, majd ugyanazt a bizonyíték promptot küldi Ollama helyi `/api/chat` végpontjára streaming nélkül. Ha Ollama nincs futtatva vagy hiányzik a `SERIES2_OLLAMA_MODEL`, ez az ág átugrásra kerül.

> [!NOTE]
> Ezen a gépen a `phi4-mini:3.8b` kb. 2,49 GB modellfájlt töltött le. A futás során Ollama 3,3 GB betöltött modellméretet jelentett és az RTX 3060 Laptop GPU-t használta.

Ez az oktatóanyagnak két szintet ad:

1. Csak CPU-s determinisztikus válaszkészítő.
2. Helyi válaszgenerálás Ollama-val és Phi-4-mini-vel.

A lekérési cső mindkettőben ugyanaz marad.

## 11. Ellenőrzés eredménye

A jegyzetfüzetet helyben futtattam Windows-on Python 3.12.6-tal.

Telepített csomagok:

| Csomag | Verzió |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Jegyzet futtatás:

- Jegyzetfüzet: `notebooks/series-2-open-source-rag.ipynb`
- Futási eredmény: sikeres `nbclient`-tel
- Betöltött dokumentumok: 2
- Elkészített darabok: 8
- Qdrant gyűjtemény: `school_policy_local`
- Beszúrt vektorok: 8
- Embedding modell: `BAAI/bge-small-en-v1.5`
- Embedding méret: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Ezt a választ nem nevezném tökéletesnek. A megfelelő bizonyíték alapján válaszol, de a végső forrás sor kevésbé pontos, mint a determinisztikus hivatkozási forma. Ez hasznos a bemutatóban, mert világossá teszi a következő mérnöki kérdést: a válaszgenerálást is értékelni kell, nem csak a lekérést.

A legfőbb dolog, amit az ellenőrzés közben tanultam, hogy a lekérés minőségét ellenőrizni kell a válaszgenerálás előtt. Az embedding eredmény már hasznos volt, és a könnyű újrarangsoroló megbízhatóan hozta előre a várt irányelv szakaszt. Pontosan az ilyen kis rendszer viselkedést szeretném, hogy a bemutató feltárja ahelyett, hogy elrejtené.

## 12. Mi következik

A következő fejlesztés az, hogy összehasonlítsuk ezt a helyi beállítást az ugyanazzal az iskola irányelvi asszisztens forgatókönyv menedzselt Azure verziójával. A forgatókönyv rögzítése megkönnyíti az áldozatokat és előnyöket: beállítási komplexitás, lekérési vezérlés, azonosítás integrációja, operatív tulajdonjog és költség.

## 13. Hivatkozások

- [Qdrant Python kliens gyorsindítás](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant kliens GitHub tároló](https://github.com/qdrant/qdrant-client)
- [FastEmbed támogatott modellek](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embedding útmutató](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 modellkártya](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 modellkártya](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 modellkártya](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini modelloldal](https://ollama.com/library/phi4-mini)
- [Ollama Windows dokumentáció](https://docs.ollama.com/windows)
- [Ollama API streaming dokumentáció](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct modellkártya](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph áttekintés](https://docs.langchain.com/oss/python/langgraph)
- [Bevezetés a RAG-be - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Előző: [1. sorozat](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->