# สอน AI ให้ตอบคำถามตามเอกสารของคุณ

![ภาพรวมระบบ AI RAG ที่อิงเอกสาร](../../assets/images/readme-hero.svg)

ที่เก็บนี้รวบรวมชุดบล็อกประจำปี 2026 เกี่ยวกับการสร้างระบบ AI ที่อิงเอกสารด้วย RAG, บริการ Azure AI, ทางเลือกแบบโอเพนซอร์ส และเวิร์กโฟลว์ที่เน้นการประเมินผล

## ภูมิหลัง

ในปี 2023 ฉันทำงานเกี่ยวกับบทเรียนคู่หนึ่งเกี่ยวกับการสอน ChatGPT ให้ตอบคำถามจากเอกสาร PDF โดยใช้ Azure AI Search และ Azure OpenAI แนวคิดของ "ChatGPT บนข้อมูลของคุณ" ยังดูใหม่ในตอนนั้น และเป้าหมายคือต้องการแสดงเวิร์กโฟลว์ที่ใช้งานได้จริง: จัดเก็บเอกสาร ดัชนีเอกสาร ดึงเนื้อหาที่เกี่ยวข้อง และสร้างคำตอบจากบริบทที่ดึงมาได้

ในปี 2026 ระบบนิเวศ RAG มีขนาดใหญ่ขึ้นมาก Azure AI Search รองรับรูปแบบการค้นหาด้วยเวกเตอร์และการผสมผสานที่ทันสมัย Azure OpenAI เป็นส่วนหนึ่งของระบบโมเดล Microsoft Foundry ที่กว้างขึ้น และเครื่องมือโอเพนซอร์สอย่าง LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, และ vLLM กลายเป็นตัวเลือกที่ใช้งานได้จริงสำหรับระบบจริง

นั่นคือเหตุผลที่ฉันอยากกลับมาพูดคุยเรื่องนี้อีกครั้ง คำถามไม่ได้เป็นแค่ "ฉันจะสร้าง RAG อย่างไร?" อีกต่อไป แต่มีหลายวิธีในการสร้าง และคำถามที่สำคัญกว่าคือ "ควรเลือกสถาปัตยกรรมใดสำหรับสถานการณ์ของฉัน?"

ชุดบทความนี้เริ่มจากชั้นการตัดสินใจนั้น จากนั้นเปลี่ยนเป็นบทเรียนแบบปฏิบัติ เส้นทางการใช้งานครั้งแรกคือการสร้างระบบ RAG แบบโอเพนซอร์สภายในเครื่องที่ใครก็สามารถรันได้ด้วยข้อมูลตัวอย่าง, Qdrant, Ollama, และ Phi-4-mini

## บทความ

ดูที่ [articles/README.md](./articles/README.md) สำหรับดัชนีบทความ

1. [ชุดที่ 1: RAG, Azure กับทางเลือกแบบโอเพนซอร์ส และเมื่อใดควรปรับโมเดล](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [ชุดที่ 2: สร้างระบบ RAG แบบโอเพนซอร์สในเครื่องตั้งแต่ต้นจนจบ](./articles/series-2-open-source-rag-end-to-end.md)

กำลังจะตามมา:

- สร้างระบบ RAG เดิมอีกครั้งด้วย Azure AI Search และ Azure OpenAI
- เพิ่มการประเมินและตรวจสอบการถดถอยนอกเหนือจากคำตอบตัวอย่าง

## โน้ตบุ๊ก

บทความการใช้งานใช้โน้ตบุ๊กเพื่อให้ขั้นตอนการค้นหาและการประเมินผลสามารถตรวจสอบได้โดยตรง ดูที่ [notebooks/README.md](./notebooks/README.md) สำหรับคำแนะนำระดับโฟลเดอร์

> [!TIP]
> เริ่มจากชุดที่ 2 หากคุณต้องการเส้นทางที่เร็วที่สุด มันรันในเครื่องด้วยข้อมูลตัวอย่าง, การฝังแบบประหยัดซีพียู, โหมดท้องถิ่นของ Qdrant, และไม่มีการใช้ข้อมูลรับรองบนคลาวด์

| ชุด | โน้ตบุ๊ก | ความต้องการ | การตรวจสอบในเครื่อง |
| --- | --- | --- | --- |
| ชุดที่ 2 | [โน้ตบุ๊ก RAG แบบโอเพนซอร์ส](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | ตรวจสอบโหมดท้องถิ่นของ Qdrant, การค้นหา, การจัดอันดับใหม่ และการเชื่อมต่อแหล่งที่มาแล้ว |

เพื่อรันโน้ตบุ๊กในเครื่อง สร้าง virtual environment และติดตั้งไฟล์ความต้องการที่ตรงกัน เช่น:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## ข้อมูลตัวอย่าง

โน้ตบุ๊กใช้กลุ่มข้อมูลท้องถิ่นขนาดเล็กที่ [sample_data](../../sample_data) เพื่อให้ตัวอย่างสามารถรันได้โดยไม่ต้องใช้เอกสารส่วนตัวหรือข้อมูลรับรองบนคลาวด์ ดูที่ [sample_data/README.md](./sample_data/README.md) สำหรับรายละเอียด

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## สรุปการตรวจสอบในเครื่อง

ผลการตรวจสอบถูกบันทึกไว้ในแต่ละบทความและใน [SERIES_PLAN.md](./SERIES_PLAN.md)

| หัวข้อ | ผลลัพธ์ |
| --- | --- |
| เส้นทางโอเพนซอร์สชุดที่ 2 | FastEmbed สร้าง embedding 384 มิติในเครื่อง, คอลเลกชันในหน่วยความจำของ Qdrant ใส่เวกเตอร์ 8 ตัว, การจัดอันดับใหม่แบบเบา ๆ ดึงส่วนที่คาดหวังมา; การสร้างผลลัพธ์ด้วย Ollama ที่เลือกได้เสร็จสมบูรณ์ด้วย `phi4-mini:3.8b` |

โน้ตบุ๊กในเครื่องหลีกเลี่ยงการใช้ความลับที่ระบุแบบเข้มงวดโดยเจตนา

## การสร้างผลลัพธ์ Ollama ในเครื่อง

โน้ตบุ๊กชุดที่ 2 ปลอดภัยสำหรับใช้งานในเครื่องโดยค่าเริ่มต้น หากต้องการเปิดใช้งานการสร้างผลลัพธ์ Ollama ในเครื่อง ให้คัดลอกไฟล์ [.env.example](../../.env.example) เป็น `.env` และกรอกข้อมูลสำหรับชุดที่ 2

สำหรับการสร้าง Ollama ชุดที่ 2 ให้ Uncomment:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

โน้ตบุ๊กชุดที่ 2 โหลด `.env` จากรากของที่เก็บโดยอัตโนมัติโดยใช้ `python-dotenv`

> [!IMPORTANT]
> กรุณาอย่าคอมมิตไฟล์ `.env` คีย์ API, จุดเชื่อมต่อส่วนตัว หรือค่าที่เจาะจงกับผู้เช่า ที่เก็บนี้เจตนาที่จะเก็บความลับออกจากไฟล์ Markdown และโน้ตบุ๊ก

ไฟล์ความต้องการถูกบันทึกไว้ใน [requirements/README.md](./requirements/README.md)

เพื่อยืนยันลิงก์ โครงสร้างโน้ตบุ๊ก ความสะอาดของผลลัพธ์ในโน้ตบุ๊ก และรูปแบบความลับที่มีความเสี่ยงสูง:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

สคริปต์ตรวจสอบถูกบันทึกไว้ใน [scripts/README.md](./scripts/README.md)

เพื่อรันโน้ตบุ๊กที่ปลอดภัยในเครื่องทั้งหมดในสภาพแวดล้อมเดียวกัน:

```powershell
python scripts\verify_notebooks.py --execute
```

เวิร์กโฟลว์ตรวจสอบเดียวกันนี้รันใน GitHub Actions เมื่อมีการ push, pull request และ manual workflow dispatch บทความร่างและโน้ตบุ๊กถูกตั้งใจไม่รวมอยู่ในเส้นทางตรวจสอบสาธารณะ

ก่อนเผยแพร่การอัปเดต ให้ใช้ [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)

ดูสรุปการเปลี่ยนแปลงที่ยังไม่เผยแพร่ใน [CHANGELOG.md](./CHANGELOG.md)

สำหรับคำแนะนำการมีส่วนร่วมและรักษาความสะอาดของโน้ตบุ๊ก ดูที่ [CONTRIBUTING.md](./CONTRIBUTING.md)

## การรองรับหลายภาษา

### รองรับผ่าน Co-op Translator (อัตโนมัติและอัปเดตเสมอ)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[อาหรับ](../ar/README.md) | [เบงกาลี](../bn/README.md) | [บัลแกเรีย](../bg/README.md) | [พม่า (เมียนมาร์)](../my/README.md) | [จีน (ตัวย่อ)](../zh-CN/README.md) | [จีน (ตัวเต็ม ฮ่องกง)](../zh-HK/README.md) | [จีน (ตัวเต็ม มาเก๊า)](../zh-MO/README.md) | [จีน (ตัวเต็ม ไต้หวัน)](../zh-TW/README.md) | [โครเอเชีย](../hr/README.md) | [เช็ก](../cs/README.md) | [เดนมาร์ก](../da/README.md) | [ดัตช์](../nl/README.md) | [เอสโตเนีย](../et/README.md) | [ฟินแลนด์](../fi/README.md) | [ฝรั่งเศส](../fr/README.md) | [เยอรมัน](../de/README.md) | [กรีก](../el/README.md) | [ฮีบรู](../he/README.md) | [ฮินดี](../hi/README.md) | [ฮังการี](../hu/README.md) | [อินโดนีเซีย](../id/README.md) | [อิตาลี](../it/README.md) | [ญี่ปุ่น](../ja/README.md) | [กันนาดา](../kn/README.md) | [เขมร](../km/README.md) | [เกาหลี](../ko/README.md) | [ลิทัวเนีย](../lt/README.md) | [มาเลย์](../ms/README.md) | [มาลายาลัม](../ml/README.md) | [มราฐี](../mr/README.md) | [เนปาล](../ne/README.md) | [นิจีเรีย พิดจิน](../pcm/README.md) | [นอร์เวย์](../no/README.md) | [เปอร์เซีย (ฟาร์ซี)](../fa/README.md) | [โปแลนด์](../pl/README.md) | [โปรตุเกส (บราซิล)](../pt-BR/README.md) | [โปรตุเกส (โปรตุเกส)](../pt-PT/README.md) | [ปัญจาบี (กุรมุขิ)](../pa/README.md) | [โรมาเนีย](../ro/README.md) | [รัสเซีย](../ru/README.md) | [เซอร์เบีย (ซีริลลิก)](../sr/README.md) | [สโลวัก](../sk/README.md) | [สโลเวเนีย](../sl/README.md) | [สเปน](../es/README.md) | [สวาฮิลี](../sw/README.md) | [สวีเดน](../sv/README.md) | [ทากาล็อก (ฟิลิปปินส์)](../tl/README.md) | [ทมิฬ](../ta/README.md) | [เทลูกู](../te/README.md) | [ไทย](./README.md) | [ตุรกี](../tr/README.md) | [ยูเครน](../uk/README.md) | [อูรดู](../ur/README.md) | [เวียดนาม](../vi/README.md)

> **ต้องการโคลนแบบโลคอล?**
>
> ที่เก็บนี้รวมการแปลมากกว่า 50 ภาษา ซึ่งเพิ่มขนาดดาวน์โหลดอย่างมาก หากต้องการโคลนโดยไม่รวมการแปล ให้ใช้ sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> วิธีนี้จะให้ทุกอย่างที่คุณต้องการเพื่อทำหลักสูตรให้เสร็จเร็วขึ้นมาก
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->