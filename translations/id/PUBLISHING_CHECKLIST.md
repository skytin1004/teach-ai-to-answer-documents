# Daftar Periksa Publikasi

Gunakan daftar periksa ini sebelum melakukan commit atau push pembaruan publik.

## Keamanan

- Pastikan tidak ada kunci API, token, kata sandi, atau endpoint privat yang tertulis dalam file Markdown, notebook, data contoh, atau skrip.
- Simpan kredensial dalam variabel lingkungan atau identitas terkelola, bukan dalam file yang di-commit.
- Jangan commit file `.env` atau output notebook yang sudah dijalankan.
- Simpan `.env.example` hanya sebagai placeholder.

## Verifikasi

Jalankan skrip verifikasi repositori:

```powershell
python scripts\verify_notebooks.py
```

Jalankan eksekusi notebook lokal yang aman secara penuh sebelum menerbitkan perubahan implementasi:

```powershell
python scripts\verify_notebooks.py --execute
```

Pemeriksaan yang diharapkan:

- tautan Markdown lokal lolos pemeriksaan
- validasi JSON notebook lolos
- notebook tidak mengandung output yang tersimpan atau hitungan eksekusi
- pemindaian pola rahasia berisiko tinggi lolos
- notebook publik dapat dieksekusi secara lokal
- materi draf di bawah `drafts/` sengaja dilewati

## Tinjauan

- Pastikan tautan artikel README mengarah ke file yang dimaksud.
- Pastikan setiap artikel memiliki navigasi repositori dan tautan notebook terkait.
- Pastikan draf tidak terhubung dari indeks publik kecuali sudah siap untuk diterbitkan.
- Pastikan template isu dan pull request GitHub masih sesuai dengan alur kerja repositori.
- Pastikan hasil verifikasi dalam artikel sesuai dengan output notebook terbaru.
- Pastikan alur kerja GitHub Actions akan dijalankan setelah push.
- Pastikan `CHANGELOG.md` mencerminkan pembaruan yang akan diterbitkan.
- Pastikan `CONTRIBUTING.md` masih sesuai dengan alur kerja repositori.

## Git

- Tinjau `git status --short --branch`.
- Tinjau `git diff --stat`.
- Commit dan push hanya saat benar-benar siap.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->