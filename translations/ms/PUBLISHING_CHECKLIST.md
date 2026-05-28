# Senarai Semak Penerbitan

Gunakan senarai semak ini sebelum melakukan komit atau menolak kemas kini awam.

## Keselamatan

- Sahkan tiada kekunci API, token, kata laluan, atau titik akhir peribadi ditulis dalam fail Markdown, buku nota, data contoh, atau skrip.
- Simpan kelayakan dalam pembolehubah persekitaran atau identiti yang diurus, bukan dalam fail yang dikomit.
- Jangan komit fail `.env` atau fail output buku nota yang telah dijalankan.
- Simpan `.env.example` hanya sebagai tempat letak.

## Pengesahan

Jalankan skrip pengesahan repositori:

```powershell
python scripts\verify_notebooks.py
```

Jalankan pelaksanaan buku nota selamat tempatan sepenuhnya sebelum menerbitkan perubahan pelaksanaan:

```powershell
python scripts\verify_notebooks.py --execute
```

Pemeriksaan yang dijangka:

- pautan Markdown tempatan lulus
- pengesahan JSON buku nota lulus
- buku nota tidak mengandungi output yang disimpan atau kiraan pelaksanaan
- imbasan corak rahsia berisiko tinggi lulus
- buku nota awam dijalankan secara tempatan
- bahan draf di bawah `drafts/` sengaja diabaikan

## Semakan

- Sahkan pautan artikel README menunjuk ke fail yang dimaksudkan.
- Sahkan setiap artikel mempunyai navigasi repositori dan pautan buku nota berkaitan.
- Sahkan draf tidak dipautkan dari indeks awam melainkan ia sudah sedia untuk diterbitkan.
- Sahkan templat isu dan permintaan tarik GitHub masih mematuhi aliran kerja repositori.
- Sahkan keputusan pengesahan dalam artikel sepadan dengan output buku nota terkini.
- Sahkan aliran kerja GitHub Actions dijangka berjalan selepas tolak.
- Sahkan `CHANGELOG.md` mencerminkan kemas kini yang diterbitkan.
- Sahkan `CONTRIBUTING.md` masih mematuhi aliran kerja repositori.

## Git

- Semak `git status --short --branch`.
- Semak `git diff --stat`.
- Komit dan tolak hanya apabila benar-benar bersedia.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->