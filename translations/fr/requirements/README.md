# Exigences

Chaque article d'implémentation possède un fichier d'exigences ciblé.

| Fichier | Utilisé par |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Carnet RAG open-source de la Série 2, incluant des aides facultatives pour la génération Ollama |
| [all.txt](../../../requirements/all.txt) | Vérification au niveau du dépôt et CI |

Utilisez le fichier ciblé lors de l'exécution d'un seul carnet. Utilisez `all.txt` lors de la validation de l'ensemble du dépôt.

`open-source-rag.txt` et `all.txt` incluent `fastembed` pour les embeddings locaux et `python-dotenv` afin que la Série 2 puisse activer facultativement la génération Ollama à partir du `.env` sans modifier le pipeline de récupération.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->