# Notebooks

Disse notebooks understøtter artikelserien med kørbare eksempler.

| Notebook | Artikel | Formål |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serie 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG med FastEmbed, Qdrant lokal tilstand, hentning, omrangering, valgfri Ollama generering og kildehenvisninger |

## Kør Lokalt

Installer kravene for den notebook, du vil køre:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Eller installer alle afhængigheder:

```powershell
python -m pip install -r requirements\all.txt
```

## Verificer

Fra repository-roden:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serie 2 kan læse Ollama-konfiguration fra en `.env`-fil i repository-roden. Start fra [../.env.example](../../../.env.example), som er grupperet efter serie.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->