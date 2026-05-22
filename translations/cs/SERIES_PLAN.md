# Naučte AI odpovídat na otázky na základě vašich dokumentů – plán série

Tento plán sleduje veřejné vydání Série 1 a Série 2. Pozdější práce na Azure a hodnocení jsou uchovávány jako koncepty, dokud nebudou příklady plně end-to-end a ověřené.

Neprovádějte commit ani push změn, dokud nebudete výslovně instruováni.

## Veřejný rozsah

Aktuální veřejné vydání:

- Článek Série 1: rozhodnutí o architektuře RAG, kompromisy Azure vs open-source, a kde zapadá doladění.
- Článek Série 2: lokální open-source RAG tutoriál.
- Notebook Série 2: spustitelná lokální RAG laboratoř s FastEmbed, Qdrant, Ollama a Phi-4-mini.
- Ukázková data: Markdown soubory školní politiky a AI doporučení ke kurzu.

Koncepty, které dosud nejsou ve veřejném indexu:

- Přestavba Azure AI Search a Azure OpenAI.
- Hodnocení RAG a kontrola regresí.

## Scénář tutoriálu

Sdílený scénář je asistent školní politiky.

Asistent odpovídá na tuto otázku z lokálních dokumentů:

```text
Can I use generative AI for my final assignment?
```

Očekávané chování je:

1. Načíst lokální Markdown dokumenty.
2. Parsovat a rozdělit je podle nadpisů.
3. Vytvořit lokální embeddingy a uložit vyhledatelné reprezentace s metadaty.
4. Vyhledat relevantní část politiky.
5. Při potřebě přeuspořádat výsledky.
6. Vygenerovat nebo složit odpověď s podkladem.
7. Vrátit citace.
8. Zaznamenat výsledky ověření.

## Aktuální veřejná struktura

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

Konceptový materiál je uložen v `drafts/` a repozitář tímto během ověřování přeskočí, dokud není připraven pro veřejné indexování.

## Ověření Série 2

Ověřeno na Windows s Pythonem 3.12.6.

- Úspěšná instalace `requirements/open-source-rag.txt`.
- Spuštěn `notebooks/series-2-open-source-rag.ipynb` pomocí `nbclient`.
- Lokální ověření prošlo: načteny 2 ukázkové dokumenty, vytvořeno 8 chunků, FastEmbed vytvořil 384-dimenzionální lokální embeddingy, inicializována paměťová kolekce Qdrant, a vloženo 8 vektorů.
- Testovací otázka: "Mohu použít generativní AI pro svou závěrečnou práci?"
- Nejlépe vyhledaný zdroj po lehkém přeuspořádání: `school_ai_policy.md`.
- Nejlépe vyhledaná sekce po lehkém přeuspořádání: `Závěrečné práce`.
- Výchozí cesta odpovědi: lokální transparentní skladatel odpovědí.
- Ollama nainstalována přes winget; `phi4-mini:3.8b` úspěšně stažen.
- Cesta generování odpovědi Ollama: dokončeno s `phi4-mini:3.8b`.
- Velikost modelového souboru Ollama: asi 2,49GB na disku.
- Načtená velikost modelu Ollama: 3,3GB hlášeno `ollama ps`.
- Odlehčení GPU: 100% GPU hlášeno `ollama ps` na RTX 3060 Laptop GPU.
- Pozorovaná GPU paměť po generování: asi 3,5GB z 6GB.
- Spuštění notebooku s cachovaným FastEmbed modelem a povolenou generací Ollama proběhlo asi za 34 sekund pomocí ověřovacího skriptu.
- Poznámka: při raném načítání dokumentů omylem zahrnuto `sample_data/README.md`; nyní notebook načítá explicitně jen dva zamýšlené ukázkové dokumenty.

## Ověření repozitáře

- `scripts/verify_notebooks.py` kontroluje lokální odkazy na Markdown, JSON notebooků, čistotu výstupů notebooků a vzory vysoce rizikových tajemství.
- `scripts/verify_notebooks.py --execute` spouští veřejné notebooky z kořenového adresáře repozitáře.
- Konceptový materiál v `drafts/` je úmyslně přeskočen.

## Další práce

- Přestavba stejného scénáře s Azure AI Search a Azure OpenAI jako budoucí část série.
- Přidání vyhledávání a hodnocení odpovědí, jakmile budou implementace lokální i Azure stabilní.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->