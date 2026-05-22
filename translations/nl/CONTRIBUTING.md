# Bijdragen

Deze repository is georganiseerd als een blogserie plus uitvoerbare notebookvoorbeelden.

## Voordat je een Pull Request opent

Voer het lokale validatiescript uit:

```powershell
python scripts\verify_notebooks.py
```

Voor implementatie- of notebookwijzigingen, voer de lokaal-veilige notebookuitvoering uit:

```powershell
python scripts\verify_notebooks.py --execute
```

## Notebook Richtlijnen

- Houd notebooks leesbaar en gericht op het gerelateerde artikel.
- Commit geen opgeslagen notebookuitvoer of uitvoertellingen.
- Gebruik kleine voorbeeldgegevens uit `sample_data/` tenzij het artikel een specifieke externe bron vereist.
- Noteer verificatieresultaten in het gerelateerde artikel wanneer het gedrag verandert.

## Geheimen en Referenties

- Commit geen API-sleutels, tokens, wachtwoorden, private eindpunten of `.env`-bestanden.
- Gebruik `.env.example` alleen voor plaatsaanduidingen.
- Gebruik omgevingsvariabelen voor optionele lokale Ollama-experimenten.

## Documentatie

- Houd navigatielinks van artikelen up-to-date.
- Werk `README.md` bij bij het toevoegen van een nieuw artikel, notebook, requirements-bestand of voorbeeldgegevensbestand.
- Werk `CHANGELOG.md` bij vóór het publiceren van een zichtbare repository-update.

## Verificatie

De GitHub Actions workflow voert uit:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Conceptmateriaal onder `drafts/` wordt overgeslagen door repositoryverificatie totdat het klaar is voor publieke indexering.

## Problemen

Gebruik de artikel feedback-sjabloon voor artikelcorrecties en de notebook issue-sjabloon voor notebookuitvoeringsproblemen.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->