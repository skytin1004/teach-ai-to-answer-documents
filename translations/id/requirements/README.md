# Persyaratan

Setiap artikel implementasi memiliki file persyaratan yang terfokus.

| File | Digunakan oleh |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Notebook RAG open-source Seri 2, termasuk pembantu generasi Ollama opsional |
| [all.txt](../../../requirements/all.txt) | Verifikasi tingkat repositori dan CI |

Gunakan file terfokus saat menjalankan satu notebook. Gunakan `all.txt` saat memvalidasi seluruh repositori.

`open-source-rag.txt` dan `all.txt` menyertakan `fastembed` untuk embedding lokal dan `python-dotenv` agar Seri 2 dapat secara opsional mengaktifkan generasi Ollama dari `.env` tanpa mengubah pipeline pengambilan.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->