# Skripte

Dieser Ordner enthält Skripte zur Überprüfung des Repositorys.

## `verify_notebooks.py`

Validiert lokale Markdown-Links, Notebook-JSON, Sauberkeit der Notebook-Ausgaben und risikoreiche Geheimmuster:

```powershell
python scripts\verify_notebooks.py
```

Führt alle öffentlichen lokal-sicheren Notebooks aus:

```powershell
python scripts\verify_notebooks.py --execute
```

Der GitHub Actions Workflow verwendet dasselbe Skript.

Entwurfsmaterial unter `drafts/` wird übersprungen, bis es für den öffentlichen Index bereit ist.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->