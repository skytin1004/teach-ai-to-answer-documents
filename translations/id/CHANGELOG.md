# Changelog

## Belum Dirilis

Lingkup rilis publik awal untuk **Ajarkan AI Menjawab Pertanyaan Berdasarkan Dokumen Anda**.

### Ditambahkan

- Artikel Seri 1 tentang keputusan arsitektur RAG, perbandingan Azure vs open-source, dan di mana fine-tuning cocok.
- Artikel dan notebook Seri 2 untuk workflow RAG open-source lokal menggunakan Qdrant mode lokal, FastEmbed embeddings lokal, reranking ringan, Ollama, dan Phi-4-mini.
- Format tutorial langkah-demi-langkah Seri 2 dari awal hingga akhir dengan potongan kode Python dan catatan verifikasi dari notebook yang dijalankan.
- Jalur opsional pembuatan jawaban Seri 2 dengan Ollama dan Phi-4-mini sambil menjaga pengambilan data lokal yang ramah CPU sebagai jalur default.
- Verifikasi Ollama lokal untuk Seri 2 menggunakan `phi4-mini:3.8b` pada RTX 3060 Laptop GPU.
- Data contoh untuk kebijakan sekolah dan panduan AI kursus.
- File persyaratan untuk notebook publik dan verifikasi tingkat repositori.
- Skrip verifikasi repositori untuk link Markdown lokal dan validasi/eksekusi notebook.
- Workflow GitHub Actions untuk verifikasi notebook.
- `.env.example` untuk setup pembuatan Ollama lokal opsional tanpa meng-commit konfigurasi lokal.
- File README tingkat folder untuk artikel, notebook, persyaratan, data contoh, dan skrip.
- Daftar periksa penerbitan untuk keamanan dan verifikasi publik.
- Workspace draft untuk konten Azure dan evaluasi di masa depan.

### Diverifikasi

- Validasi link Markdown lokal berhasil.
- Notebook Seri 2 berhasil divalidasi.
- Notebook Seri 2 berhasil dijalankan di lingkungan verifikasi lokal.
- File notebook disimpan tanpa output atau hitungan eksekusi.
- Tidak ada rahasia nyata yang dikomit.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->