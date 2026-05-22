# Vereisten

Elk implementatie-artikel heeft een gericht vereistenbestand.

| Bestand | Gebruikt door |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Serie 2 open-source RAG-notebook, inclusief optionele Ollama generatiehulpjes |
| [all.txt](../../../requirements/all.txt) | Repositorium-niveau verificatie en CI |

Gebruik het gerichte bestand bij het uitvoeren van één notebook. Gebruik `all.txt` bij het valideren van het volledige repositorium.

`open-source-rag.txt` en `all.txt` bevatten `fastembed` voor lokale embeddings en `python-dotenv` zodat Serie 2 optioneel Ollama-generatie vanuit `.env` kan inschakelen zonder de retrieval-pijplijn te veranderen.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->