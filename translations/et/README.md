# Õpeta tehisintellekt vastama küsimustele sinu dokumentide põhjal

See hoidla koondab aastal 2026 avaldatud blogiseeria dokumentide-põhiste tehisintellektisüsteemide loomise kohta, kasutades RAG-meetodit, Azure AI teenuseid, avatud lähtekoodi alternatiive ja hindamisele suunatud töövooge.

## Taust

Aastal 2023 töötasin kahe õpetuse kallal, kuidas õpetada ChatGPT-d vastama küsimustele PDF-dokumentidest, kasutades Azure AI otsingut ja Azure OpenAI-d. Mõiste "ChatGPT sinu andmete peal" tundus tol ajal veel uus ja eesmärk oli näidata praktilist töövoogu: salvestada dokumendid, indekseerida need, pärida sobivat sisu ja genereerida vastused päritud kontekstist.

Aastal 2026 on RAG-ökosüsteem palju suurem. Azure AI Search toetab kaasaegseid vektor- ja hübriidpäringute mustreid, Azure OpenAI on osa Microsoft Foundry mudelite laiemast ökosüsteemist ning avatud lähtekoodi tööriistad nagu LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ja vLLM on saanud reaalsete süsteemide jaoks praktilisteks valikuteks.

Seetõttu tahtsin seda teemat uuesti käsitleda. Küsimus ei ole enam ainult "Kuidas ma ehitan RAG-i?" Nüüd on palju erinevaid viise selle ülesehitamiseks ning olulisem küsimus on „Millise arhitektuuri peaksin oma olukorras valima?“

See seeria algab sellest otsustamise kihist. Enne sügavale realiseerimisse minemist vaatleb see, miks AI teenused vajavad päringuid, millal mõistlik on valida Azure-i hallatavad teenused, millal sobivad paremini avatud lähtekoodi alternatiivid ja kuhu jääb peenhäälestus.

## Artiklid

1. [Seeria 1: RAG, Azure vs avatud lähtekoodi alternatiivid ja millal peenhäälestus on mõistlik](./series-1-rag-azure-open-source-fine-tuning.md)

## Mitmekeelne tugi

### Toetatud Co-op tõlkega (automaatne ja alati ajakohane)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Araabia](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgaaria](../bg/README.md) | [Burma (Myanmar)](../my/README.md) | [Hiina (lihtsustatud)](../zh-CN/README.md) | [Hiina (traditsiooniline, Hongkong)](../zh-HK/README.md) | [Hiina (traditsiooniline, Macau)](../zh-MO/README.md) | [Hiina (traditsiooniline, Taiwan)](../zh-TW/README.md) | [Horvaadi](../hr/README.md) | [Tšehhi](../cs/README.md) | [Taani](../da/README.md) | [Hollandi](../nl/README.md) | [Eesti](./README.md) | [Soome](../fi/README.md) | [Prantsuse](../fr/README.md) | [Saksa](../de/README.md) | [Kreeka](../el/README.md) | [Heebrea](../he/README.md) | [Hindi](../hi/README.md) | [Ungari](../hu/README.md) | [Indoneesia](../id/README.md) | [Itaalia](../it/README.md) | [Jaapani](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korea](../ko/README.md) | [Leedu](../lt/README.md) | [Malai](../ms/README.md) | [Malajalami](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigeeria pidgin](../pcm/README.md) | [Norra](../no/README.md) | [Pärsia (Farsi)](../fa/README.md) | [Poola](../pl/README.md) | [Portugali (Brasiilia)](../pt-BR/README.md) | [Portugali (Portugal)](../pt-PT/README.md) | [Pandžabi (Gurmukhi)](../pa/README.md) | [Rumeenia](../ro/README.md) | [Vene](../ru/README.md) | [Serbia (kirilitsa)](../sr/README.md) | [Slovaki](../sk/README.md) | [Sloveeni](../sl/README.md) | [Hispaania](../es/README.md) | [Suaheli](../sw/README.md) | [Rootsi](../sv/README.md) | [Tagalogi (filipino)](../tl/README.md) | [Tamili](../ta/README.md) | [Telugu](../te/README.md) | [Tai](../th/README.md) | [Türgi](../tr/README.md) | [Ukraina](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnami](../vi/README.md)

> **Eelistad kloonida lokaalselt?**
>
> See hoidla sisaldab üle 50 keele tõlkeid, mis suurendab märkimisväärselt allalaadimise mahku. Kui soovid kloonida ilma tõlketeta, kasuta sporadiseeritud kojutõmbamist:
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
> See annab sulle kogu vajaliku aine kursuse läbimiseks palju kiirema allalaadimisega.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->