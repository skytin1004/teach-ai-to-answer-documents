# Tanítsd meg az AI-nak, hogyan válaszoljon kérdésekre a dokumentumaid alapján

Ez a tároló egy 2026-os blog sorozatot gyűjt össze, amely a dokumentumokra épülő AI rendszerek építéséről szól RAG, Azure AI szolgáltatások, nyílt forráskódú alternatívák és értékelés-orientált munkafolyamatok segítségével.

## Háttér

2023-ban két oktatóanyagon dolgoztam arról, hogyan tanítsuk meg a ChatGPT-t arra, hogy PDF dokumentumokból származó kérdésekre válaszoljon az Azure AI Search és az Azure OpenAI használatával. Akkoriban a „ChatGPT az adataidon” ötlete még újnak számított, és a cél egy gyakorlati munkafolyamat bemutatása volt: dokumentumok tárolása, indexelése, releváns tartalom lekérése, és az ebből a lekért kontextusból történő válasz generálása.

2026-ra a RAG ökoszisztéma sokkal nagyobb lett. Az Azure AI Search támogatja a modern vektoros és hibrid lekérdezési mintákat, az Azure OpenAI a Microsoft Foundry Models szélesebb ökoszisztéma része, és a nyílt forráskódú eszközök, mint a LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama és vLLM gyakorlati választások lettek valódi rendszerek számára.

Ezért akartam újra foglalkozni ezzel a témával. A kérdés már nem csak az, hogy „Hogyan építsek RAG-et?” Ma már sokféleképpen lehet építeni, és a fontosabb kérdés az, hogy „Milyen architektúrát válasszak a saját helyzetemhez?”

Ez a sorozat ebből a döntési rétegből indul ki. Mielőtt mélyen belemennénk a megvalósításba, megvizsgálja, hogy az MI szolgáltatásoknak miért van szükségük lekérésre, mikor érdemes Azure-alapú kezelt szolgáltatásokat használni, mikor jobb alternatíva a nyílt forráskódú megoldás, és hová illeszkedik a finomhangolás.

## Cikkek

1. [1. sorozat: RAG, Azure vs nyílt forráskódú alternatívák, és mikor érdemes finomhangolni](./series-1-rag-azure-open-source-fine-tuning.md)

## Többnyelvű támogatás

### A Co-op Translator segítségével támogatott (Automatizált és mindig naprakész)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arab](../ar/README.md) | [Bengáli](../bn/README.md) | [Bolgár](../bg/README.md) | [Burmai (Mianmar)](../my/README.md) | [Kínai (egyszerűsített)](../zh-CN/README.md) | [Kínai (hagyományos, Hongkong)](../zh-HK/README.md) | [Kínai (hagyományos, Makaó)](../zh-MO/README.md) | [Kínai (hagyományos, Tajvan)](../zh-TW/README.md) | [Horvát](../hr/README.md) | [Cseh](../cs/README.md) | [Dán](../da/README.md) | [Holland](../nl/README.md) | [Észt](../et/README.md) | [Finn](../fi/README.md) | [Francia](../fr/README.md) | [Német](../de/README.md) | [Görög](../el/README.md) | [Héber](../he/README.md) | [Hindi](../hi/README.md) | [Magyar](./README.md) | [Indonéz](../id/README.md) | [Olasz](../it/README.md) | [Japán](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreai](../ko/README.md) | [Litván](../lt/README.md) | [Maláj](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepáli](../ne/README.md) | [Nigériai pidgin](../pcm/README.md) | [Norvég](../no/README.md) | [Perzsa (fárszi)](../fa/README.md) | [Lengyel](../pl/README.md) | [Portugál (Brazília)](../pt-BR/README.md) | [Portugál (Portugália)](../pt-PT/README.md) | [Pandzsábi (Gurmukhi)](../pa/README.md) | [Román](../ro/README.md) | [Orosz](../ru/README.md) | [Szerb (cirill)](../sr/README.md) | [Szlovák](../sk/README.md) | [Szlovén](../sl/README.md) | [Spanyol](../es/README.md) | [Szuahéli](../sw/README.md) | [Svéd](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Török](../tr/README.md) | [Ukrán](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnami](../vi/README.md)

> **Inkább helyileg klónoznád?**
>
> Ez a tároló több mint 50 nyelvi fordítást tartalmaz, ami jelentősen megnöveli a letöltés méretét. Ha fordítások nélkül szeretnéd klónozni, használj sparse checkout-ot:
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
> Ez minden szükséges fájlt tartalmaz, hogy gyorsabban töltsd le és elvégezd a kurzust.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->