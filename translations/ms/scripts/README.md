# Skrip

Folder ini mengandungi skrip pengesahan repositori.

## `verify_notebooks.py`

Mengesahkan pautan Markdown tempatan, JSON notebook, kebersihan output notebook, dan corak rahsia berisiko tinggi:

```powershell
python scripts\verify_notebooks.py
```

Melaksanakan semua notebook tempatan selamat awam:

```powershell
python scripts\verify_notebooks.py --execute
```

Aliran kerja GitHub Actions menggunakan skrip yang sama.

Bahan draf di bawah `drafts/` diabaikan sehingga ia siap untuk indeks awam.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->