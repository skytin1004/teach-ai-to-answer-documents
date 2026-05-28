# Naučte AI odpovídat na otázky na základě vašich dokumentů

![Přehled systému dokumentově založené AI RAG](../../assets/images/readme-hero.svg)

Tento repozitář shromažďuje blogovou sérii z roku 2026 o budování dokumentově založených AI systémů s RAG, službami Azure AI, open-source alternativami a pracovními postupy zaměřenými na hodnocení.

## Pozadí

V roce 2023 jsem pracoval na páru návodů o tom, jak naučit ChatGPT odpovídat na otázky z PDF dokumentů pomocí Azure AI Search a Azure OpenAI. Myšlenka „ChatGPT nad vašimi daty“ byla tehdy stále nová a cílem bylo ukázat praktický pracovní postup: uložit dokumenty, indexovat je, načíst relevantní obsah a generovat odpovědi z tohoto načteného kontextu.

V roce 2026 je ekosystém RAG mnohem větší. Azure AI Search podporuje moderní vzory vektorového a hybridního vyhledávání, Azure OpenAI je součástí širšího ekosystému Microsoft Foundry Models a open-source nástroje jako LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama a vLLM se staly praktickými volbami pro reálné systémy.

Proto jsem chtěl toto téma znovu navštívit. Otázka už není jen „Jak postavit RAG?“. Nyní existuje mnoho způsobů, jak ho postavit, a důležitější otázka zní: „Kterou architekturu bych si měl pro svou situaci vybrat?“

Tato série začíná právě od této rozhodovací fáze a pak ji přeměňuje na praktické návody. První implementační cesta staví lokální open-source RAG systém, který může kdokoliv spustit s ukázkovými daty, Qdrant, Ollamou a Phi-4-mini.

## Články

Index článků viz [articles/README.md](./articles/README.md).

1. [Série 1: RAG, Azure vs Open-Source alternativy a kdy má smysl doladění](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Série 2: Postavte lokální open-source RAG systém od začátku do konce](./articles/series-2-open-source-rag-end-to-end.md)

Co bude následovat:

- Přestavba stejného RAG systému s Azure AI Search a Azure OpenAI.
- Přidání hodnocení a regresních kontrol nad rámec demo odpovědi.

## Notebooky

Implementační články používají notebooky, aby bylo možné přímo zkontrolovat kroky načítání a hodnocení. Viz [notebooks/README.md](./notebooks/README.md) pro pokyny na úrovni složky.

> [!TIP]
> Začněte sérií 2, pokud chcete nejrychlejší cestu. Běží lokálně s ukázkovými daty, CPU-přátelskými embeddingy, Qdrant v lokálním režimu a bez cloudových přihlašovacích údajů.

| Série | Notebook | Požadavky | Lokální ověření |
| --- | --- | --- | --- |
| Série 2 | [Open-source RAG notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Ověřeno: Qdrant lokální režim, načítání, přehodnocování a propojení zdrojů |

Pro spuštění notebooku lokálně vytvořte virtuální prostředí a nainstalujte odpovídající požadavky. Například:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Ukázková data

Notebooky používají malý lokální korpus v [sample_data](../../sample_data), aby příklady mohly běžet bez soukromých dokumentů nebo cloudových přihlašovacích údajů. Podrobnosti najdete v [sample_data/README.md](./sample_data/README.md).

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Shrnutí lokálního ověření

Výsledky ověření jsou zaznamenány v každém článku a v [SERIES_PLAN.md](./SERIES_PLAN.md).

| Oblast | Výsledek |
| --- | --- |
| Série 2 open-source cesta | FastEmbed vygeneroval 384-rozměrné lokální embeddingy, Qdrant in-memory kolekce vložila 8 vektorů, lehké přehodnocování načetlo očekávanou sekci; volitelná generace Ollamou dokončena s `phi4-mini:3.8b` |

Lokální notebook záměrně neobsahuje hardcoded tajné klíče.

## Lokální generování Ollama

Notebook série 2 je ve výchozím nastavení bezpečný pro lokální použití. Pro povolení lokální generace Ollama zkopírujte [.env.example](../../.env.example) na `.env` a vyplňte hodnoty série 2.

Pro generování Ollama ve sérii 2 odkomentujte:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook série 2 automaticky načítá `.env` z kořene repozitáře pomocí `python-dotenv`.

> [!IMPORTANT]
> Nekomitujte `.env` soubory, API klíče, soukromé endpointy nebo hodnoty specifické pro tenanty. Repozitář záměrně drží tajné údaje mimo Markdown soubory a notebooky.

Požadavkové soubory jsou dokumentovány v [requirements/README.md](./requirements/README.md).

Pro ověření odkazů, struktury notebooku, čistoty výstupů a vzorců vysokorizikových tajných údajů:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Ověřovací skripty jsou zdokumentovány v [scripts/README.md](./scripts/README.md).

Pro spuštění všech lokálně bezpečných notebooků ve stejném prostředí:

```powershell
python scripts\verify_notebooks.py --execute
```

Stejný ověřovací proces běží v GitHub Actions při push, pull requestech a manuálním spuštění workflow. Návrhy článků a notebooků jsou z veřejné ověřovací cesty záměrně vyjmuty.

Před publikováním aktualizací použijte [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Změny doposud nezveřejněné najdete v přehledu v [CHANGELOG.md](./CHANGELOG.md).

Pokyny pro přispívání a hygienu notebooků najdete v [CONTRIBUTING.md](./CONTRIBUTING.md).

## Podpora více jazyků

### Podporováno pomocí Co-op Translator (automatická a vždy aktuální)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabština](../ar/README.md) | [Bengálština](../bn/README.md) | [Bulharština](../bg/README.md) | [Barmsky (Myanmar)](../my/README.md) | [Čínština (zjednodušená)](../zh-CN/README.md) | [Čínština (tradiční, Hongkong)](../zh-HK/README.md) | [Čínština (tradiční, Macao)](../zh-MO/README.md) | [Čínština (tradiční, Tchajwan)](../zh-TW/README.md) | [Chorvatština](../hr/README.md) | [Čeština](./README.md) | [Dánština](../da/README.md) | [Nizozemština](../nl/README.md) | [Estonština](../et/README.md) | [Finština](../fi/README.md) | [Francouzština](../fr/README.md) | [Němčina](../de/README.md) | [Řečtina](../el/README.md) | [Hebrejština](../he/README.md) | [ hindština](../hi/README.md) | [Maďarština](../hu/README.md) | [Indonéština](../id/README.md) | [Italština](../it/README.md) | [Japonština](../ja/README.md) | [Kannadština](../kn/README.md) | [Khmerština](../km/README.md) | [Korejština](../ko/README.md) | [Litevština](../lt/README.md) | [Malajština](../ms/README.md) | [Malajalámština](../ml/README.md) | [Maráthština](../mr/README.md) | [Nepálština](../ne/README.md) | [Nigérijský pidžin](../pcm/README.md) | [Norština](../no/README.md) | [Perština (Fársí)](../fa/README.md) | [Polština](../pl/README.md) | [Portugalština (Brazílie)](../pt-BR/README.md) | [Portugalština (Portugalsko)](../pt-PT/README.md) | [Pandžábština (Gurmukhi)](../pa/README.md) | [Rumunština](../ro/README.md) | [Ruština](../ru/README.md) | [Srbština (cyrilice)](../sr/README.md) | [Slovenština](../sk/README.md) | [Slovinština](../sl/README.md) | [Španělština](../es/README.md) | [Svahilština](../sw/README.md) | [Švédština](../sv/README.md) | [Tagalog (filipínština)](../tl/README.md) | [Tamilština](../ta/README.md) | [Telugština](../te/README.md) | [Thajština](../th/README.md) | [Turečtina](../tr/README.md) | [Ukrajinština](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamština](../vi/README.md)

> **Raději klonovat lokálně?**
>
> Tento repozitář obsahuje více než 50 jazykových překladů, což výrazně zvyšuje velikost ke stažení. Pokud chcete klonovat bez překladů, použijte sparse checkout:
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
> To vám zajistí vše potřebné pro dokončení kurzu s mnohem rychlejším stažením.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->