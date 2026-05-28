# Nauči AI da odgovara na pitanja temeljena na tvojim dokumentima - Plan serijala

Ovaj plan prati javno izdanje Serijala 1 i Serijala 2. Kasniji rad na Azuru i evaluaciji se čuva kao nacrti dok primjeri nisu u potpunosti krajnji i verificirani.

Nemoj raditi commit ili push promjena dok ti to eksplicitno nije naređeno.

## Javni opseg

Trenutno javno izdanje:

- Članak Serijala 1: odabiri arhitekture RAG-a, kompromise Azure vs open-source i gdje se uklapa fino podešavanje.
- Članak Serijala 2: lokalni open-source RAG vodič.
- Bilježnica Serijala 2: pokretljiva lokalna RAG laboratorija s FastEmbed, Qdrant, Ollama i Phi-4-mini.
- Uzorak podataka: pravila škole i smjernice za AI na tečaju u Markdown datotekama.

Nacrti, ali još nisu u javnom indeksu:

- Pregradnja Azure AI Search i Azure OpenAI.
- Evaluacija RAG-a i provjere regresije.

## Scenario vodiča

Podijeljeni scenario je pomoćnik za pravila škole.

Pomoćnik odgovara na ovo pitanje iz lokalnih dokumenata:

```text
Can I use generative AI for my final assignment?
```

Očekivano ponašanje je:

1. Učitati lokalne Markdown dokumente.
2. Parsirati i razdijeliti ih po naslovima.
3. Kreirati lokalne ugnježđenja (embeddings) i spremiti pretražive prikaze s metapodacima.
4. Dohvatiti odgovarajući dio pravila.
5. Ponovno rangirati kad je potrebno.
6. Generirati ili sastaviti utemeljeni odgovor.
7. Vratiti citate.
8. Zabilježiti rezultate verifikacije.

## Trenutna javna struktura

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

Materijal nacrta se sprema pod `drafts/` i preskače se pri verifikaciji repozitorija dok nije spreman za javno indeksiranje.

## Verifikacija Serijala 2

Verificirano na Windows s Python 3.12.6.

- Uspješno instaliran `requirements/open-source-rag.txt`.
- Izvršen `notebooks/series-2-open-source-rag.ipynb` s `nbclient`.
- Lokalna verifikacija prošla: učitana 2 uzorka dokumenata, kreirano 8 dijelova, FastEmbed generirao 384-dimenzionalna lokalna ugnježđenja, Qdrant u memorijskoj kolekciji inicijaliziran i umetnuto 8 vektora.
- Testno pitanje: "Mogu li koristiti generativni AI za svoj završni zadatak?"
- Najbolji dohvaćeni izvor nakon laganog ponovnog rangiranja: `school_ai_policy.md`.
- Najbolje dohvaćeni odlomak nakon laganog ponovnog rangiranja: `Završni zadaci`.
- Zadan put odgovora: lokalni transparentni sastavljač odgovora.
- Ollama instalirana preko winget; `phi4-mini:3.8b` uspješno preuzeta.
- Put generiranja odgovora Ollamom: dovršen s `phi4-mini:3.8b`.
- Veličina Ollama modela na disku: oko 2.49GB.
- Veličina učitanog Ollama modela: 3.3GB prijavljeno s `ollama ps`.
- Odloženo na GPU: 100% GPU prijavljeno s `ollama ps` na RTX 3060 Laptop GPU.
- Memorija GPU-a promatrana nakon generacije: oko 3.5GB od 6GB.
- Izvršenje bilježnice s predmemoriranim FastEmbed modelom i omogućenim Ollama generiranjem prošlo je u oko 34 sekunde kroz verifikacijski skript.
- Promatranje: rana faza učitavanja dokumenata slučajno je uključila `sample_data/README.md`; bilježnica sada eksplicitno učitava samo dva namijenjena uzorna dokumenta.

## Verifikacija repozitorija

- `scripts/verify_notebooks.py` provjerava lokalne Markdown linkove, JSON bilježnice, čišćenje izlaza bilježnice i obrasce visokorizičnih tajni.
- `scripts/verify_notebooks.py --execute` izvršava javne bilježnice iz korijena repozitorija.
- Materijal nacrta pod `drafts/` je namjerno preskočen.

## Sljedeći rad

- Ponovno izgraditi isti scenario s Azure AI Search i Azure OpenAI kao budući dio serijala.
- Dodati dohvat i evaluaciju odgovora kada su lokalne i Azure implementacije obje stabilne.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->