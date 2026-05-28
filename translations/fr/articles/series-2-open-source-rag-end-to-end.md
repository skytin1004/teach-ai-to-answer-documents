# Enseigner à l’IA à répondre aux questions à partir de vos documents
## Série 2 : Construire un système RAG open-source local de bout en bout

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Cet article transforme la discussion d’architecture de la Série 1 en un tutoriel RAG local exécutable. L’objectif est de construire d’abord le workflow complet avec des données d’exemple, sans compte cloud et sans secrets, puis d’utiliser cette base fonctionnelle pour prendre de meilleures décisions architecturales par la suite.

Le système que nous allons construire est un petit assistant de politique scolaire. J’utilise deux documents Markdown locaux comme base de connaissances, puis je parcours tout le pipeline RAG : découpage, embeddings locaux, stockage vectoriel Qdrant, récupération, reranking, composition de réponse consciente des sources et génération locale optionnelle avec Ollama et Phi-4-mini.

Navigation de la série : [Accueil du dépôt](../README.md) | Précédent : [Série 1 - RAG, alternatives Azure vs open-source et quand le fine-tuning a du sens](./series-1-rag-azure-open-source-fine-tuning.md)

Carnet : [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Prérequis : [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> C’est le meilleur point de départ si vous souhaitez comprendre le pipeline RAG avant de créer des ressources cloud. Le chemin par défaut s’exécute localement avec des embeddings compatibles CPU et sans secrets.

## 1. Ce que nous construisons

Dans le tutoriel 2023, j’ai commencé par Azure car l’objectif était de montrer comment Azure AI Search et Azure OpenAI pouvaient répondre aux questions à partir de documents PDF.

Pour cette série 2026, je veux partir un cran plus bas.

Avant d’utiliser les services managés, je veux construire un petit système RAG localement et rendre chaque étape visible : chargement des documents, découpage en chunks, stockage des vecteurs, récupération de preuves, reranking, et retour d’une réponse consciente des sources.

Le scénario d’exemple est un assistant de politique scolaire. L’utilisateur demande :

```text
Can I use generative AI for my final assignment?
```

Le système ne doit pas répondre à partir de la mémoire générale du modèle. Il doit récupérer la section pertinente de la politique et répondre à partir de cette preuve.

La version complète exécutable est dans [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Le code ci-dessous montre les étapes principales pour que l’article puisse être lu comme un tutoriel.

## 2. Installer les dépendances locales

Créez un environnement virtuel et installez les prérequis de la Série 2 :

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

La première version utilise le mode local de Qdrant et FastEmbed. Le client Python de Qdrant supporte un mode local en mémoire avec `QdrantClient(":memory:")`, ce qui est utile pour les tutoriels locaux et la vérification de type CI. FastEmbed nous offre un vrai modèle d’embeddings local sans nécessiter de clé d’API cloud.

Le fichier de dépendances inclut aussi `python-dotenv` car le carnet peut optionnellement lire un nom de modèle Ollama depuis `.env`. Aucun clé API Azure OpenAI ou OpenAI n’est requise pour ce tutoriel local.

## 3. Charger les documents exemples

Le corpus d’exemple est volontairement petit :

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Dans le carnet, je charge tous les fichiers Markdown depuis `sample_data/` :

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

Quand j’ai lancé le carnet, il a chargé 2 documents. C’est assez petit pour inspecter manuellement, ce qui est utile lors de la construction de la première version d’un pipeline RAG.

## 4. Découpage par titres Markdown

L’étape suivante est de diviser les documents en chunks.

Pour ce tutoriel, j’utilise les titres Markdown comme signal de structure. Le titre principal vient de `#`, et chaque chunk de section vient de `##`.

> [!NOTE]
> Le découpage n’est pas universel. Dans ce tutoriel, j’utilise les titres Markdown car les documents exemples ont une structure claire en `#` et `##`. Pour des PDF, documents Word, diapositives, tickets ou pages web, une meilleure stratégie pourrait utiliser les limites de pages, la mise en page, les sections sémantiques, les limites de tokens, les tableaux ou les métadonnées. L’essentiel est de choisir une stratégie de découpage qui préserve le sens et la traçabilité des sources pour vos documents.

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

Puis je l’applique à chaque document :

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Cela a créé 8 chunks lors de ma session locale.

Ce que j’ai aimé dans cette étape, c’est que les métadonnées sont déjà utiles. Chaque chunk connaît sa `source`, `sectionHeading`, `documentVersion` et un placeholder `permissions`. Même dans un petit tutoriel, cela facilite les citations et la récupération consciente des permissions ensuite.

## 5. Créer des embeddings locaux

Pour la première version publique, j’utilise `BAAI/bge-small-en-v1.5` via FastEmbed.

Cela garde le tutoriel local et compatible CPU, mais utilise quand même un vrai modèle d’embeddings au lieu d’une fonction vecteur factice. La première exécution télécharge les poids du modèle. Ensuite, le carnet peut réutiliser le cache local.

> [!NOTE]
> J’utilise `BAAI/bge-small-en-v1.5` car c’est un modèle d’embeddings léger en anglais qui fonctionne bien avec FastEmbed et Qdrant pour un tutoriel local. Il crée des vecteurs en dimension 384, ce qui maintient l’exemple rapide et peu coûteux à exécuter localement. Ce n’est pas le seul bon choix. En 2023, beaucoup de tutoriels utilisaient des modèles hébergés comme `text-embedding-ada-002`. Aujourd’hui, des options hébergées plus récentes comme OpenAI `text-embedding-3-small` et `text-embedding-3-large`, ainsi que des options open-source comme BGE, E5, MiniLM, Nomic Embed, et des modèles multilingues comme `BAAI/bge-m3` sont toutes des choix raisonnables selon la charge de travail. En production, le modèle d’embeddings adapté doit être choisi via une évaluation de récupération sur vos propres documents.

Quelques alternatives pratiques :

| Famille de modèles | Quand je la considérerais |
| --- | --- |
| `text-embedding-ada-002` | Ancien standard hébergé apparu dans plusieurs tutoriels vers 2023. Je ne le choisirais pas comme défaut pour un nouveau tutoriel aujourd’hui. |
| `text-embedding-3-small` | Option par défaut moderne hébergée quand je cherche un bon compromis coût/performance et ne nécessite pas d’embeddings locaux uniquement. |
| `text-embedding-3-large` | Option hébergée quand la qualité de la récupération compte plus que la taille du vecteur ou le coût d’embeddings. |
| `BAAI/bge-small-en-v1.5` | Baseline locale légère en anglais pour tutoriels, prototypes, et expériences compatibles CPU. |
| `BAAI/bge-base-en-v1.5` ou `BAAI/bge-large-en-v1.5` | Modèles locaux anglais plus grands pour meilleure qualité de récupération et ressources de calcul supérieures. |
| `BAAI/bge-m3` | Récupération multilingue ou sur contexte plus long, surtout quand les documents ne sont pas uniquement en anglais. |
| `sentence-transformers/all-MiniLM-L6-v2` | Baseline de recherche sémantique très petite et rapide. Utile quand la vitesse et la simplicité sont prioritaires. |
| `nomic-embed-text-v1.5` | Option open source d’embeddings locaux à tester pour des configurations avec contexte long ou axées portabilité. |

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

Puis chaque chunk reçoit un embedding :

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

## 6. Stocker les vecteurs en mode Qdrant local

Nous créons maintenant une collection Qdrant en mémoire et insérons les chunks avec les métadonnées en charge utile.

> [!NOTE]
> Dans le tutoriel 2023, j’avais utilisé FAISS car c’était une façon simple et populaire de démontrer la recherche vectorielle locale avec LangChain. FAISS est toujours utile pour des expériences rapides locales. Dans cette version 2026, j’utilise Qdrant parce que je veux que le tutoriel ressemble davantage à un système RAG de production. Qdrant me permet de stocker les vecteurs avec les métadonnées comme le fichier source, le titre de section, la version du document et les permissions. Cela facilite l’inspection de la récupération et prépare l’exemple pour filtrages, citations, et des déploiements persistants ou serveurs futurs.

FAISS est idéal pour montrer la recherche vectorielle par similarité. Qdrant est meilleur pour montrer une couche de récupération RAG petite mais façonnée pour la production.

Quelques alternatives pratiques :

| Stockage vectoriel / couche de recherche | Quand je la considérerais |
| --- | --- |
| Qdrant | Prototypes locaux, filtrage des métadonnées, recherche vectorielle production-friendly, et workflow Python simple. |
| Chroma | Expériences RAG rapides locales et carnets où la simplicité prime. |
| FAISS | Recherche vectorielle locale simple quand j’ai juste besoin de similarité et peux gérer les métadonnées séparément. |
| Milvus | Recherche vectorielle open-source à plus grande échelle quand l’équipe est prête à gérer une base vectorielle dédiée. |
| Weaviate | Recherche vectorielle avec schéma, métadonnées, recherche hybride, et options de déploiement géré ou auto-hébergé. |
| Azure AI Search | RAG entreprise sur Azure quand je veux recherche par mots-clés, vecteurs, récupération hybride, classement sémantique, filtrage, sécurité, et opérations managées en une couche de recherche. |
| PostgreSQL + pgvector | Équipes déjà sur PostgreSQL souhaitant la recherche vectorielle proche des données applicatives. |

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

Ensuite, insérez les points :

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

Dans mon exécution, la collection a inséré 8 vecteurs.

C’est ici que le système RAG commence à devenir inspectable. La base vectorielle ne stocke pas que les vecteurs ; elle stocke aussi le texte des preuves et les métadonnées nécessaires pour les citations.

## 7. Récupérer les chunks candidats

Nous posons maintenant la question et récupérons les chunks candidats.

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

À ce stade, j’affiche les chunks récupérés avant de générer une réponse. C’est important. Si la récupération est erronée, la génération masquera seulement le problème derrière un texte fluide.

## 8. Ajouter un reranker léger

Lorsque j’ai testé la première fois le chemin de récupération, la similarité vectorielle seule trouvait des contenus politiques liés, mais la section la plus précise n’était pas toujours en tête.

J’ai donc ajouté un petit reranker local. Il donne un poids supplémentaire quand les termes de la question chevauchent le titre de la section et son contenu.

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

Après reranking, le meilleur résultat est devenu :

```text
school_ai_policy.md / Final Assignments
```

C’était la section attendue pour la question test.

C’était la leçon la plus utile de la première implémentation. Même dans un petit exemple local, la qualité de récupération s’est améliorée en combinant similarité vectorielle et un autre signal.

## 9. Composer une réponse locale ancrée

Pour le chemin par défaut, j’utilise un compositeur de réponses local transparent au lieu d’un LLM.

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

Ce n’est pas censé être un générateur de réponse produit final. C’est un outil de débogage. Il prouve que la récupération, les métadonnées et le câblage des citations fonctionnent avant d’ajouter la variabilité du modèle.

## 10. Générer une réponse locale avec Ollama et Phi-4-mini

Une fois la récupération opérationnelle, le carnet peut remplacer seulement l’étape finale de réponse par Ollama et `phi4-mini:3.8b`.

> [!NOTE]
> Ollama doit remplacer seulement l’étape finale de génération de réponse. Le chargement des documents, le découpage en chunks, le stockage vectoriel, la récupération, le reranking et le câblage des citations doivent rester inchangés.

D’abord, le carnet construit une invite d’évidence à partir des chunks récupérés :

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

Pour ce tutoriel, je recommande la famille Phi-4-mini de Microsoft via Ollama comme option de génération locale par défaut. Dans Ollama, le modèle que j’ai testé est :

```powershell
ollama pull phi4-mini:3.8b
```

Vous pouvez rapidement vérifier que le modèle est disponible :

```powershell
ollama list
```

Puis réglez ces variables :

```powershell
Copy-Item .env.example .env
```

Ouvrez `.env` et décommentez les valeurs Ollama de la Série 2 :

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Le carnet charge `.env` depuis la racine du dépôt avec `python-dotenv`, puis envoie la même invite d’évidence à l’endpoint local `/api/chat` d’Ollama avec le streaming désactivé. Si Ollama ne tourne pas ou que `SERIES2_OLLAMA_MODEL` manque, cette piste est sautée.

> [!NOTE]
> Sur cette machine, `phi4-mini:3.8b` a téléchargé environ 2,49 Go de fichiers modèle. Pendant l’inférence, Ollama a signalé une taille de modèle chargée de 3,3 Go et a utilisé le GPU RTX 3060 Laptop.

Cela donne deux niveaux au tutoriel :

1. Compositeur de réponse déterministe CPU uniquement.
2. Génération locale de réponse avec Ollama et Phi-4-mini.

Le pipeline de récupération reste le même dans les deux.

## 11. Résultat de vérification

J’ai exécuté le carnet localement sous Windows avec Python 3.12.6.

Packages installés :

| Package | Version |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Exécution du carnet :

- Carnet : `notebooks/series-2-open-source-rag.ipynb`
- Résultat d’exécution : réussi avec `nbclient`
- Documents chargés : 2
- Chunks créés : 8
- Collection Qdrant : `school_policy_local`
- Vecteurs insérés : 8
- Modèle d’embedding : `BAAI/bge-small-en-v1.5`
- Taille de l’embedding : 384
- Question de recherche : « Puis-je utiliser l’IA générative pour mon devoir final ? »
- Chemin de rerangement : rerangement lexical local léger
- Source la mieux récupérée après rerangement : `school_ai_policy.md`
- Section la mieux récupérée après rerangement : `Final Assignments`
- Chemin de la réponse par défaut : compositeur de réponse locale transparente
- Chemin de génération Ollama : complété avec `phi4-mini:3.8b`
- Taille du fichier modèle Ollama : 2,49 Go sur disque
- Taille du modèle Ollama chargé : 3,3 Go rapporté par `ollama ps`
- Déchargement GPU : 100 % GPU rapporté par `ollama ps`
- Mémoire GPU observée après génération : environ 3,5 Go sur 6 Go utilisés sur RTX 3060 Laptop GPU
- Exécution du notebook avec modèle FastEmbed mis en cache et génération Ollama activée : réussie en environ 34 secondes via le script de vérification

La réponse générée par Ollama était :

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Je ne qualifierais pas cette réponse de parfaite. Elle répond à partir de la bonne preuve, mais la ligne source finale est moins précise que le format de citation déterministe. Cela est utile à montrer dans le tutoriel car cela rend évidente la prochaine question d’ingénierie : la génération de réponse nécessite également une évaluation, pas seulement la récupération.

La principale chose que j’ai apprise en vérifiant cela est que la qualité de la récupération doit être vérifiée avant la génération de réponse. Le résultat de l’encodage était déjà utile, et le rerankeur léger a fait en sorte que la section de politique attendue apparaisse de manière fiable en premier. C’est exactement le genre de petit comportement de système que je veux que le tutoriel mette en évidence au lieu de le masquer.

## 12. Et ensuite

L’amélioration suivante est de comparer ce montage local avec une version Azure gérée du même scénario d’assistant politique scolaire. Conserver le scénario fixe devrait faciliter la visualisation des compromis : complexité de configuration, contrôles de récupération, intégration d’identité, propriété opérationnelle et coût.

## 13. Références

- [Introduction rapide au client Python Qdrant](https://python-client.qdrant.tech/quickstart.html)
- [Référentiel GitHub du client Qdrant](https://github.com/qdrant/qdrant-client)
- [Modèles supportés par FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Guide des embeddings OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Fiche modèle BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Fiche modèle BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Fiche modèle sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Page du modèle Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Documentation Ollama Windows](https://docs.ollama.com/windows)
- [Documentation Ollama API streaming](https://docs.ollama.com/api/streaming)
- [Fiche modèle Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Présentation de LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Introduction à RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Précédent : [Série 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->