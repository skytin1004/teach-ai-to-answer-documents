# Σημειωματάρια

Αυτά τα σημειωματάρια υποστηρίζουν τη σειρά άρθρων με εκτελέσιμα παραδείγματα.

| Σημειωματάριο | Άρθρο | Σκοπός |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Σειρά 2](../articles/series-2-open-source-rag-end-to-end.md) | Ανοικτού κώδικα RAG με FastEmbed, λειτουργία Qdrant τοπικά, ανάκτηση, επανακατάταξη, προαιρετική παραγωγή Ollama και αναφορές πηγών |

## Εκτέλεση τοπικά

Εγκαταστήστε τις απαιτήσεις για το σημειωματάριο που θέλετε να εκτελέσετε:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ή εγκαταστήστε όλες τις εξαρτήσεις:

```powershell
python -m pip install -r requirements\all.txt
```

## Επαλήθευση

Από τη ρίζα του αποθετηρίου:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Η Σειρά 2 μπορεί να διαβάσει τη ρύθμιση Ollama από ένα αρχείο `.env` στη ρίζα του αποθετηρίου. Ξεκινήστε από [../.env.example](../../../.env.example), που είναι ομαδοποιημένο κατά σειρά.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Αποποίηση ευθυνών**:
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία μετάφρασης με τεχνητή νοημοσύνη [Co-op Translator](https://github.com/Azure/co-op-translator). Ενώ επιδιώκουμε την ακρίβεια, παρακαλούμε να έχετε υπόψη ότι οι αυτοματοποιημένες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->