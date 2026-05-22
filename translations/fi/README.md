# Opeta tekoäly vastaamaan kysymyksiin asiakirjojesi perusteella

![Dokumenttipohjaisen tekoälyn RAG-järjestelmän yleiskatsaus](../../assets/images/readme-hero.svg)

Tämä repositorio kokoaa vuoden 2026 blogisarjan asiakirjapohjaisten tekoälyjärjestelmien rakentamisesta RAG:n, Azure AI -palveluiden, avoimen lähdekoodin vaihtoehtojen ja arviointikeskeisten työnkulkujen avulla.

## Taustaa

Vuonna 2023 työskentelin parin opetusohjelman parissa, joissa opetettiin ChatGPT:tä vastaamaan PDF-asiakirjoista löytyviin kysymyksiin Azure AI Searchin ja Azure OpenAI:n avulla. Ajatus "ChatGPT omien tietojesi päälle" tuntui vielä tuolloin uudelta, ja tavoitteena oli näyttää käytännön työnkulku: tallentaa asiakirjat, indeksoida ne, hakea relevanttia sisältöä ja luoda vastauksia haetun kontekstin perusteella.

Vuonna 2026 RAG-ekosysteemi on paljon laajempi. Azure AI Search tukee moderneja vektori- ja hybridihakumalleja, Azure OpenAI on osa laajempaa Microsoft Foundry Models -ekosysteemiä, ja avoimen lähdekoodin työkalut kuten LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ja vLLM ovat muodostuneet käytännöllisiksi valinnoiksi oikeisiin järjestelmiin.

Siksi halusin palata aiheen pariin. Kysymys ei enää ole pelkästään "Miten rakennan RAG:n?" Nyt tapoja on monia, ja tärkeämpi kysymys on "Minkä arkkitehtuurin valitsen omaan tilanteeseeni?"

Tämä sarja alkaa siitä päätöksentekotasosta ja kääntää sen sitten käytännön opetusohjelmiksi. Ensimmäinen toteutusreitti rakentaa paikallinen avoimen lähdekoodin RAG-järjestelmä, jota kuka tahansa voi käyttää esimerkkidataan, Qdranttiin, Ollamaan ja Phi-4-mini -malliin perustuen.

## Artikkelit

Katso artikkeliluettelo kohdasta [articles/README.md](./articles/README.md).

1. [Sarja 1: RAG, Azure vs avoimen lähdekoodin vaihtoehdot ja milloin hienosäätö kannattaa](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Sarja 2: Rakenna paikallinen avoimen lähdekoodin RAG-järjestelmä päästä päähän](./articles/series-2-open-source-rag-end-to-end.md)

Tulossa seuraavaksi:

- Rakenna sama RAG-järjestelmä uudelleen Azure AI Searchilla ja Azure OpenAI:lla.
- Lisää arviointi- ja regressiotarkastukset demovastauksen lisäksi.

## Muistikirjat

Toteutusartikkelit käyttävät muistikirjoja, jotta haun ja arvioinnin vaiheet voidaan tarkastaa suoraan. Katso kansiokohtaiset ohjeet tiedostosta [notebooks/README.md](./notebooks/README.md).

> [!TIP]
> Aloita sarjasta 2, jos haluat nopeimman polun. Se toimii paikallisesti esimerkkidatalla, suorituskykyisillä upotuksilla CPU:lle, Qdrantin paikallismoodilla eikä vaadi pilvitunnuksia.

| Sarja | Muistikirja | Vaatimukset | Paikallinen varmistus |
| --- | --- | --- | --- |
| Sarja 2 | [Avoimen lähdekoodin RAG-muistikirja](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrantin paikallismoodi, haku, uudelleenjärjestely ja lähteiden yhdistely vahvistettu |

Suorittaaksesi muistikirjan paikallisesti, luo virtuaaliympäristö ja asenna vastaava vaatimustiedosto. Esimerkiksi:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Esimerkkidata

Muistikirjat käyttävät pientä paikallista kokoelmaa kansiossa [sample_data](../../sample_data), jotta esimerkit toimivat ilman yksityisiä asiakirjoja tai pilvitunnuksia. Katso lisätietoja tiedostosta [sample_data/README.md](./sample_data/README.md).

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Paikallisen varmistuksen yhteenveto

Varmistusraportit löytyvät jokaisesta artikkelista ja tiedostosta [SERIES_PLAN.md](./SERIES_PLAN.md).

| Alue | Tulos |
| --- | --- |
| Sarja 2 avoimen lähdekoodin reitti | FastEmbed loi 384-ulotteiset paikalliset upotukset, Qdrantissa muistissa tietokokoelma lisäsi 8 vektoria, kevyt uudelleenjärjestely palautti odotetun osion; valinnainen Ollama-generointi suoritettu mallilla `phi4-mini:3.8b` |

Paikallinen muistikirja jättää tahallisesti kovakoodatut salaisuudet pois.

## Paikallinen Ollama-generointi

Sarjan 2 muistikirja on oletuksena turvallinen paikallisessa käytössä. Ota paikallinen Ollama-generointi käyttöön kopioimalla [.env.example](../../.env.example) tiedostoksi `.env` ja täyttämällä sarjan 2 arvot.

Sarjan 2 Ollama-generoinnissa poista kommenttimerkki riviltä:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Sarjan 2 muistikirja lataa automaattisesti `.env`-tiedoston repositorion juuresta `python-dotenv`-kirjaston avulla.

> [!IMPORTANT]
> Älä tallenna `.env`-tiedostoja, API-avaimia, yksityisiä päätepisteitä tai vuokralaiskohtaisia arvoja versionhallintaan. Repositorio pitää salaisuudet tahallisesti poissa Markdown-tiedostoista ja muistikirjoista.

Vaatimustiedostot on dokumentoitu tiedostossa [requirements/README.md](./requirements/README.md).

Linkkien, muistikirjan rakenteen, tuloksen siisteyden ja korkean riskin salaisuuskäytäntöjen tarkistamiseksi:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Varmistuskomentosarjat on dokumentoitu tiedostossa [scripts/README.md](./scripts/README.md).

Suorittaaksesi kaikki paikallisesti turvalliset muistikirjat samassa ympäristössä:

```powershell
python scripts\verify_notebooks.py --execute
```

Sama varmistusprosessi pyörii GitHub Actionsissa puskuissa, vetopyynnöissä ja manuaalisissa työnkulkuajoksissa. Luonnosartikkelit ja muistikirjat on tahallisesti pois julkisesta varmistepolusta.

Ennen päivittämistä käytä [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Katso nykyinen julkaisematon muutosyhteenveto tiedostosta [CHANGELOG.md](./CHANGELOG.md).

Lisäys- ja muistikirjahygieniaohjeet löytyvät tiedostosta [CONTRIBUTING.md](./CONTRIBUTING.md).

## Monikielinen tuki

### Tuettu Co-op Translatorin kautta (automaattinen ja aina ajan tasalla)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabia](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgaria](../bg/README.md) | [Burma (Myanmar)](../my/README.md) | [Kiina (yksinkertaistettu)](../zh-CN/README.md) | [Kiina (perinteinen, Hongkong)](../zh-HK/README.md) | [Kiina (perinteinen, Macao)](../zh-MO/README.md) | [Kiina (perinteinen, Taiwan)](../zh-TW/README.md) | [Kroatia](../hr/README.md) | [Tsekki](../cs/README.md) | [Tanska](../da/README.md) | [Hollanti](../nl/README.md) | [Viro](../et/README.md) | [Suomi](./README.md) | [Ranska](../fr/README.md) | [Saksa](../de/README.md) | [Kreikka](../el/README.md) | [Heprea](../he/README.md) | [Hindi](../hi/README.md) | [Unkari](../hu/README.md) | [Indonesia](../id/README.md) | [Italia](../it/README.md) | [Japani](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korea](../ko/README.md) | [Liettua](../lt/README.md) | [Malaiji](../ms/README.md) | [Malajalami](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norja](../no/README.md) | [Persia (Farsi)](../fa/README.md) | [Puola](../pl/README.md) | [Portugali (Brasilia)](../pt-BR/README.md) | [Portugali (Portugali)](../pt-PT/README.md) | [Pandžabi (Gurmukhi)](../pa/README.md) | [Romania](../ro/README.md) | [Venäjä](../ru/README.md) | [Serbia (kyrillinen)](../sr/README.md) | [Slovakki](../sk/README.md) | [Sloveeni](../sl/README.md) | [Espanja](../es/README.md) | [Swahili](../sw/README.md) | [Ruotsi](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamili](../ta/README.md) | [Telugu](../te/README.md) | [Thaimaa](../th/README.md) | [Turkki](../tr/README.md) | [Ukraina](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnam](../vi/README.md)

> **Haluatko mieluummin kloonata paikallisesti?**
>
> Tämä repositorio sisältää yli 50 kielikäännöstä, jotka nostavat latauskoon merkittävästi. Jos haluat kloonata ilman käännöksiä, käytä sparse checkout -toimintoa:
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
> Tämä antaa sinulle kaiken tarvittavan kurssin suorittamiseen nopeamman latauksen kera.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->