# Scala Agentic Engineering

Documentation Jekyll et Just the Docs du [guide français](guide.md). L’accueil public ouvre la version anglaise. Les URL des chapitres suivent `/<lang>/ch-<numéro>/`, par exemple `/en/ch-7a/`. Les six préfixes sont `en`, `fr`, `es`, `pt`, `it` et `de`.

## Aperçu local

Installer Ruby avec la version de [`.ruby-version`](.ruby-version), Bundler avec la version de [`Gemfile.lock`](Gemfile.lock), Python 3.10 ou plus récent et Node.js 20 ou plus récent.

```sh
bundle install
PAGES_URL=http://localhost:8000 PAGES_BASEURL='' scripts/build
python3 -m http.server 8000 --directory _site
```

Ouvrir [l’aperçu local](http://localhost:8000). Relancer `scripts/build` après édition. La commande exécute les tests, contrôle les traductions, construit avec `JEKYLL_ENV=production`, crée les index de recherche à partir du HTML et vérifie les pages rendues. En l’absence de variables `PAGES_URL` et `PAGES_BASEURL`, elle utilise l’URL du projet GitHub Pages.

## Mettre à jour le guide

1. Modifier [`guide.md`](guide.md). Les H1 numérotés qui suivent la séquence des chapitres ouvrent une page. Les sous-titres et les blocs clôturés restent dans leur chapitre.
2. Lancer `python3 scripts/docs.py sync` si des titres ont été ajoutés. Lors d’un renommage, modifier d’abord la clé correspondante dans [`translations/sections.json`](translations/sections.json) en conservant sa valeur. Lors d’une suppression, conserver l’entrée afin de réserver son ancre.
3. Lancer `python3 scripts/docs.py worklist`. Chaque ligne indique la langue, le chapitre, le statut et les identifiants à traiter. Les filtres `--lang de --chapter ch-7a` permettent d’attribuer une tâche précise.
4. Mettre à jour `translations/<lang>/<chapitre>.md`. Conserver les marqueurs `<!-- section: ID -->` et leur ordre. Retirer les sections supprimées. Utiliser le [glossaire](translations/GLOSSARY.md) et vérifier les passages modifiés contre la source française.
5. Enregistrer les sections relues avec `python3 scripts/docs.py record --lang de --chapter ch-7a --sections chapter s-1`. Omettre `--sections` pour enregistrer tout le chapitre et supprimer les entrées de manifeste des sections déjà retirées du fichier traduit. Si un chapitre entier disparaît, supprimer son Markdown et son manifeste dans chaque langue.
6. Lancer `scripts/build` avant de proposer la modification. Les brouillons de traduction initiaux ont été produits localement et demandent une relecture technique et linguistique.

### Identifiants et manifestes

`translations/sections.json` associe chaque titre français et son niveau à une ancre stable dans son chapitre. `next` est le prochain numéro disponible. Les ancres des titres principaux sont `guide` et `chapter`. Les sous-sections portent des identifiants `s-1`, `s-2`, etc., identiques dans les six langues.

À côté de chaque chapitre traduit, le manifeste JSON associe chaque ID à `source_sha256` et `translation_sha256`. Les deux empreintes SHA-256 couvrent les octets UTF-8 de la section correspondante, sans le marqueur. La validation signale les sections manquantes, supprimées, obsolètes, modifiées sans enregistrement, hors ordre ou structurellement divergentes. Elle compare les blocs clôturés, le code en ligne, les destinations, les valeurs numériques, les titres, listes, citations et tableaux. La traduction et sa relecture se font en dehors de la CI.

### Répartir les traductions entre Codex et Claude Code

Depuis une branche qui contient le même état de `guide.md`, attribuer des couples langue/chapitre disjoints. Donner à chaque session les IDs du worklist, le glossaire et les conventions du manifeste. Par exemple :

```sh
git worktree add -b docs/es-ch-7a ../scala-codex
git worktree add -b docs/de-ch-7a ../scala-claude
```

Ouvrir Codex dans `../scala-codex` et Claude Code dans `../scala-claude`. Demander à chaque session de modifier uniquement son Markdown et son manifeste, puis de contrôler son lot avec `worklist --lang … --chapter …`. Intégrer les deux branches et exécuter la validation complète sur leur résultat combiné.

## Publication GitHub Pages

Avant publication, confirmer que le contenu, les attributions et les licences permettent sa diffusion. Dans les paramètres du dépôt, ouvrir **Pages**, puis choisir **GitHub Actions** comme source. Après intégration sur `main`, le workflow construit et valide le site puis déploie l’artefact dans l’environnement `github-pages`. Les pull requests exécutent la validation sans déploiement. Le code HTML de sortie reste hors du dépôt.

Un domaine personnalisé peut être configuré dans **Settings → Pages**. Le workflow lit l’origine et le préfixe effectifs de Pages. [Configuration officielle des workflows GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
