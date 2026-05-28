# Notebooks

Notebook-notebook ini menyokong siri artikel dengan contoh yang boleh dijalankan.

| Notebook | Artikel | Tujuan |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG sumber terbuka dengan FastEmbed, mod tempatan Qdrant, pengambilan, penilaian semula, penjanaan Ollama pilihan, dan rujukan sumber |

## Jalankan Secara Tempatan

Pasang keperluan untuk notebook yang anda mahu jalankan:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Atau pasang semua kebergantungan:

```powershell
python -m pip install -r requirements\all.txt
```

## Sahkan

Dari akar repositori:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Siri 2 boleh membaca konfigurasi Ollama dari fail `.env` akar repositori. Mulakan dari [../.env.example](../../../.env.example), yang disusun mengikut siri.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->