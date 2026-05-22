# Naučite AI odgovarati na pitanja temeljem vaših dokumenata
## Serija 2: Izgradite lokalni RAG sustav otvorenog koda od početka do kraja

![Lokalni open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Ovaj članak pretvara raspravu o arhitekturi iz Serije 1 u pokretni lokalni RAG tutorial. Cilj je prvo izgraditi cijeli tijek rada s primjerom podataka, bez računa u oblaku i bez tajni, a zatim upotrijebiti tu radnu osnovu za donošenje boljih arhitektonskih odluka kasnije.

Sustav koji ćemo izgraditi je mali asistent za školsku politiku. Koristim dva lokalna Markdown dokumenta kao bazu znanja, zatim prolazim kroz cijeli RAG tijek rada: dijeljenje na dijelove, lokalne ugradnje, Qdrant pohranu vektora, dohvaćanje, ponovno rangiranje, odgovaranje svjesno izvora i opcionalnu lokalnu generaciju s Ollama i Phi-4-mini.

Navigacija serijom: [Početna stranica repozitorija](../README.md) | Prethodno: [Serija 1 - RAG, Azure vs alternative otvorenog koda i kada ima smisla fino podešavanje](./series-1-rag-azure-open-source-fine-tuning.md)

Bilježnica: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Zahtjevi: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Ovo je najbolja polazna točka ako želite razumjeti RAG tijek prije kreiranja resursa u oblaku. Zadani put radi lokalno s CPU-prijateljskim ugradnjama i bez tajni.

## 1. Što gradimo

U tutorialu iz 2023. krenuo sam od Azure jer je cilj bio pokazati kako Azure AI Search i Azure OpenAI mogu odgovarati na pitanja iz PDF dokumenata.

Za ovu seriju 2026. želim krenuti jednu razinu niže.

Prije korištenja upravljanih usluga, želim izgraditi mali lokalni RAG sustav i učiniti svaki korak vidljivim: učitavanje dokumenata, dijeljenje teksta na dijelove, pohrana vektora, dohvaćanje dokaza, ponovno rangiranje rezultata i vraćanje odgovora svjesnog izvora.

Primjer scenarija je asistent za školsku politiku. Korisnik pita:

```text
Can I use generative AI for my final assignment?
```

Sustav ne bi trebao odgovarati iz općeg modelnog pamćenja. Trebao bi dohvatiti relevantan odjeljak politike i odgovoriti na temelju tog dokaza.

Cijela izvodiva verzija nalazi se u [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Donji kod prikazuje glavne korake kako bi se članak mogao čitati kao tutorial.

## 2. Instalirajte lokalne ovisnosti

Stvorite virtualno okruženje i instalirajte zahtjeve Serije 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Prva verzija koristi Qdrant lokalni način rada i FastEmbed. Qdrantov Python klijent podržava lokalni način rada u memoriji s `QdrantClient(":memory:")`, što je korisno za lokalne tutoriale i CI-ovsku provjeru. FastEmbed nam daje pravi lokalni model ugradnje bez potrebe za API ključem oblaka.

Datoteka s zahtjevima također uključuje `python-dotenv` jer bilježnica može opcionalno učitati naziv Ollama modela iz `.env`. Za ovaj lokalni tutorial nije potreban Azure OpenAI ni OpenAI API ključ.

## 3. Učitajte primjere dokumenata

Primjer korpusa je namjerno malen:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

U bilježnici učitavam sve Markdown datoteke iz `sample_data/`:

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

Kad sam pokrenuo bilježnicu, učitala je 2 dokumenta. To je dovoljno malo da se može ručno pregledati, što je korisno kod izgradnje prve verzije RAG tijeka.

## 4. Dijeljenje prema Markdown naslovima

Sljedeći je korak podijeliti dokumente na dijelove.

Za ovaj tutorial koristim Markdown naslove kao signal strukture. Naslov dokumenta dolazi od `#`, a svaki odjeljak dolazi od `##`.

> [!NOTE]
> Dijeljenje nije univerzalno. U ovom tutorijalu koristim Markdown naslove jer uzorci dokumenata imaju jasnu `#` i `##` strukturu. Za PDF-ove, Word dokumente, prezentacije, tikete ili web stranice, bolja strategija može koristiti granice stranica, informacijama o rasporedu, semantičkim odjeljcima, ograničenjima tokena, tablicama ili metapodacima. Važno je odabrati strategiju dijeljenja koja čuva značenje i mogućnost traga za izvorom vaših dokumenata.

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

Zatim je primijenjujem na svaki dokument:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

To je kreiralo 8 dijelova u mojoj lokalnoj izvedbi.

Svidjelo mi se što su metapodaci već korisni. Svaki dio zna svoj `source`, `sectionHeading`, `documentVersion` i privremenu vrijednost `permissions`. Čak i u malom tutorialu, to olakšava navođenje i kasnije dohvaćanje svjesno dopuštenja.

## 5. Izradite lokalne ugradnje

Za prvu javnu verziju koristim `BAAI/bge-small-en-v1.5` preko FastEmbed.

Time tutorial ostaje lokalni i prijateljski prema CPU-u, ali još uvijek koristi pravi model ugradnje umjesto lažne funkcije vektora. Prvo pokretanje preuzima težine modela. Nakon toga bilježnica može koristiti lokalni predmemoriju.

> [!NOTE]
> Koristim `BAAI/bge-small-en-v1.5` jer je lagani engleski model ugradnje koji dobro radi s FastEmbed i Qdrantom za lokalni tutorial. Stvara 384-dimenzionalne vektore, što održava primjer brzim i jeftinim za lokalni rad. Ovo nije jedini dobar izbor. Godine 2023. mnogi su tutoriali koristili hostirane modele ugradnje poput `text-embedding-ada-002`. Danas su novije hostirane opcije poput OpenAI `text-embedding-3-small` i `text-embedding-3-large`, te open-source opcije poput BGE, E5, MiniLM, Nomic Embed i višeznačni modeli poput `BAAI/bge-m3` svi razumna mogućnost ovisno o opterećenju. U produkciji, pravi model ugradnje treba odabrati kroz evaluaciju dohvaćanja na vlastitim dokumentima.

Neke praktične alternative:

| Obitelj modela | Kada bih je razmotrio |
| --- | --- |
| `text-embedding-ada-002` | Starija hostirana osnova koja se često pojavljivala u tutorialima iz 2023. Danas je ne bih odabrao za zadani model u novom tutorijalu. |
| `text-embedding-3-small` | Moderan hostirani zadani model ako želim dobar omjer cijene i performansi i ne trebam lokalno jedine ugradnje. |
| `text-embedding-3-large` | Hostirana opcija kad kvaliteta dohvaćanja ima veći značaj od veličine vektora ili troška ugradnje. |
| `BAAI/bge-small-en-v1.5` | Lagana lokalna engleska osnova za tutoriale, prototipove i CPU-prijateljske eksperimente. |
| `BAAI/bge-base-en-v1.5` ili `BAAI/bge-large-en-v1.5` | Veći lokalni engleski modeli ako želim bolju kvalitetu dohvaćanja i mogu si priuštiti više računske snage. |
| `BAAI/bge-m3` | Višeznačni ili za dohvaćanje duljeg konteksta, naročito ako dokumenti nisu samo na engleskom. |
| `sentence-transformers/all-MiniLM-L6-v2` | Vrlo mali i brz semantički pretraživački model. Koristan kad su brzina i jednostavnost najvažniji. |
| `nomic-embed-text-v1.5` | Otvorena lokalna opcija ugradnje vrijedna ispitivanja za konfiguracije s dužim kontekstom ili fokusirane na prenosivost. |

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

Zatim svaki dio dobiva ugradnju:

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

## 6. Pohranite vektore u Qdrant lokalni način

Sada stvaramo Qdrant kolekciju u memoriji i umetnemo dijelove s metapodacima.

> [!NOTE]
> U tutorialu iz 2023. koristio sam FAISS jer je bio jednostavan i popularan način demonstracije lokalnog pretraživanja vektorske sličnosti s LangChain. FAISS je i dalje koristan za brze lokalne eksperimente. U ovoj verziji 2026. koristim Qdrant zato što želim da tutorial bude bliži produkcijskom RAG sustavu. Qdrant mi dozvoljava pohranu vektora zajedno s metapodacima poput izvora datoteke, naslova odjeljka, verzije dokumenta i dopuštenja. To olakšava pregled dohvaćanja i priprema primjer za filtriranje, citate i buduću trajnu ili serversku implementaciju.

FAISS je izvrstan za pokazivanje pretraživanja sličnosti vektora. Qdrant je bolji za pokazivanje male, ali produkcijski oblikovane RAG sloja dohvaćanja.

Neke praktične alternative:

| Sloj za pohranu / pretraživanje vektora | Kada bih ga razmotrio |
| --- | --- |
| Qdrant | Lokalni prototipovi, filtriranje metapodataka, produkcijski vektorski pretraživač i jednostavan Python tijek rada. |
| Chroma | Brzi lokalni RAG eksperimenti i bilježnice gdje najviše vrijedi jednostavnost. |
| FAISS | Lagani lokalni vektorski pretraživač kad mi treba samo pretraživanje sličnosti i metapodaci se zasebno upravljaju. |
| Milvus | Otvoreni vektorski pretraživač većih razmjera kad je tim spreman za upravljanje posvećenom bazom vektora. |
| Weaviate | Vektorsko pretraživanje sa shemom, metapodacima, hibridnim pretraživanjem i opcijama upravljanog ili samostalnog hostanja. |
| Azure AI Search | Enterprise RAG na Azureu kad želim pretraživanje po ključnim riječima, vektorsko pretraživanje, hibridno dohvaćanje, semantičko rangiranje, filtriranje, sigurnost i upravljane operacije u jednom sloju pretraživanja. |
| PostgreSQL + pgvector | Timovi koji već koriste PostgreSQL i žele pretraživanje vektora blizu podataka aplikacije. |

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

Zatim umetnite točke:

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

U mojoj izvedbi kolekcija je umetnula 8 vektora.

Ovdje RAG sustav počinje biti pregledan. Baza podataka vektora ne pohranjuje samo vektore; pohranjuje i tekst dokaza te metapodatke potrebne za citate.

## 7. Dohvati kandidate za dijelove

Sada postavljamo pitanje i dohvaćamo kandidate za dijelove.

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

U ovom trenutku ispisujem dohvaćene dijelove prije generiranja odgovora. To je važno. Ako je dohvaćanje pogrešno, generacija će samo sakriti problem iza tečnog teksta.

## 8. Dodajte lagani ponovno-rangirač

Kad sam prvi put testirao put dohvaćanja, vektorska sličnost je sama po sebi pronalazila povezani sadržaj politike, ali najprecizniji odjeljak nije uvijek bio na vrhu.

Stoga sam dodao mali lokalni ponovno-rangirač. Daje dodatnu težinu kad se pojmovi iz pitanja preklapaju s naslovom odjeljka i sadržajem.

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

Nakon ponovnog rangiranja, najbolji rezultat je postao:

```text
school_ai_policy.md / Final Assignments
```

To je bio očekivani odjeljak za testno pitanje.

Ovo je bila najkorisnija lekcija iz prve implementacije. Čak i u malenoj lokalnoj demonstraciji, kvaliteta dohvaćanja se poboljšala kad sam kombinirao vektorsku sličnost s dodatnim signalom.

## 9. Sastavite lokalni odgovor s utemeljenjem

Za zadani put koristim transparentni lokalni sastavljač odgovora umjesto LLM-a.

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

Ovo nije namijenjeno kao konačni generator odgovora proizvoda. To je alat za otklanjanje pogrešaka. Dokazuje da dohvaćanje, metapodaci i povezivanje izvora funkcioniraju prije dodavanja varijabilnosti modela.

## 10. Generirajte lokalni odgovor s Ollama i Phi-4-mini

Kad dohvaćanje radi, bilježnica može zamijeniti samo zadnji korak generiranja odgovora s Ollama i `phi4-mini:3.8b`.

> [!NOTE]
> Ollama bi trebala zamijeniti samo zadnji korak generiranja odgovora. Učitavanje dokumenata, dijeljenje, pohrana vektora, dohvaćanje, ponovno rangiranje i povezivanje izvora trebaju ostati isti.

Prvo bilježnica gradi upit za dokaze iz dohvaćenih dijelova:

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

Za ovaj tutorial preporučam Microsoftovu obitelj Phi-4-mini preko Ollama kao zadanu lokalnu opciju generacije. U Ollama, model koji sam testirao je:

```powershell
ollama pull phi4-mini:3.8b
```

Brzo možete provjeriti je li model dostupan:

```powershell
ollama list
```

Zatim postavite ove varijable:

```powershell
Copy-Item .env.example .env
```

Otvorite `.env` i ukonite komentar za Seriju 2 Ollama vrijednosti:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Bilježnica učitava `.env` iz korijena repozitorija pomoću `python-dotenv`, zatim šalje isti upit za dokaze Ollama lokalnoj `/api/chat` krajnjoj točki s onemogućenim strujanjem. Ako Ollama nije pokrenuta ili `SERIES2_OLLAMA_MODEL` nedostaje, ovaj put se preskače.

> [!NOTE]
> Na ovom računalu, `phi4-mini:3.8b` je preuzeo oko 2.49GB datoteka modela. Tijekom izvođenja, Ollama je prijavila učitanu veličinu modela od 3.3GB i koristila RTX 3060 Laptop GPU.

To daje tutorialu dvije razine:

1. Deterministički sastavljač odgovora samo za CPU.
2. Lokalnu generaciju odgovora s Ollama i Phi-4-mini.

Tijek dohvaćanja ostaje isti u oba slučaja.

## 11. Rezultat provjere

Pokrenuo sam bilježnicu lokalno na Windowsu s Python 3.12.6.

Instalirani paketi:

| Paket | Verzija |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Izvršenje bilježnice:

- Bilježnica: `notebooks/series-2-open-source-rag.ipynb`
- Rezultat izvršenja: uspješno s `nbclient`
- Učitani dokumenti: 2
- Kreirani dijelovi: 8
- Qdrant kolekcija: `school_policy_local`
- Umetnuti vektori: 8
- Model ugradnje: `BAAI/bge-small-en-v1.5`
- Veličina ugradnje: 384
- Pitanje za dohvat: "Mogu li koristiti generativnu umjetnu inteligenciju za svoj završni zadatak?"
- Put preuređivanja: lagano lokalno leksičko preuređivanje
- Najbolji dohvaćeni izvor nakon preuređivanja: `school_ai_policy.md`
- Najbolji dohvaćeni odjeljak nakon preuređivanja: `Final Assignments`
- Zadani put odgovora: lokalni transparentni tvorac odgovora
- Put generiranja Ollama: dovršeno s `phi4-mini:3.8b`
- Veličina Ollama modela na disku: 2.49GB
- Veličina učitanog Ollama modela: 3.3GB, prijavljeno od strane `ollama ps`
- GPU iskorištenje: 100% GPU, prijavljeno od strane `ollama ps`
- Promatrana GPU memorija nakon generiranja: oko 3.5GB od 6GB na RTX 3060 Laptop GPU
- Izvršavanje bilježnice s predmemoriranim FastEmbed modelom i omogućenim Ollama generiranjem: prošlo za oko 34 sekunde putem skripte za provjeru

Ollama-generirani odgovor bio je:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Ne bih ovaj odgovor nazvao savršenim. Odgovara na temelju pravih dokaza, ali zadnja linija izvora manje je precizna od determinističkog formata citata. To je korisno pokazati u vodiču jer time sljedeće inženjersko pitanje postaje očito: generiranje odgovora također treba evaluaciju, ne samo dohvat.

Glavna stvar koju sam naučio tijekom provjere jest da se kvaliteta dohvata trebala provjeriti prije generiranja odgovora. Rezultat ugrađivanja već je bio koristan, a lagani preuređivač učinio je da se očekivani odjeljak politike pouzdano pojavi prvi. To je upravo onaj mali sustavni ponašaj koji želim da vodič otkrije umjesto da ga skriva.

## 12. Što slijedi

Sljedeće poboljšanje je usporediti ovaj lokalni set s upravljanom Azure verzijom istog scenarija školskog pomoćnika za politiku. Održavanje scenarija fiksnim trebalo bi olakšati uočavanje kompromisa: složenost postavljanja, kontrola dohvata, integracija identiteta, operativno vlasništvo i troškovi.

## 13. Reference

- [Qdrant Python client brzo uvođenje](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub spremište](https://github.com/qdrant/qdrant-client)
- [FastEmbed podržani modeli](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI vodič za ugrađivanja](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 kartica modela](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 kartica modela](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 kartica modela](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini stranica modela](https://ollama.com/library/phi4-mini)
- [Ollama Windows dokumentacija](https://docs.ollama.com/windows)
- [Ollama API streaming dokumentacija](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct kartica modela](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Pregled LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Uvod u RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Prethodno: [Serija 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->