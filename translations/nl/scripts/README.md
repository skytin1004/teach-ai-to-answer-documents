# Scripts

Deze map bevat scripts voor het verifiëren van de repository.

## `verify_notebooks.py`

Valideert lokale Markdown-links, notebook JSON, netheid van notebook-uitvoer en hoog-risico geheime patronen:

```powershell
python scripts\verify_notebooks.py
```

Voert alle openbare lokaal-veilige notebooks uit:

```powershell
python scripts\verify_notebooks.py --execute
```

De GitHub Actions workflow gebruikt hetzelfde script.

Conceptmateriaal onder `drafts/` wordt overgeslagen totdat het klaar is voor de publieke index.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->