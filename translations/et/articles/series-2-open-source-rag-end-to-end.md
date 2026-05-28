# Õpeta tehisintellekt vastama küsimustele sinu dokumentide põhjal
## Seeria 2: Ehita kohalik avatud lähtekoodiga RAG-süsteem algusest lõpuni

![Kohaliku avatud lähtekoodiga RAG õppetöövoog](../../../assets/images/series-2-local-rag.svg)

> See artikkel võtab Seeria 1 arhitektuuri arutelu ning muudab selle jooksvaks kohalikuks RAG-õpetuseks. Eesmärk on esmalt ehitada täielik töövoog näitedatadega, ilma pilvekonto ja saladusteta, ning seejärel kasutada seda toimivat baasjoont paremate arhitektuuriliste otsuste tegemiseks hiljem.

Süsteem, mida me ehitame, on väike koolipoliitika assistent. Kasutan kahte kohalikku Markdown dokumenti teadmistebaasina ning käin läbi kogu RAG töövoo: tükeldamine, kohalikud manustused, Qdranti vektorite hoidla, päring, ümberjärjestamine, allikateadlik vastuse koostamine ning valikuliselt kohalik loomine Ollama ja Phi-4-mini abil.

Sarja navigeerimine: [Repositooriumi avaleht](../README.md) | Eelmine: [Seeria 1 - RAG, Azure vs Avatud Lähtekoodiga Alternatiivid ja Millal Häälestamine Mõistlik on](./series-1-rag-azure-open-source-fine-tuning.md)

Sülearvut: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Nõuded: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> See on parim lähtekoht, kui soovid mõista RAG töövoogu enne pilveressursside loomist. Vaikimisi töötab see kohapeal CPU-sõbralike manustustega ja ilma saladusteta.

## 1. Mida me ehitame

2023. aasta õppetöös alustasin Azuriga, sest eesmärk oli näidata, kuidas Azure AI Search ja Azure OpenAI suudavad vastata küsimustele PDF-dokumentidest.

Selles 2026. aasta seerias tahan alustada ühe taseme võrra madalamalt.

Enne hallatavate teenuste kasutamist soovin ehitada väikese RAG-süsteemi lokaalselt ja teha iga samm nähtavaks: dokumentide laadimine, teksti tükeldamine, vektorite salvestamine, tõendite päring, tulemuste ümberjärjestamine ja allikateadlik vastuse tagastamine.

Näidisstsenaariumiks on koolipoliitika assistent. Kasutaja küsib:

```text
Can I use generative AI for my final assignment?
```

Süsteem ei tohi vastata mudeli üldmälu põhjal. Ta peab otsima asjakohase poliitikasektsiooni ja vastama selle tõendite põhjal.

Täielik jooksev versioon on [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Allolev kood näitab põhietappe, et artikkel oleks loetav kuiõpetus.

## 2. Paigalda kohalikud sõltuvused

Loo virtuaalne keskkond ja paigalda Seeria 2 nõuded:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Esimene versioon kasutab Qdranti kohalikku režiimi ja FastEmbedi. Qdranti Python kliendi mäluplokkide lokaliseeritud režiimit toetab `QdrantClient(":memory:")` abil, mis on kasulik kohalikeks õppetöödeks ja CI-tüüpi kontrollimiseks. FastEmbed annab meile päris kohaliku manustuse mudeli, ilma et oleks vaja pilve API võtit.

Nõuete fail sisaldab ka `python-dotenv`'i, sest sülearvuti võib valikuliselt lugeda Ollama mudeli nime failist `.env`. Azure OpenAI ega OpenAI API võtit ei ole selle kohaliku õppetöö jaoks vaja.

## 3. Laadi näidisdokumendid

Näidiskorpus on tahtlikult väike:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Sülearvutis laen kõiki Markdown faile kaustast `sample_data/`:

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

Kui käivitasin sülearvuti, laeti 2 dokumenti. See on piisavalt väike, et käsitsi üle vaadata, mis on kasulik esimese RAG torujuhtme versiooni ehitamisel.

## 4. Tükelda Markdown päiste järgi

Järgmine samm on dokumendid tükeldada.

Selles õppes kasutan Markdown päiseid struktuurisignaali jaoks. Dokumendi pealkiri tuleb `#` alt ning iga sektsiooni tükk päisest `##`.

> [!NOTE]
> Tükeldamine ei sobi kõigile olukordadele ühtmoodi. Selles õpetuses kasutan Markdown päiseid, sest näidisdokumentidel on selged `#` ja `##` struktuurid. PDF-ide, Word dokumentide, slaidide, piletite või veebilehtede korral võib parem strateegia kasutad leheküljepiire, paigutusteavet, semantilisi sektsioone, tokenipiiranguid, tabeleid või metadate. Tähtis on valida tükeldamisstrateegia, mis säilitab dokumentide tähenduse ja allikajälgitavuse.

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

Seejärel rakendan seda igale dokumendile:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Minu kohalikus jooksus loodi 8 tükki.

Mulle meeldis selle sammu juures see, et metainfo on juba kasulik. Iga tükk teab oma `source`, `sectionHeading`, `documentVersion` ja kohakuva `permissions` väärtust. Isegi väikeses õpetuses teeb see tsitaatide ja hilisema õigustele vastava päringu paremini mõistetavaks.

## 5. Loo kohalikud manustused

Esimeses avalikus versioonis kasutan `BAAI/bge-small-en-v1.5` FastEmbed kaudu.

See hoiab õppetöö kohaliku ja CPU-sõbralikuna, kuid kasutab siiski päris manustuse mudelit, mitte kohatäite vektorifunktsiooni. Esimene jooks alla laadib mudeli kaalud. Pärast seda saab sülearvuti uuesti kasutada kohalikku vahemälu.

> [!NOTE]
> Kasutan `BAAI/bge-small-en-v1.5`, sest see on kergekaaluline ingliskeelne manustuse mudel, mis töötab hästi koos FastEmbed ja Qdrantiga kohaliku õppetöö jaoks. See loob 384-mõõtmelised vektorid, mis hoiab näite kiire ja odavana kohaliku jooksu jaoks. See ei ole ainus hea valik. 2023. aastal kasutasid paljud õppetööd majutatud manustuse mudeleid nagu `text-embedding-ada-002`. Täna on uued majutatud variandid nagu OpenAI `text-embedding-3-small` ja `text-embedding-3-large`, samuti avatud lähtekoodiga valikud nagu BGE, E5, MiniLM, Nomic Embed ja mitmekeelsed mudelid nagu `BAAI/bge-m3` kõik mõistlikud valikud sõltuvalt töökoormusest. Tootmises tuleks sobiv manustuse mudel valida läbi päringu hindamise oma dokumentide peal.

Mõned praktilised alternatiivid:

| Mudeli perekond | Millal ma kaaluksin |
| --- | --- |
| `text-embedding-ada-002` | Vanem majutatud baasliin, mis ilmus paljudes 2023. aasta õppetöödes. Täna ei valiks seda uusima õpetuse vaikimisi. |
| `text-embedding-3-small` | Moodne majutatud vaikimisi, kui tahan head hinna ja jõudluse tasakaalu ega vaja vaid kohalikku manustust. |
| `text-embedding-3-large` | Majutatud valik, kui päringu kvaliteet on olulisem kui vektori suurus või manustuse hind. |
| `BAAI/bge-small-en-v1.5` | Kergekaaluline kohalik ingliskeelne baasliin õppetööde, prototüüpide ja CPU-sõbralike katsete jaoks. |
| `BAAI/bge-base-en-v1.5` või `BAAI/bge-large-en-v1.5` | Suuremad kohalikud ingliskeelsed mudelid, kui tahan paremat päringu kvaliteeti ja saan lubada rohkem arvutusressurssi. |
| `BAAI/bge-m3` | Mitmekeelne või pikema kontekstiga päring, eriti kui dokumendid ei ole ainult inglise keeles. |
| `sentence-transformers/all-MiniLM-L6-v2` | Väga väike ja kiire semantilise otsingu baasliin. Kasulik, kui kiirus ja lihtsus on kõige tähtsamad. |
| `nomic-embed-text-v1.5` | Avatud kohalik manustuse valik, mida tasub testida pikema konteksti või kaasaskantavuse jaoks. |

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

Seejärel saab iga tükk manustuse:

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

## 6. Salvestage vektorid Qdranti kohalikus režiimis

Nüüd loome mälus oleva Qdranti kollektsiooni ja sisestame tükid koos metadata koormusega.

> [!NOTE]
> 2023. aasta õppetöös kasutasin FAISSi, sest see oli lihtne ja populaarne viis näidata kohalikku vektorite sarnasuse otsingut LangChainiga. FAISS on endiselt kasulik kiirete kohalike katsete jaoks. Selles 2026. aasta versioonis kasutan Qdranti, sest tahan, et õppetöö tunduks rohkem tootmissaadusliku RAG süsteemina. Qdrant võimaldab mul salvestada vektoreid koos metadata koormusega nagu lähtefail, sektsiooni pealkiri, dokumendi versioon ja õigused. See teeb päringu lihtsamini kontrollitavaks ning valmistab näite ette filtreerimiseks, tsitaatideks ja tulevaseks püsivaks või serveripõhiseks juurutamiseks.

FAISS on suurepärane vektorite sarnasuse otsingu demonstreerimiseks. Qdrant on parem väikse, kuid tootmiskujuga RAG päringukihi näitamiseks.

Mõned praktilised alternatiivid:

| Vektori hoidla / otsingukiht | Millal ma kaaluksin |
| --- | --- |
| Qdrant | Kohalikud prototüübid, metadata filterdus, tootmiskõlblik vektorite otsing ja lihtne Python töövoog. |
| Chroma | Kiired kohalikud RAG katsed ja sülearvutid, kus lihtsus on kõige tähtsam. |
| FAISS | Kergekaaluline kohalik vektorite otsing, kui vajan vaid sarnasuse otsingut ja metadata haldan eraldi. |
| Milvus | Suurem avatud lähtekoodiga vektorite otsing, kui tiim on valmis opereerima pühendatud vektoriandmebaasi. |
| Weaviate | Vektorite otsing skeemi, metadata, hübriidotsingu ja hallatavate või isehostitud juurutusvõimalustega. |
| Azure AI Search | Ettevõtte RAG Azure’is, kui tahan ühte otsingukihti märksõna otsingu, vektorite otsingu, hübriidpäringu, semantilise järjestuse, filtreerimise, turvalisuse ja hallatud operatsioonidega. |
| PostgreSQL + pgvector | Tiimidele, kes juba kasutavad PostgreSQL-i ja soovivad vektorite otsingut rakendusaineandmetele lähedal. |

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

Seejärel sisesta punktid:

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

Minu jooksus sisestati 8 vektorit.

Siin hakkab RAG süsteem muutuma kontrollitavaks. Vektorite andmebaas ei hoia mitte ainult vektoreid, vaid ka tõenditeksti ja tsitaatide jaoks vajalikku metadatat.

## 7. Päringu kandidaatide täbiboksude valimine

Nüüd esitame küsimuse ja pärime kandidaattükid.

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

Selles punktis prindin päritud tükid enne vastuse genereerimist. See on oluline. Kui päring on vale, siis genereerimine varjab probleemi vaid sujuva teksti taha.

## 8. Lisa kergekaaluline ümberjärjestaja

Kui ma esimest korda testisin päringuteed, leidis vektori sarnasus seotud poliitika sisu, kuid kõige täpsem sektsioon ei olnud alati esimesel kohal.

Seega lisasin väikese kohaliku ümberjärjestaja. See annab täiendava kaalu, kui küsimuse terminid kattuvad sektsiooni päise ja sisu sõnadega.

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

Pärast ümberjärjestamist sai tipptulemus:

```text
school_ai_policy.md / Final Assignments
```

See oli testküsimuse jaoks oodatud sektsioon.

See oli kõige kasulikum õppetund esimesest implementeerimisest. Isegi väikese kohaliku näite juures paranes päringu kvaliteet, kui ma ühendasin vektorite sarnasuse teise signaaliga.

## 9. Koosta põhjendatud kohalik vastus

Vaikimisi tee jaoks kasutan läbipaistvat kohalikku vastuse koostajat, mitte LLM-i.

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

See ei ole mõeldud kui lõplik vastuse generaator toodetele. See on silumise tööriist. See tõestab, et päring, metainfo ja tsitaatide ühendamine toimivad enne mudeli variatiivsuse lisamist.

## 10. Genereeri kohalik vastus Ollama ja Phi-4-mini abil

Kui päring töötab, võib sülearvuti asendada vaid lõpliku vastuse sammu Ollama ja `phi4-mini:3.8b` mudeliga.

> [!NOTE]
> Ollama peaks asendama ainult lõpliku vastuse genereerimise sammu. Dokumentide laadimine, tükeldamine, vektorite hoidmine, päring, ümberjärjestamine ja tsitaatide ühendamine peaksid jääma samaks.

Esmalt koostab sülearvuti päritud tükkidest tõendipõhise sisendi:

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

Selles õppes soovitan Microsofti Phi-4-mini perekonda läbi Ollama vaikimisi kohaliku generatsiooni valikuna. Ollamas on mudelinimi, mida ma testisin:

```powershell
ollama pull phi4-mini:3.8b
```

Saa kiiresti kinnitust, et mudel on olemas:

```powershell
ollama list
```

Seejärel määra need muutujad:

```powershell
Copy-Item .env.example .env
```

Ava `.env` ja eemalda kommentaarid Seeria 2 Ollama väärtustelt:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Sülearvuti loeb `.env` faili hoidla juurest kasutades `python-dotenv` ja saadab sama tõendusliku sisendi Ollama kohalikule `/api/chat` lõpp-punktile voogesituseta. Kui Ollama ei tööta või `SERIES2_OLLAMA_MODEL` puudub, see rada jääb vahele.

> [!NOTE]
> Sellel masinal laadis `phi4-mini:3.8b` umbes 2.49GB mudelifaile. Järelduse käigus teatas Ollama, et laaditud mudeli suurus oli 3.3GB ning kasutas RTX 3060 sülearvuti GPU-d.

See annab õppetööle kaks taset:

1. CPU-põhine deterministlik vastuste koostaja.
2. Kohalik vastuste genereerimine Ollama ja Phi-4-mini abil.

Päringu torujuhe jääb mõlemal samaks.

## 11. Kontrolltulemus

Jooksutasin sülearvutit lokaalselt Windowsil Python 3.12.6-ga.

Paigaldatud paketid:

| Pakett | Versioon |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Sülearvuti täitmine:

- Sülearvuti: `notebooks/series-2-open-source-rag.ipynb`
- Täitmise tulemus: edukas `nbclient` abil
- Laetud dokumendid: 2
- Loodud tükid: 8
- Qdranti kollektsioon: `school_policy_local`
- Sisestatud vektorid: 8
- Manustuse mudel: `BAAI/bge-small-en-v1.5`
- Manustuse suurus: 384
- Taastamisküsimus: "Kas ma võin kasutada generatiivset tehisintellekti oma lõputöö jaoks?"
- Taaskorrigeerimise tee: kergekaaluline kohalik leksikaline taaskorrigeerimine
- Pärast taaskorrigeerimist leitud parim allikas: `school_ai_policy.md`
- Pärast taaskorrigeerimist leitud parim jaotis: `Lõputööd`
- Vaikimisi vastuse tee: kohalik läbipaistev vastusekomponist
- Ollama generatsiooni tee: lõpetatud mudeliga `phi4-mini:3.8b`
- Ollama mudeli faili suurus: 2.49GB kettal
- Ollama laaditud mudeli suurus: 3.3GB, reported by `ollama ps`
- GPU laadimine: 100% GPU, reported by `ollama ps`
- GPU mälu kasutus pärast generatsiooni: umbes 3.5GB 6GB-st RTX 3060 sülearvuti GPU-l
- Märkmiku täitmine vahemäluga FastEmbed mudeliga ja Ollama generatsiooniga lubatud: õnnestus umbes 34 sekundiga läbi kontrollskripti

Ollama genereeritud vastus oli:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Ma ei nimetaks seda vastust täiuslikuks. Vastus põhineb õigel tõendil, kuid lõplik allikaleht on vähem täpne kui deterministlik tsitaadiformaat. See on kasulik näidata juhendis, sest see teeb järgmiseks inseneriküsimuseks ilmseks: vastuste genereerimist tuleb samuti hinnata, mitte ainult andmete taaskorraldamist.

Peamine, mida ma kontrollimise käigus õppisin, oli see, et taaskorraldamise kvaliteeti tuleks kontrollida enne vastuste genereerimist. Manustustulemus oli juba kasulik ja kergekaaluline taaskorrigeerija tegi ootuspäraselt poliitika jaotise usaldusväärselt esimeseks. Just sellist väikest süsteemikäitumist tahan juhend kuvada, mitte varjata.

## 12. Mis Järgmiseks

Järgmine parendus on võrrelda seda kohalikku seadistust hallatud Azure’i versiooniga samas koolipoliitika abistaja stsenaariumis. Stsenaariumi fikseerimine peaks lihtsustama kompromisside nägemist: seadistuse keerukus, taaskorraldamise kontrollid, identiteedi integreerimine, tegevuse omandiõigus ja kulud.

## 13. Viited

- [Qdrant Python kliendi kiire algus](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant kliendi GitHub hoidla](https://github.com/qdrant/qdrant-client)
- [FastEmbedi toetatud mudelid](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embedimise juhend](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 mudelikaart](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 mudelikaart](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 mudelikaart](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini mudelileht](https://ollama.com/library/phi4-mini)
- [Ollama Windowsi dokumentatsioon](https://docs.ollama.com/windows)
- [Ollama API voogedastuse dokumentatsioon](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct mudelikaart](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph ülevaade](https://docs.langchain.com/oss/python/langgraph)
- [Sissejuhatus RAG-sse - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Eelmine: [Seeria 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->