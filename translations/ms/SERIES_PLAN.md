# Ajarkan AI Menjawab Soalan Berdasarkan Dokumen Anda - Pelan Siri

Pelan ini menjejaki keluaran awam Siri 1 dan Siri 2. Kerja Azure dan penilaian kemudian disimpan sebagai draf sehingga contoh sepenuhnya hujung ke hujung dan disahkan.

Jangan komit atau tolak perubahan sehingga diarahkan secara eksplisit.

## Skop Awam

Keluaran awam semasa:

- Artikel Siri 1: keputusan seni bina RAG, pertukaran Azure vs sumber terbuka, dan di mana penyelarasan sesuai.
- Artikel Siri 2: tutorial RAG sumber terbuka tempatan.
- Buku nota Siri 2: makmal RAG tempatan yang boleh dijalankan dengan FastEmbed, Qdrant, Ollama, dan Phi-4-mini.
- Data contoh: fail Markdown dasar sekolah dan panduan AI kursus.

Draf tetapi belum dalam indeks awam:

- Pembinaan semula Azure AI Search dan Azure OpenAI.
- Penilaian dan pemeriksaan regresi RAG.

## Senario Tutorial

Senario dikongsi ialah pembantu dasar sekolah.

Pembantu menjawab soalan ini dari dokumen tempatan:

```text
Can I use generative AI for my final assignment?
```

Tingkah laku dijangka adalah:

1. Muatkan dokumen Markdown tempatan.
2. Parse dan pecahkan mengikut tajuk.
3. Cipta embedding tempatan dan simpan representasi boleh carian dengan metadata.
4. Dapatkan bahagian dasar yang berkaitan.
5. Susun semula apabila perlu.
6. Hasilkan atau rangka jawapan yang berasaskan fakta.
7. Pulangkan sitasi.
8. Rekod keputusan pengesahan.

## Struktur Awam Semasa

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

Bahan draf disimpan di bawah `drafts/` dan diabaikan oleh pengesahan repositori sehingga bersedia untuk pengindeksan awam.

## Pengesahan Siri 2

Disahkan pada Windows dengan Python 3.12.6.

- Berjaya memasang `requirements/open-source-rag.txt`.
- Melaksanakan `notebooks/series-2-open-source-rag.ipynb` dengan `nbclient`.
- Pengesahan tempatan lulus: 2 dokumen contoh dimuatkan, 8 kepingan dicipta, FastEmbed menghasilkan embedding tempatan berdimensi 384, koleksi dalam memori Qdrant dipasang, dan 8 vektor dimasukkan.
- Soalan ujian: "Bolehkah saya menggunakan AI generatif untuk tugasan akhir saya?"
- Sumber teratas yang diperoleh selepas susun semula ringan: `school_ai_policy.md`.
- Bahagian teratas yang diperoleh selepas susun semula ringan: `Final Assignments`.
- Laluan jawapan lalai: komposer jawapan telus tempatan.
- Ollama dipasang melalui winget; `phi4-mini:3.8b` berjaya dimuat turun.
- Laluan penjanaan jawapan Ollama: selesai dengan `phi4-mini:3.8b`.
- Saiz fail model Ollama: kira-kira 2.49GB di cakera.
- Saiz model Ollama yang dimuatkan: 3.3GB dilaporkan oleh `ollama ps`.
- Pelepasan GPU: 100% GPU dilaporkan oleh `ollama ps` pada RTX 3060 Laptop GPU.
- Memori GPU diperhatikan selepas penjanaan: kira-kira 3.5GB daripada 6GB.
- Pelaksanaan buku nota dengan model FastEmbed yang disimpan dalam cache dan penjanaan Ollama didayakan lulus dalam kira-kira 34 saat melalui skrip pengesahan.
- Pemerhatian: satu laluan muat naik dokumen awal secara tidak sengaja memasukkan `sample_data/README.md`; buku nota kini hanya memuatkan dua dokumen contoh yang dimaksudkan secara eksplisit.

## Pengesahan Repositori

- `scripts/verify_notebooks.py` mengesahkan pautan Markdown tempatan, JSON buku nota, kebersihan output buku nota, dan corak rahsia berisiko tinggi.
- `scripts/verify_notebooks.py --execute` menjalankan buku nota awam dari akar repositori.
- Bahan draf di bawah `drafts/` sengaja diabaikan.

## Kerja Seterusnya

- Bina semula senario yang sama dengan Azure AI Search dan Azure OpenAI sebagai bahagian siri masa depan.
- Tambah penarikan dan penilaian jawapan apabila pelaksanaan tempatan dan Azure keduanya stabil.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->