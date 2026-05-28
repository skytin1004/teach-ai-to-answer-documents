# Naučte AI odpovídat na otázky na základě vašich dokumentů
## Série 2: Vybudujte lokální open-source RAG systém od začátku do konce

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Tento článek přeměňuje architektonickou diskusi ze Série 1 na spustitelný lokální tutoriál RAG. Cílem je nejprve vytvořit celý pracovní postup se vzorovými daty, bez cloudového účtu a bez tajemství, a poté použít tento funkční základ pro lepší architektonická rozhodnutí později.

Systém, který postavíme, je malý asistent školní politiky. Používám dva lokální Markdown dokumenty jako znalostní bázi a poté procházím celou RAG pipeline: dělení na kousky, lokální embeddingy, vektorové úložiště Qdrant, vyhledávání, přehodnocování, tvorbu odpovědi s vědomím zdroje a volitelnou lokální generaci pomocí Ollama a Phi-4-mini.

Navigace sérií: [Domovská stránka repozitáře](../README.md) | Předchozí: [Série 1 - RAG, Azure vs Open-Source alternativy a kdy má smysl doladění](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Požadavky: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Toto je nejlepší výchozí bod, pokud chcete porozumět RAG pipeline před vytvořením cloudových zdrojů. Výchozí cesta běží lokálně s CPU-přátelskými embeddingy a bez tajemství.

## 1. Co stavíme

V tutoriálu z roku 2023 jsem začal u Azure, protože cílem bylo ukázat, jak Azure AI Search a Azure OpenAI mohou odpovídat na otázky z PDF dokumentů.

Pro tuto sérii 2026 chci začít o úroveň níže.

Než použiji spravované služby, chci postavit malý RAG systém lokálně a udělat každý krok viditelný: načítání dokumentů, dělení textu na kousky, ukládání vektorů, vyhledávání důkazů, přehodnocování výsledků a vrácení odpovědi s vědomím zdroje.

Vzorový scénář je asistent školní politiky. Uživatel se ptá:

```text
Can I use generative AI for my final assignment?
```

Systém by neměl odpovídat z obecné paměti modelu. Měl by vyhledat relevantní část politiky a odpovědět z tohoto důkazu.

Plná spustitelná verze je v [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Níže uvedený kód ukazuje hlavní kroky, aby bylo možné tento článek číst jako tutoriál.

## 2. Instalace lokálních závislostí

Vytvořte virtuální prostředí a nainstalujte požadavky Série 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

První verze používá Qdrant lokální režim a FastEmbed. Python klient Qdrantu podporuje paměťový lokální režim s `QdrantClient(":memory:")`, což je užitečné pro lokální tutoriály a CI-style ověřování. FastEmbed nám poskytuje skutečný lokální embedding model bez potřeby cloudového API klíče.

Soubor požadavků také obsahuje `python-dotenv`, protože notebook může volitelně načítat název modelu Ollama z `.env`. Pro tento lokální tutoriál není potřeba žádný Azure OpenAI nebo OpenAI API klíč.

## 3. Načtení vzorových dokumentů

Vzorkový korpus je záměrně malý:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

V notebooku načítám všechny Markdown soubory z `sample_data/`:

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

Když jsem spustil notebook, načetl 2 dokumenty. To je dost malé na ruční kontrolu, což je užitečné při budování první verze RAG pipeline.

## 4. Dělení podle nadpisů Markdown

Dalším krokem je rozdělit dokumenty na kousky.

Pro tento tutoriál používám Markdown nadpisy jako signál struktury. Titulek dokumentu je z `#`, a každý sekční kousek z `##`.

> [!NOTE]
> Dělení na kousky není univerzální. V tomto tutoriálu používám Markdown nadpisy, protože vzorové dokumenty mají jasnou strukturu `#` a `##`. U PDF, Word dokumentů, slidů, tiketů nebo webových stránek může být lepší strategie využít hranice stránek, informace o rozvržení, sémantické sekce, limity tokenů, tabulky nebo metadata. Důležité je zvolit strategii dělení, která zachová význam a sledovatelnost zdroje vašich dokumentů.

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

Pak to použiji na každý dokument:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Toto vytvořilo 8 kousků při mém lokálním spuštění.

Co se mi na tomto kroku líbilo, je, že metadata jsou už užitečná. Každý kousek zná svůj `source`, `sectionHeading`, `documentVersion` a zástupný `permissions`. I v malém tutoriálu to usnadňuje uvažování o citacích a pozdějším retrievalu s povědomím o oprávněních.

## 5. Vytvoření lokálních embeddingů

Pro první veřejnou verzi používám `BAAI/bge-small-en-v1.5` přes FastEmbed.

To udržuje tutoriál lokální a CPU-přátelský, ale stále používá skutečný embedding model místo zástupné vektorové funkce. Při prvním běhu se stáhnou váhy modelu. Poté může notebook znovu použít lokální cache.

> [!NOTE]
> Používám `BAAI/bge-small-en-v1.5`, protože je to lehký anglický embedding model, který dobře funguje s FastEmbed a Qdrant pro lokální tutoriál. Vytváří 384-dimenzionální vektory, což drží příklad rychlý a levný na lokální běh. Toto není jediná dobrá volba. V roce 2023 mnoho tutoriálů používalo hostované embedding modely jako `text-embedding-ada-002`. Dnes jsou nové hostované možnosti jako OpenAI `text-embedding-3-small` a `text-embedding-3-large` a open-source možnosti jako BGE, E5, MiniLM, Nomic Embed a vícejazyčné modely jako `BAAI/bge-m3` všechny rozumné volby podle náročnosti úlohy. Ve výrobě by měl být správný embedding model vybrán pomocí vyhodnocení retrievalu na vašich vlastních dokumentech.

Některé praktické alternativy:

| Rodina modelu | Kdy bych ji zvážil |
| --- | --- |
| `text-embedding-ada-002` | Starší hostovaný základ, který se objevil v mnoha tutoriálech z roku 2023. Dnes bych si ho nevybral jako výchozí pro nový tutoriál. |
| `text-embedding-3-small` | Moderní hostovaný výchozí model, když chci dobrý poměr cena/výkon a nepotřebuji lokální embeddingy. |
| `text-embedding-3-large` | Hostovaná volba, když záleží na kvalitě retrievalu více než na velikosti vektoru nebo nákladech. |
| `BAAI/bge-small-en-v1.5` | Lehký lokální anglický základ pro tutoriály, prototypy a CPU-přátelské experimenty. |
| `BAAI/bge-base-en-v1.5` nebo `BAAI/bge-large-en-v1.5` | Větší lokální anglické modely, když chci lepší kvalitu retrievalu a mohu si dovolit více výpočetních zdrojů. |
| `BAAI/bge-m3` | Vícejazyčný nebo retrieval s delším kontextem, zejména pokud nejsou dokumenty jen anglické. |
| `sentence-transformers/all-MiniLM-L6-v2` | Velmi malý a rychlý sémantický vyhledávací základ. Užitečný, když nejvíc záleží na rychlosti a jednoduchosti. |
| `nomic-embed-text-v1.5` | Otevřená lokální embedding možnost, kterou stojí za to vyzkoušet pro delší kontext nebo nastavení zaměřená na přenositelnost. |

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

Pak každý kousek dostane embedding:

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

## 6. Uložení vektorů do Qdrantu v lokálním režimu

Nyní vytvoříme Qdrant kolekci v paměti a vložíme do ní kousky s metadata payload.

> [!NOTE]
> V tutoriálu z roku 2023 jsem použil FAISS, protože to byl jednoduchý a populární způsob, jak demonstrovat lokální vyhledávání podobnosti vektorů s LangChain. FAISS je stále užitečný pro rychlé lokální experimenty. V této verzi 2026 používám Qdrant, protože chci, aby tutoriál působil blíže produkčnímu RAG systému. Qdrant mi umožňuje ukládat vektory společně s payload metadaty, jako je zdrojový soubor, nadpis sekce, verze dokumentu a oprávnění. To usnadňuje inspekci retrievalu a připravuje příklad pro filtrování, citace a budoucí perzistentní či serverové nasazení.

FAISS je skvělý pro ukázku vyhledávání podobnosti vektorů. Qdrant je lepší pro ukázku malé, ale produkčně tvarované vrstvy RAG retrievalu.

Některé praktické alternativy:

| Vektorové úložiště / search vrstva | Kdy bych ji zvážil |
| --- | --- |
| Qdrant | Lokální prototypy, filtrování metadat, produkčně přátelské vyhledávání vektorů a jednoduchý Python workflow. |
| Chroma | Rychlé lokální RAG experimenty a notebooky, kde nejvíce záleží na jednoduchosti. |
| FAISS | Lehký lokální vyhledávač vektorů, když potřebuji jen vyhledávání podobnosti a mohu spravovat metadata zvlášť. |
| Milvus | Širší škálovatelné open-source vyhledávání vektorů, když je tým připraven provozovat dedikovanou vektorovou databázi. |
| Weaviate | Vyhledávání vektorů se schématem, metadaty, hybridní vyhledávání a možnosti spravovaného nebo self-hosted nasazení. |
| Azure AI Search | Podnikový RAG na Azure, když chci klíčové slovo vyhledávání, vektorové vyhledávání, hybridní retrieval, sémantické řazení, filtrování, zabezpečení a spravované operace v jednom search vrstvě. |
| PostgreSQL + pgvector | Týmy, které již používají PostgreSQL a chtějí vektorové vyhledávání blízko aplikačních dat. |

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

Pak vložíme body:

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

Při mém běhu kolekce vložila 8 vektorů.

Tady RAG systém začíná být inspektovatelný. Vektorová databáze neukládá jen vektory; ukládá text důkazů a metadata potřebná pro citace.

## 7. Získání kandidátních kousků

Nyní položíme otázku a získáme kandidátní kousky.

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

V tomto okamžiku tisknu získané kousky před generováním odpovědi. To je důležité. Pokud je retrieval špatný, generování problém jen skryje za plynulý text.

## 8. Přidání lehkého přehodnotitele (rerankeru)

Když jsem poprvé testoval retrieval, samotná podobnost vektorů našla související obsah politiky, ale nejpřesnější sekce nebyla vždy na vrcholu.

Tak jsem přidal malý lokální reranker. Dává extra váhu, když se termíny otázky překrývají s nadpisem sekce a obsahem.

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

Po přehodnocení se nejlepší výsledek stal:

```text
school_ai_policy.md / Final Assignments
```

To byla očekávaná sekce pro testovací otázku.

Toto byla nejvíce užitečná lekce z první implementace. I v malém lokálním příkladu se kvalita retrievalu zlepšila, když jsem kombinoval podobnost vektorů s dalším signálem.

## 9. Složení podložené lokální odpovědi

Pro výchozí cestu používám průhledný lokální skladatel odpovědí místo LLM.

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

To není určeno jako finální generátor odpovědí. Je to nástroj pro ladění. Dokazuje, že retrieval, metadata a propojení citací fungují před přidáním modelové variability.

## 10. Generování lokální odpovědi pomocí Ollama a Phi-4-mini

Jakmile retrieval funguje, notebook může nahradit jen závěrečný krok odpovědi Ollamou a `phi4-mini:3.8b`.

> [!NOTE]
> Ollama by měla nahrazovat pouze závěrečný krok generování odpovědi. Načítání dokumentů, dělení na kousky, ukládání vektorů, retrieval, přehodnocování a propojení citací by měly zůstat stejné.

Nejprve notebook sestaví prompt s důkazy ze získaných kousků:

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

Pro tento tutoriál doporučuji rodinu Microsoft Phi-4-mini přes Ollama jako výchozí lokální generování. V Ollamě je model, který jsem testoval:

```powershell
ollama pull phi4-mini:3.8b
```

Můžete rychle zkontrolovat, že model je dostupný:

```powershell
ollama list
```

Pak nastavte tyto proměnné:

```powershell
Copy-Item .env.example .env
```

Otevřete `.env` a odkomentujte hodnoty Série 2 pro Ollamu:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook načte `.env` z kořene repozitáře pomocí `python-dotenv` a poté odešle stejný prompt s důkazy na lokální `/api/chat` endpoint Ollamy s vypnutým streamováním. Pokud Ollama neběží nebo chybí `SERIES2_OLLAMA_MODEL`, tento krok se přeskočí.

> [!NOTE]
> Na tomto stroji stáhl `phi4-mini:3.8b` přibližně 2,49 GB modelových souborů. Během inference Ollama hlásila velikost načteného modelu 3,3 GB a použila GPU RTX 3060 Laptop.

Tím má tutoriál dvě úrovně:

1. CPU-only deterministický skladatel odpovědí.
2. Lokální generování odpovědí s Ollama a Phi-4-mini.

Retrieval pipeline zůstává v obou stejná.

## 11. Výsledek ověření

Notebook jsem spustil lokálně na Windows s Pythonem 3.12.6.

Nainstalované balíčky:

| Balíček | Verze |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Spuštění notebooku:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Výsledek spuštění: prošlo s `nbclient`
- Načtené dokumenty: 2
- Vytvořené kousky: 8
- Qdrant kolekce: `school_policy_local`
- Vložené vektory: 8
- Embedding model: `BAAI/bge-small-en-v1.5`
- Velikost embeddingu: 384
- Otázka pro vyhledávání: "Mohu použít generativní AI pro svou závěrečnou práci?"
- Cesta přerovnání: lehké lokální lexikální přerovnání
- Nejlepší nalezený zdroj po přerovnání: `school_ai_policy.md`
- Nejlepší nalezená sekce po přerovnání: `Závěrečné práce`
- Výchozí cesta odpovědi: lokální transparentní skladač odpovědí
- Cesta generování Ollama: dokončeno s `phi4-mini:3.8b`
- Velikost modelového souboru Ollama: 2,49 GB na disku
- Nahlášená velikost načteného modelu Ollama: 3,3 GB podle `ollama ps`
- Vypnutí GPU: 100 % GPU podle `ollama ps`
- Na GPU použité paměti po generování: asi 3,5 GB z 6 GB použito na RTX 3060 Laptop GPU
- Spuštění notebooku s uloženým modelem FastEmbed a povoleným generováním Ollama: úspěšné přibližně za 34 sekund skrze ověřovací skript

Odpověď vygenerovaná Ollamou byla:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```
  
Neoznačil bych tuto odpověď za dokonalou. Odpovídá na základě správných důkazů, ale závěrečný řádek zdroje je méně přesný než deterministický citovací formát. To je užitečné ukázat v tutoriálu, protože to zřejmým způsobem vede k další inženýrské otázce: generování odpovědí potřebuje také vyhodnocení, nejen samotné vyhledávání.

Hlavní věcí, kterou jsem při ověřování zjistil, je, že kvalita vyhledávání by měla být zkontrolována před generováním odpovědi. Výsledek embeddingu už byl užitečný a lehký přerovnávač spolehlivě zpřístupnil očekávanou část politiky na prvním místě. To je přesně ten druh drobného chování systému, který chci, aby tutoriál odhalil místo toho, aby ho skrýval.

## 12. Co přijde dál

Další vylepšení bude porovnání tohoto lokálního nastavení s řízenou verzí Azure pro stejný scénář školního asistenta pravidel. Zachování scénáře by mělo usnadnit porozumění kompromisech: složitost nastavení, kontrola vyhledávání, integrace identity, provozní správa a náklady.

## 13. Reference

- [Rychlý start klienta Qdrant v Pythonu](https://python-client.qdrant.tech/quickstart.html)  
- [GitHub repozitář klienta Qdrant](https://github.com/qdrant/qdrant-client)  
- [Podporované modely FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)  
- [Průvodce embedováními OpenAI](https://platform.openai.com/docs/guides/embeddings)  
- [Karta modelu BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)  
- [Karta modelu BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)  
- [Karta modelu sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  
- [Stránka modelu Ollama phi4-mini](https://ollama.com/library/phi4-mini)  
- [Dokumentace Ollama pro Windows](https://docs.ollama.com/windows)  
- [Dokumentace Ollama API streamování](https://docs.ollama.com/api/streaming)  
- [Karta modelu Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)  
- [Přehled LangGraph](https://docs.langchain.com/oss/python/langgraph)  
- [Úvod do RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)  

Předchozí: [Série 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->