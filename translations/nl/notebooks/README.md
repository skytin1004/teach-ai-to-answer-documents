# Notebooks

Deze notebooks ondersteunen de artikelenserie met uitvoerbare voorbeelden.

| Notebook | Artikel | Doel |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serie 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG met FastEmbed, Qdrant lokale modus, ophalen, herordenen, optionele Ollama generatie, en bronverwijzingen |

## Lokale Uitvoering

Installeer de vereisten voor de notebook die je wilt uitvoeren:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Of installeer alle afhankelijkheden:

```powershell
python -m pip install -r requirements\all.txt
```

## Verifiëren

Vanaf de root van de repository:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serie 2 kan Ollama-configuratie lezen van een `.env` bestand in de root van de repository. Begin met [../.env.example](../../../.env.example), die gegroepeerd is per serie.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->