# Enseigner à l’IA à répondre aux questions à partir de vos documents - Plan de la série

Ce plan suit la sortie publique de la Série 1 et de la Série 2. Les travaux ultérieurs sur Azure et l’évaluation sont conservés sous forme de brouillons jusqu’à ce que les exemples soient entièrement bout à bout et vérifiés.

Ne pas valider ni pousser de modifications tant qu’on ne vous l’a pas explicitement demandé.

## Portée publique

Sortie publique actuelle :

- Article de la Série 1 : décisions d’architecture RAG, compromis Azure vs open-source, et où s’insère le fine-tuning.
- Article de la Série 2 : tutoriel local RAG open-source.
- Notebook de la Série 2 : laboratoire local RAG exécutable avec FastEmbed, Qdrant, Ollama, et Phi-4-mini.
- Données d’exemple : fichiers Markdown de politique scolaire et directives IA de cours.

Brouillons, mais pas encore dans l’index public :

- Reconstruction Azure AI Search et Azure OpenAI.
- Évaluation RAG et contrôles de régression.

## Scénario du tutoriel

Le scénario partagé est un assistant de politique scolaire.

L’assistant répond à cette question à partir de documents locaux :

```text
Can I use generative AI for my final assignment?
```
  
Le comportement attendu est :

1. Charger les documents Markdown locaux.  
2. Les analyser et les découper par titres.  
3. Créer des embeddings locaux et stocker des représentations interrogeables avec métadonnées.  
4. Récupérer la section de politique pertinente.  
5. Reclasser si nécessaire.  
6. Générer ou composer une réponse étayée.  
7. Retourner les citations.  
8. Enregistrer les résultats de vérification.

## Structure publique actuelle

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```
  
Le matériel en brouillon est stocké sous `drafts/` et est ignoré lors de la vérification du dépôt jusqu’à ce qu’il soit prêt pour l’indexation publique.

## Vérification Série 2

Vérifié sur Windows avec Python 3.12.6.

- Installation réussie de `requirements/open-source-rag.txt`.  
- Exécution de `notebooks/series-2-open-source-rag.ipynb` avec `nbclient`.  
- Vérification locale réussie : 2 documents d’exemple chargés, 8 segments créés, FastEmbed a généré des embeddings locaux de dimension 384, la collection en mémoire Qdrant initialisée, 8 vecteurs insérés.  
- Question test : « Puis-je utiliser l’IA générative pour mon devoir final ? »  
- Source la plus pertinente après reclassification légère : `school_ai_policy.md`.  
- Section la plus pertinente après reclassification légère : `Final Assignments`.  
- Chemin de réponse par défaut : compositeur de réponses transparent local.  
- Ollama installé via winget ; `phi4-mini:3.8b` téléchargé avec succès.  
- Chemin de génération de réponse Ollama : complété avec `phi4-mini:3.8b`.  
- Taille du fichier modèle Ollama : environ 2,49 Go sur disque.  
- Taille du modèle Ollama chargé : 3,3 Go rapportée par `ollama ps`.  
- Déchargement GPU : 100% GPU rapporté par `ollama ps` sur RTX 3060 Laptop GPU.  
- Mémoire GPU observée après génération : environ 3,5 Go sur 6 Go.  
- Exécution du notebook avec modèle FastEmbed mis en cache et génération Ollama activée réussie en environ 34 secondes via le script de vérification.  
- Observation : un passage précoce de chargement de documents incluait accidentellement `sample_data/README.md` ; le notebook charge désormais explicitement seulement les deux documents d’exemple prévus.

## Vérification du dépôt

- `scripts/verify_notebooks.py` valide les liens Markdown locaux, le JSON du notebook, la propreté des sorties du notebook, et les motifs secrets à haut risque.  
- `scripts/verify_notebooks.py --execute` exécute les notebooks publics depuis la racine du dépôt.  
- Le matériel en brouillon sous `drafts/` est intentionnellement ignoré.

## Travaux suivants

- Reconstruire le même scénario avec Azure AI Search et Azure OpenAI dans une future partie de la série.  
- Ajouter la récupération et l’évaluation des réponses une fois que les implémentations locales et Azure seront toutes deux stables.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->