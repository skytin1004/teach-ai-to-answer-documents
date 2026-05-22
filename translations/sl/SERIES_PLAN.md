# Naučite AI odgovarjati na vprašanja na podlagi vaših dokumentov - Načrt serije

Ta načrt spremlja javno izdajo Serije 1 in Serije 2. Kasnejše delo z Azure in evalvacija se hranita kot osnutki, dokler primeri niso popolnoma end-to-end in preverjeni.

Ne pošiljajte ali zapišite sprememb, dokler ni izrecno naročeno.

## Javni obseg

Trenutna javna izdaja:

- Članek Serije 1: odločitve o arhitekturi RAG, primerjave Azure in odprtokodne možnosti ter kje se uvršča fino prilagajanje.
- Članek Serije 2: lokalni odprtokodni RAG vodič.
- Zvezek Serije 2: zagon lokalne RAG laboratorije s FastEmbed, Qdrant, Ollama in Phi-4-mini.
- Vzorčni podatki: Markdown datoteke šolske politike in smernic AI za tečaje.

Narisano, a še ni v javnem indeksu:

- Ponovna izgradnja Azure AI Search in Azure OpenAI.
- Evalvacija RAG in preverjanje regresije.

## Scenarij Vodiča

Deljeni scenarij je pomočnik za šolsko politiko.

Pomočnik odgovori na vprašanje iz lokalnih dokumentov:

```text
Can I use generative AI for my final assignment?
```

Pričakovano vedenje je:

1. Naloži lokalne Markdown dokumente.
2. Razčleni in razdeli jih po naslovih.
3. Ustvari lokalne embedinge in shrani iskalne predstavitve z metapodatki.
4. Pridobi relevantni del politike.
5. Po potrebi ponovno razvrsti.
6. Generira ali sestavi utemeljen odgovor.
7. Vrni citate.
8. Zabeleži rezultate preverjanja.

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

Osnutki so shranjeni v `drafts/` in jih repozitorij preskoči pri preverjanju, dokler niso pripravljeni za javno indeksiranje.

## Preverjanje Serije 2

Preverjeno na Windows z Python 3.12.6.

- Uspešno nameščen `requirements/open-source-rag.txt`.
- Izveden `notebooks/series-2-open-source-rag.ipynb` z `nbclient`.
- Lokalno preverjanje uspešno: naložena 2 vzorčna dokumenta, ustvarjenih 8 kosov, FastEmbed je ustvaril 384-dimenzionalne lokalne embedinge, zagnana Qdrant zbirka v pomnilniku in vstavljeno 8 vektorjev.
- Testno vprašanje: "Ali lahko za mojo končno nalogo uporabim generativno AI?"
- Najvišje pridobljen vir po lahkem ponovnem razvrščanju: `school_ai_policy.md`.
- Najvišje pridobljen odsek po lahkem ponovnem razvrščanju: `Final Assignments`.
- Privzeta pot do odgovora: lokalni transparentni sestavljalec odgovorov.
- Ollama nameščena preko winget; `phi4-mini:3.8b` uspešno prenesen.
- Pot generiranja odgovora Ollama: zaključena s `phi4-mini:3.8b`.
- Velikost datoteke modela Ollama: približno 2,49 GB na disku.
- Naložena velikost modela Ollama: 3,3 GB, poročano z `ollama ps`.
- Odklop GPU: 100% GPU, poročano z `ollama ps` na RTX 3060 Laptop GPU.
- Pomnilnik GPU opažen po generaciji: približno 3,5 GB od 6 GB.
- Izvedba zvezka s predpomnjenim FastEmbed modelom in omogočeno Ollama generacijo je uspela v približno 34 sekundah preko preverjevalnega skripta.
- Opazka: zgodnji prehod nalaganja dokumentov je po nesreči vključeval `sample_data/README.md`; zvezek zdaj naloži samo dva namerna vzorčna dokumenta izrecno.

## Preverjanje repozitorija

- `scripts/verify_notebooks.py` preverja lokalne Markdown povezave, JSON zvezkov, čistočo izhodov zvezkov in vzorce visokorizičnih skrivnosti.
- `scripts/verify_notebooks.py --execute` izvaja javne zvezke iz korena repozitorija.
- Osnutki v `drafts/` so namerno izpuščeni.

## Naslednje delo

- Ponovno zgraditi isti scenarij z Azure AI Search in Azure OpenAI kot del prihodnje serije.
- Dodati pridobivanje in ocenjevanje odgovorov, ko bosta tako lokalna kot Azure implementacija stabilni.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->