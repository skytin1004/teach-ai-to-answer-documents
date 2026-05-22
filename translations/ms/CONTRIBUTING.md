# Menyumbang

Repositori ini diatur sebagai siri blog plus contoh buku nota boleh jalankan.

## Sebelum Membuka Permintaan Tarikan

Jalankan skrip pengesahan tempatan:

```powershell
python scripts\verify_notebooks.py
```

Untuk pelaksanaan atau perubahan buku nota, jalankan pelaksanaan buku nota tempatan-selamat:

```powershell
python scripts\verify_notebooks.py --execute
```

## Garis Panduan Buku Nota

- Pastikan buku nota dapat dibaca dan tertumpu pada artikel berkaitan.
- Jangan komit keluaran buku nota yang disimpan atau kiraan pelaksanaan.
- Gunakan data sampel kecil dari `sample_data/` kecuali artikel memerlukan sumber luaran tertentu.
- Rekod hasil pengesahan dalam artikel berkaitan apabila tingkah laku berubah.

## Rahsia dan Kelayakan

- Jangan komit kunci API, token, kata laluan, titik akhir persendirian, atau fail `.env`.
- Gunakan `.env.example` hanya untuk nilai tempat letak.
- Gunakan pemboleh ubah persekitaran untuk eksperimen Ollama tempatan pilihan.

## Dokumentasi

- Pastikan pautan navigasi artikel dikemas kini.
- Kemas kini `README.md` apabila menambah artikel baru, buku nota, fail keperluan, atau fail data sampel.
- Kemas kini `CHANGELOG.md` sebelum menerbitkan kemas kini repositori yang dapat dilihat.

## Pengesahan

Aliran kerja GitHub Actions menjalankan:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Bahan draf di bawah `drafts/` diabaikan oleh pengesahan repositori sehingga ia sedia untuk pengindeksan awam.

## Isu

Gunakan templat maklum balas artikel untuk pembetulan artikel dan templat isu buku nota untuk masalah pelaksanaan buku nota.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->