# Documentation

- Modifier le contenu éditorial dans `guide.md`. Conserver les ancres existantes de `translations/sections.json`.
- Traiter les sections listées par `python3 scripts/docs.py worklist` avec le glossaire et mettre à jour leurs manifestes avec `scripts/docs.py record`.
- Exécuter `scripts/build` avant intégration. Ne pas versionner `_site/`.
