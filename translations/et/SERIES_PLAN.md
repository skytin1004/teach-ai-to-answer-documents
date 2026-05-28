# Õpeta tehisintellekt vastama küsimustele sinu dokumentide põhjal - sarja plaan

See plaan jälgib avalikku Series 1 ja Series 2 väljaannet. Hilisem Azure ja hindamistöö hoitakse mustanditena, kuni näited on täielikult lõpuni viidud ja kinnitatud.

Ära tee muudatusi ega ühenda neid enne, kui on selgesõnaliselt juhitud.

## Avalik ulatus

Praegune avalik väljaanne:

- Series 1 artikkel: RAG arhitektuuri otsused, Azure ja avatud lähtekoodiga kompromissid ning kohandamise koht.
- Series 2 artikkel: kohalik avatud lähtekoodiga RAG juhis.
- Series 2 märkmik: käivitatav kohalik RAG labor FastEmbedi, Qdranti, Ollama ja Phi-4-mini abil.
- Näited andmetest: koolipoliitika ja kursuse tehisintellekti juhendi Markdown-failid.

Mustandina, kuid veel avalikus indeksis mitte:

- Azure AI Search ja Azure OpenAI ümberehitus.
- RAG hindamine ja regressioonikontrollid.

## Juhendi stsenaarium

Jagatud stsenaarium on koolipoliitika assistent.

Assistent vastab sellele küsimusele kohalikest dokumentidest:

```text
Can I use generative AI for my final assignment?
```

Oodatav käitumine on:

1. Laadida kohalikud Markdown dokumendid.
2. Analüüsida ja jagada need pealkirjade kaupa osadeks.
3. Luua kohalikud embedid ja salvestada otsitavad esindused koos metaandmetega.
4. Leida asjakohane poliitikasection.
5. Vajadusel ümberjärjestada.
6. Luua või koostada põhjendatud vastus.
7. Tagastada viited.
8. Salvestada kinnitustulemused.

## Praegune avalik struktuur

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

Mustandmaterjal on salvestatud kausta `drafts/` ja repositooriumi kontroll seda ignoreerib, kuni see on valmis avalikuks indeksimiseks.

## Series 2 kinnitamine

Kinnituse tehtud Windowsil Python 3.12.6-ga.

- Edukalt paigaldatud `requirements/open-source-rag.txt`.
- Käivitatud `notebooks/series-2-open-source-rag.ipynb` `nbclient` abil.
- Kohalik kontroll läbitud: laaditud 2 näitedokumenti, loodud 8 tükki, FastEmbed genereeris 384-mõõtmelised kohalikud embedid, Qdrant in-memory kogu initsialiseeritud ning sisestatud 8 vektorit.
- Testküsimus: "Kas ma võin kasutada generatiivset tehisintellekti oma lõputöö jaoks?"
- Parim allikas pärast kerget ümberjärjestamist: `school_ai_policy.md`.
- Parim jaotis pärast kerget ümberjärjestamist: `Lõputööd`.
- Vaikimisi vastamise rada: kohalik läbipaistev vastuste koostaja.
- Ollama paigaldatud wingeti kaudu; `phi4-mini:3.8b` edukalt tõmmatud.
- Ollama vastuste genereerimise rada: lõpetatud `phi4-mini:3.8b` mudeliga.
- Ollama mudelifaili suurus: umbes 2.49GB kettal.
- Ollamas laaditud mudeli suurus: 3.3GB, teatatud `ollama ps` poolt.
- GPU koormus: 100% GPU `ollama ps` andmetel RTX 3060 sülearvuti GPU-l.
- GPU mälu kasutus pärast genereerimist: umbes 3.5GB 6GB-st.
- Märkmiku käitamine vahemällu salvestatud FastEmbed mudeli ja Ollama genereerimisega läbis kinnitusskripti umbes 34 sekundiga.
- Täheldus: varajane dokumendi laadimise käik sisaldas ekslikult `sample_data/README.md`; nüüd laadib märkmik ekspliciitselt ainult kaks mõeldud näitedokumentu.

## Repositooriumi kinnitamine

- `scripts/verify_notebooks.py` kontrollib kohalikke Markdown linke, märkmiku JSON-i, märkmiku väljundi puhtust ja kõrge riski saladusmustreid.
- `scripts/verify_notebooks.py --execute` käivitab avalikke märkmikke repositooriumi juurkataloogist.
- Mustandmaterjali kausta `drafts/` on teadlikult vahele jäetud.

## Järgmine töö

- Ehita sama stsenaarium uuesti Azure AI Searchi ja Azure OpenAI-ga tulevase sarja osana.
- Lisa taaste ja vastuste hindamine, kui nii kohalik kui ka Azure rakendused on stabiilsed.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->