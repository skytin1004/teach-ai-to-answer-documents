# Scripts

Folder ini berisi skrip verifikasi repositori.

## `verify_notebooks.py`

Memvalidasi tautan Markdown lokal, JSON notebook, kebersihan keluaran notebook, dan pola rahasia berisiko tinggi:

```powershell
python scripts\verify_notebooks.py
```

Menjalankan semua notebook lokal-aman yang bersifat publik:

```powershell
python scripts\verify_notebooks.py --execute
```

Alur kerja GitHub Actions menggunakan skrip yang sama.

Materi draf di bawah `drafts/` dilewati sampai siap untuk indeks publik.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->