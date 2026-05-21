# Ajar AI Menjawab Soalan Berdasarkan Dokumen Anda

Repositori ini mengumpulkan siri blog 2026 tentang membina sistem AI berpandukan dokumen dengan RAG, perkhidmatan Azure AI, alternatif sumber terbuka, dan aliran kerja berorientasikan penilaian.

## Latar Belakang

Pada 2023, saya mengusahakan sepasang tutorial tentang mengajar ChatGPT menjawab soalan dari dokumen PDF menggunakan Azure AI Search dan Azure OpenAI. Idea "ChatGPT pada data anda" masih terasa baru ketika itu, dan matlamatnya adalah untuk menunjukkan aliran kerja praktikal: menyimpan dokumen, mengindeksnya, mendapatkan kandungan yang relevan, dan menjana jawapan dari konteks yang diperoleh itu.

Pada 2026, ekosistem RAG jauh lebih besar. Azure AI Search menyokong corak pengambilan vektor moden dan hibrid, Azure OpenAI adalah sebahagian daripada ekosistem Model Microsoft Foundry yang lebih luas, dan alat sumber terbuka seperti LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, dan vLLM telah menjadi pilihan praktikal untuk sistem sebenar.

Itulah sebabnya saya ingin meninjau semula topik ini. Soalannya bukan lagi hanya "Bagaimana saya membina RAG?" Kini terdapat banyak cara untuk membinanya, dan soalan yang lebih penting ialah "Seni bina manakah yang harus saya pilih untuk situasi saya?"

Siri ini bermula dari lapisan membuat keputusan itu. Sebelum mendalami pelaksanaan, ia melihat mengapa perkhidmatan AI memerlukan pengambilan, bila perkhidmatan terurus berasaskan Azure masuk akal, bila alternatif sumber terbuka lebih sesuai, dan di mana penyelarasan (fine-tuning) sesuai.

## Artikel

1. [Siri 1: RAG, Azure vs Alternatif Sumber Terbuka, dan Bila Penyelarasan (Fine-Tuning) Masuk Akal](./series-1-rag-azure-open-source-fine-tuning.md)

## Sokongan Pelbagai Bahasa

### Disokong melalui Penterjemah Kerjasama (Automatik dan Sentiasa Dikemaskini)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](./README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Lebih Suka Klon Secara Tempatan?**
>
> Repositori ini termasuk terjemahan lebih dari 50+ bahasa yang secara signifikan meningkatkan saiz muat turun. Untuk klon tanpa terjemahan, gunakan sparse checkout:
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
> Ini memberi anda segala yang anda perlukan untuk melengkapkan kursus dengan muat turun yang lebih pantas.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->