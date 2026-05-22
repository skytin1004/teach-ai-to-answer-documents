# Mokykite AI atsakyti į klausimus pagal jūsų dokumentus

![Dokumentais grindžiamo AI RAG sistemos apžvalga](../../assets/images/readme-hero.svg)

Šis saugyklos puslapis renka 2026 metų tinklaraščio seriją apie dokumentais grindžiamų AI sistemų kūrimą su RAG, Azure AI paslaugomis, atvirojo kodo alternatyvomis ir vertinimu pagrįstais darbo procesais.

## Fonas

2023 metais dirbau su pora mokymų apie tai, kaip išmokyti ChatGPT atsakyti į klausimus iš PDF dokumentų, naudojant Azure AI Search ir Azure OpenAI. Tuomet idėja „ChatGPT jūsų duomenyse“ dar atrodė nauja, o tikslas buvo parodyti praktišką darbo eigą: saugoti dokumentus, indeksuoti juos, gauti susijusį turinį ir generuoti atsakymus iš šio gauto konteksto.

2026 metais RAG ekosistema yra žymiai didesnė. Azure AI Search palaiko šiuolaikinius vektorinius ir hibridinius paieškos modelius, Azure OpenAI yra platesnės Microsoft Foundry Models ekosistemos dalis, o tokie atvirojo kodo įrankiai kaip LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ir vLLM tapo praktiškomis realių sistemų pasirinktimis.

Štai kodėl norėjau dar kartą pažvelgti į šią temą. Dabar klausimas nebėra tik „Kaip sukurti RAG?“ Dabar yra daug būdų tai padaryti, o svarbesnis klausimas – „Kurią architektūrą turėčiau pasirinkti savo situacijai?“

Ši serija prasideda nuo sprendimų sluoksnio ir virsta praktiniais mokymais. Pirmasis įgyvendinimo kelias stato vietinę atvirojo kodo RAG sistemą, kurią bet kas gali paleisti su pavyzdiniais duomenimis, Qdrant, Ollama ir Phi-4-mini.

## Straipsniai

Žiūrėkite [articles/README.md](./articles/README.md) su straipsnių indeksu.

1. [Serija 1: RAG, Azure ir atvirojo kodo alternatyvos, bei kada verta naudoti tikslinį apmokymą](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serija 2: Sukurkite vietinę atvirojo kodo RAG sistemą nuo pradžios iki galo](./articles/series-2-open-source-rag-end-to-end.md)

Kitoje dalyje:

- Iš naujo sukurkite tą pačią RAG sistemą, naudojant Azure AI Search ir Azure OpenAI.
- Pridėkite vertinimą ir regresijos patikrinimus, nepriklausomus nuo demonstracinio atsakymo.

## Užrašų knygelės

Įgyvendinimo straipsniai naudoja užrašų knygeles, kad būtų galima tiesiogiai patikrinti paieškos ir vertinimo žingsnius. Žr. [notebooks/README.md](./notebooks/README.md) katalogo lygmens nurodymus.

> [!TIP]
> Jei norite greičiausio kelio, pradėkite nuo Serijos 2. Ji veikia vietoje su pavyzdiniais duomenimis, procesoriui draugiškomis įdėtimis, Qdrant vietiniu režimu ir be debesijos prisijungimo duomenų.

| Serija | Užrašų knygelė | Reikalavimai | Vietinė patikra |
| --- | --- | --- | --- |
| Serija 2 | [Atvirojo kodo RAG užrašų knygelė](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Patikrintas Qdrant vietinis režimas, paieška, pertvarkymas ir šaltinių sujungimas |

Norėdami paleisti užrašų knygelę vietoje, sukurkite virtualią aplinką ir įdiekite atitinkamą reikalavimų failą. Pavyzdžiui:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Pavyzdiniai duomenys

Užrašų knygelės naudoja mažą vietinį korpusą [sample_data](../../sample_data), kad pavyzdžiai galėtų veikti be privačių dokumentų ar debesijos prisijungimų. Daugiau informacijos žr. [sample_data/README.md](./sample_data/README.md).

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Vietinės patikros santrauka

Patikros rezultatai fiksuojami kiekviename straipsnyje ir faile [SERIES_PLAN.md](./SERIES_PLAN.md).

| Sritis | Rezultatas |
| --- | --- |
| Atvirojo kodo kelias Serija 2 | FastEmbed sugeneravo 384 matmenų vietines įdėtis, Qdrant atminties rinkinio metu įdėjo 8 vektorius, lengvas pertvarkymas grąžino numatytą skyrių; neprivaloma Ollama generacija užbaigta su `phi4-mini:3.8b` |

Vietinė užrašų knygelė tyčia vengia kietai įkoduotų paslapčių.

## Vietinė Ollama generacija

Serijos 2 užrašų knygelė pagal numatytuosius nustatymus yra saugi vietoje. Norėdami įjungti vietinę Ollama generaciją, nukopijuokite [.env.example](../../.env.example) į `.env` ir užpildykite Serijos 2 reikšmes.

Serijos 2 Ollama generacijai atkomentuokite:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Serijos 2 užrašų knygelė automatiškai įkelia `.env` iš saugyklos šaknies naudodama `python-dotenv`.

> [!IMPORTANT]
> Nekelkite `.env` failų, API raktų, privačių galinių taškų ar nuomininko specifinių reikšmių. Ši saugykla tyčia laiko paslaptis už Markdown failų ir užrašų knygelių ribų.

Reikalavimų failai dokumentuoti [requirements/README.md](./requirements/README.md).

Norėdami patikrinti nuorodas, užrašų knygelės struktūrą, užrašų knygelės išvesties švarumą ir didelės rizikos paslapčių šablonus:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Patikros scenarijai dokumentuoti [scripts/README.md](./scripts/README.md).

Norėdami vykdyti visas vietoje saugias užrašų knygeles toje pačioje aplinkoje:

```powershell
python scripts\verify_notebooks.py --execute
```

Tas pats patikros procesas vyksta GitHub Actions paleidžiant push veiksmus, pull užklausas ir rankinius darbo srauto paleidimus. Juodraščių straipsniai ir užrašų knygelės tyčia neįtraukiamos į viešą patikrų kelią.

Prieš paskelbiant atnaujinimus, naudokite [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Dabartinės nepublikuotos pakeitimų santraukos žr. [CHANGELOG.md](./CHANGELOG.md).

Prisidėjimo ir užrašų knygelių higienos gairės pateikiamos faile [CONTRIBUTING.md](./CONTRIBUTING.md).

## Daugiakalbystės palaikymas

### Palaikoma naudojant Co-op Translator (automatiškai ir visada atnaujinta)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](./README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Norite klonuoti vietoje?**
>
> Ši saugykla apima daugiau nei 50 kalbų vertimus, kas žymiai padidina atsisiuntimo apimtį. Norėdami klonuoti be vertimų, naudokite sparse checkout:
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
> Tai suteikia viską, ko reikia kursui užbaigti, su žymiai greitesniu atsisiuntimu.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->