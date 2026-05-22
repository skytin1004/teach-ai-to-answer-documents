# Išmokykite DI atsakyti į klausimus, remiantis jūsų dokumentais
## 2 serija: Sukurkite vietinę atviro kodo RAG sistemą nuo pradžios iki galo

![Vietinės atviro kodo RAG mokymo vamzdis](../../../assets/images/series-2-local-rag.svg)

> Šis straipsnis paverčia 1 serijos architektūros aptarimą į paleidžiamą vietinį RAG mokymą. Tikslas yra pirmiausia sukurti visą darbo eigą su pavyzdiniais duomenimis, be debesies paskyros ir be paslapčių, o vėliau naudoti tą veikiančią bazę geresniems architektūros sprendimams priimti.

Sistemos, kurią kursime, paskirtis – nedidelis mokyklos politikos asistentas. Naudoju du vietinius Markdown dokumentus kaip žinių bazę, tada einu per visą RAG vamzdyną: dalių skaidymą, vietinius įdėklius, Qdrant vektorių saugyklą, gavimą, perrūšiavimą, šaltinio žinomą atsakymo sudarymą ir neprivalomą vietinį generavimą su Ollama ir Phi-4-mini.

Serijos navigacija: [Saugyklos pradžia](../README.md) | Ankstesnis: [1 serija - RAG, Azure vs atviro kodo alternatyvos ir kada prasminga tikslinti](./series-1-rag-azure-open-source-fine-tuning.md)

Užrašų knygelė: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Reikalavimai: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Tai geriausia pradžia, jei norite suprasti RAG vamzdyną prieš kuriant debesies išteklius. Numatytoji eiga vyksta vietoje su CPU draugiškais įdėklais ir be paslapčių.

## 1. Ką mes kursime

2023 metų mokymo metu pradėjau nuo Azure, nes tikslas buvo parodyti, kaip Azure AI Search ir Azure OpenAI galėtų atsakyti į klausimus iš PDF dokumentų.

Šiai 2026 serijai noriu pradėti vienu lygiu žemiau.

Prieš naudojant valdomas paslaugas, noriu vietoje sukurti nedidelę RAG sistemą ir padaryti kiekvieną žingsnį matomą: įkelti dokumentus, skaidyti tekstą, saugoti vektorius, gauti įrodymus, perrūšiuoti rezultatus ir pateikti šaltinio atsižvelgiantį atsakymą.

Pavyzdinis scenarijus – mokyklos politikos asistentas. Vartotojas klausia:

```text
Can I use generative AI for my final assignment?
```
  
Sistema neturėtų atsakyti iš bendros modelio atminties. Ji turėtų rasti atitinkamą politikos skyrių ir atsakyti remdamasi tuo įrodymu.

Pilna paleidžiama versija yra [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Žemiau pateiktas kodas rodo pagrindinius žingsnius, kad straipsnį būtų galima skaityti kaip mokymą.

## 2. Įdiekite vietines priklausomybes

Sukurkite virtualią aplinką ir įdiekite 2 serijos reikalavimus:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```
  
Pirmoji versija naudoja Qdrant vietinį režimą ir FastEmbed. Qdrant Python klientas palaiko atmintyje esančią vietinę režimą su `QdrantClient(":memory:")`, kas yra naudinga vietiniams mokymams ir CI tipo patikrinimams. FastEmbed suteikia tikrą vietinį įdėklių modelį be debesies API rakto.

Reikalavimų faile taip pat yra `python-dotenv`, nes užrašų knygelė gali neprivalomai nuskaityti Ollama modelio pavadinimą iš `.env`. Šiam vietiniam mokymui nereikia Azure OpenAI ar OpenAI API rakto.

## 3. Įkelkite pavyzdinius dokumentus

Pavyzdinis korausas yra sąmoningai nedidelis:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)  
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)  

Užrašų knygelėje įkraunu visus Markdown failus iš `sample_data/`:

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
  
Kai paleidau užrašų knygelę, įkėlė 2 dokumentus. Tai pakankamai mažas kiekis, kad būtų galima rankiniu būdu apžiūrėti, kas yra naudinga, kuriant pirmą RAG vamzdyno versiją.

## 4. Skaldymas pagal Markdown antraštes

Kitas žingsnis – dokumentų suskaidymas į dalis.

Šiame mokyme naudoju Markdown antraštes kaip struktūros signalą. Dokumento pavadinimas gaunamas iš `#`, o kiekviena skyriaus dalis iš `##`.

> [!NOTE]
> Dalių skaidymas nėra vienodos formulės sprendimas. Šiame mokyme naudoju Markdown antraštes, nes pavyzdiniuose dokumentuose aiški `#` ir `##` struktūra. PDF failams, Word dokumentams, skaidrėms, užduotims ar tinklalapiams geresnė strategija gali būti naudoti puslapio ribas, išdėstymo informaciją, semantinius skyrius, tokenų limitus, lenteles ar metaduomenis. Svarbiausia yra pasirinkti tokią skaidymo strategiją, kuri išsaugotų prasmę ir šaltinio atsekamumą jūsų dokumentams.

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
  
Tada pritaikau tai kiekvienam dokumentui:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```
  
Mano vietiniame paleidime susidarė 8 dalys.

Man patiko tai, kad metaduomenys jau tapo naudingi. Kiekviena dalis žino savo `source`, `sectionHeading`, `documentVersion` ir vietos rezervą `permissions`. Net mažame mokyme tai palengvina citavimą ir vėlesnį leidimų žinomą gavimą.

## 5. Sukurkite vietinius įdėklius

Pirmajai viešai versijai naudoju `BAAI/bge-small-en-v1.5` per FastEmbed.

Tai leidžia mokymą laikyti vietiniu ir CPU draugišku, bet vis tiek naudoja tikrą įdėklių modelį vietoj laikino funkcijos vektoriaus. Pirmas paleidimas atsisiunčia modelio svorius. Vėliau užrašų knygelė gali naudoti vietinę talpyklą.

> [!NOTE]
> Naudoju `BAAI/bge-small-en-v1.5`, nes tai yra lengvas anglų kalbos įdėklių modelis, puikiai veikiantis su FastEmbed ir Qdrant vietiniam mokymui. Jis sukuria 384 matmenų vektorius, kas palaiko pavyzdį greitą ir nebrangų paleisti vietoje. Tai nėra vienintelė gera pasirinktis. 2023 metais daugelis mokymų naudojo hostintus įdėklių modelius, tokius kaip `text-embedding-ada-002`. Šiandien naujesnės hostintos parinktys, tokios kaip OpenAI `text-embedding-3-small` ir `text-embedding-3-large`, bei atviro kodo parinktys, tokios kaip BGE, E5, MiniLM, Nomic Embed, ir daugialypiai modeliai, kaip `BAAI/bge-m3`, yra visi pagrįsti variantai, priklausomai nuo darbo krūvio. Gamykloje tinkamas įdėklių modelis turėtų būti parinktas įvertinant paiešką pagal jūsų pačių dokumentus.

Keletas praktinių alternatyvų:

| Modelių šeima | Kada svarstyčiau |
| --- | --- |
| `text-embedding-ada-002` | Senesnė hostinta bazė, kuri dažnai buvo naudojama 2023 metų mokymuose. Nerekomenduočiau naudoti kaip numatytosios naujajame mokyme šiandien. |
| `text-embedding-3-small` | Moderni hostinta numatytoji, kai noriu stiprios sąnaudų/veiklos pusiausvyros ir nereikia tik vietoje veikiančių įdėklių. |
| `text-embedding-3-large` | Hostinta parinktis, kai svarbesnė paieškos kokybė nei vektoriaus dydis ar įdėklių kaina. |
| `BAAI/bge-small-en-v1.5` | Lengvas vietinis anglų kalbos pavyzdys mokymams, prototipams ir CPU draugiškiems eksperimentams. |
| `BAAI/bge-base-en-v1.5` arba `BAAI/bge-large-en-v1.5` | Didesni vietiniai anglų kalbos modeliai, kai nori geresnio paieškos kokybės ir gali sau leisti daugiau skaičiavimų. |
| `BAAI/bge-m3` | Daugiakalbė arba ilgesnio konteksto paieška, ypač kai dokumentai ne tik anglų kalba. |
| `sentence-transformers/all-MiniLM-L6-v2` | Labai mažas ir greitas semantinės paieškos pagrindas. Naudinga, kai svarbiausia greitis ir paprastumas. |
| `nomic-embed-text-v1.5` | Atviras vietinis įdėklių variantas, vertas išbandymo ilgesnio konteksto ar nešiojamo naudojimo setupams. |

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
  
Tada kiekviena dalis gauna įdėklį:

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
  
## 6. Saugojimas vektorių Qdrant vietiniame režime

Dabar sukuriame atmintyje esančią Qdrant kolekciją ir įterpiame dalis su papildoma metaduomenų apkrova.

> [!NOTE]
> 2023 metų mokyme naudojau FAISS, nes tai buvo paprastas ir populiarus būdas parodyti vietinę vektorinę panašumo paiešką su LangChain. FAISS vis tiek naudinga greitiems vietiniams eksperimentams. Šioje 2026 versijoje naudoju Qdrant, nes noriu, kad mokymas būtų arčiau gamybos RAG sistemos. Qdrant leidžia saugoti vektorius kartu su apkrovos metaduomenimis, tokiais kaip šaltinio failas, skyriaus antraštė, dokumento versija ir leidimai. Tai leidžia lengviau tikrinti gavimą ir paruošia pavyzdį filtravimui, citatoms ir būsimam nuolatiniam ar serveriniu pagrindu vykdomam diegimui.

FAISS yra puikus, norint parodyti vektorinę panašumo paiešką. Qdrant yra geresnis mažo, bet pagal gamybą formuojamo RAG gavimo sluoksnio pavyzdys.

Keletas praktinių alternatyvų:

| Vektorių saugykla / paieškos sluoksnis | Kada svarstyčiau |
| --- | --- |
| Qdrant | Vietiniai prototipai, metaduomenų filtravimas, gamybai draugiška vektorinė paieška ir paprasta Python darbo eiga. |
| Chroma | Greiti vietiniai RAG eksperimentai ir užrašų knygelės, kur svarbiausia paprastumas. |
| FAISS | Lengvas vietinis vektorių paieškos variklis, kai reikia tik panašumo paieškos ir metaduomenis valdoma atskirai. |
| Milvus | Didesnio masto atviro kodo vektorių paieška komandai, pasiruošusiai valdyti specializuotą vektorių duomenų bazę. |
| Weaviate | Vektorinė paieška su schemomis, metaduomenimis, hibridine paieška ir valdomomis arba savarankiškomis diegimo galimybėmis. |
| Azure AI Search | Įmoninė RAG Azureje, kai noriu raktažodžių paieškos, vektorinės paieškos, hibridinio gavimo, semantinį rūšiavimą, filtravimą, saugumą ir valdomą veikimą viename sluoksnyje. |
| PostgreSQL + pgvector | Komandoms, kurios jau naudoja PostgreSQL ir nori vektorinės paieškos arčiau programos duomenų. |

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
  
Tada įkelkite taškus:

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
  
Mano paleidime kolekcija įterpė 8 vektorius.

Čia RAG sistema pradeda tapti apžiūrima. Vektorinė duomenų bazė ne tik saugo vektorius; ji saugo įrodymų tekstą ir metaduomenis, reikalingus citatoms.

## 7. Kandidatų dalių gavimas

Dabar klausiame klausimo ir gauname kandidatų dalis.

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
  
Šiuo momentu išspausdinu gautas dalis prieš generuojant atsakymą. Tai svarbu. Jei gavimas neteisingas, generavimas tik paslėps problemą už rišlaus teksto.

## 8. Pridėkite lengvą perrūšiuotoją

Pirmą kartą išbandžius gavimo kelią, vektorinė panašumo paieška rado susijusį politikos turinį, tačiau pats tiksliausias skyrius ne visada buvo viršuje.

Todėl pridėjau mažą vietinį perrūšiuotoją. Jis suteikia papildomą svorį, kai klausimo terminai sutampa su skyriaus antrašte ir turiniu.

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
  
Po perrūšiavimo viršutinis rezultatas tapo:

```text
school_ai_policy.md / Final Assignments
```
  
Tai buvo laukiamas skyrius testiniam klausimui.

Tai buvo naudingiausia pamoka iš pirmojo įgyvendinimo. Net mažame vietiniame pavyzdyje gavimo kokybė pagerėjo, kai sujungiau vektorinį panašumą su kitu signalu.

## 9. Sudarykite pagrįstą vietinį atsakymą

Numatytajai eigai naudoju skaidrų vietinį atsakymų sudarytoją, o ne LLM.

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
  
Tai nėra skirta galutiniam produktui generuoti. Tai yra derinimo priemonė. Ji įrodo, kad gavimas, metaduomenys ir citavimo jungtys veikia prieš įtraukiant modelio kintamumą.

## 10. Vietinis atsakymas su Ollama ir Phi-4-mini generavimas

Kai gavimas veikia, užrašų knygelė gali pakeisti tik galutinį atsakymo žingsnį naudojant Ollama ir `phi4-mini:3.8b`.

> [!NOTE]
> Ollama turi pakeisti tik galutinį atsakymo generavimo žingsnį. Dokumentų įkėlimas, skaidymas, vektorių saugojimas, gavimas, perrūšiavimas ir citavimo jungtys turi išlikti tokios pačios.

Pirmiausia užrašų knygelė sukuria įrodymų užklausą iš gautų dalių:

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
  
Šiam mokymui rekomenduoju „Microsoft“ Phi-4-mini šeimą per Ollama kaip numatytąją vietinę generavimo parinktį. Ollama modelio pavadinimas, kurį išbandžiau, yra:

```powershell
ollama pull phi4-mini:3.8b
```
  
Greitai patikrinkite, ar modelis yra prieinamas:

```powershell
ollama list
```
  
Tada nustatykite šias reikšmes:

```powershell
Copy-Item .env.example .env
```
  
Atverkite `.env` ir atkomentuokite 2 serijos Ollama reikšmes:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```
  
Užrašų knygelė įkelia `.env` iš saugyklos šaknies naudodama `python-dotenv`, tada siunčia tą pačią įrodymų užklausą į Ollama vietinį `/api/chat` galinį tašką su srauto išjungimu. Jei Ollama neveikia arba trūksta `SERIES2_OLLAMA_MODEL`, ši dalis praleidžiama.

> [!NOTE]
> Šiame kompiuteryje `phi4-mini:3.8b` atsisiuntė apie 2,49GB modelio failų. Darbo metu Ollama pranešė apie 3,3GB užkrautą modelio dydį ir naudojo RTX 3060 Laptop GPU.

Tai suteikia mokymui du lygius:

1. Tik CPU determininis atsakymų sudarytojas.  
2. Vietinis atsakymų generavimas su Ollama ir Phi-4-mini.

Gavimo vamzdis išlieka toks pats abiem atvejais.

## 11. Tikrinimo rezultatas

Aš paleidau užrašų knygelę vietoje Windows su Python 3.12.6.

Įdiegti paketai:

| Paketas | Versija |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Užrašų knygelės vykdymas:

- Užrašų knygelė: `notebooks/series-2-open-source-rag.ipynb`  
- Vykdymo rezultatas: praeita su `nbclient`  
- Įkelti dokumentai: 2  
- Sukurta dalių: 8  
- Qdrant kolekcija: `school_policy_local`  
- Įterpti vektoriai: 8  
- Įdėklių modelis: `BAAI/bge-small-en-v1.5`  
- Įdėklių dydis: 384  
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Aš nesakyčiau, kad šis atsakymas yra tobulas. Jis remiasi teisingais įrodymais, tačiau galutinė šaltinio eilutė yra mažiau tiksli nei deterministinis citavimo formatas. Tai naudinga parodyti mokymo priemonėje, nes tai aiškiai nurodo kitą inžinerinį klausimą: atsakymų generavimas taip pat turi būti vertinamas, ne tik atranka.

Svarbiausia, ką sužinojau patikrindamas šį procesą, yra tai, kad atsakymo kokybė turėtų būti tikrinama prieš atsakymų generavimą. Įterpimo rezultatas jau buvo naudingas, o lengvasis vietinis perrūšiuotojas patikimai pakėlė laukiamą politikos skyrių pirmam vietai. Būtent tokį mažą sistemos elgesį noriu atskleisti mokymo priemonėje, o ne slėpti.

## 12. Kas toliau

Kitas žingsnis – palyginti šią vietinę sistemą su valdomu Azure versija to paties mokyklos politikos asistento scenarijui. Laikant scenarijų pastoviu, bus lengviau pastebėti kompromisus: diegimo sudėtingumą, paieškos kontrolę, tapatybės integraciją, operacinę atsakomybę ir kainą.

## 13. Nuorodos

- [Qdrant Python klientas greitas pradžia](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant kliento GitHub repozitorija](https://github.com/qdrant/qdrant-client)
- [FastEmbed palaikomi modeliai](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI įterpimų vadovas](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 modelio kortelė](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 modelio kortelė](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 modelio kortelė](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini modelio puslapis](https://ollama.com/library/phi4-mini)
- [Ollama Windows dokumentacija](https://docs.ollama.com/windows)
- [Ollama API srautinio perdavimo dokumentacija](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct modelio kortelė](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph apžvalga](https://docs.langchain.com/oss/python/langgraph)
- [Įvadinis RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Ankstesnis: [Serija 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->