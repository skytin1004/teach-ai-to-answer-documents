# Carnets

Ces carnets accompagnent la série d'articles avec des exemples exécutables.

| Carnet | Article | Objectif |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Série 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG open-source avec FastEmbed, Qdrant en mode local, recherche, reranking, génération Ollama optionnelle, et références aux sources |

## Exécuter localement

Installez les dépendances pour le carnet que vous souhaitez exécuter :

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ou installez toutes les dépendances :

```powershell
python -m pip install -r requirements\all.txt
```

## Vérifier

Depuis la racine du dépôt :

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

La Série 2 peut lire la configuration Ollama depuis un fichier `.env` à la racine du dépôt. Commencez par [../.env.example](../../../.env.example), qui est organisé par série.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->