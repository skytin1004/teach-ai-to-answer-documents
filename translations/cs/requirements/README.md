# Požadavky

Každý článek o implementaci má zaměřený soubor požadavků.

| Soubor | Používá |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Série 2 open-source RAG notebook, včetně volitelných pomocníků pro generování Ollama |
| [all.txt](../../../requirements/all.txt) | Ověření na úrovni repozitáře a CI |

Použijte zaměřený soubor při spuštění jednoho notebooku. Použijte `all.txt` při validaci celého repozitáře.

`open-source-rag.txt` a `all.txt` zahrnují `fastembed` pro lokální vkládání a `python-dotenv`, takže Série 2 může volitelně povolit generování Ollama z `.env` bez změny pipeline vyhledávání.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->