# Enseigner à l'IA à répondre aux questions basées sur vos documents

![Vue d'ensemble du système RAG AI basé sur les documents](../../assets/images/readme-hero.svg)

Ce dépôt rassemble une série de blogs de 2026 sur la construction de systèmes d'IA basés sur les documents avec RAG, les services Azure AI, les alternatives open source et les flux de travail orientés évaluation.

## Contexte

En 2023, j'ai travaillé sur une paire de tutoriels visant à enseigner à ChatGPT comment répondre aux questions à partir de documents PDF en utilisant Azure AI Search et Azure OpenAI. L'idée de "ChatGPT sur vos données" semblait encore nouvelle à l'époque, et l'objectif était de montrer un flux de travail pratique : stocker des documents, les indexer, récupérer le contenu pertinent et générer des réponses à partir de ce contexte récupéré.

En 2026, l'écosystème RAG est bien plus vaste. Azure AI Search prend en charge des modèles modernes de recherche vectorielle et hybride, Azure OpenAI fait partie de l'écosystème plus large des modèles Microsoft Foundry, et des outils open source tels que LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama et vLLM sont devenus des choix pratiques pour des systèmes réels.

C’est pourquoi j’ai voulu revisiter ce sujet. La question n’est plus seulement "Comment construire un RAG ?" Il existe désormais de nombreuses façons de le construire, et la question la plus importante est "Quelle architecture devrais-je choisir pour ma situation ?"

Cette série commence par cette couche de prise de décision, puis se transforme en tutoriels pratiques. Le premier chemin d'implémentation construit un système RAG open source local que tout un chacun peut exécuter avec des données d’exemple, Qdrant, Ollama et Phi-4-mini.

## Articles

Voir [articles/README.md](./articles/README.md) pour l’index des articles.

1. [Série 1 : RAG, Azure vs alternatives open source, et quand le fine-tuning a du sens](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Série 2 : Construire un système RAG open source local de bout en bout](./articles/series-2-open-source-rag-end-to-end.md)

À venir :

- Reconstruire le même système RAG avec Azure AI Search et Azure OpenAI.
- Ajouter une évaluation et des vérifications de régression au-delà d’une réponse démo.

## Carnets (Notebooks)

Les articles d’implémentation utilisent des carnets pour que les étapes de recherche et d’évaluation puissent être inspectées directement. Voir [notebooks/README.md](./notebooks/README.md) pour des indications au niveau du dossier.

> [!TIP]
> Commencez par la Série 2 si vous voulez le chemin le plus rapide. Elle s’exécute localement avec des données d’exemple, des embeddings compatibles CPU, le mode local de Qdrant et sans informations d’identification cloud.

| Série | Carnet | Prérequis | Vérification locale |
| --- | --- | --- | --- |
| Série 2 | [Carnet RAG open source](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Mode local de Qdrant, recherche, reranking et gestion des sources vérifiés |

Pour exécuter un carnet localement, créez un environnement virtuel et installez le fichier de dépendances correspondant. Par exemple :

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Données d’exemple

Les carnets utilisent un petit corpus local dans [sample_data](../../sample_data) pour que les exemples puissent s’exécuter sans documents privés ni informations d’identification cloud. Voir [sample_data/README.md](./sample_data/README.md) pour plus de détails.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Résumé de la Vérification Locale

Les résultats de vérification sont consignés dans chaque article et dans [SERIES_PLAN.md](./SERIES_PLAN.md).

| Domaine | Résultat |
| --- | --- |
| Chemin open source Série 2 | FastEmbed a généré des embeddings locaux de dimension 384, la collection mémoire de Qdrant a inséré 8 vecteurs, le reranking léger a récupéré la section attendue ; la génération optionnelle Ollama avec `phi4-mini:3.8b` est complétée |

Le carnet local évite intentionnellement les secrets codés en dur.

## Génération Locale Ollama

Le carnet de la Série 2 est sécurisé localement par défaut. Pour activer la génération Ollama locale, copiez [.env.example](../../.env.example) en `.env` et remplissez les valeurs de la Série 2.

Pour la génération Ollama Série 2, décommentez :

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Le carnet Série 2 charge automatiquement `.env` depuis la racine du dépôt grâce à `python-dotenv`.

> [!IMPORTANT]
> Ne pas committer les fichiers `.env`, les clés API, les points de terminaison privés ni les valeurs spécifiques aux locataires. Le dépôt garde intentionnellement les secrets hors des fichiers Markdown et des carnets.

Les fichiers de dépendances sont documentés dans [requirements/README.md](./requirements/README.md).

Pour valider les liens, la structure des carnets, la propreté de la sortie des carnets et les patrons de secrets à haut risque :

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Les scripts de vérification sont documentés dans [scripts/README.md](./scripts/README.md).

Pour exécuter tous les carnets compatibles localement dans le même environnement :

```powershell
python scripts\verify_notebooks.py --execute
```

Le même flux de vérification s’exécute dans GitHub Actions lors de push, pull request et déclenchements manuels de workflow. Les articles et carnets en brouillon sont volontairement exclus du chemin de vérification publique.

Avant de publier des mises à jour, utilisez [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Voir [CHANGELOG.md](./CHANGELOG.md) pour le résumé actuel des modifications non publiées.

Pour les directives de contribution et d’hygiène des carnets, voir [CONTRIBUTING.md](./CONTRIBUTING.md).

## Support Multilingue

### Pris en charge via Co-op Translator (Automatisé et Toujours à Jour)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabe](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgare](../bg/README.md) | [Birman (Myanmar)](../my/README.md) | [Chinois (Simplifié)](../zh-CN/README.md) | [Chinois (Traditionnel, Hong Kong)](../zh-HK/README.md) | [Chinois (Traditionnel, Macao)](../zh-MO/README.md) | [Chinois (Traditionnel, Taïwan)](../zh-TW/README.md) | [Croate](../hr/README.md) | [Tchèque](../cs/README.md) | [Danois](../da/README.md) | [Néerlandais](../nl/README.md) | [Estonien](../et/README.md) | [Finnois](../fi/README.md) | [Français](./README.md) | [Allemand](../de/README.md) | [Grec](../el/README.md) | [Hébreu](../he/README.md) | [Hindi](../hi/README.md) | [Hongrois](../hu/README.md) | [Indonésien](../id/README.md) | [Italien](../it/README.md) | [Japonais](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coréen](../ko/README.md) | [Lituanien](../lt/README.md) | [Malais](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Népalais](../ne/README.md) | [Pidgin Nigérian](../pcm/README.md) | [Norvégien](../no/README.md) | [Persan (Farsi)](../fa/README.md) | [Polonais](../pl/README.md) | [Portugais (Brésil)](../pt-BR/README.md) | [Portugais (Portugal)](../pt-PT/README.md) | [Pendjabi (Gurmukhi)](../pa/README.md) | [Roumain](../ro/README.md) | [Russe](../ru/README.md) | [Serbe (Cyrillique)](../sr/README.md) | [Slovaque](../sk/README.md) | [Slovène](../sl/README.md) | [Espagnol](../es/README.md) | [Swahili](../sw/README.md) | [Suédois](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamoul](../ta/README.md) | [Telugu](../te/README.md) | [Thaï](../th/README.md) | [Turc](../tr/README.md) | [Ukrainien](../uk/README.md) | [Ourdou](../ur/README.md) | [Vietnamien](../vi/README.md)

> **Préférez cloner localement ?**
>
> Ce dépôt inclut plus de 50 traductions de langues ce qui augmente considérablement la taille du téléchargement. Pour cloner sans les traductions, utilisez le sparse checkout :
>
> **Bash / macOS / Linux :**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows) :**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Cela vous donne tout ce dont vous avez besoin pour suivre le cours avec un téléchargement beaucoup plus rapide.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->