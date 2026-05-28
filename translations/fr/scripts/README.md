# Scripts

Ce dossier contient des scripts de vérification du dépôt.

## `verify_notebooks.py`

Valide les liens Markdown locaux, le JSON des notebooks, la propreté des sorties de notebooks, et les motifs de secrets à haut risque :

```powershell
python scripts\verify_notebooks.py
```

Exécute tous les notebooks publics sans risque local :

```powershell
python scripts\verify_notebooks.py --execute
```

Le workflow GitHub Actions utilise le même script.

Le matériel en brouillon sous `drafts/` est ignoré jusqu’à ce qu’il soit prêt pour l’index public.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->