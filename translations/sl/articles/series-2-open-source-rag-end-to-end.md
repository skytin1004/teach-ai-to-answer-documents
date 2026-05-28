# Naučite AI odgovarjati na vprašanja na podlagi vaših dokumentov
## Serija 2: Zgradite lokalni odprtokodni RAG sistem od začetka do konca

![Lokalni odprtokodni RAG tutorial potek](../../../assets/images/series-2-local-rag.svg)

> Ta članek spreminja arhitekturno razpravo iz Serije 1 v izvajalni lokalni RAG tutorial. Cilj je najprej zgraditi celoten potek dela s primeri podatkov, brez oblaka in brez skrivnosti, nato pa uporabiti to delujočo osnovo za boljše arhitekturne odločitve pozneje.

Sistem, ki ga bomo zgradili, je majhen pomočnik za šolsko politiko. Uporabim dva lokalna Markdown dokumenta kot bazo znanja, nato pa prehodim celoten RAG potek: razdeljevanje na koščke, lokalne vgradnje, Qdrant shranjevanje vektorjev, iskanje, ponovni vrstni red, sestavljanje odgovora z zavedanjem vira in neobvezno lokalno generacijo z Ollamo in Phi-4-mini.

Navigacija po seriji: [Zavihek repozitorija](../README.md) | Prejšnji: [Serija 1 - RAG, Azure proti odprtokodnim alternativam in kdaj je smiselno fino nastavljanje](./series-1-rag-azure-open-source-fine-tuning.md)

Zvezek: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Zahteve: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> To je najboljši izhodiščni točka, če želite razumeti RAG potek, preden ustvarite vire v oblaku. Privzeta pot poteka lokalno z embeddings prijaznimi za CPU in brez skrivnosti.

## 1. Kaj gradimo

V tutorialu za leto 2023 sem začel z Azure, ker je bil cilj pokazati, kako lahko Azure AI Search in Azure OpenAI odgovarjata na vprašanja iz PDF dokumentov.

Za to serijo 2026 želim začeti eno plast nižje.

Pred uporabo upravljanih storitev želim zgraditi majhen lokalni RAG sistem in narediti vsak korak viden: nalaganje dokumentov, razdeljevanje besedila, shranjevanje vektorjev, iskanje dokazov, ponovni vrstni red rezultatov in vrnitev odgovora z zavedanjem vira.

Primer scenarija je pomočnik za šolsko politiko. Uporabnik vpraša:

```text
Can I use generative AI for my final assignment?
```

Sistem ne sme odgovarjati iz splošnega pomnilnika modela. Mora poiskati ustrezen del politike in odgovoriti na podlagi teh dokazov.

Celotna delujoča različica je v [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Spodnja koda prikazuje glavne korake, da je članek lahko prebran kot tutorial.

## 2. Namestite lokalne odvisnosti

Ustvarite virtualno okolje in namestite zahteve Serije 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Prva različica uporablja Qdrant v lokalnem načinu in FastEmbed. Python odjemalec za Qdrant podpira lokalni način v pomnilniku z `QdrantClient(":memory:")`, kar je uporabno za lokalne tutoriale in preverjanje v slogu CI. FastEmbed nam daje pravi lokalni model vgradnje brez potrebe po ključu API oblaka.

Datoteka z zahtevami vsebuje tudi `python-dotenv`, ker lahko zvezek po potrebi prebere ime modela Ollama iz `.env`. Za ta lokalni tutorial ni potreben noben ključ Azure OpenAI ali OpenAI API.

## 3. Naložite primere dokumentov

Vzorec korpusa je namerno majhen:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

V zvezku naložim vse Markdown datoteke iz `sample_data/`:

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

Ko sem zagnal zvezek, sta bila naložena 2 dokumenta. To je dovolj majhno za ročni pregled, kar je uporabno ob gradnji prve različice RAG poteka.

## 4. Razdeljevanje po Markdown naslovih

Naslednji korak je razdeliti dokumente na koščke.

Za ta tutorial uporabljam Markdown naslove kot signal strukture. Naslov dokumenta izhaja iz `#`, vsak odsek pa iz `##`.

> [!NOTE]
> Razdeljevanje ni univerzalno. V tem tutorialu uporabljam Markdown naslove, ker imajo vzorčni dokumenti jasno strukturo z `#` in `##`. Za PDF-je, Word dokumente, diapozitive, vstopnice ali spletne strani je lahko boljša strategija uporaba mej strani, informacij o postavitvi, semantičnih odsekov, omejitev števila tokenov, tabel ali metapodatkov. Pomembno je izbrati strategijo razdeljevanja, ki ohranja pomen in sledljivost vira za vaše dokumente.

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

Nato to aplikiram na vsak dokument:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

V mojem lokalnem zagonu je to ustvarilo 8 koščkov.

Všeč mi je bilo to, da so metapodatki že koristni. Vsak košček pozna svoj `source`, `sectionHeading`, `documentVersion` in začasno `permissions`. Tudi v majhnem tutorialu to olajša navajanje in kasnejše iskanje z upoštevanjem dovoljenj.

## 5. Ustvarite lokalne vgradnje

Za prvo javno različico uporabljam `BAAI/bge-small-en-v1.5` preko FastEmbed.

To ohranja tutorial lokalno in prijazno za CPU, hkrati pa uporablja pravi model vgradnje namesto funkcije nadomestnega vektorja. Prvi zagon prenese uteži modela. Po tem lahko zvezek ponovno uporabi lokalni predpomnilnik.

> [!NOTE]
> Uporabljam `BAAI/bge-small-en-v1.5`, ker je lahek angleški model vgradnje, ki dobro deluje s FastEmbed in Qdrantom za lokalni tutorial. Ustvari 384-dimenzionalne vektorje, kar ohranja primer hiter in poceni za lokalno izvajanje. To ni edina dobra izbira. Leta 2023 so mnogi tutoriali uporabljali gostovane modele vgradnje, kot `text-embedding-ada-002`. Danes so novejše gostovane možnosti, kot OpenAI `text-embedding-3-small` in `text-embedding-3-large`, ter odprtokodne možnosti, kot BGE, E5, MiniLM, Nomic Embed in večjezični modeli, kot `BAAI/bge-m3`, vse razumske izbire glede na obremenitev. V produkciji je treba pravi model vgradnje izbrati z oceno iskanja na lastnih dokumentih.

Nekatere praktične alternative:

| Družina modelov | Kdaj bi ga upošteval |
| --- | --- |
| `text-embedding-ada-002` | Starejša gostovana osnova, ki se je pojavila v mnogih tutorialih iz leta 2023. Danes je ne bi izbral kot privzeto za nov tutorial. |
| `text-embedding-3-small` | Moderna gostovana privzeta izbira, ko želim močno ravnotežje stroškov/zmogljivosti in ne potrebujem samo lokalnih vgradnjev. |
| `text-embedding-3-large` | Gostovana možnost, ko je kvaliteta iskanja pomembnejša od velikosti vektorja ali stroška vgradnje. |
| `BAAI/bge-small-en-v1.5` | Lahka lokalna angleška osnova za tutoriale, prototipe in eksperimente prijazne do CPU. |
| `BAAI/bge-base-en-v1.5` ali `BAAI/bge-large-en-v1.5` | Večji lokalni angleški modeli, ko želim boljšo kakovost iskanja in si lahko privoščim več izračuna. |
| `BAAI/bge-m3` | Večjezično ali iskanje daljšega konteksta, zlasti ko dokumenti niso samo v angleščini. |
| `sentence-transformers/all-MiniLM-L6-v2` | Zelo majhna in hitra osnova za semantično iskanje. Uporabno, kadar sta hitrost in enostavnost najpomembnejši. |
| `nomic-embed-text-v1.5` | Odprta lokalna možnost vgradnje, vredna preizkušanja za daljše kontekste ali nastavitve, osredotočene na prenosljivost. |

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

Nato vsak košček dobi vgradnjo:

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

## 6. Shranjevanje vektorjev v Qdrant lokalnem načinu

Zdaj ustvarimo Qdrant zbirko v pomnilniku in vstavimo koščke s metapodatki.

> [!NOTE]
> V tutorialu iz 2023 sem uporabljal FAISS, ker je bil enostaven in priljubljen način za demonstracijo lokalnega iskanja podobnosti vektorjev z LangChain. FAISS je še vedno uporaben za hitre lokalne eksperimente. V tej 2026 različici uporabljam Qdrant, ker želim, da tutorial deluje bližje produkcijskemu RAG sistemu. Qdrant mi omogoča shranjevanje vektorjev skupaj z metapodatki, kot so datoteka vira, naslov odseka, različica dokumenta in dovoljenja. To olajša preglednost iskanja in pripravi primer za filtriranje, navajanje in prihodnji trajni ali strežniški zagon.

FAISS je odličen za prikaz iskanja po podobnosti vektorjev. Qdrant je boljši za prikaz majhnega, a produkcijsko oblike RAG plasti iskanja.

Nekatere praktične alternative:

| Shranjevanje vektorjev / sloj iskanja | Kdaj bi ga upošteval |
| --- | --- |
| Qdrant | Lokalni prototipi, filtriranje metapodatkov, produkcijsko prijazno iskanje vektorjev in preprost Python potek dela. |
| Chroma | Hitri lokalni RAG eksperimenti in zvezki, kjer je enostavnost pomembna. |
| FAISS | Lahko localno iskanje vektorjev, ko potrebujem le iskanje podobnosti in lahko metapodatke upravljam ločeno. |
| Milvus | Večja odprtokodna baza za iskanje vektorjev, ko je ekipa pripravljena upravljati namensko vektorsko bazo podatkov. |
| Weaviate | Iskanje vektorjev s shemo, metapodatki, hibridnim iskanjem ter upravljane ali samostojne možnosti zagona. |
| Azure AI Search | Podjetniški RAG na Azure, ko želim iskanje po ključnih besedah, iskanje vektorjev, hibridno pridobivanje, semantično rangiranje, filtriranje, varnost in upravljanje v enem sloju iskanja. |
| PostgreSQL + pgvector | Ekipe, ki že uporabljajo PostgreSQL in želijo iskanje vektorjev blizu podatkov aplikacije. |

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

Nato vstavim točke:

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

V mojem zagonu je zbirka vključila 8 vektorjev.

Tukaj sistem RAG začne postajati pregledljiv. Vektorska baza ne shranjuje samo vektorjev, ampak tudi besedilo dokazov in metapodatke, potrebne za navajanje.

## 7. Izbira kandidatnih koščkov

Zdaj postavimo vprašanje in poiščemo kandidatne koščke.

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

V tem trenutku izpišem najdene koščke pred generiranjem odgovora. To je pomembno. Če je iskanje napačno, bo generiranje problem samo zakrilo z tekočim besedilom.

## 8. Dodajte lahko ponovni vrstni red

Ko sem prvič preizkusil pot iskanja, je sama podobnost vektorjev našla povezano politiko, vendar najprimernejši odsek ni bil vedno na vrhu.

Zato sem dodal majhen lokalni ponovni vrstni red. Daje dodatno težo, ko se vprašalna beseda prekriva z naslovom odseka in vsebino.

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

Po ponovnem vrstnem redu je bil najboljši rezultat:

```text
school_ai_policy.md / Final Assignments
```

To je bil pričakovan odsek za testno vprašanje.

To je bila najbolj dragocena lekcija iz prve izvedbe. Tudi v majhnem lokalnem primeru se je kakovost iskanja izboljšala, ko sem združil podobnost vektorjev z dodatnim signalom.

## 9. Sestavite lokalni ozemljeni odgovor

Za privzeto pot uporabljam preglednega lokalnega sestavljalca odgovorov namesto LLM.

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

To ni mišljeno kot končni generator odgovorov. Je orodje za odpravljanje napak. Dokazuje, da iskanje, metapodatki in povezave citatov delujejo, preden dodamo variabilnost modela.

## 10. Lokalna generacija odgovora z Ollamo in Phi-4-mini

Ko iskanje deluje, zvezek lahko nadomesti le zadnji korak odgovora z Ollamo in `phi4-mini:3.8b`.

> [!NOTE]
> Ollama naj zamenja samo zadnji korak generiranja odgovora. Nalaganje dokumentov, razdeljevanje, shranjevanje vektorjev, iskanje, ponovni vrstni red in povezovanje citatov naj ostanejo enaki.

Najprej zvezek ustvari dokazni poziv iz najdenih koščkov:

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

Za ta tutorial priporočam družino Phi-4-mini podjetja Microsoft preko Ollame kot privzeto možnost lokalne generacije. V Ollami je ime modela, ki sem ga testiral:

```powershell
ollama pull phi4-mini:3.8b
```

Lahko hitro preverite, ali je model na voljo:

```powershell
ollama list
```

Nato nastavite te spremenljivke:

```powershell
Copy-Item .env.example .env
```

Odprite `.env` in odkomentirajte vrednosti Ollama iz Serije 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Zvezek naloži `.env` iz korena repozitorija z `python-dotenv`, nato pa pošlje isti dokazni poziv na lokalno Ollamino `/api/chat` končno točko z onemogočenim pretakanjem. Če Ollama ni zagnana ali pa manjka `SERIES2_OLLAMA_MODEL`, se ta pot preskoči.

> [!NOTE]
> Na tem računalniku je `phi4-mini:3.8b` prenesel približno 2,49 GB modelskih datotek. Med inferenco je Ollama poročala o velikosti naloženega modela 3,3 GB in uporabljala RTX 3060 Laptop GPU.

To tutorialu daje dve stopnji:

1. Deterministični sestavljalec odgovorov samo za CPU.
2. Lokalno generiranje odgovorov z Ollamo in Phi-4-mini.

Potek iskanja ostaja enak v obeh.

## 11. Rezultat preverjanja

Zvezek sem zagnal lokalno na Windows z Python 3.12.6.

Naloženi paketi:

| Paket | Verzija |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Izvajanje zvezka:

- Zvezek: `notebooks/series-2-open-source-rag.ipynb`
- Rezultat zagona: uspel z `nbclient`
- Naloženi dokumenti: 2
- Ustvarjeni koščki: 8
- Qdrant zbirka: `school_policy_local`
- Vstavljeni vektorji: 8
- Model vgradnje: `BAAI/bge-small-en-v1.5`
- Velikost vgradnje: 384
- Vprašanje iskanja: "Ali lahko uporabim generativno AI za svojo zaključni nalogo?"
- Pot ponovnega razvrščanja: lahka lokalna leksikalna ponovna razvrstitev
- Najboljši pridobljeni vir po ponovni razvrstitvi: `school_ai_policy.md`
- Najboljši pridobljeni odsek po ponovni razvrstitvi: `Zaključne naloge`
- Privzeta pot odgovora: lokalni prozorni sestavljalec odgovorov
- Pot generiranja Ollama: zaključena z `phi4-mini:3.8b`
- Velikost datoteke modela Ollama: 2,49 GB na disku
- Naložena velikost modela Ollama: 3,3 GB, poročano z `ollama ps`
- Odklop GPU: 100 % GPU, poročano z `ollama ps`
- Opazovani pomnilnik GPU po generiranju: približno 3,5 GB od 6 GB na RTX 3060 prenosnem GPU
- Izvedba zvezka s predpomnjenim modelom FastEmbed in omogočenim generiranjem Ollama: uspešno v približno 34 sekundah prek preverjevalnega skripta

Ollama-generated answer was:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Ne bi rekel, da je ta odgovor popoln. Odgovarja na osnovi pravih dokazov, vendar je zadnja vrstica vira manj natančna kot deterministična oblika citiranja. To je koristno pokazati v vodiču, ker naredi naslednje inženirsko vprašanje očitno: tudi generiranje odgovorov potrebuje evalvacijo, ne samo iskanje.

Glavna stvar, ki sem se je naučil med preverjanjem tega, je, da je kakovost iskanja treba preveriti pred generiranjem odgovorov. Rezultat vdelave je bil že uporaben, lahki ponovni razvrščevalec pa je zanesljivo naredil, da se pričakovani odsek pravilnika pojavi prva. To je ravno tista vrsta majhnega vedenja sistema, ki ga želim, da vodič izpostavi namesto skriva.

## 12. Kaj sledi

Naslednja izboljšava je primerjati to lokalno nastavitev z upravljano različico Azure istega scenarija šolskega pomočnika za politike. Ohranjanje fiksnega scenarija bo olajšalo opazovanje kompromisov: zahtevnost nastavitve, nadzor iskanja, integracijo identitete, operativno lastništvo in stroške.

## 13. Viri

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

Prejšnji: [Serija 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->