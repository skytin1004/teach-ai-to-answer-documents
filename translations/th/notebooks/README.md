# Notebooks

สมุดบันทึกเหล่านี้สนับสนุนชุดบทความพร้อมตัวอย่างที่สามารถรันได้

| Notebook | บทความ | จุดประสงค์ |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [ชุดที่ 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG แบบโอเพ่นซอร์สที่ใช้ FastEmbed, โหมดท้องถิ่นของ Qdrant, การดึงข้อมูล, การจัดอันดับใหม่, การสร้าง Ollama แบบเลือกได้ และแหล่งอ้างอิง |

## รันในเครื่อง

ติดตั้งไลบรารีที่จำเป็นสำหรับสมุดบันทึกที่คุณต้องการรัน:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

หรือจะติดตั้งทุกอย่างพร้อมกัน:

```powershell
python -m pip install -r requirements\all.txt
```

## ตรวจสอบ

จากโฟลเดอร์รากของ repository:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

ชุดที่ 2 สามารถอ่านการตั้งค่า Ollama จากไฟล์ `.env` ที่อยู่ในโฟลเดอร์ราก repository เริ่มต้นจาก [../.env.example](../../../.env.example) ซึ่งจัดกลุ่มตามชุดบทความแล้ว

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->