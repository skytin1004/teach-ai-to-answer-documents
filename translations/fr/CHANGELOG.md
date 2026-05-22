# Journal des modifications

## Non publié

Portée de la première version publique pour **Enseigner à l'IA à répondre aux questions basées sur vos documents**.

### Ajouté

- Article de la série 1 sur les décisions d'architecture RAG, les compromis Azure vs open-source, et où s'insère l'affinage.
- Article et cahier de la série 2 pour un flux de travail RAG open-source local utilisant Qdrant en mode local, FastEmbed embeddings locaux, reranking léger, Ollama, et Phi-4-mini.
- Format tutoriel pas à pas de bout en bout de la série 2 avec extraits Python et notes de vérification issues du cahier exécuté.
- Chemin optionnel de génération de réponses de la série 2 avec Ollama et Phi-4-mini tout en conservant la récupération locale adaptée au CPU comme chemin par défaut.
- Vérification locale Ollama de la série 2 utilisant `phi4-mini:3.8b` sur GPU RTX 3060 Laptop.
- Données d'exemple pour la politique scolaire et l'orientation IA des cours.
- Fichiers de dépendances pour le cahier public et la vérification au niveau du dépôt.
- Script de vérification du dépôt pour les liens Markdown locaux et la validation/exécution des cahiers.
- Workflow GitHub Actions pour la vérification des cahiers.
- `.env.example` pour la configuration optionnelle de génération locale Ollama sans valider la configuration locale.
- Fichiers README au niveau des dossiers pour articles, cahiers, dépendances, données d'exemple et scripts.
- Check-list de publication pour sécurité publique et vérification.
- Espace de travail brouillon pour futur contenu Azure et évaluation.

### Vérifié

- Validation des liens Markdown locaux réussie.
- Cahier de la série 2 validé avec succès.
- Cahier de la série 2 exécuté avec succès dans l'environnement de vérification local.
- Les fichiers de cahier sont conservés sans sorties enregistrées ni compteurs d'exécution.
- Aucun secret réel n'est validé.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->