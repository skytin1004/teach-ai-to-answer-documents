# Tanítsd meg az MI-t a dokumentumaid alapján kérdések megválaszolására

![Dokumentumalapú MI RAG rendszer áttekintése](../../assets/images/readme-hero.svg)

Ez a tároló egy 2026-os blog-sorozatot gyűjt össze a dokumentumalapú MI rendszerek építéséről RAG, Azure AI szolgáltatások, nyílt forráskódú alternatívák és értékelésorientált munkafolyamatok segítségével.

## Háttér

2023-ban dolgoztam két oktatóanyagon arról, hogyan tanítsuk meg a ChatGPT-t PDF dokumentumokból származó kérdések megválaszolására az Azure AI Search és Azure OpenAI használatával. Akkor még újnak tűnt az „adatokon futó ChatGPT” ötlete, és a cél egy gyakorlati munkafolyamat bemutatása volt: dokumentumok tárolása, indexelése, releváns tartalom előkeresése és válaszok generálása a lekért tartalom alapján.

2026-ra a RAG ökoszisztéma sokkal nagyobb lett. Az Azure AI Search támogatja a modern vektoros és hibrid keresési mintákat, az Azure OpenAI a szélesebb Microsoft Foundry Models ökoszisztéma része, és olyan nyílt forráskódú eszközök, mint a LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, és vLLM gyakorlati választások lettek valós rendszerekhez.

Ezért akartam újra elővenni ezt a témát. A kérdés már nemcsak az, hogy „Hogyan építsek RAG-et?” Most már sokféleképpen lehet ezt megtenni, és a fontosabb kérdés az, hogy „Melyik architektúrát válasszam a saját helyzetemre?”

Ez a sorozat ettől a döntési rétegtől indul, majd gyakorlati oktatóanyagokká alakul. Az első megvalósítási út egy helyi, nyílt forráskódú RAG rendszert épít, amelyet bárki futtathat mintadokumentumokkal, Qdrant-tal, Ollama-val és Phi-4-mini-vel.

## Cikkek

Lásd a [articles/README.md](./articles/README.md) fájlt a cikkek indexéhez.

1. [1. sorozat: RAG, Azure és nyílt forráskódú alternatívák, valamint mikor érdemes finomhangolás](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [2. sorozat: Helyi nyílt forráskódú RAG rendszer építése végig](./articles/series-2-open-source-rag-end-to-end.md)

Hamarosan:

- Azonos RAG rendszer újraépítése Azure AI Search és Azure OpenAI használatával.
- Értékelés és regressziós ellenőrzések hozzáadása a demó válaszon túl.

## Jegyzetfüzetek

A megvalósító cikkek jegyzetfüzeteket használnak, így a lekérdezési és értékelési lépések közvetlenül átnézhetők. Lásd a [notebooks/README.md](./notebooks/README.md) útmutatót a mappaszintű tájékoztatásért.

> [!TIP]
> Ha a leggyorsabb utat szeretnéd, kezd a 2. sorozattal. Ez helyileg fut mintadokumentumokkal, CPU-barát beágyazásokkal, Qdrant helyi móddal és felhőbeli hitelesítők nélkül.

| Sorozat | Jegyzetfüzet | Követelmények | Helyi ellenőrzés |
| --- | --- | --- | --- |
| 2. sorozat | [Nyílt forráskódú RAG jegyzetfüzet](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant helyi mód, lekérdezés, rangsorolás és forráskapcsolás ellenőrizve |

Jegyzetfüzet helyi futtatásához készíts virtuális környezetet és telepítsd a megfelelő követelményfájlt. Például:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Mintadokumentumok

A jegyzetfüzetek kis helyi korpuszt használnak a [sample_data](../../sample_data) mappában, így a példák futtathatók privát dokumentumok vagy felhőbeli hitelesítők nélkül. Lásd a [sample_data/README.md](./sample_data/README.md) fájlt a részletekért.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Helyi ellenőrzés összefoglaló

Az ellenőrzési eredmények minden cikkben és a [SERIES_PLAN.md](./SERIES_PLAN.md) fájlban rögzítve vannak.

| Terület | Eredmény |
| --- | --- |
| 2. sorozat nyílt forráskódú útvonal | FastEmbed 384 dimenziós helyi beágyazásokat generált, a Qdrant memóriában 8 vektort szúrt be, a könnyű rangsorolás a várt szakaszt hozta elő; opcionálisan Ollama generálás a `phi4-mini:3.8b`-vel befejeződött |

A helyi jegyzetfüzet szándékosan elkerüli a keménykódolt titkokat.

## Helyi Ollama generálás

A 2. sorozat jegyzetfüzete alapértelmezés szerint helyileg biztonságos. A helyi Ollama generálás engedélyezéséhez másold át a [.env.example](../../.env.example) fájlt `.env` néven, és töltsd ki a 2. sorozat értékeit.

A 2. sorozatbeli Ollama generáláshoz vedd ki megjegyzésjelzést:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

A 2. sorozat jegyzetfüzete automatikusan betölti a `.env` fájlt a tároló gyökérkönyvtárából a `python-dotenv` segítségével.

> [!IMPORTANT]
> Ne töltsd fel a `.env` fájlokat, API kulcsokat, privát végpontokat vagy bérlő-specifikus értékeket. A tároló szándékosan tartja a titkokat távol a Markdown fájloktól és jegyzetfüzetektől.

A követelményfájlokról a [requirements/README.md](./requirements/README.md) fájlban van dokumentáció.

A linkek, jegyzetfüzet-struktúra, jegyzetfüzet kimenet tisztasága és magas biztonsági kockázatú titkos minták ellenőrzéséhez:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Az ellenőrző szkriptekről a [scripts/README.md](./scripts/README.md) fájlban találsz leírást.

Az összes helyileg biztonságos jegyzetfüzet lefuttatásához ugyanabban a környezetben:

```powershell
python scripts\verify_notebooks.py --execute
```

Ugyanez az ellenőrzési folyamat fut GitHub Actions-ben push-ok, pull requestek és kézi munkafolyamat-indítások alkalmával. Vázlatcikkek és jegyzetfüzetek szándékosan ki vannak zárva a nyilvános ellenőrzési folyamatból.

Frissítések közzététele előtt használd a [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md) fájlt.

Lásd a jelenleg nem publikált változtatások összefoglalóját a [CHANGELOG.md](./CHANGELOG.md) fájlban.

Az együttműködés és jegyzetfüzet-higiénia irányelveiért nézd meg a [CONTRIBUTING.md](./CONTRIBUTING.md) fájlt.

## Többnyelvű támogatás

### Co-op Translator segítségével (Automatikus és Mindig Naprakész)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arab](../ar/README.md) | [Bengáli](../bn/README.md) | [Bolgár](../bg/README.md) | [Burmai (Mianmar)](../my/README.md) | [Kínai (Egyszerűsített)](../zh-CN/README.md) | [Kínai (Hagyományos, Hongkong)](../zh-HK/README.md) | [Kínai (Hagyományos, Makaó)](../zh-MO/README.md) | [Kínai (Hagyományos, Tajvan)](../zh-TW/README.md) | [Horvát](../hr/README.md) | [Cseh](../cs/README.md) | [Dán](../da/README.md) | [Holland](../nl/README.md) | [Észt](../et/README.md) | [Finn](../fi/README.md) | [Francia](../fr/README.md) | [Német](../de/README.md) | [Görög](../el/README.md) | [Héber](../he/README.md) | [Hindi](../hi/README.md) | [Magyar](./README.md) | [Indonéz](../id/README.md) | [Olasz](../it/README.md) | [Japán](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreai](../ko/README.md) | [Litván](../lt/README.md) | [Maláj](../ms/README.md) | [Malajálam](../ml/README.md) | [Maráthi](../mr/README.md) | [Nepáli](../ne/README.md) | [Nigériai Pidgin](../pcm/README.md) | [Norvég](../no/README.md) | [Perzsa (Fárszi)](../fa/README.md) | [Lengyel](../pl/README.md) | [Portugál (Brazília)](../pt-BR/README.md) | [Portugál (Portugália)](../pt-PT/README.md) | [Pandzsábi (Gurmukhi)](../pa/README.md) | [Román](../ro/README.md) | [Orosz](../ru/README.md) | [Szerb (Cirill)](../sr/README.md) | [Szlovák](../sk/README.md) | [Szlovén](../sl/README.md) | [Spanyol](../es/README.md) | [Szuahéli](../sw/README.md) | [Svéd](../sv/README.md) | [Tagalog (Fülöp-szigetek)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tháj](../th/README.md) | [Török](../tr/README.md) | [Ukrán](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnami](../vi/README.md)

> **Szeretnéd helyileg klónozni?**
>
> Ez a tároló 50+ nyelvi fordítást tartalmaz, amelyek jelentősen megnövelik a letöltési méretet. Ha fordítások nélkül szeretnéd klónozni, használj szűkített letöltést:
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
> Így minden szükséges fájl meglesz a kurzus elvégzéséhez sokkal gyorsabb letöltéssel.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->