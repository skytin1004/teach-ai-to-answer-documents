# สอน AI ให้ตอบคำถามจากเอกสารของคุณ

ที่เก็บนี้รวบรวมชุดบล็อกปี 2026 เกี่ยวกับการสร้างระบบ AI ที่อิงเอกสารด้วย RAG, บริการ Azure AI, ทางเลือกแบบโอเพนซอร์ส และเวิร์กโฟลว์ที่มุ่งเน้นการประเมินผล

## เบื้องหลัง

ในปี 2023 ฉันได้ทำคู่มือสองชุดเกี่ยวกับการสอน ChatGPT ให้ตอบคำถามจากเอกสาร PDF โดยใช้ Azure AI Search และ Azure OpenAI แนวคิด "ChatGPT บนข้อมูลของคุณ" ยังดูใหม่ในเวลานั้น และเป้าหมายคือการแสดงเวิร์กโฟลว์ที่ใช้งานได้จริง: เก็บเอกสาร, ทำดัชนี, ดึงเนื้อหาที่เหมาะสม และสร้างคำตอบจากบริบทที่ดึงมา

ในปี 2026 ระบบนิเวศของ RAG มีขนาดใหญ่ขึ้นมาก Azure AI Search สนับสนุนรูปแบบการดึงข้อมูลเวกเตอร์และไฮบริดสมัยใหม่ Azure OpenAI เป็นส่วนหนึ่งของระบบนิเวศ Microsoft Foundry Models ที่กว้างขึ้น และเครื่องมือโอเพนซอร์ส เช่น LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama และ vLLM กลายเป็นตัวเลือกที่ใช้งานได้จริงสำหรับระบบจริง

นั่นคือเหตุผลที่ฉันต้องการกลับมาที่หัวข้อนี้อีกครั้ง คำถามไม่ใช่แค่ "ฉันจะสร้าง RAG ได้อย่างไร?" อีกต่อไป ตอนนี้มีหลายวิธีในการสร้าง และคำถามที่สำคัญกว่าคือ "ควรเลือกสถาปัตยกรรมแบบไหนสำหรับสถานการณ์ของฉัน?"

ชุดบทความนี้เริ่มต้นจากชั้นการตัดสินใจนั้น ก่อนที่จะลงลึกในการใช้งานจริง จะดูว่าทำไมบริการ AI ถึงต้องการการดึงข้อมูล, เมื่อใดที่บริการจัดการแบบ Azure มีเหตุผล, เมื่อใดที่ทางเลือกโอเพนซอร์สเหมาะสมกว่า และการปรับแต่งละเอียด (fine-tuning) เข้ากับภาพรวมอย่างไร

## บทความ

1. [ชุดบทความที่ 1: RAG, Azure กับทางเลือกโอเพนซอร์ส และเมื่อใดที่การปรับแต่งละเอียดเหมาะสม](./series-1-rag-azure-open-source-fine-tuning.md)

## รองรับหลายภาษา

### รองรับผ่าน Co-op Translator (อัตโนมัติและอัปเดตตลอดเวลา)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](./README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ต้องการโคลนแบบภายในเครื่องใช่ไหม?**
>
> ที่เก็บนี้รวมการแปลมากกว่า 50 ภาษา ซึ่งเพิ่มขนาดดาวน์โหลดอย่างมีนัยสำคัญ หากต้องการโคลนโดยไม่รวมการแปล ให้ใช้ sparse checkout:
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
> วิธีนี้จะให้ทุกอย่างที่คุณต้องใช้เพื่อทำคอร์สให้เสร็จด้วยความเร็วดาวน์โหลดที่เร็วกว่ามาก
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->