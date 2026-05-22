# Changelog

## Niet vrijgegeven

Initiële publieke release scope voor **Leer AI vragen beantwoorden op basis van je documenten**.

### Toegevoegd

- Serie 1 artikel over RAG architectuurkeuzes, Azure versus open-source afwegingen, en waar fine-tuning past.
- Serie 2 artikel en notebook voor een lokale open-source RAG workflow met Qdrant lokale modus, FastEmbed lokale embeddings, lichte herordening, Ollama en Phi-4-mini.
- Serie 2 stap-voor-stap end-to-end tutorial-formaat met Python fragments en verificatienotities van de uitgevoerde notebook.
- Optionele Serie 2 antwoordgeneratie-pad met Ollama en Phi-4-mini terwijl lokale CPU-vriendelijke retrieval de standaard blijft.
- Lokale Ollama verificatie voor Serie 2 met `phi4-mini:3.8b` op RTX 3060 Laptop GPU.
- Voorbeelddata voor schoolbeleid en AI-richtlijnen voor cursussen.
- Vereistenbestanden voor de publieke notebook en repository-level verificatie.
- Repository verificatiescript voor lokale Markdown links en notebook validatie/uitvoering.
- GitHub Actions workflow voor notebook verificatie.
- `.env.example` voor optionele lokale Ollama generatie setup zonder lokale configuratie te committen.
- README-bestanden per map voor artikelen, notebooks, vereisten, voorbeelddata en scripts.
- Publicatie checklist voor publieke veiligheid en verificatie.
- Concept workspace voor toekomstige Azure en evaluatie-inhoud.

### Gecontroleerd

- Lokale Markdown link validatie slaagt.
- Serie 2 notebook valideert succesvol.
- Serie 2 notebook voert succesvol uit in de lokale verificatie-omgeving.
- Notebook bestanden worden bewaard zonder opgeslagen uitvoer of uitvoeringsaantallen.
- Geen echte geheimen zijn gecommit.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->