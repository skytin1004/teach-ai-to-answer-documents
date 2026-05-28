# Nauči AI da Odgovara na Pitanja Temeljena na Tvojim Dokumentima

![Pregled AI sustava RAG temeljenog na dokumentima](../../assets/images/readme-hero.svg)

Ovo spremište prikuplja seriju blogova iz 2026. o izgradnji AI sustava temeljenih na dokumentima s RAG-om, Azure AI uslugama, otvorenim izvorima i radnim tokovima usmjerenim na evaluaciju.

## Pozadina

U 2023., radio sam na paru vodiča o poučavanju ChatGPT-a da odgovara na pitanja iz PDF dokumenata koristeći Azure AI Search i Azure OpenAI. Ideja "ChatGPT na tvojim podacima" tada je još bila nova, a cilj je bio pokazati praktičan radni tijek: spremanje dokumenata, indeksiranje, dohvat relevantnog sadržaja i generiranje odgovora iz tog dohvaćenog konteksta.

Godine 2026., RAG ekosustav je mnogo veći. Azure AI Search podržava moderne vektorske i hibridne obrasce dohvata, Azure OpenAI je dio šireg Microsoft Foundry Models ekosustava, a alati otvorenog koda kao što su LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama i vLLM postali su praktični izbori za stvarne sustave.

Zbog toga sam htio ponovno obraditi ovu temu. Pitanje više nije samo "Kako izgraditi RAG?" Sada postoji mnogo načina za njegovu izgradnju, a važnije pitanje je "Koju arhitekturu trebam odabrati za svoju situaciju?"

Ova serija počinje od te razine donošenja odluke, a zatim se pretvara u praktične vodiče. Prvi put realizacije gradi lokalni open-source RAG sustav koji svatko može pokrenuti s uzorcima podataka, Qdrantom, Ollamom i Phi-4-mini.

## Članci

Pogledajte [articles/README.md](./articles/README.md) za indeks članaka.

1. [Serija 1: RAG, Azure vs Otvorene alternative i Kada je Fine-Tuning smislen](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serija 2: Izgradnja Lokalnog Open-Source RAG Sustava od Početka do Kraja](./articles/series-2-open-source-rag-end-to-end.md)

Uskoro slijedi:

- Ponovno izgraditi isti RAG sustav s Azure AI Search i Azure OpenAI.
- Dodati evaluaciju i regresijske provjere osim demo odgovora.

## Bilježnice

Članci o implementaciji koriste bilježnice kako bi se koraci dohvaćanja i evaluacije mogli direktno pregledati. Pogledajte [notebooks/README.md](./notebooks/README.md) za upute na razini mape.

> [!TIP]
> Počni sa Serijom 2 ako želiš najbrži put. Pokreće se lokalno s uzorcima podataka, CPU-prijateljskim embeddingsima, Qdrant lokalnim načinom i bez cloud vjerodajnica.

| Serija | Bilježnica | Zahtjevi | Lokalna verifikacija |
| --- | --- | --- | --- |
| Serija 2 | [Bilježnica Open-source RAG](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Verificiran Qdrant lokalni način, dohvaćanje, prerangiranje i povezivanje izvora |

Za lokalno pokretanje bilježnice, stvori virtualno okruženje i instaliraj odgovarajuću datoteku sa zahtjevima. Na primjer:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Uzorak podataka

Bilježnice koriste mali lokalni korpus u [sample_data](../../sample_data) kako bi primjeri mogli raditi bez privatnih dokumenata ili cloud vjerodajnica. Pogledajte [sample_data/README.md](./sample_data/README.md) za detalje.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Sažetak lokalne verifikacije

Rezultati verifikacije zabilježeni su u svakom članku i u [SERIES_PLAN.md](./SERIES_PLAN.md).

| Područje | Rezultat |
| --- | --- |
| Otvorena staza Serije 2 | FastEmbed je generirao 384-dimenzionalne lokalne embeddings, Qdrant je u memorijsku kolekciju umetnuo 8 vektora, lagano prerangiranje dohvatilo je očekivani odjeljak; opcionalna Ollama generacija završena s `phi4-mini:3.8b` |

Lokalna bilježnica namjerno izbjegava hardkodirane tajne.

## Lokalna Ollama Generacija

Bilježnica Serije 2 je po zadanim postavkama sigurna za lokalno korištenje. Za omogućavanje lokalne Ollama generacije, kopirajte [.env.example](../../.env.example) u `.env` i ispunite vrijednosti za Seriju 2.

Za Ollama generaciju iz Serije 2, uklonite komentar:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Bilježnica Serije 2 automatski učitava `.env` iz korijena spremišta koristeći `python-dotenv`.

> [!IMPORTANT]
> Nemojte pohranjivati `.env` datoteke, API ključeve, privatne krajnje točke niti vrijednosti specifične za zakupnika. Spremište namjerno drži tajne izvan Markdown datoteka i bilježnica.

Datoteke zahtjeva su dokumentirane u [requirements/README.md](./requirements/README.md).

Za validaciju poveznica, strukture bilježnica, čistoće izlaza i obrasca visokorizičnih tajni:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Skripte za verifikaciju su dokumentirane u [scripts/README.md](./scripts/README.md).

Za izvođenje svih lokalno sigurnih bilježnica u istom okruženju:

```powershell
python scripts\verify_notebooks.py --execute
```

Isti tok verifikacije izvršava se u GitHub Actions prilikom pushanja, pull requestova i ručnih pokretanja radnog tijeka. Skice članaka i bilježnica namjerno su isključene iz javnog puta verifikacije.

Prije objave ažuriranja, koristi [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Pogledaj [CHANGELOG.md](./CHANGELOG.md) za trenutni neobjavljeni sažetak promjena.

Za smjernice o doprinosima i higijeni bilježnica, vidi [CONTRIBUTING.md](./CONTRIBUTING.md).

## Podrška za Više Jezika

### Podržano putem Co-op Translatora (Automatski i Uvijek Ažurni)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](./README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Preferiraš Klonirati Lokalno?**
>
> Ovo spremište uključuje prijevode na više od 50 jezika što znatno povećava veličinu preuzimanja. Za kloniranje bez prijevoda, koristi sparse checkout:
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
> Ovo ti daje sve što trebaš za završetak tečaja s puno bržim preuzimanjem.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->