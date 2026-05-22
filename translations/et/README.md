# Õpeta tehisintellekt vastama küsimustele sinu dokumentide põhjal

![Dokumentide-põhine AI RAG süsteemi ülevaade](../../assets/images/readme-hero.svg)

See hoidla koondab 2026. aasta blogiseeria dokumentide-põhiste tehisintellektisüsteemide loomise kohta RAGi, Azure AI teenuste, avatud lähtekoodiga alternatiivide ja hindamiskeskse töövooga.

## Taust

Aastal 2023 töötasin välja kaks õppetutvustust, kuidas õpetada ChatGPT-d vastama PDF-dokumentidest pärit küsimustele, kasutades Azure AI Searchi ja Azure OpenAI-d. Mõte „ChatGPT sinu andmetel” tundus siis veel uus ning eesmärk oli näidata praktilist töövoogu: dokumentide salvestamine, indekseerimine, asjakohase sisu pärimine ja vastuste genereerimine põhinedes päritud kontekstile.

Aastal 2026 on RAG ökosüsteem palju suurem. Azure AI Search toetab kaasaegseid vektori- ja hübriidpäringu mustreid, Azure OpenAI on osa laiemast Microsoft Foundry mudelite ökosüsteemist ning avatud lähtekoodi tööriistad nagu LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ja vLLM on muutunud reaalseks valikuks pärissüsteemide jaoks.

Seetõttu tahtsin seda teemat uuesti käsitleda. Küsimus ei ole enam ainult „Kuidas ma RAGi üles ehitan?” Nüüd on palju viise selle ehitamiseks ning olulisem küsimus on „Millist arhitektuuri valida oma olukorra jaoks?”

See seeria algab sellest otsustuskihtist ja jätkub praktiliste õppetutvustustega. Esimene teostus tekitab lokaalse avatud lähtekoodiga RAG süsteemi, mida igaüks saab proovida näitedataga, Qdranti, Ollama ja Phi-4-mini abil.

## Artiklid

Vaata artiklite indeksi jaoks [articles/README.md](./articles/README.md).

1. [Seeria 1: RAG, Azure vs avatud lähtekoodiga alternatiivid ja millal mõistlik on täiendõpe](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Seeria 2: Ehita lokaalne avatud lähtekoodiga RAG süsteem otsast lõpuni](./articles/series-2-open-source-rag-end-to-end.md)

Järgmised sammud:

- Sama RAG süsteemi uuestisünd Azure AI Searchi ja Azure OpenAI abil.
- Lisa hindamine ja regressioonikontrollid demo vastusest kaugemale.

## Märkmikud

Teostusartiklid kasutavad märkmikke, et pärimise ja hindamise samme saaks otse uurida. Vaata kausta kohta juhiseid [notebooks/README.md](./notebooks/README.md).

> [!TIP]
> Alusta seeriast 2, kui soovid kiireimat rada. See töötab lokaalselt näitedata, protsessori-sõbraliku manustega, Qdrant'i lokaalses režiimis ja ilma pilvautentimiseta.

| Seeria | Märkmik | Nõuded | Kohalik kontroll |
| --- | --- | --- | --- |
| Seeria 2 | [Avatud lähtekoodiga RAG märkmik](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Kontrollitud Qdranti lokaalne režiim, päring, ümberjärjestamine ja allika ühendus |

Märkmiku käivitamiseks lokaalselt loo virtuaalne keskkond ja paigalda sobiv nõudefaile. Näiteks:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Näitedata

Märkmikud kasutavad väikest lokaalset korpust kaustas [sample_data](../../sample_data), et näited saaksid käivituda ilma privaatsete dokumentide või pilveautentimiseta. Vaata üksikasju [sample_data/README.md](./sample_data/README.md).

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Kohaliku kontrolli kokkuvõte

Kontrolli tulemused on dokumenteeritud igas artiklis ning failis [SERIES_PLAN.md](./SERIES_PLAN.md).

| Valdkond | Tulemus |
| --- | --- |
| Seeria 2 avatud lähtekoodiga rada | FastEmbed lõi 384-mõõtmelised lokaalsed manused, Qdrant sisestas mälukogusse 8 vektorit, kergekaaluline ümberjärjestamine tõi oodatud lõigu; valikuline Ollama genereerimine lõpule viidud `phi4-mini:3.8b` abil |

Lokaalne märkmik väldib sihilikult kõvasid salasõnu.

## Lokaalne Ollama genereerimine

Seeria 2 märkmik on vaikimisi lokaalselt turvaline. Lokaalse Ollama genereerimise lubamiseks kopeeri [.env.example](../../.env.example) faili `.env` ja täida seeria 2 väärtused.

Seeria 2 Ollama genereerimiseks eemalda kommentaar:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Seeria 2 märkmik laadib automaatselt `.env` failid hoidla juurest, kasutades `python-dotenv`.

> [!IMPORTANT]
> Ära kunagi lükka `.env` faile, API võtmeid, privaatseid otspunkte ega rentniku-spetsiifilisi väärtusi. Hoidla hoiab sihilikult saladused markdownfailidest ja märkmikest eemal.

Nõudefaile on dokumenteeritud kaustas [requirements/README.md](./requirements/README.md).

Linkide, märkmiku struktuuri, väljundi puhtuse ja kõrge riskiga salajaste mustrite valideerimiseks:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Kontrolliskriptid on dokumenteeritud kaustas [scripts/README.md](./scripts/README.md).

Kõigi lokaalselt turvaliste märkmike samaaegseks käivitamiseks samas keskkonnas:

```powershell
python scripts\verify_notebooks.py --execute
```

Sama kontrolliprotsess töötab GitHub Actions’is, kui toimub ligiüleslaadimine, Pull request või käsitsi töövoo käivitamine. Artiklite ja märkmike eelnökke avalikust kontrollitee on sihilikult välistatud.

Enne uuenduste avaldamist kasuta [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Praeguse mitteavaliku muudatuste kokkuvõtte leiad failist [CHANGELOG.md](./CHANGELOG.md).

Panustamise ja märkmike hooldusjuhiste jaoks vaata [CONTRIBUTING.md](./CONTRIBUTING.md).

## Mitmekeelne tugi

### Co-op Tõlkija kaudu toetatud (Automaatne ja alati ajakohane)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Araabia](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgaaria](../bg/README.md) | [Burma (Myanmar)](../my/README.md) | [Hiina (lihtsustatud)](../zh-CN/README.md) | [Hiina (traditsiooniline, Hongkong)](../zh-HK/README.md) | [Hiina (traditsiooniline, Macau)](../zh-MO/README.md) | [Hiina (traditsiooniline, Taiwan)](../zh-TW/README.md) | [Horvaadi](../hr/README.md) | [Tšehhi](../cs/README.md) | [Taani](../da/README.md) | [Hollandi](../nl/README.md) | [Eesti](./README.md) | [Soome](../fi/README.md) | [Prantsuse](../fr/README.md) | [Saksa](../de/README.md) | [Kreeka](../el/README.md) | [Heebrea](../he/README.md) | [Hindi](../hi/README.md) | [Ungari](../hu/README.md) | [Indoneesia](../id/README.md) | [Itaalia](../it/README.md) | [Jaapani](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korea](../ko/README.md) | [Leedu](../lt/README.md) | [Malai](../ms/README.md) | [Malajalami](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigeeria pidžin](../pcm/README.md) | [Norra](../no/README.md) | [Pärsia (Farsi)](../fa/README.md) | [Poola](../pl/README.md) | [Portugali (Brasiilia)](../pt-BR/README.md) | [Portugali (Portugal)](../pt-PT/README.md) | [Pandžabi (Gurmukhi)](../pa/README.md) | [Rumeenia](../ro/README.md) | [Vene](../ru/README.md) | [Serbia (kirillitsa)](../sr/README.md) | [Slovaki](../sk/README.md) | [Sloveeni](../sl/README.md) | [Hispaania](../es/README.md) | [Suahiili](../sw/README.md) | [Rootsi](../sv/README.md) | [Tagalogi (Filipino)](../tl/README.md) | [Tamili](../ta/README.md) | [Telugu](../te/README.md) | [Tai](../th/README.md) | [Türgi](../tr/README.md) | [Ukraina](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnami](../vi/README.md)

> **Eelistad kloonimist kohalikult?**
>
> See hoidla sisaldab üle 50 keele tõlkeid, mis suurendavad oluliselt allalaadimise mahtu. Kõikide tõlgeteta kloonimiseks kasuta harva esinevat checkouti:
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
> See annab sulle kõik vajaliku kursuse lõpetamiseks palju kiirema allalaadimisega.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->