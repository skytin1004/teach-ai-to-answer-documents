# Liste de contrôle de publication

Utilisez cette liste de contrôle avant de valider ou de pousser des mises à jour publiques.

## Sécurité

- Confirmez qu’aucune clé API, jeton, mot de passe ou point de terminaison privé n’est écrit dans les fichiers Markdown, notebooks, données d’exemple ou scripts.
- Gardez les identifiants dans des variables d’environnement ou des identités gérées, pas dans les fichiers validés.
- Ne validez pas les fichiers `.env` ni les fichiers de sortie de notebooks exécutés.
- Gardez `.env.example` uniquement comme espace réservé.

## Vérification

Exécutez le script de vérification du dépôt :

```powershell
python scripts\verify_notebooks.py
```

Exécutez l’exécution complète locale et sécurisée du notebook avant de publier des modifications d’implémentation :

```powershell
python scripts\verify_notebooks.py --execute
```

Vérifications attendues :

- les liens Markdown locaux passent
- la validation JSON du notebook passe
- les notebooks ne contiennent pas de sorties sauvegardées ni de comptes d’exécution
- le scan de motifs secrets à haut risque passe
- les notebooks publics s’exécutent localement
- le matériel en brouillon sous `drafts/` est intentionnellement ignoré

## Revue

- Confirmez que les liens des articles README pointent vers les fichiers prévus.
- Confirmez que chaque article dispose de la navigation du dépôt et des liens vers les notebooks associés.
- Confirmez que les brouillons ne sont pas liés depuis les index publics à moins qu’ils ne soient prêts à être publiés.
- Confirmez que les modèles d’issues et de pull requests GitHub correspondent toujours au workflow du dépôt.
- Confirmez que les résultats de vérification dans l’article correspondent à la dernière sortie du notebook.
- Confirmez que le workflow GitHub Actions doit s’exécuter après la poussée.
- Confirmez que `CHANGELOG.md` reflète la mise à jour publiée.
- Confirmez que `CONTRIBUTING.md` correspond toujours au workflow du dépôt.

## Git

- Passez en revue `git status --short --branch`.
- Passez en revue `git diff --stat`.
- Validez et poussez uniquement lorsque vous êtes explicitement prêt.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->