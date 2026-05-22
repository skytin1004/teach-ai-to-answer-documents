# Naučte AI odpovedať na otázky na základe vašich dokumentov
## Séria 2: Vytvorenie lokálneho open-source RAG systému od začiatku do konca

![Lokálny open-source RAG tutoriálový pipeline](../../../assets/images/series-2-local-rag.svg)

> Tento článok premieňa diskusiu architektúry zo Série 1 na spustiteľný lokálny RAG tutoriál. Cieľom je najprv vybudovať celý pracovný tok s ukážkovými dátami, bez cloudového účtu a bez tajomstiev, a potom použiť tento funkčný základ na lepšie architektonické rozhodnutia.

Systém, ktorý postavíme, je malý asistent pre školskú politiku. Používam dva lokálne Markdown dokumenty ako databázu poznatkov, a potom prechádzam celým RAG pipeline: rozdelenie na časti, lokálne embeddingy, ukladanie vektorov do Qdrant, vyhľadávanie, pretriedenie, skladanie odpovedí s uvedením zdroja a voliteľná lokálna generácia pomocou Ollama a Phi-4-mini.

Navigácia série: [Domovská stránka repozitára](../README.md) | Predchádzajúce: [Séria 1 - RAG, Azure vs Open-Source alternatívy a kedy má zmysel doladenie](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Požiadavky: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Toto je najlepší východiskový bod, ak chcete pochopiť RAG pipeline pred vytvorením cloudových zdrojov. Predvolená cesta beží lokálne s CPU-priateľskými embeddingmi a bez tajomstiev.

## 1. Čo Staviame

V tutoriáli z roku 2023 som začínal na Azure, pretože cieľom bolo ukázať, ako Azure AI Search a Azure OpenAI môžu odpovedať na otázky z PDF dokumentov.

Pre túto sériu z roku 2026 začínam o úroveň nižšie.

Pred použitím spravovaných služieb chcem postaviť malý lokálny RAG systém a urobiť každý krok viditeľným: načítanie dokumentov, delenie textu na časti, ukladanie vektorov, vyhľadávanie dôkazov, pretriedenie výsledkov a vrátenie odpovede s uvedením zdroja.

Ukážkový scenár je asistent pre školskú politiku. Používateľ sa pýta:

```text
Can I use generative AI for my final assignment?
```

Systém by nemal odpovedať zo všeobecnej pamäti modelu. Mal by vyhľadať príslušnú časť politiky a odpovedať na základe tohto dôkazu.

Plná spustiteľná verzia je v [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Nasledujúci kód ukazuje hlavné kroky, takže článok možno čítať ako tutoriál.

## 2. Inštalácia lokálnych závislostí

Vytvorte virtuálne prostredie a nainštalujte požiadavky Série 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Prvá verzia používa lokálny režim Qdrant a FastEmbed. Python klient Qdrant podporuje režim v pamäti s `QdrantClient(":memory:")`, čo je užitočné pre lokálne tutoriály a CI-štýl overovania. FastEmbed nám poskytuje skutočný lokálny embedding model bez potreby cloudového API kľúča.

Súbor požiadaviek tiež obsahuje `python-dotenv`, pretože notebook môže voliteľne načítať názov modelu Ollama z `.env`. Pre tento lokálny tutoriál nie je potrebný kľúč pre Azure OpenAI alebo OpenAI API.

## 3. Načítanie ukážkových dokumentov

Ukážkový korpus je zámerne malý:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

V notebooku načítavam všetky Markdown súbory z `sample_data/`:

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

Keď som spustil notebook, načítal 2 dokumenty. To je dosť málo na to, aby som ich mohol manuálne skontrolovať, čo je užitočné pri budovaní prvej verzie RAG pipeline.

## 4. Rozdelenie podľa nadpisov Markdown

Ďalším krokom je rozdelenie dokumentov na časti.

Pre tento tutoriál používam nadpisy Markdown ako signál štruktúry. Názov dokumentu je z `#`, a každá sekcia je z `##`.

> [!NOTE]
> Rozdelenie na časti nie je univerzálne. V tomto tutoriáli používam Markdown nadpisy, pretože ukážkové dokumenty majú jasnú štruktúru `#` a `##`. Pre PDF, Word dokumenty, prezentácie, lístky alebo webstránky môže byť lepšia stratégia založená na stránkovaní, informáciách o rozložení, sémantických sekciách, limite tokenov, tabuľkách alebo metadátach. Dôležité je zvoliť stratégiu delenia, ktorá zachová význam a možnosť stopy k zdroju pre vaše dokumenty.

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

Potom to aplikuje na každý dokument:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Toto vytvorilo 8 častí v mojom lokálnom behu.

Páčilo sa mi na tomto kroku, že metadáta sú už užitočné. Každá časť pozná svoj `source`, `sectionHeading`, `documentVersion` a zástupný znak `permissions`. Už v malom tutoriáli to uľahčuje citácie a neskoršie vyhľadávanie s ohľadom na práva.

## 5. Vytvorenie lokálnych embeddingov

Pre prvú verejnú verziu používam `BAAI/bge-small-en-v1.5` cez FastEmbed.

Tento prístup udržiava tutoriál lokálny a CPU-priateľský, ale stále používa skutočný embedding model namiesto zástupnej vektorovej funkcie. Pri prvom spustení sa stiahnu váhy modelu. Potom notebook môže znovu použiť lokálnu cache.

> [!NOTE]
> Používam `BAAI/bge-small-en-v1.5`, pretože ide o ľahký anglický embedding model, ktorý dobre funguje s FastEmbed a Qdrant pre lokálny tutoriál. Vytvára 384-dimenzionálne vektory, čo udržiava príklad rýchly a lacný na lokálne spustenie. Nie je to jediná dobrá voľba. V roku 2023 mnohé tutoriály používali hosťované embedding modely ako `text-embedding-ada-002`. Dnes sú nové hosťované možnosti ako OpenAI `text-embedding-3-small` a `text-embedding-3-large`, a open-source možnosti ako BGE, E5, MiniLM, Nomic Embed a viacjazyčné modely ako `BAAI/bge-m3` rozumné voľby podľa záťaže. V produkcii by mal byť správny embedding model vybraný na základe vyhodnotenia vyhľadávania vo vlastných dokumentoch.

Niektoré praktické alternatívy:

| Rodina modelov | Kedy by som ju zvážil |
| --- | --- |
| `text-embedding-ada-002` | Starší hosťovaný základ, ktorý sa objavoval v mnohých tutoriáloch z roku 2023. Dnes by som ho nevychválal ako predvolený pre nový tutoriál. |
| `text-embedding-3-small` | Moderný hosťovaný predvolený model, keď chcem silný pomer cena/výkon a nepotrebujem len lokálne embeddingy. |
| `text-embedding-3-large` | Hosťovaná možnosť, keď kvalita vyhľadávania je dôležitejšia než veľkosť vektora alebo náklady na embedding. |
| `BAAI/bge-small-en-v1.5` | Ľahký lokálny anglický základ pre tutoriály, prototypy a CPU-priateľské experimenty. |
| `BAAI/bge-base-en-v1.5` alebo `BAAI/bge-large-en-v1.5` | Väčšie lokálne anglické modely, keď chcem lepšiu kvalitu vyhľadávania a môžem si dovoliť viac výpočtov. |
| `BAAI/bge-m3` | Viacjazyčné alebo dlhšie kontextové vyhľadávanie, najmä keď dokumenty nie sú len v angličtine. |
| `sentence-transformers/all-MiniLM-L6-v2` | Veľmi malý a rýchly semantický vyhľadávací základ. Užitočný, keď najviac záleží na rýchlosti a jednoduchosti. |
| `nomic-embed-text-v1.5` | Otvorená lokálna embedding možnosť, stojí za otestovanie pre dlhšie kontexty alebo nastavenia fokusované na prenositeľnosť. |

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

Potom každá časť dostane embedding:

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

## 6. Ukladanie vektorov v lokálnom režime Qdrant

Teraz vytvoríme Qdrant kolekciu v pamäti a vložíme do nej časti s metadátami payloadu.

> [!NOTE]
> V tutoriáli z roku 2023 som používal FAISS, pretože to bol jednoduchý a populárny spôsob, ako demonštrovať lokálne vyhľadávanie podobnosti vektorov s LangChain. FAISS je stále užitočný pre rýchle lokálne experimenty. V tejto verzii z roku 2026 používam Qdrant, pretože chcem, aby sa tutoriál cítil bližšie k produkčnému RAG systému. Qdrant mi umožňuje ukladať vektory spolu s metadátami ako sú zdrojový súbor, nadpis sekcie, verzia dokumentu a oprávnenia. To uľahčuje kontrolu vyhľadávania a pripravuje príklad na filtrovanie, citácie a budúce trvalé alebo serverové nasadenie.

FAISS je skvelý na demonštráciu vyhľadávania podobnosti vektorov. Qdrant je lepší na ukážku malej, ale produkčne orientovanej RAG vrstvy vyhľadávania.

Niektoré praktické alternatívy:

| Vektorové úložisko / vrstva vyhľadávania | Kedy by som ju zvážil |
| --- | --- |
| Qdrant | Lokálne prototypy, filtrovanie metadát, produkčne priateľské vyhľadávanie vektorov a jednoduchý Python pracovný tok. |
| Chroma | Rýchle lokálne RAG experimenty a notebooky, kde najviac záleží na jednoduchosti. |
| FAISS | Ľahké lokálne vyhľadávanie vektorov, keď potrebujem len podobnosť a môžem spravovať metadáta zvlášť. |
| Milvus | Väčšie open-source vyhľadávanie vektorov, keď tím je pripravený prevádzkovať dedikovanú vektorovú databázu. |
| Weaviate | Vektorové vyhľadávanie so schémou, metadátami, hybridné vyhľadávanie a spravované alebo vlastne hostené nasadenia. |
| Azure AI Search | Podnikové RAG na Azure, keď chcem kľúčové slová, vektorové vyhľadávanie, hybridnú retrieval, sémantické radenie, filtrovanie, bezpečnosť a spravované operácie v jednom vyhľadávacom nástroji. |
| PostgreSQL + pgvector | Tímy, ktoré už používajú PostgreSQL a chcú vektorové vyhľadávanie blízko aplikačných dát. |

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

Potom vložte body:

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

Pri mojom behu kolekcia vložila 8 vektorov.

Tu sa RAG systém začína stať kontrolovateľným. Vektorová databáza neukladá len vektory, ale aj dôkazový text a metadáta potrebné pre citácie.

## 7. Vyhľadávanie kandidátnych častí

Teraz položíme otázku a vyhľadáme kandidátne časti.

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

V tomto bode vypíšem vyhľadané časti pred generovaním odpovede. To je dôležité. Ak je vyhľadávanie zlé, generovanie len zakryje problém za plynulým textom.

## 8. Pridanie ľahkého pretriedenia (rerankera)

Keď som prvýkrát testoval cestu vyhľadávania, samotná vektorová podobnosť našla súvisiaci obsah politiky, ale najpresnejšia sekcia nebola vždy na vrchu.

Tak som pridal malý lokálny pretriediaci modul. Dáva väčšiu váhu, keď sa otázkové termíny prekrývajú s nadpisom sekcie a obsahom.

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

Po pretriedení sa na vrchol dostal výsledok:

```text
school_ai_policy.md / Final Assignments
```

To bola očakávaná sekcia pre testovaciu otázku.

Toto bola najcennejšia lekcia z prvej implementácie. Aj v malom lokálnom príklade sa kvalita vyhľadávania zlepšila, keď som skombinoval vektorovú podobnosť s ďalším signálom.

## 9. Skladanie podloženej lokálnej odpovede

Pre predvolenú cestu používam transparentný lokálny skladateľ odpovedí namiesto LLM.

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

Toto nie je určené ako finálny generátor odpovedí produktu. Je to nástroj na ladenie. Dokazuje, že vyhľadávanie, metadáta a prepojenie citácií fungujú pred pridaním variability modelu.

## 10. Generovanie lokálnej odpovede s Ollama a Phi-4-mini

Keď vyhľadávanie funguje, notebook môže nahradiť len posledný krok generovania odpovede Ollamou a `phi4-mini:3.8b`.

> [!NOTE]
> Ollama by mala nahradiť len posledný krok generovania odpovedí. Načítanie dokumentov, delenie na časti, ukladanie vektorov, vyhľadávanie, pretriedenie a prepojenie citácií by mali zostať rovnaké.

Najprv notebook vytvorí prompt s dôkazmi z vyhľadaných častí:

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

Pre tento tutoriál odporúčam rodinu Phi-4-mini od Microsoftu cez Ollamu ako predvolenú lokálnu možnosť generovania. V Ollame som testoval model s názvom:

```powershell
ollama pull phi4-mini:3.8b
```

Môžete rýchlo overiť, že model je dostupný:

```powershell
ollama list
```

Potom nastavte tieto premenné:

```powershell
Copy-Item .env.example .env
```

Otvorte `.env` a odkomentujte hodnoty Ollama pre Sériu 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook načíta `.env` z koreňa repozitára pomocou `python-dotenv`, potom pošle ten istý prompt s dôkazmi na lokálny Ollama `/api/chat` endpoint so zakázaným streamovaním. Ak Ollama neběží alebo chýba `SERIES2_OLLAMA_MODEL`, takáto cesta sa preskočí.

> [!NOTE]
> Na tomto stroji si `phi4-mini:3.8b` stiahol približne 2,49 GB súborov modelu. Počas inferencie Ollama hlásila 3,3 GB načítanej veľkosti modelu a použila GPU RTX 3060 Laptop.

Týmto tutoriál ponúka dve úrovne:

1. Deterministický skladateľ odpovedí iba na CPU.
2. Lokálne generovanie odpovedí s Ollamou a Phi-4-mini.

Pipeline vyhľadávania zostáva rovnaký v oboch.

## 11. Výsledok overenia

Notebook som spustil lokálne na Windows s Python 3.12.6.

Nainštalované balíky:

| Balík | Verzia |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Spustenie notebooku:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Výsledok spustenia: úspešne s `nbclient`
- Načítané dokumenty: 2
- Vytvorené časti: 8
- Qdrant kolekcia: `school_policy_local`
- Vložené vektory: 8
- Embedding model: `BAAI/bge-small-en-v1.5`
- Veľkosť embeddingu: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Túto odpoveď by som nenazval dokonalou. Odpovedá z tých správnych dôkazov, ale posledný riadok zdroja je menej presný než deterministický formát citácie. To je užitočné ukázať v návode, pretože to robí ďalšiu inžiniersku otázku zrejmou: generovanie odpovedí potrebuje tiež vyhodnotenie, nielen vyhľadávanie.

Hlavná vec, ktorú som sa naučil pri overovaní, je, že kvalita vyhľadávania by sa mala skontrolovať pred generovaním odpovedí. Výsledok vloženia (embedding) už bol užitočný a ľahký preklasifikátor zabezpečil, že očakávaná sekcia politiky sa spoľahlivo objavila na prvom mieste. Presne toto sú také malé správanie systému, ktoré chcem, aby návod odhalil namiesto toho, aby ho skrýval.

## 12. Čo nasleduje ďalej

Ďalšie zlepšenie je porovnať túto lokálnu súpravu s riadenou verziou Azure toho istého scenára školského asistenta politiky. Udržiavanie fixného scenára by malo uľahčiť videnie kompromisov: zložitosť nastavenia, ovládanie vyhľadávania, integrácia identity, prevádzkové vlastníctvo a náklady.

## 13. Odkazy

- [Rýchly štart Python klienta Qdrant](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant klient GitHub úložisko](https://github.com/qdrant/qdrant-client)
- [Podporované modely FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Príručka OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Karta modelu BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Karta modelu BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Karta modelu sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Stránka modelu Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Dokumentácia Ollama Windows](https://docs.ollama.com/windows)
- [Dokumentácia Ollama API streamovania](https://docs.ollama.com/api/streaming)
- [Karta modelu Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Prehľad LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Úvod do RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Predchádzajúce: [Séria 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->