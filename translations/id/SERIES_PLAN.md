# Mengajarkan AI Menjawab Pertanyaan Berdasarkan Dokumen Anda - Rencana Seri

Rencana ini melacak rilis Seri 1 dan Seri 2 yang dipublikasikan. Pekerjaan Azure dan evaluasi selanjutnya disimpan sebagai draft sampai contoh-contoh tersebut sepenuhnya end-to-end dan terverifikasi.

Jangan melakukan commit atau push perubahan sampai secara eksplisit diperintahkan.

## Cakupan Publik

Rilis publik saat ini:

- Artikel Seri 1: keputusan arsitektur RAG, tradeoff Azure vs open-source, dan di mana fine-tuning cocok.
- Artikel Seri 2: tutorial RAG open-source lokal.
- Notebook Seri 2: lab RAG lokal yang dapat dijalankan dengan FastEmbed, Qdrant, Ollama, dan Phi-4-mini.
- Data contoh: file Markdown kebijakan sekolah dan panduan AI kursus.

Sudah dibuat draft tapi belum masuk indeks publik:

- Pembangunan ulang Azure AI Search dan Azure OpenAI.
- Evaluasi RAG dan pemeriksaan regresi.

## Skenario Tutorial

Skenario yang dibagikan adalah asisten kebijakan sekolah.

Asisten menjawab pertanyaan ini dari dokumen lokal:

```text
Can I use generative AI for my final assignment?
```
  
Perilaku yang diharapkan adalah:

1. Memuat dokumen Markdown lokal.
2. Mem-parsing dan memecahnya berdasarkan judul.
3. Membuat embedding lokal dan menyimpan representasi yang dapat dicari dengan metadata.
4. Mengambil bagian kebijakan yang relevan.
5. Melakukan reranking saat diperlukan.
6. Menghasilkan atau menyusun jawaban yang berlandaskan.
7. Mengembalikan sitasi.
8. Mencatat hasil verifikasi.

## Struktur Publik Saat Ini

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```
  
Materi draft disimpan di bawah `drafts/` dan dilewati oleh verifikasi repositori sampai siap untuk diindeks publik.

## Verifikasi Seri 2

Diverifikasi di Windows dengan Python 3.12.6.

- Berhasil menginstal `requirements/open-source-rag.txt`.
- Menjalankan `notebooks/series-2-open-source-rag.ipynb` dengan `nbclient`.
- Verifikasi lokal berhasil: 2 dokumen contoh dimuat, 8 chunk dibuat, FastEmbed menghasilkan embedding lokal berdimensi 384, koleksi dalam memori Qdrant diinisialisasi, dan 8 vektor dimasukkan.
- Pertanyaan tes: "Bisakah saya menggunakan AI generatif untuk tugas akhir saya?"
- Sumber teratas yang diambil setelah reranking ringan: `school_ai_policy.md`.
- Bagian teratas yang diambil setelah reranking ringan: `Final Assignments`.
- Jalur jawaban default: penyusun jawaban lokal yang transparan.
- Ollama diinstal melalui winget; `phi4-mini:3.8b` berhasil diunduh.
- Jalur pembuatan jawaban Ollama: selesai dengan `phi4-mini:3.8b`.
- Ukuran file model Ollama: sekitar 2.49GB di disk.
- Ukuran model Ollama yang dimuat: 3.3GB dilaporkan oleh `ollama ps`.
- Offload GPU: 100% GPU dilaporkan oleh `ollama ps` pada GPU Laptop RTX 3060.
- Memori GPU yang diamati setelah pembuatan jawaban: sekitar 3.5GB dari 6GB.
- Eksekusi notebook dengan model FastEmbed yang di-cache dan pembuatan jawaban Ollama yang diaktifkan berhasil dalam sekitar 34 detik melalui skrip verifikasi.
- Pengamatan: satu kali pemuatan dokumen awal secara tidak sengaja memasukkan `sample_data/README.md`; notebook kini hanya memuat dua dokumen contoh yang dimaksud secara eksplisit.

## Verifikasi Repositori

- `scripts/verify_notebooks.py` memvalidasi tautan Markdown lokal, JSON notebook, kebersihan output notebook, dan pola rahasia berisiko tinggi.
- `scripts/verify_notebooks.py --execute` menjalankan notebook publik dari akar repositori.
- Materi draft di bawah `drafts/` sengaja dilewati.

## Pekerjaan Selanjutnya

- Membangun ulang skenario yang sama dengan Azure AI Search dan Azure OpenAI sebagai bagian seri mendatang.
- Menambahkan evaluasi pengambilan dan jawaban setelah implementasi lokal dan Azure keduanya stabil.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->