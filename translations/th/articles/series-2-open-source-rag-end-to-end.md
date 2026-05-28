# สอน AI ให้ตอบคำถามโดยอ้างอิงจากเอกสารของคุณ
## ซีรีส์ 2: สร้างระบบ RAG แบบโอเพนซอร์สในเครื่องครบวงจร

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> บทความนี้จะเปลี่ยนการพูดคุยเรื่องสถาปัตยกรรมในซีรีส์ 1 ให้กลายเป็นบทเรียน RAG แบบรันได้ในเครื่อง เป้าหมายคือการสร้าง workflow ทั้งหมดก่อนด้วยข้อมูลตัวอย่าง ไม่ต้องใช้บัญชีคลาวด์และไม่ต้องใช้ความลับ จากนั้นใช้เส้นฐานที่ทำงานได้นี้เพื่อช่วยตัดสินใจเรื่องสถาปัตยกรรมให้ดีขึ้นในภายหลัง

ระบบที่เราจะสร้างเป็นผู้ช่วยนโยบายโรงเรียนขนาดเล็ก ฉันใช้เอกสาร Markdown 2 ฉบับในเครื่องเป็นฐานความรู้ แล้วเดินผ่าน pipeline RAG ทั้งหมด: การแบ่งชิ้นข้อมูล, embedding ในเครื่อง, การเก็บข้อมูลเวกเตอร์ Qdrant, การดึงข้อมูล, การจัดอันดับใหม่, การแต่งคำตอบที่รับรู้แหล่งที่มา และการสร้างคำตอบแบบท้องถิ่นทางเลือกด้วย Ollama และ Phi-4-mini

นำทางซีรีส์: [หน้าแรกของ Repository](../README.md) | ก่อนหน้า: [ซีรีส์ 1 - RAG, Azure vs Open-Source Alternatives, and When Fine-Tuning Makes Sense](./series-1-rag-azure-open-source-fine-tuning.md)

โน้ตบุ๊ก: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | ความต้องการระบบ: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> นี่คือตำแหน่งเริ่มต้นที่ดีที่สุดถ้าคุณต้องการเข้าใจ pipeline RAG ก่อนสร้างทรัพยากรบนคลาวด์ เส้นทางปกติรันในเครื่องด้วย embedding ที่เหมาะกับ CPU และไม่ต้องใช้ความลับใดๆ

## 1. สิ่งที่เรากำลังสร้าง

ในบทเรียนปี 2023 ฉันเริ่มจาก Azure เพราะเป้าหมายคือแสดงให้เห็นว่า Azure AI Search และ Azure OpenAI สามารถตอบคำถามจากเอกสาร PDF ได้อย่างไร

สำหรับซีรีส์ปี 2026 นี้ ฉันต้องการเริ่มที่ระดับลึกกว่านั้น

ก่อนจะใช้บริการที่จัดการแล้ว ฉันต้องการสร้างระบบ RAG ขนาดเล็กในเครื่องและทำให้ทุกขั้นตอนมองเห็นได้: การโหลดเอกสาร, การแบ่งชิ้นข้อความ, การเก็บเวกเตอร์, การดึงข้อมูลหลักฐาน, การจัดอันดับใหม่ผลลัพธ์, และการคืนคำตอบที่รู้จักแหล่งที่มา

สถานการณ์ตัวอย่างคือผู้ช่วยนโยบายโรงเรียน ผู้ใช้ถามว่า:

```text
Can I use generative AI for my final assignment?
```

ระบบไม่ควรตอบคำถามจากความทรงจำของโมเดลทั่วไป แต่ควรดึงส่วนของนโยบายที่เกี่ยวข้องและตอบคำถามจากหลักฐานนั้น

เวอร์ชันที่รันได้ทั้งหมดอยู่ใน [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) โค้ดด้านล่างแสดงขั้นตอนหลักเพื่อให้บทความนี้อ่านเป็นบทเรียนได้

## 2. ติดตั้ง Dependencies ในเครื่อง

สร้างสภาพแวดล้อมเสมือนและติดตั้งความต้องการของซีรีส์ 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

เวอร์ชันแรกใช้โหมด Qdrant ในเครื่องและ FastEmbed ลูกค้า Python ของ Qdrant รองรับโหมดในหน่วยความจำด้วย `QdrantClient(":memory:")` ซึ่งเหมาะสำหรับบทเรียนในเครื่องและการตรวจสอบแบบ CI FastEmbed ให้โมเดล embedding ในเครื่องจริงโดยไม่ต้องใช้คีย์ API คลาวด์

ไฟล์ความต้องการยังรวม `python-dotenv` เพราะโน้ตบุ๊กสามารถอ่านชื่อโมเดล Ollama จาก `.env` ได้โดยเลือก ไม่ต้องใช้คีย์ Azure OpenAI หรือ OpenAI สำหรับบทเรียนนี้ในเครื่อง

## 3. โหลดเอกสารตัวอย่าง

ชุดข้อมูลตัวอย่างมีขนาดเล็กโดยเจตนา:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

ในโน้ตบุ๊ก ฉันโหลดไฟล์ Markdown ทั้งหมดจาก `sample_data/`:

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

ตอนที่รันโน้ตบุ๊ก มันโหลดเอกสารได้ 2 ฉบับ เล็กพอที่จะตรวจสอบด้วยตนเอง ซึ่งมีประโยชน์เมื่อสร้างเวอร์ชันแรกของ pipeline RAG

## 4. แบ่งชิ้นด้วยหัวเรื่อง Markdown

ขั้นตอนถัดไปคือแยกเอกสารเป็นชิ้นๆ

สำหรับบทเรียนนี้ ฉันใช้หัวเรื่อง Markdown เป็นสัญญาณโครงสร้าง ชื่อเอกสารมาจาก `#` และแต่ละชิ้นส่วนของส่วนหัวมาจาก `##`

> [!NOTE]
> การแบ่งชิ้นไม่ได้เหมือนกันหมดทุกกรณี ในบทเรียนนี้ ฉันใช้หัวเรื่อง Markdown เพราะเอกสารตัวอย่างมีโครงสร้าง `#` และ `##` ชัดเจน สำหรับ PDF, เอกสาร Word, สไลด์, ตั๋วงาน หรือเว็บเพจ อาจใช้วิธีการดีกว่าที่รวมขอบเขตหน้ากระดาษ, ข้อมูลเลย์เอาต์, ส่วนความหมาย, ขีดจำกัดโทเค็น, ตาราง หรือข้อมูลเมตา จุดสำคัญคือเลือกวิธีแบ่งชิ้นที่รักษาความหมายและสามารถสืบย้อนแหล่งที่มาได้ในเอกสารของคุณ

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

จากนั้นนำไปใช้กับเอกสารทุกฉบับ:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

ผลลัพธ์คือสร้างชิ้นข้อมูล 8 ชิ้นในรันของฉัน

สิ่งที่ฉันชอบในขั้นตอนนี้คือ metadata มีประโยชน์แล้ว ชิ้นข้อมูลแต่ละชิ้นรู้จัก `source`, `sectionHeading`, `documentVersion` และสถานะจำลอง `permissions` แม้ในบทเรียนน้อยนี้ก็ช่วยให้การอ้างอิงและการดึงข้อมูลที่รับรู้สิทธิ์ในภายหลังง่ายขึ้น

## 5. สร้าง Embedding ในเครื่อง

สำหรับเวอร์ชันสาธารณะแรก ฉันใช้ `BAAI/bge-small-en-v1.5` ผ่าน FastEmbed

สิ่งนี้ทำให้บทเรียนรันในเครื่องและเหมาะกับ CPU แต่ยังใช้โมเดล embedding จริง แทนฟังก์ชันเวกเตอร์จำลอง การรันครั้งแรกจะดาวน์โหลดน้ำหนักโมเดล หลังจากนั้นโน้ตบุ๊กสามารถใช้แคชในเครื่องได้ซ้ำ

> [!NOTE]
> ฉันเลือก `BAAI/bge-small-en-v1.5` เพราะเป็นโมเดล embedding ภาษาอังกฤษที่น้ำหนักเบา ใช้ได้ดีร่วมกับ FastEmbed และ Qdrant สำหรับบทเรียนในเครื่อง มันสร้างเวกเตอร์ขนาด 384 มิติ ทำให้อย่างนี้เร็วและประหยัดสำหรับรันในเครื่อง นี่ไม่ใช่ทางเลือกเดียวที่ดี ในปี 2023 บทเรียนหลายชุดใช้โมเดล embedding ที่โฮสต์ เช่น `text-embedding-ada-002` ปัจจุบันตัวเลือกโฮสต์ใหม่อย่าง OpenAI `text-embedding-3-small` และ `text-embedding-3-large` รวมถึงตัวเลือกโอเพนซอร์สเช่น BGE, E5, MiniLM, Nomic Embed และโมเดลหลายภาษาอย่าง `BAAI/bge-m3` ต่างเหมาะสมขึ้นอยู่กับภาระงาน ในการใช้งานจริง ควรเลือกโมเดล embedding ที่เหมาะสมโดยการประเมินการดึงข้อมูลในเอกสารของคุณเอง

ทางเลือกที่ใช้งานได้จริง:

| ตระกูลโมเดล | เมื่อไหร่ที่ฉันจะพิจารณาใช้ |
| --- | --- |
| `text-embedding-ada-002` | เป็น baseline ที่โฮสต์เก่าที่ปรากฏในบทเรียนหลายชุดของปี 2023 ฉันจะไม่เลือกเป็นค่าเริ่มต้นสำหรับบทเรียนใหม่ในวันนี้ |
| `text-embedding-3-small` | ค่าเริ่มต้นสมัยใหม่ที่โฮสต์สำหรับผู้ที่ต้องการสมดุลค่าใช้จ่าย/ประสิทธิภาพดีและไม่จำเป็นต้อง embedding เฉพาะในเครื่อง |
| `text-embedding-3-large` | ตัวเลือกโฮสต์เมื่อคุณภาพการดึงข้อมูลสำคัญกว่าขนาดเวกเตอร์หรือค่า embedding |
| `BAAI/bge-small-en-v1.5` | ค่าเริ่มต้นภาษาอังกฤษน้ำหนักเบาในเครื่องสำหรับบทเรียน ต้นแบบ และทดลองที่เหมาะกับ CPU |
| `BAAI/bge-base-en-v1.5` หรือ `BAAI/bge-large-en-v1.5` | โมเดลภาษาอังกฤษในเครื่องขนาดใหญ่ขึ้นเมื่อคุณต้องการคุณภาพการดึงสูงกว่าและมีทรัพยากรมากพอ |
| `BAAI/bge-m3` | ดึงข้อมูลหลายภาษาหรือบริบทยาว โดยเฉพาะเอกสารที่ไม่ใช่ภาษาอังกฤษเท่านั้น |
| `sentence-transformers/all-MiniLM-L6-v2` | baseline การค้นหาความหมายขนาดเล็กและรวดเร็ว เหมาะเมื่อเน้นความเร็วและความเรียบง่ายที่สุด |
| `nomic-embed-text-v1.5` | ตัวเลือก embedding ในเครื่องแบบเปิดที่น่าสนใจสำหรับการทดสอบบริบทยาวหรือเซ็ตอัพที่เน้นพกพา |

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

จากนั้นแต่ละชิ้นข้อมูลจะได้รับ embedding:

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

## 6. เก็บเวกเตอร์ในโหมด Qdrant ท้องถิ่น

ตอนนี้เราสร้างคอลเลกชัน Qdrant ในหน่วยความจำและแทรกชิ้นข้อมูลพร้อม metadata payload

> [!NOTE]
> ในบทเรียนปี 2023 ฉันใช้ FAISS เพราะมันง่ายและนิยมสำหรับแสดงการค้นหาเวกเตอร์ในเครื่องร่วมกับ LangChain FAISS ยังมีประโยชน์สำหรับทดลองในเครื่องอย่างรวดเร็ว สำหรับเวอร์ชันปี 2026 นี้ ฉันใช้ Qdrant เพราะอยากให้บทเรียนรู้สึกใกล้เคียงกับระบบ RAG ในการผลิต Qdrant อนุญาตให้จัดเก็บเวกเตอร์ควบคู่กับ metadata เช่น ไฟล์ต้นทาง หัวข้อส่วน เวอร์ชันเอกสาร และสิทธิ์การใช้งาน ทำให้การดึงข้อมูลง่ายตรวจสอบและพร้อมสำหรับการกรอง อ้างอิง และการเผยแพร่แบบถาวรหรือบนเซิร์ฟเวอร์ในอนาคต

FAISS เหมาะในการแสดงการค้นหาเวกเตอร์ที่คล้ายกัน Qdrant เหมาะสำหรับแสดงชั้นดึงข้อมูล RAG เล็กแต่เหมือนผลิตจริง

ทางเลือกที่ใช้งานได้จริง:

| ชั้นเก็บเวกเตอร์ / การค้นหา | เมื่อไหร่ที่ฉันจะพิจารณาใช้ |
| --- | --- |
| Qdrant | ต้นแบบในเครื่อง, การกรอง metadata, การค้นหาเวกเตอร์แบบเหมาะกับการผลิต และ workflow Python ง่ายๆ |
| Chroma | ทดลอง RAG ในเครื่องแบบรวดเร็ว และโน้ตบุ๊กที่เน้นความเรียบง่ายมากที่สุด |
| FAISS | การค้นหาเวกเตอร์ในเครื่องขนาดเบาเมื่อฉันแค่อยากได้ความเหมือนกันและจัดการ metadata แยกต่างหากได้ |
| Milvus | การค้นหาเวกเตอร์โอเพนซอร์สขนาดใหญ่เมื่อต้องการทีมที่พร้อมบริหารฐานข้อมูลเวกเตอร์เฉพาะ |
| Weaviate | การค้นหาเวกเตอร์พร้อม schema, metadata, การค้นหาแบบผสม และตัวเลือกเผยแพร่แบบจัดการหรือเซิร์ฟเวอร์เอง |
| Azure AI Search | RAG สำหรับธุรกิจบน Azure เมื่อฉันต้องการการค้นหาคีย์เวิร์ด, การค้นหาเวกเตอร์, การดึงข้อมูลแบบผสม, การจัดอันดับความหมาย, การกรอง, ความปลอดภัย และการบริหารจัดการในชั้นค้นหาเดียว |
| PostgreSQL + pgvector | ทีมที่ใช้ PostgreSQL อยู่แล้วและต้องการการค้นหาเวกเตอร์ใกล้กับข้อมูลแอปพลิเคชัน |

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

จากนั้นแทรกจุดข้อมูล:

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

ในรันของฉัน คอลเลกชันแทรกเวกเตอร์ได้ 8 จุด

ตอนนี้ระบบ RAG เริ่มตรวจสอบได้ ฐานข้อมูลเวกเตอร์ไม่ได้เก็บแค่เวกเตอร์ แต่ยังเก็บข้อความหลักฐานและ metadata ที่ใช้สำหรับอ้างอิง

## 7. ดึงชิ้นข้อมูลที่เป็นตัวอย่าง

ตอนนี้เราถามคำถามและดึงชิ้นข้อมูลที่เป็นตัวอย่าง

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

ในจุดนี้ ฉันพิมพ์ชิ้นที่ดึงก่อนสร้างคำตอบ นี่สำคัญมาก ถ้าการดึงผิด การสร้างคำตอบจะแค่ซ่อนปัญหาไว้หลังข้อความเรียบลื่น

## 8. เพิ่มตัวจัดอันดับใหม่ขนาดเล็ก

ตอนที่ฉันทดสอบเส้นทางดึงข้อมูลครั้งแรก ความเหมือนเวกเตอร์อย่างเดียวพบเนื้อหานโยบายที่เกี่ยวข้อง แต่ส่วนที่แม่นยำที่สุดไม่เสมอไปอยู่บนสุด

ดังนั้นฉันเพิ่มตัวจัดอันดับขนาดเล็กในเครื่อง มันให้น้ำหนักพิเศษเมื่อคำถามตรงกับหัวเรื่องส่วนและเนื้อหา

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

หลังจัดอันดับใหม่ ผลลัพธ์ด้านบนกลายเป็น:

```text
school_ai_policy.md / Final Assignments
```

นั่นคือส่วนที่คาดไว้สำหรับคำถามทดสอบ

นี่คือบทเรียนที่มีประโยชน์ที่สุดจากการใช้งานครั้งแรก แม้ในตัวอย่างท้องถิ่นเล็ก ๆ คุณภาพการดึงข้อมูลดีขึ้นเมื่อผสมสัญญาณความเหมือนเวกเตอร์กับสัญญาณอื่น

## 9. แต่งคำตอบในเครื่องโดยมีแหล่งที่มากำกับ

สำหรับเส้นทางปกติ ฉันใช้ตัวแต่งคำตอบในเครื่องที่โปร่งใสแทน LLM

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

นี่ไม่ใช่ตัวสร้างคำตอบขั้นสุดท้าย แต่เป็นเครื่องมือดีบัก มันทดสอบว่าการดึงข้อมูล, metadata, และการเชื่อมโยงอ้างอิงทำงานก่อนเพิ่มความแปรปรวนของโมเดล

## 10. สร้างคำตอบท้องถิ่นด้วย Ollama และ Phi-4-mini

เมื่อการดึงข้อมูลทำงานได้ โน้ตบุ๊กสามารถแทนที่ขั้นตอนสร้างคำตอบสุดท้ายด้วย Ollama และ `phi4-mini:3.8b`

> [!NOTE]
> Ollama ควรแทนที่เฉพาะขั้นตอนสร้างคำตอบเท่านั้น การโหลดเอกสาร, การแบ่งชิ้น, การเก็บเวกเตอร์, การดึงข้อมูล, การจัดอันดับใหม่ และการเชื่อมโยงอ้างอิงควรเหมือนเดิม

แรกสุด โน้ตบุ๊กจะสร้าง prompt หลักฐานจากชิ้นข้อมูลที่ดึงมา:

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

สำหรับบทเรียนนี้ ฉันแนะนำใช้อังกฤษ Phi-4-mini ของ Microsoft ผ่าน Ollama เป็นตัวเลือกสร้างคำตอบในเครื่องแบบเริ่มต้น ชื่อโมเดลที่ฉันทดสอบใน Ollama คือ:

```powershell
ollama pull phi4-mini:3.8b
```

คุณสามารถตรวจสอบว่าโมเดลพร้อมใช้งานได้อย่างรวดเร็ว:

```powershell
ollama list
```

จากนั้นตั้งค่าตัวแปรเหล่านี้:

```powershell
Copy-Item .env.example .env
```

เปิดไฟล์ `.env` และปลดคอมเมนต์ค่าของ Ollama สำหรับซีรีส์ 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

โน้ตบุ๊กโหลด `.env` จาก repository root ด้วย `python-dotenv` แล้วส่ง prompt หลักฐานเดียวกันไปยังจุดสิ้นสุด `/api/chat` ของ Ollama ในเครื่องโดยปิดสตรีมมิง ถ้า Ollama ไม่ได้รันหรือไม่มี `SERIES2_OLLAMA_MODEL` ช่องทางนี้จะถูกข้าม

> [!NOTE]
> บนเครื่องนี้ `phi4-mini:3.8b` ดาวน์โหลดไฟล์โมเดลประมาณ 2.49GB ในระหว่างประมวลผล Ollama รายงานขนาดโมเดลที่โหลดเป็น 3.3GB และใช้ RTX 3060 Laptop GPU

บทเรียนนี้มีสองระดับ:

1. ตัวแต่งคำตอบแบบกำหนดได้โดย CPU เท่านั้น
2. การสร้างคำตอบในเครื่องด้วย Ollama และ Phi-4-mini

pipeline การดึงข้อมูลเหมือนเดิมทั้งสองระดับ

## 11. ผลลัพธ์การตรวจสอบ

ฉันรันโน้ตบุ๊กในเครื่องบน Windows ด้วย Python 3.12.6

แพ็กเกจที่ติดตั้ง:

| แพ็กเกจ | เวอร์ชัน |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

การรันโน้ตบุ๊ก:

- โน้ตบุ๊ก: `notebooks/series-2-open-source-rag.ipynb`
- ผลลัพธ์การรัน: ผ่านด้วย `nbclient`
- เอกสารที่โหลด: 2 ฉบับ
- ชิ้นที่สร้าง: 8 ชิ้น
- คอลเลกชัน Qdrant: `school_policy_local`
- เวกเตอร์ที่แทรก: 8 จุด
- โมเดล embedding: `BAAI/bge-small-en-v1.5`
- ขนาด embedding: 384
- คำถามการค้นคืน: "ฉันสามารถใช้ AI สร้างสรรค์สำหรับการมอบหมายงานสุดท้ายของฉันได้หรือไม่?"
- เส้นทางการจัดลำดับใหม่: การจัดลำดับใหม่แบบเล็กน้อยโดยใช้คำศัพท์ในเครื่อง
- แหล่งข้อมูลที่ค้นคืนอันดับต้นหลังจากจัดลำดับใหม่: `school_ai_policy.md`
- ส่วนที่ค้นพบอันดับต้นหลังจากจัดลำดับใหม่: `Final Assignments`
- เส้นทางคำตอบเริ่มต้น: ตัวประมวลผลคำตอบในเครื่องที่โปร่งใส
- เส้นทางการสร้างคำตอบ Ollama: เสร็จสิ้นด้วย `phi4-mini:3.8b`
- ขนาดไฟล์โมเดล Ollama: 2.49GB บนดิสก์
- ขนาดโมเดลที่โหลดของ Ollama: 3.3GB รายงานโดย `ollama ps`
- การปล่อยโหลดบน GPU: รายงาน 100% GPU โดย `ollama ps`
- หน่วยความจำ GPU ที่สังเกตหลังการสร้าง: ใช้ประมาณ 3.5GB จาก 6GB บน RTX 3060 Laptop GPU
- การรันโน้ตบุ๊กพร้อมโมเดล FastEmbed ที่แคชไว้และเปิดใช้การสร้าง Ollama: ผ่านในประมาณ 34 วินาทีผ่านสคริปต์ตรวจสอบ

คำตอบที่สร้างโดย Ollama คือ:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

ฉันจะไม่เรียกคำตอบนี้ว่าเป็นคำตอบที่สมบูรณ์แบบ มันตอบจากหลักฐานที่ถูกต้อง แต่บรรทัดแหล่งที่มาสุดท้ายไม่แม่นยำเท่ากับรูปแบบการอ้างอิงแบบกำหนดตายตัว นั่นมีประโยชน์ที่จะโชว์ในบทเรียนเพราะมันทำให้คำถามวิศวกรรมถัดไปชัดเจน: การสร้างคำตอบก็ต้องมีการประเมินผลด้วย ไม่ใช่แค่การค้นคืนเท่านั้น

สิ่งสำคัญที่ฉันได้เรียนรู้ขณะตรวจสอบนี้คือคุณภาพของการค้นคืนควรตรวจสอบก่อนการสร้างคำตอบ ผลลัพธ์การฝังตัว (embedding) นั้นมีประโยชน์แล้ว และตัวจัดลำดับเบา ๆ ช่วยให้ส่วนที่เป็นนโยบายที่คาดหวังแสดงขึ้นมาเป็นอันดับแรกอย่างน่าเชื่อถือ นั่นคือพฤติกรรมระบบเล็ก ๆ ที่ฉันอยากให้บทเรียนนำเสนอแทนที่จะซ่อนมันไว้

## 12. สิ่งที่จะตามมา

การปรับปรุงถัดไปคือการเปรียบเทียบการตั้งค่าในเครื่องนี้กับเวอร์ชัน Azure ที่มีการจัดการสำหรับสถานการณ์ผู้ช่วยนโยบายโรงเรียนเดียวกัน การรักษาสถานการณ์ให้คงที่จะทำให้เห็นข้อแลกเปลี่ยนได้ง่ายขึ้น: ความซับซ้อนในการตั้งค่า การควบคุมการค้นคืน การผนวกตัวตน ความเป็นเจ้าของปฏิบัติการ และค่าใช้จ่าย

## 13. เอกสารอ้างอิง

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

ก่อนหน้า: [ชุดที่ 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->