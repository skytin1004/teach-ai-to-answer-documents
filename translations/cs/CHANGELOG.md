# Změny

## Nezveřejněno

Počáteční rozsah veřejného vydání pro **Naučit AI odpovídat na otázky podle vašich dokumentů**.

### Přidáno

- Článek Série 1 o rozhodnutích architektury RAG, kompromisy Azure vs open-source a kde zapadá doladění.
- Článek Série 2 a poznámkový blok pro lokální open-source workflow RAG používající Qdrant v lokálním režimu, FastEmbed lokální embeddingy, lehké přerankování, Ollama a Phi-4-mini.
- Krok za krokem tutoriál Série 2 v end-to-end formátu s úryvky Pythonu a ověřovacími poznámkami z vykonaného poznámkového bloku.
- Volitelná cesta generování odpovědí Série 2 s Ollama a Phi-4-mini při zachování lokálního CPU-friendly vyhledávání jako výchozí cesty.
- Lokální ověření Ollama pro Série 2 používající `phi4-mini:3.8b` na RTX 3060 Laptop GPU.
- Vzorová data pro školní politiku a AI vedení kurzu.
- Soubory požadavků pro veřejný poznámkový blok a ověřování na úrovni repozitáře.
- Skript ověřování repozitáře pro lokální odkazy Markdown a validaci/spuštění poznámkových bloků.
- Workflow GitHub Actions pro ověřování poznámkových bloků.
- `.env.example` pro volitelné nastavení lokální generace Ollama bez ukládání lokální konfigurace.
- README soubory na úrovni složek pro články, poznámkové bloky, požadavky, vzorová data a skripty.
- Kontrolní seznam publikování pro veřejnou bezpečnost a ověření.
- Návrhové pracovní prostředí pro budoucí obsah Azure a hodnocení.

### Ověřeno

- Validace lokálních Markdown odkazů proběhla úspěšně.
- Poznámkový blok Série 2 prošel validací.
- Poznámkový blok Série 2 byl úspěšně spuštěn v lokálním ověřovacím prostředí.
- Soubory poznámkových bloků jsou uchovány bez uložených výstupů nebo počtů spuštění.
- Žádná skutečná tajemství nebyla uložena do repozitáře.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->