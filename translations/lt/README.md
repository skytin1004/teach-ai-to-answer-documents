# Išmokykite AI atsakyti į klausimus remiantis jūsų dokumentais

Ši saugykla renka 2026 metų tinklaraščio seriją apie dokumentais grindžiamų AI sistemų kūrimą su RAG, Azure AI paslaugomis, atvirojo kodo alternatyvomis ir įvertinimu orientuotais darbo srautais.

## Fonas

2023 metais dirbau prie poros pamokų, kaip išmokyti ChatGPT atsakyti į klausimus iš PDF dokumentų naudojant Azure AI Search ir Azure OpenAI. Tada „ChatGPT pagal jūsų duomenis“ idėja dar atrodė nauja, o tikslas buvo parodyti praktišką darbo eigą: saugoti dokumentus, indeksuoti juos, gauti susijusį turinį ir generuoti atsakymus iš to turinio.

2026 metais RAG ekosistemos apimtis gerokai išsiplėtė. Azure AI Search palaiko modernius vektorių ir hibridinius paieškos modelius, Azure OpenAI yra didesnės Microsoft Foundry Modelių ekosistemos dalis, o atvirojo kodo įrankiai, tokie kaip LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ir vLLM tapo praktiškais pasirinkimais realioms sistemoms.

Todėl norėjau dar kartą peržiūrėti šią temą. Klausimas dabar ne tik „Kaip sukurti RAG?“ – jau yra daug būdų tai padaryti, o svarbesnis klausimas yra „Kurią architektūrą pasirinkti mano atveju?“

Ši serija prasideda nuo sprendimų priėmimo lygmens. Prieš gilų įgyvendinimą, ji nagrinėja, kodėl AI paslaugoms reikalinga paieška, kada prasminga naudotis Azure valdomomis paslaugomis, kada geriau tinka atvirojo kodo alternatyvos ir kur tinka papildomas mokymas.

## Straipsniai

1. [Serija 1: RAG, Azure vs Atvirojo Kodo Alternatyvos ir Kada Tikslingas Papildomas Mokymas](./series-1-rag-azure-open-source-fine-tuning.md)

## Daugiakalbė Pagalba

### Palaikoma per Co-op Translator (Automatizuota ir Visada Naujausia)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](./README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Norite Klonuoti Vietoje?**
>
> Ši saugykla apima daugiau nei 50 kalbų vertimus, kurie reikšmingai padidina parsisiuntimo dydį. Norėdami klonuoti be vertimų, naudokite sparsų atsisiuntimą:
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
> Tai suteikia jums viską, ko reikia kursui įvykdyti, žymiai greitesniu atsisiuntimu.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->