# Fundisha AI Kujibu Maswali Kulingana na Nyaraka Zako

![Muhtasari wa mfumo wa AI RAG unaotegemea nyaraka](../../assets/images/readme-hero.svg)

Hifadhidata hii inakusanya mfululizo wa blogu wa 2026 kuhusu kujenga mifumo ya AI inayotegemea nyaraka kwa kutumia RAG, huduma za Azure AI, mbadala za chanzo wazi, na mitiririko ya kazi inayolenga tathmini.

## Historia

Mnamo 2023, nilifanya kazi kwenye mafunzo mawili kuhusu kufundisha ChatGPT kujibu maswali kutoka kwa nyaraka za PDF kwa kutumia Azure AI Search na Azure OpenAI. Wazo la "ChatGPT kwenye data yako" bado lilihisi jipya wakati huo, na lengo lilikuwa kuonyesha mtiririko wa kazi wa vitendo: kuhifadhi nyaraka, kuzifungua kwenye index, kupata maudhui yanayohusiana, na kuunda majibu kutoka kwa muktadha huo uliopatikana.

Mnamo 2026, mfumo wa RAG umechanjuliwa zaidi. Azure AI Search inaunga mkono mifumo ya kisasa ya utoaji wa vector na mchanganyiko, Azure OpenAI ni sehemu ya mfumo mpana wa Microsoft Foundry Models, na zana za chanzo wazi kama LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, na vLLM zimekuwa chaguo za vitendo kwa mifumo halisi.

Ndiyo sababu nilitaka kurudi kwenye mada hii. Suala si tena tu "Jinsi gani ninavyotengeneza RAG?" Sasa kuna njia nyingi za kuijenga, na swali muhimu ni "Nini usanifu ni bora kwa hali yangu?"

Mfululizo huu unaanza kutoka safu ya kutengeneza maamuzi, kisha hubadilika kuwa mafunzo ya vitendo. Njia ya utekelezaji wa kwanza hujenga mfumo wa RAG wa chanzo wazi wa ndani ambao mtu yeyote anaweza kuendesha kwa data ya sampuli, Qdrant, Ollama, na Phi-4-mini.

## Makala

Tazama [articles/README.md](./articles/README.md) kwa orodha ya makala.

1. [Mfululizo 1: RAG, Azure dhidi ya Mbadala za Chanzo Huru, na Wakati Ufanyaji Upya Utafaa](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Mfululizo 2: Tengeneza Mfumo wa RAG wa Chanzo Huru wa Ndani Mwisho kwa Mwisho](./articles/series-2-open-source-rag-end-to-end.md)

Kinakuja hivi karibuni:

- Jenga upya mfumo huo huo wa RAG kwa kutumia Azure AI Search na Azure OpenAI.
- Ongeza upimaji na ukaguzi wa mabadiliko zaidi ya jibu la maonyesho.

## Daftari za Kumbukumbu

Makala za utekelezaji hutumia daftari za kumbukumbu ili hatua za upokezaji na tathmini ziweze kuchunguzwa moja kwa moja. Tazama [notebooks/README.md](./notebooks/README.md) kwa mwongozo wa kiwango cha folda.

> [!TIP]
> Anza na Mfululizo 2 ikiwa unataka njia ya haraka zaidi. Inaendesha ndani ya eneo kwa data ya sampuli, embeddings zinazoweza kuendeshwa kwa CPU, hali ya ndani ya Qdrant, na haidingi nyaraka za wingu.

| Mfululizo | Daftari la Kumbukumbu | Mahitaji | Ukaguzi wa Ndani |
| --- | --- | --- | --- |
| Mfululizo 2 | [Daftari la RAG la Chanzo Huru](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Hali ya ndani ya Qdrant, upokezaji, upangaji upya, na uunganishaji wa chanzo umehakikiwa |

Ili kuendesha daftari la kumbukumbu ndani ya eneo, tengeneza mazingira ya mtandao wa virtual na sakinisha faili za mahitaji zinazolingana. Kwa mfano:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```
  
## Data ya Sampuli

Daftari la kumbukumbu linatumia makusanyo madogo ya ndani kwenye [sample_data](../../sample_data) ili mifano iweze kuendeshwa bila nyaraka binafsi au nyaraka za wingu. Tazama [sample_data/README.md](./sample_data/README.md) kwa maelezo.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Muhtasari wa Ukaguzi wa Ndani

Matokeo ya ukaguzi yameandikwa katika kila makala na katika [SERIES_PLAN.md](./SERIES_PLAN.md).

| Eneo | Matokeo |
| --- | --- |
| Njia ya chanzo huru ya Mfululizo 2 | FastEmbed ilizalisha embeddings za mwelekeo wa vipimo 384, mkusanyiko wa kumbukumbu wa Qdrant ulingiza vectors 8, upangaji upya wa mwepesi ulipatikana sehemu iliyotarajiwa; kizazi cha hiari cha Ollama kilikamilika na `phi4-mini:3.8b` |

Daftari la kumbukumbu la ndani linakusudia kuepuka siri zilizokatwa ndani.

## Kizazi cha Ollama cha Ndani

Daftari la kumbukumbu la Mfululizo 2 ni salama kwa matumizi ya ndani kwa kawaida. Ili kuwezesha kizazi cha Ollama cha ndani, nakili [.env.example](../../.env.example) hadi `.env` na jaza maadili ya Mfululizo 2.

Kwa kizazi cha Ollama cha Mfululizo 2, toa alama ya kuhusisha:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```
  
Daftari la kumbukumbu la Mfululizo 2 lina automatic load ya `.env` kutoka kwenye mizizi ya hifadhidata kwa kutumia `python-dotenv`.

> [!IMPORTANT]
> Usihifadhi faili `.env`, funguo za API, miisho binafsi, au maadili ya mpangilio wa mwenyeji. Hifadhidata hii inakusudia kuweka siri mbali na faili za Markdown na daftari za kumbukumbu.

Faili za mahitaji zimeripotiwa katika [requirements/README.md](./requirements/README.md).

Ili kuthibitisha viungo, muundo wa daftari, usafi wa matokeo ya daftari, na mifumo ya siri hatarishi:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```
  
Vitabu vya ukaguzi vimerkodiwa katika [scripts/README.md](./scripts/README.md).

Ili kuendesha daftari zote za kumbukumbu zilizo salama kwa ndani katika mazingira sawa:

```powershell
python scripts\verify_notebooks.py --execute
```
  
Mtiririko huo wa ukaguzi unafanya kazi pia kwenye GitHub Actions wakati wa push, pull requests, na utendakazi wa mikono. Makala na daftari za kumbukumbu za rasimu hupunguzwa kutoka kwenye njia ya ukaguzi wa umma kwa makusudi.

Kabla ya kuchapisha masasisho, tumia [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Tazama [CHANGELOG.md](./CHANGELOG.md) kwa muhtasari wa mabadiliko yasiyochapishwa ya sasa.

Kwa mwongozo wa michango na usafi wa daftari, tazama [CONTRIBUTING.md](./CONTRIBUTING.md).

## Msaada wa Lugha Nyingi

### Unaungwa mkono kupitia Mtafsiri wa Ushirikiano (Kiotomatiki na Sasa Daima Hali ya Hewa)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Kiarabu](../ar/README.md) | [Kibengali](../bn/README.md) | [Kiblgaria](../bg/README.md) | [Kiburma (Myanmar)](../my/README.md) | [Kichina (Rahisi)](../zh-CN/README.md) | [Kichina (Tamaduni, Hong Kong)](../zh-HK/README.md) | [Kichina (Tamaduni, Macau)](../zh-MO/README.md) | [Kichina (Tamaduni, Taiwan)](../zh-TW/README.md) | [Kroeshia](../hr/README.md) | [Kicheki](../cs/README.md) | [Kidenmaki](../da/README.md) | [Kiholanzi](../nl/README.md) | [Kiestonia](../et/README.md) | [Kifini](../fi/README.md) | [Kifaransa](../fr/README.md) | [Kijerumani](../de/README.md) | [Kigiriki](../el/README.md) | [Kiebrania](../he/README.md) | [Kihindi](../hi/README.md) | [Kihungari](../hu/README.md) | [Kiindonesia](../id/README.md) | [Kiitaliano](../it/README.md) | [Kijapani](../ja/README.md) | [Kikannada](../kn/README.md) | [Kikhemera](../km/README.md) | [Kikorea](../ko/README.md) | [Kilithuania](../lt/README.md) | [Kimalay](../ms/README.md) | [Kimalayalam](../ml/README.md) | [Kimarathi](../mr/README.md) | [Kinepali](../ne/README.md) | [Kipidgin cha Nigeria](../pcm/README.md) | [Kinorwega](../no/README.md) | [Kiajemi (Farsi)](../fa/README.md) | [Kipolandi](../pl/README.md) | [Kireno (Brazil)](../pt-BR/README.md) | [Kireno (Portugal)](../pt-PT/README.md) | [Kipunjabi (Gurmukhi)](../pa/README.md) | [Kiromania](../ro/README.md) | [Kirusi](../ru/README.md) | [Kiserbia (Cyrillic)](../sr/README.md) | [Kislovakia](../sk/README.md) | [Kislovenia](../sl/README.md) | [Kihispania](../es/README.md) | [Kiswahili](./README.md) | [Kiswidi](../sv/README.md) | [Kitagalogi (Kifilipino)](../tl/README.md) | [Kitamili](../ta/README.md) | [Kitelugu](../te/README.md) | [Kithai](../th/README.md) | [Kituruki](../tr/README.md) | [Kiukraini](../uk/README.md) | [Kiurdu](../ur/README.md) | [Kivietinamu](../vi/README.md)

> **Unapendelea Kuleta Nakala Ndani ya Kawaida?**
>
> Hifadhidata hii inajumuisha tafsiri zaidi ya lugha 50 ambayo huongeza ukubwa wa kupakua kwa kiasi kikubwa. Ili kuleta bila tafsiri, tumia sparse checkout:
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
> Hii inakupa kila kitu unachohitaji kukamilisha kozi kwa kupakua kwa kasi zaidi.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->