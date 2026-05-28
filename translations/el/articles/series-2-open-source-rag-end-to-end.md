# Διδάξτε την ΤΝ να Απαντά σε Ερωτήσεις Βασισμένες στα Έγγραφά σας
## Σειρά 2: Δημιουργία Τοπικού Ανοιχτού Κώδικα Συστήματος RAG από την Αρχή

![Τοπικός ανοιχτού κώδικα οδηγός RAG](../../../assets/images/series-2-local-rag.svg)

> Αυτό το άρθρο μετατρέπει τη συζήτηση της αρχιτεκτονικής της Σειράς 1 σε έναν εκτελέσιμο τοπικό οδηγό RAG. Ο στόχος είναι να δημιουργήσουμε πρώτα την πλήρη ροή εργασίας με δείγματα δεδομένων, χωρίς λογαριασμό cloud και χωρίς μυστικά, και στη συνέχεια να χρησιμοποιήσουμε αυτή τη λειτουργική βάση για να πάρουμε καλύτερες αρχιτεκτονικές αποφάσεις αργότερα.

Το σύστημα που θα κατασκευάσουμε είναι ένας μικρός βοηθός πολιτικής σχολείου. Χρησιμοποιώ δύο τοπικά έγγραφα Markdown ως βάση γνώσης και μετά διασχίζω ολόκληρη τη ροή εργασίας RAG: κατακερματισμό, τοπικές ενσωματώσεις, αποθήκευση διανυσμάτων στο Qdrant, ανάκτηση, επαναταξινόμηση, σύνθεση απαντήσεων με συνείδηση πηγής, και προαιρετική τοπική δημιουργία με Ollama και Phi-4-mini.

Πλοήγηση σειράς: [Αρχική αποθετηρίου](../README.md) | Προηγούμενο: [Σειρά 1 - RAG, Azure vs Εναλλακτικές Ανοιχτού Κώδικα, και Πότε Έχει Νόημα η Εξειδικευμένη Εκπαίδευση](./series-1-rag-azure-open-source-fine-tuning.md)

Σημειωματάριο: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Απαιτήσεις: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Αυτό είναι το καλύτερο σημείο εκκίνησης αν θέλετε να κατανοήσετε τη ροή εργασίας RAG πριν δημιουργήσετε πόρους στο cloud. Η προεπιλεγμένη διαδρομή τρέχει τοπικά με CPU-φιλικές ενσωματώσεις και χωρίς μυστικά.

## 1. Τι Δημιουργούμε

Στον οδηγό του 2023, ξεκίνησα από το Azure επειδή ο στόχος ήταν να δείξω πώς το Azure AI Search και το Azure OpenAI μπορούσαν να απαντούν σε ερωτήσεις από PDF έγγραφα.

Για αυτή τη σειρά 2026, θέλω να ξεκινήσω ένα επίπεδο πιο χαμηλά.

Πριν χρησιμοποιήσω διαχειριζόμενες υπηρεσίες, θέλω να δημιουργήσω ένα μικρό σύστημα RAG τοπικά και να κάνω κάθε βήμα ορατό: φόρτωση εγγράφων, κατακερματισμό κειμένου, αποθήκευση διανυσμάτων, ανάκτηση αποδείξεων, επαναταξινόμηση αποτελεσμάτων, και επιστροφή απάντησης με συνείδηση πηγής.

Το δείγμα σενάριο είναι ένας βοηθός πολιτικής σχολείου. Ο χρήστης ρωτά:

```text
Can I use generative AI for my final assignment?
```

Το σύστημα δεν πρέπει να απαντά από τη γενική μνήμη του μοντέλου. Πρέπει να ανακτά το σχετικό τμήμα πολιτικής και να απαντά βάσει αυτής της απόδειξης.

Η πλήρης εκτελέσιμη έκδοση είναι στο [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Ο παρακάτω κώδικας δείχνει τα κύρια βήματα ώστε το άρθρο να μπορεί να διαβαστεί ως οδηγός.

## 2. Εγκατάσταση Τοπικών Εξαρτήσεων

Δημιουργήστε ένα εικονικό περιβάλλον και εγκαταστήστε τις απαιτήσεις της Σειράς 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Η πρώτη έκδοση χρησιμοποιεί τον τοπικό τρόπο λειτουργίας Qdrant και το FastEmbed. Ο πελάτης Python του Qdrant υποστηρίζει έναν τοπικό τρόπο λειτουργίας εντός μνήμης με `QdrantClient(":memory:")`, που είναι χρήσιμος για τοπικούς οδηγούς και επαλήθευση τύπου CI. Το FastEmbed μας δίνει ένα πραγματικό τοπικό μοντέλο ενσωμάτωσης χωρίς να απαιτεί κλειδί API cloud.

Το αρχείο απαιτήσεων περιλαμβάνει επίσης το `python-dotenv` επειδή το σημειωματάριο μπορεί προαιρετικά να διαβάσει ένα όνομα μοντέλου Ollama από το `.env`. Δεν απαιτείται κλειδί API για Azure OpenAI ή OpenAI για αυτόν τον τοπικό οδηγό.

## 3. Φόρτωση Δειγματικών Εγγράφων

Το δείγμα σώματος είναι σκόπιμα μικρό:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Στο σημειωματάριο, φορτώνω όλα τα αρχεία Markdown από το `sample_data/`:

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

Όταν έτρεξα το σημειωματάριο, φόρτωσε 2 έγγραφα. Αυτό είναι αρκετά μικρό ώστε να ελεγχθεί χειροκίνητα, κάτι που είναι χρήσιμο όταν δημιουργείς την πρώτη έκδοση μιας ροής RAG.

## 4. Κατακερματισμός με Βάση τους Τίτλους Markdown

Το επόμενο βήμα είναι να χωρίσουμε τα έγγραφα σε τμήματα.

Για αυτόν τον οδηγό, χρησιμοποιώ τους τίτλους Markdown ως σήμα δομής. Ο τίτλος εγγράφου προέρχεται από `#`, και κάθε τμήμα τμήματος προέρχεται από `##`.

> [!NOTE]
> Ο κατακερματισμός δεν είναι για όλους κατάλληλος. Σε αυτόν τον οδηγό, χρησιμοποιώ τους τίτλους Markdown επειδή τα δείγματα εγγράφων έχουν ξεκάθαρη δομή `#` και `##`. Για PDF, έγγραφα Word, διαφάνειες, tickets ή σελίδες web, μια καλύτερη στρατηγική μπορεί να χρησιμοποιεί όρια σελίδων, πληροφορίες διάταξης, σημασιολογικά τμήματα, όρια tokens, πίνακες ή μεταδεδομένα. Το σημαντικό είναι να επιλέξετε μια στρατηγική κατακερματισμού που διατηρεί το νόημα και την ιχνηλασιμότητα πηγής για τα έγγραφά σας.

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

Μετά το εφαρμόζω σε κάθε έγγραφο:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Αυτό δημιούργησε 8 τμήματα στην τοπική εκτέλεση.

Αυτό που μου άρεσε σε αυτό το βήμα είναι ότι τα μεταδεδομένα είναι ήδη χρήσιμα. Κάθε τμήμα γνωρίζει την `πηγή`, το `sectionHeading`, την `documentVersion` και τις θέσεις για `permissions`. Ακόμη και σε έναν μικρό οδηγό, αυτό καθιστά τις αναφορές και την αργότερη ανάκτηση με συνείδηση αδειών ευκολότερη στην κατανόηση.

## 5. Δημιουργία Τοπικών Ενσωματώσεων

Για την πρώτη δημόσια έκδοση, χρησιμοποιώ το `BAAI/bge-small-en-v1.5` μέσω FastEmbed.

Αυτό κρατάει τον οδηγό τοπικό και φιλικό προς CPU, αλλά εξακολουθεί να χρησιμοποιεί ένα πραγματικό μοντέλο ενσωμάτωσης αντί για μια πλασματική συνάρτηση διανύσματος. Η πρώτη εκτέλεση κατεβάζει τα βάρη του μοντέλου. Μετά, το σημειωματάριο μπορεί να επαναχρησιμοποιήσει τον τοπικό cache.

> [!NOTE]
> Χρησιμοποιώ το `BAAI/bge-small-en-v1.5` επειδή είναι ένα ελαφρύ αγγλικό μοντέλο ενσωμάτωσης που λειτουργεί καλά με το FastEmbed και το Qdrant για έναν τοπικό οδηγό. Δημιουργεί διανύσματα 384 διαστάσεων, διατηρώντας το παράδειγμα γρήγορο και οικονομικό στην τοπική εκτέλεση. Δεν είναι η μόνη καλή επιλογή. Το 2023, πολλοί οδηγοί χρησιμοποιούσαν φιλοξενούμενα μοντέλα ενσωμάτωσης όπως το `text-embedding-ada-002`. Σήμερα, νεότερες φιλοξενούμενες επιλογές όπως τα OpenAI `text-embedding-3-small` και `text-embedding-3-large`, καθώς και ανοιχτού κώδικα επιλογές όπως BGE, E5, MiniLM, Nomic Embed και πολυγλωσσικά μοντέλα όπως το `BAAI/bge-m3` είναι λογικές επιλογές ανάλογα με το φόρτο εργασίας. Στην παραγωγή, το κατάλληλο μοντέλο ενσωμάτωσης πρέπει να επιλέγεται μέσω αξιολόγησης ανάκτησης στα δικά σας έγγραφα.

Μερικές πρακτικές εναλλακτικές:

| Οικογένεια μοντέλου | Πότε θα το σκεφτόμουν |
| --- | --- |
| `text-embedding-ada-002` | Παλαιότερη φιλοξενούμενη βάση που εμφανίστηκε σε πολλούς οδηγούς εποχής 2023. Δεν θα την επέλεγα ως προεπιλογή για νέο οδηγό σήμερα. |
| `text-embedding-3-small` | Σύγχρονη φιλοξενούμενη προεπιλογή όταν θέλω καλή ισορροπία κόστους/απόδοσης και δεν χρειάζομαι μόνο τοπικές ενσωματώσεις. |
| `text-embedding-3-large` | Φιλοξενούμενη επιλογή όταν έχει μεγαλύτερη σημασία η ποιότητα ανάκτησης από το μέγεθος διανύσματος ή το κόστος ενσωμάτωσης. |
| `BAAI/bge-small-en-v1.5` | Ελαφρύ τοπικό αγγλικό πρότυπο για οδηγούς, πρωτότυπα και πειράματα φιλικά προς CPU. |
| `BAAI/bge-base-en-v1.5` ή `BAAI/bge-large-en-v1.5` | Μεγαλύτερα τοπικά αγγλικά μοντέλα όταν θέλω καλύτερη ποιότητα ανάκτησης και μπορώ να αντέξω περισσότερη υπολογιστική ισχύ. |
| `BAAI/bge-m3` | Πολυγλωσσική ή ανάκτηση με μεγαλύτερο πλαίσιο, ειδικά όταν τα έγγραφα δεν είναι μόνο στα αγγλικά. |
| `sentence-transformers/all-MiniLM-L6-v2` | Πολύ μικρή και γρήγορη βάση για σημασιολογική αναζήτηση. Χρήσιμη όταν μετράει περισσότερο η ταχύτητα και η απλότητα. |
| `nomic-embed-text-v1.5` | Τοπική ανοιχτή επιλογή ενσωμάτωσης άξια δοκιμής για μεγάλες πλαισιακές ή φορητές ρυθμίσεις. |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

Μετά, κάθε τμήμα αποκτά μια ενσωμάτωση:

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. Αποθήκευση Διανυσμάτων σε Τοπικό Τρόπο Qdrant

Τώρα δημιουργούμε μια συλλογή Qdrant εντός μνήμης και εισάγουμε τα τμήματα με μεταδεδομένα φόρτωσης.

> [!NOTE]
> Στον οδηγό του 2023, χρησιμοποίησα το FAISS επειδή ήταν ένας απλός και δημοφιλής τρόπος να δείξω τοπική αναζήτηση ομοιότητας διανυσμάτων με LangChain. Το FAISS είναι ακόμα χρήσιμο για γρήγορα τοπικά πειράματα. Σε αυτή την έκδοση του 2026 χρησιμοποιώ το Qdrant επειδή θέλω ο οδηγός να μοιάζει πιο πολύ με ένα παραγωγικό σύστημα RAG. Το Qdrant επιτρέπει να αποθηκεύω διανύσματα μαζί με μεταδεδομένα όπως αρχείο πηγής, τίτλο τμήματος, έκδοση εγγράφου και δικαιώματα. Αυτό διευκολύνει την επιθεώρηση ανάκτησης και προετοιμάζει το παράδειγμα για φιλτράρισμα, αναφορές, και μελλοντική επίμονη ή server-based ανάπτυξη.

Το FAISS είναι εξαιρετικό για εμφάνιση αναζήτησης ομοιότητας διανυσμάτων. Το Qdrant είναι καλύτερο για μια μικρή αλλά παραγωγικά μορφοποιημένη στρώση ανάκτησης RAG.

Μερικές πρακτικές εναλλακτικές:

| Αποθήκη διανυσμάτων / στρώση αναζήτησης | Πότε θα το σκεφτόμουν |
| --- | --- |
| Qdrant | Τοπικά πρωτότυπα, φιλτράρισμα μεταδεδομένων, παραγωγική αναζήτηση διανυσμάτων, και απλή ροή εργασίας Python. |
| Chroma | Γρήγορα τοπικά πειράματα RAG και σημειωματάρια όπου μετράει η απλότητα. |
| FAISS | Ελαφριά τοπική αναζήτηση διανυσμάτων όταν χρειάζομαι μόνο ομοιότητα και μπορώ να διαχειρίζομαι μεταδεδομένα ξεχωριστά. |
| Milvus | Μεγαλύτερης κλίμακας ανοιχτού κώδικα αναζήτηση διανυσμάτων όταν η ομάδα είναι έτοιμη να λειτουργήσει μια ειδική βάση δεδομένων διανυσμάτων. |
| Weaviate | Αναζήτηση διανυσμάτων με σχήμα, μεταδεδομένα, υβριδική αναζήτηση, και επιλογές διαχείρισης ή αυτο-φιλοξενίας. |
| Azure AI Search | Επιχειρησιακό RAG στο Azure όταν θέλω αναζήτηση με λέξεις-κλειδιά, αναζήτηση διανυσμάτων, υβριδική ανάκτηση, σημασιολογική κατάταξη, φιλτράρισμα, ασφάλεια και διαχειριζόμενες λειτουργίες σε μία στρώση αναζήτησης. |
| PostgreSQL + pgvector | Ομάδες που ήδη χρησιμοποιούν PostgreSQL και θέλουν αναζήτηση διανυσμάτων κοντά στα δεδομένα εφαρμογής. |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

Μετά εισάγουμε τα σημεία:

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

Στο δικό μου τρέξιμο, η συλλογή εισήγαγε 8 διανύσματα.

Εδώ το σύστημα RAG αρχίζει να γίνεται επιθεωρήσιμο. Η βάση δεδομένων διανυσμάτων δεν αποθηκεύει μόνο διανύσματα· αποθηκεύει το κείμενο απόδειξης και τα μεταδεδομένα που χρειάζονται για τις αναφορές.

## 7. Ανάκτηση Υποψήφιων Τμημάτων

Τώρα θέτουμε την ερώτηση και ανακτούμε υποψήφια τμήματα.

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

Σε αυτό το σημείο, εκτυπώνω τα ανακτηθέντα τμήματα πριν από τη δημιουργία απάντησης. Αυτό είναι σημαντικό. Αν η ανάκτηση είναι λανθασμένη, η δημιουργία θα κρύψει το πρόβλημα πίσω από ρέον κείμενο.

## 8. Προσθήκη Ελαφριάς Επαναταξινόμησης

Όταν δοκίμασα για πρώτη φορά τη διαδρομή ανάκτησης, η ομοιότητα διανυσμάτων βρήκε σχετικό περιεχόμενο πολιτικής, αλλά το πιο ακριβές τμήμα δεν ήταν πάντα πρώτο.

Έτσι πρόσθεσα έναν μικρό τοπικό επαναταξινομητή. Αυτός δίνει επιπλέον βάρος όταν οι όροι της ερώτησης επικαλύπτονται με τον τίτλο και το περιεχόμενο του τμήματος.

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

Μετά την επαναταξινόμηση, το κορυφαίο αποτέλεσμα έγινε:

```text
school_ai_policy.md / Final Assignments
```

Αυτό ήταν το αναμενόμενο τμήμα για την ερώτηση δοκιμής.

Αυτό ήταν το πιο χρήσιμο μάθημα από την πρώτη υλοποίηση. Ακόμη και σε ένα μικρό τοπικό παράδειγμα, η ποιότητα ανάκτησης βελτιώθηκε όταν συνδύασα την ομοιότητα διανυσμάτων με ένα άλλο σήμα.

## 9. Σύνθεση Μιας Θεμελιωμένης Τοπικής Απάντησης

Για την προεπιλεγμένη διαδρομή, χρησιμοποιώ έναν διαφανή τοπικό συνθέτη απαντήσεων αντί για LLM.

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

Αυτό δεν προορίζεται να είναι τελικός generator απαντήσεων. Είναι εργαλείο αποσφαλμάτωσης. Αποδεικνύει ότι η ανάκτηση, τα μεταδεδομένα και η διασύνδεση αναφορών λειτουργούν πριν προστεθεί η μεταβλητότητα του μοντέλου.

## 10. Δημιουργία Τοπικής Απάντησης με Ollama και Phi-4-mini

Αφού η ανάκτηση δουλεύει, το σημειωματάριο μπορεί να αντικαταστήσει μόνο το τελικό βήμα απάντησης με Ollama και `phi4-mini:3.8b`.

> [!NOTE]
> Το Ollama πρέπει να αντικαθιστά μόνο το τελικό βήμα παραγωγής απάντησης. Η φόρτωση εγγράφων, ο κατακερματισμός, η αποθήκευση διανυσμάτων, η ανάκτηση, η επαναταξινόμηση και η διασύνδεση αναφορών πρέπει να παραμείνουν τα ίδια.

Πρώτα, το σημειωματάριο δημιουργεί ένα prompt αποδεικτικών από τα ανακτημένα τμήματα:

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

Για αυτόν τον οδηγό, προτείνω την οικογένεια Phi-4-mini της Microsoft μέσω Ollama ως προεπιλεγμένη τοπική επιλογή δημιουργίας. Στο Ollama, το όνομα μοντέλου που δοκίμασα είναι:

```powershell
ollama pull phi4-mini:3.8b
```

Μπορείτε γρήγορα να ελέγξετε ότι το μοντέλο είναι διαθέσιμο:

```powershell
ollama list
```

Έπειτα ορίζουμε αυτές τις μεταβλητές:

```powershell
Copy-Item .env.example .env
```

Ανοίξτε το `.env` και ξεσχολιάστε τις τιμές Ollama της Σειράς 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Το σημειωματάριο φορτώνει το `.env` από τη ρίζα του αποθετηρίου με `python-dotenv`, και μετά στέλνει το ίδιο prompt αποδεικτικών στο τοπικό endpoint `/api/chat` του Ollama με απενεργοποιημένη ροή. Αν το Ollama δεν τρέχει ή λείπει το `SERIES2_OLLAMA_MODEL`, αυτή η διαδρομή παραλείπεται.

> [!NOTE]
> Σε αυτόν τον υπολογιστή, το `phi4-mini:3.8b` κατέβηκε περίπου 2.49GB αρχεία μοντέλου. Κατά την εκτέλεση, το Ollama ανέφερε μέγεθος φορτωμένου μοντέλου 3.3GB και χρησιμοποίησε την κάρτα γραφικών RTX 3060 Laptop.

Αυτό δίνει στον οδηγό δύο επίπεδα:

1. Συνθέτης απαντήσεων μόνο με CPU και με καθοριστικό τρόπο.
2. Τοπική δημιουργία απάντησης με Ollama και Phi-4-mini.

Η ροή ανάκτησης παραμένει η ίδια και στις δύο.

## 11. Αποτέλεσμα Επαλήθευσης

Έτρεξα το σημειωματάριο τοπικά σε Windows με Python 3.12.6.

Εγκατεστημένα πακέτα:

| Πακέτο | Έκδοση |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Εκτέλεση σημειωματαρίου:

- Σημειωματάριο: `notebooks/series-2-open-source-rag.ipynb`
- Αποτέλεσμα εκτέλεσης: επιτυχής με `nbclient`
- Φορτωμένα έγγραφα: 2
- Δημιουργημένα τμήματα: 8
- Συλλογή Qdrant: `school_policy_local`
- Εισαγμένα διανύσματα: 8
- Μοντέλο ενσωμάτωσης: `BAAI/bge-small-en-v1.5`
- Μέγεθος ενσωμάτωσης: 384
- Ερώτηση ανάκτησης: "Μπορώ να χρησιμοποιήσω γενετική AI για την τελική μου εργασία;"
- Διαδρομή επαναταξινόμησης: ελαφριά τοπική λεξιλογική επαναταξινόμηση
- Κορυφαία ανακτηθείσα πηγή μετά την επαναταξινόμηση: `school_ai_policy.md`
- Κορυφαία ανακτηθείσα ενότητα μετά την επαναταξινόμηση: `Final Assignments`
- Προεπιλεγμένη διαδρομή απάντησης: τοπικός διάφανος συνθέτης απάντησης
- Διαδρομή δημιουργίας Ollama: ολοκληρώθηκε με `phi4-mini:3.8b`
- Μέγεθος αρχείου μοντέλου Ollama: 2.49GB στο δίσκο
- Φορτωμένο μέγεθος μοντέλου Ollama: 3.3GB αναφέρεται από το `ollama ps`
- Αποφόρτωση GPU: 100% GPU αναφέρεται από το `ollama ps`
- Μνήμη GPU που παρατηρήθηκε μετά τη δημιουργία: περίπου 3.5GB από 6GB χρησιμοποιούνται σε RTX 3060 Laptop GPU
- Εκτέλεση σημειωματάριου με αποθηκευμένο μοντέλο FastEmbed και ενεργοποιημένη τη δημιουργία Ollama: πέρασε σε περίπου 34 δευτερόλεπτα μέσω του σεναρίου επαλήθευσης

Η απάντηση που παρήγαγε το Ollama ήταν:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Δεν θα χαρακτήριζα αυτή την απάντηση τέλεια. Απαντά από τη σωστή απόδειξη, αλλά η τελική γραμμή πηγής είναι λιγότερο ακριβής από τη μορφή αυστηρής παραπομπής. Αυτό είναι χρήσιμο να δείχνει το εκπαιδευτικό υλικό επειδή καθιστά προφανές το επόμενο μηχανικό ερώτημα: η δημιουργία απάντησης χρειάζεται επίσης αξιολόγηση, όχι μόνο ανάκτηση.

Το κύριο πράγμα που έμαθα ενώ επαλήθευα αυτό είναι ότι η ποιότητα της ανάκτησης θα πρέπει να ελέγχεται πριν από τη δημιουργία της απάντησης. Το αποτέλεσμα του ενσωματωμένου ήδη ήταν χρήσιμο, και ο ελαφρύς επαναταξινομητής έκανε την αναμενόμενη ενότητα πολιτικής να εμφανίζεται αξιόπιστα πρώτη. Αυτό είναι ακριβώς το είδος συμπεριφοράς μικρού συστήματος που θέλω το εκπαιδευτικό υλικό να αποκαλύψει αντί να κρύβει.

## 12. Τι Ακολουθεί

Η επόμενη βελτίωση είναι να συγκριθεί αυτό το τοπικό περιβάλλον με μια διαχειριζόμενη έκδοση Azure του ίδιου σεναρίου βοηθού πολιτικής σχολείου. Η σταθερή διατήρηση του σεναρίου θα κάνει πιο εύκολη την κατανόηση των ανταλλαγών: πολυπλοκότητα εγκατάστασης, έλεγχοι ανάκτησης, ενσωμάτωση ταυτότητας, λειτουργική ιδιοκτησία και κόστος.

## 13. Αναφορές

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub repository](https://github.com/qdrant/qdrant-client)
- [FastEmbed supported models](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 model card](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 model card](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini model page](https://ollama.com/library/phi4-mini)
- [Ollama Windows documentation](https://docs.ollama.com/windows)
- [Ollama API streaming documentation](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct model card](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph)
- [Introduction to RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Προηγούμενο: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Αποποίηση ευθυνών**:
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία μετάφρασης με τεχνητή νοημοσύνη [Co-op Translator](https://github.com/Azure/co-op-translator). Ενώ επιδιώκουμε την ακρίβεια, παρακαλούμε να έχετε υπόψη ότι οι αυτοματοποιημένες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->