# Ajari AI untuk Menjawab Pertanyaan Berdasarkan Dokumen Anda

![Ikhtisar sistem AI RAG berbasis dokumen](../../assets/images/readme-hero.svg)

Repositori ini mengumpulkan seri blog 2026 tentang membangun sistem AI berbasis dokumen dengan RAG, layanan Azure AI, alternatif open-source, dan alur kerja berorientasi evaluasi.

## Latar Belakang

Pada 2023, saya mengerjakan sepasang tutorial tentang mengajari ChatGPT untuk menjawab pertanyaan dari dokumen PDF menggunakan Azure AI Search dan Azure OpenAI. Gagasan "ChatGPT pada data Anda" masih terasa baru saat itu, dan tujuannya adalah untuk menunjukkan alur kerja praktis: menyimpan dokumen, mengindeksnya, mengambil konten yang relevan, dan menghasilkan jawaban dari konteks yang diambil tersebut.

Pada 2026, ekosistem RAG jauh lebih besar. Azure AI Search mendukung pola pengambilan vektor modern dan hybrid, Azure OpenAI merupakan bagian dari ekosistem Model Foundry Microsoft yang lebih luas, dan alat open-source seperti LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, dan vLLM telah menjadi pilihan praktis untuk sistem nyata.

Oleh karena itu, saya ingin mengulas kembali topik ini. Pertanyaannya kini tidak hanya "Bagaimana saya membangun RAG?" Ada banyak cara untuk membangunnya, dan pertanyaan yang lebih penting adalah "Arsitektur mana yang harus saya pilih untuk situasi saya?"

Seri ini dimulai dari lapisan pengambilan keputusan tersebut, lalu mengubahnya menjadi tutorial praktis. Jalur implementasi pertama membangun sistem RAG open-source lokal yang bisa dijalankan siapa saja dengan data contoh, Qdrant, Ollama, dan Phi-4-mini.

## Artikel

Lihat [articles/README.md](./articles/README.md) untuk indeks artikel.

1. [Seri 1: RAG, Azure vs Alternatif Open-Source, dan Kapan Fine-Tuning Masuk Akal](./articles/series-1-rag-azure-open-source-fine-tuning.md)  
2. [Seri 2: Bangun Sistem RAG Open-Source Lokal dari Awal sampai Akhir](./articles/series-2-open-source-rag-end-to-end.md)

Berikutnya:

- Membangun ulang sistem RAG yang sama dengan Azure AI Search dan Azure OpenAI.  
- Menambahkan evaluasi dan pemeriksaan regresi di luar jawaban demo.

## Notebook

Artikel implementasi menggunakan notebook agar langkah pengambilan dan evaluasi dapat diperiksa langsung. Lihat [notebooks/README.md](./notebooks/README.md) untuk panduan level folder.

> [!TIP]  
> Mulailah dengan Seri 2 jika Anda ingin jalur tercepat. Notebook ini berjalan lokal dengan data contoh, embedding ramah CPU, mode lokal Qdrant, dan tanpa kredensial cloud.

| Seri | Notebook | Persyaratan | Verifikasi lokal |
| --- | --- | --- | --- |
| Seri 2 | [Notebook RAG open-source](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Mode lokal Qdrant, pengambilan, reranking, dan pengurutan sumber diverifikasi |

Untuk menjalankan notebook secara lokal, buat lingkungan virtual dan pasang file persyaratan yang sesuai. Contohnya:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```
  
## Data Contoh

Notebook menggunakan korpus lokal kecil di [sample_data](../../sample_data) sehingga contoh dapat dijalankan tanpa dokumen pribadi atau kredensial cloud. Lihat [sample_data/README.md](./sample_data/README.md) untuk detail.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)  
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)  

## Ringkasan Verifikasi Lokal

Hasil verifikasi dicatat di setiap artikel dan di [SERIES_PLAN.md](./SERIES_PLAN.md).

| Area | Hasil |
| --- | --- |
| Jalur open-source Seri 2 | FastEmbed menghasilkan embedding lokal berdimensi 384, koleksi in-memory Qdrant memasukkan 8 vektor, reranking ringan mengambil bagian yang diharapkan; generasi opsional Ollama selesai dengan `phi4-mini:3.8b` |

Notebook lokal sengaja menghindari penggunaan rahasia yang dikodekan langsung.

## Generasi Ollama Lokal

Notebook Seri 2 aman untuk lokal secara default. Untuk mengaktifkan generasi Ollama lokal, salin [.env.example](../../.env.example) ke `.env` dan isi nilai Seri 2.

Untuk generasi Ollama Seri 2, uncomment:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```
  
Notebook Seri 2 secara otomatis memuat `.env` dari root repositori dengan menggunakan `python-dotenv`.

> [!IMPORTANT]  
> Jangan meng-commit file `.env`, kunci API, endpoint privat, atau nilai khusus tenant. Repositori sengaja menjaga rahasia di luar file Markdown dan notebook.

File persyaratan didokumentasikan di [requirements/README.md](./requirements/README.md).

Untuk memvalidasi tautan, struktur notebook, kebersihan output notebook, dan pola rahasia berisiko tinggi:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```
  
Skrip verifikasi didokumentasikan di [scripts/README.md](./scripts/README.md).

Untuk menjalankan semua notebook yang aman lokal di lingkungan yang sama:

```powershell
python scripts\verify_notebooks.py --execute
```
  
Alur verifikasi yang sama berjalan di GitHub Actions pada push, pull request, dan manual workflow dispatch. Artikel dan notebook draft sengaja tidak disertakan dalam jalur verifikasi publik.

Sebelum menerbitkan pembaruan, gunakan [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Lihat [CHANGELOG.md](./CHANGELOG.md) untuk ringkasan perubahan belum dipublikasikan saat ini.

Untuk pedoman kontribusi dan kebersihan notebook, lihat [CONTRIBUTING.md](./CONTRIBUTING.md).

## Dukungan Multi-Bahasa

### Didukung melalui Co-op Translator (Otomatis dan Selalu Terbaru)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arab](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgaria](../bg/README.md) | [Burma (Myanmar)](../my/README.md) | [Cina (Sederhana)](../zh-CN/README.md) | [Cina (Tradisional, Hong Kong)](../zh-HK/README.md) | [Cina (Tradisional, Macau)](../zh-MO/README.md) | [Cina (Tradisional, Taiwan)](../zh-TW/README.md) | [Kroasia](../hr/README.md) | [Ceko](../cs/README.md) | [Denmark](../da/README.md) | [Belanda](../nl/README.md) | [Estonia](../et/README.md) | [Finlandia](../fi/README.md) | [Prancis](../fr/README.md) | [Jerman](../de/README.md) | [Yunani](../el/README.md) | [Ibrani](../he/README.md) | [Hindi](../hi/README.md) | [Hongaria](../hu/README.md) | [Indonesia](./README.md) | [Italia](../it/README.md) | [Jepang](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korea](../ko/README.md) | [Litunia](../lt/README.md) | [Melayu](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Pidgin Nigeria](../pcm/README.md) | [Norwegia](../no/README.md) | [Persia (Farsi)](../fa/README.md) | [Polandia](../pl/README.md) | [Portugis (Brasil)](../pt-BR/README.md) | [Portugis (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumania](../ro/README.md) | [Rusia](../ru/README.md) | [Serbia (Sirilik)](../sr/README.md) | [Slovakia](../sk/README.md) | [Slovenia](../sl/README.md) | [Spanyol](../es/README.md) | [Swahili](../sw/README.md) | [Swedia](../sv/README.md) | [Tagalog (Filipina)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turki](../tr/README.md) | [Ukraina](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnam](../vi/README.md)

> **Lebih suka Clone secara Lokal?**  
>  
> Repositori ini mencakup lebih dari 50 terjemahan bahasa yang secara signifikan meningkatkan ukuran unduhan. Untuk meng-clone tanpa terjemahan, gunakan sparse checkout:  
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
> Ini memberi Anda semua yang dibutuhkan untuk menyelesaikan kursus dengan unduhan yang jauh lebih cepat.  
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->