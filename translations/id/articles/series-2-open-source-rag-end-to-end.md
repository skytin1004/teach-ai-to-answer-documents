# Ajari AI Menjawab Pertanyaan Berdasarkan Dokumen Anda
## Seri 2: Membangun Sistem RAG Open-Source Lokal Dari Awal hingga Akhir

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Artikel ini mengubah diskusi arsitektur Seri 1 menjadi tutorial RAG lokal yang dapat dijalankan. Tujuannya adalah membangun alur kerja penuh terlebih dahulu dengan data contoh, tanpa akun cloud, dan tanpa rahasia, lalu menggunakan baseline yang berfungsi tersebut untuk membuat keputusan arsitektur yang lebih baik nanti.

Sistem yang akan kita bangun adalah asisten kebijakan sekolah kecil. Saya menggunakan dua dokumen Markdown lokal sebagai basis pengetahuan, kemudian menjalankan seluruh pipeline RAG: pembagian chunk, embedding lokal, penyimpanan vektor Qdrant, pengambilan, pengurutan ulang, komposisi jawaban yang sadar sumber, dan generasi lokal opsional dengan Ollama dan Phi-4-mini.

Navigasi seri: [Beranda Repository](../README.md) | Sebelumnya: [Seri 1 - RAG, Azure vs Alternatif Open-Source, dan Kapan Fine-Tuning Masuk Akal](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Persyaratan: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Ini adalah titik awal terbaik jika Anda ingin memahami pipeline RAG sebelum membuat sumber daya cloud. Jalur default dijalankan secara lokal dengan embedding ramah CPU dan tanpa rahasia.

## 1. Apa yang Kita Bangun

Dalam tutorial 2023, saya memulai dari Azure karena tujuannya adalah menunjukkan bagaimana Azure AI Search dan Azure OpenAI dapat menjawab pertanyaan dari dokumen PDF.

Untuk seri 2026 ini, saya ingin mulai satu lapisan lebih rendah.

Sebelum menggunakan layanan terkelola, saya ingin membangun sistem RAG kecil secara lokal dan membuat setiap langkah terlihat: memuat dokumen, membagi teks menjadi chunk, menyimpan vektor, mengambil bukti, mengurutkan ulang hasil, dan mengembalikan jawaban yang sadar sumber.

Skenario contoh adalah asisten kebijakan sekolah. Pengguna bertanya:

```text
Can I use generative AI for my final assignment?
```

Sistem tidak boleh menjawab dari memori model umum. Sistem harus mengambil bagian kebijakan yang relevan dan menjawab dari bukti tersebut.

Versi lengkap yang dapat dijalankan ada di [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Kode di bawah ini menunjukkan langkah utama agar artikel ini dapat dibaca sebagai tutorial.

## 2. Instalasi Dependensi Lokal

Buat lingkungan virtual dan instal persyaratan Seri 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Versi pertama menggunakan mode lokal Qdrant dan FastEmbed. Klien Python Qdrant mendukung mode lokal dalam memori dengan `QdrantClient(":memory:")`, yang berguna untuk tutorial lokal dan verifikasi gaya CI. FastEmbed memberi kita model embedding lokal nyata tanpa memerlukan kunci API cloud.

File persyaratan juga mencakup `python-dotenv` karena notebook dapat membaca nama model Ollama dari `.env` secara opsional. Tidak diperlukan kunci API Azure OpenAI atau OpenAI untuk tutorial lokal ini.

## 3. Memuat Dokumen Contoh

Korpus contoh sengaja dibuat kecil:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Di notebook, saya memuat semua file Markdown dari `sample_data/`:

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

Saat saya menjalankan notebook, ia memuat 2 dokumen. Itu cukup kecil untuk diperiksa secara manual, yang berguna saat membangun versi pertama pipeline RAG.

## 4. Membagi Berdasarkan Judul Markdown

Langkah berikutnya adalah memecah dokumen menjadi chunk.

Untuk tutorial ini, saya menggunakan judul Markdown sebagai sinyal struktur. Judul dokumen berasal dari `#`, dan setiap chunk bagian berasal dari `##`.

> [!NOTE]
> Pembagian chunk tidak satu ukuran untuk semua. Dalam tutorial ini, saya menggunakan judul Markdown karena dokumen contoh memiliki struktur `#` dan `##` yang jelas. Untuk PDF, dokumen Word, slide, tiket, atau halaman web, strategi yang lebih baik mungkin menggunakan batas halaman, informasi tata letak, bagian semantik, batas token, tabel, atau metadata. Poin pentingnya adalah memilih strategi chunking yang mempertahankan makna dan keterlacakan sumber untuk dokumen Anda.

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

Lalu saya terapkan ke setiap dokumen:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Ini menghasilkan 8 chunk dalam jalankan lokal saya.

Yang saya sukai dari langkah ini adalah bahwa metadata sudah berguna. Setiap chunk tahu `source`, `sectionHeading`, `documentVersion`, dan placeholder `permissions`. Bahkan dalam tutorial kecil sekalipun, ini memudahkan penalaran tentang sitasi dan pengambilan berbasis izin di kemudian hari.

## 5. Membuat Embedding Lokal

Untuk versi publik pertama, saya menggunakan `BAAI/bge-small-en-v1.5` melalui FastEmbed.

Ini membuat tutorial tetap lokal dan ramah CPU, tapi tetap menggunakan model embedding nyata bukan fungsi vektor placeholder. Jalankan pertama kali mengunduh bobot model. Setelah itu, notebook dapat menggunakan cache lokal.

> [!NOTE]
> Saya menggunakan `BAAI/bge-small-en-v1.5` karena ini adalah model embedding bahasa Inggris ringan yang bekerja baik dengan FastEmbed dan Qdrant untuk tutorial lokal. Ini membuat vektor berdimensi 384, yang membuat contoh cepat dan murah dijalankan secara lokal. Ini bukan satu-satunya pilihan bagus. Pada 2023, banyak tutorial menggunakan model embedding terhosting seperti `text-embedding-ada-002`. Saat ini, opsi terhosting yang lebih baru seperti OpenAI `text-embedding-3-small` dan `text-embedding-3-large`, dan opsi open-source seperti BGE, E5, MiniLM, Nomic Embed, dan model multibahasa seperti `BAAI/bge-m3` semua pilihan masuk akal tergantung beban kerja. Dalam produksi, model embedding yang tepat harus dipilih melalui evaluasi pengambilan pada dokumen Anda sendiri.

Beberapa alternatif praktis:

| Keluarga Model | Kapan Saya Mempertimbangkannya |
| --- | --- |
| `text-embedding-ada-002` | Baseline terhosting lama yang muncul di banyak tutorial era 2023. Saya tidak akan memilihnya sebagai default untuk tutorial baru hari ini. |
| `text-embedding-3-small` | Default modern terhosting saat saya inginkan keseimbangan biaya/kinerja yang kuat dan tidak memerlukan embedding lokal saja. |
| `text-embedding-3-large` | Opsi terhosting saat kualitas pengambilan lebih penting dari ukuran vektor atau biaya embedding. |
| `BAAI/bge-small-en-v1.5` | Baseline lokal bahasa Inggris ringan untuk tutorial, prototipe, dan eksperimen ramah CPU. |
| `BAAI/bge-base-en-v1.5` atau `BAAI/bge-large-en-v1.5` | Model bahasa Inggris lokal yang lebih besar saat saya ingin kualitas pengambilan lebih baik dan mampu menggunakan lebih banyak komputasi. |
| `BAAI/bge-m3` | Pengambilan multibahasa atau konteks lebih panjang, terutama saat dokumen tidak hanya bahasa Inggris. |
| `sentence-transformers/all-MiniLM-L6-v2` | Baseline pencarian semantik sangat kecil dan cepat. Berguna saat kecepatan dan kesederhanaan paling penting. |
| `nomic-embed-text-v1.5` | Opsi embedding lokal terbuka yang layak diuji untuk konteks lebih panjang atau pengaturan berfokus portabilitas. |

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

Kemudian setiap chunk mendapatkan embedding:

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

## 6. Menyimpan Vektor di Mode Lokal Qdrant

Sekarang kita buat koleksi Qdrant dalam memori dan masukkan chunk dengan metadata payload.

> [!NOTE]
> Dalam tutorial 2023, saya menggunakan FAISS karena itu adalah cara sederhana dan populer untuk mendemonstrasikan pencarian kesamaan vektor lokal dengan LangChain. FAISS masih berguna untuk eksperimen lokal cepat. Dalam versi 2026 ini, saya menggunakan Qdrant karena ingin tutorial terasa lebih dekat dengan sistem RAG produksi. Qdrant memungkinkan saya menyimpan vektor bersama metadata payload seperti file sumber, judul bagian, versi dokumen, dan izin. Itu membuat pengambilan lebih mudah diperiksa dan mempersiapkan contoh untuk penyaringan, sitasi, dan penerapan jangka panjang atau berbasis server.

FAISS bagus untuk menunjukkan pencarian kesamaan vektor. Qdrant lebih baik untuk menunjukkan lapisan pengambilan RAG kecil tapi berbentuk produksi.

Beberapa alternatif praktis:

| Penyimpanan Vektor / Lapisan Pencarian | Kapan Saya Mempertimbangkannya |
| --- | --- |
| Qdrant | Prototipe lokal, penyaringan metadata, pencarian vektor ramah produksi, dan alur kerja Python sederhana. |
| Chroma | Eksperimen RAG lokal cepat dan notebook di mana kesederhanaan yang paling utama. |
| FAISS | Pencarian vektor lokal ringan saat saya hanya butuh pencarian kesamaan dan bisa mengelola metadata terpisah. |
| Milvus | Pencarian vektor open-source skala besar saat tim siap mengoperasikan basis data vektor khusus. |
| Weaviate | Pencarian vektor dengan skema, metadata, pencarian hibrid, dan opsi penerapan terkelola atau self-hosted. |
| Azure AI Search | RAG perusahaan di Azure saat saya ingin pencarian kata kunci, pencarian vektor, pengambilan hibrid, perankingan semantik, penyaringan, keamanan, dan operasi terkelola dalam satu lapisan pencarian. |
| PostgreSQL + pgvector | Tim yang sudah menggunakan PostgreSQL yang ingin pencarian vektor dekat dengan data aplikasi. |

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

Kemudian masukkan poin-poinnya:

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

Pada jalankan saya, koleksi memasukkan 8 vektor.

Di sinilah sistem RAG mulai bisa diperiksa. Basis data vektor tidak hanya menyimpan vektor; juga menyimpan teks bukti dan metadata yang dibutuhkan untuk sitasi.

## 7. Mengambil Chunk Kandidat

Sekarang kita ajukan pertanyaan dan ambil chunk kandidat.

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

Pada titik ini, saya mencetak chunk yang diambil sebelum membuat jawaban. Ini penting. Jika pengambilan salah, generasi hanya akan menyembunyikan masalah di balik teks yang lancar.

## 8. Menambahkan Reranker Ringan

Saat pertama kali saya menguji jalur pengambilan, kesamaan vektor saja menemukan konten kebijakan terkait, tapi bagian paling tepat tidak selalu di urutan teratas.

Jadi saya tambahkan reranker lokal kecil. Ia memberi bobot ekstra saat istilah pertanyaan tumpang tindih dengan judul bagian dan isi.

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

Setelah pengurutan ulang, hasil teratas menjadi:

```text
school_ai_policy.md / Final Assignments
```

Itu adalah bagian yang diharapkan untuk pertanyaan uji.

Ini adalah pelajaran paling berguna dari implementasi pertama. Bahkan di contoh lokal kecil, kualitas pengambilan membaik saat saya menggabungkan kesamaan vektor dengan sinyal lain.

## 9. Menyusun Jawaban Lokal yang Berbasis Bukti

Untuk jalur default, saya gunakan penyusun jawaban lokal transparan alih-alih LLM.

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

Ini bukan dimaksudkan sebagai generator jawaban produk akhir. Ini adalah alat debugging. Ini membuktikan bahwa pengambilan, metadata, dan sambungan sitasi bekerja sebelum menambahkan variabilitas model.

## 10. Menghasilkan Jawaban Lokal dengan Ollama dan Phi-4-mini

Setelah pengambilan bekerja, notebook dapat mengganti hanya langkah jawaban akhir dengan Ollama dan `phi4-mini:3.8b`.

> [!NOTE]
> Ollama hanya mengganti langkah pembuatan jawaban akhir. Pemuatan dokumen, pembagian chunk, penyimpanan vektor, pengambilan, pengurutan ulang, dan sambungan sitasi harus tetap sama.

Pertama, notebook membangun prompt bukti dari chunk yang diambil:

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

Untuk tutorial ini, saya merekomendasikan keluarga Phi-4-mini Microsoft melalui Ollama sebagai opsi generasi lokal default. Di Ollama, nama model yang saya uji adalah:

```powershell
ollama pull phi4-mini:3.8b
```

Anda bisa cepat memeriksa apakah model tersedia:

```powershell
ollama list
```

Lalu atur variabel ini:

```powershell
Copy-Item .env.example .env
```

Buka `.env` dan buka komentar nilai Seri 2 Ollama:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook memuat `.env` dari akar repository dengan `python-dotenv`, lalu mengirim prompt bukti yang sama ke endpoint lokal Ollama `/api/chat` dengan streaming dinonaktifkan. Jika Ollama tidak berjalan atau `SERIES2_OLLAMA_MODEL` hilang, jalur ini dilewati.

> [!NOTE]
> Di mesin ini, `phi4-mini:3.8b` mengunduh sekitar 2,49GB file model. Saat inferensi, Ollama melaporkan ukuran model dimuat 3,3GB dan menggunakan GPU Laptop RTX 3060.

Ini memberikan tutorial dua tingkat:

1. Penyusun jawaban deterministik hanya-CPU.
2. Generasi jawaban lokal dengan Ollama dan Phi-4-mini.

Pipeline pengambilan tetap sama di keduanya.

## 11. Hasil Verifikasi

Saya menjalankan notebook secara lokal di Windows dengan Python 3.12.6.

Paket yang terpasang:

| Paket | Versi |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Eksekusi notebook:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Hasil eksekusi: berhasil dengan `nbclient`
- Dokumen dimuat: 2
- Chunk dibuat: 8
- Koleksi Qdrant: `school_policy_local`
- Vektor dimasukkan: 8
- Model embedding: `BAAI/bge-small-en-v1.5`
- Ukuran embedding: 384
- Pertanyaan pengambilan: "Bisakah saya menggunakan AI generatif untuk tugas akhir saya?"
- Jalur penyusunan ulang peringkat: penyusunan ulang peringkat leksikal lokal ringan
- Sumber teratas yang diambil setelah penyusunan ulang peringkat: `school_ai_policy.md`
- Bagian teratas yang diambil setelah penyusunan ulang peringkat: `Final Assignments`
- Jalur jawaban default: penyusun jawaban transparan lokal
- Jalur generasi Ollama: selesai dengan `phi4-mini:3.8b`
- Ukuran file model Ollama: 2,49GB di disk
- Ukuran model Ollama yang dimuat: 3,3GB dilaporkan oleh `ollama ps`
- GPU offload: 100% GPU dilaporkan oleh `ollama ps`
- Memori GPU yang diamati setelah generasi: sekitar 3,5GB dari 6GB digunakan pada RTX 3060 Laptop GPU
- Eksekusi notebook dengan model FastEmbed yang di-cache dan generasi Ollama diaktifkan: lolos dalam sekitar 34 detik melalui skrip verifikasi

Jawaban yang dihasilkan Ollama adalah:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Saya tidak akan menyebut jawaban ini sempurna. Jawaban ini berasal dari bukti yang tepat, tetapi baris sumber akhir kurang tepat daripada format kutipan deterministik. Itu berguna untuk ditunjukkan dalam tutorial karena membuat pertanyaan rekayasa berikutnya menjadi jelas: generasi jawaban juga perlu evaluasi, bukan hanya pengambilan.

Hal utama yang saya pelajari saat memverifikasi ini adalah kualitas pengambilan harus diperiksa sebelum generasi jawaban. Hasil embedding sudah berguna, dan penyusun ulang peringkat ringan membuat bagian kebijakan yang diharapkan muncul pertama secara andal. Itu adalah jenis perilaku sistem kecil yang saya ingin tutorial ini ungkapkan daripada sembunyikan.

## 12. Apa Selanjutnya

Perbaikan berikutnya adalah membandingkan pengaturan lokal ini dengan versi Azure yang dikelola dari skenario asisten kebijakan sekolah yang sama. Menjaga skenario tetap sama harus membuat pertukaran menjadi lebih mudah dilihat: kompleksitas pengaturan, kontrol pengambilan, integrasi identitas, kepemilikan operasional, dan biaya.

## 13. Referensi

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Repositori GitHub klien Qdrant](https://github.com/qdrant/qdrant-client)
- [Model yang didukung FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Panduan embeddings OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Kartu model BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Kartu model BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Kartu model sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Halaman model Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Dokumentasi Ollama Windows](https://docs.ollama.com/windows)
- [Dokumentasi streaming API Ollama](https://docs.ollama.com/api/streaming)
- [Kartu model Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Ikhtisar LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Pengantar RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Sebelumnya: [Seri 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->