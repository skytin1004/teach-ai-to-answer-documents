# Mokykite DI atsakyti į klausimus remiantis jūsų dokumentais – serijos planas

Šis planas stebi viešąją Serijos 1 ir Serijos 2 versijas. Vėlesni darbai su Azure ir vertinimu laikomi juodraščiais, kol pavyzdžiai bus visiškai galu iki galo patikrinti.

Nesiųskite jokių pakeitimų, kol jums aiškiai nebus nurodyta.

## Viešasis aprėptis

Dabartinė viešoji versija:

- Serija 1 straipsnis: RAG architektūros sprendimai, Azure ir atvirojo kodo kompromisai bei kur tinkamas smulkus reguliavimas.
- Serija 2 straipsnis: vietinis atvirojo kodo RAG mokymas.
- Serija 2 užrašinė: paleidžiamas vietinis RAG laboratorijos darbas su FastEmbed, Qdrant, Ollama ir Phi-4-mini.
- Pavyzdiniai duomenys: mokyklos politika ir kursų AI gairių Markdown failai.

Parengta, bet dar neindeksuota viešai:

- Azure AI Search ir Azure OpenAI pertvarkymas.
- RAG vertinimas ir regresijos patikros.

## Mokymo scenarijus

Bendrinamas scenarijus yra mokyklos politikos asistentas.

Asistentas atsako į šį klausimą iš vietinių dokumentų:

```text
Can I use generative AI for my final assignment?
```

Tikėtinas elgesys yra:

1. Užkrauti vietinius Markdown dokumentus.
2. Išanalizuoti ir suskirstyti juos pagal antraštes.
3. Sukurti vietinius įterpimus ir išsaugoti paieškai tinkamas reprezentacijas su metaduomenimis.
4. Gauti atitinkamą politinės dalies fragmentą.
5. Jeigu reikia, atlikti iš naujo patikrinimą (rerank).
6. Generuoti arba sukurti pagrįstą atsakymą.
7. Grąžinti citatas.
8. Užrašyti patikros rezultatus.

## Dabartinė viešoji struktūra

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

Juodraščių medžiaga saugoma `drafts/` kataloge ir yra praleidžiama repozitorijos patikroje, kol nėra paruošta viešajam indeksavimui.

## Serijos 2 patikra

Patikrinta Windows aplinkoje su Python 3.12.6.

- Sėkmingai įdiegtas `requirements/open-source-rag.txt`.
- Vykdyta `notebooks/series-2-open-source-rag.ipynb` su `nbclient`.
- Vietinė patikra sėkminga: užkrauti 2 pavyzdiniai dokumentai, sukurta 8 dalių, FastEmbed sugeneravo 384 dimensijų vietinius įterpimus, inicijuota Qdrant atminties kolekcija, įdėta 8 vektoriai.
- Testo klausimas: „Ar galiu naudoti generatyvinį DI savo baigiamajam darbui?“
- Geriausiai pasirinktas šaltinis po lengvo perrikiavimo: `school_ai_policy.md`.
- Geriausiai pasirinkta dalis po lengvo perrikiavimo: `Final Assignments`.
- Numatytoji atsakymo kryptis: vietinis skaidrus atsakymų komponuotojas.
- Ollama įdiegta per winget; sėkmingai parsisiųsta `phi4-mini:3.8b`.
- Ollama atsakymų generavimo kelias: užbaigtas su `phi4-mini:3.8b`.
- Ollama modelio failo dydis: apie 2.49 GB diske.
- Ollama užkrauto modelio dydis: apie 3.3 GB, pranešta per `ollama ps`.
- GPU atjungimas: 100 % GPU, pranešta per `ollama ps` RTX 3060 Laptop GPU.
- GPU atminties naudojimas po generavimo: apie 3.5 GB iš 6 GB.
- Užrašinės vykdymas su talpykloje laikomu FastEmbed modeliu ir įjungtu Ollama generavimu praėjo apie 34 sekundes per patikros skriptą.
- Pastebėjimas: ankstyvas dokumentų užkrovimo procesas netyčia įtraukė `sample_data/README.md`; dabar užrašinė aiškiai užkrauna tik du numatytus pavyzdinius dokumentus.

## Repozitorijos patikra

- `scripts/verify_notebooks.py` tikrina vietinius Markdown saitų veikimą, užrašinių JSON struktūrą, išvalytą užrašinių išvestį ir didelės rizikos slaptumo modelius.
- `scripts/verify_notebooks.py --execute` paleidžia viešąsias užrašines iš repozitorijos šaknies.
- Juodraščių medžiaga `drafts/` kataloge sąmoningai praleidžiama.

## Tolimesni darbai

- Pertvarkyti tą pačią scenarijų su Azure AI Search ir Azure OpenAI ateities serijos dalyje.
- Pridėti paieškos ir atsakymų vertinimą, kai vietinė ir Azure įgyvendinimai abiejose bus stabilūs.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->