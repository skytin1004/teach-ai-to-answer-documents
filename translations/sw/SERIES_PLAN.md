# Fundisha AI Kujibu Maswali Kulingana na Nyaraka Zako - Mpango wa Mfululizo

Mpango huu unafuatilia toleo la umma la Mfululizo 1 na Mfululizo 2. Baadaye kazi za Azure na tathmini zinahifadhiwa kama rasimu hadi mifano iwe kamili kabisa na kuthibitishwa.

Usifanye commit au push ya mabadiliko hadi utolewe maelekezo wazi.

## Uwanja wa Umma

Toleo la sasa la umma:

- Makala ya Mfululizo 1: maamuzi ya usanifu wa RAG, manufaa na hasara ya Azure dhidi ya chanzo huria, na wapi fine-tuning inaendana.
- Makala ya Mfululizo 2: mafunzo ya RAG ya chanzo huria cha eneo la karibu.
- Notebook la Mfululizo 2: maabara ya RAG ya eneo la karibu inayoweza kutekelezwa na FastEmbed, Qdrant, Ollama, na Phi-4-mini.
- Sampuli ya data: sera za shule na faili za maelekezo ya AI ya kozi kwa Markdown.

Imeandaliwa lakini bado haijaingizwa kwenye faharasa ya umma:

- Ujenzi upya wa Azure AI Search na Azure OpenAI.
- Tathmini ya RAG na ukaguzi wa regression.

## Hali ya Mafunzo

Hali iliyoshirikiwa ni msaidizi wa sera za shule.

Msaidizi hujibu swali hili kutoka kwa nyaraka za eneo la karibu:

```text
Can I use generative AI for my final assignment?
```

Tabia inayotarajiwa ni:

1. Pakua nyaraka za Markdown za eneo la karibu.
2. Tafsiri na gawanya kwa vichwa vya habari.
3. Tengeneza embeddings za eneo la karibu na hifadhi taswira zinazoweza kutafutwa pamoja na metadata.
4. Rudisha sehemu husika ya sera.
5. Panga upya mara inapohitajika.
6. Tengeneza au tengeneza jibu lenye msingi.
7. Rejesha marejeleo.
8. Rekodi matokeo ya uthibitishaji.

## Muundo wa Sasa wa Umma

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```

Vifaa vya rasimu vinahifadhiwa chini ya `drafts/` na vinapita bila kuangaliwa na ukaguzi wa hazina hadi viwe tayari kwa faharasa ya umma.

## Uthibitishaji wa Mfululizo 2

Imethibitishwa kwenye Windows kwa kutumia Python 3.12.6.

- `requirements/open-source-rag.txt` imewekwa kwa mafanikio.
- `notebooks/series-2-open-source-rag.ipynb` ilitekelezwa kwa kutumia `nbclient`.
- Uthibitishaji wa eneo la karibu ulifanikisha: nyaraka 2 za sampuli zilipakuliwa, vipande 8 vilianzishwa, FastEmbed ilizalisha embeddings za eneo la karibu zenye vipimo 384, mkusanyiko wa kumbukumbu wa Qdrant ulianzishwa, na vector 8 ziliingizwa.
- Swali la majaribio: "Nawezaje kutumia AI ya kizazi kwa kazi yangu ya mwisho?"
- Chanzo kilichorejeshwa cha juu baada ya upangaji mwepesi: `school_ai_policy.md`.
- Sehemu iliyoangaliwa ya juu baada ya upangaji mwepesi: `Final Assignments`.
- Njia ya jibu ya chaguo-msingi: mchanganyiko wa jibu la uwazi la eneo la karibu.
- Ollama iliyoanzishwa kupitia winget; `phi4-mini:3.8b` ilipakuliwa kwa mafanikio.
- Njia ya uundaji jibu ya Ollama: imekamilika kwa `phi4-mini:3.8b`.
- Ukubwa wa faili ya mfano wa Ollama: takriban 2.49GB kwenye diski.
- Ukubwa wa mfano uliopakiwa wa Ollama: 3.3GB ulioripotiwa na `ollama ps`.
- Ugawaji wa GPU: 100% ya GPU ikiripotiwa na `ollama ps` kwenye RTX 3060 Laptop GPU.
- Kumbukumbu ya GPU iliyoonekana baada ya uundaji: takriban 3.5GB kati ya 6GB.
- Utekelezaji wa notebook uliopitia na modeli ya FastEmbed iliyohifadhiwa pamoja na uanzishaji wa Ollama ulipita kwa takriban sekunde 34 kupitia script ya uthibitishaji.
- Uchunguzi: mzunguko wa awali wa kupakua nyaraka ulijumuisha `sample_data/README.md` kwa bahati mbaya; notebook sasa inapakua nyaraka mbili za sampuli zilizokusudiwa moja kwa moja.

## Uthibitishaji wa Hazina

- `scripts/verify_notebooks.py` inathibitisha viungo vya Markdown vya eneo la karibu, JSON ya notebook, usafi wa matokeo ya notebook, na mifumo ya siri yenye hatari kubwa.
- `scripts/verify_notebooks.py --execute` inatekeleza notebooks za umma kutoka kwenye mizizi ya hazina.
- Vifaa vya rasimu chini ya `drafts/` hupitwa kwa makusudi.

## Kazi Inayofuata

- Jenga tena hali ile ile na Azure AI Search na Azure OpenAI kama sehemu ya mfululizo wa baadaye.
- Ongeza utafutaji na tathmini ya jibu mara utekelezaji wa eneo la karibu na Azure utakapokuwa thabiti.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->