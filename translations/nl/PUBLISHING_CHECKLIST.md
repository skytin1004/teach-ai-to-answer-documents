# Publicatie Controlelijst

Gebruik deze controlelijst voordat je publieke updates commit of pusht.

## Veiligheid

- Bevestig dat er geen API-sleutels, tokens, wachtwoorden of private endpoints zijn opgenomen in Markdown-bestanden, notebooks, voorbeelddata of scripts.
- Bewaar inloggegevens in omgevingsvariabelen of beheerde identiteit, niet in gecommitte bestanden.
- Commit geen `.env` bestanden of notebooks uitvoerbestanden.
- Houd `.env.example` alleen als placeholder.

## Verificatie

Voer het verificatiescript van de repository uit:

```powershell
python scripts\verify_notebooks.py
```

Voer de volledige lokaal-veilige notebook-uitvoering uit voordat implementatiewijzigingen gepubliceerd worden:

```powershell
python scripts\verify_notebooks.py --execute
```

Verwachte controles:

- lokale Markdown-links werken
- notebook JSON-validatie slaagt
- notebooks bevatten geen opgeslagen uitvoer of uitvoeringsaantallen
- scan op hoog risico geheim patroon slaagt
- publieke notebooks draaien lokaal
- conceptmateriaal onder `drafts/` wordt opzettelijk overgeslagen

## Review

- Bevestig dat README-artikellinks verwijzen naar de bedoelde bestanden.
- Bevestig dat elk artikel repository-navigatie en gerelateerde notebook-links heeft.
- Bevestig dat concepten niet gelinkt zijn vanaf publieke indexen tenzij ze klaar zijn voor publicatie.
- Bevestig dat GitHub issue- en pull request-sjablonen nog overeenkomen met de repository workflow.
- Bevestig dat verificatieresultaten in het artikel overeenkomen met de laatste notebookuitvoer.
- Bevestig dat de GitHub Actions workflow verwacht wordt te draaien na push.
- Bevestig dat `CHANGELOG.md` de update die wordt gepubliceerd reflecteert.
- Bevestig dat `CONTRIBUTING.md` nog overeenkomt met de repository workflow.

## Git

- Bekijk `git status --short --branch`.
- Bekijk `git diff --stat`.
- Commit en push alleen als je expliciet klaar bent.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->