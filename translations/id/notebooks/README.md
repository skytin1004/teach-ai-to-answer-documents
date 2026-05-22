# Notebooks

Notebook ini mendukung rangkaian artikel dengan contoh yang dapat dijalankan.

| Notebook | Artikel | Tujuan |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Seri 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG sumber terbuka dengan FastEmbed, mode lokal Qdrant, pengambilan, pengurutan ulang, pembuatan Ollama opsional, dan referensi sumber |

## Jalankan Secara Lokal

Pasang persyaratan untuk notebook yang ingin Anda jalankan:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Atau pasang semua dependensi:

```powershell
python -m pip install -r requirements\all.txt
```

## Verifikasi

Dari root repositori:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Seri 2 dapat membaca konfigurasi Ollama dari file `.env` di root repositori. Mulai dari [../.env.example](../../../.env.example), yang dikelompokkan berdasarkan seri.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->