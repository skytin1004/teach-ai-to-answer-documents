# Ajar AI Menjawab Soalan Berdasarkan Dokumen Anda
## Siri 2: Bina Sistem RAG Sumber Terbuka Tempatan dari Awal hingga Akhir

![Saluran tutorial RAG sumber terbuka tempatan](../../../assets/images/series-2-local-rag.svg)

> Artikel ini menukar perbincangan seni bina Siri 1 menjadi tutorial RAG tempatan yang boleh dijalankan. Matlamatnya adalah membina aliran kerja penuh terlebih dahulu dengan data contoh, tanpa akaun awan, dan tanpa rahsia, kemudian gunakan asas kerja itu untuk membuat keputusan seni bina yang lebih baik kemudian.

Sistem yang akan kami bina ialah pembantu dasar sekolah kecil. Saya menggunakan dua dokumen Markdown tempatan sebagai pangkalan pengetahuan, kemudian melalui saluran RAG penuh: pemecahan, embedding tempatan, storan vektor Qdrant, pengambilan, penyusunan semula, penyusunan jawapan yang sedar sumber, dan penjanaan tempatan pilihan dengan Ollama dan Phi-4-mini.

Navigasi siri: [Rumah repositori](../README.md) | Sebelumnya: [Siri 1 - RAG, Azure vs Alternatif Sumber Terbuka, dan Bila Penalaan Halus Masuk Akal](./series-1-rag-azure-open-source-fine-tuning.md)

Nota buku: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Keperluan: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Ini adalah titik permulaan terbaik jika anda mahu memahami saluran RAG sebelum membuat sumber awan. Laluan lalai dijalankan secara tempatan dengan embedding mesra CPU dan tanpa rahsia.

## 1. Apa Yang Kita Bina

Dalam tutorial 2023, saya bermula dari Azure kerana matlamatnya adalah untuk menunjukkan bagaimana Azure AI Search dan Azure OpenAI boleh menjawab soalan dari dokumen PDF.

Untuk siri 2026 ini, saya mahu bermula satu lapisan lebih rendah.

Sebelum menggunakan perkhidmatan terurus, saya mahu membina sistem RAG kecil secara tempatan dan menjadikan setiap langkah kelihatan: memuatkan dokumen, memecah teks, menyimpan vektor, mengambil bukti, menyusun semula keputusan, dan mengembalikan jawapan yang sedar sumber.

Senario contoh ialah pembantu dasar sekolah. Pengguna bertanya:

```text
Can I use generative AI for my final assignment?
```

Sistem tidak sepatutnya menjawab dari memori model umum. Ia sepatutnya mengambil bahagian dasar yang relevan dan menjawab dari bukti tersebut.

Versi penuh yang boleh dijalankan terdapat dalam [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Kod di bawah menunjukkan langkah utama supaya artikel ini boleh dibaca sebagai tutorial.

## 2. Pasang Kebergantungan Tempatan

Bina persekitaran maya dan pasang keperluan Siri 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Versi pertama menggunakan mod tempatan Qdrant dan FastEmbed. Klien Python Qdrant menyokong mod tempatan dalam ingatan dengan `QdrantClient(":memory:")`, yang berguna untuk tutorial tempatan dan pengesahan gaya CI. FastEmbed memberi kita model embedding tempatan sebenar tanpa memerlukan kunci API awan.

Fail keperluan juga termasuk `python-dotenv` kerana nota buku boleh secara pilihan membaca nama model Ollama dari `.env`. Tiada kunci Azure OpenAI atau OpenAI API diperlukan untuk tutorial tempatan ini.

## 3. Muatkan Dokumen Contoh

Korpus contoh sengaja kecil:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Dalam nota buku, saya memuatkan semua fail Markdown dari `sample_data/`:

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

Apabila saya jalankan nota buku, ia memuatkan 2 dokumen. Itu cukup kecil untuk disemak secara manual, yang berguna apabila membina versi pertama saluran RAG.

## 4. Pecah Mengikut Tajuk Markdown

Langkah seterusnya adalah memecah dokumen menjadi bahagian.

Untuk tutorial ini, saya menggunakan tajuk Markdown sebagai isyarat struktur. Tajuk dokumen datang dari `#`, dan setiap bahagian datang dari `##`.

> [!NOTE]
> Pemecahan tidak sesuai untuk semua keadaan. Dalam tutorial ini, saya menggunakan tajuk Markdown kerana dokumen contoh mempunyai struktur `#` dan `##` yang jelas. Untuk PDF, dokumen Word, slaid, tiket, atau halaman web, strategi yang lebih baik mungkin menggunakan sempadan halaman, maklumat susun atur, bahagian semantik, had token, jadual, atau metadata. Perkara penting ialah memilih strategi pemecahan yang mengekalkan makna dan jejak sumber untuk dokumen anda.

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

Kemudian saya terapkan kepada setiap dokumen:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Ini mencipta 8 bahagian dalam laluan tempatan saya.

Apa yang saya suka tentang langkah ini ialah metadata sudah berguna. Setiap bahagian tahu `source`, `sectionHeading`, `documentVersion`, dan penanda tempat `permissions`. Walaupun dalam tutorial kecil, ini memudahkan sitasi dan pengambilan yang sedar kebenaran kemudian untuk difahami.

## 5. Cipta Embedding Tempatan

Untuk versi awam pertama, saya menggunakan `BAAI/bge-small-en-v1.5` melalui FastEmbed.

Ini menjadikan tutorial tempatan dan mesra CPU, tetapi masih menggunakan model embedding sebenar bukan fungsi vektor tempat letak. Larian pertama memuat turun berat model. Selepas itu, nota buku boleh menggunakan semula cache tempatan.

> [!NOTE]
> Saya menggunakan `BAAI/bge-small-en-v1.5` kerana ia adalah model embedding bahasa Inggeris ringan yang berfungsi baik dengan FastEmbed dan Qdrant untuk tutorial tempatan. Ia mencipta vektor berdimensi 384, yang menjadikan contoh ini pantas dan murah untuk dijalankan secara tempatan. Ini bukan satu-satunya pilihan baik. Pada tahun 2023, banyak tutorial menggunakan model embedding hos seperti `text-embedding-ada-002`. Hari ini, pilihan hos lebih baru seperti OpenAI `text-embedding-3-small` dan `text-embedding-3-large`, dan pilihan sumber terbuka seperti BGE, E5, MiniLM, Nomic Embed, dan model berbilang bahasa seperti `BAAI/bge-m3` adalah pilihan munasabah bergantung pada beban kerja. Dalam pengeluaran, model embedding yang sesuai harus dipilih melalui penilaian pengambilan pada dokumen anda sendiri.

Beberapa alternatif praktikal:

| Keluarga model | Bila saya akan pertimbangkan |
| --- | --- |
| `text-embedding-ada-002` | Asas hos lama yang muncul dalam banyak tutorial era 2023. Saya tidak akan memilihnya sebagai lalai untuk tutorial baru hari ini. |
| `text-embedding-3-small` | Lalai hos moden apabila saya mahu keseimbangan kos/capai kerja yang kuat dan tidak memerlukan embedding hanya tempatan. |
| `text-embedding-3-large` | Pilihan hos apabila kualiti pengambilan lebih penting daripada saiz vektor atau kos embedding. |
| `BAAI/bge-small-en-v1.5` | Baseline tempatan ringan bahasa Inggeris untuk tutorial, prototaip, dan eksperimen mesra CPU. |
| `BAAI/bge-base-en-v1.5` atau `BAAI/bge-large-en-v1.5` | Model bahasa Inggeris tempatan lebih besar apabila saya mahu kualiti pengambilan lebih baik dan boleh menanggung lebih banyak pengiraan. |
| `BAAI/bge-m3` | Pengambilan berbilang bahasa atau konteks lebih panjang, terutamanya apabila dokumen bukan hanya Inggeris. |
| `sentence-transformers/all-MiniLM-L6-v2` | Baseline carian semantik sangat kecil dan pantas. Berguna apabila kelajuan dan kesederhanaan paling penting. |
| `nomic-embed-text-v1.5` | Pilihan embedding tempatan terbuka yang berbaloi diuji untuk konteks lebih panjang atau set up fokus kebolehbawaan. |

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

Kemudian setiap bahagian mendapat embedding:

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

## 6. Simpan Vektor dalam Mod Tempatan Qdrant

Sekarang kita cipta koleksi Qdrant dalam ingatan dan masukkan bahagian dengan metadata payload.

> [!NOTE]
> Dalam tutorial 2023, saya menggunakan FAISS kerana ia cara mudah dan popular untuk menunjukkan carian kesamaan vektor tempatan dengan LangChain. FAISS masih berguna untuk eksperimen tempatan yang pantas. Dalam versi 2026 ini, saya menggunakan Qdrant kerana saya mahu tutorial rasa lebih dekat dengan sistem RAG pengeluaran. Qdrant membenarkan saya menyimpan vektor bersama metadata payload seperti fail sumber, tajuk bahagian, versi dokumen, dan kebenaran. Itu memudahkan pemeriksaan pengambilan dan menyediakan contoh untuk penapisan, sitasi, dan pelaksanaan kekal atau pelayan kemudian.

FAISS hebat untuk menunjukkan carian kesamaan vektor. Qdrant lebih baik untuk menunjukkan lapisan pengambilan RAG yang kecil tetapi berbentuk pengeluaran.

Beberapa alternatif praktikal:

| Lapisan storan vektor / carian | Bila saya akan pertimbangkan |
| --- | --- |
| Qdrant | Prototip tempatan, penapisan metadata, carian vektor mesra pengeluaran, dan aliran kerja Python mudah. |
| Chroma | Eksperimen RAG tempatan pantas dan nota buku di mana kesederhanaan paling penting. |
| FAISS | Carian vektor tempatan ringan apabila saya hanya perlukan carian kesamaan dan boleh mengurus metadata secara berasingan. |
| Milvus | Carian vektor sumber terbuka skala besar apabila pasukan sudah bersedia mengendalikan pangkalan data vektor khusus. |
| Weaviate | Carian vektor dengan skema, metadata, carian hibrid, dan pilihan pelaksanaan terurus atau kendiri. |
| Azure AI Search | RAG perusahaan di Azure apabila saya mahu carian kata kunci, carian vektor, pengambilan hibrid, penyusunan semantik, penapisan, keselamatan, dan operasi terurus dalam satu lapisan carian. |
| PostgreSQL + pgvector | Pasukan yang sudah menggunakan PostgreSQL yang mahu carian vektor dekat dengan data aplikasi. |

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

Kemudian masukkan titik-titik itu:

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

Dalam larian saya, koleksi memasukkan 8 vektor.

Di sinilah sistem RAG mula menjadi boleh diperiksa. Pangkalan data vektor bukan sahaja menyimpan vektor; ia menyimpan teks bukti dan metadata yang diperlukan untuk sitasi.

## 7. Ambil Bahagian Calon

Sekarang kita tanya soalan dan ambil bahagian calon.

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

Pada ketika ini, saya cetak bahagian yang diambil sebelum menjana jawapan. Ini penting. Jika pengambilan salah, penjanaan hanya akan menyembunyikan masalah di belakang teks yang lancar.

## 8. Tambah Penyusun Semula Ringan

Apabila saya mula menguji laluan pengambilan, kesamaan vektor sahaja menemui kandungan dasar berkaitan, tetapi bahagian paling tepat tidak selalu berada di atas.

Jadi saya tambah penyusun semula kecil tempatan. Ia memberi berat tambahan apabila istilah soalan tumpang tindih dengan tajuk bahagian dan kandungan.

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

Selepas penyusunan semula, keputusan teratas menjadi:

```text
school_ai_policy.md / Final Assignments
```

Itu ialah bahagian yang dijangka untuk soalan ujian.

Itu adalah pelajaran paling berguna dari pelaksanaan pertama. Walaupun dalam contoh tempatan yang kecil, kualiti pengambilan bertambah baik apabila saya gabungkan kesamaan vektor dengan isyarat lain.

## 9. Susun Jawapan Tempatan Berdasarkan Bukti

Untuk laluan lalai, saya menggunakan penyusun jawapan tempatan telus dan bukannya LLM.

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

Ini bukan maksud untuk menjadi penjana jawapan produk akhir. Ia alat debugging. Ia membuktikan bahawa pengambilan, metadata, dan pengaitan sitasi berfungsi sebelum menambah variasi model.

## 10. Jana Jawapan Tempatan dengan Ollama dan Phi-4-mini

Setelah pengambilan berfungsi, nota buku boleh menggantikan hanya langkah jawapan akhir dengan Ollama dan `phi4-mini:3.8b`.

> [!NOTE]
> Ollama sepatutnya hanya menggantikan langkah penjanaan jawapan akhir. Pemuatan dokumen, pemecahan, storan vektor, pengambilan, penyusunan semula, dan pengaitan sitasi harus kekal sama.

Pertama, nota buku membina arahan bukti dari bahagian yang diambil:

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

Untuk tutorial ini, saya cadangkan keluarga Phi-4-mini Microsoft melalui Ollama sebagai pilihan penjanaan tempatan lalai. Dalam Ollama, nama model yang saya uji ialah:

```powershell
ollama pull phi4-mini:3.8b
```

Anda boleh periksa dengan cepat bahawa model itu tersedia:

```powershell
ollama list
```

Kemudian tetapkan pemboleh ubah ini:

```powershell
Copy-Item .env.example .env
```

Buka `.env` dan nyahkomen nilai Ollama Siri 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Nota buku memuat `.env` dari akar repositori dengan `python-dotenv`, kemudian hantar arahan bukti yang sama ke titik akhir `/api/chat` Ollama tempatan dengan aliran dimatikan. Jika Ollama tidak berjalan atau `SERIES2_OLLAMA_MODEL` tiada, laluan ini diabaikan.

> [!NOTE]
> Pada mesin ini, `phi4-mini:3.8b` memuat turun kira-kira 2.49GB fail model. Semasa inferens, Ollama melaporkan saiz model dimuat 3.3GB dan menggunakan GPU RTX 3060 Laptop.

Ini memberikan tutorial dua peringkat:

1. Penyusun jawapan deterministik hanya CPU.
2. Penjanaan jawapan tempatan dengan Ollama dan Phi-4-mini.

Saluran pengambilan kekal sama dalam kedua-duanya.

## 11. Keputusan Pengesahan

Saya jalankan nota buku secara tempatan pada Windows dengan Python 3.12.6.

Pakej dipasang:

| Pakej | Versi |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Pelaksanaan nota buku:

- Nota buku: `notebooks/series-2-open-source-rag.ipynb`
- Keputusan pelaksanaan: lulus dengan `nbclient`
- Dokumen dimuat: 2
- Bahagian dibuat: 8
- Koleksi Qdrant: `school_policy_local`
- Vektor dimasukkan: 8
- Model embedding: `BAAI/bge-small-en-v1.5`
- Saiz embedding: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Saya tidak akan menganggap jawapan ini sempurna. Ia menjawab berdasarkan bukti yang tepat, tetapi garis sumber akhir kurang tepat berbanding format sitasi deterministik. Ini berguna untuk ditunjukkan dalam tutorial kerana ia menjadikan soalan kejuruteraan seterusnya jelas: penjanaan jawapan juga memerlukan penilaian, bukan hanya pengambilan.

Perkara utama yang saya pelajari semasa mengesahkan ini ialah kualiti pengambilan perlu diperiksa sebelum penjanaan jawapan. Keputusan embedding sudah berguna, dan pemeringkat ringan memastikan bahagian dasar yang dijangka muncul sebagai pertama dengan boleh dipercayai. Itulah jenis tingkah laku sistem kecil yang saya mahu tutorial dedahkan bukannya disembunyikan.

## 12. Apa Yang Akan Datang

Penambahbaikan seterusnya adalah membandingkan susunan tempatan ini dengan versi Azure yang diuruskan bagi keadaan pembantu polisi sekolah yang sama. Mengekalkan senario tetap akan memudahkan untuk melihat pertukaran: kerumitan penyediaan, kawalan pengambilan, integrasi identiti, pemilikan operasi, dan kos.

## 13. Rujukan

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Repositori GitHub klien Qdrant](https://github.com/qdrant/qdrant-client)
- [Model yang disokong FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Panduan embedding OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Kad model BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Kad model BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Kad model sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Halaman model Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Dokumentasi Ollama Windows](https://docs.ollama.com/windows)
- [Dokumentasi streaming API Ollama](https://docs.ollama.com/api/streaming)
- [Kad model Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Gambaran LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Pengenalan kepada RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Sebelum: [Siri 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->