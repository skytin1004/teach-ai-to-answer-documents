# Krav

Hver implementationsartikel har en fokuseret kravfil.

| Fil | Bruges af |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Series 2 open-source RAG-notesbog, inklusive valgfrie Ollama-genereringshjælpere |
| [all.txt](../../../requirements/all.txt) | Repositorie-niveau verifikation og CI |

Brug den fokuserede fil, når du kører én notesbog. Brug `all.txt`, når du validerer hele repositoriet.

`open-source-rag.txt` og `all.txt` inkluderer `fastembed` til lokale embeddings og `python-dotenv`, så Series 2 valgfrit kan aktivere Ollama-generering fra `.env` uden at ændre retrieval-pipelinen.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->