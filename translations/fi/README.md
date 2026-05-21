# Opeta tekoälyä vastaamaan kysymyksiin dokumenttiesi perusteella

Tämä arkisto kokoaa vuoden 2026 blogisarjan dokumenttipohjaisten tekoälyjärjestelmien rakentamisesta RAG:n, Azure AI -palveluiden, avoimen lähdekoodin vaihtoehtojen ja arviointikeskeisten työnkulkujen avulla.

## Tausta

Vuonna 2023 tein pari opetusohjelmaa ChatGPT:n opettamisesta vastaamaan PDF-dokumenttien kysymyksiin käyttäen Azure AI Searchia ja Azure OpenAI:ta. Ajatus "ChatGPT omien tietojesi päällä" tuntui silloin vielä uudelta, ja tavoitteena oli esitellä käytännön työnkulku: tallentaa dokumentit, indeksoida ne, hakea relevantti sisältö ja luoda vastauksia haetun kontekstin pohjalta.

Vuonna 2026 RAG-ekosysteemi on paljon laajempi. Azure AI Search tukee moderneja vektori- ja hybridihausta, Azure OpenAI on osa laajempaa Microsoft Foundry Models -ekosysteemiä, ja avoimen lähdekoodin työkalut kuten LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ja vLLM ovat käytännöllisiä vaihtoehtoja oikeisiin järjestelmiin.

Siksi halusin palata tähän aiheeseen. Kysymys ei enää ole vain "Miten rakennan RAG:n?" Nyt on monia tapoja rakentaa sitä, ja tärkeämpi kysymys on "Minkä arkkitehtuurin valitsen omaan tilanteeseeni?"

Tämä sarja alkaa tästä päätöksentekokerroksesta. Ennen syventymistä toteutukseen tarkastellaan, miksi tekoälypalvelut tarvitsevat haun, milloin Azure-pohjaiset hallinnoidut palvelut ovat järkeviä, milloin avoimen lähdekoodin vaihtoehdot sopivat paremmin ja missä vaiheessa hienosäätö sopii.

## Artikkelit

1. [Sarja 1: RAG, Azure vs avoimen lähdekoodin vaihtoehdot ja milloin hienosäätö on järkevää](./series-1-rag-azure-open-source-fine-tuning.md)

## Monikielinen tuki

### Tuettu Co-op Translatorin kautta (automaattinen ja aina ajan tasalla)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](./README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Haluatko mieluummin kloonata paikallisesti?**
>
> Tämä arkisto sisältää yli 50 kielivaihtoehtoa, mikä kasvattaa merkittävästi lataustiedostojen kokoa. Jos haluat kloonata ilman käännöksiä, käytä sparse checkout -toimintoa:
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
> Tämä antaa sinulle kaiken tarvittavan kurssin suorittamiseen paljon nopeammalla latauksella.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->