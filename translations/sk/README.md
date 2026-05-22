# Naučte AI odpovedať na otázky na základe vašich dokumentov

![Prehľad systému dokumentmi podloženej AI RAG](../../assets/images/readme-hero.svg)

Tento repozitár zhromažďuje sériu blogov z roku 2026 o budovaní systémov dokumentmi podloženej AI pomocou RAG, služieb Azure AI, open-source alternatív a workflow orientovaných na vyhodnocovanie.

## Pozadie

V roku 2023 som pracoval na dvoch tutoriáloch o učení ChatGPT odpovedať na otázky z PDF dokumentov pomocou Azure AI Search a Azure OpenAI. Myšlienka „ChatGPT nad vašimi dátami“ bola vtedy stále nová a cieľom bolo ukázať praktický workflow: uložiť dokumenty, indexovať ich, vyhľadať relevantný obsah a generovať odpovede z takto získaného kontextu.

V roku 2026 je ekosystém RAG oveľa širší. Azure AI Search podporuje moderné vektorové a hybridné vyhľadávacie vzory, Azure OpenAI je súčasťou širšieho ekosystému Microsoft Foundry Models a open-source nástroje ako LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama a vLLM sa stali praktickými možnosťami pre reálne systémy.

Preto som sa rozhodol túto tému znovu otvoriť. Otázka už nie je len „Ako postaviť RAG?“ Existuje teraz veľa spôsobov, ako ho vybudovať, a dôležitejšia otázka znie „Ktorú architektúru si vybrať pre moju situáciu?“

Táto séria začína týmto rozhodovacím krokom a následne ho prevedie do praktických tutoriálov. Prvá implementačná cesta vytvára lokálny open-source RAG systém, ktorý si môže spustiť každý s ukážkovými dátami, Qdrantom, Ollamou a Phi-4-mini.

## Články

Index článkov nájdete v [articles/README.md](./articles/README.md).

1. [Séria 1: RAG, Azure vs Open-Source Alternatívy a Kedy Má Zmysel Fine-Tuning](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Séria 2: Postavte Lokálny Open-Source RAG Systém od Začiatku do Konca](./articles/series-2-open-source-rag-end-to-end.md)

Pripravujeme:

- Prestavba toho istého RAG systému s Azure AI Search a Azure OpenAI.
- Pridanie vyhodnocovania a regresných kontrol nad rámec demo odpovede.

## Notebooky

Implementačné články používajú notebooky, aby bolo možné priamo kontrolovať kroky vyhľadávania a vyhodnocovania. Nájdete ich v [notebooks/README.md](./notebooks/README.md).

> [!TIP]
> Začnite so Sériou 2, ak chcete najrýchlejšiu cestu. Beží lokálne s ukážkovými dátami, embeddingmi vhodnými pre CPU, Qdrantom v lokálnom režime bez cloudových prihlasovacích údajov.

| Séria | Notebook | Požiadavky | Lokálna verifikácia |
| --- | --- | --- | --- |
| Séria 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Overený lokálny režim Qdrant, vyhľadávanie, preradenie a prepojenie zdrojov |

Pre spustenie notebooku lokálne vytvorte virtuálne prostredie a nainštalujte zodpovedajúce požiadavky. Napríklad:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Ukážkové dáta

Notebooky používajú malý lokálny korpus v [sample_data](../../sample_data), aby príklady mohli bežať bez súkromných dokumentov alebo cloudových prihlasovacích údajov. Detaily nájdete v [sample_data/README.md](./sample_data/README.md).

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Zhrnutie lokálnej verifikácie

Výsledky verifikácie sú zapísané v každom článku a v [SERIES_PLAN.md](./SERIES_PLAN.md).

| Oblasť | Výsledok |
| --- | --- |
| Séria 2 open-source cesta | FastEmbed vygeneroval lokálne embeddingy 384 dimenzií, Qdrant in-memory kolekcia vložila 8 vektorov, ľahký reranking vyhľadal očakávanú sekciu; voliteľná generácia Ollamou prebehla s `phi4-mini:3.8b` |

Lokálny notebook zámerne neobsahuje pevne zakódované tajné údaje.

## Lokálna generácia Ollama

Notebook Séria 2 je predvolene bezpečný pre lokálne použitie. Ak chcete povoliť lokálnu generáciu Ollamou, skopírujte [.env.example](../../.env.example) do `.env` a vyplňte hodnoty pre Sériu 2.

Pre generáciu Ollama v Sérii 2 odkomentujte:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook Séria 2 automaticky načíta `.env` zo koreňa repozitára pomocou `python-dotenv`.

> [!IMPORTANT]
> Nezdieľajte `.env` súbory, API kľúče, súkromné endpointy ani tenant-specifické hodnoty. Repozitár úmyselne uchováva tajné údaje mimo Markdown súborov a notebookov.

Požiadavkové súbory sú zdokumentované v [requirements/README.md](./requirements/README.md).

Na validáciu odkazov, štruktúry notebookov, čistoty výstupov notebookov a vysoko rizikových vzorcov tajných údajov:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Overovacie skripty sú zdokumentované v [scripts/README.md](./scripts/README.md).

Na vykonanie všetkých notebookov bezpečných pre lokálne použitie v rovnakom prostredí:

```powershell
python scripts\verify_notebooks.py --execute
```

Ten istý overovací proces beží vo GitHub Actions pri pushnutiach, pull requestoch a manuálnom spustení workflow. Návrhové články a notebooky sú zámerne vylúčené z verejnej overovacej cesty.

Pred publikovaním aktualizácií používajte [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Zhrnutie aktuálnych nepublikovaných zmien nájdete v [CHANGELOG.md](./CHANGELOG.md).

Pokyny na príspevky a hygienu notebookov nájdete v [CONTRIBUTING.md](./CONTRIBUTING.md).

## Viacjazyčná podpora

### Podporované cez Co-op Translator (automatizované a vždy aktuálne)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabčina](../ar/README.md) | [Bengálčina](../bn/README.md) | [Bulharčina](../bg/README.md) | [Barmčina (Myanmar)](../my/README.md) | [Čínština (zjednodušená)](../zh-CN/README.md) | [Čínština (tradičná, Hongkong)](../zh-HK/README.md) | [Čínština (tradičná, Macao)](../zh-MO/README.md) | [Čínština (tradičná, Taiwan)](../zh-TW/README.md) | [Chorvátčina](../hr/README.md) | [Čeština](../cs/README.md) | [Dánčina](../da/README.md) | [Holandčina](../nl/README.md) | [Estónčina](../et/README.md) | [Fínčina](../fi/README.md) | [Francúzština](../fr/README.md) | [Nemčina](../de/README.md) | [Gréčtina](../el/README.md) | [Hebrejčina](../he/README.md) | [Hindčina](../hi/README.md) | [Maďarčina](../hu/README.md) | [Indonézština](../id/README.md) | [Taliančina](../it/README.md) | [Japončina](../ja/README.md) | [Kannadčina](../kn/README.md) | [Khmerčina](../km/README.md) | [Kórejčina](../ko/README.md) | [Litovčina](../lt/README.md) | [Malajčina](../ms/README.md) | [Malajálamčina](../ml/README.md) | [Maráthčina](../mr/README.md) | [Nepálčina](../ne/README.md) | [Nigérijská pidžinčina](../pcm/README.md) | [Nórčina](../no/README.md) | [Perzština (Farsi)](../fa/README.md) | [Poľština](../pl/README.md) | [Portugalčina (Brazília)](../pt-BR/README.md) | [Portugalčina (Portugalsko)](../pt-PT/README.md) | [Pandžábčina (Gurmukhi)](../pa/README.md) | [Rumunčina](../ro/README.md) | [Ruština](../ru/README.md) | [Srbčina (Cyrilika)](../sr/README.md) | [Slovenčina](./README.md) | [Slovinčina](../sl/README.md) | [Španielčina](../es/README.md) | [Svahilčina](../sw/README.md) | [Švédčina](../sv/README.md) | [Tagalog (Filipínčina)](../tl/README.md) | [Tamilčina](../ta/README.md) | [Telugčina](../te/README.md) | [Thajčina](../th/README.md) | [Turečtina](../tr/README.md) | [Ukrajinčina](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamčina](../vi/README.md)

> **Radšej klonovať lokálne?**
>
> Tento repozitár obsahuje viac ako 50 jazykových prekladov, čo značne zväčšuje veľkosť sťahovania. Ak chcete klonovať bez prekladov, použite sparse checkout:
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
> Takto získate všetko potrebné na dokončenie kurzu s oveľa rýchlejším sťahovaním.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->