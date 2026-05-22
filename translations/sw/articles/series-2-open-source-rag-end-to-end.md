# Fundisha AI Kujibu Maswali Kulingana na Nyaraka Zako
## Mfululizo 2: Jenga Mfumo wa RAG wa Chanzo Huria wa Eneo Hilo Kuanzia mwanzoni Mwakani

![Mhimili wa mafunzo ya RAG wa chanzo huria wa eneo hilo](../../../assets/images/series-2-local-rag.svg)

> Makala hii hubadilisha mjadala wa usanifu wa Mfululizo 1 kuwa mafunzo ya RAG yanayoweza kuendeshwa kwa ndani eneo hilo. Lengo ni kujenga mtiririko mzima kwanza kwa data ya sampuli, bila akaunti ya wingu, na bila siri yoyote, halafu tumia msingi huo unaofanya kazi kufanya maamuzi bora ya usanifu baadaye.

Mfumo tutakaoujenga ni msaidizi mdogo wa sera za shule. Ninatumia nyaraka mbili za Markdown zenye eneo la maarifa, halafu nimepitia mtiririko mzima wa RAG: kugawanya vipande, uingizaji wa ndani, kuhifadhi vector za Qdrant, utafutaji, upangaji upya, muundo wa jibu unaojua chanzo, na uzalishaji wa hiari wa ndani kwa Ollama na Phi-4-mini.

Uratibu wa mfululizo: [Nyumbani kwa Hifadhidata](../README.md) | Awali: [Mfululizo 1 - RAG, Azure dhidi ya Mbadala za Chanzo Huria, na Wakati wa Kufanya Fine-Tuning](./series-1-rag-azure-open-source-fine-tuning.md)

Daftari la kumbukumbu: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Mahitaji: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Hii ni sehemu bora ya kuanza ikiwa unataka kuelewa mtiririko wa RAG kabla ya kuunda rasilimali za wingu. Njia ya chaguo-msingi huendeshwa hapa eneo la ndani kwa uingizaji wa CPU rafiki na bila siri.

## 1. Tunachojenga

Katika mafunzo ya 2023, nilianza na Azure kwa sababu lengo lilikuwa kuonyesha jinsi Azure AI Search na Azure OpenAI vilivyoweza kujibu maswali kutoka kwa nyaraka za PDF.

Kwa mfululizo huu wa 2026, nataka kuanza ngazi moja chini.

Kabla ya kutumia huduma zinazosimamiwa, nataka kujenga mfumo mdogo wa RAG eneo la ndani na kufanya kila hatua ionekane: kupakia nyaraka, kugawanya maandishi, kuhifadhi vector, kutafuta ushahidi, kupanga upya matokeo, na kurudisha jibu linalojua chanzo.

Mtazamo wa mfano ni msaidizi wa sera za shule. Mtumiaji anauliza:

```text
Can I use generative AI for my final assignment?
```

Mfumo haupaswi kujibu kutoka kwa kumbukumbu ya modeli ya jumla. Unapaswa kupata sehemu husika ya sera na kujibu kutoka kwa ushahidi huo.

Toleo kamili linaloweza kuendeshwa lipo katika [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Msimbo hapa chini unaonyesha hatua kuu ili makala iweze kusomwa kama mafunzo.

## 2. Sakinisha Mtegemezi wa Eneo Hilo

Tengeneza mazingira ya mtandao na usakinishe mahitaji ya Mfululizo 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Toleo la kwanza linatumia hali ya Qdrant ya ndani na FastEmbed. Mteja wa Python wa Qdrant unaunga mkono hali ya ndani ya kumbukumbu ndani ya kumbukumbu na `QdrantClient(":memory:")`, ambayo ni ya manufaa kwa mafunzo ya eneo la ndani na uthibitishaji wa aina ya CI. FastEmbed hutupa mfano halisi wa uingizaji wa ndani bila kuhitaji funguo za API za wingu.

Faili la mahitaji pia linajumuisha `python-dotenv` kwa sababu daftari linaweza hiari kusoma jina la modeli ya Ollama kutoka `.env`. Hakuna ufunguo wa Azure OpenAI au OpenAI API unahitajika kwa mafunzo haya ya eneo la ndani.

## 3. Pakia Nyaraka za Sampuli

Mkusanyiko wa sampuli ni mdogo kwa makusudi:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Katika daftari, napakia faili zote za Markdown kutoka `sample_data/`:

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

Nilikimbia daftari, lilipakia nyaraka 2. Hii ni ndogo kiasi cha kutosha kuchunguza kwa mkono, ambayo ni muhimu wakati wa kujenga toleo la kwanza la mtiririko wa RAG.

## 4. Gawanya Kwa Vichwa vya Markdown

Hatua inayofuata ni kugawanya nyaraka katika vipande.

Kwa mafundisho haya, ninatumia vichwa vya Markdown kama ishara ya muundo. Kichwa cha nyaraka huletwa na `#`, na kila kipande cha sehemu hutoka kwa `##`.

> [!NOTE]
> Kugawanya si ya ukubwa mmoja kwa wote. Katika mafundisho haya, ninatumia vichwa vya Markdown kwa sababu nyaraka za sampuli zina muundo wazi wa `#` na `##`. Kwa PDF, nyaraka za Word, slaidi, tiketi, au kurasa za wavuti, mkakati bora unaweza kutumia mipaka ya ukurasa, taarifa za muundo, sehemu za maana, mipaka ya tokeni, meza, au metadata. Muhimu ni kuchagua mkakati wa kugawanya unaohifadhi maana na ufuatiliaji wa chanzo kwa nyaraka zako.

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

Kisha natumia kwenye kila nyaraka:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Hili liliunda vipande 8 katika utekelezaji wangu wa ndani.

Nilipenda kuhusu hatua hii ni kwamba metadata ilikuwa tayari ya manufaa. Kila kipande kinajua `source`, `sectionHeading`, `documentVersion`, na `permissions` ya kidokezo. Hata katika mafunzo madogo, hii hufanya rejea na utafutaji unaojua ruhusa baadaye kuwa rahisi kuelewa.

## 5. Tengeneza Uingizaji wa Ndani

Kwa toleo la umma la kwanza, ninatumia `BAAI/bge-small-en-v1.5` kupitia FastEmbed.

Hii hufanya mafunzo haya ya eneo la ndani na rafiki kwa CPU, lakini bado inatumia mfano halisi wa uingizaji badala ya kazi ya kidokezo cha vector. Mara ya kwanza hupanua uzito wa modeli. Baadaye, daftari linaweza kutumia tena cache ya eneo la ndani.

> [!NOTE]
> Ninatumia `BAAI/bge-small-en-v1.5` kwa sababu ni mfano mwepesi wa uingizaji wa Kiingereza unaofanya kazi vizuri na FastEmbed na Qdrant kwa mafunzo ya eneo la ndani. Huunda vector za wima 384, ambayo hufanya mfano huu kuwa haraka na nafuu kuendesha kwa eneo la ndani. Hii sio chaguo pekee nzuri. Mwaka 2023, mafunzo mengi yalitumia modeli zilizo hoteledhwa kama `text-embedding-ada-002`. Leo, chaguzi mpya zilizohoteledhwa kama OpenAI `text-embedding-3-small` na `text-embedding-3-large`, na chaguzi za chanzo huria kama BGE, E5, MiniLM, Nomic Embed, na modeli za lugha nyingi kama `BAAI/bge-m3` ni chaguo zote zinazofaa kulingana na mzigo wa kazi. Katika utengenezaji, modeli sahihi ya uingizaji inapaswa kuchaguliwa kupitia tathmini ya utafutaji kwenye nyaraka zako mwenyewe.

Mbadala kadhaa za vitendo:

| Familia ya modeli | Wakati Ningezingatia |
| --- | --- |
| `text-embedding-ada-002` | Msingi wa zamani uliowekwa mwenyeji uliotokea katika mafunzo mengi ya enzi ya 2023. Sisingechukua kama chaguo-msingi kwa mafunzo mapya leo. |
| `text-embedding-3-small` | Chaguo-msingi cha kisasa kilicho hoteledhwa ninapotaka uwiano mzuri wa gharama/utendaji na sihitaji uingizaji wa ndani tu. |
| `text-embedding-3-large` | Chaguo lililo hoteledhwa wakati ubora wa utafutaji unahitajika zaidi kuliko ukubwa wa vector au gharama ya uingizaji. |
| `BAAI/bge-small-en-v1.5` | Msingi mwepesi wa Kiingereza wa eneo la ndani kwa mafunzo, miundo na majaribio rafiki kwa CPU. |
| `BAAI/bge-base-en-v1.5` au `BAAI/bge-large-en-v1.5` | Modeli kubwa za Kiingereza za eneo la ndani ninapohitaji ubora bora wa utafutaji na naweza kumudu kutumia kompyuta zaidi. |
| `BAAI/bge-m3` | Utaftajaji wa lugha nyingi au muktadha mrefu, hasa wakati nyaraka si za Kiingereza pekee. |
| `sentence-transformers/all-MiniLM-L6-v2` | Msingi mdogo na wa haraka wa utaftaji wa maana. Mzuri pale haraka na urahisi ni muhimu zaidi. |
| `nomic-embed-text-v1.5` | Chaguo la uingizaji wa eneo la ndani la chanzo huria lenye thamani ya kujaribu kwa muktadha mrefu au mipangilio inayolenga uhamishaji. |

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

Kisha kila kipande kinapata uingizaji:

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

## 6. Hifadhi Vector Katika Hali ya Ndani ya Qdrant

Sasa tunaunda mkusanyiko wa Qdrant wa ndani wa kumbukumbu na tukaingize vipande pamoja na metadata ya mzigo.

> [!NOTE]
> Katika mafunzo ya 2023, nilitumia FAISS kwa sababu ilikuwa njia rahisi na maarufu kuonyesha utaftaji wa kufanana kwa vector eneo la ndani kwa LangChain. FAISS bado ni nzuri kwa majaribio ya haraka ya eneo la ndani. Katika toleo hili la 2026, ninatumia Qdrant kwa sababu nataka mafunzo haya yaonekane karibu na mfumo wa RAG wa utengenezaji. Qdrant inaniruhusu kuhifadhi vector pamoja na metadata za mzigo kama faili la chanzo, kichwa cha sehemu, toleo la nyaraka, na ruhusa. Hii hufanya utafutaji kuwa rahisi kuchunguza na kuandaa mfano kwa kuchuja, rejea, na uenezaji wa baadaye wa kuhifadhi au kuendesha seva.

FAISS ni nzuri kuonyesha utaftaji wa vector unaofanana. Qdrant ni bora kuonyesha safu ndogo lakini ya mtindo wa utengenezaji wa RAG.

Mbadala kadhaa za vitendo:

| Hifadhi vector / safu ya utaftaji | Wakati Ningezingatia |
| --- | --- |
| Qdrant | Mifano ya ndani, kuchuja metadata, utaftaji wa vector rafiki kwa utengenezaji, na mtiririko rahisi wa Python. |
| Chroma | Majaribio ya haraka ya RAG ya ndani na daftari ambapo urahisi ni muhimu zaidi. |
| FAISS | Utaftaji mwepesi wa vector wa eneo la ndani ninapotakiwa utaftaji wa kufanana tu na naweza kusimamia metadata tofauti. |
| Milvus | Utaftaji wa vector wa chanzo huria katika kiwango kikubwa wakati timu iko tayari kuendesha hifadhidata ya vector maalum. |
| Weaviate | Utaftaji wa vector na schema, metadata, utaftaji mchanganyiko, na chaguo la usimamizi au mwenyeji wa mwenyewe. |
| Azure AI Search | RAG ya biashara kwenye Azure ninapotaka utaftaji wa maneno, utaftaji wa vector, ufuatiliaji mchanganyiko, kupanga muhimu kwa maana, kuchuja, usalama, na uendeshaji ulio simamiwa katika safu moja ya utaftaji. |
| PostgreSQL + pgvector | Timu tayari kutumia PostgreSQL zinapotaka utaftaji wa vector karibu na data ya programu. |

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

Kisha ingiza pointi:

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

Katika utekelezaji wangu, mkusanyiko uliingiza vector 8.

Hii ndio sehemu ambapo mfumo wa RAG unaanza kuweza kuchunguzwa. Hifadhidata ya vector haijihifadhi vector tu; inahifadhi maandishi ya ushahidi na metadata zinazohitajika kwa rejea.

## 7. Tafuta Vipande Vinavyowezekana

Sasa tunauliza swali na kupata vipande vinavyowezekana.

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

Katika hatua hii, ninachapisha vipande vilivyopatikana kabla ya kuzalisha jibu. Hii ni muhimu. Ikiwa utafutaji ni kosa, uzalishaji utatosea tatizo nyuma ya maandishi yenye mtiririko mzuri.

## 8. Ongeza Upangaji Upya Mwepesi wa Mzigo

Nilipojaribu njia ya utafutaji kwa mara ya kwanza, kufanana kwa vector peke yake kulipata maudhui ya sera yanayohusiana, lakini sehemu sahihi zaidi haikuwahi kuwa juu kabisa.

Hivyo niliongeza upangaji upya mdogo wa ndani. Hutoa uzito wa ziada mara maneno ya swali yanapovumiliana na kichwa cha sehemu na maudhui.

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

Baada ya upangaji upya, matokeo ya juu yalikuwa:

```text
school_ai_policy.md / Final Assignments
```

Hiyo ilikuwa sehemu iliyotarajiwa kwa swali la majaribio.

Hii ilikuwa masomo muhimu zaidi kutoka utekelezaji wa kwanza. Hata katika mfano mdogo wa ndani, ubora wa utafutaji uliboreshwa ninapochanganya kufanana kwa vector na ishara nyingine.

## 9. Tengeneza Jibu la Ndani lililo na Msingi

Kwa njia ya chaguo-msingi, ninatumia mtunzi wa jibu la eneo la ndani lililo wazi badala ya LLM.

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

Huu sio mtengeneza jibu wa mwisho uliokusudiwa. Ni chombo cha urekebishaji. Inathibitisha kuwa utafutaji, metadata, na muunganisho wa rejea hufanya kazi kabla ya kuongeza kubadilika kwa modeli.

## 10. Tengeneza Jibu la Ndani kwa Ollama na Phi-4-mini

Mara utafutaji unaporekebishwa, daftari linaweza kubadilisha hatua ya mwisho ya jibu kwa Ollama na `phi4-mini:3.8b`.

> [!NOTE]
> Ollama inapaswa kubadilisha tu hatua ya mwisho ya uzalishaji wa jibu. Kupakia nyaraka, kugawanya vipande, kuhifadhi vector, utafutaji, upangaji upya, na muunganisho wa rejea vinapaswa kubaki vile vile.

Kwanza, daftari linaunda msukumo wa ushahidi kutoka kwa vipande vilivyopatikana:

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

Kwa mafundisho haya, ninapendekeza familia ya Phi-4-mini ya Microsoft kupitia Ollama kama chaguo-msingi la uzalishaji wa eneo la ndani. Katika Ollama, jina la modeli niliyojaribu ni:

```powershell
ollama pull phi4-mini:3.8b
```

Unaweza haraka angalia kwamba modeli ipo:

```powershell
ollama list
```

Kisha weka vigezo hivi:

```powershell
Copy-Item .env.example .env
```

Fungua `.env` na toa alama ya makoma kwenye thamani za Mfululizo 2 za Ollama:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Daftari linapakia `.env` kutoka kwa mizizi ya hifadhidata na `python-dotenv`, halafu linatumia msukumo huo huo wa ushahidi kwa sehemu ya ndani `/api/chat` ya Ollama bila mtiririko. Ikiwa Ollama haiko hai au `SERIES2_OLLAMA_MODEL` haipo, njia hii inasimbuliwa.

> [!NOTE]
> Kwenye mashine hii, `phi4-mini:3.8b` ilipakuliwa takriban faili za modeli zenye ukubwa wa GB 2.49. Wakati wa utambuzi, Ollama iliripoti modeli yenye ukubwa wa GB 3.3 na kutumia GPU ya Laptop RTX 3060.

Hii hutoa ngazi mbili za mafunzo:

1. Mtunzi wa jibu la kisahihi kwa CPU tu.
2. Uzalishaji wa jibu wa eneo la ndani kwa Ollama na Phi-4-mini.

Mtiririko wa utafutaji unabaki ule ule kwa zote mbili.

## 11. Matokeo ya Uhakiki

Nilikimbia daftari eneo la ndani kwenye Windows kwa Python 3.12.6.

Vipakuliwa vilivyowekwa:

| Kifurushi | Toleo |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Utekelezaji wa daftari:

- Daftari: `notebooks/series-2-open-source-rag.ipynb`
- Matokeo ya utekelezaji: yamepitishwa na `nbclient`
- Nyaraka zilizopakiwa: 2
- Vipande vilivyoundwa: 8
- Mkusanyiko wa Qdrant: `school_policy_local`
- Vector zilizowekwa: 8
- Modeli ya uingizaji: `BAAI/bge-small-en-v1.5`
- Ukubwa wa uingizaji: 384
- Swali la urejeshaji: "Je, naweza kutumia AI ya kizazi kwa ajili ya kazi yangu ya mwisho?"
- Njia ya upangaji upya: upangaji upya wa maneno kwa ndani wa mwanga
- Chanzo kilichopatikana baada ya upangaji upya: `school_ai_policy.md`
- Sehemu iliyoongoza kutafutwa baada ya upangaji upya: `Kazi za Mwisho`
- Njia ya jibu la msingi: muundaji jibu wazi wa ndani
- Njia ya uzalishaji ya Ollama: imekamilika na `phi4-mini:3.8b`
- Ukubwa wa faili ya mfano wa Ollama: 2.49GB kwenye diski
- Ukubwa wa mfano wa Ollama uliyochomwa: 3.3GB kama ilivyoarifiwa na `ollama ps`
- Kupakia GPU: 100% GPU kama ilivyoarifiwa na `ollama ps`
- Kumbukumbu ya GPU iliyoshuhudiwa baada ya uzalishaji: takriban 3.5GB ya 6GB zilizo tumika kwenye RTX 3060 Laptop GPU
- Utekelezaji wa daftari na mfano wa FastEmbed uliohifadhiwa na uzalishaji wa Ollama umewezeshwa: ulipita kwa takriban sekunde 34 kupitia script ya uthibitisho

Jibu lililotolewa na Ollama lilikuwa:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Sisingesema jibu hili ni kamili. Linajibu kutoka kwa ushahidi sahihi, lakini mstari wa chanzo cha mwisho si sahihi kama muundo wa rejea wa wazi. Hii ni muhimu kuonyesha katika mafunzo kwani inafanya swali lijalo la uhandisi kuwa wazi: uzalishaji wa jibu unahitaji tathmini pia, si urejeshaji tu.

Kitu kikuu nilichojifunza wakati wa kuthibitisha hiki ni kwamba ubora wa urejeshaji unapaswa kuangaliwa kabla ya uzalishaji wa jibu. Matokeo ya embedding yalikuwa tayari ya manufaa, na upangaji upya mwepesi ulifanya sehemu ya sera inayotarajiwa ionekane kwanza kwa uhakika. Hilo ndilo tabia ndogo ya mfumo niliyotaka mafunzo yaonyeshe badala ya kuficha.

## 12. Nini Kifuatacho

Marekebisho yanayofuata ni kulinganisha usanidi huu wa ndani na toleo la Azure lililoendeshwa la hali ile ile ya msaidizi wa sera ya shule. Kuhifadhi hali fasta kutafanya iwe rahisi kuona makubaliano: ugumu wa usanidi, udhibiti wa urejeshaji, uunganishaji wa utambulisho, umiliki wa uendeshaji, na gharama.

## 13. Marejeleo

- [Mwongozo wa haraka wa mteja wa Qdrant Python](https://python-client.qdrant.tech/quickstart.html)
- [Hifadhi ya mteja wa Qdrant GitHub](https://github.com/qdrant/qdrant-client)
- [Mifano ya modeli zinazounga mkono FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Mwongozo wa embeddings wa OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Kadi ya mfano wa BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Kadi ya mfano wa BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Kadi ya mfano wa sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ukurasa wa mfano wa Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Nyaraka za Ollama Windows](https://docs.ollama.com/windows)
- [Nyaraka za utiririshaji wa API ya Ollama](https://docs.ollama.com/api/streaming)
- [Kadi ya mfano wa Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Muhtasari wa LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Utangulizi wa RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Iliyotangulia: [Mfululizo 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->