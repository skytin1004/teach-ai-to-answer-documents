# Naučte AI odpovedať na otázky na základe vašich dokumentov - plán série

Tento plán sleduje verejné vydanie Série 1 a Série 2. Neskoršia práca s Azure a hodnotením je uchovávaná ako návrhy, kým nebudú príklady plne end-to-end a overené.

Neposielajte ani nezverejňujte zmeny, kým nebudete výslovne vyzvaní.

## Verejný rozsah

Aktuálne verejné vydanie:

- Článok Série 1: rozhodnutia architektúry RAG, kompromisy medzi Azure a open-source, a kde sa hodí doladenie.
- Článok Série 2: tutoriál lokálneho open-source RAG.
- Zápisník Série 2: spustiteľná lokálna RAG laboratórium s FastEmbed, Qdrant, Ollama a Phi-4-mini.
- Ukážkové dáta: školská politika a pokyny AI k predmetom v Markdown súboroch.

Návrhy, ktoré ešte nie sú vo verejnom indexe:

- Prebudovanie Azure AI Search a Azure OpenAI.
- Hodnotenie RAG a regresné kontroly.

## Scenár tutoriálu

Zdieľaný scenár je asistent školských pravidiel.

Asistent odpovedá na túto otázku z lokálnych dokumentov:

```text
Can I use generative AI for my final assignment?
```

Očakávané správanie je:

1. Načítať lokálne Markdown dokumenty.
2. Parsovať a rozdeliť ich podľa záhlaví.
3. Vytvoriť lokálne embeddingy a uložiť vyhľadávateľné reprezentácie s metadátami.
4. Získať relevantnú časť politiky.
5. Podľa potreby preradiť výsledky.
6. Vygenerovať alebo zložiť podloženú odpoveď.
7. Vrátiť citácie.
8. Zaznamenať výsledky overenia.

## Aktuálna verejná štruktúra

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

Návrhový materiál je uložený v `drafts/` a je preskakovaný overovacím nástrojom repozitára, kým nie je pripravený na verejné indexovanie.

## Overenie Série 2

Overené na Windows s Python 3.12.6.

- Úspešne nainštalované `requirements/open-source-rag.txt`.
- Spustený `notebooks/series-2-open-source-rag.ipynb` pomocou `nbclient`.
- Lokálne overenie úspešné: načítané 2 ukážkové dokumenty, vytvorených 8 chunkov, FastEmbed vygeneroval 384-dimenzionálne lokálne embeddingy, inicializovaná Qdrant kolekcia v pamäti, vložených 8 vektorov.
- Testovacia otázka: "Môžem použiť generatívnu AI na moju záverečnú prácu?"
- Najlepšie získaný zdroj po ľahkom preradení: `school_ai_policy.md`.
- Najlepšia získaná sekcia po ľahkom preradení: `Final Assignments`.
- Predvolená cesta odpovede: lokálny transparentný skladateľ odpovedí.
- Ollama nainštalovaný cez winget; `phi4-mini:3.8b` úspešne stiahnutý.
- Cesta generovania odpovede cez Ollama: dokončená s `phi4-mini:3.8b`.
- Veľkosť súboru Ollama modelu: približne 2,49 GB na disku.
- Nahlásená veľkosť načítaného modelu Ollama: 3,3 GB podľa `ollama ps`.
- Offload na GPU: 100 % GPU podľa `ollama ps` na RTX 3060 Laptop GPU.
- Pamäť GPU pozorovaná po generovaní: približne 3,5 GB z 6 GB.
- Spustenie zápisníka s kešovaným FastEmbed modelom a povolenou generáciou Ollama prebehlo úspešne za približne 34 sekúnd pomocou overovacieho skriptu.
- Pozorovanie: skoré prebehnutie načítania dokumentov omylom zahrnulo `sample_data/README.md`; zápisník teraz explicitne načítava iba dva zamýšľané ukážkové dokumenty.

## Overenie repozitára

- `scripts/verify_notebooks.py` validuje lokálne Markdown odkazy, JSON zápisníkov, čistotu výstupov zápisníkov a vzory vysoko rizikových tajomstiev.
- `scripts/verify_notebooks.py --execute` spúšťa verejné zápisníky z koreňa repozitára.
- Návrhový materiál v `drafts/` je zámerne preskakovaný.

## Ďalšia práca

- Prebudovať ten istý scenár s Azure AI Search a Azure OpenAI ako časť budúcej série.
- Pridať vyhľadávanie a hodnotenie odpovedí, keď budú lokálne a Azure implementácie stabilné.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->