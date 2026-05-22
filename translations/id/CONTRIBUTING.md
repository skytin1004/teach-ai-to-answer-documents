# Berkontribusi

Repositori ini disusun sebagai seri blog plus contoh notebook yang dapat dijalankan.

## Sebelum Membuka Pull Request

Jalankan skrip validasi lokal:

```powershell
python scripts\verify_notebooks.py
```

Untuk perubahan implementasi atau notebook, jalankan eksekusi notebook lokal yang aman:

```powershell
python scripts\verify_notebooks.py --execute
```

## Panduan Notebook

- Jaga agar notebook tetap dapat dibaca dan fokus pada artikel terkait.
- Jangan meng-commit output notebook yang disimpan atau jumlah eksekusi.
- Gunakan data sampel kecil dari `sample_data/` kecuali artikel memerlukan sumber eksternal tertentu.
- Catat hasil verifikasi di artikel terkait saat perilaku berubah.

## Rahasia dan Kredensial

- Jangan meng-commit kunci API, token, kata sandi, endpoint privat, atau file `.env`.
- Gunakan `.env.example` hanya untuk nilai placeholder.
- Gunakan variabel lingkungan untuk eksperimen Ollama lokal opsional.

## Dokumentasi

- Jaga agar tautan navigasi artikel tetap mutakhir.
- Perbarui `README.md` saat menambahkan artikel baru, notebook, file persyaratan, atau file data sampel.
- Perbarui `CHANGELOG.md` sebelum menerbitkan pembaruan repositori yang terlihat.

## Verifikasi

Workflow GitHub Actions menjalankan:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Bahan rancangan di bawah `drafts/` dilewati oleh verifikasi repositori sampai siap untuk pengindeksan publik.

## Masalah

Gunakan template umpan balik artikel untuk koreksi artikel dan template masalah notebook untuk masalah eksekusi notebook.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->