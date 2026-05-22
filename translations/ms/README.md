# Ajar AI Menjawab Soalan Berdasarkan Dokumen Anda

![Gambaran sistem AI RAG berpandukan dokumen](../../assets/images/readme-hero.svg)

Repositori ini mengumpulkan siri blog tahun 2026 tentang membina sistem AI berpandukan dokumen menggunakan RAG, perkhidmatan AI Azure, alternatif sumber terbuka, dan aliran kerja berorientasikan penilaian.

## Latar Belakang

Pada tahun 2023, saya mengendalikan sepasang tutorial mengenai mengajar ChatGPT untuk menjawab soalan daripada dokumen PDF menggunakan Azure AI Search dan Azure OpenAI. Idea "ChatGPT pada data anda" masih terasa baru ketika itu, dan tujuan adalah untuk menunjukkan aliran kerja praktikal: menyimpan dokumen, mengindeksnya, mengambil kandungan yang berkaitan, dan menghasilkan jawapan daripada konteks yang diperoleh.

Pada tahun 2026, ekosistem RAG jauh lebih besar. Azure AI Search menyokong corak pengambilan vektor dan hibrid moden, Azure OpenAI adalah sebahagian daripada ekosistem Model Foundry Microsoft yang lebih luas, dan alat sumber terbuka seperti LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, dan vLLM telah menjadi pilihan praktikal untuk sistem sebenar.

Itulah sebabnya saya mahu mengimbas kembali topik ini. Soalannya bukan lagi hanya "Bagaimana saya membina RAG?" Kini terdapat banyak kaedah untuk membinanya, dan soalan yang lebih penting ialah "Arkitektur mana yang harus saya pilih untuk situasi saya?"

Siri ini bermula dari lapisan membuat keputusan tersebut, kemudian menukarnya menjadi tutorial praktikal. Laluan pelaksanaan pertama membina sistem RAG sumber terbuka tempatan yang boleh dijalankan sesiapa sahaja dengan data contoh, Qdrant, Ollama, dan Phi-4-mini.

## Artikel

Lihat [articles/README.md](./articles/README.md) untuk indeks artikel.

1. [Siri 1: RAG, Azure vs Alternatif Sumber Terbuka, dan Bila Penalaan Semula Masuk Akal](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Siri 2: Bina Sistem RAG Sumber Terbuka Tempatan Dari Awal Hingga Akhir](./articles/series-2-open-source-rag-end-to-end.md)

Akan datang seterusnya:

- Bina semula sistem RAG yang sama dengan Azure AI Search dan Azure OpenAI.
- Tambah penilaian dan pemeriksaan regresi melebihi jawapan demo.

## Nota

Artikel pelaksanaan menggunakan nota supaya langkah pengambilan dan penilaian boleh diperiksa secara langsung. Lihat [notebooks/README.md](./notebooks/README.md) untuk panduan tahap folder.

> [!TIP]
> Mulakan dengan Siri 2 jika anda mahu laluan terpantas. Ia berjalan secara tempatan dengan data contoh, penanaman mesra CPU, mod lokal Qdrant, dan tiada kredensial awan.

| Siri | Nota | Keperluan | Pengesahan tempatan |
| --- | --- | --- | --- |
| Siri 2 | [Nota RAG Sumber Terbuka](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Mod lokal Qdrant, pengambilan, penilaian semula, dan sambungan sumber disahkan |

Untuk menjalankan nota secara tempatan, buat persekitaran maya dan pasang fail keperluan yang sepadan. Contohnya:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Data Contoh

Nota menggunakan korpus kecil tempatan dalam [sample_data](../../sample_data) supaya contoh boleh dijalankan tanpa dokumen peribadi atau kredensial awan. Lihat [sample_data/README.md](./sample_data/README.md) untuk butiran.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Ringkasan Pengesahan Tempatan

Keputusan pengesahan direkodkan dalam setiap artikel dan dalam [SERIES_PLAN.md](./SERIES_PLAN.md).

| Kawasan | Keputusan |
| --- | --- |
| Laluan sumber terbuka Siri 2 | FastEmbed menghasilkan penanaman tempatan berdimensi 384, koleksi dalam ingatan Qdrant memasukkan 8 vektor, penilaian semula ringan memperoleh bahagian yang dijangkakan; generasi Ollama pilihan selesai dengan `phi4-mini:3.8b` |

Nota tempatan sengaja mengelak rahsia yang dikod keras.

## Generasi Ollama Tempatan

Nota Siri 2 selamat secara tempatan secara lalai. Untuk mengaktifkan generasi Ollama tempatan, salin [.env.example](../../.env.example) ke `.env` dan isi nilai Siri 2.

Untuk generasi Ollama Siri 2, nyahkomen:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Nota Siri 2 secara automatik memuat `.env` dari akar repositori menggunakan `python-dotenv`.

> [!IMPORTANT]
> Jangan komit fail `.env`, kunci API, titik akhir peribadi, atau nilai khusus penyewa. Repositori sengaja mengekalkan rahsia di luar fail Markdown dan nota.

Fail keperluan didokumentasikan dalam [requirements/README.md](./requirements/README.md).

Untuk mengesahkan pautan, struktur nota, kebersihan output nota, dan corak rahsia berisiko tinggi:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Skrip pengesahan didokumentasikan dalam [scripts/README.md](./scripts/README.md).

Untuk menjalankan semua nota selamat secara tempatan dalam persekitaran yang sama:

```powershell
python scripts\verify_notebooks.py --execute
```

Aliran pengesahan yang sama dijalankan dalam GitHub Actions pada push, permintaan tarik, dan pengesahan manual aliran kerja. Artikel draf dan nota sengaja dikecualikan daripada laluan pengesahan awam.

Sebelum menerbitkan kemas kini, gunakan [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Lihat [CHANGELOG.md](./CHANGELOG.md) untuk ringkasan perubahan belum diterbitkan terkini.

Untuk garis panduan sumbangan dan kebersihan nota, lihat [CONTRIBUTING.md](./CONTRIBUTING.md).

## Sokongan Pelbagai Bahasa

### Disokong melalui Co-op Translator (Automatik dan Sentiasa Dikemas Kini)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](./README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Lebih Suka Klon Secara Tempatan?**
>
> Repositori ini termasuk terjemahan lebih 50+ bahasa yang secara signifikan meningkatkan saiz muat turun. Untuk klon tanpa terjemahan, gunakan sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Ini memberikan anda semua yang diperlukan untuk melengkapkan kursus dengan muat turun yang jauh lebih pantas.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->