# Научите вештачку интелигенцију да одговара на питања на основу ваших докумената
## Серия 2: Направите локални отворени RAG систем од почетка до краја

![Локални отворени RAG туторијал процес](../../../assets/images/series-2-local-rag.svg)

> Овај чланак претвара дискусију о архитектури из Серие 1 у извршни локални RAG туторијал. Циљ је прво изградити цео радни ток са примером података, без облачног налога и без тајни, затим користити ту радну основицу за боље одлуке о архитектури касније.

Систем који ћемо изградити је мали асистент за политику школе. Користим два локална Markdown документа као базу знања, а затим пролазим кроз цео RAG процес: подела на делове, локална уграђивања (embeddings), Qdrant складиште вектора, преузимање, поновно рангирање, састављање одговора са познавањем извора и опционално локална генерација помоћу Ollama и Phi-4-mini.

Навигација кроз серију: [Почетак репозиторијума](../README.md) | Претходно: [Серија 1 - RAG, Azure против отворених алтернатива и када има смисла фино подешавање](./series-1-rag-azure-open-source-fine-tuning.md)

Бележница: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Захтеви: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Ово је најбоља почетна тачка ако желите да разумете RAG процес пре креирања облачних ресурса. Подразумевани пут ради локално са CPU-пријатељским уграђивањима и без тајни.

## 1. Шта градимо

У туторијалу из 2023. године почео сам од Azure јер је циљ био да се покаже како Azure AI Search и Azure OpenAI могу да одговарају на питања из PDF докумената.

За ову серију 2026. желим да почнем један слој ниже.

Пре коришћења управљаних сервиса, желим да локално изградим мали RAG систем и да учиним сваки корак видљивим: учитавање докумената, подела текста на делове, чување вектора, преузимање доказа, поновно рангирање резултата и враћање одговора са познавањем извора.

Пример сценарија је помоћник за политику школе. Корисник пита:

```text
Can I use generative AI for my final assignment?
```

Систем не би требало да одговара из опште меморије модела. Требало би да преузме релевантни одељак политике и одговори на основу тог доказа.

Цела извршна верзија је у [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Код испод показује главне кораке тако да се чланак може читати као туторијал.

## 2. Инсталирајте локалне зависности

Креирајте виртуелно окружење и инсталирајте захтеве за Серију 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Прва верзија користи Qdrant локални режим и FastEmbed. Qdrant Python клијент подржава меморијски локални режим са `QdrantClient(":memory:")`, што је корисно за локалне туторијале и CI врсту провере. FastEmbed нам даје стварни локални модел уграђивања без потребе за cloud API кључем.

Фајл захтева такође укључује `python-dotenv` јер бележница може опционално да учита име Ollama модела из `.env`. За овај локални туторијал није потребан Azure OpenAI или OpenAI API кључ.

## 3. Учитајте пример докумената

Пример корпуса је намерно мали:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

У бележници учитавам све Markdown фајлове из `sample_data/`:

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

Када сам покренуо бележницу, учитала су се 2 документа. То је довољно мало за ручну проверу, што је корисно када се гради прва верзија RAG процеса.

## 4. Поделите по Markdown насловима

Следећи корак је подела докумената на делове.

За овај туторијал користим Markdown наслове као сигнал структуре. Наслов документа је из `#`, а сваки одељак долази из `##`.

> [!NOTE]
> Подела није универзална. У овом туторијалу користим Markdown наслове јер примери докумената имају јасну структуру `#` и `##`. За PDF-ове, Word документе, слајдове, тикете или веб странице, боља стратегија може укључивати странице, информације о распореду, семантичке одељке, ограничења броја токена, табеле или метаподатке. Важно је одабрати стратегију дељења која чува значење и праћење извора у вашим документима.

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

Онда примењујем то на сваки документ:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Ово је у мом локалном покретању створило 8 делова.

Оно што ми се свидело код овог корака је да су метаподаци већ корисни. Сваком делу су познати његов `source`, `sectionHeading`, `documentVersion` и привремено `permissions`. Чак и у малом туторијалу ово олакшава референце и касније преузимање са свешћу о дозволама.

## 5. Креирајте локална уграђивања

За прву јавну верзију користим `BAAI/bge-small-en-v1.5` преко FastEmbed.

Ово задржава туторијал локалним и CPU-пријатељским, али и даље користи стварни модел уграђивања уместо функције места за векторе. Прво покретање преузима тежине модела. Након тога, бележница може да поново користи локални кеш.

> [!NOTE]
> Користим `BAAI/bge-small-en-v1.5` јер је то лагани енглески модел уграђивања који добро ради са FastEmbed и Qdrant за локални туторијал. Креира векторе димензија 384, што одржава пример брзим и јефтиним за локално покретање. Ово није једини добар избор. У 2023. многи туторијали користили су домаћене моделе уграђивања као што је `text-embedding-ada-002`. Данас су новије домаћене опције као што су OpenAI `text-embedding-3-small` и `text-embedding-3-large`, и отворене опције као што су BGE, E5, MiniLM, Nomic Embed и мултијезички модели као `BAAI/bge-m3` разумни избори у зависности од оптерећења. У продукцији, прави модел уграђивања треба изабрати кроз процену преузимања на сопственим документима.

Неколико практичних алтернатива:

| Породица модела | Када бих размотрилa |
| --- | --- |
| `text-embedding-ada-002` | Старија домаћена база која се појављивала у многим туторијалима из 2023. Ја то не бих изабрао као подразумевани за нови туторијал данас. |
| `text-embedding-3-small` | Модерна домаћа подразумевана опција када желим добар однос цене/перформанси и не требају ми само локална уграђивања. |
| `text-embedding-3-large` | Домаћа опција када је квалитет преузимања важнији од величине вектора или цене уграђивања. |
| `BAAI/bge-small-en-v1.5` | Лагани локални енглески базични модел за туторијале, прототипове и CPU-пријатељске експерименте. |
| `BAAI/bge-base-en-v1.5` или `BAAI/bge-large-en-v1.5` | Велики локални енглески модели када желим бољи квалитет преузимања и могу да приуштим више рачунске снаге. |
| `BAAI/bge-m3` | Мултијезично или преузимање са дужим контекстом, посебно када документи нису само на енглеском. |
| `sentence-transformers/all-MiniLM-L6-v2` | Веома мали и брзи базични модел за семантичко претраживање. Корисно када брзина и једноставност највише значе. |
| `nomic-embed-text-v1.5` | Отворена локална опција уграђивања вредна тестирања за подешавања са дугим контекстом или усмерена на преносивост. |

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

Онда сваки део добија уграђивање:

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

## 6. Сачувајте векторе у Qdrant локалном режиму

Сада креирамо Qdrant колекцију у меморији и убацујемо делове са метаподацима у трошку.

> [!NOTE]
> У туторијалу из 2023. користио сам FAISS јер је био једноставан и популаран начин да се демонстрира локална претрага векторске сличности са LangChain. FAISS је и даље користан за брзе локалне експерименте. У овој верзији из 2026. користим Qdrant јер желим да туторијал делује ближе продукционом RAG систему. Qdrant ми омогућава да чувам векторе заједно са метаподацима као што су изворни фајл, наслов одељка, верзија документа и дозволе. То олакшава инспекцију преузимања и припрема пример за филтрирање, референце и будуће упорне или серверске примене.

FAISS је сјајан за показивање претраге векторске сличности. Qdrant је бољи за приказивање малог али продукцијски обликуп RAG слоја преузимања.

Неколико практичних алтернатива:

| Складиште вектора / слој претраге | Када бих размотрилa |
| --- | --- |
| Qdrant | Локални прототипови, филтрирање метаподатака, продукцијски пријатељска претрага вектора и једноставан Python радни ток. |
| Chroma | Брзи локални RAG експерименти и бележнице где је једноставност најважнија. |
| FAISS | Лаган локални векторски претраживач када треба само претрага сличности и могу да управљам метаподацима одвојено. |
| Milvus | Већи отворени векторски претраживач за тимове спремне да користе посебну базу вектора. |
| Weaviate | Претрага вектора са шемом, метаподацима, хибридном претрагом и опцијама управљане или самосталне примене. |
| Azure AI Search | Ентерпрајс RAG на Azure када желим претрагу кључних речи, претрагу вектора, хибридно преузимање, семантичко рангирање, филтрирање, безбедност и управљане операције у једном слоју претраге. |
| PostgreSQL + pgvector | Тимови који већ користе PostgreSQL и желе претрагу вектора близу података апликације. |

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

Онда убацујем тачке:

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

У мом покретању, колекција је убацила 8 вектора.

Овде RAG систем почиње да постаје проверљив. Векторска база не само да чува векторе; она чува текст доказа и метаподацке потребне за референце.

## 7. Преузмите кандидатске делове

Сада постављамо питање и преузимамо кандидатске делове.

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

У овом тренутку штампам преузете делове пре генерисања одговора. Ово је важно. Ако је преузимање погрешно, генерисање ће само сакрити проблем иза течног текста.

## 8. Додајте лагани поновни рангирање

Када сам први пут тестирао пут преузимања, векторска сличност је пронашла повезани садржај политике, али најпрецизнији одељак није увек био на врху.

Зато сам додао мали локални поновни рангирање. Даје додатну тежину када се термини питања поклапају са насловом одељка и садржајем.

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

После поновног рангирања, врх резултата је постао:

```text
school_ai_policy.md / Final Assignments
```

То је био очекивани одељак за тест питање.

Ово је била најкориснија лекција из прве имплементације. Чак и у малом локалном примеру, квалитет преузимања се побољшао када сам комбиновала сличност вектора са другим сигналом.

## 9. Саставите локални одговор са упориштем

За подразумевани пут користим транспарентан локални састављач одговора уместо LLM.

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

Ово није намењено као генератор коначног одговора. То је алат за отклањање грешака. Докazuje да преузимање, метаподаци и повезивање референци раде пре додавања варијабилности модела.

## 10. Генеришите локални одговор помоћу Ollama и Phi-4-mini

Када преузимање ради, бележница може да замени само последњи корак одговора Ollama и `phi4-mini:3.8b`.

> [!NOTE]
> Ollama треба да замени само последњи корак генерисања одговора. Учитавање докумената, подела на делове, чување вектора, преузимање, поновно рангирање и повезивање референци треба да остану исти.

Прво, бележница прави знак за доказ из преузетих делова:

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

За овај туторијал препоручујем Microsoft-ову Phi-4-mini породицу преко Ollama као подразумевану локалну опцију генерисања. У Ollama, име модела који сам тестирао је:

```powershell
ollama pull phi4-mini:3.8b
```

Можете брзо проверити да ли је модел доступан:

```powershell
ollama list
```

Онда подесите ове променљиве:

```powershell
Copy-Item .env.example .env
```

Отворите `.env` и уклоните коментаре са вредности Ollama из Серије 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Бележница учитава `.env` из корена репозиторијума са `python-dotenv`, затим шаље исти доказни знак на локални Ollama `/api/chat` крајњу тачку са онемогућеним стримингом. Ако Ollama не ради или `SERIES2_OLLAMA_MODEL` недостаје, овај ток се заобиђе.

> [!NOTE]
> На овом рачунару, `phi4-mini:3.8b` је преузео око 2.49GB фајлова модела. Током инференције, Ollama је пријавио 3.3GB учитане величине модела и користио RTX 3060 лаптоп GPU.

Ово даје туторијалу два нивоа:

1. Детерминистички састављач одговора само на CPU-у.
2. Локална генерација одговора са Ollama и Phi-4-mini.

Поступак преузимања остаје исти у оба случаја.

## 11. Резултат верификације

Покренуо сам бележницу локално на Windows са Python 3.12.6.

Инсталирани пакети:

| Пакет | Верзија |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Извршење бележнице:

- Бележница: `notebooks/series-2-open-source-rag.ipynb`
- Резултат извршења: успешно са `nbclient`
- Учитани документи: 2
- Креирани делови: 8
- Qdrant колекција: `school_policy_local`
- Умештени вектори: 8
- Модел уграђивања: `BAAI/bge-small-en-v1.5`
- Величина уграђивања: 384
- Питање за преузимање: „Могу ли да користим генеративну вештачку интелигенцију за мој завршни задатак?“
- Путања за поновно рангирање: лагано локално лексичко поновно рангирање
- Најбољи извор након поновног рангирања: `school_ai_policy.md`
- Најбољи одељак након поновног рангирања: `Завршни задаци`
- Подразумевани пут за одговор: локални транспарентни композитор одговора
- Пут генерисања Оллама: завршен са `phi4-mini:3.8b`
- Величина моделске датотеке Оллама: 2.49GB на диску
- Учитавана величина модела Оллама: 3.3GB пријављено од стране `ollama ps`
- GPU оптерећење: 100% GPU пријављено од стране `ollama ps`
- Обзор коришћења графичке меморије након генерисања: око 3.5GB од 6GB коришћено на RTX 3060 Laptop GPU
- Извршење нотебука са кешираним FastEmbed моделом и омогућеним генерисањем Оллама: прошло за око 34 секунде кроз скрипту за верификацију

Одговор генерисан Олламом био је:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Не бих назвао овај одговор савршеним. Одговара на основу правих доказа, али последња линија извора је мање прецизна од детерминистичког формата цитирања. То је корисно приказати у туторијалу јер чини следеће питање за инжењеринг очигледним: генерисање одговора такође треба да се процењује, а не само преузимање.

Главна ствар коју сам научио током верификовања је да квалитет преузимања треба проверавати пре генерисања одговора. Резултат уграђивања је већ био користан, а лагани рангирач је учинио да се очекивани одељак о политици појави као први. То је управо врста малог понашања система коју желим да туторијал открије уместо да сакрије.

## 12. Шта следи

Следеће унапређење је да се ова локална поставка упореди са управљаном Azure верзијом истог сценарија школског помоћника за политику. Остављајући сценарио непомерен, трговине би требало да буду лакше видљиве: сложеност поставке, контроле преузимања, интеграција идентитета, оперативно власништво и трошкови.

## 13. Референце

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

Претходно: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Изјава о одрицању одговорности**:
Овај документ је преведен коришћењем услуге за аутоматски превод [Co-op Translator](https://github.com/Azure/co-op-translator). Иако тежимо тачности, имајте у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитативним извором. За критичне информације препоручује се професионални људски превод. Нисмо одговорни за било каква неспоразума или погрешна тумачења која произилазе из коришћења овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->