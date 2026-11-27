# Guide ultime du développeur senior Scala utilisant les LLMs

# 1. Principe directeur

Pour un dev senior Scala, l'objectif n'est pas de “coder plus vite”, mais de maximiser ce ratio :

```text
Changements utiles déployés et stables
÷
(diffs inutiles + retours review + bugs + crédits brûlés + temps humain)
```

Le bon modèle mental :

```text
Toi = tech lead et arbitre final
IntelliJ = vérité structurelle Scala/JVM et poste de contrôle
JetBrains AI = assistance inline et actions IDE à faible friction
Codex = agent principal d'exécution pour les issues standard + reviewer indépendant quand Claude écrit
Claude Code = agent principal de raisonnement/debug/architecture + reviewer indépendant quand Codex écrit
Qwen local = assistant économique
GitHub Copilot = couche GitHub-native pour issues, PR et review automatique
Aider = petit diff propre orienté Git
MCP + Sourcebot + Context7 = contexte ciblé
RTK + Headroom = réduction du bruit
Jev = decision layer probabiliste pour classifier, scorer et router — jamais un coding model ni un gate critique seul
GPT‑6 Luna / GPT‑6.2 Sol / GPT‑6.2 Astra = route Codex selon micro-boucle, agentique et frontier
Haiku 5.5 / Sonnet 5.5 / Opus 5.5 / Fable 5.2 = route Claude selon volume, contrôle humain et autonomie
Tests + Stryker4s + CI = juges finaux (déterministes)
```

---

# 1A. Vibe coding, AI-assisted coding et agentic coding

Le terme **vibe coding**, popularisé par Andrej Karpathy en février 2025, décrivait à l'origine une pratique où le
programmeur délègue presque entièrement l'écriture du code, accepte les propositions du modèle et raisonne surtout par
résultat observable. Cette approche est efficace pour un prototype jetable, une exploration ou une interface sans enjeu.
Ce n'est pas une méthode de production suffisante pour un système métier, financier, sécurisé ou durable.

Deux précisions d'attribution stabilisent le débat en 2026. Karpathy a lui-même précisé que le tweet était à moitié une
plaisanterie et visait des projets jetables du week-end — il n'a jamais proposé le vibe coding comme méthode de
production. Et Simon Willison a posé dès février 2025 la frontière de référence : accepter les diffs sans les lire,
c'est du vibe coding ; relire chaque ligne en comprenant ce qu'elle fait, c'est de l'AI-assisted programming — le
problème n'est pas l'IA, c'est l'absence de relecture. Le vocabulaire s'est complété fin 2025 avec le **vibe
engineering** : des professionnels expérimentés qui accélèrent massivement avec des agents LLM tout en restant
pleinement responsables du logiciel produit. La différence entre les deux « vibes » n'est pas l'outil, c'est la
relecture, les tests et la responsabilité — c'est exactement la cible de ce guide.

Il faut distinguer trois modes de travail :

| Mode                        | Contrôle humain                                                     | Usage adapté                                     | Risque principal                                           |
|-----------------------------|---------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------|
| **Vibe coding**             | Faible, validation par sensation et exécution                       | Prototype, spike, outil personnel jetable        | Dette invisible, sécurité, compréhension perdue            |
| **AI-assisted engineering** | Le développeur conçoit et relit, le modèle accélère                 | Travail quotidien sur code maintenu              | Automatiser des décisions qui devraient rester humaines    |
| **Agentic coding**          | L'agent explore, planifie, modifie et teste dans un périmètre borné | Tâches bien spécifiées avec tests et permissions | Dérive, boucle, action hors périmètre, injection indirecte |

Pour un senior Scala, la cible n'est donc pas « davantage de vibe coding », mais une **ingénierie agentique contrôlée
** :

```text
spécification vérifiable
→ contexte minimal mais suffisant
→ plan
→ permissions proportionnées
→ exécution instrumentée
→ compile et tests déterministes
→ review indépendante
→ validation humaine
```

**Evidence-driven agentic engineering** : le SDD fixe le contrat, le harness engineering rend ses contraintes
exécutables, et les preuves déterminent si le changement peut avancer. Pour chaque exigence, associe une preuve
indépendante (test de comportement, inspection, benchmark ou mesure runtime), le SHA réellement validé et les
risques non couverts. Une affirmation de l'agent, une review sans preuve ou un simple statut vert ne constituent
pas un oracle. Le cycle se termine après validation de l'artefact déployé, pas simplement au merge (section 15B).

## Ce que montre l'état de l'art en 2026

1. **Le modèle seul ne détermine pas la réussite.** Le harness, les outils disponibles, le debugger, la qualité du
   contexte et les tests peuvent modifier les résultats presque autant que le choix du modèle. Les comparaisons entre
   scores publiés par des fournisseurs ne sont valides que si le harness, l'effort, les outils et le protocole sont
   comparables.
2. **Les benchmarks courts surestiment l'autonomie longue.** Les agents obtiennent de bons résultats sur des issues
   isolées, mais chutent fortement sur les évolutions multi-fichiers, longues et historiques. SWE-EVO, par exemple, vise
   des tâches beaucoup plus longues que SWE-bench et met en évidence cet écart.
3. **SWE-bench Verified n'est plus un bon étalon unique.** OpenAI a documenté des problèmes de contamination et de tests
   défectueux. Pour le code, préfère un portefeuille comprenant des tâches SWE-bench auditées, Terminal-Bench, des tâches de review et
   surtout un benchmark interne Scala non public.
4. **La productivité humaine n'est pas garantie par un bon score agentique.** Une étude randomisée de METR sur des
   développeurs expérimentés dans leurs propres dépôts observait un ralentissement avec les outils de début 2025. Les
   données recueillies ensuite suggèrent une amélioration possible, mais METR juge le nouvel essai non fiable à cause de
   biais de sélection et de mesures difficiles avec plusieurs agents concurrents. Il n'existe donc pas encore de
   réplication causale propre avec les outils de 2026. La mesure locale du temps jusqu'au merge reste indispensable.
   Ordre de grandeur de la mise à jour de février 2026 : estimation ponctuelle d'environ 18 % d'accélération sur la
   sous-cohorte historique (intervalle de confiance −38 % à +9 %) et d'environ 4 % sur les nouveaux participants (IC
   −15 % à +9 %) — un signal trop bruité pour conclure, que METR a préféré traiter en refondant le protocole plutôt
   qu'en publiant un chiffre unique. Détail décisif pour le pilotage : dans l'essai initial, les participants estimaient
   en moyenne avoir été ~20 % plus rapides grâce à l'IA alors qu'ils étaient ~19 % plus lents — l'écart entre perception
   et mesure est la raison pour laquelle ce guide exige des métriques locales (coût par changement accepté, temps
   jusqu'au merge) plutôt que le ressenti des sessions.
5. **Les instructions de dépôt sont utiles seulement si elles sont opérationnelles.** Les recherches sur `AGENTS.md`
   trouvent un bénéfice lorsque le fichier contient commandes, conventions non standard, invariants et règles d'arrêt.
   Une longue description générique de l'architecture peut augmenter le contexte sans améliorer le résultat.
6. **Le multi-agent n'est pas un multiplicateur automatique d'intelligence.** Il aide lorsque les sous-tâches sont
   réellement indépendantes, que les responsabilités et fichiers sont séparés et qu'un agent racine synthétise. Sur un
   état mutable partagé, il augmente conflits, coût et erreurs de coordination.
7. **Un patch techniquement correct ne suffit pas à évaluer un agent.** Mesure aussi le respect du scope, des règles
   d'arrêt et des conventions, la qualité du plan, la capacité à signaler l'incertitude et le coût de review humaine.
   Deux agents qui passent les mêmes tests peuvent avoir une valeur très différente si l'un génère deux fois plus de
   rework ou de changements hors périmètre.
8. **La mémoire, les skills et les règles persistantes deviennent une surface d'ingénierie.** Les agents capables de
   faire évoluer leur propre mémoire, leurs skills ou leur routage ne doivent jamais auto-promouvoir ces changements.
   Toute évolution persistante doit être diffable, versionnée, testable, reviewée et réversible avant activation.
9. **Une grande fenêtre de contexte ne supprime pas le *context rot*.** Les évaluations 2026 distinguent la capacité
   physique de la fenêtre et la qualité effective d'utilisation de son contenu : à tâche identique, davantage de tokens
   peuvent dégrader récupération, respect des contraintes et raisonnement bien avant la limite maximale. Le bon objectif
   n'est donc pas « remplir 1M tokens », mais maintenir un **working set minimal et décisionnel**. Les sous-agents
   isolés sont une parade structurelle : ils consomment localement beaucoup de contexte et ne renvoient au parent qu'un
   résultat condensé.

Conclusion : le niveau frontier augmente la surface de tâches possibles, mais la qualité de l'ingénierie autour de
l'agent reste le facteur contrôlable le plus important.

### Complément méthodologique

> **SWE-bench Pro ne remplace pas à lui seul SWE-bench Verified.** OpenAI estime désormais qu'environ 30 % des tâches de
> SWE-bench Pro sont elles aussi défectueuses : tests trop stricts, exigences cachées absentes du prompt, couverture
> insuffisante ou consigne trompeuse. L'audit du 8 juillet 2026
> (pipeline automatisée : 27,4 % des 731 tâches publiques marquées ; annotation par cinq ingénieurs seniors : 34,1 %)
> a d'ailleurs conduit OpenAI à **retirer explicitement sa recommandation** d'en faire l'évaluation de codage de
> référence — un signal plus fort que la seule estimation. Le bon portefeuille d'évaluation combine donc plusieurs axes
> plutôt qu'un nouveau
> classement unique.

| Axe à mesurer                | Évaluation utile                 | Ce qu'elle révèle                                                                               |
|------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------|
| Correctif de dépôt classique | SWE-bench, avec audit des tâches | Capacité de réparation sur issues isolées                                                       |
| Tâche originale longue       | **DeepSWE**                      | Contamination réduite, vérificateurs écrits pour accepter plusieurs solutions valides           |
| Collaboration itérative      | **SWE-Interact** ou SWE-Together | Découverte d'intention, mémorisation des contraintes, besoin de corrections humaines            |
| Exploration de dépôt         | **SWE-Explore**                  | Localisation au niveau des lignes et efficacité du contexte                                     |
| Cycle complet                | **SWE-Cycle**                    | Reconstruction d'environnement, implémentation et génération de tests dans une même trajectoire |
| Réalité de ton travail       | **Benchmark Scala privé**        | Coût et qualité sur Play, Pekko, Tapir, Spark, implicits, sérialisation et build réels          |

Pour une tâche de code, mesure le **coût par changement accepté** ; pour piloter la livraison, le **coût par changement déployé et stable** (section 15B), pas le taux de réussite brut :

```text
coût par changement accepté
= tokens + latence + minutes humaines + CI + reprises + défauts échappés
```

Utilise une unité commune pour agréger ces coûts (par exemple euros avec un coût horaire explicite), ou garde
les composantes séparées. Les tokens et les minutes ne s’additionnent pas directement. Pour le coût jusqu’à la
production, ajoute déploiement, validation runtime, rollback/hotfix et défauts observés pendant une fenêtre fixée
avant la mesure. Ne compte comme stable qu’un changement ayant terminé cette fenêtre.

Ne cherche pas une « productivité IA » globale. Stratifie au minimum les mesures par **greenfield, maintenance, legacy,
bugfix, migration, refactor et code critique** : les études 2026 obtiennent des résultats contradictoires précisément
parce qu'elles ne mesurent pas toujours les mêmes tâches, développeurs ni coûts de review.

### Un benchmark vert n'est pas encore un diff mergeable

Une évaluation METR menée sur 296 PRs générées par agents a constaté que le grader SWE-bench accordait en moyenne **24,2
points de réussite de plus** que les mainteneurs chargés d'évaluer si le changement était réellement utile et
mergeable ; environ la moitié des PRs qui passaient les tests n'auraient pas été mergées. L'échantillon ne porte que sur
trois dépôts, des modèles antérieurs à la génération la plus récente et un seul essai sans itération sur le feedback
mainteneur : ce n'est pas une limite fondamentale de capacité, mais cela invalide l'équivalence naïve
`tests du benchmark passants = changement acceptable`.

Sur les tâches longues, SlopCodeBench observe en outre une accumulation de duplication, de verbosité et d'érosion
structurelle à mesure que les checkpoints s'enchaînent. Un prompt demandant de la qualité réduit certains défauts au
début sans supprimer leur croissance. Le bon régime de preuve cumule donc quatre barrières indépendantes :

```text
contrat métier explicite
→ reproduction qui échoue avant le patch
→ tests déterministes, propriétés et mutation testing
→ review du diff, de son scope et de sa maintenabilité par un humain responsable
```

Les scores de benchmark servent au routage et aux expérimentations ; ils ne doivent jamais devenir une autorisation
d'autonomie ou de merge.

> **Écart entre écrire et livrer.** Le working paper NBER *Writing Code vs. Shipping Code* observe, sur plus de
> 500 000 développeurs GitHub, une hausse estimée de l’activité beaucoup plus forte pour les commits que pour les
> projets et les releases. L’étude reste observationnelle avec appariement : elle ne démontre pas un effet causal
> identique sur ton dépôt. Limite donc le WIP à la capacité de review et de livraison, et mesure jusqu’à la production.

### Garde-fou de production pour le vibe coding

Les études empiriques de 2026 sur des applications réellement « vibe codées » retrouvent des familles de défauts
récurrentes : logique provisoire laissée en production, entrées non filtrées, secrets exposés, oubli de contraintes au
fil des tours et optimisation locale qui dégrade le système global. Un modèle plus fort ou un meilleur prompt réduit ces
défauts, mais ne les élimine pas.

> **Ordres de grandeur mesurés en 2026.** L'audit de 200 applications réellement « vibe codées » et déployées
> (1 471 vulnérabilités validées) trouve au moins une vulnérabilité dans **90 % des dépôts**, dont plus des trois
> quarts de sévérité haute ou critique ; le contrôle d'accès cassé apparaît dans 75,5 % des dépôts, soit environ 20×
> la ligne de base OWASP 2025. Un scan indépendant de 1 400+ applications aboutit au même ordre de grandeur (65 %
> présentent au moins un problème de sécurité, 58 % au moins une vulnérabilité critique, 400+ secrets exposés).
> L'analyse des causes racines classe ces défauts en trois familles — **mémoire** (contraintes oubliées entre les
> tours), **objectif** (optimisation locale qui dégrade le système global) et **connaissance** (patterns dangereux
> reproduits) : exactement les trois mécanismes que les gates déterministes et la revue humaine de ce guide doivent
> interrompre, puisqu'aucun prompt ne les corrige durablement.

```text
Prototype vibe coding
→ aucune donnée ou clé de production
→ tests fonctionnels + sécurité + performance + maintenabilité
→ lecture humaine du diff et des dépendances
→ migration vers le workflow agentique contrôlé
→ seulement ensuite : déploiement
```

Une session de vibe coding ne doit jamais pousser directement en production, même lorsque la démonstration paraît
fonctionnelle. La frontière de production est un **changement de régime de preuve**, pas une simple étape suivante du
chat.

# 2. Stack recommandée

Avec **MacBook Pro 16" M5 Max, 18 cœurs CPU, 40 cœurs GPU, Neural Engine 16 cœurs, 128 Go de mémoire unifiée, SSD 8
To**, **IntelliJ Ultimate**, **Scala/Java/Play/Spark**, je choisirais cette stack :

| Couche                 | Outil                                                 | Rôle                                                                                                                                   |
|------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| IDE principal          | **IntelliJ Ultimate**                                 | Navigation, typage, refactor, debug, tests et poste de contrôle des agents                                                             |
| Assistance IDE         | **JetBrains AI**                                      | Code Completion, Next Edit Suggestions, AI Actions et petites transformations sans remplacer l'agent principal                         |
| Agent Claude principal | **Claude Code Max**                                   | Opus 5.5 `medium` pour agentic coding, architecture et debugging ; Sonnet 5.5 `medium` pour micro-dev ; Fable 5.2 en escalade frontier |
| Modèle local           | **Qwen3-Coder-Next / Qwen3.8-27B**                    | Coder-Next comme baseline rapide ; Qwen3.8-27B comme challenger quality-first à mesurer                                                |
| Harness local          | **Qwen Code ou OpenCode**                             | Qwen Code est désormais un harness agentique complet ; OpenCode reste une alternative à mesurer                                        |
| Agent Codex / reviewer | **Codex dans IntelliJ / ChatGPT Desktop / Codex CLI** | GPT‑6.2 Sol `Medium` pour l’ownership end-to-end ; GPT‑6 Luna `High` en micro-dev ; GPT‑6.2 Astra `Light`+ pour les tâches frontier      |
| GitHub workflow        | **GitHub Copilot**                                    | Issues → agent, PR, review automatique et corrections CI pour les repositories GitHub                                                  |
| Suivi de PR optionnel   | **Codex Goal mode / Heartbeats / Cloud ; Claude Code `/ship` / `/steward` / Cloud Auto-fix ; Claude Ship** | GPT‑6.2 Sol `Medium` pour le suivi Codex borné ; agents GitHub centralisés en équipe, sans remplacer la review croisée ni la CI |
| Petit diff             | **Aider**                                             | Modifications ciblées, git-first, boucle lint/test                                                                                     |
| IDE agent optionnel    | **JetBrains Junie / JetBrains AI**                    | Agent natif dans IntelliJ si tu veux rester dans l'UI                                                                                  |
| Recherche codebase     | **Sourcebot**                                         | Recherche multi-repos, symboles, usages, fichiers pertinents                                                                           |
| KnowledgeGraph         | **ScalaSemantic MCP / Codebase-Memory MCP**           | ScalaSemantic pour le graphe sémantique Scala ; Codebase-Memory pour le graphe structurel polyglotte Java/Kotlin                       |
| Decision layer         | **Jev 1.14**                                          | Décisions fermées à haute fréquence : classification, routing, skill selection, scoring et signal d’escalade                           |
| Docs à jour            | **Context7**                                          | Vérification API, frameworks, libs (anti-hallucination)                                                                                |
| Intégration agent IDE  | **JetBrains ACP + MCP**                               | ACP relie l'IDE aux agents ; MCP expose outils, contexte et actions IntelliJ                                                           |
| Optimisation tokens    | **RTK + Headroom**                                    | Réduction logs, diffs, outputs terminal                                                                                                |
| Routage API            | **OpenRouter**                                        | Accès ponctuel aux modèles alternatifs                                                                                                 |

Statut et maturité des outils :

| Outil                   | Statut                                           | Point de vigilance avant adoption                                                                                                                                  |
|-------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code             | Stable, outil officiel                           | Opus 5.5 est le modèle Opus courant pour l’agentic coding long ; Sonnet 5.5 est le tier rapide ; Agent Teams reste expérimental, Ultrareview en research preview   |
| Claude Ship             | Code Review GA ; Steward / Approvals en beta     | Service Team/Enterprise facturé séparément ; `/ship` et `/steward` locaux relèvent de l’usage Claude Code. Voir section 12.                                             |
| Codex post-PR           | Goal mode, Scheduled tasks, Cloud et Code Review officiels | Heartbeats selon surface ; permissions et quotas à vérifier ; Watch and Fix non confirmé ; pas de merge automatique. Voir section 12. |
| Claude Mods             | Disponible depuis Claude Code 2.1.287            | Extension JS/TS in-process ; très puissante mais non sandboxée : n’installer que du code audité et limiter son usage aux besoins que hooks/skills/MCP couvrent mal |
| Jev 1.14                | Early access ; API System One                    | Très bon candidat pour les décisions fermées ; seuils à calibrer par tâche, état minimal, jamais autorité finale sur une action critique                           |
| Qwen3-Coder-Next local  | Stable côté modèle                               | Sur 128 Go : Q4_K_M ≈ 48,4 Go confortable ; Q5_K_M ≈ 56,7 Go recommandé ; Q6_K ≈ 65,5 Go viable ; Q8_0 ≈ 84,8 Go à tester ponctuellement                           |
| OpenCode                | Actif, LSP partiellement exp.                    | Valider le LSP Metals sur ton repo avant standardisation                                                                                                           |
| Qwen Code               | Actif, alternative sérieuse                      | Auto-Memory/Skills, subagents, worktrees, MCP/LSP ; Agent Teams et Arena restent expérimentaux                                                                     |
| ChatGPT Desktop / Codex | App desktop ChatGPT, CLI, extension IDE et Cloud | Codex sait désormais piloter plusieurs sessions/agents ; plugins et permissions restent à auditer                                                                  |
| JetBrains Junie / CLI   | **Stable**, BYOK                                 | Option crédible, à départager par bake-off sur le dépôt Scala                                                                                                      |
| Aider                   | Stable, maintenu                                 | Discipline "peu de fichiers" indispensable                                                                                                                         |
| Sourcebot               | Stable                                           | Coût d'hébergement et d'indexation multi-repos                                                                                                                     |
| Context7                | Stable                                           | Couverture variable selon les libs Scala de niche                                                                                                                  |
| RTK                     | Stable                                           | Hooks PreToolUse à tester sur tes sorties sbt réelles                                                                                                              |
| Headroom                | **Expérimental**                                 | Tester sur logs/diffs non critiques uniquement                                                                                                                     |
| OpenRouter              | Stable                                           | Zéro infra ; idéal comme porte de sortie ponctuelle vers GLM/Kimi/Gemini/Grok et nouveaux modèles                                                                  |

JetBrains a deux niveaux MCP à distinguer : le support MCP côté AI Assistant existe depuis IntelliJ IDEA 2025.1 comme
client, et les IDE JetBrains exposent aussi un serveur MCP intégré depuis 2025.2 pour que des clients externes accèdent
aux outils de l'IDE. C'est particulièrement important pour Scala, où l'agent a besoin de symboles, types, modules,
inspections et run configurations, pas seulement de texte brut.

Depuis IntelliJ IDEA 2026.1 — qui a intégré Codex, Claude Agent et Junie, puis Cursor et GitHub Copilot via le registre
ACP public (ouvert fin janvier 2026), avec une gestion MCP par agent consolidée dans 2026.2 — ajoute une distinction de
protocole : **ACP (Agent Client Protocol) relie l'IDE au coding agent**, tandis que **MCP relie l'agent aux outils et au
contexte**. IntelliJ peut ainsi servir d'UI et de vérité structurelle tout en laissant Claude, Codex, Junie, GitHub
Copilot ou un autre agent ACP interchangeable. Chaque agent conserve son propre harness, ses modèles, son
authentification et ses permissions ; l'unité remplaçable n'est donc plus seulement le LLM, mais l'agent complet. Les
outils du serveur MCP IntelliJ peuvent être restreints par agent ; pour le debugging Scala/JVM, les outils debugger
exposés par le serveur MCP IntelliJ (outils préfixés
`xdebug_`, activables depuis la configuration du MCP Server) permettent de collecter stack, variables, threads et
preuves runtime sans injecter des `println` dans le code.

### Architecture IntelliJ 2026.2 recommandée

```text
IntelliJ IDEA
├── JetBrains AI
│   ├── Code Completion
│   ├── Next Edit Suggestions
│   └── AI Actions / petites transformations
├── Claude Code officiel
│   ├── plugin JetBrains / CLI
│   └── Claude Code Desktop
│       → abonnement Claude Max, agent principal sur raisonnement/debug/architecture
├── Codex
│   ├── agent ACP dans AI Chat
│   ├── ChatGPT Desktop / CLI
│   └── compte ChatGPT/OpenAI
│       → agent principal sur issues standard / reviewer croisé quand Claude écrit
└── GitHub Copilot
    └── couche GitHub-native : issues, PR, review automatique, CI
```

**ACP ne remplace pas les intégrations officielles.** Pour Claude, garde **Claude Code officiel** comme voie principale
lorsque tu veux exploiter l'abonnement Claude Max : le plugin JetBrains, le CLI et l'onglet Code de Claude Desktop
partagent le même harness Claude Code et ses règles (`AGENTS.md` en fallback ou `CLAUDE.md`, permissions, hooks, MCP,
skills). Claude Code Desktop ajoute plusieurs sessions isolées par worktrees, revue visuelle des diffs, terminal/éditeur
intégrés et suivi des PR. ACP reste surtout la couche d'interopérabilité qui permet à IntelliJ d'accueillir plusieurs
agents dans une UI commune.

Pour Codex, l'agent intégré à IntelliJ peut s'authentifier avec le **compte ChatGPT** ou une clé OpenAI. Avec une
authentification propre au fournisseur, l'usage de l'agent ne consomme pas les AI Credits JetBrains. Même logique pour
les autres agents ACP qui utilisent leur propre compte fournisseur. Les fonctions in-editor **Code Completion** et
**Next Edit Suggestions** ne consomment pas non plus le quota d'AI Credits. Un abonnement **JetBrains AI Ultimate (35 AI
Credits / 30 jours)** devient donc surtout un budget pour Junie, AI Chat et les fonctions cloud JetBrains ; il n'a pas à
financer le gros du développement agentique si Claude Code et Codex utilisent leurs abonnements respectifs.

À noter côté JetBrains en 2026 : **Codex est désormais intégré comme agent dans les IDE** aux côtés de Junie et Claude,
le registre ACP permet d'ajouter d'autres agents, et un système de **Skills** réutilisables complète MCP. L'IDE devient
ainsi un **control plane local** : navigation, diagnostics et debugger restent JetBrains, tandis que le writer ou le
reviewer peut être changé par session sans abandonner l'environnement Scala/JVM.

---

# 3. Répartition optimale des modèles

## Règle simple

```text
Qwen / Haiku préparent et filtrent.
Micro-dev sous fort contrôle humain → GPT‑6 Luna High ou Sonnet 5.5 Medium.
Agentic coding end-to-end → GPT‑6.2 Sol Medium ou Opus 5.5 Medium.
Debugging / architecture difficiles → Opus 5.5 High ou GPT‑6.2 Sol High.
Frontier ponctuel → GPT‑6.2 Astra Light ou Fable 5.2 Low avant de pousser aveuglément l'effort du modèle inférieur au maximum.
Un seul writer par worktree.
L'autre famille de modèles reviewe ou challenge, elle ne duplique pas automatiquement toute la trajectoire.
Ultra / multi-agent uniquement lorsque les sous-problèmes sont réellement indépendants.
IntelliJ valide.
Toi, tu décides.
```

Le routage doit minimiser le **coût de la tâche terminée**, pas le prix du premier appel :

```text
charge totale attendue
= découverte + implémentation + vérification
+ probabilité de reprise × coût de reprise
+ coût de coordination
```

Un modèle plus cher peut donc être le meilleur achat s'il évite une mauvaise exploration, plusieurs diffs inutiles et
des boucles de CI. À l'inverse, une micro-boucle contrôlée par un senior rend Luna, Sonnet ou Haiku dominants dès que
l'erreur est détectée en quelques minutes.

*Ne jamais déléguer la mise à jour des versions dans `build.sbt` sans exiger que l'agent interroge d'abord un MCP,
Context7, Maven Central ou la documentation officielle. Les noms et versions de bibliothèques sont exactement le type
d'information que les modèles hallucinent quand ils travaillent hors contexte.*

## Matrice de routage

| Tâche                                                    | Mode         | Agent principal recommandé                   | Second passage utile                           | Pourquoi                                                                           |
|----------------------------------------------------------|--------------|----------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------|
| Résumer un module, grep, usages, logs simples            | Micro-dev    | **Haiku 5.5** ou Qwen local                  | Aucun sauf ambiguïté                           | Lecture haute fréquence, faible risque                                             |
| Modification mécanique précise, boilerplate, renommage   | Micro-dev    | **GPT‑6 Luna High**                          | Sonnet 5.5 Medium si types subtils             | Très bon coût quand l'humain garde la direction                                    |
| Écrire un test simple à partir d'un comportement connu   | Micro-dev    | **GPT‑6 Luna High**                          | Sonnet 5.5 Medium si règle métier riche        | Sortie facilement vérifiable                                                       |
| Stack trace ou failure précise                           | Micro-dev    | **Sonnet 5.5 Medium**                        | Luna High pour appliquer un patch borné        | Sonnet apporte plus de compréhension sans payer Opus                               |
| Petit bug reproduit, périmètre connu                     | Micro-dev    | **Sonnet 5.5 Medium**                        | Luna High pour tests/édition mécanique         | Boucles courtes, feedback immédiat                                                 |
| Patch local, types ou invariants non triviaux            | Micro-dev    | **GPT‑6.1 Terra Medium**                     | GPT‑6.2 Sol Medium si exploration nécessaire  | Tier intermédiaire à mesurer sur les patchs bornés |
| Petit refactor local                                     | Micro-dev    | **Sonnet 5.5 Medium**                        | Luna High pour vérification mécanique          | Le senior conserve l'architecture                                                  |
| Review ciblée d'un petit diff                            | Vérification | **GPT‑6.2 Sol Light**                        | Sonnet 5.5 Medium si second avis utile         | Plus de jugement qu'un worker, sans payer une review agentique complète            |
| Issue standard complète, spec claire                     | Agentic      | **GPT‑6.2 Sol Medium**                       | **Opus 5.5 Medium** en review                  | Meilleur défaut Codex pour exploration → patch → tests → PR                        |
| Feature multi-fichiers normale                           | Agentic      | **GPT‑6.2 Sol Medium**                       | Opus 5.5 Medium en review                      | Ownership end-to-end avec coût contenu                                             |
| Feature complexe, plusieurs couches                      | Agentic      | **GPT‑6.2 Sol High**                         | Opus 5.5 Medium/High                           | Davantage de planification et vérification                                         |
| Architecture ou choix de migration                       | Agentic      | **Opus 5.5 High**                            | Sol Medium pour challenger le plan             | Le jugement domine la production de code                                           |
| Root cause inconnue / bug Scala subtil                   | Agentic      | **Opus 5.5 High**                            | Sol Medium/High pour hypothèse indépendante    | Comprendre le problème coûte plus que le patch                                     |
| Concurrence, async, flaky test difficile                 | Agentic      | **Opus 5.5 High**                            | Sol High si la première piste échoue           | Réduit le risque d'ancrage sur une fausse cause                                    |
| Migration / compatibilité publique                       | Agentic      | **GPT‑6.2 Sol High**                         | Opus 5.5 High en review conceptuelle           | Exécution disciplinée + second jugement indépendant                                |
| Gros refactor transversal                                | Agentic      | **Opus 5.5 High**                            | Sol Medium/High en review                      | Opus pour cohérence globale ; Sol pour casser les angles morts                     |
| Review normale d'une PR écrite par Codex                 | Vérification | **Opus 5.5 Medium**                          | Aucun sauf finding critique                    | Contexte frais et autre famille de modèles                                         |
| Review normale d'une PR écrite par Claude                | Vérification | **GPT‑6.2 Sol Medium**                       | Aucun sauf finding critique                    | Symétrie auteur/reviewer                                                           |
| Review architecture, invariants, cas limites             | Vérification | **Opus 5.5 High**                            | Astra Light si enjeu particulièrement élevé    | Chercher les erreurs conceptuelles plutôt que seulement relire le diff             |
| Sécurité, auth, contrat critique                         | Critique     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High comme reviewer                   | Acheter la capacité supérieure sans partir directement en effort extrême           |
| Problème très ambigu, jugement end-to-end                | Frontier     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High pour critiquer le plan           | La capacité de jugement compte davantage que la longueur du diff                   |
| Décision très difficile au milieu d'une tâche normale    | Advisor      | **Fable 5.2 Low**                            | Sol/Opus reste l'exécuteur                     | Acheter ponctuellement du jugement frontier sans transférer toute la tâche         |
| Sol High échoue par limite de capacité                   | Escalade     | **GPT‑6.2 Astra Light**                        | Medium/High seulement si nécessaire            | Changer de tier peut coûter moins qu'un Sol Extra High prolongé                    |
| Opus High échoue par limite de capacité                  | Escalade     | **Fable 5.2 Low**                            | Sol/Astra pour challenger                      | Même logique : frontier faible effort avant effort maximal inférieur               |
| Échec CI simple après implémentation correcte            | Reprise      | **GPT‑6 Luna High** ou **Sonnet 5.5 Medium** | Escalade seulement si problème conceptuel      | Ne pas payer Sol/Opus pour une correction locale et vérifiable                     |
| Suivi post-PR autonome (CI, review, mergeabilité)         | Reprise      | **GPT‑6.2 Sol Medium**                      | High si root cause difficile ; Sol 6.1 en fallback | Goal mode, Heartbeats ou Cloud ; boucle séquentielle bornée, pas Ultra           |
| Deuxième échec révélant une mauvaise conception          | Reprise      | **GPT‑6.2 Sol High** ou **Opus 5.5 High**    | Utiliser l'autre famille pour casser l'ancrage | Le problème n'est plus mécanique : il faut requalifier l'hypothèse                 |
| Échecs répétés malgré Sol High / Opus High               | Escalade     | **GPT‑6.2 Astra Light** ou **Fable 5.2 Low**   | L'autre frontier en challenger                 | La capacité devient le facteur limitant ; repartir avec un contexte propre         |
| Session autonome > 30 min, dépendances séquentielles     | Long-horizon | **Opus 5.5 Extra (`xhigh`)**                 | Sol High à la fin                              | Extra est justifié par la longueur, pas par l'importance symbolique                |
| Travail extrêmement difficile durant plusieurs heures    | Frontier     | **Fable 5.2 High**                           | Astra Light/Medium en review indépendante      | Réserver le coût frontier élevé aux trajectoires où il évite des reprises majeures |
| Exploration codebase-scale décomposable                  | Multi-agent  | **GPT‑6.2 Sol Ultra**                        | Opus Medium pour synthèse/review               | Ultra vaut surtout pour les axes read-heavy indépendants                           |
| Tests, exploration et triage massivement parallélisables | Multi-agent  | **GPT‑6.2 Sol Ultra**                        | Claude seulement sur les anomalies importantes | Le parallélisme paie quand les sous-tâches sont indépendantes et vérifiables       |
| Plusieurs writers sur les mêmes fichiers                 | —            | **À éviter**                                 | Séquentialiser                                 | Le coût de coordination dépasse généralement le gain                               |

> **Note Qwen3-Coder-Next en local** : le modèle officiel est un MoE de **80B paramètres au total, 3B activés**, avec 48
> couches hybrides, un contexte natif de **262 144 tokens** et un fonctionnement exclusivement **non-thinking**. Le
> nombre
> réduit de paramètres actifs améliore le coût de calcul, mais les **80B de poids doivent tout de même résider en
> mémoire
> ** : « 3B actifs » ne signifie donc pas qu'il se comporte en RAM comme un dense 3B.
>
> Les tailles GGUF officielles sont : **Q4_K_M 48,4 Go**, **Q5_K_M 56,7 Go**, **Q6_K 65,5 Go** et **Q8_0 84,8 Go**. La
> taille du fichier n'est cependant pas la consommation totale : ajoute le cache de contexte, les buffers du backend, le
> serveur, macOS, IntelliJ, sbt et les JVM du projet. Sur **128 Go**, les quatre variantes peuvent théoriquement être
> chargées, mais elles n'offrent pas la même marge opérationnelle.
>
> ```text
> Q4_K_M  → défaut « marge maximale » : IDE, sbt et plusieurs JVM restent confortables.
> Q5_K_M  → défaut recommandé : meilleur compromis qualité / mémoire sur cette machine.
> Q6_K    → option haute qualité : viable si les autres applications restent raisonnables.
> Q8_0    → option d'évaluation : possible, mais marge réduite et bénéfice à prouver face à Q5/Q6.
> ```
>
> La documentation officielle Qwen utilise justement **Q5_K_M** dans son exemple `llama.cpp`, avec `-c 40960`, et non le
> contexte maximal de 256K. Pour le travail agentique quotidien, pars sur **32K à 64K**, puis augmente seulement si une
> tâche réelle le justifie. Le contexte déclaré par le modèle est une capacité maximale, pas une configuration
> économique
> par défaut.
>
> **Recommandation pour ton M5 Max 128 Go** : conserve **Q4_K_M et Q5_K_M** sur le SSD. Utilise Q5_K_M comme profil
> quotidien de pré-analyse, résumé de modules et génération de tests simples ; bascule sur Q4_K_M lorsque IntelliJ,
> plusieurs modules sbt, Spark ou des JVM lourdes consomment déjà beaucoup de mémoire. Ne conserve Q6_K ou Q8_0 que si
> un
> bake-off Scala montre un gain de qualité mesurable. Avec 8 To de SSD, le stockage n'est pas la contrainte ; la
> pression
> mémoire, la latence et la qualité par tâche le sont.
>
> **Backend Apple Silicon** : teste **MLX-LM et llama.cpp** au lieu de figer immédiatement un seul moteur. Des
> conversions MLX 4-bit et 8-bit existent, et un rapport reproductible sur Qwen3-Coder-Next a observé un décodage
> nettement plus rapide sous MLX que sous une version donnée de llama.cpp sur Apple Silicon. Ce résultat dépend des
> versions et ne constitue pas une garantie pour le M5 Max ; il justifie un benchmark local avec versions figées.
> `llama.cpp` reste néanmoins la voie la mieux documentée par Qwen et expose facilement un serveur OpenAI-compatible.
>
> **Metal et mémoire câblée** : ne présente pas « 75 % » comme une limite matérielle absolue. `llama.cpp` affiche au
> démarrage `recommendedMaxWorkingSetSize`, qui est la valeur à observer sur la version de macOS et le Mac concernés. Le
> réglage non documenté `iogpu.wired_limit_mb` existe et est utilisé par la communauté, mais il ne doit pas devenir un
> prérequis standard : teste d'abord le modèle sans modification système. Q8_0 peut fonctionner sur une machine 128 Go,
> mais un contexte long ou plusieurs slots peuvent rapprocher le processus de cette limite avant que la RAM physique
> soit
> entièrement occupée.
>
> **Protocole de mesure minimal** : compare Q4_K_M, Q5_K_M et éventuellement Q6_K sur les mêmes dix tâches Scala, avec
> le même contexte et le même harness. Mesure séparément le prompt processing, le débit de génération, le temps jusqu'au
> premier token, la mémoire maximale, la pression mémoire macOS et le taux de tâches acceptées. Ne déduis pas la vitesse
> du seul nombre de paramètres actifs : l'architecture hybride et l'implémentation des kernels peuvent produire des
> écarts
> importants entre backends.
>
> **Qwen3.8-27B.** Le dense **Qwen3.8-27B** devient le challenger local quality-first à ajouter au
> bake-off Scala. Qwen publie un contexte pouvant aller jusqu'à 1M selon le déploiement et des scores éditeur de 73 sur
> Terminal-Bench 2.1 et 61,7 sur SWE-bench Pro. Ces chiffres ne justifient pas de remplacer Coder-Next par défaut :
> teste
> les deux avec le même harness, le même contexte, les mêmes outils et le même budget de temps. **Coder-Next reste la
> baseline locale spécialisée et économique ; Qwen3.8-27B est le challenger à privilégier lorsque la qualité compte plus
> que le débit.** Les tarifs API Qwen3.8 dépendent de la région et ne doivent pas être présentés comme un prix mondial.

>
> **Qwen3.8-Omni-Flash.** Depuis le 17 septembre 2026, Alibaba propose aussi ce modèle API multimodal : texte, image,
> audio et vidéo en entrée, texte en sortie, function calling, thinking configurable, recherche web, cache de contexte,
> **1M tokens de contexte** et jusqu'à **131 072 tokens de sortie** via Chat Completions ou Responses API. Il complète
> le routage pour l'analyse de screencasts, talks, interfaces ou documentation multimodale ; il **ne remplace pas**
> Qwen3-Coder-Next comme baseline locale de code ni Qwen3.8-27B comme challenger Scala quality-first. Ses tarifs varient
> selon la région de déploiement : garde cette donnée hors des règles de routage durables et vérifie Model Studio au
> moment du choix.

### Côté Anthropic

| Modèle         | API ID              | Tarif (input/output / M tokens) | Contexte          | Effort par défaut | Rôle actif dans ce guide                                                           |
|----------------|---------------------|---------------------------------|-------------------|-------------------|------------------------------------------------------------------------------------|
| **Fable 5.2**  | `claude-fable-5-2`  | $8 / $40                        | 1M (sortie 128K)  | `high`            | Frontier : raisonnement exigeant et long-horizon quand Opus 5.5 ne suffit pas      |
| **Opus 5.5**   | `claude-opus-5-5`   | $4 / $20                        | 1M (sortie 128K)  | **`medium`**      | Défaut agentique : coding autonome, architecture, debugging et gros refactors      |
| **Sonnet 5.5** | `claude-sonnet-5-5` | $2 / $10                        | 1M (sortie 128K)  | `high` API        | Micro-dev / tâches bien spécifiées ; `medium` recommandé pour agentic coding borné |
| **Haiku 5.5**  | `claude-haiku-5-5`  | $0.10 / $0.50 (prompt ≤ 100K)   | 1M (sortie 128K)  | `medium`          | Workers, triage, extraction, logs, sous-agents à faible risque                     |

> **Routage courant:** Anthropic recommande de démarrer la plupart des workloads avec **Opus 5.5**,
> dont l'effort par défaut est `medium`, puis d'ajuster l'effort avant de changer de modèle. Pour **Sonnet 5.5**, le
> coding agentique bien spécifié commence utilement à `medium` et monte à `high` pour les tâches plus longues ou
> difficiles.
> `xhigh` (noté **Extra** dans ce guide) et `max` sont réservés aux cas où les evals montrent un gain. **Haiku 4.5 ne
> supporte pas le paramètre d'effort ; Haiku 5.5, qui le remplace, le supporte avec `medium` par défaut.** Les paragraphes ci-dessous sur Sonnet 5 / Opus 5 restent des repères de
> migration
> historiques ; ils ne remplacent pas cette matrice active.

> **Migration API vers Opus 5.5 / Sonnet 5.5.** Les deux modèles imposent davantage de discipline au client que les
> générations précédentes : l'adaptive thinking est le régime normal, le *forced tool use* (`tool_choice: any/tool`)
> renvoie une erreur 400, et les *thinking blocks* doivent rester attachés à leur modèle et à la conversation qui les a
> produits. **Opus 5.5** rejette aussi les paramètres de sampling non standard et l'assistant prefill ; son effort par
> défaut est `medium`. **Sonnet 5.5** utilise `thinking: {"type": "between_tools"}` pour supprimer le thinking initial
> (`low` à `high` seulement), et renvoie désormais le texte intermédiaire entre tool calls dans des blocs `thinking`.
> Sur Claude API et Google Cloud, les deux modèles utilisent le toolset computer-use courant
> `computer_toolset_20260801` plutôt que `computer_20251124`. Une migration de modèle doit donc tester **payloads,
> streaming, tools et reprise de conversation**, pas seulement remplacer l'ID du modèle.

> **Sonnet 5** remplace Sonnet 4.6 (`claude-sonnet-4-6`, toujours disponible au même tarif
> $3/$15) comme driver quotidien. C'est un *drop-in replacement* côté API, avec trois changements de comportement à
> connaître avant de migrer :
> - **Adaptive thinking activé par défaut** ; l'extended thinking manuel (`thinking: {type: "enabled"}` avec
>   `budget_tokens`) renvoie désormais une **erreur 400** — migre vers l'adaptive thinking.
> - **Paramètres de sampling verrouillés** : toute valeur non-défaut de `temperature`, `top_p` ou `top_k` renvoie
>   une erreur 400.
> - **Nouveau tokenizer** (même lignée qu'Opus 4.7+) : ~30% de tokens en plus pour le même texte (jusqu'à 1.35x
>   selon le contenu). Le tokenizer peut toujours augmenter le nombre de tokens facturés ; recompte donc les
>   prompts avec l'endpoint de token counting et revois les `max_tokens` serrés.
>
> Autres spécificités opérationnelles : **Effort Control** généralisé (niveaux low → **xhigh**, défaut *high* sur
> l'API et Claude Code), premiers **garde-fous cybersécurité temps réel** sur un Sonnet (un refus revient en HTTP
> 200 avec `stop_reason: "refusal"`, pas en erreur — à gérer dans le client), pas de Priority Tier, sortie 128K
> (300K en batch via le header beta `output-300k-2026-03-24`). C'est aussi le nouveau modèle par défaut des plans
> Free et Pro sur claude.ai.

> **Remises communes** : le prompt caching et le batch (–50% input et output) s'appliquent à *tous* les modèles
> Claude. Le tarif de lecture du cache dépend toutefois du modèle : **Fable 5.2 coûte $0.20/M tokens en cache lu**
> (contre $0.25/M pour Fable 5.1). Le batch reste utile pour le travail non urgent : PR summaries groupés,
> audits planifiés et génération de fixtures. Fable 5.2, Opus 5.5 et Sonnet 5.5 incluent le contexte 1M au tarif
> standard, sans surcharge de long contexte.
>
> **Précision tarifaire.** Le cache read vaut **0,025× l'input** sur Fable 5.2/5.1 ($0.20 et $0.25/M),
> **0,05×** sur Opus 5.5 et Sonnet 5.5 ($0.20 et $0.10/M) et 0,1× sur Haiku 4.5. Haiku 5.5 est le seul modèle courant
> avec un **palier de longueur de prompt** : au-delà de 100 000 tokens d'entrée (cache inclus), tous ses tarifs sont
> multipliés par cinq. Batch : Fable 5.2 $4/$20, Opus 5.5 $2/$10, Sonnet 5.5 $1/$5. Fast mode : Fable 5.2 $16/$80,
> Opus 5.5 $8/$40. `inference_geo: "us"` applique un multiplicateur de 1,1× sur les catégories concernées.

> **Claude Fable 5.2 remplace Fable 5.1 dans le routage actif de ce guide.** Fiche
> technique : ID `claude-fable-5-2` (`anthropic.claude-fable-5-2` sur Bedrock), contexte **1M**, sortie **128K**,
> **$8/$40**, cache write 5 min $10 et 1 h $16, cache read **$0.20/M**, batch $4/$20, fast mode `speed: "fast"` à
> $16/$80, adaptive thinking toujours actif, effort par défaut `high`, cutoff juin 2026, retrait pas avant le
> 9 novembre 2027. Mêmes contraintes que 5.1 : **30 jours de rétention obligatoires (pas de ZDR sans autorisation
> expresse)**, `tool_choice: any/tool` et prefill en 400, sampling à omettre, pas de Priority Tier, pas de structured
> outputs pour les organisations CMEK. Le modèle génère environ 30 % plus vite que 5.1. **Mythos 5.2** est le même
> modèle avec moins de garde-fous, réservé aux organisations vérifiées.
>
> **Positionnement.** La matrice officielle reste « la plupart des workloads commencent avec Opus 5.5 » ; on passe à
> Fable 5.2 si les evals à `xhigh` ou `max` restent insuffisantes sur du raisonnement exigeant ou du long-horizon.
> Fait nouveau à intégrer au routage : sur FrontierCode 2.0 (qui mesure si des mainteneurs mergeraient le changement),
> Anthropic rapporte **Fable 5.2 `high` à 45,3 %, au niveau d'Opus 5.5 au meilleur effort (45,5 %), pour environ la
> moitié du coût par tâche**. Scores éditeur au meilleur effort : FrontierCode 2.0 **49,1 %** (Opus 5.5 45,5 ; Astra
> 42,8 ; Fable 5.1 32,4), FrontierSWE v2 **69,9 %** (Opus 62,3 ; Astra 65,5), Remote Labor Index 41,3 % contre 21,3 %
> pour Opus. Sur le coding court l'écart est faible : Terminal-Bench 4.0 67,6 % contre 66,4 % (Opus `xhigh`), dans la
> marge d'erreur. Les mesures indépendantes Vals confirment la nuance : égalité avec Opus 5.5 sur Terminal-Bench 4.0
> (65,15 %), Opus devant sur SWE-bench Multimodal (70,2 % contre 62,3 %). Sur le protocole
> **Mini-SWE-agent** de Vals, cette égalité correspond pourtant à environ **$14,56/tâche pour Fable contre
> $12,04 pour Opus**, avec Fable plus rapide (55 min contre 64 min) : l'avantage de coût par tâche annoncé
> par Anthropic sur FrontierCode **ne se généralise pas** aux autres harness. Conséquence pratique :
>
> ```text
> Opus 5.5 High insuffisant (capacité)        → Fable 5.2 avant Opus 5.5 Max, à mesurer sur le benchmark Scala privé
> Décision difficile ponctuelle (advisor)     → Fable 5.2 low/medium
> Mission longue autonome                     → Fable 5.2 high (low/medium finissent plus souvent le tour trop tôt)
> Tâche bornée, bug UI/front, review courante → Opus 5.5 ou Sonnet 5.5 restent les meilleurs achats
> ```
>
> **Breaking changes depuis Fable 5.1** (vérifiés dans le guide de migration officiel) :
> - le **prefix check** s'applique désormais à tous les comptes : un thinking block renvoyé avec un `system`, des
>   `tools` ou un historique différents de ceux qui l'ont produit donne un 400 (`The block is bound to a different
>   conversation`). **Un changement de la liste d'outils MCP entre deux requêtes compte comme une édition** : épingle
>   la tool list pendant la session, ou utilise les changements d'outils en cours de conversation (beta
>   `inline-tools-2026-09-15`, via des messages `role: "system"`). Attention aux harness qui chargent les outils à la
>   demande en modifiant `tools` ;
> - **Fable 5.1 et Opus 5.5 ne lisent pas les thinking blocks de Fable 5.2** (ils sont supprimés sans erreur, donc le
>   raisonnement est perdu en silence) ; Fable 5.2 lit ceux de 5.1 et d'Opus 5.5. Les fallbacks serveur
>   (`fallbacks: "default"`, beta `server-side-fallback-2026-07-01`) ne ciblent que `claude-opus-4-8` et
>   `claude-opus-5` : journalise le modèle exécuté ;
> - `computer_20251124` renvoie 400 (sauf Bedrock) : utiliser `computer_toolset_20260801` ;
> - l'advisor d'un exécuteur Fable 5.2 doit être `claude-fable-5-2` ou `claude-mythos-5-2` ;
> - le thinking compte dans `max_tokens` (risque de `stop_reason: "max_tokens"` avant tout texte) et Fable 5.2 a sa
>   **propre rate limit**, distincte de celle de Fable 5/5.1. Nouveaux betas utiles : compaction à la demande
>   (`compact-2026-09-04`), binding des thinking blocks (`thinking-binding-controls-2026-08-01`, avec
>   `prefix_mismatch_behavior: "drop_block"` seulement comme palliatif).
>
> **Comportements qui touchent directement la qualité des diffs et le coût** (guide de prompting Fable 5.2) :
> - **Propriété du code.** Sans consigne explicite, le modèle ajoute à la structure existante, duplique et signale les
>   problèmes voisins au lieu de les corriger. La phrase proposée par Anthropic (« This codebase is yours… ») fait
>   fusionner le code dupliqué dans environ la moitié des essais, mais coûte environ 1,5× de tokens de sortie, ajoute
>   des tests et docs non demandés et modifie un comportement existant dans un essai sur six à dix. **Pour les tickets
>   à diff minimal de ce guide, ne l'ajoute pas** ; réserve-la à une tâche explicite de déduplication ou de refactor,
>   et relis le diff plutôt que le résumé, qui omet souvent les petits changements.
> - **Sur-délégation.** À `xhigh` et `max`, Fable 5.2 peut lancer des subagents pour relire son propre travail, et les
>   subagents peuvent représenter une grande part du coût de session. Audite les lignes de `AGENTS.md`, skills et
>   fichiers d'agents qui invitent à déléguer, et vérifie le modèle par défaut des subagents.
> - **Fins de tour prématurées** (liste de tâches restantes, offre de continuer) plus fréquentes à `low` et `medium` :
>   pour une mission longue, ajoute la consigne « ne t'arrête pas tant qu'il reste du travail demandé », tout en
>   distinguant obstacle ordinaire (à traiter) et blocage délibéré (fichier interdit, garde-fou : à laisser et
>   signaler). Garde tes propres confirmations pour les actions risquées.
> - **Budget serveur ≠ coupe-circuit.** Le `task_budget` API est indicatif : fixe un **plafond externe** de coût,
>   nombre d'appels, durée et nombre de tentatives dans le harness. Un `max_tokens` trop serré peut interrompre
>   Fable avant le premier texte visible, car les tokens de thinking comptent dans la sortie. Si la session semble
>   silencieuse, utilise les mises à jour entre outils lorsque disponibles au lieu de multiplier les relances.
> - **Instructions héritées à purger** : « réponds sans délibérer » n'arrête pas la réflexion à partir de `medium`
>   (baisse plutôt l'effort) ; les lignes « traite cette réponse comme terminée » issues du prompting Opus 5.5 rendent
>   le modèle beaucoup moins apte à rattraper ses propres erreurs ; les budgets de tokens écrits dans le prompt
>   peuvent être retirés à `high`/`xhigh` sans perte ; les précautions périmées accumulées en mémoire réduisent des
>   comportements utiles. C'est exactement le rôle de `/doctor prompt-audit` (section 3, subagents).
>
> **Accès et quota.** Claude Code **2.1.321+** (`claude --model claude-fable-5-2` ; l'alias `fable` dépend
> de la gateway). Les plans Max/Ultra éligibles peuvent utiliser Fable jusqu'à une fraction plafonnée à **50 % des
> limites hebdomadaires**, selon les conditions effectives ; l'usage sur Pro peut dépendre de crédits supplémentaires
> ou d'une promotion temporaire. Ne confonds
> jamais **modèle visible**, **quota inclus** et **facturation API/crédits** : contrôle l'écran de consommation et les
> conditions du plan au moment de la session. Recalibre les efforts `medium`, `high` et `xhigh` et le coût par tâche.

> **Note tokenizer** : le nouveau tokenizer a été introduit par **Opus 4.7** (pas 4.8) et génère jusqu'à ~35% de
> tokens en plus qu'Opus 4.6 pour le même texte. **Sonnet 5 adopte la même lignée** (~30% de tokens en plus que
> Sonnet 4.6, jusqu'à 1.35x selon le contenu). La pénalité de comptage reste pertinente pour les migrations Opus à
> tarif identique ; sur Sonnet 5, le tarif permanent **$2/$10** compense une grande partie de l'augmentation du nombre
> de tokens par rapport à Sonnet 4.6. Le passage Opus 4.7 → 4.8 ne porte aucune pénalité supplémentaire de tokenizer.

> **Opus 5 et transition depuis 4.8** : Opus 5 est désormais le **modèle Anthropic difficile par défaut** à tarif
> identique à Opus 4.8 ($5/$25). Garde 4.8 uniquement comme fallback de compatibilité ou référence historique.
> - **Fast Mode** ($10/$50, ~2.5x la vitesse standard) : pour une tâche dure mais *interactive* (debugging en pair),
>   Opus 5 Fast est souvent un meilleur achat que Fable.
> - **Effort Control** : router par effort reste l’étape explicite avant Fable 5.2. Sur Opus 5, `xhigh` et `max`
>   exigent que le thinking reste activé ; `thinking: disabled` avec ces niveaux renvoie une erreur 400.
> - **Dynamic Workflows** reste pertinent pour le parallélisme codebase-scale ; dans Claude Code, complète-le désormais
>   avec Agent View. **Agent Teams** reste expérimental et **Ultrareview** en research preview : ne les transforme pas
>   encore en dépendances obligatoires du workflow.

> **Note Claude Managed Agents** (plateforme hébergée, beta publique depuis avril 2026, header
> `managed-agents-2026-04-01`) : depuis Code with Claude (6 mai 2026), la plateforme ajoute **Outcomes** (grader
> indépendant sur rubrique, boucle de révision si l'output ne passe pas), l' **orchestration multi-agent** (jusqu'à
> 20 sous-agents spécialistes en parallèle sur un filesystem partagé), des **webhooks** de fin de session (beta
> publique) et le **Dreaming** (research preview : curation de mémoire entre les sessions). Tarification : tokens au
> tarif API + $0.08 par heure de session active. Pour ce guide, c'est la troisième option sur les missions longues,
> à côté de Fable mono-agent et d'Opus + Dynamic Workflows — pertinente surtout si tu veux un harness hébergé avec
> critères de succès exécutoires (Outcomes est la version plateforme du « gate de review » de la section 15A).

> **OpenAI Agents API** est le pendant hébergé côté OpenAI : elle utilise le
> harness géré de Codex avec **sessions durables**, compaction et reprise gérées, MCP et sous-agents à contexte isolé.
> Deux primitives matérialisent directement le context engineering de la section 10 : **tool search** ne charge les
> définitions d'outils que lorsqu'elles deviennent pertinentes, et le **programmatic tool calling** permet de chaîner,
> paralléliser et filtrer des appels avant de ne réinjecter que les résultats utiles. Ce n'est pas une nouvelle raison
> de préférer OpenAI à Anthropic : compare **Agents API**, Claude Managed Agents et les harness locaux au coût par
> changement accepté, en gardant les mêmes specs, tests et règles d'arrêt.
>
> **Computer use** peut aussi s'exécuter dans un navigateur hébergé par OpenAI. L'application
> crée la session, approuve explicitement chaque nouvelle origine et gère elle-même les authentifications sensibles.
> Une approbation d'origine n'est pas une confirmation par action : pour achat, suppression ou autre opération
> conséquente, garde un runtime contrôlé ou un gate applicatif séparé.


Caractéristiques opérationnelles complémentaires :

| Modèle         | Latence relative | Prompt caching     | Batch (–50%) | Spécificité opérationnelle                                                                        |
|----------------|------------------|--------------------|--------------|---------------------------------------------------------------------------------------------------|
| **Fable 5.2**  | Modérée          | Oui ; read $0.20/M | Oui          | Adaptive thinking toujours on ; défaut `high` ; effort par message ; fast mode $16/$80            |
| **Opus 5.5**   | Modérée          | Oui                | Oui          | Adaptive thinking toujours on ; défaut **`medium`** ; Low→Max                                     |
| **Sonnet 5.5** | Rapide           | Oui                | Oui          | Adaptive thinking ; défaut API `high`, mais `medium` recommandé pour agentic coding bien spécifié |
| **Haiku 5.5**  | La plus rapide   | Oui ; read $0.01/M | Oui          | Adaptive thinking par défaut ; effort `medium` par défaut ; palier de prix au-delà de 100K tokens |

### Côté OpenAI / Codex

**GPT‑6.2 Sol** est le défaut recommandé pour le **coding complexe et les workflows agentiques répétés** dans
Codex lorsqu'il est disponible. OpenAI le positionne comme plus efficace par tâche que Sol 6.1, au même tarif API.
**GPT‑6 Luna** vise les tâches focalisées, répétables et à haut volume ; **GPT‑6.1 Terra** est le tier intermédiaire.
**GPT‑6.2 Astra** reste l'escalade de capacité pour les tâches les plus exigeantes.

| Modèle          | ID API        | Prix standard / 1 M tokens (input / output) | Rôle recommandé dans ce guide |
|-----------------|---------------|---------------------------------------------|-------------------------------|
| **GPT‑6 Luna**  | `gpt-6-luna`  | **$0.10 / $0.50** | Micro-dev, modifications mécaniques, tests simples, triage et workers à faible risque |
| **GPT‑6.1 Terra** | `gpt-6.1-terra` | **$1 / $5** | Patch local et review ciblée lorsque Luna manque de jugement |
| **GPT‑6.2 Sol** | `gpt-6.2-sol` | **$2 / $10** | **Défaut Codex agentique Medium** : issue end-to-end, feature multi-fichiers, tests, PR, review et stewardship |
| **GPT‑6.2 Astra** | `gpt-6.2-astra` | **$8 / $40** | Frontier : problème très ambigu, contrat critique, escalade de capacité |
| GPT‑6.1 Sol / GPT‑6 Astra | `gpt-6.1-sol` / `gpt-6-astra` | $2 / $10 ; $10 / $50 | Fallbacks si les versions 6.2 ne sont pas disponibles ; baselines historiques |

> **GPT‑6.1 Terra comble le trou entre Luna et Sol.** Sorti le 26 octobre 2026 (`gpt-6.1-terra`),
> il coûte **$1/$5** (cached input $0.05/M), soit la moitié de Sol 6.1, avec la même fenêtre d'environ 1,05M tokens. Il
> est disponible dans ChatGPT Work et Codex (Plus, Pro, Enterprise, Edu ; pas dans l'onglet Chat) et demande un Codex
> CLI récent (0.159+ selon les sources). OpenAI le positionne sur les corrections de bugs courantes, le computer use,
> la vision et l'écriture ; pour le coding exigeant, préfère désormais **Sol 6.2 ou Astra 6.2**. Score publié :
> 50,3 % sur Terminal-Bench 4.0 à effort max (21,5 % pour GPT‑5.6 Terra). Pour ce guide, Terra devient le **candidat
> naturel pour les patchs bornés et la review de petits diffs** quand Luna est trop juste et Sol trop cher : à départager
> par bake-off avant de modifier la matrice.

> **GPT‑6.2 Sol et Astra** : 1,05M tokens de fenêtre, dont 922K d'entrée maximum et 128K de sortie maximum.
> Cache read : $0.10/M pour Sol, $0.40/M pour Astra ; cache write 30 min à 1,25× l'input, 12 h à 2,5×.
> Au-delà de 272K tokens d'entrée, les tarifs input/cache doublent et le tarif output est multiplié par 1,5 pour
> la requête entière. Batch est à 50 % du tarif Standard ; Flex n'est pas proposé sur les nouveaux modèles 6.2.
> Ne transpose pas ces prix au quota d'abonnement. Sol 6.1 Medium et Astra 6 Light restent des fallbacks si les
> versions 6.2 sont indisponibles. Le stewardship est une capacité du harness, pas du modèle. Les benchmarks
> antérieurs restent des baselines historiques, à ne pas attribuer aux modèles 6.2.

> **Ultrafast est un tier de service, pas un nouveau modèle ni un niveau d'effort.** Repère historique : pour GPT-6 Astra, l'API Ultrafast
> vise jusqu'à ~8× la vitesse de Standard et facture en contexte court **$60/M input, $6/M cached input, $75/M cache
> write et $300/M output**. Utilise-le uniquement quand la latence domine réellement le coût total ; pour les boucles
> agentiques à nombreux tool calls, OpenAI recommande une connexion Responses persistante en WebSocket. Ultrafast ne
> prend pas en charge la résidence des données UE : il fonctionne en traitement global ou avec résidence US. Côté
> produit, Astra Ultrafast est notamment inclus dans **Pro 500** et certaines offres Enterprise. Il ne change donc pas
> le routage qualité de cette section : `Astra Standard` et `Astra Ultrafast` ont la même capacité modèle.
> Sur GPT‑6.2, vérifie les tarifs et les droits du plan avant activation ; ne réserve les tiers rapides qu'aux boucles
> interactives réellement limitées par la latence, pas à l'attente de CI.

Dans **Codex / Work**, raisonne avec les niveaux visibles **Light → Medium → High → Extra High → Ultra**. Le défaut de
ce guide est **Sol Medium**, **Luna High** pour les micro-boucles et **Astra Light** pour une escalade de capacité.
`Ultra` dépasse un simple run mono-agent et n'est rentable que si le travail peut réellement se décomposer en axes
indépendants. Côté API, les noms des niveaux restent `low/medium/high/xhigh/max` selon le modèle : ne confonds pas le
libellé produit avec la valeur portable de `reasoning.effort`.

Les modèles GPT‑5.6 peuvent rester disponibles pendant le rollout, mais ils ne constituent plus la route active par
défaut de ce guide.

#### Cinq dimensions à ne pas confondre

| Levier                            | Ce qu'il change                                                                                     | Règle pratique                                                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Modèle**                        | Capacité, vitesse et prix : Luna, Terra, Sol 6.2 ou Astra 6.2.                                 | Luna pour le borné ; Sol 6.2 pour l’agentique répété ; Astra seulement quand la capacité supérieure réduit les reprises. |
| **Effort**                        | Budget de raisonnement : libellés Codex Light→Ultra ; API `low/medium/high/xhigh/max` selon modèle. | Sol : Medium par défaut ; Luna : High ; Astra : Light ; augmenter seulement si planification/vérification le justifie.   |
| **`reasoning.mode: "pro"`** (API) | Davantage de travail modèle pour une réponse finale plus fiable.                                    | Indépendant de l'effort ; comparer standard/pro sur des tâches représentatives.                                          |
| **`ultra` comme effort Codex**    | Certains SDK/harness Codex exposent désormais `ultra` comme niveau de reasoning au-dessus de `max`. | Le traiter comme une capacité du harness, pas comme une valeur portable de la Responses API.                             |
| **Ultra / Multi-agent**           | Orchestration de plusieurs agents ou sessions selon la surface produit/API.                         | L'utiliser seulement si le travail se sépare réellement en volets indépendants.                                          |

Dans la **Responses API**, la valeur maximale documentée de `reasoning.effort` reste `max` et **Multi-agent** demeure
une fonctionnalité beta distincte. Dans certains harness Codex, `ultra` peut au contraire désigner un effort de
raisonnement. Ne déduis donc jamais la sémantique du seul mot « ultra » : logge la surface, le modèle, l'effort et le
nombre réel d'agents. OpenAI ne publie pas de multiplicateur de coût fixe ; mesure coût total, latence et taux de succès
sur ton dépôt avant standardisation.

#### Astra : contrôles pour missions longues

Astra ajoute trois capacités particulièrement utiles aux agents :

```text
async tool calling
→ continuer à raisonner ou appeler d'autres outils pendant qu'un outil lent s'exécute

mid-turn steering
→ ajouter une contrainte ou changer de direction sans redémarrer toute la mission

configuration updates
→ changer l'effort en cours de trajectoire sans casser inutilement le préfixe de cache
```

Pour un backend agentique, privilégie la **Responses API** : le tool calling Astra y est la surface de référence. Astra
n'accepte pas `reasoning.effort = none`, ni les réglages personnalisés de `temperature` / `top_p` documentés comme
incompatibles. Le **Fast mode** API peut aller jusqu'à ~2× plus vite pour **2× le prix standard** ; il n'a pas de SLA de
latence et ne doit pas devenir le défaut d'une mission longue.

#### Disponibilité et surfaces ChatGPT / Codex

| Surface                  | Accès modèle et mode                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **ChatGPT Work / Codex** | GPT‑6.2 Sol et Astra, GPT‑6.1 Terra, Luna et fallbacks selon plan, client, workspace et rollout.                                              |
| **GPT‑6.2 Sol / Astra**  | Plus, Pro, Business, Enterprise et Edu dans Codex/Work selon droits ; contrôles d'effort Light→Ultra selon paramètres disponibles. |
| **GPT‑6 Luna**           | Modèle économique pour tâches focalisées et répétables dans Work/Codex.                                                            |
| **Ultra / multi-agent**  | À réserver aux axes indépendants ; ne pas l'assimiler à « davantage de réflexion » sur une chaîne séquentielle.                    |
| **API**                  | `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6-luna` via les surfaces supportées ; vérifier les outils et efforts par modèle.                |

Les droits effectifs dépendent toujours du plan, de la région, du workspace et du rollout. Ne code jamais une règle de
produit durable à partir du seul nom d'un abonnement.

#### Caching, sécurité et garde-fous

GPT‑6.2 Sol facture le cached input **$0.10/M** contre $2/M en input standard ; les cache writes restent à 1,25×
l'input. GPT‑6 Luna descend à **$0.01/M** en cached input. Stabilise donc le haut du prompt (`AGENTS.md`, conventions
Scala, contrats, règles de test) et laisse diffs, logs et erreurs en bas.

> **Deux leviers de coût en volume.** Sur GPT‑6.1 Sol et GPT‑6 Luna, Batch et Flex coûtent 50 % de moins que
> Standard ; sur GPT‑6.2 Sol/Astra, Batch conserve cette réduction, mais Flex n’est pas proposé.
> Utilise-les pour ce qui tolère la latence : audits planifiés, PR summaries groupés, génération de fixtures et triage
> massif. Ne transpose pas automatiquement ces tarifs API au quota ChatGPT/Codex : le bon indicateur reste le coût par
> tâche terminée dans la surface réellement utilisée.

GPT‑5.6 reste classé « High » mais non « Critical » en cyber. **GPT‑6 Astra (génération originale) est le premier modèle OpenAI classé Critical
en cybersécurité** : avec les bons outils, il peut trouver des vulnérabilités inconnues et développer de nouvelles
chaînes d'exploitation. Ce niveau de capacité s'accompagne d'un monitoring de trajectoire plus strict : dans
ChatGPT/Codex, une tâche légitime peut être ralentie, mise en pause ou demander une validation ; via API, le travail
peut être stoppé.

Cette hausse de capacité ne justifie aucune autonomie supplémentaire. Avec Astra, rends encore plus explicites : scope
de fichiers, réseau, opérations externes, écritures destructives, budget, durée, conditions d'arrêt et validation
humaine. Point favorable pour le code sensible : **Astra supporte le Zero Data Retention pour les clients API
éligibles**, alors que Fable 5.2 impose 30 jours par défaut sauf autorisation expresse d'Anthropic.

#### Benchmarks et prudence

Les chiffres de lancement Astra sont particulièrement forts en **coding agentique et computer use**, mais doivent rester
attachés à leur harness. OpenAI rapporte notamment : Terminal-Bench 4.0 **57,9 % Astra vs 55,8 % Fable 5.1**, DeepSWE
1.1 **74,1 % vs 67,4 %**, FrontierCode Extended **64,5 % vs 63,6 %** et ses tâches internes de migration DB **63,9 % vs
57,8 %**. Sur AutomationBench, Astra atteint **41,4 % vs 31,4 %** pour Fable 5.1. Ce sont des évaluations publiées par
OpenAI : utiles comme signal, jamais comme verdict sur Scala.

L'évaluation indépendante Artificial Analysis nuance fortement le tableau. Dans son **Coding Agent Index v1.4**, Claude
Code + Fable 5.1 (`max`, avec fallback) obtient **70** contre **67** pour Codex + Astra (`max`), mais Astra consomme
environ **4,0M tokens/tâche contre 7,1M** et coûte environ **$4,72/tâche contre $9,18**. Sur l' **Intelligence Index**,
Fable 5.1 `max` est également devant (**66 vs 61**). Le bon enseignement n'est donc pas « Astra > Fable » : **Fable
garde un petit avantage de qualité agrégée dans ces protocoles, Astra un avantage majeur d'efficacité par tâche dans
Codex**.

Astra publie aussi un très bon rappel long contexte sur MRCR v2 : **100 % à 256–512K** et **96,3 % à 512K–1M**. Ne
transforme pas ces scores en permission d'envoyer le monorepo entier : au-delà de 272K, son tarif augmente et le
*context rot* reste un problème de raisonnement, pas seulement de capacité physique.

Pour ce guide, la conclusion robuste devient :

```text
GPT‑6 Luna High = micro-dev et workers Codex sous contrôle humain fort.
GPT‑6.2 Sol Medium = défaut Codex pour l'agentic coding end-to-end.
GPT‑6.2 Sol High = feature complexe, migration et reprise difficile.
GPT‑6.2 Astra Light = escalade de capacité avant de pousser mécaniquement Sol à l'effort extrême.
Sonnet 5.5 Medium = micro-dev Claude et tâches agentiques bien spécifiées.
Opus 5.5 Medium = défaut Claude pour l'agentic coding autonome.
Opus 5.5 High = architecture, debugging et refactor difficiles.
Fable 5.2 Low = escalade frontier quand Opus High reste insuffisant.
Astra vs Fable = décider au coût par changement accepté, pas au prix par token.
```

### GPT‑6 Astra vs Claude Fable 5.2 : repère historique de deux frontiers

Ce comparatif conserve les chiffres du GPT‑6 Astra original : pour le routage courant, utilise GPT‑6.2 Astra si
le client le propose. Son tarif Standard court est $8/$40 (cache read $0.40/M) ; ne lui attribue pas
les résultats de l’ancien Astra. Comparer les modèles actuels sur le même harness et le même dépôt.

Compare le **modèle dans son harness réel**, pas un chiffre éditeur isolé. Fable 5.2 est moins cher par token
standard que GPT‑6 Astra, mais l'écart de coût par tâche dépend du caching, de l'effort, des outils et des reprises.

| Axe | GPT‑6 Astra | Claude Fable 5.2 | Conséquence pratique |
|-----|-------------|------------------|---------------------|
| Harness naturel | Codex / ChatGPT Work / Responses API | Claude Code / Messages API | Mesurer le système complet |
| Prix standard input / output (M tokens) | **$10 / $50** | **$8 / $40** | Fable moins cher nominalement |
| Cache read (M tokens) | **$1** | **$0.20** | Avantage Fable sur préfixes réellement réutilisés |
| Long contexte | 1,05M ; surcharge au-delà de 272K | 1M ; tarif standard | Préférer contexte ciblé dans les deux cas |
| Effort | Light→Ultra selon surface ; API low→max | low→max ; adaptive thinking | Fable `high` pour longue autonomie, `low` pour avis ponctuel |
| Computer use | Capable, avec orchestration et outils | Résultats éditeur forts | Vérifier sur scénarios reproductibles |
| Qualité de diff mergeable | Évaluations avec harness Codex | FrontierCode 2.0 : 49,1 % au meilleur effort selon Anthropic | Les protocoles éditeur ne prouvent pas une supériorité générale |
| Indépendance des mesures | Évaluations tierces disponibles | Vals : égalité avec Opus sur Terminal-Bench 4.0, recul en multimodal | Attendre une comparaison Fable 5.2 / Astra à harness comparable |
| ZDR | Clients API éligibles | 30 jours par défaut, exception contractuelle requise | Filtrer les tâches par exigences de confidentialité |
| Missions longues | Async tools, mid-turn steering | Effort par tour, thinking lié à l'historique | Protéger état, outils et règles d'arrêt |

**Lecture des benchmarks.** Anthropic annonce Fable 5.2 devant Astra sur FrontierCode 2.0, FrontierSWE v2 et
OSWorld 2.1, mais ce sont des **résultats éditeur**. Le Coding Agent Index d'Artificial Analysis comparant Claude
Code + Opus 5.5 à Codex + Astra indique un compromis différent entre taux de réussite, coût et durée ; il **ne mesure
pas Fable 5.2**. La comparaison historique Fable 5.1/Astra ne doit plus servir de règle de routage courante.
Les résultats indépendants Vals montrent eux aussi que Fable 5.2 n'est pas systématiquement meilleur qu'Opus 5.5.

Règle de routage pratique :

```text
Micro-dev interactif, humain dans la boucle
→ GPT‑6 Luna High ou Sonnet 5.5 Medium

Issue standard end-to-end
→ GPT‑6.2 Sol Medium
→ Opus 5.5 Medium en review indépendante

Architecture / root cause / refactor difficile
→ Opus 5.5 High
→ GPT‑6.2 Sol Medium/High pour challenger

Sol High insuffisant par limite de capacité
→ GPT‑6.2 Astra Light puis Medium si nécessaire

Opus High insuffisant par limite de capacité
→ Fable 5.2 Low puis Medium si nécessaire

Même tâche vraiment frontier, choix Astra vs Fable
→ deux worktrees / même spec / mêmes tests
→ comparer coût total + minutes humaines + qualité du diff
→ humain arbitre
```

Ne fixe plus un couple permanent « Claude writer / Codex reviewer ». **Le writer se choisit par nature de tâche** :
Sol 6.2 possède généralement l'issue standard ; Opus 5.5 possède plus volontiers l'architecture, le debugging et les
refactors dominés par le jugement. L'autre famille sert alors de reviewer ou de challenger indépendant. Dupliquer les
deux trajectoires complètes n'est justifié que pour un bake-off ou une décision vraiment frontier.

### Côté modèles open-weight chinois (Kimi K3, GLM‑5.2, et le reste du cluster)

Depuis mi-2026, une troisième famille s'est imposée à côté d'Anthropic et d'OpenAI : les modèles **ouverts chinois de
niveau frontier**, qui atteignent un codage agentique proche de Sonnet/Opus à un coût par token très inférieur. Pour un
senior Scala qui pilote déjà Claude Code et Codex, ce ne sont pas des remplaçants du driver quotidien, mais **un levier
de coût sur une classe précise de sous-tâches** et une **option de souveraineté** (self-host) pour le code sensible.

**Piège de catégorie à énoncer d'emblée** : ces modèles ne sont **pas** dans la même catégorie que Qwen3-Coder-Next.
Qwen local (80B/3B actifs) est réellement exploitable sur ton laptop 128 Go : Q4_K_M laisse une marge très large, Q5_K_M
constitue le meilleur défaut et Q6_K reste viable. Q8_0 peut être chargé, mais doit être validé avec le contexte,
IntelliJ et sbt réellement ouverts. GLM‑5.2 (753B) et surtout Kimi K3 (2.8T) ne tiennent **pas** en local sur 128 Go :
ce sont des modèles **API** (Z.ai, Moonshot, OpenRouter) ou **self-host sur serveur multi-GPU**. Moonshot recommande
d'ailleurs un déploiement Kimi K3 sur des configs de 64+ accélérateurs. Ne les mets donc jamais dans la case « Qwen
local » : ils vivent dans la case « API tierce » ou « serveur d'équipe ».

| Modèle      | Éditeur / accès                                                                                                    | Architecture                                                                                             | Contexte                 | Prix API (in / out /M)                | Repère de perf (mesures indépendantes / éditeur)                                                                                             |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Kimi K3** | Moonshot — API, OpenRouter (`moonshotai/kimi-k3`), Kimi Code CLI ; **poids complets publiés** sous licence Kimi K3 | MoE 2.8T total, **104B activés** ; 896 experts, 16 activés ; KDA + Attention Residuals, vision native    | Jusqu'à 1M selon le plan | **$3 / $15** (cache-hit input $0.30)  | Scores éditeur à effort max et avec plusieurs harness ; excellents signaux frontend et long-horizon, à confirmer sur Scala                   |
| **GLM‑5.2** | Zhipu/Z.ai — API OpenAI- **et Anthropic-compatible**, GLM Coding Plan ; checkpoint MIT publié                      | MoE **753B** total en BF16 ; nombre actif non documenté officiellement ; sparse attention « IndexShare » | 1M                       | **$1.40 / $4.40** (cache input $0.26) | Scores éditeur : SWE-bench Pro **62.1**, Terminal-Bench 2.1 81.0 avec Terminus-2 et 82.7 meilleur harness ; à comparer à protocole identique |

**Effort de raisonnement.** GLM‑5.2 expose **High** et **Max**. Kimi K3 expose
`reasoning_effort: low | high | max`. La page modèle/API indique **`max` par défaut**, tandis que Kimi Code peut définir
un défaut différent selon sa version et son plan : fixe donc toujours l'effort explicitement dans un benchmark ou une
automatisation. Le contexte de 1M dépend du plan : 256K sur Moderato, jusqu'à 1M sur Allegretto et au-dessus. Pour une
tâche interactive courte, commence à `low` ou `high` ; réserve `max` aux missions longues où son coût de sortie est
justifié.

#### Où ils entrent dans *ton* routage

```text
✅ Review de volume et triage à faible enjeu   → GLM‑5.2 (High) : tarif token très inférieur à Opus, mais coût par tâche à mesurer
✅ Extraction, classification, PR summaries bulk → GLM‑5.2 ou Kimi K3, en batch, quand le volume rend Sonnet/Terra cher
✅ Génération frontend / maquette web           → Kimi K3 (#1 Frontend Code Arena) si tu sors du périmètre Scala pur
✅ Second avis open-weight indépendant          → un modèle d'une 3e « école » d'entraînement casse les angles morts communs Claude/GPT
✅ Code sensible / air-gapped / souveraineté     → GLM‑5.2 en self-host (poids MIT) : rien ne sort de ton infra
```

```text
❌ Driver quotidien Scala à la place de Sonnet 5.5 : capable, mais tu perds l'écosystème (Claude Code, subagents, Metals MCP mûrs)
❌ Tâche interactive courte sur Kimi K3 en effort max : latence et verbosité, mauvais achat ; utiliser low/high
❌ Décision d'architecture critique en solo : garde Opus/Fable ou un vrai second avis Sol ; l'open-weight y reste un challenger, pas l'arbitre
❌ « Remplacer » Qwen local : mauvaise catégorie (voir piège ci-dessus)
```

#### Accès occasionnel à GLM via OpenRouter

Pour ce workflow, ne rajoute pas un abonnement GLM dédié par défaut. **GLM reste un modèle de secours**, à appeler via
OpenRouter lorsque Claude Code, Codex et Qwen local n'ont pas permis de résoudre le problème. Cela préserve la diversité
de modèles sans ajouter un nouveau compte, une nouvelle clé et un nouveau plan à suivre.

Si GLM devient un outil utilisé chaque semaine ou apporte un gain mesurable sur une classe de tâches, réévalue alors
l'intérêt d'un accès direct Z.ai. Tant que ce seuil n'est pas atteint, la simplicité prime.

#### Le reste du cluster (pour situer, pas pour tout adopter)

`MiniMax M3` (juin 2026) est le premier open-weight à combiner codage frontier, contexte 1M *et* multimodalité native
(tête de l'open-weight sur SWE-bench Pro à 59.0 avant GLM‑5.2). `DeepSeek V4` décline un V4 Pro et un V4 Flash
(≈ $0.14/$0.28 /M) imbattables sur le rapport coût/contexte long pour du triage massif. Aucun n'est « le meilleur
partout » : la scène open-weight de mi-2026 est un cluster serré où le bon choix dépend de la tâche et du prix, pas d'un
classement global.

#### Deux réserves à garder en tête

1. **Provenance et distillation.** Kimi K3 s'est identifié comme « Claude » dans au moins un échange rapporté. Cette
   auto-identification anecdotique **n'est pas une preuve de distillation** et ne permet aucune conclusion scientifique
   ou contractuelle sur les données d'entraînement. Si la provenance compte pour un client, exige une documentation de
   l'éditeur et traite l'information comme inconnue tant qu'elle n'est pas publiée.
2. **Méthodologie de benchmark.** Les tables éditeur mélangent des harness différents (KimiCode, Claude Code, Codex,
   mini-SWE-agent) et K3 est sensible à la préservation de l'historique de *thinking*. Les écarts affichés sont souvent
   inférieurs à un point : ils ne survivent pas toujours à un changement de harness. Règle inchangée : **bake-off
   contrôlé sur tes vraies tâches** (versions figées, permissions fixes, tests d'acceptation déterministes, coût par
   changement accepté), pas adoption sur la foi d'un classement.

#### Protocole de bake-off Scala : Kimi K3 contre GLM‑5.2

Ne compare pas seulement les réponses finales. Utilise au minimum **15 tâches privées**, jamais publiées, réparties
entre :

```text
3 bugs Scala 3 subtils : givens, implicits, variance, types opaques
3 évolutions Play / Tapir / Pekko sur 3 à 8 fichiers
3 tâches Spark / concurrence / performance
3 reviews de PR avec défauts injectés connus
3 tâches de tests : ScalaTest, ScalaCheck, mutation testing
```

Protocole : même commit, même worktree initial, mêmes outils, même limite de temps, même réseau, même paquet de
contexte, mêmes critères d'arrêt et **trois répétitions par tâche**. Kimi doit être testé séparément en `high` et `max`;
GLM en
`High` et `Max`. Si les harness ne peuvent pas être identiques, publie deux matrices et n'attribue pas l'écart au seul
modèle.

Mesures obligatoires :

```text
- tâche acceptée par les tests et la review humaine ;
- compilation, tests ciblés, mutation score ;
- défauts de sécurité ou de contrat détectés ;
- lignes ajoutées / supprimées et fichiers touchés ;
- nombre de reprises, tool calls et boucles identiques ;
- tokens input, cache, reasoning et output ;
- coût API total, latence et minutes humaines jusqu'au merge ;
- taux de réussite pass@1 et stabilité sur trois runs.
```

Adopte GLM ou Kimi sur un flux seulement s'il réduit le coût par changement accepté **sans** dégrader les garde-fous. Un
score éditeur supérieur mais davantage de corrections humaines est une régression, pas un gain.

## Règle de décision par tâche

### Quand utiliser **Fable 5.2** (Mythos-class)

Fable 5.2 coûte deux fois Opus 5.5 par token ($8/$40 contre $4/$20). Anthropic recommande de commencer par **Opus 5.5 `medium`**, de
monter vers `high`, puis de réserver Fable 5.2 aux evals encore insuffisantes ou au vrai long-horizon. Pour une escalade
de capacité, teste **Fable `low`** avant de pousser systématiquement Opus à `Extra`/`Max` :

```text
✅ Migration complète d'un framework (Play 2 → 3, Pekko, Spark upgrade)
✅ Session autonome multi-heures / multi-jours sans supervision
✅ Refactor cross-modules sur > 10 fichiers interdépendants
✅ Débogage d'un bug métier dont la cause est très loin du symptôme
✅ Décision architecturale sans "bonne réponse évidente" après essai Opus 5.5 High
✅ Tâche où tu paierais sinon un senior engineer une demi-journée
```

```text
❌ Tâche bien scoped et bornée : Sonnet 5.5 ou Opus 5.5 sont de meilleurs achats
❌ Revue de diff ou PR summary : overkill, coût inutile
❌ Génération de boilerplate ou de fixtures : Qwen ou Haiku suffisent
❌ One-liner ou patch ciblé : Luna High, Sonnet 5.5 Medium ou Aider
❌ Tâche dure mais interactive avec toi dans la boucle : Opus 5.5 Medium/High suffit généralement
```

> **Positionnement 5.2.** Anthropic recommande de conserver **Opus 5.5 comme point de départ** pour la plupart des
> workloads. Fable 5.2 `low` est un **advisor ponctuel**, à évaluer sur une tâche bornée et vérifiable ; pour une mission
> réellement autonome, commence à `high` afin de réduire les fins de tour prématurées. Mesure le **coût par changement
> accepté** sur le benchmark Scala privé, plutôt que de généraliser les résultats du fournisseur. Le cache read à
> $0.20/M améliore l'économie des longs préfixes stables. Lorsque le vérificateur est fiable, teste aussi le schéma
> **Low → retry High sur échec** en incluant reprises, latence, review et validation humaine.

### Prompting Fable 5.2 : structurer une mission longue

Fable 5.2 (fenêtre 1M, sortie jusqu'à 128K) n'est pas un simple Opus plus fort. Il vise le raisonnement exigeant
et le long-horizon lorsque les évaluations Opus restent insuffisantes. La continuité des thinking blocks et la stabilité
des définitions d'outils deviennent des contraintes du harness, en plus de l'effort configurable par message. Référence :
`https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2`. Les leviers
ci-dessous restent valables pour 5.2 ; les points propres à 5.2 (propriété du code, sur-délégation, fins de tour
prématurées, historique append-only, instructions héritées à purger) sont détaillés dans la note Fable 5.2 de la
section « Côté Anthropic ».

Cinq leviers spécifiques :

1. **Charte de mission en tête de contexte, cachée.** Le bloc initial (objectif, non-objectifs, invariants, règles
   d'arrêt) ne doit jamais changer entre les tours : il bénéficie du prompt caching et sert d'ancre anti-dérive sur les
   sessions longues. Tout ce qui évolue (état, erreurs, diffs) va après.
2. **État persistant explicite.** Sur une mission multi-heures, exige un fichier d'état (`MIGRATION_STATE.md` dans le
   worktree) que le modèle met à jour à chaque jalon : modules traités, modules restants, décisions prises, blocages.
   C'est ce fichier — pas la conversation — qui fait foi en cas de compaction de contexte ou de reprise.
3. **Checkpoints avec critère de sortie.** Découpe la mission en jalons vérifiables par des commandes déterministes
   (`compile`, tests ciblés, scalafmtCheckAll). Pas de passage au jalon suivant sans jalon courant vert.
4. **Route l'effort par tour sans changer de modèle.** Utilise `medium/high` pour l'exploration, `xhigh/max` pour une
   décision réellement difficile, puis `low/medium` pour une édition mécanique. Le per-message effort préserve le cache
   et évite de payer le niveau maximal pendant toute la trajectoire.
5. **Si une compaction est nécessaire, impose son contrat de résumé.** Demande de préserver explicitement problèmes et
   résolutions, pistes essayées ou écartées, décisions et contraintes, état courant, points ouverts et détails
   difficiles à reconstruire. La compaction serveur gère déjà ce besoin ; pour une compaction côté client, ne résume
   jamais en prose libre sans ces champs.

Gabarit de mission Fable 5.2 :

```text
# MISSION (statique — ne pas modifier en cours de session)
Objectif : [migration / refactor précis]
Non-objectifs : [ce qui est explicitement hors scope]
Invariants : API publiques, contrats JSON, comportements listés dans AGENTS.md
Durée max : [N heures] — Coût max : [N USD] — Diff max par jalon : [N lignes]

# RÈGLES D'ARRÊT (statique)
Stop et rapport immédiat si :
- un invariant doit être violé pour avancer ;
- le même jalon échoue 2 fois pour des causes différentes ;
- build.sbt, migration DB ou contrat public doit changer ;
- l'estimation de durée restante dépasse 2x l'estimation initiale.

# PROTOCOLE (statique)
1. Lire AGENTS.md et MIGRATION_STATE.md.
2. Traiter UN jalon : plan court → diff → compile → tests ciblés.
3. Mettre à jour MIGRATION_STATE.md et committer le jalon.
4. Rapport de progression : jalon terminé, jalons restants, risques nouveaux, écart au plan.
5. Reprendre en 2.

# ÉTAT (dynamique — joindre la version courante de MIGRATION_STATE.md)
[état]
```

> **Continuité Fable 5.2.** Ne rétrograde pas silencieusement une session : Fable 5.1 et Opus 5.5 ne relisent pas les
> thinking blocks de Fable 5.2. N'édite pas non plus les anciens messages, le préfixe système ou la liste des outils
> en réutilisant ces blocs : le contrôle de cohérence peut produire une erreur 400. Si un changement d'outils ou de
> modèle est indispensable, sauvegarde l'état utile dans `MIGRATION_STATE.md`, puis repars avec un contexte propre.
> `tool_choice: any/tool` est interdit sur Fable 5.2 ; utilise `auto` et valide le résultat avec un schéma strict.

> **Note opérationnelle** : une bascule de sécurité peut changer le modèle réellement exécuté. Si la mission touche du
> code crypto ou sécurité bas niveau, logge ce modèle, vérifie qu'il conserve le niveau de capacité attendu et prévois
> ce cas dans la règle d'arrêt plutôt que de le découvrir en cours de session.

### Quand utiliser **Opus 5.5**

C'est le **défaut Claude Code pour l'agentic coding autonome**. Son effort par défaut est `medium`, ce qui change le
routage par rapport à Opus 5 : commence à `medium`, monte à `high` quand la tâche est difficile, puis n'utilise
`Extra` (`xhigh`) ou `Max` que si la durée ou les evals le justifient.

```text
✅ Issue complète quand Claude possède la trajectoire exploration → patch → tests
✅ Architecture, migration et plan multi-modules
✅ Root cause éloignée du symptôme, implicits/givens/effets difficiles
✅ Gros refactor où la cohérence globale domine la simple édition
✅ Review indépendante d'une PR écrite par Codex
✅ Orchestration de sous-agents read-heavy avec contexte isolé
```

```text
medium → défaut agentique
high   → debugging / architecture / long-horizon difficile
Extra  → >30 min et chaîne réellement longue ; pas pour une simple tâche "importante"
Max    → exceptionnel, qualité absolue prioritaire et gain mesuré
```

### Quand utiliser **Sonnet 5.5**

Le meilleur choix Claude quand **le senior garde fortement la main** ou quand la tâche agentique est bien spécifiée.
Anthropic recommande explicitement `medium` pour le coding agentique et l'usage multistep d'outils bien cadrés, puis
`high` pour les tâches plus longues ou difficiles.

```text
✅ Petit bug reproductible
✅ Refactor local bien scoped
✅ Tests métier et property-based tests ciblés
✅ Stack trace → diagnostic → correctif
✅ Feature claire dont l'architecture est déjà décidée
✅ Worker d'implémentation derrière un plan humain ou Opus
```

```text
low    → transformation simple / latence prioritaire
medium → défaut micro-dev et agentic coding bien spécifié
high   → tâche plus longue ou plus difficile
Extra / Max → seulement si tes evals montrent un gain ; sinon passer à Opus 5.5
```

La règle économique n'est donc plus « Sonnet à effort maximal avant Opus ». Si Sonnet High échoue pour une limite de
capacité, **Opus Medium** est souvent un meilleur achat qu'un Sonnet Extra/Max prolongé.

### Quand utiliser **Haiku 5.5**

Systématiquement pour les tâches *haute fréquence et faible risque* :

```text
✅ Sous-agents de lecture ou extraction à faible risque (sortie vérifiable)
✅ Résumés de logs, PR summaries rapides
✅ Classification et routage
✅ Éditions ciblées < 20 lignes
✅ Génération de messages de commit
✅ Appels répétitifs à faible risque, si le benchmark confirme le gain
```

> **Haiku 5.5 remplace Haiku 4.5 comme worker Claude.** Il coûte **$0.10/$0.50** tant que le prompt
> reste sous 100 000 tokens (cache read $0.01/M), soit **dix fois moins que Haiku 4.5** et le même ordre de prix que
> GPT‑6 Luna ; au-delà de 100K tokens d'entrée, cache compris, le tarif passe à $0.50/$2.50. Contexte 1M, sortie 128K,
> adaptive thinking actif par défaut et **paramètre `effort` supporté (`medium` par défaut)**. Pièges de migration :
> le prefill renvoie désormais 400, `temperature`/`top_p`/`top_k` sont à omettre, `budget_tokens` renvoie 400, le
> thinking compte dans `max_tokens`, et un `tool_choice` forcé reste accepté mais supprime la réflexion avant l'appel.
> Le tokenizer compte environ 30 % de tokens de plus que Haiku 4.5. Règle pratique : garde les contrats de subagents
> **sous 100K tokens** pour rester dans le palier bas, ce qui rejoint la discipline d'isolation de la section 3.
> Haiku 4.5 reste actif, mais son retrait est désormais possible à tout moment avec le préavis habituel de 60 jours.

### Quand utiliser **GPT‑6 Luna**

```text
✅ Micro-dev : modification locale dont tu contrôles la direction
✅ Tests simples, fixtures, boilerplate, renommages et transformations mécaniques
✅ Recherche d'occurrences, résumés, logs et PR summaries
✅ Worker/subagent dont la sortie est vérifiée immédiatement
```

OpenAI recommande de commencer Luna à **High**. N'essaie pas de transformer Luna en agent frontier avec Extra High : si
la tâche devient ambiguë ou conceptuelle, passe à Sol 6.2 plutôt que de payer de longues reprises sur un modèle trop
petit.

### Quand utiliser **GPT‑6.2 Sol**

```text
✅ Issue standard complète : découverte → implémentation → tests → PR
✅ Feature multi-fichiers et bug non trivial
✅ Review indépendante d'une PR écrite par Claude
✅ Migration bornée, compatibilité et refactor transversal
✅ Second avis sérieux sur une architecture proposée par Opus
```

```text
Light       → issue très bien spécifiée, patch local, reproduction claire
Medium      → défaut agentique quotidien
High        → feature complexe, root cause difficile, migration, beaucoup de cas limites
Extra High  → capacité suffisante mais besoin réel de davantage d'analyse/vérification
Ultra       → uniquement si le travail se décompose en investigations indépendantes
```

### Quand utiliser **GPT‑6.2 Astra**

```text
✅ Sol High échoue parce que la capacité/jugement manque, pas parce que le contexte est pollué
✅ Sécurité, auth, contrat critique ou décision où une mauvaise direction coûte plusieurs reprises
✅ Workflow end-to-end très ambigu avec nombreux outils / computer use
✅ Reviewer frontier ponctuel sur une décision à fort impact
```

Commence par **Astra Light**. Pour une tâche réellement frontier, Astra Light peut coûter moins cher au total qu'un Sol
Extra High suivi d'une reprise, parce qu'il évite une mauvaise trajectoire. Monte à Medium/High seulement si
nécessaire ; Extra High/Ultra restent exceptionnels.

### Quand utiliser **le mode `ultra` dans ChatGPT Work / Codex**

```text
✅ Cartographie codebase-scale d'une application legacy
✅ Migration multi-modules en worktree dédié
✅ Audit architecture + tests + sécurité + performance en parallèle
✅ Décomposition d'un refactor en micro-PRs
✅ Mission où plusieurs sous-analyses indépendantes apportent une vraie valeur
```

```text
❌ One-shot “réécris proprement”
❌ Tâche interactive courte
❌ Repo mal testé sans limite de diff
❌ Modification directe de fichiers critiques sans plan validé
```

Dans cette sous-section, `ultra` désigne le **mode d'orchestration multi-agent du produit**, et non le niveau d'effort
`ultra` que certains SDK Codex exposent désormais. Il convient aux volets indépendants ; évite-le lorsque les agents
écrivent dans le même état mutable ou lorsqu'une seule opération lente domine la tâche. Sur une application legacy,
commence par cartographier, produire un registre de dette, proposer des tests de caractérisation, puis découper en
micro-PRs. Ne commence pas par écrire du code.

Gabarit minimal pour une mission `ultra` :

```text
Tu interviens comme équipe de reviewers/agents sur une application legacy Scala.

Rôles à simuler :
- architecte legacy ;
- tech lead Scala ;
- reviewer sécurité défensive ;
- QA / test engineer ;
- maintainer sceptique.

Objectif :
[objectif précis]

Contraintes :
- aucun changement de comportement observable sans validation ;
- pas de modification build.sbt / migrations DB / contrats JSON publics sans stop ;
- micro-PRs de moins de 300 lignes modifiées ;
- tests de caractérisation avant refactoring ;
- chaque conclusion doit citer les fichiers observés ;
- distinguer faits, hypothèses et recommandations.

Sortie attendue :
1. carte du périmètre ;
2. risques ;
3. registre de dette ;
4. tests de caractérisation prioritaires ;
5. plan en micro-PRs ;
6. première PR proposée, sans l'appliquer tant que le plan n'est pas validé.
```

## Matrice de sélection modèle rapide

```text
Micro-dev, humain garde le contrôle      → GPT‑6 Luna High / Sonnet 5.5 Medium
Worker lecture / triage à faible risque  → Haiku 5.5 / Qwen local / GPT‑6 Luna
Patch local au jugement intermédiaire    → GPT‑6.1 Terra Medium
Issue standard end-to-end                → GPT‑6.2 Sol Medium
Agent Claude end-to-end                  → Opus 5.5 Medium
Feature / bug difficile                  → GPT‑6.2 Sol High ou Opus 5.5 High selon nature
Architecture / root cause dominante      → Opus 5.5 High
Review croisée                           → famille opposée à l'auteur, Medium par défaut
Suivi post-PR Codex                       → GPT‑6.2 Sol Medium (Goal / Heartbeat / Cloud)
Sol High insuffisant                     → GPT‑6.2 Astra Light
Opus High insuffisant                    → Fable 5.2 Low
Long-horizon séquentiel > 30 min         → Opus 5.5 Extra (`xhigh`)
Codebase-scale parallélisable            → GPT‑6.2 Sol Ultra, surtout read-heavy
Frontier absolu                          → Astra Medium+ / Fable Medium+ après preuve du besoin
```

Règle pratique :

```text
Le senior garde la direction → modèle rapide et économique.
L'agent possède la trajectoire → Sol 6.2 ou Opus 5.5.
La compréhension domine le patch → privilégier Opus.
L'exécution end-to-end domine → privilégier Sol 6.2.
Une limite de capacité apparaît → Astra Light ou Fable Low avant l'effort extrême du tier inférieur.
Ultra uniquement si le problème contient plusieurs axes réellement indépendants.
```

## Routage automatique des tâches de développement

La matrice de sélection ne doit pas rester uniquement manuelle. Pour éviter de brûler des crédits sur des tâches simples
ou, inversement, d'envoyer une tâche critique à un modèle trop faible, ajoute une étape explicite de routage avant
chaque tâche agentique.

Le principe n'est pas de choisir le modèle le plus intelligent, mais le plus petit modèle capable de produire un
résultat mergeable avec un risque acceptable.

```text
Demande / ticket / stack trace
→ classification de tâche
→ estimation difficulté + risque
→ sélection du modèle minimal acceptable
→ exécution avec permissions limitées
→ tests déterministes
→ escalade si échec
→ log coût / qualité
```

### Architecture recommandée

```text
CLI / IDE / ticket
→ task-classifier
→ context-builder
→ model-router
→ agent-runner
→ test-runner
→ reviewer
→ cost-quality log
```

| Composant          | Rôle                                                         | Modèle / outil recommandé                                                                             |
|--------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `task-classifier`  | Classer la tâche, le risque et la difficulté                 | **Jev** si la sortie est fermée ; Qwen local / Haiku si un raisonnement ouvert est nécessaire         |
| `context-builder`  | Trouver fichiers, relations, tests, docs et commandes utiles | Sourcebot, ScalaSemantic MCP, Codebase-Memory MCP si polyglotte, rg, IntelliJ, Metals MCP, Context7   |
| `model-router`     | Choisir le plus petit modèle acceptable                      | Règles déterministes + Jev comme signal probabiliste ; OpenRouter seulement pour escalade ponctuelle  |
| `agent-runner`     | Exécuter avec les bonnes permissions                         | Codex, Claude Code subagents, Aider, OpenCode, Qwen Code                                              |
| `test-runner`      | Valider de manière déterministe                              | sbt, IntelliJ, Metals MCP, CI                                                                         |
| `reviewer`         | Relire sans écrire                                           | Famille opposée au writer : Opus 5.5 Medium ou GPT‑6.2 Sol Medium ; Astra/Fable seulement si critique |
| `cost-quality log` | Mesurer coût, qualité, retours review et reprises            | Scripts locaux, tableau de suivi                                                                      |

### Jev : decision layer, pas coding model

**Jev 1.14 (`jev-1.14.0`)** est le modèle System One courant de TypeSafe AI. Il ne génère ni texte ni code : il reçoit
un `state` et des questions typées, puis renvoie directement des décisions probabilistes. Le bon modèle mental est un
**« smart if » sémantique** : entrée ouverte, branches définies par le développeur.

| Primitive | Usage                                                           |
|-----------|-----------------------------------------------------------------|
| `Choice`  | choisir parmi des options fermées : modèle, agent, skill, route |
| `Score`   | noter sur une échelle ordonnée : risque, pertinence, priorité   |
| `Noul`    | estimer la probabilité qu’une proposition soit vraie            |

Jev 1.14 coûte **$0.042/M tokens input** et ne facture pas la sortie. Le régime standard accepte **64K tokens par
requête** et **32K pour `state` + la question la plus longue** ; les limites de débit dépendent de l'organisation et
se lisent dans la console. Un contexte expérimental plus long et les entrées image existent sous conditions, sans devenir
le défaut du routeur. `jev-latest` pointe vers `jev-1.14.0` : **épingle la version** dès que tu calibres des seuils,
car le changement de distribution peut invalider les seuils de risque.

> **OpenAI Decisions API.** Endpoint `POST /v1/decisions`, désormais généralement disponible sur `gpt-6-luna`, avec
> réponses typées `predicate`, `choice` et `score`. Jusqu'à **400 questions** peuvent partager une même entrée ; texte,
> images et données structurées sont supportés selon le champ. Prix standard : **$0.10/M tokens d'entrée**, **$0.01/M
> tokens d'entrée en cache lu**, aucune facturation de sortie ; les écritures de cache, entrées longues et traitements
> régionaux suivent leurs tarifs. Pour le `task-classifier` et le `model-router`, compare Decisions et Jev sur les mêmes
> questions avec une calibration par tâche et par risque, jamais sur le seul prix du token.

Dans ce workflow, les meilleurs candidats sont :

```text
✅ task / risk / difficulty classification
✅ model routing : Luna / Sol / Astra / Sonnet / Opus / Fable
✅ sélection progressive de quelques skills parmi un gros catalogue
✅ triage des résultats de subagents et pertinence d’un contexte
✅ signal topic-shift / « faut-il envisager une compaction ? »
✅ filtrage de notifications et décisions qui méritent l’attention humaine

❌ écrire ou expliquer du Scala
❌ architecture ou root-cause ouverts
❌ calcul, comptage ou comparaison de dates
❌ décider seul d’un push, déploiement, suppression, secret ou migration DB
```

Architecture recommandée :

```text
règles déterministes
→ Jev pour un jugement fermé et fréquent
→ code combine probabilités + seuils
→ LLM génératif si raisonnement ouvert ou confiance insuffisante
→ humain si action critique ou irréversible
```

**Type-safe ≠ correct.** L’argument « zero hallucinations » signifie surtout que Jev ne sort pas d’une structure ou d’un
ensemble d’options déclaré ; il peut toujours sélectionner la mauvaise option. Une évaluation indépendante sur **346 009
requêtes / 37 datasets** trouve des probabilités `Choice` bien calibrées, mais montre aussi qu’un seuil universel de
`0.5`
est mauvais pour certaines tâches binaires : les seuils doivent être **calibrés par tâche et par risque**.

Trois règles d’intégration :

1. **Le code garde l’autorité.** Les signaux déterministes (`touches_security`, fichier critique, action destructive)
   priment toujours sur Jev.
2. **État minimal.** Jev subit lui aussi le *context rot* ; filtre avant l’appel et n’envoie que ce qui change
   réellement la décision.
3. **Teste la stabilité.** Sur `Choice`, réordonne ponctuellement les options ; des évaluations de `jev-1.13`
   signalent une sensibilité possible à l’ordre, à revalider sur `jev-1.14.0`. Le `state` adversarial peut aussi influencer la réponse : Jev est un signal, pas une sandbox.

### Classification minimale

Le routeur doit produire une décision structurée, pas une réponse libre. Exemple de sortie attendue :

```json
{
  "task_type": "implementation | debug | test | review | migration | architecture | boilerplate | research",
  "risk": "low | medium | high | critical",
  "difficulty": "trivial | simple | normal | hard | frontier",
  "expected_files": "1 | 2-5 | 6-10 | 10+",
  "requires_code_write": true,
  "requires_external_docs": false,
  "touches_public_api": false,
  "touches_json_contract": false,
  "touches_database": false,
  "touches_build": false,
  "touches_security": false,
  "touches_concurrency": false,
  "model": "qwen | haiku55 | sonnet55 | opus55 | fable52 | gpt6_luna | gpt61_terra | gpt62_sol | gpt62_astra | gpt61_sol | gpt6_astra",
  "reasoning_effort": "light | low | medium | high | extra | xhigh | max | ultra | null",
  "reasoning_mode": "standard | pro | null",
  "multi_agent": false,
  "max_parallel_agents": 3,
  "max_cost_usd": 0.0,
  "max_duration_minutes": 0,
  "confidence": 0.0,
  "escalation_rule": "string",
  "stop_conditions": [
    "string"
  ]
}
```

**Hiérarchie des signaux** : les critères déterministes (`touches_*`, `expected_files`, taille de diff attendue) sont
les déclencheurs *primaires* de routage et d'escalade. Si la classification vient de **Haiku/Qwen**, `confidence` reste
une auto-estimation secondaire et mal calibrée. Si elle vient de **Jev**, utilise la distribution et la `confidence`
retournées, mais avec un **seuil calibré par question et par niveau de risque**, jamais un `0.75` universel. Dans les
deux cas, une confiance élevée ne doit jamais *désescalader* un signal déterministe critique.

`reasoning_effort` doit être normalisé par surface : Claude utilise `low | medium | high | xhigh | max` sur les modèles
compatibles, avec **Opus 5.5 et Haiku 5.5 `medium`** par défaut ; Codex affiche **Light | Medium | High |
Extra High | Ultra**, tandis que l'API OpenAI expose des valeurs `low | medium | high | xhigh | max`
selon modèle. `multi_agent` reste une décision d'orchestration distincte. L'effort est un levier de qualité et de coût,
mais un tier supérieur à faible effort peut être moins cher au total qu'un tier inférieur poussé à l'extrême.

### Matrice de routage automatique

| Signal détecté                                               | Modèle initial                | Escalade                                                                      |
|--------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------|
| Résumé, triage, grep, logs simples                           | Haiku 5.5 / Qwen              | Sonnet 5.5 Medium si ambigu                                                   |
| Boilerplate, DTO, fixtures, édition mécanique                | GPT‑6 Luna High               | Sonnet 5.5 Medium si types/domaine subtils                                    |
| Test simple ou non-régression localisée                      | GPT‑6 Luna High               | Sonnet 5.5 Medium si règle métier importante                                  |
| Patch ciblé, humain garde la direction                       | Luna High / Sonnet 5.5 Medium | Sol 6.2 Light/Medium si exploration nécessaire                                |
| Patch borné avec jugement intermédiaire                      | GPT‑6.1 Terra Medium           | GPT‑6.2 Sol Medium si exploration nécessaire |
| Feature métier bornée, 1 à 5 fichiers                        | GPT‑6.2 Sol Medium            | Sol High si difficulté ; Opus Medium en review                                |
| Feature 5 à 10 fichiers avec invariants                      | GPT‑6.2 Sol Medium/High       | Opus 5.5 High si architecture/root cause domine                               |
| Bug Scala subtil, implicits, givens, effets                  | Opus 5.5 High                 | Sol High pour hypothèse indépendante ; Fable Low si capacité insuffisante     |
| Migration multi-modules bornée                               | GPT‑6.2 Sol High              | Opus High en review ; Astra Light si Sol plafonne                             |
| Refactor codebase-scale                                      | Opus 5.5 High                 | Extra si long-horizon ; Fable Low si Opus plafonne                            |
| Review d'une PR Codex                                        | Opus 5.5 Medium               | High si risque critique                                                       |
| Review d'une PR Claude                                       | GPT‑6.2 Sol Medium            | High puis Astra Light si risque frontier                                      |
| Suivi autonome d'une PR Codex                               | GPT‑6.2 Sol Medium            | High si diagnostic difficile ; Sol 6.1 Medium si 6.2 indisponible             |
| Sécurité / auth / contrat critique                           | GPT‑6.2 Astra Light + humain    | Astra Medium/High + review Opus High                                          |
| Axes read-heavy indépendants                                 | GPT‑6.2 Sol Ultra             | Astra Ultra seulement si la capacité supplémentaire est réellement nécessaire |
| Changement `build.sbt`, dépendances, DB, contrat JSON public | Pas d'auto-écriture           | Plan + validation humaine                                                     |

### Politique d'escalade

Le routage automatique doit fonctionner comme une cascade contrôlée :

```text
Micro-boucle vérifiable : Qwen / Haiku / GPT‑6 Luna High / Sonnet 5.5 Medium
→ ownership agentique : GPT‑6.2 Sol Medium / Opus 5.5 Medium
→ difficulté : Sol High / Opus High
→ limite de capacité : Astra Light / Fable Low
→ effort supérieur seulement si la capacité est suffisante mais le raisonnement manque
→ Ultra seulement si parallélisable
→ humain
```

**Ne change pas simplement de modèle au milieu d'une conversation qui déraille.** Si l'échec vient d'une trajectoire
polluée — hypothèse fausse répétée, hallucinations qui s'accumulent, corrections qui recréent d'autres erreurs — le
contexte est lui-même une partie du problème. Avant Sonnet 5.5 → Opus 5.5, Sol 6.2 → Astra ou Opus 5.5 → Fable 5.2 :

```text
1. Stop write mode.
2. Produire HANDOFF.md : objectif, état du diff, faits vérifiés, essais échoués, erreur actuelle, inconnues.
3. Ouvrir une session fraîche avec seulement spec + AGENTS.md + HANDOFF.md + fichiers/diff pertinents.
4. Escalader le modèle dans cette nouvelle session si la difficulté le justifie toujours.
```

L'escalade de **capacité** est utile sur un problème proprement posé ; elle ne doit pas transporter la dette
conversationnelle d'une session déjà biaisée.

Escalade automatiquement si :

```text
- un signal déterministe critique est présent (touches_* sensible, diff hors gabarit) ;
- auto-confidence LLM < 0.75, ou confidence Jev sous le seuil calibré pour cette décision ;
- erreur de compilation identique 2 fois ;
- test ciblé toujours rouge après 2 corrections ;
- diff hors scope ;
- plus de fichiers modifiés que prévu ;
- plus de 300 lignes de diff inattendues ;
- build.sbt, plugins.sbt, migration DB ou contrat JSON public est touché ;
- API publique modifiée ;
- le routeur détecte sécurité, concurrence, performance ou argent ;
- le modèle déclare explicitement une incertitude forte ;
- le coût estimé d'une erreur dépasse le coût du modèle supérieur.
```

Interromps (sans escalader automatiquement) si :

```text
- max_cost_usd est atteint (budget local) ;
- max_duration_minutes est atteint (timeout wall-clock) :
  une session agentique qui boucle est un mode de défaillance distinct d'une session qui échoue,
  et l'escalade vers un modèle plus cher ne corrige pas une boucle.
```

Désescalade automatiquement si :

```text
- tâche purement textuelle ;
- aucun write mode nécessaire ;
- pas de risque métier ;
- moins de 20 lignes attendues ;
- fichier unique ;
- objectif déterministe ;
- test existant très ciblé ;
- contexte stable et déjà connu du projet.
```

### Règles de non-automatisation

Ne laisse jamais un routeur décider seul d'une écriture sur :

```text
- build.sbt ;
- plugins.sbt ;
- resolvers ;
- versions de dépendances ;
- migrations DB ;
- contrats JSON publics ;
- sécurité ;
- authentification ;
- autorisation ;
- concurrence ;
- gestion d'argent ;
- suppression de données ;
- scripts de déploiement ou d'infrastructure.
```

Dans ces cas, le routeur peut seulement proposer :

```text
- modèle recommandé ;
- plan ;
- fichiers probables ;
- tests à exécuter ;
- risques ;
- règle d'arrêt.
```

### Subagents Claude Code recommandés

**Calibration Codex 6.2.** Pour un parent GPT‑6.2 Sol ou Astra, pars avec le même modèle et le même effort pour
les subagents (recommandation officielle OpenAI). Réduis ensuite le tier des tâches réellement mécaniques, à
sortie contrôlable : Luna/Haiku pour grep, extraction, logs et résumés ; Sol/Opus pour invariants, architecture et
root cause. Le même principe de mesure vaut côté Claude. Un reviewer de l’autre famille reste une session
indépendante, pas un worker moins coûteux de l’auteur.

Claude Code est le meilleur endroit pour appliquer ce routage au quotidien, car les subagents peuvent avoir leur propre
contexte, leurs outils et leurs permissions.

```text
researcher
- Modèle : Haiku / Qwen si externe
- Mode : read-only
- Rôle : trouver fichiers, usages, tests, documentation

scala-implementer
- Modèle : Sonnet 5.5 `medium`
- Mode : write limité au repo
- Rôle : implémenter les tâches bornées sous contrôle d’un plan clair

hard-debugger
- Modèle : Opus 5.5 `high`
- Mode : write limité, plan obligatoire
- Rôle : bugs Scala subtils, implicits, effets, causes éloignées

migration-planner
- Modèle : Opus 5.5 `high` ; Fable 5.2 `low` (décision ponctuelle) ou `high` (mission longue) si Opus plafonne
- Mode : plan-first, worktree dédié
- Rôle : migrations multi-modules, refactors longs, stratégie de découpage
- Note : évaluer Dynamic Workflows (Opus 5.5 + subagents parallèles massifs)
  comme alternative à un Fable mono-agent sur les migrations codebase-scale

reviewer
- Modèle : Codex / GPT‑6.2 Sol `medium` ; Astra `light` si critique
- Mode : no-write
- Rôle : review indépendante, classement bloquant / important / optionnel

pr-summarizer
- Modèle : Qwen / GPT‑6 Luna
- Mode : no-write
- Rôle : résumé PR, release notes, checklist finale
```

#### Isolation de contexte : rôle principal des subagents sur les tâches longues

Le gain des subagents n'est pas seulement le parallélisme. Chaque sous-agent travaille dans une **fenêtre de contexte
fraîche et isolée** ; le parent n'a donc pas besoin d'accumuler les recherches, logs, fichiers écartés et impasses de
chaque sous-tâche. Cette isolation protège le contexte principal contre le *context rot*.

Le partage recommandé est :

```text
PARENT
- objectif
- contraintes et non-objectifs
- plan validé
- décisions prises
- diff courant
- preuves essentielles
- risques ouverts

SUBAGENTS
- exploration de nombreux fichiers
- recherche Sourcebot / rg
- call paths, hiérarchies, usages et chaînes de givens via ScalaSemantic
- graphe structurel cross-language via Codebase-Memory si Java/Kotlin/Scala cohabitent
- investigation live des types / givens / diagnostics via Metals
- documentation externe
- logs et suites de tests volumineuses
- cartographie d'un module legacy
```

Règle de décision :

```text
Les détails de cette sous-tâche seront-ils encore utiles au parent après sa fin ?

NON → subagent isolé
OUI → garder dans le contexte parent
```

Le message de délégation doit être un **contrat**, car le subagent ne doit pas dépendre de tout l'historique
conversationnel du parent :

```text
Mission :
[périmètre précis]

Mode :
read-only / write borné

Cherche :
[questions précises]

Ne fais pas :
[hors scope]

Retourne uniquement :
1. conclusion ;
2. preuves file:line ;
3. tests ou commandes pertinents ;
4. incertitudes restantes.

Réponse cible : < 1–2K tokens.
```

Le retour est une interface, pas un transcript. Si un sous-agent lit 80K tokens et en renvoie 1,5K, l'isolation est
utile ; s'il en lit 10K et en renvoie 8K, il a surtout déplacé le bruit. Une métrique simple à suivre sur les tâches
longues est :

```text
isolation_ratio
= tokens consommés par le subagent
/ tokens retournés au parent
```

Le bon pattern est donc **map → reduce** : plusieurs workers spécialisés dépensent du contexte localement, puis le
parent synthétise quelques résultats courts. Évite l'anti-pattern inverse — sept agents qui lisent chacun le repo et
renvoient des rapports de dix pages — qui recrée le *context rot* dans le contexte racine.

Pour **ton workflow solo Scala**, traite aussi le fan-out comme un budget de tokens/quota :

```text
défaut                              → 1 agent actif
2 investigations indépendantes     → 2 subagents read-only
2 User Stories indépendantes        → 2 writers maximum pour commencer (WIP inclut les PR en review)
3+ sessions parallèles              → uniquement si le gain et la capacité de review sont mesurés
writer                              → toujours 1 par branche / PR / worktree
```

Logge au minimum `parallel_sessions_peak`, `subagent_count` et `subagent_tokens`. Un subagent protège le contexte du
parent, mais il recharge son propre contexte : il n'est donc jamais « gratuit ». S'il n'apporte ni isolation utile ni
travail réellement parallèle, ne le lance pas.

Pour la coordination, préfère une **topologie en étoile** : le parent délègue des contrats indépendants et synthétise
les retours. Évite les équipes où les agents se parlent librement, partagent une mailbox ou se répartissent eux-mêmes un
état mutable. Dans ce guide, le « coordinateur » doit rester un **délégateur simple**, pas un système social d'agents.

> **Orchestration Claude Code** : **Agent View** sert à superviser plusieurs sessions et tâches ;
> **Agent Teams** permet la collaboration entre instances mais reste expérimental ; **Ultrareview** est une review cloud
> multi-agent en research preview. **Remote Control** permet de superviser une session locale depuis un autre appareil
> tout en gardant l'exécution et les MCP sur la machine locale. Ces surfaces complètent les subagents ; elles ne
> changent
> pas la règle « un seul writer par worktree ».

> **Mod `You should know` (2.1.287+)** : `cc-plugin-you-should-know` lance un side agent pendant les tâches longues
> et affiche au-dessus du prompt les éléments que toi ou Claude pourriez manquer. Il est **désactivé par défaut** et
> s’active via `/plugin enable cc-plugin-you-should-know@builtin`. Traite-le comme un signal de vigilance opportuniste,
> jamais comme un reviewer indépendant, un oracle ni un gate : ses remarques doivent encore être reliées à une preuve,
> un test ou un diff vérifiable.

> **Claude Code 2.1.27x : isolation plus fine.** Depuis 2.1.277, un subagent personnalisé ou fourni par un plugin peut
> déclarer `omitClaudeMd` pour ne pas charger les `CLAUDE.md` utilisateur, projet et local ; les politiques administrées
> restent chargées. Réserve ce mode aux workers d'exploration très spécialisés dont le contrat de délégation contient
> déjà tout le contexte nécessaire. La même version permet d'attacher des `allowed_domains` à une commande
> Bash/PowerShell/Monitor : l'ouverture réseau vaut pour cette commande, pas pour toute la session. Cela **confirme**
> les
> règles « contexte minimal par subagent » et « permissions minimales par sous-tâche », sans justifier de supprimer le
> contexte projet pour un implementer qui en a besoin.
>
> Depuis 2.1.278, le mode Auto utilise par défaut un **classifier côté serveur** sur les surfaces compatibles et
> Anthropic
> indique que ce classifier n'ajoute pas de coût de classification ; `/status` indique si `Auto mode server` est actif.
> Cela réduit un overhead de routage, pas les exigences d'autorisation ou de review. Enfin, les plugins et skills
> deviennent eux-mêmes des artefacts testables : `claude plugin eval` (2.1.269) exécute une suite d'évaluations scorées
> et reproductibles avec sortie JSON/HTML, tandis que `/skill-doctor` aide à repérer les skills chargés mais inutiles.
> Un changement persistant de plugin ou de skill doit donc passer par eval + review avant promotion.
>
> Les versions suivantes ajoutent deux outils complémentaires pour éviter la dérive du harness. Depuis **2.1.283**,
> `/doctor prompt-audit` (alias `/checkup prompt-audit`) audite `CLAUDE.md`, skills, agents et commandes pour repérer
> les
> instructions devenues obsolètes ou contradictoires après un changement de génération de modèle. Et en mode
> non-interactif, **`--bare`** est désormais documenté comme le moyen de lancer un harness minimal : pas
> d'auto-discovery des hooks/plugins/MCP/mémoire/instructions, et depuis 2.1.286 seuls les serveurs MCP explicitement
> nommés sont connectés, sans rappels système ni tâches de fond. Utilise `--bare` pour des **evals et scripts
> reproductibles**, pas comme mode quotidien par défaut.

### OpenRouter pour le routage API occasionnel

Dans **ce workflow solo précis**, le routage principal n'a pas besoin d'une gateway API. Les cinq chemins quotidiens ont
déjà leur propre surface et leur propre budget :

```text
Claude Code        → abonnement Claude Max
Codex              → abonnement ChatGPT
Qwen local         → MLX / llama.cpp / endpoint local
GitHub Copilot     → abonnement GitHub Copilot
JetBrains AI       → abonnement JetBrains AI
```

Le besoin API restant est **exceptionnel** : lorsque Claude Code puis Codex restent bloqués et que tu veux une opinion
issue d'une autre famille de modèles, par exemple **GLM, Kimi, Gemini, Grok ou un nouveau modèle à évaluer**. Dans ce
cas, **OpenRouter est le meilleur défaut** : une seule clé, aucun serveur à maintenir, accès rapide à de nombreux
modèles et providers, facturation centralisée et fallback de disponibilité.

```text
Blocage persistant
→ extraire le contexte minimal utile
→ OpenRouter
   ├── GLM
   ├── Kimi
   ├── Gemini
   ├── Grok
   └── nouveau modèle à tester
→ comparer l'analyse avec Claude / Codex
→ humain arbitre
```

**Ne route pas automatiquement le travail quotidien vers OpenRouter.** Le choix du modèle de secours doit rester
explicite : l'objectif est précisément d'obtenir une autre perspective, pas de laisser un routeur choisir
silencieusement une famille différente.

#### Fallbacks : provider oui, modèle non par défaut

OpenRouter peut basculer automatiquement entre providers. Pour ce guide, distingue deux niveaux :

```text
Même modèle, provider A indisponible
→ même modèle, provider B
→ OUI : résilience sans changer la nature du reviewer

GLM indisponible
→ Gemini
→ Kimi
→ Grok
→ NON par défaut : le changement de modèle doit rester visible et intentionnel
```

Pour une investigation technique, logge donc toujours **le modèle réellement utilisé**. Un fallback inter-modèle peut
masquer la raison pour laquelle une conclusion diffère de Claude ou Codex.

#### Qwen local : reste direct

N'ajoute pas OpenRouter uniquement pour uniformiser Qwen. `llama.cpp`, MLX ou le harness local peuvent déjà exposer un
endpoint OpenAI-compatible. Tant qu'il n'y a qu'un ou deux modèles locaux, la couche supplémentaire n'apporte pas assez
de valeur :

```text
Qwen local
→ llama-server / MLX
→ Qwen Code / OpenCode / script local
```

#### Confidentialité avec un agrégateur

Les providers accessibles via OpenRouter peuvent avoir des politiques de rétention différentes. Pour du code
professionnel sensible :

```text
- ne jamais envoyer le repository entier par défaut ;
- préférer un reproducer minimal, quelques types/méthodes, la stack trace et le test ciblé ;
- anonymiser le contexte métier si possible ;
- choisir explicitement les providers compatibles avec les exigences de rétention du projet ;
- garder le code le plus sensible en local ou chez les fournisseurs directs déjà approuvés.
```

### Métriques à logger

Le routeur doit être ajusté sur données réelles, pas sur intuition. Pour chaque tâche agentique, logue :

```plaintext
task_type
risk
difficulty
decision_layer
decision_confidence
decision_threshold
decision_overridden
model_used
effort_level
fallbacks
parallel_sessions_peak
subagent_count
subagent_tokens
input_tokens
output_tokens
cost_usd
duration
files_changed
diff_lines
tests_run
tests_passed
review_findings
human_rework
merged_or_reverted
time_to_deploy
human_active_minutes
review_queue_minutes
review_true_positives
review_false_positives
review_missed_defects
quota_consumed_by_role
production_regressions
rollback_or_hotfix
```

Après deux semaines, ajuste les seuils :

```text
- si Qwen échoue souvent sur un type de tâche, route directement vers Sonnet ;
- si Sonnet réussit sans retours review sur un type de tâche, évite Opus ;
- si Opus réduit fortement les boucles de correction, garde-le pour cette classe ;
- si Opus `xhigh/max` suffit là où tu envoyais Fable, redescends ;
- si Fable ne produit pas moins de reprises humaines, réserve-le aux vraies sessions longues ;
- si `max` ne trouve que des remarques optionnelles, redescends vers `high` ou `medium`.
```

### Prompt routeur minimal (fallback génératif)

Si Jev est disponible et que les sorties sont fermées, préfère des `Choice` / `Score` / `Noul` atomiques puis combine
les résultats en code. Le prompt ci-dessous reste utile lorsqu’un raisonnement ouvert est nécessaire ou comme baseline
de comparaison.

```text
Tu es un routeur de tâches de développement logiciel pour un projet Scala/Java/Play/Spark.

Analyse la demande ci-dessous et retourne uniquement du JSON valide.

Objectif : choisir le plus petit modèle capable de produire un résultat mergeable avec un risque acceptable.

Prends en compte :
- type de tâche ;
- difficulté ;
- risque métier ;
- taille probable du diff ;
- nombre probable de fichiers ;
- besoin d'écriture ;
- besoin de docs externes ;
- risque Scala spécifique : implicits, givens, effets, sérialisation JSON ;
- fichiers critiques : build.sbt, migrations DB, auth, sécurité, concurrence, argent ;
- modèle, effort et, si nécessaire, mode `pro` ou multi-agent (`ultra` côté produit) ;
- plafond de coût et de durée ;
- règle d'escalade ;
- conditions d'arrêt.

Les signaux déterministes (fichiers critiques, taille de diff) priment sur ta propre confidence.

Demande :
[COLLER LA DEMANDE]

Contexte disponible :
[COLLER FICHIERS, STACK TRACE, DIFF STAT OU RÉSUMÉ]
```

### Principe directeur du routage

```text
Le routeur ne choisit pas le modèle le plus intelligent.
Il choisit le modèle le moins cher capable de produire un diff mergeable,
avec une règle d'escalade explicite dès que le risque ou l'incertitude augmente.
```

## Impact sur le budget mensuel

*(ordre relatif indicatif à partir des tarifs API standard ; l'abonnement et le quota ne se convertissent pas
mécaniquement en dollars API)*

| Modèle              |           Prix API input/output / M | Recommandation de volume                                                                          |
|---------------------|------------------------------------:|---------------------------------------------------------------------------------------------------|
| Qwen local          |                                   0 | Pré-analyse et tâches sûres en volume                                                             |
| **Jev 1.14**        | **$0.042/M input ; output gratuit** | Decision layer : classification, routing, scoring et sélection de skills à haute fréquence        |
| **GPT‑6 Luna**      |                   **$0.10 / $0.50** | Micro-dev Codex, workers, triage, tests simples                                                   |
| **Haiku 5.5**       |                   **$0.10 / $0.50** | Sous-agents, triage ; palier ×5 si input > 100K ; effort `medium` configurable                        |
| **GPT‑6.2 Sol**     |                        **$2 / $10** | Défaut Codex agentique ; excellent point de rendement avant Astra                                 |
| **Sonnet 5.5**      |                        **$2 / $10** | Défaut micro-dev Claude ; `medium` pour agentic coding bien spécifié                              |
| **Opus 5.5**        |                        **$4 / $20** | Défaut Claude agentique à `medium`; `high` pour les tâches difficiles                             |
| **GPT‑6.2 Astra**   |                        **$8 / $40** | Escalade de capacité ; commencer à Light                                                          |
| **Fable 5.2**       |                        **$8 / $40** | Frontier Claude ; commencer à Low lors d'une escalade de capacité                                 |
| Extra / Max / Ultra |                            variable | N'utiliser qu'après mesure : plus d'effort n'est pas synonyme de meilleur coût par tâche terminée |

> **Le prix par token n'est pas le TCO.** Évalue aussi Fable 5.2 `low` sur des tâches bornées et vérifiables : il peut coûter moins par tâche résolue
> qu'un modèle inférieur qui cherche, relit et backtracke davantage ; inversement, Opus 5.5 `medium` peut atteindre la
> même qualité que Fable sur certains workloads pour une fraction du coût. Le benchmark local doit donc mesurer
> **coût par changement accepté**, reprises et minutes humaines.

## Règle anti-crédits brûlés

Ne lance Fable 5.2, GPT‑6.2 Astra, Opus 5.5 `Extra/Max` ou un mode `Ultra` coûteux que si tu peux fournir :

```text
- objectif précis ;
- contraintes ;
- fichiers ou modules probables ;
- critères d'acceptation ;
- tests à exécuter ;
- non-objectifs ;
- limite explicite de diff ;
- plafond de coût et de durée ;
- règle d'arrêt.
```

Un modèle très fort sur un prompt flou ne produit pas un bon résultat : il produit une dérive plus chère.

> **Plafonds exécutoires plutôt que discipline seule.** Plusieurs réglages Claude Code transforment cette règle en
> garde-fou : `maxEffortLevel` plafonne l'effort sur tous les providers ; une règle deny ciblant un paramètre d'outil
> (par exemple `Agent(model:opus)`) interdit de lancer un subagent sur un modèle cher ; `CLAUDE_CODE_SUBAGENT_MODEL`
> fixe le modèle des subagents ; `fallbackModel` liste jusqu'à trois modèles de repli essayés dans l'ordre (à
> journaliser, voir plus haut) ; `/usage` ventile la consommation par skill, subagent, plugin et serveur MCP ; et les
> hooks voient l'effort courant via `$CLAUDE_EFFORT`. Côté API, les **task budgets** (beta
> `task-budgets-2026-03-13`, `output_config.task_budget`) donnent au modèle un budget de tokens pour toute la boucle
> agentique : c'est un budget **indicatif**, pas un plafond, qui doit être doublé d'un `max_tokens` et d'un plafond
> côté client ; sa valeur fait partie du prompt rendu, donc la modifier casse le cache. Vérifie dans la doc la liste
> des modèles supportés avant de l'utiliser sur Fable 5.2 ou Opus 5.5.

#### Checklist pré-flight avant toute tâche > $2 de coût estimé

Avant de lancer Fable 5.2, GPT‑6.2 Astra, Opus 5.5 à effort haut ou une session multi-agent, valide cette checklist.
Chaque case non cochée est une raison de NE PAS lancer et de redescendre en modèle ou en scope.

□ Objectif formulé en 1 phrase avec verbe d'action □ Non-objectifs explicités (au moins 2)
□ Fichiers/modules concernés identifiés (chemins exacts)
□ Critère d'acceptation testable défini □ Commande de test ciblée prête à exécuter □ Diff maximum acceptable fixé (ex: <
300 lignes)
□ Plafond de coût fixé (ex: $5) et plafond de durée (ex: 30 min)
□ Règle d'arrêt formulée ("stop si [condition]")
□ Le plan a été validé par l'humain AVANT le write mode □ Worktree dédié créé si la tâche touche > 5 fichiers □ Contexte
minimal préparé (pas de "voilà toute la repo")

Estimation de coût rapide (ordre de grandeur) :

| Tâche               | Modèle      | Tokens estimés      | Coût estimé |
|---------------------|-------------|---------------------|-------------|
| Feature 3 fichiers  | Sonnet 5.5  | ~20K in / ~5K out   | ~$0.09      |
| Bug multi-modules   | Opus 5.5    | ~50K in / ~10K out  | ~$0.40      |
| Migration framework | Fable 5.2   | ~200K in / ~50K out | ~$3.60      |
| Audit Astra max     | GPT‑6.2 Astra | ~100K in / ~20K out | ~$1.60      |

Si le coût estimé dépasse 3x le coût du modèle inférieur pour la même tâche, la différence de qualité doit être
justifiée par le risque.
"Plus intelligent" n'est pas une justification.
---

# 4. Budget mensuel raisonnable et stratégie de caching

Le budget doit être piloté comme un budget d'ingénierie, pas comme une dépense “IA” abstraite. La bonne métrique n'est
pas le coût par message, mais :

```text
coût total d'une tâche mergeable
= coût modèle + temps humain + temps CI + retours review + reprises de bugs
```

## Budget de départ réaliste

| Poste                                                 |                 Budget indicatif | Remarque                                                                                                                                                                                    |
|-------------------------------------------------------|---------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code via Claude Pro/Max                        |                      20 à 200+ $ | Max se justifie si Opus/Sonnet tournent tous les jours ; le quota est partagé entre les surfaces Claude compatibles.                                                                        |
| ChatGPT avec Codex                                    |                     20 $ et plus | Plus convient à l'usage borné ; Pro se justifie si Sol 6.2 devient un writer quotidien et pas seulement un reviewer.                                                                        |
| JetBrains AI Ultimate                                 | ~300 $/an ; 35 AI Credits / 30 j | Utile pour les fonctions cloud JetBrains et Junie ; Code Completion / Next Edit Suggestions et agents authentifiés chez leur fournisseur ne consomment pas ces crédits.                     |
| GitHub Copilot                                        |                         variable | Optionnel : pertinent surtout si GitHub est le centre du workflow issues/PR/review ; largement redondant comme troisième chat de code.                                                      |
| OpenRouter / API ponctuelle GLM/Kimi/Gemini/Grok      |                         0 à 50 $ | Porte de sortie exceptionnelle quand Claude/Codex/Qwen ne suffisent pas ; budget volontairement faible et plafonné.                                                                         |
| GLM Coding Plan (Z.ai) — second abonnement optionnel  |                 ~18 à 160 $/mois | Forfait open-weight *conforme* : endpoint Anthropic-compatible, se branche dans Claude Code pour absorber review/triage sans entamer tes limites Claude. Lite ~18 $, Pro ~72 $, Max ~160 $. |
| Qwen local                                            |             0 $ hors électricité | Très bon pour pré-analyse, synthèse et boilerplate, mais pas pour décider seul sur code critique.                                                                                           |
| Sourcebot, Aider, OpenCode/Qwen Code, RTK             |                     0 à variable | Beaucoup d'outils sont open source, mais l'hébergement, les index et les clés API éventuelles coûtent.                                                                                      |
| Headroom et outils récents de compression de contexte |                     expérimental | À tester sur des logs/diffs non critiques avant de l'intégrer au workflow standard.                                                                                                         |

Total cible réaliste pour un usage solo intensif : **250 à
450 $/mois**, à ajuster après deux semaines de mesure réelle. Le budget initial de 300 à 350 $ reste plausible, mais il
ne faut pas le figer : une seule mauvaise boucle agentique sur un gros contexte peut coûter plus cher qu'une semaine de
micro-patches bien routés.

## Points de prix et quotas à ne pas figer dans le guide

Claude Code est inclus dans les plans Claude payants compatibles, mais l'usage exact dépend du plan, du modèle et des
limites de session. Les pages officielles indiquent notamment Claude Pro à 20 $/mois, Max à partir de 100 $/mois, et des
usages Max 5x/20x selon l'offre. Garde donc le guide sous forme de fourchettes, pas comme une vérité comptable
permanente.

Côté Codex, évite de transformer les noms de modèles et réglages ChatGPT en vérité comptable permanente. Le routage
actif de ce guide est **GPT‑6 Luna / GPT‑6.1 Terra / GPT‑6.2 Sol / GPT‑6.2 Astra**, avec Sol 6.2 Medium comme défaut agentique. Les limites
d'usage, l'accès à Max/Ultra et la facturation dépendent du plan, de la surface, de la région et du rollout. Écris donc
les règles autour de la **classe de tâche et du coût par changement accepté**, puis vérifie la page officielle avant
d'industrialiser un profil ou un budget.

Rappel important : **Anthropic réserve l'usage par abonnement Claude Free/Pro/Max/Team/Enterprise aux applications
natives Anthropic et aux usages prévus par ses conditions.** Depuis début 2026, Anthropic a explicitement interdit
l'usage de tokens OAuth de ces abonnements dans des harness tiers ou des outils non officiels : ces flux doivent passer
par une clé API dédiée (Claude Console ou cloud provider) et respecter les termes commerciaux. Concrètement : Claude
Code et Claude.ai pour les abonnements Claude ; OpenCode/Qwen Code/Aider pour Qwen local, modèles API ou clés BYOK, sans
jamais réutiliser un token de session Claude Pro/Max dans un outil externe.

À ne pas confondre avec ce qui *est* permis : brancher Claude Code sur l' **endpoint Anthropic-compatible de Z.ai** avec
une **clé Z.ai** (GLM Coding Plan, §3) est licite — tu utilises la clé d'un fournisseur contre l'endpoint de ce même
fournisseur, tu ne détournes aucun token OAuth Claude. La ligne rouge est le **réemploi d'un token d'abonnement Claude**
hors des apps Anthropic, pas le fait de pointer Claude Code vers un autre fournisseur avec sa propre clé.

**Budget post-PR Claude Ship.** En solo, `/ship`, `/steward` et Cloud Auto-fix consomment l’usage applicable de Claude
Code (pas de coût VM séparé pour le cloud Anthropic selon la documentation) ; une surveillance en arrière-plan n'est pas gratuite. Les agents GitHub de Claude Ship (Team/Enterprise)
consomment des crédits d'usage d'organisation hors allocation incluse. Estime `PR/mois × coût moyen de review ×
nombre de reviews par PR + corrections Steward + classifiers Approvals + CI supplémentaire`. Commence avec une review
sur demande ou à l'ouverture, pas sur chaque push, et fixe un plafond mensuel pour Code Review et PR Steward (ce
dernier n'en a pas par défaut). Le mode `observe` d'Approvals peut lui aussi déclencher des reviews et classifiers
facturés. Désactiver les usage credits ne suffit pas à arrêter les agents actifs : désactive Approvals, puis Steward,
puis Code Review si tu veux couper ces dépenses.

**Budget post-PR Codex.** `@codex review` et les reviews automatiques GitHub relèvent des conditions de Code
Review ; `/review` local, Goal mode, Heartbeats et tâches Codex Cloud authentifiés avec ton compte ChatGPT utilisent
les allocations applicables au plan et à la surface. Aucun script de surveillance archivé ni clé API OpenAI
supplémentaire n'est requis pour le workflow natif. Vérifie néanmoins les quotas, crédits supplémentaires et
permissions effectives : chaque reprise et chaque correction peuvent consommer du quota, même sans nouveau diff.
Préfère un objectif borné ou un Heartbeat court avec déduplication par SHA et arrêt explicite ; jamais les deux
simultanément sur une même branche. `openai/codex-action` avec clé API reste une option de CI distinctement facturée,
à réserver aux besoins d'automatisation que les surfaces natives ne couvrent pas.

## Prompt caching : levier majeur, mais à formuler précisément

Pour ne pas exploser le budget, structure les requêtes des agents de manière déterministe :

1. Place le contexte statique en haut : `AGENTS.md`, règles Scala, architecture, conventions de tests.
2. Place le contexte semi-statique ensuite : schémas, contrats JSON, conventions métier.
3. Place le contexte dynamique en bas : fichiers modifiés, erreurs de compilation, logs de tests.
4. Évite de modifier l'en-tête de prompt à chaque itération si tu veux bénéficier du cache.

Un cache hit réussi peut ramener le coût de **lecture** de tokens d'entrée à environ 10 % du coût input normal selon les
fournisseurs (sur les modèles Anthropic courants : 5 % pour Opus 5.5 et Sonnet 5.5, 2,5 % pour Fable 5.2, 10 % pour
Haiku 5.5 ; 5 % pour GPT‑6.2 Sol/Astra et GPT‑6.1 Sol/Terra). Ce n'est pas “90 % d'économie sur toute la tâche” : les tokens de sortie, l'écriture du cache, les tool
calls et les erreurs de boucle restent facturés.

## Règles anti-crédits brûlés

```text
- Ne donne jamais toute la repo par défaut.
- Donne des chemins de fichiers et une hypothèse de zone concernée.
- Coupe les logs à la première erreur utile.
- Après 2 échecs identiques, stop : repasse en diagnostic humain/IDE.
- Après 3 fichiers modifiés hors plan, stop : demande un nouveau plan.
- Après 300 lignes de diff inattendues, stop : review manuelle avant suite.
- Quand le contexte n'aide plus : `HANDOFF.md` explicite + session fraîche ; `/compact` n'est qu'un dernier recours.
- Préfère rg, Sourcebot, IntelliJ, Metals ou scripts locaux aux longs dumps MCP.
```

**Économies sur le double abonnement.** Stabilise le writer et son effort pendant une trajectoire ; les
changements de modèle peuvent perturber le cache et ajoutent du rework. Un contexte frais reste volontaire
pour le reviewer indépendant ou une hypothèse contaminée. Ne lance ni review exhaustive systématique sur
chaque micro-patch, ni deuxième steward sur une même PR. Déduplique le suivi par repo/PR/SHA/check/finding,
privilégie une reprise événementielle ou un Heartbeat borné lorsque la CI attend, et arrête-le au checkpoint.
Mesure les quotas consommés par rôle et par tâche (quand exposés par le fournisseur) ; distingue crédits
inclus, dépassements payants et API. Un quota restant élevé n'est pas une raison d'ouvrir plus de tickets.

# 5. Workflow standard pour une tâche métier Scala

## Étape 0 : cadrage humain

Avant l'IA, tu écris ou clarifies :

```text
Objectif :
Comportement actuel :
Comportement attendu :
Contraintes métier :
API publique à préserver :
Fichiers probablement concernés :
Tests ciblés :
Validation harness :
Risque :
Critère d'acceptation :
```

Numérote les exigences métier et invariants importants (`REQ-01`, `REQ-02`, etc.). Pour chaque exigence, déclare
le test ou la preuve attendue avant l’implémentation ; une exigence sans oracle doit être explicitement marquée
non couverte et arbitrée. Dans la PR, associe exigence, commande/test, résultat, SHA validé et limites de la preuve.
La matrice de traçabilité peut rester très courte pour un ticket trivial.

`Validation harness` doit nommer **avant le write mode** les preuves que l'agent pourra exécuter lui-même :
compilation ciblée, tests unitaires/intégration, ScalaCheck, scalafmt, éventuellement Stryker4s et contrôle du diff. Si
tu ne sais pas encore comment prouver que le changement est correct, la tâche n'est pas prête à être déléguée.

Sans ça, tu paies les modèles pour découvrir le problème au lieu de le résoudre.

> **Positionnement vs l'état de l'art 2026 (« Spec-Driven Development »)** : ce cadrage est exactement ce que
> l'industrie a formalisé sous le nom de SDD, devenu le contrepoids dominant au « vibe coding » — la spec comme
> artefact le plus rentable produit par l'humain quand l'agent écrit le code. L'outillage (GitHub Spec Kit, OpenSpec,
> AWS Kiro, notation EARS pour des exigences testables) peut structurer ce workflow, mais n'est pas obligatoire : ce
> guide pratique déjà la variante **spec-anchored** (la spec cadre et survit à la tâche, le code + les tests restent
> la source de vérité), qui est la posture recommandée pour du code métier existant — par opposition au
> **spec-as-source** (l'humain n'édite que la spec), encore expérimental. Règle de dosage issue des retours
> terrain : le niveau de détail de la spec doit suivre la *criticité* du code — sur-spécifier un script jetable est
> du gaspillage, sous-spécifier un contrat public est une dérive garantie.
>
> **Choisir un outillage SDD sans framework-sprawl.** Le paysage SDD
> dépasse désormais la trentaine de frameworks (Spec Kit, OpenSpec, Kiro, BMAD-METHOD, GSD, Tessl…). Le consensus
> pratique qui s'en dégage : **GitHub Spec Kit** pour du greenfield (constitution → specify → clarify → plan →
> checklist → tasks → analyze → implement → converge, avec des étapes de contrôle facultatives) ;
> **OpenSpec** pour du brownfield itératif — specs versionnées dans le repo avec *delta markers* par changement, la
> posture la plus proche de la variante spec-anchored de ce guide ; **AWS Kiro** si tu veux la notation EARS intégrée
> et l'écosystème AWS. Aucun n'est un prérequis : si `AGENTS.md` + le paquet de cadrage ci-dessus + les gates CI
> (section 15A) font déjà le travail, ajouter un framework SDD ajoute du contexte, pas de la qualité. Règle non
> négociable : la spec vit dans le repo et se reviewe comme du code — une spec tenue hors version devient une seconde
> source de vérité divergente.

> **Deux harness à ne pas confondre.** Un papier SDD publié le 31 août 2026 propose une distinction utile entre
> **technical harness** (modèle, outils, contexte, permissions, tests) et **methodological harness** (spec, rôles,
> responsabilités, review et autorité de release). Ce vocabulaire **confirme** la structure de ce guide : améliorer
> Claude Code, Codex ou MCP ne remplace pas la discipline de spécification et de validation humaine. La publication est
> toutefois principalement conceptuelle et s'appuie largement sur la littérature grise ; utilise cette distinction
> comme cadre de conception, pas comme une preuve empirique qu'un framework SDD donné améliore la productivité.

> **Premières données de pratique réelle.** L'étude CMU/Google « Spec-Driven Development as Prescribed
> and as Practiced » (déclarative, non répliquée) observe que les praticiens expérimentés appliquent déjà le SDD de
> façon **sélective, surtout pour de nouvelles fonctionnalités ou des changements risqués**, avec des specs rédigées par les agents à partir d'une intention
> humaine puis relues, et une vérification surtout par tests écrits par les agents. Le défaut principal est la
> **dérive silencieuse spec ↔ code** quand aucun plan de maintenance n'existe ; les retours Thoughtworks ajoutent
> l'*instruction bloat* (specs et contexte qui grossissent jusqu'à ce que l'agent perde le fil). Cela confirme deux
> règles de ce guide : dosage par criticité, et spec versionnée et reviewée. Ajoute seulement une troisième règle :
> **un test écrit par l'agent ne valide pas sa propre spec** ; garde le test de reproduction qui échoue avant le patch
> et le mutation testing (section 5, étape 4). Côté outillage, **`/speckit.converge`** relit le code face à
> `spec.md`, `plan.md` et `tasks.md` et **ajoute seulement les tâches manquantes à `tasks.md`**. C'est un contrôle de
> cohérence utile après l'implémentation, **pas un oracle** : ni les tests indépendants ni la review humaine ne doivent
> être supprimés sous prétexte que Spec Kit annonce « Converged ».

#### Template de spec opérationnel (copier-coller)

Ce template matérialise la variante spec-anchored du guide. Il vit dans le repo (par exemple `specs/TICKET-123.md`) et
se reviewe comme du code.

# SPEC : [TICKET-123] — [Titre court]

## 1. Objectif (1 phrase, verbe d'action)

[Ex: "Ajouter un taux de remise par palier de quantité au service DiscountService"]

## 2. Non-objectifs (explicite, anti-dérive)

- [Ex: "Ne pas modifier le calcul de remise existant par code promo"]
- [Ex: "Ne pas toucher à l'API publique du module pricing"]

## 3. Comportement attendu (règles métier, numérotées)

1. [Règle 1 : si quantité >= 10, remise 5%]
2. [Règle 2 : si quantité >= 50, remise 12%]
3. [Règle 3 : les paliers ne se cumulent pas, le plus haut s'applique]

## 4. Contraintes techniques

- API publique à préserver : [signatures exactes]
- Sérialisation JSON : [inchangée / ajouter champ X avec backward compat]
- Performance : [pas de requête DB supplémentaire dans le hot path]
- Concurrence : [état immuable / atomicité requise]

## 5. Fichiers probablement concernés

- `src/main/scala/.../DiscountService.scala`
- `src/test/scala/.../DiscountServiceSpec.scala`

## 6. Tests d'acceptation (critères de "done")

| Exigence / invariant | Preuve attendue |
|----------------------|-----------------|
| REQ-01 : seuil 10 | Test unitaire : 9 → 0 %, 10 → 5 % |
| REQ-02 : seuil 50 | Test unitaire : 49 → 5 %, 50 → 12 % ; propriété remise ≤ 12 % |
| REQ-03 : non-cumul | Test de non-régression sur le cumul ; remise par code promo inchangée |
| REQ-04 : contrat JSON | Test de compatibilité |
| REQ-05 : performance | Mesure du nombre de requêtes DB sur le scénario d'intégration |

- [ ] Mutation testing : score / mutants importants à justifier sur les fichiers touchés
- [ ] Résultats reliés au SHA et aux exigences ; exceptions et risques résiduels explicites

## 7. Risques et mitigations

| Risque               | Probabilité | Impact | Mitigation                      |
|----------------------|-------------|--------|---------------------------------|
| [Arrondi BigDecimal] | Moyen       | Haut   | [Utiliser RoundingMode.HALF_UP] |

## 8. Définition de done (checklist finale)

- [ ] Compile sans warning
- [ ] Tests ciblés verts
- [ ] scalafmtCheckAll passe
- [ ] Review second modèle effectuée
- [ ] Diff < [N] lignes
- [ ] Pas de fichier hors scope modifié

Niveau de détail adapté à la criticité :

- Script jetable → sections 1, 2, 6 suffisent
- Contrat public / argent / sécurité → toutes les sections obligatoires

---

## Étape 1 : recherche ciblée

Utilise dans cet ordre :

1. **Sourcebot** pour localiser fichiers, usages, tests.
2. **IntelliJ** pour vérifier symboles, types, hiérarchies.
3. **Context7** si une API externe ou une version récente est impliquée.
4. **Qwen local** pour produire un briefing.

Prompt Qwen :

```text
Analyse ces fichiers et produis :
- résumé du flux métier
- classes et méthodes impliquées
- invariants à préserver
- tests existants
- risques
- ambiguïtés
- prompt propre à donner à Claude Code

Ne propose pas encore de patch.
```

---

## Étape 2 : plan par l’agent writer, sans modification

Prompt writer (Codex ou Claude Code) :

```text
Tu es l'agent writer de cette tâche.

Objectif :
[objectif]

Contraintes :
- diff minimal
- pas de changement d'API publique sans validation explicite
- préserver les comportements existants
- ajouter ou adapter les tests
- procéder par petites étapes
- expliquer les risques
- ne rien modifier avant validation

Commence par explorer le code et proposer un plan.
```

Règle issue des documents : **pas de plan, pas de write mode**. Le plan doit lister les fichiers à modifier, les
fichiers à ne pas toucher, la stratégie de test, les risques et la taille attendue du diff.

---

## Étape 3 : implémentation par petits diffs

Prompt :

```text
Exécute uniquement l'étape 1.
Ne touche pas aux autres étapes.
Garde le diff minimal.
Après modification, donne :
- fichiers modifiés
- raison de chaque changement
- commande de test ciblée
```

Pour Scala, évite les gros refactors automatiques. Demande des lots de 30 à 300 lignes de diff quand c'est possible. Les
retours terrain et les études récentes sur les PRs agentiques convergent vers des PRs petites et bornées, plus faciles à
relire et moins sujettes aux échecs CI. À l'échelle organisationnelle, l'étude du déploiement Claude Code / Copilot CLI
chez Microsoft (arXiv, juillet 2026, dizaines de milliers d'ingénieurs) mesure ~24% de PRs mergées en plus chez les
adopteurs — l'effet est réel, mais il se matérialise dans des PRs *reviewables*, pas dans des diffs géants.

---

## Étape 4 : validation IntelliJ + tests

Les agents LLM sont connus pour écrire des tests "happy path" (des tests qui passent mais ne vérifient pas les cas
d'erreur ou les limites). Ordre recommandé pour Scala/SBT :

```plaintext
scalafmtCheckAll
compile
Test / compile
testOnly <TestCiblé>
IntegrationTest / testOnly <TestCiblé>
```

Puis seulement si le risque le justifie :

```plaintext
test
IntegrationTest / test
```

> **Note sbt :** la configuration `IntegrationTest` est **dépréciée depuis sbt 1.9.0** au profit d'un sous-projet
> dédié (par exemple un module `it` qui `dependsOn(core % "test->test")`) ou de tests taggés. Si ton projet l'utilise
> encore, les commandes ci-dessus restent valides, mais ne laisse jamais un agent migrer cette configuration tout seul —
> c'est exactement le genre de changement `build.sbt` qui doit passer par une validation explicite. Sur un nouveau
> module,
> pars directement sur un sous-projet `it`. Pense aussi à donner à l'agent la commande la plus rapide disponible :
> `sbt --client` (ou Bloop) évite de payer le démarrage de la JVM à chaque itération de la boucle test-correction, ce
> qui
> peut accélérer les boucles agentiques. Sous **sbt 2.x**, `sbt` utilise déjà le mode client-serveur natif `sbtn`
> par défaut ; `sbt --client` reste une forme explicite. Mesure le démarrage sur le projet réel : migration 1.x → 2.x
> et changement de `build.sbt` exigent une validation humaine (voir section 15A).
>
> Si `serverConnectionType` est configuré à `Tcp`, sbt 1.4.0 à 2.0.6 est
> vulnérable à une exécution de code non authentifiée via BSP. Supprime ce réglage ou passe au minimum à **sbt 1.13.0
> ou 2.0.7**. Le transport local par défaut (socket Unix ou named pipe) n'est pas affecté. Cette mise à jour est
> prioritaire avant d'exposer le serveur sbt à un IDE, un agent ou un conteneur distant.

#### Optimisations sbt pour les boucles agentiques

La vitesse de la boucle compile-test est le premier levier de productivité agentique. Configuration recommandée dans
`.sbtopts` (repo) :

# .sbtopts — optimisé pour les boucles agentiques

```plaintext
-J-Xms2g
-J-Xmx8g
-J-XX:+UseZGC
-J-XX:+UseStringDeduplication
-Dsbt.supershell=false
-Dsbt.color=false
-Dsbt.log.noformat=true
```

Explication des choix :

- `UseZGC` : option à mesurer contre le G1 par défaut sur le dépôt réel ; ne promets pas un gain systématique
  ni des pauses toujours inférieures à 1 ms
- `supershell=false` et `color=false` : réduit le bruit dans les sorties parsées par l'agent (moins de tokens, moins de
  context rot)
- `noformat=true` : idem, sorties brutes plus faciles à parser

Sous sbt 2.x, `sbt` lance déjà le client natif par défaut ; `sbtn` reste une entrée explicite utile :

# Premier lancement (démarre le serveur)

`sbt`

# Appels suivants depuis l'agent (démarrage quasi-instantané)

`sbtn "compile"`
`sbtn "testOnly *DiscountServiceSpec"`

Configuration du serveur dans `project/server.sbt` :

```scala
// Keep the build server on a local transport.
Global / serverConnectionType := ConnectionType.Local
```

Le transport local est normalement le défaut : **n'expose pas le serveur sbt en TCP** pour accélérer les agents. Ne
modifie pas `build.sbt` uniquement pour masquer des recompilations ou des vérifications :
`onChangedBuildSource := IgnoreSourceChanges`, `Test / fork := false` et la désactivation de Scaladoc peuvent
rendre le résultat non représentatif de la CI ou modifier les comportements des tests. Préfère cibler le module et
les suites (`project`, `testOnly`) sans altérer leur sémantique. Sous **sbt 2.x, `test` est incrémental et peut
réutiliser ses résultats en cache** : utilise `testFull` pour une validation exhaustive avant une PR ou en CI.

**Benchmark avant/après sur ton dépôt.** Compare à JVM et options identiques, sur au moins dix cycles compilations
incrémentales + tests ciblés : latence médiane, p95, redémarrages sbt, pression mémoire et stabilité des tests. Ne
présente pas une économie chiffrée sur un autre projet comme une garantie.

Pour Play Framework ou projets multi-modules :

```plaintext
sbt "project api" compile
sbt "project api" "testOnly *DiscountServiceSpec"
sbt "project integration" "testOnly *OrderFlowSpec"
```

Le point essentiel reste : ne demande pas seulement à l'IA “d'être prudente”, fais tourner les tests. Les garde-fous
déterministes battent les instructions textuelles.

Choisis les validations selon le risque réel, sans empiler des outils inutiles :

| Risque Scala/JVM | Preuve pertinente |
|------------------|-------------------|
| Calcul métier | ScalaCheck, limites, mutation testing |
| Compatibilité binaire / TASTy | MiMa / TASTy-MiMa lorsque pertinent |
| REST / JSON | Tests de contrats, schémas et compatibilité |
| Concurrence et effets | Ordonnancement contrôlé, cancellation, timeout, libération des ressources |
| Spark | Datasets déterministes, nulls, schémas, partitions, idempotence |
| Performance JVM | JMH ou benchmark ciblé reproductible |
| Architecture | Scalafix / fitness functions sur bytecode ou sources |
| Sécurité | SAST couvrant réellement Scala, SCA, secret scanning et tests d'autorisation |

**CodeQL Java/Kotlin ne prouve pas une couverture Scala** : vérifie la liste de langages supportés et éprouve
l'analyseur choisi sur des défauts connus. N'assimile pas un scanner de dépendances à une analyse des sources.


### Valeur probante des tests générés

Un test écrit par le même agent que l'implémentation n'est pas un oracle indépendant. Des travaux récents constatent que
les agents produisent fréquemment des tests d'observation ou d'impression sans assertions discriminantes ; augmenter le
nombre de tests par le prompt ne suffit pas à améliorer le taux de résolution. D'autres évaluations par mutation
montrent que des suites vertes détectent mal des défauts réalistes générés par agents, et que leur efficacité se dégrade
lorsque le code évolue même sans changement sémantique attendu.

Pour un bugfix, conserve donc la preuve la plus rentable :

```text
1. ajouter un test de reproduction minimal ;
2. vérifier qu'il échoue sur le commit de base pour la bonne raison ;
3. appliquer le patch ;
4. vérifier que ce test puis la suite pertinente passent ;
5. faire varier l'oracle : propriétés, cas limites, tests métamorphiques ou mutants ciblés ;
6. faire relire le test avant l'implémentation lorsque le domaine est critique.
```

Ne fixe pas un seuil de mutation universel qui inciterait à « jouer la métrique ». Compare le score sur le périmètre
touché, exige une justification pour chaque mutant survivant important et suis surtout le **delta de mutation score**,
les régressions échappées et les retours de review. Un test qui ne pouvait pas échouer avant le patch ne prouve pas le
correctif.

**L'étape de durcissement (Mutation Testing) :**
Une fois que l'IA a écrit les tests et qu'ils sont verts, valide leur robustesse avec Stryker4s :

```plaintext
sbt "project api" stryker
```

Un score faible **peut** révéler des tests insuffisants, mais aussi des mutants équivalents, non pertinents ou mal
ciblés. Examine d'abord les mutants survivants, leur impact métier et les exclusions ; n'ajoute pas des assertions
artificielles pour augmenter le score. Si un mutant important reste vivant, renvoie le rapport à l'agent en demandant
un **test de comportement observable indépendant du patch**, puis relance les tests ciblés.

---

#### Étape 5 : Forcer la vérification avant déclaration de complétion

Les agents LLM déclarent fréquemment "done" sans avoir vérifié. Ajoute cette instruction systématique à la fin de chaque
prompt d'implémentation :

Avant de déclarer cette tâche terminée, tu DOIS :

1. Exécuter la commande de compilation et montrer le résultat
2. Exécuter le test ciblé et montrer le résultat
3. Vérifier le diff depuis la base approuvée, les changements committés et non committés, et les fichiers non suivis
4. Lister les fichiers modifiés avec la raison de chaque changement
5. Si une étape échoue, corriger et recommencer depuis 1 Ne dis "done" que si les 5 points ci-dessus sont satisfaits.

Pour automatiser ces vérifications, utilise les scripts communs de la section 5 (hooks) et la CI de la section 15A.
Le hook `PostToolUse` compile seulement : `Test/compile` n'exécute pas les tests. Les résultats des suites et le
diff complet doivent être associés au SHA candidat, et la CI doit refaire la validation indépendamment.
Un Stop hook n'est pas une preuve de complétion ; il ne doit pas empêcher un arrêt pour blocage.

Variante pour les tâches critiques (sécurité, argent, contrat public) :

Avant de déclarer cette tâche terminée, exécute et montre :

1. sbt compile (zéro erreur, zéro warning nouveau)
2. sbt "testOnly *SpecCiblé" (tous verts)
3. sbt scalafmtCheckAll (formatage conforme)
4. Diff base → candidat et état Git complet (uniquement les fichiers du plan)
5. Vérifie que le diff ne contient PAS : TODO, FIXME, println de debug, import inutilisé, changement de signature
   publique non demandé Montre le résultat de chaque étape. Si une étape échoue, corrige et recommence. Ne déclare pas
   "done" avant que les 5 étapes soient vertes.

---

## Étape 6 : self-review par le writer

Prompt :

```text
Fais une review de ton propre diff avant de le transmettre au reviewer indépendant.
Liste :
- risques métier
- cas limites
- tests manquants
- changements inutiles
- fichiers à relire manuellement
- hypothèses que tu as faites
```

Cette étape retire souvent les erreurs évidentes avant review externe. **Elle ne vaut jamais approbation** : l'agent qui
a écrit le diff partage les mêmes hypothèses que son implémentation et ne peut pas constituer le gate final. Le writer
peut nettoyer ; un contexte frais de **l’autre famille de modèles** doit fournir ses constats indépendants. L’humain approuve.

---

## Étape 7 : review indépendante par l’autre famille de modèles

Prompt reviewer : **Opus 5.5 Medium** si Codex a écrit ; **GPT‑6.2 Sol Medium** si Claude a écrit. Monte à High pour une
PR risquée et vers Astra Light/Fable Low seulement si la capacité supplémentaire est justifiée :

```text
Interviens comme relecteur indépendant senior de code Scala/JVM.

Relis le SHA exact de la tête de la PR par rapport à sa base de fusion, à la spécification approuvée, aux critères d’acceptation et à AGENTS.md.
Travaille dans une nouvelle session en lecture seule. Ne modifie pas l’implémentation. Forme ton propre jugement
avant de consulter le raisonnement de l’agent qui a écrit le code.

Donne la priorité à la correction fonctionnelle, aux invariants à préserver, aux régressions, à la compatibilité, à la qualité des oracles de test,
à la gestion des erreurs et des ressources, à la concurrence, aux performances, à la sécurité et au respect du périmètre.

Pour chaque constat qui appelle une action, indique la gravité, le fichier et la ligne, le SHA relu, l’exigence ou l’invariant enfreint,
un scénario concret de défaillance ou de reproduction, le plus petit correctif plausible et les incertitudes restantes.
Distingue les défauts vérifiés des hypothèses. Écarte les préférences stylistiques et les refactorings sans rapport avec la tâche.
Rends uniquement un verdict concis et des constats étayés. N’invente aucun constat.
N’approuve et ne fusionne jamais la PR toi-même.
```

Variante avec classification de sévérité machine-exploitable — préférable pour le triage et un gate alimenté
uniquement par des findings validés indépendamment (voir l'exemple de décodage typé en section 12) :

```text
Classe chaque retour avec exactement un de ces labels :
- BLOCKING        : bug métier, perte de données, faille, contrat public cassé
- REGRESSION_RISK : comportement existant potentiellement altéré, cas limite non couvert
- STYLE           : lisibilité, convention, nommage — jamais bloquant
- OUT_OF_SCOPE    : amélioration valable mais hors ticket — à ignorer dans cette PR

Retourne uniquement du JSON valide :
{
  "findings": [ { "severity": "...", "file": "...", "message": "..." } ],
  "summary": "..."
}
```

La règle de gate associée : `BLOCKING` et `REGRESSION_RISK` doivent être traités ou explicitement contestés avant
merge ; `STYLE` est optionnel ; `OUT_OF_SCOPE` part dans le backlog, jamais dans le diff courant.

Ces labels restent des **hypothèses de review**, pas des faits. Chaque retour bloquant doit porter une preuve
vérifiable :
fichier et ligne, contrat violé, reproduction, test qui échoue ou règle statique précise. Sans preuve, il passe en
triage humain ; l'auto-étiquette d'un modèle ne doit jamais bloquer seule un merge. Cette validation évite les faux
positifs coûteux et les boucles « auteur IA ↔ reviewer IA » qui brûlent des crédits sans information nouvelle.

Le pattern recommandé reste : **un writer, un reviewer de l’autre famille**. La review croisée est une hypothèse
de travail, non une garantie : une étude *Cross-Model LLM Code Review* sur 116 problèmes algorithmiques avec
Opus 4.7 / GPT-5.5 observe un gain Codex → Claude (71,6 → 89,7 % de réussite) et une baisse Claude → Codex (91,4 → 82,8 %)
lorsque le reviewer réécrit le programme sans exécuter les tests. N'en déduis aucun classement des modèles actuels sur Scala. Le reviewer
détecte et justifie ; le writer corrige après triage. Mesure les vrais/faux positifs, défauts manqués et régressions
introduites par les corrections. Après une correction mineure, re-review ciblée des changements et invariants ;
review complète seulement si le risque ou la portée a changé.

> **Effort et limites de la review.** Sur 90 patches Django, une étude *How Much Effort Does an AI Code Reviewer
> Need?* trouve Opus 5.5 Medium non inférieur à High dans une marge prédéfinie de 15 points, pour un coût moyen
> inférieur d'environ 20 %. Même High accepte 45 % des patches jugés incorrects par l'oracle renforcé ; certaines
> étiquettes restent discutables. CR-Bench-v2 (584 défauts reviewables associés à des PRs) confirme que la couverture
> des défauts par les agents est limitée. Ces résultats confortent Medium pour le quotidien, mais ne prouvent ni
> l'équivalence universelle Medium/High ni l'efficacité des modèles actuels sur Scala. Pas de gate autonome LLM.

 Par défaut :
**Sol 6.2 Medium écrit → Opus 5.5 Medium review**, ou **Opus 5.5 Medium/High écrit → Sol 6.2 Medium review**. Luna/Haiku
servent aux tâches mécaniques ; Astra/Fable ne sont mobilisés qu'en escalade. `Ultra` reste réservé aux missions
découpables en axes indépendants.

---

## Étape 8 : correction ciblée

Tu ne demandes jamais au reviewer d'appliquer automatiquement toutes ses suggestions. Tu sélectionnes les retours
utiles, puis tu repasses au **writer original** :

```text
Voici les retours de review que je valide :
[liste]

Corrige uniquement ces points.
Ignore les suggestions optionnelles.
Garde un diff minimal.
Relance les tests ciblés.
```

**Stoppe la révision quand les critères sont verts.** Une passe corrective après review est le défaut ; une deuxième
n'est justifiée que par un finding `BLOCKING` / `REGRESSION_RISK` nouveau et étayé, un test rouge ou une preuve
déterministe. N'utilise pas de prompt du type « itère encore jusqu'à ce que ce soit parfait » : au-delà du meilleur
checkpoint, l'agent finit souvent par inventer des changements pour satisfaire la demande et peut dégrader le diff.

Si une nouvelle passe est nécessaire, compare systématiquement le nouveau diff au checkpoint précédent et garde la
version qui satisfait le mieux **spec + tests + scope**, pas la version la plus récente.

Si tu délègues la correction post-PR à Codex (Goal mode, Heartbeat ou Cloud), `/steward` ou PR Steward (section 12),
transfère-lui explicitement l'ownership de la branche, avec le SHA de départ, la spec et les seuls retours autorisés.
Arrête sa surveillance avant toute
reprise par le writer original. Tout nouveau commit relance les validations pertinentes ; la review indépendante doit
porter sur le diff final, pas sur le SHA précédant la correction automatique.

## Étape 9 : garde-fous anti-dérive agentique

Ajoute des règles d'arrêt explicites. Elles réduisent les diffs inutiles, les boucles de correction et les crédits
brûlés :

```text
Stop immédiat si :
- l'agent touche un fichier hors plan sans explication ;
- l'agent modifie build.sbt, plugins.sbt, resolvers ou versions sans validation explicite ;
- la même erreur de compilation revient 2 fois ;
- les tests ciblés échouent 2 fois avec des causes différentes ;
- le diff dépasse la taille annoncée ;
- le correctif commence à changer l'architecture au lieu de résoudre le ticket.
- l'agent tente une écriture destructrice, un push, un déploiement, un partage externe ou une action sur des secrets
  qui n'étaient pas explicitement autorisés.
```

Dans ce cas, ne relance pas “fix it”. Demande plutôt :

```text
Stop. Résume l'état exact :
- fichiers modifiés
- hypothèses faites
- erreur actuelle
- commandes exécutées
- prochaine action minimale proposée
Ne modifie rien.
```

> **Reprendre la main sans payer deux fois la même exploration.** Trois mécanismes Claude Code à connaître :
>
> - **Checkpoints** : chaque prompt crée un checkpoint (snapshot des fichiers avant chaque édition par les outils de
>   Claude). `Échap Échap` ou `/rewind` restaure la conversation, le code ou les deux à un point antérieur, y compris
>   après fermeture du terminal. Limite connue : seules les modifications faites via les outils d'édition de Claude
>   sont suivies, pas celles lancées en Bash — un checkpoint ne remplace ni un commit ni le worktree.
> - **`/compact` ne lave pas une mauvaise hypothèse** : la compaction résume la conversation et *conserve* donc
>   l'hypothèse erronée que le modèle répète. Quand l'agent revient deux fois à la même fausse piste, la parade est
>   `/clear` puis un prompt resserré avec le nouvel état — pas une compaction supplémentaire.
> - **Permissions en deny-by-default** : `settings.json` accepte des règles allow / ask / deny ; combine une allowlist
>   étroite avec des deny explicites (réseau, fichiers critiques, push) plutôt que d'approuver à la main en boucle.
>   C'est la version produit des règles de non-automatisation de la section 3.
> - **Auto mode par défaut** : depuis le 14 août 2026, le mode auto est le mode de permission par défaut des nouvelles
>   sessions sur les plans Pro, Max et Team. Son classifieur réduit les interruptions, mais ce n'est pas un gate
>   métier : vérifie que tes règles `deny` sur `build.sbt`, migrations, workflows CI et push restent actives (les
>   *hard deny rules* de l'auto mode bloquent sans tenir compte des exceptions `allow`), et garde les hooks ci-dessous.

#### Claude Mods : quand dépasser les hooks classiques

Depuis **Claude Code 2.1.287**, un **Mod** est un plugin dont les handlers JavaScript/TypeScript s’exécutent dans le
processus Claude Code. Un handler peut **observer, réécrire ou prendre en charge** un événement : tool call, prompt,
tour, commande ou rendu de l’interface. C’est une couche différente de MCP : un MCP fournit des outils depuis un
processus/service externe ; un Mod peut changer le comportement du harness lui-même. Au **3 octobre 2026**, la version
2.1.288 ajoute déjà `$.ui.selection()` et plusieurs correctifs Mods/plugins : traite donc cette API comme **jeune et
évolutive**, et épingle la version Claude Code pour tout Mod qui devient critique dans ton workflow.

| Besoin                                                                                                 | Primitive à préférer |
|--------------------------------------------------------------------------------------------------------|----------------------|
| Répéter des instructions / une méthode                                                                 | **Skill**            |
| Donner accès à un système ou à un outil externe                                                        | **MCP**              |
| Bloquer, autoriser ou logger un événement avec une règle simple                                        | **Settings hook**    |
| UI interactive, état partagé entre événements, commande locale, interception/réécriture d’un événement | **Mod**              |

La Mods API peut notamment enregistrer des commandes, tools et subagents, appeler un modèle, lire l’état et l’usage de
la session, conserver un store partagé, lire/écrire des fichiers, lancer un processus, appeler HTTP ou un MCP, et
communiquer avec d’autres sessions. Les Mods fonctionnent avec leurs hooks dans le terminal — y compris le terminal
intégré et le plugin JetBrains — ainsi que dans le Code tab de Claude Desktop ; les éléments d’UI ne sont pas rendus sur
toutes les surfaces headless/cloud.

**Ne remplace pas les trois hooks shell ci-dessous par un Mod uniquement parce que c’est possible.** Pour les gates
simples et déterministes (`build.sbt`, migrations, diff max, tests obligatoires), un settings hook reste plus petit,
plus lisible et plus facile à auditer. Utilise un Mod seulement si tu as besoin d’état cross-event, d’une UI, d’un
workflow interactif ou d’une interception que le hook classique exprime mal.

> **Frontière de confiance beaucoup plus large.** Un Mod s’exécute avec les droits de ton utilisateur, peut lire les
> prompts, tool calls, variables d’environnement et settings, démarrer des processus ou faire du réseau, réécrire une
> requête et dépenser du quota via des appels modèle. Les processus qu’il démarre sont **hors du sandbox Bash** de
> Claude.
> Un Mod installé peut aussi approuver certains tool calls qu’une règle `ask` ou un `PreToolUse` utilisateur aurait
> arrêtés.
> Les permissions Claude ne constituent donc pas une sandbox autour du code du plugin.

Avant d’installer ou de promouvoir un Mod tiers :

```text
1. Vérifier la source du marketplace et figer la version/commit quand c’est possible.
2. Lire .claude-plugin/plugin.json, hooks/hooks.json, le module register.*, bin/ et .mcp.json éventuel.
3. claude plugin validate ./mon-mod
   → inspecter en particulier les lignes hooks: et calls: sans exécuter le Mod.
4. claude --plugin-dir ./mon-mod plugin details <nom>
   → vérifier l’inventaire réel des composants.
5. claude plugin test ./mon-mod
   → tests de hooks déterministes, sans session, login ni réseau.
6. Si le plugin a des evals : claude plugin eval ... avant promotion.
7. Premier essai avec --plugin-dir dans un worktree jetable ; --safe-mode comme voie de récupération.
```

Pour une organisation, un vrai contrôle doit vivre dans les **managed settings** (`allowManagedModsOnly`, ordre des
plugins gérés, `disableAllHooks` selon politique) et dans le Mod intégré `cc-plugin-sec-default`, pas dans la bonne
volonté d’un Mod utilisateur. Pour ton usage solo, la règle équivalente est simple : **built-ins / code personnel
audité > plugin communautaire opaque**, et aucune mise à jour automatique d’un Mod sensible sans relecture du diff de la
version.

#### Configuration commune des hooks Claude Code / Codex

Sépare **feedback local** et **gate de validation**. Un hook sur une commande `Edit` ne voit pas nécessairement les
écritures Bash, MCP ou IDE ; il ne peut pas garantir le confinement. Supprime `ai-guard.sh` fondé sur la recherche de
chaînes dans une commande : les chemins dynamiques, symlinks et exécutions indirectes échappent à ce filtre.
Applique les permissions/sandbox de la section 12 ; contrôle les chemins réellement modifiés dans le diff final.
Les hooks ne sont pas un substitut à la CI indépendante.

Exemples pour un projet de confiance, `.claude/settings.json` :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Et `.codex/hooks.json` :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "apply_patch",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Les deux harness appellent les mêmes scripts (les événements et payloads propres aux outils restent distincts).
Codex exige de relire et approuver les définitions de hooks non gérées (`/hooks`) ; ne désactive pas ce contrôle.
Un worktree peut charger les hooks du checkout principal ; vérifie les sources réellement exécutées. Les hooks
et scripts de confiance doivent être protégés de l'écriture par l'agent ; en environnement géré, place-les hors
du worktree. N'exécute pas de hooks de projet non audité.

Script `scripts/ai-compile-check.sh` (feedback de compilation uniquement ; peut être désactivé si trop fréquent) :

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
logFile=$(mktemp)
trap 'rm -f "$logFile"' EXIT
# Capture the process exit code, not a pattern in the logs.
if sbt --client "Test/compile" >"$logFile" 2>&1; then
  exit 0
else
  exitCode=$?
  printf 'sbt Test/compile failed (exit %s)\n' "$exitCode" >&2
  tail -n 40 "$logFile" >&2
  exit 2
fi
```

Le résultat repose sur le code de retour de sbt, même sans ligne `[error]`. `Test/compile` compile les tests mais
ne les exécute pas. N'utilise pas `grep` ou une commande RTK comme arbitre du succès ; conserve le code de retour
de la commande originale. En présence de plusieurs sessions, ne lance pas des compilations concurrentes sur le
même serveur sbt.

Script `scripts/ai-stop-audit.sh` (rappel non bloquant, commun aux deux harness) :

```bash
#!/usr/bin/env bash
set -euo pipefail
# No transcript heuristics and no forced retry on legitimate blockers.
cat >/dev/null
printf '%s\n' '{"systemMessage":"Completion requires a fresh validation receipt for the exact candidate SHA and independent CI; report blockers without claiming done."}'
```

Le Stop hook ne cherche jamais une commande dans le transcript : une mention de `testOnly` ne prouve ni son
exécution ni son succès. Ne force pas l'agent à continuer lorsqu'un invariant ou un budget impose un arrêt.
Pour la complétion, exige le rapport structuré de `scripts/ai-validate.py` (section 11) et les checks CI sur le
candidat. Les preuves locales produites sous l'identité de l'agent sont utiles au diagnostic, mais falsifiables :
la politique de CI, ses scripts et ses résultats doivent vivre dans une frontière indépendante de l'agent.

Un Mod Claude privilégié ou un hook non fiable peut modifier le pipeline ; garde les restrictions externes et
les contrôles administrés. Le gate final ne peut pas être modifié puis auto-approuvé par le writer. Les hooks peuvent être ignorés ou ne pas
se déclencher selon la surface ; vérifie les événements, les chemins et les permissions effectifs avant adoption.

#### Protocole de récupération quand l'agent boucle

Une boucle agentique (même erreur, même correction, même échec) est un mode de défaillance distinct de l'échec simple.
L'escalade de modèle ne la corrige pas. Voici le protocole en 4 étapes :

**Étape R1 — Stop et extraction d'état (0 token supplémentaire)**

Arrête l'agent immédiatement. Ne relance PAS "fix it". Exécute :

Stop. Ne modifie plus rien. Résume en 5 points :

1. Fichiers modifiés jusqu'ici (diff depuis la base approuvée + git status)
2. Hypothèse actuelle sur la cause
3. Ce qui a été tenté et pourquoi ça a échoué
4. La prochaine action minimale que tu proposerais
5. Ce dont tu n'es pas sûr

**Étape R2 — Diagnostic humain avec l'IDE (5-10 min)**

Utilise IntelliJ pour vérifier ce que l'agent ne peut pas voir :

- Le type réel d'une expression (Ctrl+Shift+P / type info)
- La résolution effective d'un implicite/given (Ctrl+B sur l'implicit)
- La hiérarchie de types attendue vs produite
- Le breakpoint debugger sur le comportement inattendu

L'objectif est de trouver l'information structurelle qui manque à l'agent.

**Étape R3 — Session fraîche avec contexte resserré**

/clear Nouveau prompt avec UNIQUEMENT :

- L'objectif (1 phrase)
- Le fichier ou la méthode exacte concernée
- L'erreur précise (copiée depuis l'IDE, pas depuis le transcript)
- L'information structurelle trouvée en R2
- "Ne propose qu'un seul changement minimal. Compile et teste."

**Étape R4 — Si échec après R3, escalade de modèle**

C'est seulement maintenant que l'escalade Sonnet → Opus → Fable est justifiée, car le contexte est propre et le problème
est bien posé.

Anti-pattern absolu : relancer le même modèle sur le même contexte en espérant un résultat différent. C'est la
définition de la boucle.

> **Ré-ancrage périodique, la parade mesurée contre la dérive longue.**
> La recherche 2026 sur l'« agent drift » (dégradation comportementale mesurée sur les trajectoires longues et les
> systèmes multi-agents) converge sur trois familles de mitigations : consolidation épisodique de l'historique en
> résumés structurés, ancrage comportemental adaptatif (ré-injection périodique de la charte et de l'objectif
> courant) et routage tenant compte de la dérive. Traduction immédiate pour tes sessions :
> - **ré-injecte la charte** (objectif, non-objectifs, invariants, définition de done) à chaque jalon et au retour de
>   subagent — pas seulement au premier prompt : une contrainte qui n'est plus dans la fenêtre récente n'existe plus ;
> - **généralise le fichier d'état** (`MIGRATION_STATE.md`) à toute session longue, pas seulement aux missions
>   Fable : c'est l'ancre qui survit aux compactions et aux reprises ;
> - **circuit breakers à double seuil** : un avertissement sur la répétition d'un même tool call ou d'une même
>   erreur, puis un arrêt dur sur la deuxième répétition identique — plutôt qu'un seul seuil brutal ;
> - **session fraîche en cas de boucle** : l'escalade de modèle ne corrige pas une boucle (section 3) ; `/clear` +
>   état + charte relue, si.

---

# 6. Workflow TDD agentique pour code métier sensible

Pour une règle métier importante, inverse le workflow :

```text
Spec → tests générés → tests validés humainement → implémentation → tests verts → review
```

Pour les tâches critiques, sépare aussi les auteurs : Claude (ou Codex) prépare les tests depuis le commit de
base et la spec, l'humain valide l'oracle, puis l'autre agent implémente. Le writer n'affaiblit pas ces assertions ;
si un oracle est erroné, correction explicitement arbitrée avant de reprendre. Une nouvelle session de review
indépendante inspecte les cas limites du SHA final. Pour les micro-correctifs, garde une boucle plus courte.

Prompt test engineer indépendant :

```text
Interviens comme ingénieur de test indépendant. Lis la spécification approuvée, AGENTS.md et les contrats existants.
Pars du commit de base sans examiner d’implémentation proposée.
Conçois les tests minimaux couvrant les critères d’acceptation, les cas limites, les défaillances et les invariants à préserver.
Associe chaque test à une exigence. Privilégie les comportements observables et les tests par propriétés lorsque c’est pertinent.
Pour un correctif, démontre que le test de reproduction échoue sur le commit de base pour la raison attendue.
Ne modifie ni le code de production, ni les assertions existantes, ni la configuration du build ou de la CI.
Ne déduis pas les résultats attendus de l’implémentation testée.
Indique les exigences non couvertes, les contrats ambigus, les commandes exactes et les résultats d’exécution.
Attends la validation humaine de l’oracle avant de transmettre les tests à l’agent chargé de l’implémentation.
```


Prompt :

```text
À partir de cette règle métier, écris d'abord les tests.
Ne modifie pas encore le code de production.
Les tests doivent couvrir :
- cas nominal
- cas limite
- non-régression
- comportement existant à préserver
```

Tu relis les tests. Ensuite seulement :

```text
Implémente le minimum de code pour faire passer ces tests.
Ne modifie pas les contrats publics.
```

Ce pattern est l'un des plus fiables pour faire travailler un agent en boucle contrôlée, à condition de doubler la
validation locale par une CI indépendante. Pour un **bugfix**, demande en plus un *bug-reproduction test* : il doit
échouer sur le commit de départ, reproduire le défaut observé, puis passer avec le correctif. Un test ajouté après le
patch sans preuve qu'il échouait avant apporte beaucoup moins d'information.

Pour Scala, exige du **Property-Based Testing** pour la logique complexe :

```text
À partir de cette règle métier, écris d'abord les tests en utilisant ScalaCheck (Property-based testing).
Ne te contente pas de tests unitaires classiques. Définis les générateurs (Gen) pour éprouver toutes les limites du domaine.
```

---

## Exemple : à quoi doivent ressembler les propriétés générées

Le LLM doit produire des propriétés qui encodent des **invariants métier**, pas des tests unitaires déguisés en
`forAll`. Exemple de cible pour un service de remise :

```scala
import org.scalacheck.*
import org.scalacheck.Prop.forAll

object DiscountServiceProps extends Properties("DiscountService"):

  // Générateurs qui éprouvent les limites du domaine : zéro, bornes, valeurs extrêmes.
  // C'est ici que le LLM apporte de la valeur — à condition de lui demander
  // les invariants en langage naturel AVANT le code.
  val amounts: Gen[BigDecimal] =
    Gen.frequency(
      8 -> Gen.chooseNum(1L, 100_000_00L).map(c => BigDecimal(c) / 100),
      1 -> Gen.const(BigDecimal(0)),
      1 -> Gen.const(BigDecimal("9999999999.99")) // borne haute du domaine
    )

  val rates: Gen[Int] =
    Gen.frequency(8 -> Gen.choose(1, 99), 1 -> Gen.const(0), 1 -> Gen.const(100))

  property("le montant remisé n'est jamais négatif") =
    forAll(amounts, rates) { (amount, rate) =>
      DiscountService.applyDiscount(amount, rate) >= BigDecimal(0)
    }

  property("la remise ne dépasse jamais le montant initial") =
    forAll(amounts, rates) { (amount, rate) =>
      DiscountService.applyDiscount(amount, rate) <= amount
    }

  property("0% est l'identité") =
    forAll(amounts) { amount =>
      DiscountService.applyDiscount(amount, 0) == amount
    }

  property("monotone : plus de remise → montant final plus petit ou égal") =
    forAll(amounts, rates, rates) { (amount, r1, r2) =>
      val (lo, hi) = if r1 <= r2 then (r1, r2) else (r2, r1)
      DiscountService.applyDiscount(amount, hi) <= DiscountService.applyDiscount(amount, lo)
    }
```

La propriété de monotonie est l'exemple type de ce qu'un LLM ne génère pas spontanément mais produit très bien sur
demande explicite : *"liste d'abord les relations d'ordre et les identités du domaine, puis encode-les en propriétés"*.
Croisé avec Stryker4s (section 5, étape 4), ce niveau de test tue la grande majorité des mutants.

---

# 7. Règles spécifiques Scala

## Ne jamais laisser l'agent faire automatiquement

* changer une signature publique ;
* modifier des implicits, givens, typeclasses ou conversions sans explication ;
* remplacer un type précis par `Any`, `Object`, `String` ou `Map[String, Any]` ;
* avaler une erreur avec `recover { case _ => ... }` ;
* rendre un effet synchrone bloquant dans une boucle ;
* modifier `build.sbt`, plugins, versions ou resolvers sans validation et vérification réseau préalable;
* toucher aux migrations DB sans plan de rollback ;
* “simplifier” un modèle de domaine sans test métier ;
* changer la sérialisation JSON publique.

## À demander explicitement

```text
Avant de modifier du Scala :
- explique les types impliqués
- indique les implicits/givens utilisés
- identifie les effets de bord
- vérifie les tests existants
- conserve les signatures publiques
- ne change pas la sérialisation JSON sans test
```

## Checklist Scala post-diff

```text
- Le code compile-t-il vraiment ?
- Les imports sont-ils corrects ?
- Les implicits/givens restent-ils résolus ?
- Les types d'erreur sont-ils préservés ?
- Les Futures/IO/Effects ne bloquent pas ?
- La sérialisation JSON est inchangée ?
- Les tests couvrent-ils le comportement métier ?
- Le diff est-il minimal ?
```

## Refactors mécaniques : scalafix avant le LLM

Pour les réécritures syntaxiques répétitives (migration de syntaxe Scala 2 → 3, remplacement systématique d'une API
dépréciée, réorganisation d'imports), **scalafix est déterministe là où un LLM est probabiliste** : une règle s'applique
identiquement sur 500 fichiers, sans hallucination ni oubli. Le bon partage des rôles :

```text
LLM (Claude) : écrire ou adapter la règle scalafix
scalafix : appliquer la transformation sur toute la base
LLM : traiter les cas que la règle n'a pas pu couvrir
```

C'est la même logique que « les garde-fous déterministes battent les instructions textuelles », appliquée aux refactors.

Exemple concret du partage des rôles — une règle syntaxique que le LLM écrit une fois et que scalafix applique sur toute
la base sans dérive :

```scala
package fix

import scalafix.v1.*
import scala.meta.*

// Règle générée par Claude, relue par un humain, appliquée par scalafix.
// Migration : `logger.warn(msg, exception)` (API dépréciée)
//          →  `logger.warn(exception)(msg)` (nouvelle API curryfiée)
class MigrateLoggerWarn extends SyntacticRule("MigrateLoggerWarn"):

  override def fix(implicit doc: SyntacticDocument): Patch =
    doc.tree.collect {
      case t @ Term.Apply(Term.Select(qual, Term.Name("warn")), List(msg, ex))
          if qual.syntax.toLowerCase.contains("logger") =>
        Patch.replaceTree(t, s"${qual.syntax}.warn(${ex.syntax})(${msg.syntax})")
    }.asPatch
```

```bash
# Application déterministe sur 500 fichiers, en secondes :
sbt "scalafixAll MigrateLoggerWarn"
# Puis : le LLM ne traite QUE les cas que scalafix a laissés (rapport de la règle)
```

Le prompt à donner au LLM n'est pas « migre les appels logger » mais : *"écris une règle scalafix `SyntacticRule`
pour cette transformation, avec ses tests, et liste les patterns que la règle ne couvrira pas"*. Le coût est payé une
fois ; l'application est gratuite et reproductible.

## Spécificités Scala 3 vs Scala 2

Les modèles LLM mélangent très souvent les deux syntaxes ou réinventent des macros complexes. Exige explicitement :

```text
- Utilise la syntaxe stricte Scala 3 (indentation optionnelle, enums, extensions).
- Interdiction stricte de créer des Macros (inline, quoted) sans validation humaine préalable. Préfère toujours des fonctions standards.
```

## Hallucination de dépendances : le risque « slopsquatting »

Les modèles n'inventent pas seulement des numéros de version : ils inventent des **noms d'artefacts entiers**, et des
attaquants enregistrent ces noms plausibles dans les registres publics pour y déposer des charges utiles. Cette attaque
supply-chain, documentée sous le nom de *slopsquatting*, est mesurée en 2026 à environ **19,7 %** des échantillons de
code généré contenant au moins un nom de paquet halluciné, avec plus de 200 000 noms fictifs uniques identifiés ; les
modèles open-weight en produisent environ quatre fois plus que les frontier propriétaires (~21,7 % contre ~5,2 %) — à
garder en tête avant de laisser Qwen local proposer une dépendance.

Règles dérivées, à appliquer au niveau du repo :

```text
- tout nouvel artefact dans build.sbt doit exister sur Maven Central AVANT l'écriture
  (vérification réseau, pas mémoire du modèle) ;
- pour toute dépendance inconnue : exiger une date de première publication et un éditeur
  avec un historique établi ;
- commiter les lockfiles (coursier / dependencyLock) et vérifier les hashes en CI ;
- toute installation initiée par un agent hors allowlist → revue humaine avant exécution ;
- ne jamais laisser un agent résoudre les dépendances (sbt update) avec un build modifié
  sans diff relu.
```

C'est la version supply-chain de la règle « vérifier les versions via Context7 / Maven Central » de la section 3 :
le nom lui-même est une donnée non fiable.

---

# 7A. Intégration LLM en Scala fonctionnel

Quand le LLM devient une dépendance de ton *produit* (et plus seulement de ton workflow de dev), il doit être traité
comme n'importe quel service externe : interface abstraite, erreurs typées, effets aux bords, testabilité.

## Panorama des approches (juin 2026)

| Approche                         | Librairies                        | Forces                                              | Limites                                                 |
|----------------------------------|-----------------------------------|-----------------------------------------------------|---------------------------------------------------------|
| Client HTTP bas niveau           | `sttp` + `circe` (ou `zio-http`)  | Contrôle total, zéro dépendance lourde, caching fin | Tout est à écrire : retry, streaming, tool_use          |
| Wrapper API dédié                | `sttp-openai`                     | Endpoints typés, maintenu par softwaremill          | Couvre OpenAI/compatibles ; Anthropic via client séparé |
| Écosystème JVM                   | `langchain4j` (Java, appelable)   | Agents, RAG, mémoire, intégrations nombreuses       | API très orientée Java ; ergonomie Scala moyenne        |
| Génération de client par contrat | `smithy4s` (si spec Smithy dispo) | Client/serveur typés, doc générée                   | Suppose une spec Smithy maintenue — rare pour les LLM   |

Recommandation : pour un backend Scala, **client bas niveau sttp + abstraction maison** bat presque toujours un
framework d'agents généraliste. Les APIs LLM sont de simples APIs HTTP JSON ; la valeur est dans *ton* typage du
domaine, pas dans l'abstraction générique.

## Structurer un `LlmClient[F[_]]` générique

```scala
import io.circe.Decoder

opaque type ModelId = String
object ModelId:
  def apply(s: String): ModelId = s
  val sonnet: ModelId = "claude-sonnet-5-5"
  val haiku:  ModelId = "claude-haiku-5-5"

final case class Prompt(system: String, user: String)
final case class Usage(inputTokens: Int, outputTokens: Int, cacheReadTokens: Int)
final case class Completion(text: String, usage: Usage)

// L'interface ne mentionne ni HTTP, ni JSON, ni fournisseur :
// elle est mockable dans les tests et substituable (Anthropic, Qwen local).
trait LlmClient[F[_]]:
  def complete(model: ModelId, prompt: Prompt, maxTokens: Int = 1024): F[Completion]
  def completeAs[A: Decoder](model: ModelId, prompt: Prompt): F[A]
```

```scala
import zio.*

// Implémentation ZIO câblée en ZLayer — la version Cats Effect est un Resource + trait identique
final case class AnthropicConfig(apiKey: String, baseUrl: String = "https://api.anthropic.com")

object AnthropicLlmClient:
  val layer: ZLayer[AnthropicConfig, Nothing, LlmClient[Task]] =
    ZLayer.scoped {
      for
        config  <- ZIO.service[AnthropicConfig]
        backend <- sttp.client3.httpclient.zio.HttpClientZioBackend.scoped().orDie
      yield new AnthropicLlmClientLive(config, backend)
    }
```

Dans les tests, on substitue une implémentation déterministe (`LlmClient` qui rejoue des réponses enregistrées) — la
logique métier autour du LLM se teste alors sans réseau, sans coût et sans flakiness.

<!-- NOUVELLE SECTION -->

# 7B. Typage fort des entrées/sorties LLM

La sortie d'un LLM est une `String` non fiable. La frontière entre « texte du modèle » et « valeur du domaine » doit
être un décodage typé qui échoue explicitement — jamais un parsing optimiste.

## Le pattern ADT + Circe

Reprenons la classification de sévérité de la review Codex (section 5, étape 6) :

```scala
import io.circe.*
import io.circe.generic.semiauto.*

enum Severity:
  case Blocking, RegressionRisk, Style, OutOfScope

object Severity:
  given Decoder[Severity] = Decoder.decodeString.emap {
    case "BLOCKING"        => Right(Severity.Blocking)
    case "REGRESSION_RISK" => Right(Severity.RegressionRisk)
    case "STYLE"           => Right(Severity.Style)
    case "OUT_OF_SCOPE"    => Right(Severity.OutOfScope)
    case other             => Left(s"Sévérité inconnue : $other") // échec explicite, pas de fallback silencieux
  }

final case class Finding(severity: Severity, file: String, message: String)
final case class ReviewResult(findings: List[Finding], summary: String)

object ReviewResult:
  given Decoder[Finding]      = deriveDecoder
  given Decoder[ReviewResult] = deriveDecoder
```

Trois règles non négociables, en écho à la section 7 :

* jamais de `Map[String, Any]` pour « aller plus vite » : si le schéma change, tu veux une erreur de décodage, pas une
  `NullPointerException` trois couches plus loin ;
* l'`enum` + `emap` plutôt qu'une `String` : le compilateur force l'exhaustivité du `match` en aval ;
* le décodeur échoue sur valeur inconnue — un LLM qui invente `"CRITICAL"` doit faire échouer le pipeline, pas être
  silencieusement classé optionnel.

## Forcer le schéma côté modèle : tool_use et Structured Outputs

Le décodage typé attrape les sorties malformées ; encore mieux est de les rendre rares en forçant le schéma côté API :

* **Anthropic** : déclarer un outil avec `input_schema` (JSON Schema). Pour les modèles qui acceptent le tool choice
  forcé, `tool_choice: {"type": "tool", "name": "report_review"}` impose l'appel. **Exception Fable 5.2 / Opus 5.5** :
  `tool_choice: "any"` et `tool_choice: {"type": "tool", ...}` renvoient une erreur 400 ; utilise `tool_choice: "auto"`,
  une instruction explicite (« appelle `report_review` avant de conclure ») et un schéma strict. Dans tous les cas,
  décode les arguments vers `ReviewResult`.
* **OpenAI** : dans la **Responses API**, le format structuré se déclare via `text.format` avec
  `type: "json_schema"` et `strict: true` ; `response_format` appartient à la surface Chat Completions. Le schéma
  contraint une réponse terminée normalement, mais le client doit encore traiter explicitement refus, réponse
  incomplète, erreur API et invariants métier non exprimables en JSON Schema.
* **Jev** : ne le réduis pas à « Structured Outputs moins cher ». Pour une décision fermée, les options font partie de
  l'interface du modèle et la réponse fournit directement une **distribution de probabilités** exploitable par le code.
  Pour produire du texte, une explication ou une structure ouverte, garde un LLM génératif + décodage typé.

```scala
import io.circe.Json
import io.circe.syntax.*

// Le schéma est dérivable automatiquement (zio-schema, ou tapir SchemaType → JSON Schema),
// mais le maintenir à la main reste lisible pour un petit contrat :
val reviewToolSchema: Json = Json.obj(
  "type" -> "object".asJson,
  "properties" -> Json.obj(
    "findings" -> Json.obj(
      "type"  -> "array".asJson,
      "items" -> Json.obj(
        "type" -> "object".asJson,
        "properties" -> Json.obj(
          "severity" -> Json.obj(
            "type" -> "string".asJson,
            "enum" -> List("BLOCKING", "REGRESSION_RISK", "STYLE", "OUT_OF_SCOPE").asJson
          ),
          "file"    -> Json.obj("type" -> "string".asJson),
          "message" -> Json.obj("type" -> "string".asJson)
        ),
        "required" -> List("severity", "file", "message").asJson
      )
    ),
    "summary" -> Json.obj("type" -> "string".asJson)
  ),
  "required" -> List("findings", "summary").asJson
)
```

> **Validation supplémentaire** : pour les contrats plus riches, `zio-schema` (ou `io.circe.schema`) permet de
> dériver le JSON Schema depuis le type Scala — une seule source de vérité, le `case class`, au lieu d'un schéma
> maintenu à la main qui dérive du code.

# 8. Organisation repo recommandée

Ajoute ces fichiers ou dossiers à la racine, en gardant **un seul endroit de vérité** :

```text
AGENTS.md                       # Source commune, courte, versionnée
CLAUDE.md                       # Optionnel :Importe @AGENTS.md + règles Claude spécifiques
GEMINI.md                       # Pointeur vers AGENTS.md ou symlink selon ton outil
.github/copilot-instructions.md # Règles de review / coding agent GitHub Copilot, si utilisé
.github/instructions/           # Règles Copilot path-specific si nécessaire
.aiignore                       # Exclusions IA : secrets, gros artefacts, generated
.claude/rules/scala.md          # Règles Claude path/scopes si utiles
.claude/rules/testing.md
.claude/rules/security.md
stryker4s.conf                  # Mutation testing
docs/architecture.md
docs/testing.md
docs/review-checklist.md
docs/scala-style.md
scripts/ai-test-changed
scripts/ai-lint-changed
scripts/ai-diff-context
scripts/ai-rules-drift
```

Le but n'est pas d'accumuler de la documentation, mais d'éviter que l'agent redécouvre les mêmes règles à chaque
session. Le fichier doit rester court, stable et opérationnel.

> **Synchronisation des fichiers contexte :** Codex charge les instructions globales de `CODEX_HOME`, puis
> les fichiers du chemin projet depuis la racine vers le répertoire courant. À chaque niveau,
> `AGENTS.override.md` prime sur `AGENTS.md` ; les instructions les plus proches du répertoire de travail
> sont ajoutées en dernier. Les noms de fallback et la taille maximale dépendent de la configuration.
>
> Claude Code, avec le Mod intégré `cc-plugin-agents-md`, utilise par défaut `claude-md-or-agents-md` :
> `AGENTS.md` est chargé si aucun `CLAUDE.md`, `.claude/CLAUDE.md` ou `CLAUDE.local.md` n'existe dans le
> répertoire courant ou ses parents. Les instructions utilisateur/administrées et `.claude/rules/` continuent
> de s'appliquer. `AGENTS.override.md` n'est pas lu par Claude via ce fallback. Le mode
> `claude-md-and-agents-md` charge les deux sans dupliquer un fichier déjà importé. Le fallback peut être
> indisponible sur certaines surfaces ; il ne remplace pas un import explicite lorsque nécessaire.
>
> Pour ce workflow mixte, privilégie un `AGENTS.md` commun, et si un `CLAUDE.md` existe, commence-le par
> `@AGENTS.md`. Garde ensuite seulement les règles réellement spécifiques à Claude. Vérifie les instructions
> chargées dans une nouvelle session (`/context all` côté Claude, et demander à Codex de lister les fichiers
> d'instructions applicables). Pour les sous-modules, vérifie aussi la découverte depuis le répertoire réel
> d'exécution. Aucun override ne doit pouvoir affaiblir une règle de sécurité externe.

À savoir côté Claude Code : les **rules** sous `.claude/rules/` permettent de compléter les instructions projet avec des
consignes plus ciblées, par exemple par sous-arborescence ou type de tâche. C'est souvent préférable à un énorme
`CLAUDE.md` global lorsque ce fichier existe.

À savoir aussi : l' **auto-memory** Claude Code nécessite une version récente, documentée à partir de v2.1.59+. Les
premières lignes de `MEMORY.md` peuvent être chargées automatiquement, et les sous-agents peuvent avoir leur propre
mémoire. Utilise cette mémoire pour des rappels de patterns récurrents, pas pour des secrets, pas pour des décisions
d'architecture non revues, et pas comme substitut à la documentation versionnée.

## Contenu minimal de `AGENTS.md`

```text
Commandes exactes de build, de test et de formatage
Frontières architecturales et invariants métier peu évidents
Contraintes d’API publique, de JSON et de migration
Fichiers protégés et périmètre d’écriture autorisé
Conventions Scala absentes de la documentation existante
Conditions d’arrêt et critères de fin de tâche
Références vers la documentation et la spécification pertinentes
```

Écris ces règles **pour l'agent, pas comme une documentation humaine** : préfère des chemins, commandes, nombres
et conditions vérifiables. Garde quelques centaines de mots comme point de départ. Le README, les tutoriels,
la liste exhaustive des modules et les comparatifs de modèles restent dans `docs/`, chargés à la demande.

### Routage dans la configuration utilisateur

Conserve la matrice de la section 3 dans un document de routage ou des profils utilisateur Codex/Claude plutôt que
dans chaque `AGENTS.md` : le dépôt doit rester indépendant du modèle. Si un orchestrateur doit consulter cette
matrice, ajoute seulement un pointeur vers elle. Les contraintes métier et de sécurité ne changent pas selon le modèle.

## Contenu minimal de `CLAUDE.md`

```text
@AGENTS.md

## Claude Code
Utilise le mode plan pour les modifications risquées qui touchent plusieurs fichiers.
```

Déplace les règles communes de l'ancien `CLAUDE.md` vers `AGENTS.md` (pas de duplication). Le mode plan Claude
est une préférence de harness ; les autorisations effectives restent dans la configuration et la sandbox.

## Pourquoi garder `AGENTS.md`

Avec Codex et le Mod intégré `cc-plugin-agents-md` de Claude Code (fallback `AGENTS.md` par défaut), `AGENTS.md`
devient encore plus naturellement le contrat commun. Des travaux récents sur les agents de codage indiquent qu'un
fichier d'instructions de ce type peut réduire le temps d'exécution et les tokens de sortie tout en gardant un taux de
complétion comparable. L'effet pratique attendu est simple : moins de contexte répété, moins de consignes oubliées,
moins de dérive entre outils.

> **État des preuves : résultat mixte, pas bénéfice automatique.** Une autre évaluation de 2026 observe que les fichiers
> de contexte réduisent souvent légèrement le taux de réussite et augmentent le coût de plus de 20 %, surtout lorsqu'ils
> répètent le README ou ajoutent des exigences inutiles. Les fichiers écrits par les mainteneurs font mieux que ceux
> générés automatiquement, mais doivent eux aussi être mesurés.
>
> Règle corrigée : `AGENTS.md` doit contenir uniquement ce qui change effectivement une action — commandes exactes,
> invariants non évidents, fichiers interdits, conventions absentes du README et règles d'arrêt. Pas de visite guidée
> narrative du dépôt, pas de catalogue de technologies, pas de conseils génériques. Compare régulièrement un échantillon
> de tâches avec et sans le fichier. Repère quantitatif complémentaire issu de la
> même littérature : rester sous **~500 mots**, centré sur les normes de test, les conventions de style et les
> avertissements de danger — pas de visite guidée du dépôt — et relire le fichier comme du code à chaque revue.

#### Protocole de validation : mesurer l'efficacité d'AGENTS.md

Un AGENTS.md qui ne change rien au résultat est du contexte mort qui coûte des tokens à chaque session. Protocole de
validation trimestriel :

**Test A/B sur 10 tâches représentatives :**

1. Sélectionne 10 tâches réelles du backlog (mix greenfield/bugfix/refactor)
2. Pour chaque tâche, exécute 2 fois :
    - Run A : avec AGENTS.md dans le contexte
    - Run B : sans AGENTS.md (ou avec une version vide)
3. Mesure pour chaque run :
    - Nombre de tours avant complétion
    - Nombre de fichiers hors scope touchés
    - Nombre d'erreurs de compilation
    - Respect des conventions de test
    - Coût total en tokens
4. Compare :
    - Si AGENTS.md ne réduit AUCUNE métrique → il est inutile, supprime-le
    - S'il réduit certaines métriques → garde uniquement les sections utiles
    - S'il augmente le coût sans améliorer la qualité → il est nocif

**Indicateurs d'un AGENTS.md efficace :**

- L'agent cite les commandes de test exactes sans les redécouvrir
- L'agent ne touche pas les fichiers interdits sans qu'on le lui rappelle
- L'agent respecte les conventions de nommage dès le premier diff
- Le nombre de "rappels" humains en cours de session diminue

**Indicateurs d'un AGENTS.md nocif :**

- L'agent produit des diffs plus verbeux (il "applique" trop de règles)
- Le coût en tokens augmente > 20% sans amélioration mesurable
- L'agent hallucine des commandes qui ne sont pas dans le fichier
- Les règles génériques noient les règles spécifiques

Règle de maintenance : chaque fois qu'une règle d'AGENTS.md est violée par un agent ET que la violation est attrapée en
review, la règle est soit mal formulée, soit au mauvais endroit. Corrige-la ou matérialise-la dans un contrôle de la section 5 ou 15A plutôt
que d'ajouter une phrase de plus.

#### Audit de *rule drift* : vérifier que les instructions décrivent encore le repo réel

Les règles destinées aux agents sont volontairement spécifiques — chemins, commandes, modules, fichiers interdits — et
c'est précisément pour cela qu'elles vieillissent vite. Une instruction fausse est pire qu'une instruction absente :
elle force l'agent à réconcilier `AGENTS.md` avec une codebase qui a déjà changé.

Ajoute `scripts/ai-rules-drift` et exécute-le après tout changement d'architecture/build, puis au minimum une fois par
semaine si le dépôt bouge beaucoup :

```text
Vérifier :
- chaque chemin cité dans AGENTS.md / CLAUDE.md existe encore ;
- chaque module sbt cité existe encore ;
- chaque commande de compile/test/format est encore valide ;
- aucun nom de DB, service, dossier ou script supprimé n'est encore référencé ;
- les fichiers « interdits » correspondent encore aux vraies surfaces critiques ;
- si CLAUDE.md existe, il importe ou complète toujours la source commune attendue.
```

Le script peut rester déterministe pour les checks simples (`test -e`, grep des modules, commandes `--help`/dry-run) et
faire seulement **rapporter** les cas ambigus. N'autorise jamais l'agent qui détecte la dérive à réécrire puis
auto-approuver ses propres règles persistantes : le diff de règles se reviewe comme du code.

### Instructions GitHub Copilot sans dupliquer `AGENTS.md`

Si le dépôt utilise GitHub Copilot, conserve `AGENTS.md` comme contrat commun et réserve
`.github/copilot-instructions.md` aux attentes spécifiques de **review GitHub** : sévérité des findings, conventions de
PR, fichiers à surveiller et critères qui doivent être signalés. Les fichiers
`.github/instructions/**/*.instructions.md`
permettent de spécialiser ces règles par chemin. Évite d'y recopier toute l'architecture ou toutes les règles Scala :
une instruction commune doit rester dans `AGENTS.md`.

Copilot Code Review lit les instructions et skills de la **branche de tête de la PR**. Une modification de ces règles
fait donc partie de la surface de code à reviewer : un agent ne doit pas pouvoir assouplir ses propres contraintes dans
la même PR sans que ce changement soit explicitement visible et validé.

# 9. MCP prioritaires

## Indispensables

| MCP                        | Rôle                                                                                 |
|----------------------------|--------------------------------------------------------------------------------------|
| **Metals MCP**             | Intelligence Scala live : compile, diagnostics, types, symboles                      |
| **ScalaSemantic MCP**      | Graphe sémantique Scala via SemanticDB : usages, hiérarchies, call paths, givens     |
| **JetBrains MCP**          | Exposer IntelliJ, fichiers ouverts, actions IDE                                      |
| **Sourcebot**              | Recherche/discovery codebase multi-repos                                             |
| **Codebase-Memory MCP**    | Knowledge graph structurel persistant polyglotte ; surtout Java/Kotlin/cross-service |
| **GitHub MCP**             | Issues, PR, Actions, checks                                                          |
| **Context7**               | Documentation de libs à jour                                                         |
| **Playwright MCP**         | Validation UI si app web                                                             |
| **Sentry MCP**             | Diagnostic bugs prod                                                                 |
| **Postgres read-only MCP** | Schéma, migrations, requêtes                                                         |
| **ast-grep MCP**           | Recherche structurelle et refactors ciblés                                           |

Caractéristiques opérationnelles (à revérifier au moment de l'installation — transports et versions évoluent vite) :

| MCP                    | Transport typique               | Version minimale notable                   | Maintenance juin 2026                                    |
|------------------------|---------------------------------|--------------------------------------------|----------------------------------------------------------|
| Metals MCP             | stdio ; standalone depuis 1.6.6 | Metals 1.5.3 (intégré), 1.6.6 (standalone) | Actif (Scalameta)                                        |
| ScalaSemantic MCP      | MCP local                       | SemanticDB requis pour le cœur de l’index  | Jeune ; spécialisé Scala, à benchmarker sur le repo      |
| JetBrains MCP          | serveur intégré IDE             | IntelliJ 2025.2 (serveur)                  | Actif (JetBrains)                                        |
| Sourcebot              | HTTP                            | —                                          | Actif                                                    |
| Codebase-Memory MCP    | MCP local                       | —                                          | Actif ; Hybrid LSP documenté pour Java/Kotlin, pas Scala |
| GitHub MCP             | HTTP distant ou stdio local     | —                                          | Actif (GitHub officiel)                                  |
| Context7               | HTTP distant                    | —                                          | Actif                                                    |
| Playwright MCP         | stdio                           | —                                          | Actif (Microsoft)                                        |
| Sentry MCP             | HTTP distant                    | —                                          | Actif (Sentry officiel)                                  |
| Postgres read-only MCP | stdio                           | —                                          | Variable selon l'implémentation — auditer avant prod     |
| ast-grep MCP           | stdio                           | —                                          | Actif                                                    |

> **Évolutions du protocole MCP à connaître** : **MCP 2026-07-28 est maintenant la spécification publiée de référence**.
> Le cœur devient stateless : retrait des sessions de niveau protocolaire, de `Mcp-Session-Id` et, pour cette révision,
> du handshake `initialize` / `notifications/initialized`. Chaque requête transporte dans `_meta` les informations
> nécessaires, dont la version et les capacités du client. `server/discover` permet de découvrir identité, versions et
> capacités du serveur. La révision formalise aussi le framework d' **Extensions**, les **Tasks** pour le travail long,
> les **MCP Apps**, l'autorisation alignée OAuth/OIDC et une politique de dépréciation ; `Roots`, `Sampling` et
> `Logging` sont dépréciés. Pour un nouveau développement, **cible 2026-07-28**, mais garde des tests de compatibilité
> 2025-11-25 tant que tous les clients/serveurs utilisés ne sont pas migrés. Claude Code 2.1.27x a généralisé son client
> MCP v2 et la négociation 2026-07-28 aux connexions HTTP directes, y compris Bedrock, Vertex, Foundry et les
> installations
> sans télémétrie ; un mode legacy subsiste. Ne suppose donc toujours pas que tous les pairs MCP d'un environnement
> récent
> ont migré en même temps.

> **MCP Events reste une extension proposée, pas le cœur du protocole.** ChatGPT sait expérimenter des abonnements
> `events/list`, `events/subscribe` et `events/unsubscribe` avec livraison webhook sur des serveurs en MCP 2.0
> (`2026-07-28`). C'est utile pour des workflows événementiels — commentaire créé, incident, message, changement
> d'état — mais ne rends pas une intégration critique dépendante de cette extension tant que son statut et son support
> croisé clients/serveurs ne sont pas stabilisés.

## ChatGPT et Codex : rôles MCP à ne pas confondre

Il faut distinguer **ChatGPT web**, les **clients Codex locaux** et l' **Agents API**. MCP décrit une relation
client/serveur ; le fait qu'un produit puisse aussi exposer une API d'orchestration ne le transforme pas en serveur MCP.

| Surface                                                       | Rôle MCP et transports                                                                            | Authentification                                                                      | Lecture / écriture                                                                          |
|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Codex CLI / extension IDE / hôte Codex de ChatGPT Desktop** | **Client MCP** ; STDIO local et Streamable HTTP distant ; configuration partagée sur le même hôte | Bearer, OAuth, CIMD et DCR ; `codex mcp login` pour OAuth                             | Selon les outils du serveur, le sandbox et les approbations ; lecture et écriture possibles |
| **ChatGPT web Pro**                                           | Client d'apps MCP **distantes**                                                                   | OAuth selon l'app                                                                     | Developer mode limité aux outils `read` / `fetch`                                           |
| **ChatGPT web Business / Enterprise / Edu**                   | Client d'apps MCP distantes ; **full MCP en beta**                                                | OAuth + contrôles workspace/admin                                                     | Outils de lecture et actions `write` / `modify` possibles pour les MCP personnalisés        |
| **OpenAI Agents API**                                         | Client MCP hébergé ou depuis l'environnement ; HTTP ou STDIO selon l'origine de connexion         | Headers/Bearer, coffre de credentials ou variables d'environnement selon le transport | `allowed_tools` permet de réduire explicitement la surface exposée                          |

> **Documentation OpenAI contradictoire.** Le Help Center détaillé maintient **Pro =
> `read`/`fetch`** et réserve le full MCP read/write à Business/Enterprise/Edu, tandis que la page développeur
> généraliste affirme désormais que le developer mode donne le full MCP read/write à Plus et Pro. Tant que ces deux
> sources officielles ne convergent pas, garde le tableau ci-dessus comme hypothèse conservatrice et **détecte les
> capacités réellement exposées par le compte/workspace** avant de concevoir un workflow d'écriture.

**Codex n'est plus un serveur MCP.** `codex mcp-server` et le binaire `codex-mcp-server` ont été supprimés. Une
intégration qui veut piloter Codex comme service doit migrer vers **Codex App Server**, qui utilise son propre JSON-RPC
et **n'est pas MCP** ; Codex continue en parallèle à consommer des serveurs MCP externes comme client.

ChatGPT web ne se connecte pas directement à `localhost`. Pour un MCP local, privé ou on-premise, expose-le via le
**Secure MCP Tunnel** au lieu d'ouvrir le serveur publiquement. Deux limitations de surface restent importantes :
**Agent mode n'utilise pas les apps MCP personnalisées**, et **Deep Research** ne les utilise qu'en `read` / `fetch`.

### Gouverner un catalogue MCP comme une API versionnée

Quand un administrateur approuve une app MCP dans ChatGPT, le produit conserve un **snapshot approuvé des outils et de
leurs entrées**. Ajouter, retirer ou modifier un outil sur le serveur ne rend pas automatiquement la nouvelle surface
active. Une évolution incompatible peut donc casser des appels tant qu'un administrateur n'a pas revu et republié le
catalogue, et ChatGPT ne garantit pas actuellement une alerte proactive sur cette dérive.

```text
changement de nom / schéma / permission / nouvel outil MCP
→ diff de surface
→ review
→ validation admin
→ publication
```

Cette règle **complète**, sans la remplacer, la politique de sécurité de cette section : versions épinglées, permissions
minimales, logs d'outils et séparation lecture/écriture.

## Knowledge graph MCP pour Scala, Java et Kotlin

**Sourcebot n'est pas un knowledge graph.** Il reste la couche de recherche/discovery : retrouver rapidement fichiers,
symboles, usages textuels et extraits pertinents, notamment sur plusieurs repositories. Un knowledge graph répond à une
autre classe de questions : relations entre symboles, chemins d'appel, hiérarchies, dépendances structurelles et impact
d'un changement.

### Scala : privilégier ScalaSemantic, compléter avec Metals

Pour un dépôt principalement Scala, **ScalaSemantic MCP** est le meilleur candidat identifié pour la couche « graphe
sémantique ». Il ne reconstruit pas uniquement le code depuis un AST Tree-sitter : son index principal est alimenté par
**SemanticDB**, donc par des symboles déjà résolus lors de la compilation. Il expose des requêtes globales adaptées aux
agents, notamment usages exacts, signatures, hiérarchies, overloads, `call_path`, recherche de givens et traçage de
chaînes d'implicits.

```text
Sourcebot
→ « où est X ? »
→ « quels fichiers parlent de Y ? »

ScalaSemantic MCP
→ « quels sont les usages exacts de ce symbole ? »
→ « quel chemin d'appel relie A à B ? »
→ « qui étend ce trait ? »
→ « quels givens peuvent produire T ? »
→ « de quels implicits dépend ce given ? »

Metals MCP
→ « quel est le type réel ici, maintenant ? »
→ « ce fichier compile-t-il ? »
→ « quels diagnostics le compilateur retourne-t-il ? »
→ « quels tests échouent ? »
```

ScalaSemantic et Metals sont **complémentaires**. ScalaSemantic est index-wide et excellent pour les relations
globales ; Metals reste la source de vérité live pour le buffer courant, le presentation compiler, les diagnostics, la
compilation et les tests. SemanticDB représente principalement le dernier état compilé : si le code vient d'être modifié
sans recompilation, Metals peut être plus frais.

Ne présente pas non plus ScalaSemantic comme un Neo4j/RDF générique : c'est plus précisément un **semantic code graph
MCP**. Certaines opérations restent des approximations de haut niveau et ne reproduisent pas nécessairement toute la
logique du compilateur à un call site précis. En cas de contradiction sur la résolution effective d'un type, d'un
overload ou d'un given, **Metals/scalac gagne**.

### Java et Kotlin : Codebase-Memory devient beaucoup plus intéressant

**Codebase-Memory MCP** construit un knowledge graph persistant de fonctions, classes, call chains, routes HTTP et liens
cross-service à partir de Tree-sitter. Sa seconde passe « Hybrid LSP » documente actuellement une résolution enrichie
pour plusieurs langages dont **Java et Kotlin**. Sur ces deux langages, il est donc plus pertinent que sur Scala pour
les questions structurelles de codebase-scale.

```text
Java / Kotlin

Sourcebot
= recherche et discovery

Codebase-Memory MCP
= knowledge graph persistant
= call graph
= impact analysis
= architecture
= routes et relations cross-service

IntelliJ / LSP
= sémantique live et arbitrage local
```

Sur une codebase JVM polyglotte, la répartition recommandée devient :

```text
Scala pur
→ Sourcebot + ScalaSemantic + Metals

Java/Kotlin
→ Sourcebot + Codebase-Memory + IntelliJ/LSP

Scala + Java + Kotlin / microservices
→ Sourcebot
→ ScalaSemantic pour la sémantique Scala
→ Codebase-Memory pour la topologie polyglotte et cross-service
→ Metals / IntelliJ pour arbitrer la sémantique live
```

Le critère déterminant n'est pas « possède-t-il une base graphe ? », mais **quelle information crée les arêtes** :

```text
Tree-sitter
→ structure syntaxique et résolution heuristique

SemanticDB
→ symboles résolus par le compilateur Scala

LSP / presentation compiler
→ état sémantique live du code courant
```

Pour le développement Scala, préfère donc une arête SemanticDB à une arête reconstruite uniquement depuis le texte
lorsque les deux sont disponibles.

### Effet sur le context engineering

Cette couche de graphe est surtout utile si elle évite de charger des dizaines de fichiers. Un subagent read-only peut
interroger ScalaSemantic ou Codebase-Memory, puis ne remonter que quelques chemins, symboles et preuves `file:line` au
parent :

```text
question d'impact
→ subagent isolé
→ knowledge graph / semantic graph
→ 5–10 relations pertinentes
→ vérification Metals / IntelliJ si nécessaire
→ résumé < 1–2K tokens
→ parent
```

Cela augmente l'`isolation_ratio` et réduit directement le *context rot*. En revanche, n'active pas plusieurs MCP de
graphe par principe : benchmarke-les sur dix tâches réelles et garde uniquement ceux qui réduisent le nombre de fichiers
lus, les tokens injectés ou les erreurs de compréhension.

### Alternatives à connaître sans les standardiser

`agent4s` est une toolbox Scala MCP intéressante, basée sur Scalameta avec SemanticDB optionnel, qui expose notamment
références, hiérarchies, dépendances et call graph. Elle mérite un bake-off si ScalaSemantic ne couvre pas une classe de
tâches, mais n'ajoute pas les deux d'emblée.

Joern construit un véritable **Code Property Graph** très riche pour l'analyse de sécurité et de data flow, mais son
frontend source ne cible pas Scala comme langage de premier ordre. L'analyse du bytecode JVM Scala est envisageable, au
prix de la perte d'une partie des abstractions source ; réserve donc Joern à des audits spécialisés plutôt qu'au
contexte quotidien de Claude Code.

## Metals MCP : l'outil Scala manquant dans la plupart des stacks

C'est probablement le MCP le plus sous-utilisé par les développeurs Scala. **Metals (le language server Scala) embarque
un serveur MCP depuis la v1.5.3** (mai 2025), et la **v1.6.6 « Osmium » (3 mars 2026) a ajouté un serveur MCP
standalone** qui tourne sans éditeur ouvert — donc utilisable directement par Claude Code ou Codex CLI en terminal.
Cette même version a ajouté le support des **templates Twirl de Play**, directement pertinent pour ta stack.

Les outils exposés incluent notamment `compile-file`, `compile-full`, `compile-module`, `test`, `inspect`, `get-docs`,
`get-usages`, `get-source`, `import-build`, `find-dep`, les outils Scalafix, `glob-search` et `typed-glob-search`.
L'outil clé pour les boucles agentiques reste **`compile-file`** : l'agent écrit, compile le fichier, reçoit les erreurs
de types/implicits et corrige immédiatement, sans payer un cycle `sbt compile` complet à chaque itération.

Articulation avec JetBrains MCP et ScalaSemantic :

```text
JetBrains MCP     = contexte IDE quand IntelliJ est ouvert (fichiers ouverts, inspections, run configs)
ScalaSemantic MCP = relations globales SemanticDB : usages, hiérarchies, call paths, givens
Metals MCP        = feedback compilateur live pour les agents terminal, même IDE fermé
```

Les trois sont complémentaires, pas redondants. Pour les sessions Claude Code longues ou les tâches lancées hors IDE (CI
locale, worktree parallèle), Metals MCP est celui qui transforme « l'agent devine les types » en « l'agent interroge le
compilateur ».

> **Versionnement Metals** : **Metals 1.6.9 est publiée depuis le 14 septembre 2026** (après 1.6.8 du 23 juillet). Côté
> MCP, elle apporte le `glob-search` sur tous les modules, la résolution des suites de tests entre modules, la
> suggestion d'`import-build` quand aucune cible de build n'est trouvée et un correctif contre les blocages sur erreurs
> de linkage. C'est directement utile aux monorepos Play/sbt multi-modules : prends 1.6.9 comme minimum pour les
> boucles agentiques. Des milestones Metals 2 existent, mais ne les standardise pas avant une release stable.

## Exemple : boucle test-correction agentique sur `compile-file`

Squelette ZIO de la boucle qui fait la valeur de Metals MCP — l'agent corrige contre le **compilateur**, pas contre sa
propre confiance, avec une borne de tours qui matérialise la règle « 2 échecs → stop » :

```scala
import zio.*

final case class Diagnostic(file: String, line: Int, message: String)
final case class CompileResult(success: Boolean, diagnostics: List[Diagnostic])

// Abstraction du client MCP : l'implémentation parle JSON-RPC à Metals en stdio
trait MetalsMcp:
  def compileFile(path: String): Task[CompileResult]

def fixLoop(
    llm: LlmClient[Task],
    metals: MetalsMcp,
    path: String,
    maxRounds: Int = 3
): Task[Either[CompileResult, CompileResult]] =

  def round(n: Int): Task[Either[CompileResult, CompileResult]] =
    metals.compileFile(path).flatMap {
      case ok if ok.success =>
        ZIO.succeed(Right(ok))

      case ko if n >= maxRounds =>
        // Règle anti-dérive : on n'insiste pas, on rend la main avec un état exploitable
        ZIO.logWarning(s"$path : toujours rouge après $maxRounds tours — escalade humaine/IDE")
          .as(Left(ko))

      case ko =>
        val errors = ko.diagnostics
          .map(d => s"${d.file}:${d.line} ${d.message}")
          .mkString("\n")
        for
          source  <- ZIO.readFile(path)
          patched <- llm.complete(
                       ModelId.sonnet,
                       Prompt(
                         system = "Corrige UNIQUEMENT les erreurs de compilation listées. " +
                                  "Diff minimal. Ne restructure pas. Retourne le fichier complet.",
                         user   = s"Erreurs :\n$errors\n\nFichier :\n$source"
                       ),
                       maxTokens = 8192
                     )
          _       <- ZIO.writeFile(path, patched.text)
          result  <- round(n + 1)
        yield result
    }

  round(1)
```

Chaque itération coûte un `compile-file` (millisecondes, incrémental) au lieu d'un `sbt compile` complet : c'est ce qui
rend la boucle économiquement viable avec Sonnet, et inutilement chère sans Metals.

## Règle de sécurité

* MCP filesystem limité au repo.
* DB MCP en read-only par défaut.
* Pas de secrets exposés.
* Pas de prod directe.
* Pas deux agents avec droits d'écriture sur les mêmes fichiers.
* Worktree séparé pour toute tâche parallèle.

### Modèle zéro-trust contre l'injection indirecte

Un agent peut lire des instructions malveillantes dans une issue, un README, un commentaire de code, une sortie de
build, une page web, un résultat MCP ou un fichier généré. Ces contenus sont des **données non fiables**, même
lorsqu'ils se présentent comme des règles système. La robustesse du modèle ne suffit pas : les défenses doivent être
structurelles.

```text
1. Explorer en read-only dans un worktree ou conteneur jetable.
2. Refuser le réseau par défaut ; autoriser seulement les domaines nécessaires.
3. Monter les secrets hors du contexte et utiliser des clés à portée, budget et durée minimaux.
4. Exiger une approbation humaine pour installation, réseau, push, déploiement, suppression et écriture hors repo.
5. Épingler les versions des serveurs MCP et limiter chaque outil à son répertoire et à ses actions.
6. Séparer l'agent qui lit des données externes de celui qui dispose des permissions d'écriture.
7. Journaliser chaque tool call et arrêter si une donnée lue tente de modifier la politique ou les permissions.
8. Traiter **skills, plugins, serveurs MCP et mémoire persistante comme des dépendances exécutables** : versions épinglées,
   provenance vérifiée, allowlist explicite et échec fermé si la politique ne peut pas être déterminée.
9. Un decision model comme **Jev ne peut jamais élargir une permission** : son `state` peut contenir du texte adversarial.
   Il peut réduire le bruit ou demander une escalade, mais push, déploiement, suppression et secrets restent régis par code/policy.
```

Le contenu du dépôt ne doit jamais pouvoir élargir son propre périmètre d'autorisation.

---

# 10. Gestion du contexte et des coûts

## Pipeline recommandé

```text
Sourcebot / ScalaSemantic / Codebase-Memory si polyglotte / rg / IntelliJ
→ workers isolés si exploration volumineuse
   ├── recherche / codebase
   ├── graphe sémantique Scala / impact structurel JVM
   ├── Metals / types / diagnostics
   ├── tests / logs
   └── documentation
→ résumés courts
→ Claude Code parent : plan + petit diff
→ tests déterministes
→ Codex reviewer dans un contexte frais
```

## À compresser avec RTK / Headroom

* logs CI ;
* sorties `sbt test` longues ;
* gros `git diff` ;
* `rg` massif ;
* JSON volumineux ;
* documentation longue ;
* listings de fichiers.

## À ne pas compresser agressivement

* code source à modifier ;
* tests critiques ;
* `build.sbt` ;
* migrations ;
* stack traces Scala complexes ;
* erreurs d'implicits/givens ;
* contrats JSON publics.

Les cinq leviers de coût cumulables sont : routage vers modèles bon marché, compaction du contexte, prompts scopés avec
chemins de fichiers, prompt caching et Batch API quand elle est adaptée.

> **Context rot.** Ne confonds pas trois limites différentes :
>
> ```text
> capacité physique     = combien de tokens entrent dans la fenêtre ;
> récupération          = le modèle retrouve-t-il encore l'information pertinente ;
> raisonnement utile    = sait-il encore l'appliquer correctement parmi tout le reste ?
> ```
>
> La littérature 2026 montre que les deux dernières peuvent se dégrader progressivement **bien avant** la saturation
> physique. À tâche identique, ajouter du contexte inutile peut réduire la qualité même lorsque l'information pertinente
> est toujours présente. Les symptômes typiques d'une longue session agentique sont : contraintes anciennes moins
> saillantes, retour d'hypothèses déjà réfutées, relecture répétée des mêmes fichiers, boucles de correction et abandon
> prématuré malgré une information suffisante.
>
> Un transcript long n'est donc pas une meilleure mémoire. Dans une session de code, il accumule aussi `rg`, sorties
> MCP,
> logs, anciennes versions du diff, résultats de tests, documentation et impasses. Le **working set décisionnel** doit
> rester petit :
>
> ```text
> objectif + contraintes + plan + décisions + diff courant + preuves essentielles
> ```
>
> La compaction (`/compact`) reste une compression avec pertes : elle intervient après l'accumulation et peut
> résumer un invariant discret, une hypothèse réfutée ou un détail rare. **Ne la traite pas comme un mécanisme normal de
> continuation.** Pour une tâche importante, préfère un handoff explicite et contrôlé (`HANDOFF.md` ou fichier d'état),
> puis une session fraîche. La parade structurelle reste l' **isolation en amont** : déléguer l'exploration volumineuse,
> les logs, les tests, la documentation et les investigations indépendantes à des sous-agents avec leur propre contexte,
> puis ne faire remonter que des conclusions courtes et sourcées.
>
> ```text
> 100K tokens explorés dans un worker
> → 1–2K tokens de résultat
> → parent propre pour décider et écrire
> ```
>
> Cette règle vaut aussi pour la review : **ne donne pas à Codex le transcript complet d'une longue session Claude**.
> Donne-lui une fenêtre fraîche avec `spec + diff final + fichiers modifiés + tests + invariants`. Tu obtiens à la fois
> une isolation de modèle et une isolation de contexte.

Pour le cache explicite OpenAI, raisonne en coût total : une écriture à 1,25× sans aucune réutilisation coûte plus cher
qu'un appel normal. Avec au moins une réutilisation du même préfixe pendant la durée de vie du cache, une écriture puis
une lecture à 0,1× coûtent 1,35× au total contre 2× sans cache. N'active donc un breakpoint que pour un préfixe stable
dont la réutilisation est probable, et mesure séparément tokens écrits, tokens lus, taux de hit et invalidations.

---

## Les quatre stratégies canoniques du context engineering

La discipline a été formalisée fin 2025 sous le nom de **context engineering** — définition Anthropic:
« l'ensemble des stratégies pour curer et maintenir l'ensemble optimal de tokens pendant l'inférence » ; formulation
Karpathy : « remplir la fenêtre de contexte avec exactement la bonne information pour l'étape suivante ». La taxonomie
de référence (LangChain) distingue quatre stratégies, que ce guide pratique déjà séparément — les nommer permet de
vérifier qu'aucune n'est oubliée :

| Stratégie    | Question posée                                      | Mise en œuvre dans ce guide                                                                                      |
|--------------|-----------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| **Write**    | Qu'est-ce qui doit survivre hors de la fenêtre ?    | `AGENTS.md`, `MIGRATION_STATE.md`, auto-memory, journaux de tâches, registre de dette                            |
| **Select**   | Qu'est-ce qui entre dans la fenêtre, et quand ?     | Sourcebot / ScalaSemantic / Codebase-Memory / rg / Metals MCP, récupération juste-à-temps                        |
| **Compress** | Qu'est-ce qui peut perdre des tokens sans signal ?  | RTK / Headroom sur logs et diffs, sorties tronquées, handoff structuré ; `/compact` seulement en dernier recours |
| **Isolate**  | Qu'est-ce qui doit vivre dans une fenêtre séparée ? | Subagents read-only, worktrees, reviewer no-write, sessions distinctes par tâche                                 |

Deux règles opérationnelles qui découlent de cette grille et que le reste du guide ne couvre pas explicitement :

- **Progressive disclosure des outils** : chaque serveur MCP ajoute ses schémas d'outils à la fenêtre de chaque session.
  Limite les serveurs et outils activés par agent (l'ACP d'IntelliJ et Claude Code le permettent) et préfère la
  découverte à la demande — la roadmap MCP d'août 2026 fait d'ailleurs de la *progressive discovery* des catalogues
  d'outils une priorité du protocole. Sur un gros catalogue, **Jev peut servir de pré-sélecteur** : choisir quelques
  skills/outils candidats avant de charger leurs définitions dans le contexte du LLM.
- **Compaction comme décision, pas comme réflexe** : un score Jev peut signaler `topic_shift` ou
  `old_context_still_needed`, mais c'est le harness qui décide ensuite de compacter. Ne laisse jamais le decision model
  réécrire lui-même l'historique ; conserve les décisions et artefacts durables dans `HANDOFF.md` /
  `MIGRATION_STATE.md`.
- **Budget de sélection** : si un élément de contexte ne change aucune décision de l'étape courante, il n'appartient pas
  à la fenêtre. Mesure périodiquement la part des tokens qui ont réellement influencé la sortie (taux de cache hit,
  redondance des fichiers injectés) : une fenêtre grande n'est pas une excuse pour un contexte non filtré.

>
> **Qwen Code rend désormais ce budget observable.** Les versions 0.23.x affichent la part du contexte consommée par le
> system prompt, les outils intégrés, MCP, mémoire, skills et messages. Les versions 0.24.x ajoutent l'attribution du
> coût
> en tokens aux fichiers de contexte/extensions, des limites sur les grandes *tool surfaces*, une allowlist d'outils par
> subagent et la construction du system prompt à partir du **resident tool set** réellement actif. Les outils différés
> peuvent rester hors du préfixe tout en préservant le prompt cache. Utilise ces métriques comme audit empirique :
> **retire ou diffère un provider, une extension ou un outil qui consomme régulièrement du contexte sans modifier une
> décision**.

> **Chiffres et cascade pour ce budget.** Les travaux 2025-2026
> convergent sur un objectif d'utilisation de **~30–40 % de la fenêtre** en régime normal (une fenêtre de 200K vise
> ~60–80K de contenu réel, pas 190K) : au-delà, le *context rot* s'installe même avec de la capacité restante. Trois
> résultats concrets à intégrer :
> - **concevoir les sorties d'outils d'abord** : modes silencieux, troncature (ex. > 2 000 tokens → écrit sur
>   disque + preview de 10 lignes), champs actionnables plutôt que JSON brut. Cela étend le contexte effectif de
>   ~3–4× sans aucune infrastructure de compression ; résumer par LLM ce qu'un outil aurait pu ne pas émettre est
>   la version payante du même problème ;
> - **masquage d'observation avant résumé LLM** : un benchmark JetBrains sur SWE-bench Verified montre que
>   remplacer les anciens outputs d'outils par des placeholders (en gardant le squelette actions/raisonnement)
>   réduit les coûts de ~52 % sans allonger les trajectoires, alors que le résumé LLM pur (−50 % de coût) allonge les
>   trajectoires de ~15 %. Les couches sans LLM traitent la majorité de la pression ; le résumé est le backstop cher ;
> - **résumés structurés à champs fixes** (intention, progression, faits clés, artefacts, prochaine étapes, questions
>   ouvertes) : ils battent la prose libre, mais **aucune approche ne préserve bien la trace des artefacts** (fichiers
>   créés/modifiés) — d'où le fichier d'état maintenu hors du pipeline de compression, et la vigilance sur les
>   « résumés de résumés » qui perdent les détails des premières heures.
>
> Ces pratiques répondent aux quatre modes de défaillance nommés dans la taxonomie de référence : *context poisoning*
> (une hallucination référencée en boucle), *context distraction* (le modèle surpondère l'historique au détriment de
> l'objectif), *context confusion* (du contenu superflu dégrade même sans saturation — cas canonique : échec avec
> 46 outils, succès avec 19, à fenêtre identique) et *context clash* (une correction coexiste avec l'erreur
> qu'elle remplace, ~−39 % de performance). Ce sont les causes racines que les stratégies Write / Select / Compress /
> Isolate ci-dessus neutralisent une par une.

> **Validation industrielle, pas benchmark contrôlé.** GitHub a documenté la migration du runtime
> Copilot de TypeScript vers **832 378 lignes de Rust de production**, livrée progressivement en **128 PRs**. Le retour
> d'expérience mesure **96,22 % de cache reads** sur le volume de tokens d'entrée et **5 116 compactions** ; les
> subagents
> dépensent leur contexte dans une fenêtre séparée puis ne retournent que leur réponse au parent, tandis que les
> sessions
> qui écrivent en parallèle disposent de leur propre branche et worktree. C'est une confirmation industrielle très forte
> de **préfixe stable + Isolate + map→reduce + worktrees**, mais pas une preuve causale généralisable à tous les dépôts.
>
> Le même retour insiste sur deux garde-fous déjà présents ici : les **tests E2E doivent rester un oracle indépendant
que
> l'agent ne peut pas réécrire silencieusement**, et une migration doit **traduire le comportement d'abord, redesigner
> ensuite**. Pour une migration Scala/JVM, protège donc les tests de caractérisation et contrats avant de donner au
> writer
> la permission de modifier l'implémentation.

#### Arbre de décision : continuer vs handoff + session fraîche vs `/compact`

L'erreur la plus coûteuse en crédits est de continuer une session polluée. Voici l'arbre de décision à appliquer toutes
les ~15 interactions ou dès qu'un symptôme de context rot apparaît :

```text
Session en cours
│
├─ L'agent répète une hypothèse déjà réfutée ou accumule les erreurs ?
│  └─ OUI → STOP → HANDOFF.md vérifié → nouvelle session
│             (ne PAS changer seulement de modèle dans la conversation polluée)
│
├─ Le contexte contient > 50 % de tokens non décisionnels
│  (logs bruts, rg massif, anciennes versions du diff) ?
│  └─ OUI → écrire HANDOFF.md :
│             objectif, contraintes, plan, décisions, artefacts,
│             diff courant, preuves, erreurs non résolues, prochaine action
│           → relire le handoff
│           → nouvelle session avec ce working set minimal
│
├─ La tâche a changé de nature ?
│  (bugfix → refactor, feature → migration)
│  └─ OUI → nouveau cadrage complet (Étape 0) + nouvelle session
│
├─ Le modèle utilise encore correctement les invariants et non-objectifs ?
│  └─ NON → ré-injecter la charte si le contexte reste sain ;
│           sinon handoff + nouvelle session
│
└─ Aucune condition ci-dessus → continuer
```

`/compact` devient le **plan B**, réservé aux cas où la surface impose de conserver la session. Avant de l'utiliser,
fais produire puis relis un handoff structuré ; après compaction, vérifie explicitement que les invariants, décisions,
artefacts et erreurs ouvertes ont survécu. Si un détail critique manque, abandonne la session compactée.

Règle métrique : si le ratio (tokens dans la fenêtre) / (tokens réellement cités ou utilisés dans les 3 dernières
réponses) dépasse 5:1, la session est en surpoids. Le défaut est **handoff + session fraîche**, pas davantage de
compression.

---

## Exemple : structurer une requête cachable en Scala 3

La discipline de la section 4 (statique en haut, dynamique en bas) se traduit directement dans la construction de la
requête. Les blocs marqués `cache_control` sont facturés ~5 à 10 % du tarif input à partir du deuxième appel (5 % sur
Sonnet 5.5 et Opus 5.5) — à condition
d'être octet pour octet identiques entre les appels :

```scala
import io.circe.Json
import io.circe.syntax.*

object CacheablePrompt:

  // STATIQUE — chargé une fois au démarrage, jamais reconstruit dynamiquement :
  // toute interpolation (timestamp, compteur...) dans ces blocs casse le cache.
  def systemBlocks(agentsMd: String, scalaRules: String): Json =
    Json.arr(
      Json.obj(
        "type"          -> "text".asJson,
        "text"          -> agentsMd.asJson,
        "cache_control" -> Json.obj("type" -> "ephemeral".asJson)
      ),
      Json.obj(
        "type"          -> "text".asJson,
        "text"          -> scalaRules.asJson,
        "cache_control" -> Json.obj("type" -> "ephemeral".asJson)
      )
    )

  // DYNAMIQUE — change à chaque itération, va dans messages, jamais dans les blocs cachés
  def userMessage(diff: String, compileErrors: String): Json =
    Json.obj(
      "role"    -> "user".asJson,
      "content" -> s"Diff courant :\n$diff\n\nErreurs :\n$compileErrors".asJson
    )

  def request(agentsMd: String, scalaRules: String, diff: String, errors: String): Json =
    Json.obj(
      "model"      -> "claude-sonnet-5-5".asJson,
      "max_tokens" -> 4096.asJson,
      "system"     -> systemBlocks(agentsMd, scalaRules),
      "messages"   -> Json.arr(userMessage(diff, errors))
    )
```

Vérifie le cache hit dans la réponse (`usage.cache_read_input_tokens > 0`) et logge-le : un taux de cache hit qui
s'effondre signale presque toujours un en-tête de prompt devenu instable — exactement le bug de la règle 4 de la section

4.

<!-- NOUVELLE SECTION -->

# 10A. Observabilité des appels LLM

Un workflow agentique sans télémétrie se pilote à l'intuition — et l'intuition sous-estime systématiquement les coûts
des boucles d'échec. Trois métriques suffisent pour piloter : **coût par tâche mergeable**, **latence P50/P99 par
modèle**, **taux de cache hit**.

## Tracing avec otel4s

```scala
import cats.effect.*
import org.typelevel.otel4s.Attribute
import org.typelevel.otel4s.trace.Tracer

final case class LlmUsage(
    model: String,
    inputTokens: Int,
    outputTokens: Int,
    cacheReadTokens: Int,
    costUsd: BigDecimal
)

// Chaque appel LLM devient un span : visualisable dans Jaeger/Grafana Tempo,
// agrégeable en métriques de coût par task_type via les attributs.
def traced[F[_]: Tracer: Concurrent](taskType: String)(call: F[LlmUsage]): F[LlmUsage] =
  Tracer[F]
    .span(
      "llm.call",
      Attribute("llm.task_type", taskType)
    )
    .use { span =>
      call.flatTap { u =>
        span.addAttributes(
          Attribute("llm.model",          u.model),
          Attribute("llm.tokens.input",   u.inputTokens.toLong),
          Attribute("llm.tokens.output",  u.outputTokens.toLong),
          Attribute("llm.tokens.cached",  u.cacheReadTokens.toLong),
          Attribute("llm.cache.hit",      u.cacheReadTokens > 0),
          Attribute("llm.cost.usd",       u.costUsd.toString)
        )
      }
    }
```

Le coût se calcule côté client (tokens × tarif du modèle, table de la section 3) — ne dépends pas du fournisseur pour
cette métrique, les champs varient. Pour les `tool_use`, logge chaque appel d'outil en JSON structuré (nom, durée,
succès) : c'est ce qui permet de voir qu'un agent a passé 40 tours sur `bash` au lieu de 3 sur
`compile-file`.

## Choisir sa couche d'observabilité

| Option                        | Effort d'intégration         | Forces                                                 | Limites                                                   |
|-------------------------------|------------------------------|--------------------------------------------------------|-----------------------------------------------------------|
| **otel4s** (OpenTelemetry)    | Moyen (instrumentation code) | Standard, s'agrège avec le tracing applicatif existant | Pas de vue "LLM" préfabriquée — dashboards à construire   |
| **Logs JSON structurés**      | Faible (logback + appender)  | Zéro dépendance nouvelle, suffisant pour le suivi solo | Pas de traces distribuées, agrégation manuelle            |
| **Langfuse** (spécialisé LLM) | Faible (SDK ou proxy)        | Vues coût/latence/prompt prêtes, replay des sessions   | Service supplémentaire à héberger ou SaaS — à auditer     |
| **Dashboard OpenRouter**      | Nul                          | Suffisant pour suivre les rares appels de secours      | Ne voit ni Claude Max, ni Codex abonnement, ni Qwen local |

Pour l'usage actuel : le dashboard OpenRouter suffit pour les **appels externes exceptionnels**, tandis que les quotas
Claude, Codex, Copilot et JetBrains restent suivis dans leurs surfaces respectives. N'introduis pas Grafana uniquement
pour unifier quelques appels mensuels. otel4s devient pertinent quand le LLM entre dans le produit (section 7A) ou quand
les appels API sont suffisamment automatisés pour justifier une observabilité centralisée.

L'observabilité des agents de code est devenue une catégorie produit en soi (ex. Amazon CloudWatch « Coding Agent
Insights », juillet 2026, qui agrège la télémétrie de Claude Code, Codex et GitHub Copilot). Pour un usage solo, tes
trois métriques suffisent ; mais c'est le signe que la mesure du comportement des agents est désormais traitée comme un
poste de coût à part entière, pas comme un raffinement.

# 10B. OpenRouter comme porte de sortie ponctuelle

Pour le workflow actuel, **aucune gateway locale n'est nécessaire** : OpenRouter sert uniquement de porte de sortie vers
les modèles de secours. Crée une clé dédiée, fixe une limite de dépense côté compte et sélectionne explicitement le
modèle à tester.

```text
Claude Code / Codex bloqués
→ préparer un reproducer minimal
→ OpenRouter
→ choisir volontairement GLM / Kimi / Gemini / Grok
→ conserver le nom du modèle et du provider dans le journal de tâche
```

Le principe est volontairement simple : **OpenRouter ne devient pas le chemin normal de développement**. Claude Code,
Codex, Qwen local, GitHub Copilot et JetBrains AI continuent d'utiliser leurs surfaces natives.

> État de la route Gemini.** Google a fermé l'accès
> gratuit/Pro/Ultra à Gemini CLI le 18 juin 2026 ; son successeur Antigravity CLI est closed-source avec un quota
> gratuit très réduit (ordre de grandeur : ~20 requêtes/jour). Ne compte plus sur « un troisième agent gratuit » côté
> Google : pour un avis Gemini en dépannage, la voie rationnelle reste l'API ou OpenRouter, ce que cette section
> prévoit déjà. Leçon générale pour tout le stack : ne bâtis jamais un workflow sur un quota gratuit — il peut
> disparaître en cours de trimestre.

## Configuration minimale

Une seule variable d'environnement suffit pour les scripts ou outils qui utilisent OpenRouter :

```bash
export OPENROUTER_API_KEY="..."
```

Pour une intégration Scala ponctuelle, garde la même abstraction `LlmClient[F[_]]` que dans la section 7A et injecte une
configuration dédiée :

```scala
import zio.*

final case class OpenRouterConfig(
    apiKey: String,
    baseUrl: String = "https://openrouter.ai/api/v1"
)

object OpenRouterConfig:
  val layer: ZLayer[Any, SecurityException, OpenRouterConfig] =
    ZLayer.fromZIO {
      for
        key <- System.env("OPENROUTER_API_KEY").someOrFail(
                 SecurityException("OPENROUTER_API_KEY manquante")
               )
      yield OpenRouterConfig(key)
    }
```

Le client conserve alors un endpoint OpenAI-compatible sans introduire de serveur local supplémentaire.

## Règles de fallback

Pour ce guide :

```text
Provider fallback pour le même modèle
→ autorisé

Fallback automatique vers un autre modèle
→ désactivé par défaut
```

Le changement de provider améliore la disponibilité sans changer la nature de l'analyse. Un changement automatique de
modèle brouille au contraire l'objectif recherché : obtenir consciemment une opinion issue d'une autre famille de
modèles.

## Règles de confidentialité

OpenRouter agrège plusieurs providers dont les politiques peuvent différer. Pour du code professionnel :

```text
- envoyer le minimum de contexte nécessaire ;
- préférer un reproducer, une stack trace et les fichiers strictement concernés ;
- ne jamais envoyer le repository entier par défaut ;
- anonymiser les données métier et secrets ;
- choisir explicitement les providers compatibles avec les exigences du projet ;
- garder les parties les plus sensibles en local ou chez les fournisseurs directs déjà approuvés.
```

## Ce qu'OpenRouter ne doit pas remplacer

```text
Claude Code        → agent principal raisonnement/debug + reviewer croisé via abonnement Claude
Codex              → agent principal d'exécution + reviewer croisé via abonnement ChatGPT
Qwen local         → modèle local direct
GitHub Copilot     → workflow GitHub
JetBrains AI       → assistance IDE
OpenRouter         → escalade exceptionnelle vers d'autres modèles
```

Cette séparation évite de transformer une simple porte de secours en nouvelle couche d'infrastructure à maintenir.

---

# 11. Quand utiliser Aider — et où placer OpenCode/Qwen Code

Aider reste utile, maintenu et très efficace pour du **pair programming terminal orienté Git** : on lui donne des
fichiers précis, il produit des patches lisibles, et l'historique Git reste l'undo stack.

OpenCode est un agent open source plus généraliste, avec terminal, IDE/desktop selon configuration, sessions multiples
et intégrations LSP/MCP. Pour Scala, c'est intéressant, mais il faut rester précis : certaines capacités LSP sont encore
documentées comme expérimentales ou dépendantes d'un flag de configuration, et **Metals ne fait pas partie des LSP
câblés nativement** — la demande d'intégration ouverte sur le dépôt OpenCode (janvier 2026) est toujours au stade de
discussion mi-juillet 2026. En pratique, le feedback compilateur Scala fiable dans OpenCode passe soit par une config
LSP manuelle, soit par le **Metals MCP standalone** (section 9), qui reste la voie recommandée. Ne base donc pas une
décision d'architecture d'équipe uniquement sur “OpenCode a du LSP”. Teste-le sur ton repo, avec Metals, puis mesure la
qualité des diffs.

Qwen Code est désormais plus qu'un simple harness pour Qwen : **Auto-Memory, Auto-Skills, subagents, MCP, LSP, worktrees
Git, mode headless et fournisseurs OpenAI/Anthropic/Qwen/local** en font une alternative open source sérieuse à Claude
Code et Codex. Les versions **0.24.x** renforcent précisément les points qui comptent pour ce guide : chaque `agent()`
peut recevoir une **allowlist explicite d'outils**, les workflows enregistrent des checkpoints et peuvent être repris ou
relancés, les subagents peuvent être isolés en conteneur, et le contexte injecté par fichiers/extensions ainsi que la
*tool surface* deviennent mesurables et limitables. Depuis **0.24.7**, les outils différés peuvent être **lazy-loadés en
Code Mode** : `tools.eager` conserve seulement les schémas nécessaires dans la requête initiale, les autres restent
enregistrés et sont découverts via `tool_search` → `tool_call`. La même release ajoute une **mémoire à rappel structuré
à la demande** et poursuit les sessions/workspaces durables. C'est une implémentation particulièrement nette de
`Select + Isolate` : retire les schémas inutiles du préfixe sans perdre la capacité d'appeler l'outil plus tard. La
fondation de sandbox Linux s'appuie désormais sur `bwrap`. **Agent Teams** et **Agent Arena** restent expérimentaux ;
Arena est particulièrement utile pour le benchmark privé, car plusieurs modèles peuvent recevoir la même tâche dans des
worktrees isolés. `/advisor` fournit un second avis indépendant. Le choix face à OpenCode reste empirique : qualité des
patches Scala, stabilité avec Metals, coût total et qualité de la gestion des permissions. Local Control doit rester
limité à un réseau local de confiance.

Le bon partage des rôles :

```text
Claude Code       = Opus 5.5/Sonnet 5.5 pour raisonnement, debugging et micro-dev
Codex             = Sol 6.2/Luna pour ownership d’issues et micro-dev OpenAI
OpenCode/QwenCode = harness pour Qwen local, modèles API et tâches parallèles isolées
Aider             = micro-diffs git-first quand tu veux un commit/petit patch par étape
```

> **Rappel** : ne branche pas ton abonnement Claude Max sur OpenCode ou un autre harness tiers. Pour les harness tiers,
> utilise Qwen local ou des clés API conformes aux conditions du fournisseur.

## Quand utiliser Aider

Utilise-le pour :

* petit patch ciblé ;
* correction d'un test ;
* renommage local ;
* migration mécanique simple ;
* modification où le diff Git est central ;
* boucle lint/test très courte.

Ne l'utilise pas pour :

* architecture ;
* gros legacy ;
* bugs multi-modules ;
* refactor métier profond ;
* décision de design.

Aider est d'autant meilleur que tu respectes cette règle : **ajouter peu de fichiers, donner une demande précise,
vérifier le diff, lancer les tests ciblés**. Si tu ajoutes trop de fichiers, tu recrées le problème que tu voulais
éviter : contexte coûteux, attention diluée, diff plus large.

Si cette discipline t'importe moins que le feedback LSP, OpenCode/Qwen Code peuvent mieux couvrir les mêmes cas, mais
seulement après validation locale sur ton repo Scala.

---

## Comparatif synthétique des trois harness

| Critère                 | Aider                            | OpenCode                              | Qwen Code                             |
|-------------------------|----------------------------------|---------------------------------------|---------------------------------------|
| Philosophie             | Diff Git-first, minimal          | Agent généraliste, sessions multiples | Agent aligné écosystème Qwen          |
| Qualité de diff (Scala) | Très bonne sur petit scope       | Variable — à mesurer sur ton repo     | Variable — à mesurer sur ton repo     |
| Support LSP/Metals      | Non (repo map statique)          | Oui, partiellement expérimental       | Oui ; valider Metals sur le repo      |
| MCP                     | Non natif                        | Oui                                   | Oui                                   |
| Local / BYOK            | Oui (tout endpoint compatible)   | Oui                                   | Oui, optimal avec Qwen local          |
| Undo / traçabilité      | Excellente (un commit par étape) | Sessions, moins Git-centré            | Sessions                              |
| Maturité Scala          | Éprouvée sur micro-diffs         | Prometteuse, non éprouvée             | Harness mûr ; qualité Scala à mesurer |

La colonne décisive n'est pas dans le tableau : c'est **la qualité des diffs sur ton repo**, mesurée sur dix tâches
réelles avec la grille de métriques de la section 3. Le tableau sert à savoir quoi tester, pas à décider.

## Exemple : la commande de test que tout harness doit recevoir

Le levier numéro un de la boucle lint/test est une commande commune, reproductible et rapide. Ne déduis pas
`FooSpec` du nom de `Foo.scala` : la suite peut porter un autre nom et un `testOnly` sans test sélectionné peut
réussir. Sur une CI propre, `git diff HEAD` ne voit pas les commits de la PR. Fixe donc une **base Git immuable**
et compare-la au candidat (merge base), en tenant compte de tous les états Git pour le feedback local.

Exemple `scripts/ai-validate.py` (Python 3, Git, sbt ; adapter `MODULES`, la politique de chemins et les rapports
JUnit au projet). Les suites listées doivent couvrir tous les modules de test, y compris les modules d'intégration ;
une suite sans test exécuté exige une configuration explicite, pas un succès silencieux.

```python
#!/usr/bin/env python3
"""Repository-specific example: adapt and protect the module map and policy."""
import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MODULES = {"api/": "api", "integration/": "integration"}
PROTECTED_NAMES = {"build.sbt", "plugins.sbt", "AGENTS.md", "CLAUDE.md", "CODEOWNERS", ".gitmodules"}
PROTECTED_DIRS = {".github", ".claude", ".codex", ".agents", "project", "migrations", "scripts"}
MAX_FILES, MAX_LINES = 20, 600


def git(*args):
    return subprocess.check_output(["git", *args])


def nul_paths(*args):
    return {p.decode("utf-8", "surrogateescape") for p in git(*args).split(b"\0") if p}


def changed_paths(base):
    # Union of committed, staged, unstaged and untracked paths; count renames as delete/add.
    return (nul_paths("diff", "--name-only", "-z", "--no-renames", base, "HEAD")
            | nul_paths("diff", "--cached", "--name-only", "-z", "--no-renames", base)
            | nul_paths("diff", "--name-only", "-z", "--no-renames", base)
            | nul_paths("ls-files", "--others", "--exclude-standard", "-z"))


def protected(path):
    parts = Path(path).parts
    return (bool(set(parts) & PROTECTED_DIRS) or Path(path).name in PROTECTED_NAMES
            or path.endswith(".sbt"))


def check_diff(base, head):
    # A final proof requires a committed candidate; never ignore untracked files.
    if git("status", "--porcelain=v1", "-z", "--untracked-files=all"):
        raise ValueError("Dirty candidate (including untracked files); inspect and commit authorized files first")
    raw = git("diff", "--raw", "-z", "--no-renames", base, head).split(b"\0")
    for metadata, raw_path in zip(raw[0:-1:2], raw[1:-1:2]):
        old_mode, new_mode = metadata[1:].split(b" ", 2)[:2]
        if {old_mode, new_mode} & {b"120000", b"160000"}:
            raise ValueError(f"Symlink or submodule requires separate review: {raw_path!r}")
    records = git("diff", "--numstat", "-z", "--no-renames", base, head).split(b"\0")
    count, lines = 0, 0
    for record in filter(None, records):
        added, removed, raw_path = record.split(b"\t", 2)
        path = raw_path.decode("utf-8", "surrogateescape")
        if protected(path):
            raise ValueError(f"Protected path requires separate human-approved policy: {path!r}")
        if added == b"-" or removed == b"-":
            raise ValueError(f"Binary change requires separate review: {path!r}")
        count += 1
        lines += int(added) + int(removed)
    if count > MAX_FILES or lines > MAX_LINES:
        raise ValueError(f"Diff exceeds policy: {count} files, {lines} lines")
    return {"files": count, "lines": lines}


def select_modules(paths):
    # Unknown/shared changes or no identified tests -> all declared test modules.
    if not paths or any(not any(p.startswith(prefix) for prefix in MODULES) for p in paths):
        return list(MODULES.values())
    return [module for prefix, module in MODULES.items()
            if any(path.startswith(prefix) for path in paths)]


def run_step(args, results):
    rc = subprocess.run(args, check=False).returncode
    results.append({"argv": args, "exit_code": rc})
    if rc:
        raise ValueError(f"Command failed ({rc}): {args!r}")


def verify_reports(prefix):
    # Adapt to actual report paths and frameworks; after clean, no stale reports.
    executed = 0
    for report in Path(prefix).glob("target/**/TEST-*.xml"):
        suite = ET.parse(report).getroot()
        if suite.tag != "testsuite":
            raise ValueError(f"Unexpected report format: {report}")
        if int(suite.get("failures", "0")) or int(suite.get("errors", "0")):
            raise ValueError(f"Failed tests in report: {report}")
        executed += int(suite.attrib["tests"]) - int(suite.get("skipped", "0"))
    if executed <= 0:
        raise ValueError(f"No executed tests proven for {prefix}")
    return executed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Approved full Git commit SHA")
    parser.add_argument("--mode", choices=["targeted", "validate"], required=True)
    parser.add_argument("--sbt2", action="store_true")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    root = Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve()
    receipt = args.receipt.resolve()
    if receipt == root or root in receipt.parents:
        parser.error("Receipt must be outside the repository")
    import os
    os.chdir(root)
    result = {"base": args.base, "mode": args.mode, "steps": [], "status": "FAILED"}
    try:
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", args.base):
            raise ValueError("Expected a full immutable base SHA")
        head = git("rev-parse", "HEAD").decode().strip()
        base = git("merge-base", args.base, head).decode().strip()
        result.update(head=head, merge_base=base)
        if args.mode == "validate":
            result["diff"] = check_diff(base, head)
            modules = list(MODULES.values())
            # Full final validation, not a heuristic selection.
            run_step(["sbt", "scalafmtCheckAll", "compile", "Test/compile"], result["steps"])
        else:
            modules = select_modules(changed_paths(base))
        result["modules"] = modules
        test_task = "testFull" if args.sbt2 else "test"
        for prefix, module in MODULES.items():
            if module not in modules:
                continue
            # Explicit module suite: do not infer test names from source filenames.
            command = ["sbt", f"project {module}"]
            if args.mode == "validate":
                command.append("clean")
            run_step([*command, test_task], result["steps"])
            if args.mode == "validate":
                result.setdefault("executed_tests", {})[module] = verify_reports(prefix)
        if args.mode == "validate":
            if git("rev-parse", "HEAD").decode().strip() != head:
                raise ValueError("Candidate SHA changed during validation")
            check_diff(base, head)
            result["status"] = "PASSED"
        else:
            result["status"] = "FEEDBACK_ONLY"
    except (OSError, ValueError, subprocess.SubprocessError, ET.ParseError, KeyError) as exc:
        result["error"] = str(exc)
    finally:
        receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    return 0 if result["status"] in {"PASSED", "FEEDBACK_ONLY"} else 1


if __name__ == "__main__":
    sys.exit(main())
```

`--mode targeted` ne produit que du feedback, même si les tests sont verts. Il inspecte aussi les fichiers
non suivis et les modifications locales. Si aucun module fiable n'est identifié, il exécute toutes les suites
déclarées. Dans un build réel, étends la sélection aux dépendants impactés (ex. api → intégration) ; le fallback
reste toutes les suites lorsque l’impact est incertain. `--mode validate` exige un candidat committé et un worktree propre, contrôle le diff complet,
exécute les suites complètes après `clean`, vérifie les rapports de tests, le SHA et la propreté finale. Il
refuse les chemins protégés, binaires, symlinks et changements de sous-module par défaut ; toute exception est une décision humaine dans une
politique de validation séparée et approuvée, jamais un argument de bypass donné au writer.
`--sbt2` utilise `testFull` au lieu de `test` pour une réexécution exhaustive en sbt 2.x.
Le script est un exemple de harness à adapter et tester ; le scope exact de la spec et les exceptions doivent
être vérifiés par un humain ou une allowlist de chemins approuvée indépendamment. Il ne couvre pas à lui seul tous les builds Scala,
les sous-modules, les tests hors JUnit ou les fichiers ignorés. La CI doit s’exécuter dans un checkout isolé
et propre, avec la politique de confiance (section 15A). Ne confonds pas rapport JSON et attestation inviolable.

Wrapper `scripts/ai-test-changed` (exécutable, partagé par Aider, Codex et Claude) :

```bash
#!/usr/bin/env bash
set -euo pipefail
: "${AI_BASE_SHA:?Set the approved base commit SHA first}"
repoRoot=$(git rev-parse --show-toplevel)
receiptDir=$(mktemp -d)
printf 'Local feedback receipt: %s\n' "$receiptDir/validation.json"
exec python3 "$repoRoot/scripts/ai-validate.py" --base "$AI_BASE_SHA" \
  --mode targeted --receipt "$receiptDir/validation.json" "$@"
```

Au démarrage, fixe `AI_BASE_SHA` à la révision approuvée (pas à `HEAD` réévalué après chaque commit).
Par exemple, dans le worktree de tâche :

```bash
export AI_BASE_SHA="$(git rev-parse origin/main)"
aider --test-cmd "./scripts/ai-test-changed"
```

Avant de pousser la PR, sur un candidat propre et committé :

```bash
receiptDir=$(mktemp -d)
python3 scripts/ai-validate.py --base "$AI_BASE_SHA" --mode validate \
  --receipt "$receiptDir/validation.json"
```

Conserve la preuve structurée dans le paquet de review (base, merge base, SHA candidat, commandes, codes
de retour, nombre de tests exécutés et statut). Si la validation est absente, échoue ou porte sur un autre SHA,
ne déclare pas « done ». Les scripts de validation eux-mêmes nécessitent des tests : sortie sbt non nulle sans
`[error]`, untracked, commit déjà créé, fichier renommé vers un chemin interdit, rapport absent/vide, SHA changé.
Exécute ces cas sur un repo temporaire et un sbt simulé avant de promouvoir la politique.
Ces exemples ont été éprouvés avec un dépôt Git temporaire et un sbt simulé ; cela valide la logique des scripts,
pas les commandes sbt ni les chemins de rapports de ton projet. Les checks end-to-end restent à exécuter en CI.


---

# 12. Quand utiliser Codex / OpenAI en plus de Claude Code

Codex est un très bon **critique OpenAI**, second agent contrôlé ou arbitre indépendant ; **GPT‑6.2 Astra relève son
plafond de capacité** sans changer ce rôle. Il ne doit pas nécessairement remplacer Claude Code. Depuis juillet 2026, il
vit aussi dans l' **application ChatGPT Desktop** : choisis **Codex**
pour le travail de développement local, **Work** pour une tâche agentique de connaissance ou de documents, et **Chat**
pour une conversation ponctuelle. L'app Codex précédente devient cette app Desktop ; le CLI et l'extension IDE restent
adaptés au terminal et à IntelliJ, tandis que Codex Cloud délègue une tâche dans un environnement hébergé.

Le rôle « reviewer / second agent » reste une **doctrine de ce guide**, mais Codex est aussi devenu un **control plane
multi-session** : `codex agents` permet de suivre plusieurs tâches, `codex queue` d'adresser des sessions locales ou
distantes, et les Agent Plugins rendent skills/outils plus portables. Les versions récentes ont également durci les
permissions et le sandbox, et rattachent la consommation des sous-agents imbriqués au budget de l'objectif racine.
Utilise ces capacités pour isoler des worktrees ou des pistes d'investigation ; elles ne justifient toujours pas deux
writers concurrents sur les mêmes fichiers.

Depuis **Codex 0.154**, les worktrees gérés sont aussi disponibles directement via `--worktree` ou `/worktree`, et le
**mid-run steering** permet de préciser ou réorienter la tâche pendant que l'agent continue son exécution. Utilise le
worktree natif quand tu restes dans Codex ; garde `git worktree` manuel comme fallback portable entre Claude Code,
Codex, Qwen Code et les scripts. La même release a supprimé `codex mcp-server` : voir section 9 pour la distinction
**Codex client MCP** / **Codex App Server non-MCP**.

Les versions **0.158–0.159** complètent surtout l'intégration et le contrôle en cours d'exécution : les MCP OAuth qui
exigent un **client secret pré-enregistré** sont pris en charge (`codex mcp add --oauth-client-secret`), les connexions
WebSocket directes à exec-server peuvent être protégées par bearer token, les commandes exécutées avec privilèges élevés
demandent par défaut une approbation terminal, et l'option **`instant_interrupt`** permet de réorienter Codex pendant
une réponse modèle ou certains appels Code Mode longs. Ce sont des améliorations de harness et de sécurité, pas une
raison d'assouplir les approbations.

**Codex Cloud** utilise maintenant des **environnements réutilisables** : dépôt, dépendances, outils et paramètres sont
préparés et publiés une fois, puis chaque nouvelle tâche reçoit son propre workspace isolé. Une tâche existante conserve
son état et peut continuer pendant que le poste local dort, depuis desktop, web ou mobile. L'environnement partagé
réduit le setup ; il ne remplace ni les commits ni les tests déterministes.

| Surface                           | Quand l'utiliser pour Scala                                                             | Garde-fou                                                                    |
|-----------------------------------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **IntelliJ 2026.2 → Codex (ACP)** | Review interactive dans l'IDE avec contexte projet et authentification ChatGPT/OpenAI.  | Préférer le mode no-write pour le rôle de reviewer ; permissions explicites. |
| **ChatGPT Desktop → Codex**       | Exploration interactive, worktrees, revue de diff, tests locaux et travail multi-repos. | Choisir explicitement les permissions et le périmètre du dossier.            |
| **Codex CLI / extension IDE**     | Boucle courte terminal/IntelliJ, commandes ciblées, diff en contexte.                   | Conserver les règles `AGENTS.md` et ne pas contourner les approbations.      |
| **Codex Cloud**                   | Tâche isolée, parallélisable ou longue, à partir d'un repo préparé.                     | Vérifier l'environnement, les secrets et le diff avant merge.                |
| **API Responses**                 | Routeur, review automatisée, intégration Scala typée, observabilité et budgets.         | Utiliser une clé API, des limites de coût et des tests déterministes.        |

Utilise Codex / OpenAI pour relire les diffs Claude, challenger un plan d'architecture, inspecter les risques de
régression, produire un second avis sur un bug difficile, vérifier les invariants et cartographier un module legacy.
Pour sécurité, performance et concurrence, reste dans un cadre défensif, autorisé et humainement validé.

Pour un workflow **Claude Code writer → Codex reviewer**, l'intégration ACP d'IntelliJ est particulièrement adaptée :
Claude travaille via son plugin/CLI officiel avec l'abonnement Claude Max, puis Codex est sélectionné dans AI Chat et
s'authentifie avec le compte ChatGPT. Cette séparation conserve deux harness, deux familles de modèles et deux quotas
indépendants. Elle évite aussi de consommer les AI Credits JetBrains pour la review lorsque Codex utilise directement
l'authentification OpenAI.

Cette séparation doit aussi rester **contextuelle** : Codex ne gagne rien à recevoir les centaines de milliers de tokens
de la trajectoire Claude. Pour une review, reconstruis un paquet frais `spec + non-objectifs + diff + tests + invariants

+ risques ouverts`. La self-review Claude sert au nettoyage évident ; Codex sert de reviewer externe avec **zéro dette
  conversationnelle** de l'auteur.

Évite deux agents en écriture dans le même worktree :

```text
Claude modifie les fichiers
Codex modifie les mêmes fichiers
Claude corrige
Codex remodifie
→ conflit, dérive, crédits brûlés
```

#### Commandes worktree concrètes pour le workflow multi-agent

Le worktree isole les fichiers de travail et l’index pour deux writers, **pas leurs permissions**. Codex peut désormais créer et reprendre
ses worktrees nativement ; les commandes Git ci-dessous restent la **procédure portable et explicite**, indépendante du
harness :

# 1. Créer un worktree pour une tâche spécifique

`git worktree add ../project-feature-x -b feature/task-x main`

# 2. Créer un worktree pour la review (lecture seule)

`git worktree add --detach ../project-review-x "$headSha"`

Récupère au préalable le SHA exact de la PR ; communique aussi le SHA de base et calcule le merge base.
Ne reviewe pas `HEAD` de `main` par défaut.

# 3. Lister les worktrees actifs

`git worktree list`

# 4. Travailler dans le worktree (sandbox séparée à configurer)

`cd ../project-feature-x`

# Claude Code travaille ici avec ses permissions limitées à ce dossier

# 5. Vérifier l'état depuis le repo principal

`git -C ../project-feature-x diff --stat`
`git -C ../project-feature-x log --oneline -5`

# 6. Merger le résultat (après review humaine)

`Ouvrir la PR puis merger via les rulesets / required checks après review humaine.`

# 7. Nettoyer le worktree après merge

`git worktree remove ../project-feature-x`
`git branch -d feature/task-x`

# Script utilitaire : scripts/ai-worktree.sh

```sh
#!/usr/bin/env bash
# Usage: ./scripts/ai-worktree.sh create|list|remove|merge <name> [base]
set -euo pipefail
ACTION="${1:-list}"
NAME="${2:-}"
BASE="${3:-main}"
if [[ "$ACTION" != "list" && ! "$NAME" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]]; then
  echo "Invalid worktree name" >&2
  exit 1
fi

case "$ACTION" in
  create)
    BRANCH="agent/${NAME}"
    DIR="../$(basename "$(pwd)")-${NAME}"
    git worktree add "$DIR" -b "$BRANCH" "$BASE"
    echo "Worktree créé : $DIR (branche $BRANCH)"
    echo "cd $DIR && claude"
    ;;
  list)
    git worktree list
    ;;
  remove)
    DIR="../$(basename "$(pwd)")-${NAME}"
    git worktree remove "$DIR" # Refuses dirty worktrees
    git branch -d "agent/${NAME}" # Refuses unmerged branches
    echo "Worktree supprimé : $DIR"
    ;;
  merge)
    echo "Merge through the reviewed PR and required checks." >&2
    exit 1
    ;;
esac
```

Règles de sécurité worktree :

- Un worktree = un agent = une tâche. Jamais deux agents dans le même worktree.
- Le worktree principal (main) est réservé à l'humain et à la CI.
- Tout worktree agent doit être créé depuis une branche propre (pas de WIP).
- Le merge d'un worktree agent passe TOUJOURS par une review humaine.
- Nettoie les worktrees après merge : un worktree orphelin est de la dette.

**Isolation effective.** Un worktree partage les refs et une partie de la configuration Git, ainsi que les
credentials/caches du compte utilisateur si rien ne les sépare. Donne à chaque agent une sandbox avec racines
d'écriture explicites, un répertoire temporaire, des outils MCP en moindre privilège et des secrets distincts ;
pour du code non fiable, préfère un conteneur/VM sans montage de `$HOME`, sans socket Docker ni clés de production.
En local, refuse le full-access / bypass ; côté Codex configure sandbox et approbations, côté Claude sandbox et
permissions allow/deny, puis teste des tentatives d'écriture hors périmètre et d'accès réseau interdites.
Les hooks sont des signaux/contrôles complémentaires, non une frontière de confinement.

| Rôle | Droits effectifs |
|------|------------------|
| Researcher / reviewer | Lecture dépôt ; aucun push ; scratch isolé si test de reproduction |
| Writer | Écriture dans sa sandbox et branche de tâche ; push seulement autorisé |
| Steward | Corrections sur la PR explicitement transférée ; jamais merge / force-push |
| CI non fiable | Checkout, compile, tests ; token lecture, aucun secret privilégié |
| Release pipeline | Identité et secrets dédiés à l'environnement, après gate humain/politique |

Sépare les accès réseau et tokens GitHub par rôle ; ne donne pas les credentials de déploiement à l'agent.
Les commentaires de PR, logs et fichiers non fiables sont des données, pas de nouvelles permissions.


Le workflow sûr :

```text
worktree A : writer choisi par la nature de la tâche
worktree B : l’autre famille peut expérimenter ou reviewer
diff final : humain arbitre
review : modèle indépendant no-write
tests : CI / IntelliJ / sbt
```

### Parallélisme inter-issues et WIP

Pour un développeur solo, commence avec deux User Stories indépendantes au maximum, y compris les PR en review.
Un writer Codex et un writer Claude peuvent avancer sur des branches distinctes ; chacun fournit à l'autre un
paquet de review frais. Déclare les dépendances, modules/fichiers partagés, contrats et ordre d'intégration avant
de démarrer. Les stories qui modifient un même invariant ou une migration doivent être séquencées ; seule leur
exploration read-only peut être parallèle. Intègre et revalide après chaque merge. Dès que la review ou la CI
s'accumule, termine l'existant avant de lancer un ticket. Mesure débit livré et minutes humaines, pas le nombre
d'agents actifs.

Routage recommandé :

| Besoin                                        | Modèle / effort Codex                                         |
|-----------------------------------------------|---------------------------------------------------------------|
| Résumé PR, release note, message de commit    | GPT‑6 Luna Light/Medium                                       |
| Micro-dev / patch précis sous contrôle humain | **GPT‑6 Luna High**                                           |
| Issue standard end-to-end                     | **GPT‑6.2 Sol Medium**                                        |
| Feature ou bug difficile                      | **GPT‑6.2 Sol High**                                          |
| Review d'une PR écrite par Claude             | **GPT‑6.2 Sol Medium** ; High si risquée                      |
| Audit critique / limite de capacité Sol       | **GPT‑6.2 Astra Light** puis Medium/High si nécessaire          |
| Cartographie legacy multi-axes                | **GPT‑6.2 Sol Ultra** seulement si les axes sont indépendants |

Traduction concrète dans `~/.codex/config.toml` (profils à adapter après mesure) :

```toml
# Défaut agentique quotidien
model = "gpt-6.2-sol"
model_reasoning_effort = "medium"

[profiles.micro]        # patch ciblé, tests, transformations mécaniques
model = "gpt-6-luna"
model_reasoning_effort = "high"

[profiles.deep]         # feature complexe, migration, bug difficile
model = "gpt-6.2-sol"
model_reasoning_effort = "high"

[profiles.frontier]     # capacité supérieure ponctuelle
model = "gpt-6.2-astra"
model_reasoning_effort = "low"

[profiles.audit]        # qualité-first exceptionnel
model = "gpt-6.2-astra"
model_reasoning_effort = "high"
```

Pour la **Responses API**, `model_reasoning_effort` s'arrête à `max`. Certains SDK/harness Codex récents exposent
cependant aussi `ultra` comme effort : ne rends donc pas ce fichier portable dépendant de cette valeur sans vérifier la
version du client. **Ultra comme effort** et **Ultra/Multi-agent comme orchestration** sont deux notions distinctes ;
dans les deux cas, impose budget, durée, preuves attendues et espace de travail isolé.

Et le pendant dans un document de routage utilisateur (`docs/llm-routing.md` si la politique est partagée), référencé à la demande :

```text
## Sélection de modèle

- GPT-6 Luna High pour micro-dev, tests simples et transformations mécaniques sous contrôle humain
- GPT-6.2 Sol Medium pour l'agentic coding quotidien ; High pour feature/bug/migration difficiles
- GPT-6.2 Astra Light pour une escalade de capacité ; augmenter l'effort seulement si nécessaire
- Sonnet 5.5 Medium pour micro-dev Claude ; Opus 5.5 Medium pour l'agentic coding, High pour architecture/debugging
- Fable 5.2 Low si Opus High plafonne réellement (High pour une mission longue autonome)
- Reviewer = famille différente du writer
- Ultra / multi-agent seulement pour des axes indépendants ; jamais plusieurs écritures sur le même worktree
```

Règle stricte : une mission Ultra ne doit jamais écrire directement dans le worktree principal d'une application legacy.
Elle doit d'abord produire un plan, des micro-PRs, des tests de caractérisation et des règles d'arrêt. L'application
éventuelle se fait ensuite par étapes, avec test et review humaine.

## Exploiter la review Codex en machine : décodage typé

Avec la classification de sévérité de la section 5 (étape 7) et l'ADT `ReviewResult` de la section 7B, une sortie Codex
**déjà triée et étayée** devient une donnée exploitable par un gate de merge plutôt qu'un texte à relire. Les constats
bruts du modèle restent dans une étape de triage : seuls un test, une règle déterministe ou une décision humaine les
promouvent au gate.

```scala
import io.circe.parser.decode
import zio.*

object CodexReviewGate:

  def parse(raw: String): IO[LlmError, ReviewResult] =
    // Les modèles entourent parfois le JSON de ```json ... ``` malgré la consigne — nettoyage défensif
    val cleaned = raw.replaceAll("(?s)```json|```", "").trim
    ZIO.fromEither(decode[ReviewResult](cleaned))
      .mapError(e => LlmError.Decode(s"Sortie Codex non conforme : ${e.getMessage}"))

  // Le gate ne reçoit que des findings préalablement validés :
  // BLOCKING et REGRESSION_RISK doivent être vides (ou contestés explicitement).
  def gate(review: ReviewResult): IO[String, Unit] =
    val blocking = review.findings.filter(f =>
      f.severity == Severity.Blocking || f.severity == Severity.RegressionRisk
    )
    ZIO
      .fail(
        blocking
          .map(f => s"[${f.severity}] ${f.file} — ${f.message}")
          .mkString("Retours à traiter avant merge :\n", "\n", "")
      )
      .when(blocking.nonEmpty)
      .unit
```

Notez la symétrie avec le principe directeur : l'humain reste l'arbitre (il peut contester un `BLOCKING`), mais le
chemin par défaut est déterministe. Une sortie Codex non parsable fait échouer le gate — un reviewer qui ne respecte pas
le format convenu ne valide rien.

## GitHub Copilot : couche GitHub-native, pas troisième reviewer profond

Si le repository vit sur GitHub, Copilot apporte une valeur complémentaire à Claude Code et Codex **au niveau du
workflow GitHub**, pas comme troisième chat généraliste dans IntelliJ. La **GitHub Copilot app** ajoute une vue « My
work » pour parcourir issues et PR, démarrer une session depuis une issue, examiner les checks, demander la correction
d'un commentaire ou d'une CI rouge et, si tu l'autorises, piloter l'atterrissage de la PR. Utilise cette surface comme
control plane GitHub ; garde IntelliJ + Claude Code pour l'implémentation locale exigeante et Codex pour la review
indépendante.

```text
Issue GitHub bien spécifiée
→ Copilot coding agent possible pour une petite tâche bornée
→ PR
→ CI déterministe
→ Copilot Code Review automatique
→ Codex Terra / Sol si review profonde nécessaire
→ humain
```

Usages où Copilot est réellement utile :

```text
✅ parcourir et prendre en charge des issues depuis GitHub ;
✅ déléguer une petite issue bien bornée à un coding agent ;
✅ créer / suivre une PR et ses checks ;
✅ reviewer automatiquement les nouvelles PR ou les nouveaux pushes ;
✅ proposer des corrections depuis les commentaires de review ;
✅ exploiter AGENTS.md, instructions GitHub, skills et MCP dans la review ;
✅ compléter CodeQL / Code Quality par un signal LLM GitHub-native.
```

Usages où il devient surtout redondant :

```text
❌ architecture ou bug Scala difficile déjà traité par Opus 5.5 ;
❌ troisième review manuelle systématique après Codex Sol 6.2 ;
❌ deuxième writer sur la même branche pendant qu’un agent principal travaille ;
❌ remplacement de sbt, tests, mutation testing, CodeQL ou review humaine.
```

**Copilot Code Review est un signal, pas un gate d'approbation.** Une review Copilot est publiée avec le statut
`Comment`, pas `Approve` ou `Request changes` ; elle ne compte donc pas comme approbation requise et ne bloque pas le
merge à elle seule. C'est une bonne place pour une review automatique peu frictionnelle, tandis que Codex reste le
reviewer indépendant déclenché volontairement sur les changements non triviaux ou risqués.

La règle de concurrence reste la même que pour tous les agents : si Copilot cloud agent applique un correctif, Claude
Code et Codex ne doivent pas écrire simultanément sur la même branche. Utilise une délégation claire, ou un worktree /
une branche séparée, puis fais arbitrer le diff par l'humain.

## Claude Ship : automatiser l'après-PR, pas la responsabilité du merge

**Claude Ship** est une couche GitHub post-implémentation, indépendante du coding agent qui a produit la PR. Elle
sépare trois responsabilités : trouver les défauts, appliquer des corrections et évaluer une politique d'approbation.
Ne la confonds ni avec un nouveau modèle, ni avec `/code-review` ou Ultrareview (reviews à la demande).

| Surface | Rôle | Accès / consommation |
|---------|------|----------------------|
| **`/ship`** | Commit/push, ouverture de PR si nécessaire, review locale puis surveillance des checks et retours | Claude Code local ; usage normal de la session |
| **`/steward`** | Surveillance et corrections d'une PR déjà ouverte, sans review initiale | Claude Code local ; usage normal de la session |
| **Code Review** | Review statique multi-agent, vérification et classement des findings, commentaires inline et check | Team/Enterprise ; crédits d'usage ; GA |
| **PR Steward** | Corrections de CI, conflits et feedback ; commits sur la branche et compte rendu des changements | Team/Enterprise ; crédits d'usage ; beta |
| **Claude Approvals** | Évaluation de `.claude/approvals.yml`, check et éventuellement approbation GitHub | Team/Enterprise ; classifiers et reviews déclenchées facturés ; beta |

Le service d'organisation agit via la Claude GitHub App, sans nécessiter Claude Code comme writer. Il n'est pas
inclus dans Claude Max et n'est pas disponible avec ZDR, la configuration HIPAA ou les clés CMEK. Les commandes
locales agissent, elles, avec tes propres identités Git/GitHub. Vérifie leur présence après mise à jour de Claude Code,
avec `gh auth status` et un clone local GitHub. La référence détaillée des commandes est liée dans les sources.

### Workflow solo : `/ship` ou `/steward` avec Codex et Claude Code

```text
Writer Codex ou Claude → spec satisfaite + tests locaux verts
→ vérifier le diff, les fichiers non suivis et les secrets avant tout push
→ ouvrir la PR ; /ship si tu veux aussi une review Claude locale
→ /steward si la PR est déjà ouverte et que seule la surveillance est utile
→ correctifs mécaniques bornés → stop de la surveillance
→ review indépendante de l'autre famille sur le SHA final
→ CI verte → humain : merge
```

Pour ton usage Claude Max + Codex, teste d'abord `/steward` sur une petite PR : évite de repayer une review initiale
si Opus/Sol l'a déjà faite. Si Claude a écrit ou corrigé le code, garde Codex comme reviewer indépendant. Si Codex a
écrit et que Claude a aussi appliqué les corrections, exige une review fraîche des corrections par Codex et relis
l'ensemble du diff ; deux modèles intervenus ne constituent pas automatiquement deux jugements indépendants.

**Attention à `/ship` :** la commande peut committer des changements non commités, y compris des fichiers non suivis,
et pousser sans confirmation interactive bloquante. Ne compte pas sur la détection de noms de fichiers sensibles pour
protéger le contenu. Vérifie `git status`, le diff staged et unstaged, les nouveaux fichiers, le scan de secrets et
le remote avant de l'invoquer. Préfère une branche dédiée et un worktree dont le contenu est déjà validé.

La surveillance locale peut exécuter du code récupéré depuis GitHub avec tes droits : ne l'active que sur un dépôt
et une branche dont les contributeurs autorisés sont de confiance. Ne laisse pas un commentaire de PR élargir la
spec ou les permissions. Utilise un environnement sans secrets de production, et arrête la boucle avec `/ship stop`
(ou interruption de la session) avant d'intervenir sur la même branche. Les restrictions natives des actions sans
message utilisateur ne remplacent ni les règles GitHub ni les garde-fous locaux.

### Workflow équipe : adoption progressive, pas trois agents obligatoires

- **Code Review** : commence par `Standard`, `Quick` pour les changements routiniers, `Deep` pour les dépôts critiques.
  Anthropic choisit les modèles ; ces niveaux ne sont pas les efforts d'Opus. Configure `REVIEW.md` pour les invariants
  Scala et la sévérité des findings ; la review lit les règles de la branche de base ou par défaut, pas celles proposées
  par la PR. Elle ne compile ni n'exécute le code et son check ne constitue pas un veto sur le merge.
- **PR Steward** : commence en mode manuel (`@claude steward`) avec un seul dépôt pilote et un plafond de dépense.
  Il écrit sur la branche sans demander pour chaque correction et traite aussi les retours de bots. Exclure de sa
  délégation les changements d'architecture, les conflits sémantiques, les migrations et les fichiers critiques.
  `@claude stop` ou le retrait du label `claude-pr-steward-watching` arrête la surveillance de la PR.
- **Claude Approvals** : commence en `mode: observe` sans rendre le check bloquant. La politique vient de la branche
  par défaut, combine les règles applicables les plus strictes et peut utiliser des chemins, faits de PR et classifiers.
  Protège `.claude/approvals.yml`, `REVIEW.md`, `CODEOWNERS` et les workflows CI comme des fichiers critiques.
  Voir les limites d'approbation en section 15A.

Pour une PR Scala, limite le steward à une correction de lint, un import, une erreur de compilation locale ou un
finding reproduit. Stop après deux échecs identiques, tout écart au scope ou tout besoin de modifier un invariant.
Ne lui demande jamais de rendre la CI verte en affaiblissant un test, une assertion ou un check. Un conflit qui touche
une règle métier n'est pas une correction mécanique. Ces règles sont ton protocole d'exploitation : elles doivent
être contrôlées indépendamment, pas supposées garanties par le service.

**Claude Ship vs Copilot :** ce sont des couches post-PR partiellement concurrentes. Garde un seul flux automatique de
review par défaut et un seul writer correctif par branche. Le service Claude peut être pertinent pour le volume en
équipe ; en solo, les commandes locales et la review croisée existante évitent un nouvel abonnement et des reviews
redondantes. Mesure sur des PR comparables : minutes humaines jusqu'au merge, coût total (reviews, corrections, CI),
findings réellement utiles, correctifs hors scope, nombre de pushes, défauts échappés et reverts. Les gains de volume
et de reverts annoncés par Anthropic sur ses propres repos concernent un processus complet, pas un effet causal isolé
de Claude Ship ni une preuve spécifique à Scala.

## Équivalent Codex de Claude Ship : review, correction et surveillance

Codex couvre les mêmes besoins par plusieurs primitives, sans imposer une suite d'agents post-PR. Ne confonds pas
review, autorisation d'écriture et autorisation de merge.

| Besoin | Claude | Codex |
|--------|--------|-------|
| Préparer et ouvrir une PR | `/ship` | Prompt de finalisation : tests → `/review` local si utile → commit/push → PR |
| Surveiller une PR existante | `/steward` | **Goal mode (`/goal`)** ou **Heartbeat** ; tâche Codex Cloud pour exécution hébergée |
| Review GitHub | Code Review | **Codex Code Review** : `@codex review` ou déclenchement automatique |
| Corriger un finding ou un échec CI | PR Steward | `@codex fix the P1 issue`, `@codex fix the CI failures` ou objectif Codex borné |
| Suivi persistant / automatisation hébergée | PR Steward | Codex Cloud (tâche bornée), événements GitHub (suivi partiel) ; GitHub Action si orchestration CI dédiée |
| Review de sécurité dédiée | Review spécialisée | `@codex security review` (selon éligibilité) |
| Politique d'approbation | Claude Approvals | GitHub Rulesets, CODEOWNERS et required checks ; équivalence partielle |

### Codex Code Review : privilégier les retours à fort signal

Connecte le dépôt à Codex et configure les reviews dans les paramètres Code Review. Pour une PR écrite par Claude,
`@codex review` fournit une review GitHub indépendante, centrée sur les défauts P0/P1. Les règles propres au dépôt
vivent dans `AGENTS.md`, idéalement sous `## Code Review Rules` près du module concerné (contrats JSON, compatibilité
binaire, concurrence, invariants métier). Exige des findings exploitables et étayés. Pour une review approfondie
pilotée par le senior, garde la session Codex fraîche et read-only de la section 5 : le modèle et l'effort de la
review hébergée ne se déduisent pas du sélecteur de la session locale.

Une mention `@codex` demandant un correctif peut lancer une tâche cloud et pousser sur la PR si les permissions le
permettent. Ce n'est plus une review read-only : ne la déclenche pas si un autre writer ou steward possède la branche.
Les instructions d'un commentaire GitHub ne peuvent ni étendre la spec ni autoriser une modification critique.

### Goal mode, Heartbeats et Codex Cloud : équivalent fonctionnel de `/steward`

Privilégie les primitives natives maintenues par OpenAI plutôt que l'ancien skill de surveillance retiré du dépôt
Codex et ses forks communautaires. Elles permettent de construire une boucle post-PR sans script Python archivé,
plugin tiers ni clé API OpenAI supplémentaire avec un compte ChatGPT éligible. Ce n'est pas un service PR Steward
identique à celui d'Anthropic : la durée de vie, les déclencheurs et les écritures GitHub dépendent du harness,
des permissions et du plan. **GPT‑6.2 Sol Medium** est le modèle de référence pour cette mission ; le choix du modèle
ne crée pas à lui seul une surveillance permanente.

| Surface | Mécanisme recommandé | Limite opérationnelle |
|---------|----------------------|-----------------------|
| Codex Desktop / CLI / extension IDE | `/goal` avec critères de sortie vérifiables | Session et environnement disponibles ; poste éveillé pour le travail local |
| Codex Desktop | Heartbeat (Scheduled task dans le chat) | Poste allumé et application active pour un dépôt local ; sandbox et permissions à vérifier |
| Codex Cloud | Tâche hébergée avec objectif explicite | Pas de garantie de boucle permanente ni de disponibilité de `/goal` sur le web |
| ChatGPT web / mobile | Tâches déclenchées par événements GitHub sur plans éligibles | Reviews, commentaires, commits, merges ; fin de CI et reprise du worktree Cloud non garanties |

#### Goal mode : objectif persistant et vérifiable

`/goal <objective>` attache l'objectif et ses critères de complétion à la session. Dans le CLI, `/goal` affiche
l'objectif ; `/goal edit`, `/goal pause`, `/goal resume` et `/goal clear` permettent de le modifier, suspendre,
reprendre ou retirer. Dans Desktop, utilise les contrôles de progression. Pour du code Scala local, garde le même
worktree et les preuves de la spec ; pas de nouveau writer en parallèle. Le modèle doit pouvoir vérifier la CI et
les retours publiés sur GitHub avec les outils réellement disponibles.

Gabarit pour une PR existante, après autorisation du push sur sa branche (GPT‑6.2 Sol Medium) :

```text
/goal Amène la pull request en cours à un état vérifié et prêt à fusionner.

Appuie-toi sur la spécification approuvée et AGENTS.md. Confirme l’URL de la PR, la branche de base, la branche source et le SHA initial.
Surveille les contrôles CI requis sur GitHub, la possibilité de fusionner et les retours de revue publiés. Avant chaque action,
actualise l’état de la PR et vérifie son SHA de tête. Arrête-toi en cas de changement inattendu ou d’écritures concurrentes.

Corrige uniquement les défaillances vérifiées liées à la branche et les constats qui appellent une action dans le périmètre approuvé.
Résous les conflits uniquement si le comportement attendu est sans ambiguïté. Garde des diffs minimaux.
N’affaiblis jamais les tests, les assertions, les contrôles de sécurité ou les exigences CI. Ne modifie aucun contrat public,
aucune dépendance, configuration de build, workflow ou schéma de base de données sans approbation explicite.
Réessaie au plus trois fois les opérations dont l’échec est clairement transitoire. Ne corrige pas de tests instables ni d’infrastructure sans rapport.
Après chaque correction, lance les contrôles ciblés requis, puis committe et pousse uniquement sur la branche autorisée de la PR.
Réévalue les contrôles requis et les retours de revue sur le nouveau SHA. Exige une revue indépendante du diff final.
N’approuve pas, ne fusionne pas, ne fais pas de force push et ne réponds pas aux relecteurs humains ni ne résous leurs fils sans autorisation.

Arrête-toi quand les contrôles requis passent sur le dernier SHA, que les conflits et les constats qui appellent une action sont résolus,
et qu’il ne reste qu’une revue indépendante ou une approbation humaine. Arrête-toi aussi si la PR ferme,
si des permissions manquent, si le périmètre doit s’étendre, si la même cause échoue deux fois ou après 60 minutes.
Indique les contrôles encore en cours ou indisponibles. Ne présente pas la PR comme prête.
Termine par un rapport concis en français avec l’URL de la PR, le SHA final, l’état de la CI, les correctifs poussés,
l’état de la revue indépendante, les constats non résolus et les blocages.
```

La durée de 60 minutes et les compteurs sont des limites de mission proposées, pas des timeouts garantis par le
produit. Interromps ou pause le goal si nécessaire ; ne confonds pas « objectif atteint » et approbation du merge.

#### Heartbeats : suivi récurrent sans session de raisonnement en continu

Les Scheduled tasks dans un chat (Heartbeats) réutilisent son contexte et permettent des intervalles courts en
minutes. OpenAI documente le cas de suivi d'une PR et de traitement de nouveaux retours. Préfère ce mécanisme
si le temps d'attente CI domine le travail : une reprise brève sur un événement nouveau plutôt qu'une boucle de
raisonnement permanente. Une reprise n'est pas gratuite. En local, le poste doit rester allumé et l'application
Desktop active. Teste d'abord une exécution manuelle, puis vérifie dans Scheduled le modèle, l'effort, le sandbox,
les autorisations et les conditions d'arrêt. Ne suppose pas que le prompt peut désactiver la tâche : vérifie son
état et désactive-la manuellement si nécessaire.

Gabarit à envoyer dans le chat Codex de la PR (sans Goal mode actif) :

```text
Mets en place dans cette conversation un suivi récurrent de la pull request GitHub actuelle toutes les 10 minutes.
Utilise GPT-6.2 Sol Medium si ce choix est disponible. Garde la spécification approuvée et les contraintes d’AGENTS.md.
Confirme l’URL de la PR, la branche autorisée, le SHA initial, les outils GitHub disponibles et la planification avant toute écriture.

À chaque exécution :
- Actualise le SHA de tête, les contrôles requis, la possibilité de fusionner et les retours de revue publiés.
- Déduplique par dépôt, PR, SHA et identifiant de constat ou de contrôle. Réponds brièvement si rien n’appelle d’action.
- Arrête-toi si la branche change de manière inattendue, si des écritures sont concurrentes, si des permissions manquent ou si un constat est hors périmètre.
- Corrige uniquement les défaillances vérifiées liées à la branche et les constats dont le traitement est autorisé. Exécute les tests ciblés,
  committe et pousse uniquement sur la branche de la PR. Contrôle à nouveau le nouveau SHA.
- Préserve les exigences de validation et les contrats publics. Écarte les refactorings et les changements de CI ou de dépendances sans rapport.
- Réessaie au maximum trois fois les opérations qui échouent de manière transitoire. Arrête-toi après deux corrections infructueuses pour une même cause.
- N’approuve pas, ne fusionne pas, ne fais pas de force push et n’interviens pas dans les fils des relecteurs humains sans autorisation.

Conserve entre les exécutions leur nombre, le dernier SHA, les constats traités et les compteurs de tentatives.
Arrête et désactive le suivi quand les contrôles requis passent sur le dernier SHA, sans conflit ni
constat appelant une action, et qu’il ne reste qu’une revue indépendante ou une approbation humaine. Arrête-toi aussi si la PR
ferme, si une intervention humaine est nécessaire, après six exécutions ou après 60 minutes.
Si la désactivation automatique est indisponible, signale qu’il faut désactiver la planification manuellement et cesse les modifications.
Rapporte uniquement les changements significatifs, en français, avec l’URL de la PR, le SHA final, les contrôles, les correctifs et les blocages.
```

#### Codex Cloud : même contrat, exécution hébergée

Pour travailler Mac éteint, utilise un environnement Codex Cloud publié (section 12) avec le dépôt, le JDK, sbt,
les outils de test et les accès GitHub nécessaires. Vérifie dans une première tâche non critique la branche cible,
la lecture des checks/logs et reviews, les permissions de push et, si nécessaire, de rerun CI. Un connecteur GitHub
ou la présence de `gh` ne garantit pas à lui seul ces droits. Utilise les secrets gérés et les domaines réseau
autorisés, pas de token dans le prompt ou le repo. Ne confonds pas l'environnement réutilisable avec la tâche
isolée qui s'y exécute, ni la possibilité de continuer sans le poste avec une garantie de surveillance indéfinie.

Pour une PR existante, sélectionne GPT‑6.2 Sol Medium et reprends intégralement le prompt Goal mode ci-dessus
**sans le préfixe `/goal`** si la commande n'est pas exposée par le client Cloud. Pour finaliser une User Story
avant cette surveillance, ajoute ce préambule (dans Cloud ou dans le chat local avant de lancer le goal) :

```text
Termine l’implémentation en cours conformément à la spécification approuvée et à AGENTS.md.
Lance le build, le formatage et les tests ciblés requis. Relis le diff pour vérifier sa correction, les régressions et le périmètre.
Avant de committer, vérifie les fichiers indexés, non indexés et non suivis, les secrets et le dépôt distant.
Committe, pousse et crée ou mets à jour la PR uniquement avec autorisation. Indique son URL et le SHA de tête.
Applique ensuite l’objectif de suivi borné de la PR ci-dessous dans le même environnement autorisé.
Si le push direct ou la création de PR est indisponible, indique le blocage exact et fournis le patch validé.
```

Si la tâche Cloud atteint sa limite avant la CI verte, reprends le même chat avec le SHA et l'état des checks ;
ne crée pas plusieurs tâches concurrentes sur la même branche. Aucun script externe ni plugin de babysitting
n'est nécessaire pour ce contrat. Les permissions, limites d'exécution et droits d'écriture restent à valider.

#### Routage et arrêt de la boucle

```text
Triage ou correction mécanique isolée → GPT‑6 Luna High
Stewardship end-to-end                → GPT‑6.2 Sol Medium (Sol 6.1 Medium en fallback)
Root cause difficile / conflit subtil → GPT‑6.2 Sol High, après requalification de la cause
Limite de capacité prouvée            → Astra Light si disponible, sur contexte propre
```

Ne mobilise ni Ultra ni Ultrafast par défaut : l'attente CI est essentiellement séquentielle. Mesure le nombre de
reprises, de pushes, les minutes humaines et la consommation jusqu'au merge. Un état vert sur un ancien SHA ne
prouve rien sur la version courante ; après correction, exige les checks et la review indépendante du diff final.

### Automations et GitHub Action : ne pas confondre les surfaces

Les événements GitHub dans les Scheduled tasks web/mobile peuvent filtrer par PR, auteur, titre ou label et
réagir aux reviews, commentaires, nouveaux commits ou merges. Les événements de fin/échec de CI et le transfert
automatique vers une tâche Codex Cloud existante ne sont pas garantis par la documentation. Préfère d'abord le
triage read-only et la notification si les droits d'écriture ou le contexte du worktree ne sont pas établis.
Ne cumule pas ce déclencheur avec un Heartbeat correctif ou un goal actif sur la même PR.

L'action officielle `openai/codex-action@v1` exécute `codex exec` en CI avec un prompt, un sandbox et des paramètres
de modèle/effort configurables. Elle permet une review ou une correction déclenchée par un événement GitHub, mais
ne constitue pas à elle seule un PR Steward permanent. Le tutoriel officiel d'autofix sépare la génération du patch
de sa publication ; respecte les protections de la section 15A. La voie standard avec clé API est un budget séparé.

> **Watch and Fix Pull Requests.** Des réglages desktop de surveillance/correction et d'auto-merge ont été observés
> par un tiers, mais leur disponibilité générale et leur contrat d'exécution ne sont pas établis par les références
> officielles consultées. À tester uniquement si exposés dans ton client ; garder l'auto-merge désactivé. Le workflow
> ne doit pas dépendre de ces réglages.

### Claude Code Cloud Auto-fix : stewardship événementiel en solo

Auto-fix est distinct de Claude Ship PR Steward (Team/Enterprise). Dans Claude Code Cloud, l'agent s'abonne
aux événements GitHub de la PR (échecs CI, reviews/commentaires) et peut pousser un correctif lorsque celui-ci
est clair. Aucun poste local à laisser allumé. Le suivi relève des limites Claude Code du plan compatible ;
l'installation de la Claude GitHub App sur le repository est requise.

Pour une PR créée en cloud, active Auto-fix dans le menu de la PR de la carte Changes. Depuis le CLI local
sur la branche de PR, `/autofix-pr` détecte la PR via `gh`, ouvre une session cloud et active le suivi.
Pour une PR existante (y compris écrite par Codex), donne son URL à une session Claude Cloud et demande
l'auto-fix. Arrête le suivi via le menu Auto-fix ou en demandant à Claude de ne plus surveiller la PR.

**Limites importantes :** GitHub ne notifie pas automatiquement Auto-fix d'un conflit causé par l'avancée
de la base ; inspecte la mergeabilité et demande un rebase explicite si nécessaire. Claude peut répondre aux
threads sous ton compte (réponse signalée comme agentique) ; audite les automatisations `issue_comment` qui
pourraient déclencher une opération privilégiée. N'active pas Auto-fix sur un dépôt où un commentaire peut
déclencher un déploiement ou une opération infra sans gate externe. Les consignes de durée et d'arrêt dans
le prompt ne sont pas un coupe-circuit système garanti ; vérifie la désactivation effective à la fin.

Prompt pour la session Claude Cloud :

```text
Active Auto-fix pour [PR_URL] uniquement après avoir vérifié qui contrôle la branche et quelle spécification est approuvée.
Surveille les retours de revue publiés et les échecs de CI. Corrige uniquement les défauts vérifiés, liés à la branche et dans le périmètre.
N’affaiblis jamais les tests, les assertions, la CI ou les contrôles de sécurité. Ne modifie ni les fichiers protégés ni les contrats publics.
Avant chaque correction, vérifie le SHA de tête, assure-toi qu’aucun autre agent n’écrit et lance la validation ciblée.
Committe et pousse uniquement les corrections minimales autorisées. Ne fais jamais de force push, n’approuve pas et ne fusionne pas.
Ne publie rien dans les fils de revue humaine et ne les résous pas sans autorisation explicite.
Arrête-toi et signale les constats ambigus, les conflits, les problèmes de permissions, deux cycles de correction infructueux
pour la même cause ou l’épuisement du budget de temps convenu.
Quand le SHA final passe les contrôles requis et qu’il ne reste aucun constat appelant une action, désactive Auto-fix et vérifie son arrêt.
Indique en français le SHA final, les preuves de CI, les modifications et les blocages.
```

### Transfert d'ownership et routage des stewards

| Writer | Reviewer indépendant | Steward par défaut |
|--------|----------------------|-------------------|
| Codex local | Opus 5.5 Medium | GPT‑6.2 Sol Medium, Goal ou Heartbeat |
| Codex Cloud | Opus 5.5 Medium | Codex Cloud, objectif borné |
| Claude Code local | GPT‑6.2 Sol Medium | Claude `/steward` |
| Claude Code Cloud | GPT‑6.2 Sol Medium | Cloud Auto-fix |

Une PR peut passer à l'autre fournisseur si le suivi natif y est plus adapté. Transfère explicitement
`repo + PR + branch + head SHA + base SHA + spec + findings autorisés + permissions + budget + conditions
d'arrêt`. Arrête le watcher, Heartbeat, Goal, Auto-fix et les tâches correctives existants avant d'autoriser
le nouveau writer ; vérifie l'absence de session concurrente et l'état distant avant chaque push.
Un changement inattendu de SHA interrompt le travail. Ne réutilise pas un vieux worktree comme source de
vérité. Après transfert, le steward est l'auteur des corrections : une nouvelle review indépendante des
changements et des preuves sur le SHA final reste requise.

**Choix solo :** si Codex écrit, Opus reviewe et Codex reprend les corrections via Goal mode, Heartbeat ou
Cloud (GPT‑6.2 Sol Medium) si nécessaire ; si Claude écrit, Codex reviewe et Claude reprend via `/steward` ou Cloud Auto-fix. Après toute correction, revalide les changements
sur le SHA final avec l'autre famille et les checks déterministes. Ne cumule pas systématiquement Codex Code Review,
Claude Code Review, Copilot et une review locale : un seul flux automatique par défaut, une review indépendante
proportionnée au risque, un seul writer correctif, puis l'humain arbitre.

## Note de positionnement : A2A face à MCP

Le protocole **A2A (Agent-to-Agent)**, initié par Google puis confié à la Linux Foundation, standardise la communication
*entre agents* de fournisseurs différents (découverte de capacités, délégation de tâches, suivi d'exécution), là où MCP
standardise la communication *agent ↔ outils*. Pour le workflow de ce guide, le verdict juin 2026 est simple : **A2A
n'apporte rien à un dev solo**. L'orchestration Claude ↔ Codex décrite ici passe par l'humain (et c'est une feature : tu
filtres les retours), et les subagents Claude Code ont leur propre mécanisme natif. A2A devient pertinent si une
organisation industrialise des agents hétérogènes (un agent Claude qui délègue formellement à un agent Codex hébergé
ailleurs) — auquel cas, réévaluer la maturité du protocole et de ses implémentations à ce moment-là, pas avant.

---

# 13. Paquet de review minimal pour réduire les retours

Avant de demander une review à Codex, Claude ou un collègue, prépare toujours un paquet court :

```text
Ticket/spec :
Objectif :
Non-objectifs :
Fichiers modifiés :
Base SHA / merge base / PR head SHA :
Diff base → candidat + fichiers non suivis :
Exigences → preuves (commandes, résultats, rapports et SHA) :
Tests exécutés :
Tests non exécutés et pourquoi :
Risques résiduels :
Questions ouvertes :
```

Ne donne pas seulement le diff. Une review sans spec produit des commentaires génériques ; une review avec objectif,
limites et tests produit plus souvent des retours actionnables.
Fournis d'abord le contrat et le diff sans les conclusions du writer ; les justifications viennent après
la première analyse indépendante. Le paquet doit être régénéré lorsque le SHA change.

> **Pourquoi ce paquet n'est pas optionnel.** LinearB, *Software Engineering Benchmarks Report* (8,1 M+
> PRs, 4 800+ organisations), distingue PRs assistées, PRs créées par agents et PRs non assistées. Le pickup
> (attente avant première prise en charge) est environ 4,6× plus long pour les PRs assistées ; les PRs agentiques
> attendent environ 17,6 h contre 3,4 h pour les non assistées (≈ 5,2–5,3× selon arrondis). Les PRs assistées
> peuvent être plus grosses (408 lignes contre 157 au 75e percentile). La métrique d'acceptation de LinearB
> est le **pourcentage des PRs ouvertes mergées dans les 30 jours** : 32,7 % pour les PRs IA de la catégorie
> publiée contre 84,4 % pour les non assistées. Ce n'est ni un taux de réussite des tests ni un taux de rejet
> définitif. Ne confonds pas les catégories : l'écart de pickup agentique n'est pas le chiffre des PRs assistées.
>
> Opsera, *AI Coding Impact Benchmark Report* (250 000+ développeurs, 60+ entreprises), étudie les gains de
> vitesse de création des PRs et le déplacement du goulot vers la review. DORA observe que l'IA amplifie les
> fondations existantes : les gains de débit n'impliquent pas une amélioration automatique de la stabilité.
> Ces rapports restent observationnels, avec des définitions et des tâches différentes ; ils ne démontrent
> pas la causalité pour ton dépôt. Priorité : PRs courtes, contrat explicite, WIP borné, preuve de validation
> et réduction du délai jusqu'à la production. Le seuil 600 lignes / 20 fichiers est un plafond d'alerte,
> pas une cible de taille de PR.

Pour les PRs agentiques, surveille particulièrement :

```text
- nombre de fichiers modifiés ;
- taille du diff ;
- fichiers hors scope ;
- CI rouge ;
- tests ajoutés qui ne peuvent pas échouer ;
- refactor non demandé ;
- changement implicite de contrat public ou JSON ;
- modification de build sans validation.
```

# 14. Planning hebdomadaire optimal

## Lundi : planification

* Découper les tickets.
* Identifier risques et tests.
* Préparer les contextes Sourcebot.
* Mettre à jour `AGENTS.md` si une règle projet commune manque ; `CLAUDE.md` seulement pour une règle spécifique Claude.
* Lancer Qwen sur la pré-analyse.

## Mardi à jeudi : production

* 1 à 2 grosses tâches Claude Code par demi-journée.
* Qwen pour boilerplate et pré-analyse.
* Codex pour review avant PR.
* Tests ciblés systématiques.
* Pas de tâche agentique ouverte sans critère d'acceptation.

## Vendredi : durcissement

* Review globale Codex.
* Tests plus larges.
* Nettoyage des diffs.
* Documentation.
* Analyse des coûts.
* Ajout de hooks si un type d'erreur s'est répété.

---

# 15. Définition de done pour une tâche agentique Scala

```text
- Objectif et contraintes explicités
- Plan validé avant modification
- Diff minimal
- Pas de refactor hors scope
- API publique inchangée ou changement documenté
- Sérialisation JSON inchangée ou testée
- Tests ciblés ajoutés ou mis à jour
- scalafmt / compile / tests ciblés OK
- Review second modèle effectuée
- Retours bloquants traités
- Risques résiduels listés
- Commandes exécutées documentées dans la PR
- Chaque exigence importante reliée à une preuve ; résultats et risques sur le SHA candidat
- CI indépendante et review finale sur les bons commits ; voir section 15B pour le done production
```

---

# 15A. CI/CD pour workflows agentiques

La CI est le juge final déterministe du principe directeur — à condition de l'adapter aux PRs agentiques, qui ont des
modes de défaillance spécifiques : tests qui ne peuvent pas échouer, diffs hors gabarit, boucles coûteuses.

## Les quatre gates spécifiques aux PRs agentiques

```text
1. Gate de gabarit et scope : diff base → candidat, fichiers protégés, taille et nombre de fichiers
2. Gate de qualité de test : suites réellement exécutées + mutation score et mutants importants selon risque
3. Gate de review : findings BLOCKING / REGRESSION_RISK vérifiés traités ou arbitrés humainement
4. Gate de budget : tout job appelant un LLM a un timeout ET un plafond de coût
```

Deux axes complémentaires à considérer une fois la base des quatre gates en place :

- **Contrôle de dérive d'architecture** : le Technology Radar de Thoughtworks (avril 2026) note que l'usage intensif
  d'agents accélère la dérive entre le code réel et l'architecture visée, et recommande de coupler des contrôles
  déterministes (fitness functions — ArchUnit, qui analyse le bytecode JVM et fonctionne donc aussi sur du Scala
  compilé) avec une évaluation LLM périodique. Une règle ArchUnit « le module `api` ne dépend pas de l'implémentation »
  exécutée en CI coûte moins qu'un tour d'agent et arrête une dérive structurelle que ni scalafmt ni Stryker4s ne
  voient.
- **Contrôle de duplication** : SlopCodeBench (section 1A) mesure une accumulation de duplication au fil des checkpoints
  agents ; un scan type jscpd (détecteur de copié-collé qui tokenise les sources Scala) sur les fichiers touchés
  transforme ce signal en métrique suivie, voire en gate. La duplication est le défaut le moins visible en review
  humaine et l'un des plus coûteux en maintenance différée.

Sur GitHub, **Copilot Code Review ou Codex Code Review peut s'ajouter comme signal automatique**, mais ne remplace
aucun de ces gates. Une review du bot n'est pas une approbation humaine ; vérifie les règles GitHub effectives.
Commence par une review sur demande ou à l'ouverture, puis réserve la re-review après correction aux changements qui
la justifient et aux nouveaux SHA qui exigent une validation indépendante.

**Claude Approvals n'est pas une preuve de qualité.** Une règle `claude: approves` ne déclenche pas à elle seule
Code Review ; `seats: 1` peut compter l'auteur et `seats: 0` peut permettre un merge sans lecture humaine. GitHub
peut également compter l'approbation du bot dans son quota de reviews. Pour le workflow de ce guide, garde
`claude: comments` au départ, des approbateurs humains indépendants en équipe, et un merge humain en solo. N'utilise
jamais un classifier probabiliste comme seul arbitre d'un changement critique.

La présence de `.claude/approvals.yml` peut désactiver les reviews automatiques sur les chemins couverts, même en
mode observe : pour les conserver, référence `claude/code_review` dans les règles (par exemple sous `advisory`).
Une condition Approvals ne lit pas les résultats de CI : conserve compile, tests, scalafmt, sécurité et mutation
testing comme required checks GitHub séparés. En équipe, protège la branche cible et la politique avec CODEOWNERS,
interdis les bypass aux agents et invalide les anciennes approbations lorsque le diff change. Ne rends le check
Approvals obligatoire qu'après avoir évalué les décisions en observe ; n'active ni auto-merge ni merge queue sans
un gate humain effectif pour les changements qui le nécessitent. Un check vert, une discussion résolue ou un commentaire
« aucun défaut » ne valent jamais une validation métier.

### GitHub Rulesets et indépendance du gate

Impose des required checks provenant de l'intégration attendue, sans bypass pour les identités d'agents ;
protège les branches cibles, interdiction de force-push et suppression, approbation des modifications récentes
et invalidation des anciennes approbations lorsque le diff change. En équipe, requiers l'approbation d'un
humain indépendant, et `CODEOWNERS` pour les fichiers de contrôle ; en solo, ne configure pas une règle
impossible à satisfaire par l'auteur, conserve le merge humain et un contrôle de politique séparé. Ne compte
pas une review bot comme un humain. Une merge queue est optionnelle, à condition de vérifier `merge_group`,
et d'exiger les gates du commit d'intégration. En cas de conflit, changement de SHA ou avancée de la base,
réévalue l'état ; une CI verte sur une ancienne révision ne valide pas le nouveau candidat.

## Exemple : `.github/workflows/ai-review.yml`

Exemple pour le dépôt à deux modules de la section 11 (sbt 1.x). Fige les actions à un SHA complet audité et
vérifie leurs dépendances transitives ; mets-les à jour par PR dédiée. Le SHA de base vient de l'événement GitHub,
pas d'un champ de PR contrôlé par son auteur. `github.sha` est le candidat d'intégration pour `pull_request` et
`merge_group` ; la review humaine porte sur le diff base/PR head, distinct de ce commit de test. Pour une merge
queue, les contrôles doivent être exécutés aussi sur le groupe de merge.

```yaml
name: ai-review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  merge_group:
    types: [checks_requested]

permissions:
  contents: read

concurrency:
  group: ai-review-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  deterministic-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          fetch-depth: 0
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1

      # Validate the integration candidate; fail on a missing base or wrong checkout.
      - name: Validate candidate
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}
          CANDIDATE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail
          test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
          test -n "$BASE_SHA"
          git merge-base --is-ancestor "$BASE_SHA" "$CANDIDATE_SHA"
          python3 scripts/ai-validate.py --base "$BASE_SHA" --mode validate \
            --receipt "$RUNNER_TEMP/validation.json"

  mutation-gate:
    needs: deterministic-checks
    runs-on: ubuntu-latest
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1
      # Configure Stryker's break threshold and inspect surviving mutants in the actual project.
      - name: Mutation testing
        run: sbt "project api" stryker
```

**Frontière de confiance de la CI :** ce YAML illustre les checks, pas un mécanisme inviolable à lui seul.
La PR peut modifier les scripts et le workflow qu'elle contient, voire les commandes de build ou les rapports.
Protège les workflows, scripts, règles de test, politiques et `CODEOWNERS` ; si disponible, impose un required
workflow de confiance issu d'un dépôt/commit protégé (ruleset d'organisation) et charge le validateur depuis
cette source plutôt que depuis le candidat. Une modification légitime de politique passe par une PR et une
validation humaines séparées. En solo sans required workflow externe, compare ces fichiers à la base et
n'autorise pas de merge tant qu'une modification de gate n'a pas été revue. Ne te repose pas sur une simple
convention `AGENTS.md`.

Le checkout de la PR peut exécuter du code arbitraire via sbt : aucun secret privilégié, aucun token d'écriture,
pas de `pull_request_target` exécutant le code de la PR, pas de cache partagé avec les jobs privilégiés sans
contrôle de provenance. Les rapports de test sont des preuves opérationnelles, pas des attestations inviolables
si le code de test lui-même est hostile. Archive les rapports et la provenance dans la CI selon la politique du
projet ; la validation doit être refaite sur le candidat final (et sur le commit livré si différent).

Points de doctrine :

* **les juges déterministes passent en premier** : compile, format et tests ciblés sont peu coûteux comparés à un appel
  LLM — un job LLM qui tourne sur du code qui ne compile pas est du budget brûlé ;
* si une review LLM de CI est réellement automatisée, donne-lui une **clé API dédiée**, un timeout et un plafond de
  dépense propre au job ; pour un usage principalement interactif via les abonnements Claude et ChatGPT, cette
  automatisation reste optionnelle ;
* **le job LLM est read-only** : il commente la PR, il ne committe jamais. Un agent qui corrige dans la CI recrée le
  problème « deux agents en écriture » de la section 16, en pire (sans humain dans la boucle) ;
* **`sbt --client` en local, JVM fraîche en CI** : le démon sbt est le levier des boucles locales ; en CI, un cache
  de dépendances contrôlé peut accélérer la résolution, mais ne remplace ni les tests ni l'isolation. **sbt 2.0.0 est stable depuis le 14 juin 2026** ; utilise au minimum **2.0.7**
  (ou **1.13.0** sur la branche 1.x) à cause du correctif BSP/TCP du 21 août :
  définitions de build en Scala 3, JDK 17 minimum, client natif `sbtn` (démarrage bien plus rapide — directement utile
  aux boucles agentiques), cache local/distant compatible Bazel et `test` incrémental. Ce guide suit la convention sbt
  1.x : la migration vers sbt 2.x est un changement de build critique qui ne se délègue jamais à un agent — plan humain,
  branche dédiée, vérification de la compatibilité des plugins (60+ portés, dont Play et Scala.js en cours), puis
  adaptation de ces jobs.

**Autofix Codex en CI : exception explicite au job de review read-only.** Si un flux correctif hébergé est réellement
nécessaire, sépare le job de génération du patch (sans droit de push) du job de publication contrôlée ; limite les
déclencheurs aux événements et acteurs approuvés. Ne lance jamais du code non fiable issu d'une PR avec des secrets ou
un token d'écriture privilégié (notamment via `pull_request_target`). Fige les actions par SHA, applique des permissions
minimales, un timeout, un budget externe et un verrou de concurrence par PR ; vérifie le head SHA avant publication,
puis relance les checks requis. Pas de force-push, d'auto-approbation ni de merge par le job LLM. Les commentaires,
logs et patches restent des données non fiables ; un échec ne doit jamais entraîner une modification des gates.

Le même découpage se transpose en GitLab CI : trois stages (`deterministic`, `mutation`, `llm-review`), mêmes gates,
`rules: changes` pour ne lancer Stryker que sur les modules touchés.

---

# 15B. Release engineering : de la PR mergeable au logiciel déployable

Le merge n'est pas la fin de la preuve. Pour un code métier en production, utilise une chaîne de validation
proportionnée au risque ; ne transforme pas les agents en opérateurs de production.

```text
spec + REQ/acceptance evidence
→ implementation gate (scope, compilation, tests)
→ review gate (independent findings, final PR head)
→ integration gate (CI on the actual merge candidate)
→ release gate (immutable artifact, staging, security)
→ production gate (authorized deployment, progressive rollout)
→ runtime verification (SLO, regressions, rollback)
```

**Release gate.** Construis une fois l'artefact du commit livré, teste cet artefact, identifie-le par digest
immuable (image OCI, JAR, distribution) et promeus-le sans le reconstruire entre staging et production.
Conserve le SHA source, le digest, les versions de build/dépendances, les résultats CI et, selon le projet,
SBOM, scans et attestation de provenance. L'identité de déploiement est distincte du writer et de la CI
qui exécute du code non fiable. Aucun secret de production dans les agents ; permissions temporaires et
environnement protégé par gate humain ou politique de release.

**Canary / rollout progressif.** Sur un service critique, déploie sur un périmètre réduit (instances, trafic,
tenants ou jobs pilotes) et compare au groupe de contrôle. Définis avant de commencer les métriques, seuils
d'erreur et de latence, fenêtre d'observation et volume minimum ; sans signal suffisant, suspends la promotion.
Augmente progressivement seulement si les SLO et invariants restent satisfaits. Pour un petit projet ou un job
non critique, staging + smoke tests et rollback reproductible peuvent suffire. Le canary n'est utile que si
les deux versions sont effectivement comparables et si la mesure permet de détecter les régressions.

| Application | Signaux de régression à surveiller |
|-------------|------------------------------------|
| Play / Tapir | 5xx, latence p95/p99, erreurs métier, taux de succès |
| Pekko / effets | mailboxes, timeouts, dead letters, ressources et saturation |
| Spark | volumes, schémas, nulls, partitions, doublons, erreurs, coût/durée de jobs |
| JVM | heap, GC, threads, CPU |
| Base de données | erreurs, locks, latence, intégrité, migration |

Instrumente logs structurés, métriques et traces (OpenTelemetry si adapté). Corrèle service/version/digest et
événement de déploiement. N'envoie ni PII ni secrets dans les logs/LLM. Définis les critères d'arrêt et
le responsable d'astreinte ; si un seuil est franchi, stoppe la promotion, rollback via le pipeline approuvé
ou désactive la fonctionnalité, puis ouvre un incident et un ticket de correction. Ne laisse pas un agent
corriger directement la production.

**Rollback.** Garde le dernier artefact sain, une procédure testée, les flags de désactivation et les preuves de
récupération. Une migration DB destructive ou une écriture irréversible ne s'annule pas en redéployant un JAR :
utilise expand/contract, compatibilité ascendante/descendante pendant le rollout, sauvegarde/restauration
éprouvées et plan de réconciliation pour les données. Pour Spark, privilégie les traitements idempotents,
rejouables et les sorties isolées avant promotion. L'humain valide les opérations irréversibles.

### Définition de done côté production

```text
- PR et candidat d'intégration validés.
- Artefact immuable identifié, testé et promu par le pipeline autorisé.
- Staging et smoke tests passants ; rollback / récupération testés selon risque.
- Canary ou rollout approuvé ; aucune alerte ou régression au-delà des seuils.
- Fenêtre d'observation terminée ; métriques et exceptions documentées.
```

Le premier état est « merge-ready », le deuxième « déployé », le dernier « stable ». Mesure séparément
ces états plutôt que d'attribuer le succès à un commit ou à une review verte.

---

# 16. Anti-patterns à éviter

| Anti-pattern                                                                         | Pourquoi c'est mauvais                                                                                   |
|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| “Améliore ce module”                                                                 | Trop vague, diff large                                                                                   |
| Donner toute la repo                                                                 | Coûte cher, noie le signal                                                                               |
| Laisser l'agent refactorer spontanément                                              | Diffs difficiles à reviewer                                                                              |
| Trois agents sur la même branche                                                     | Conflits et perte de contrôle                                                                            |
| Review IA sans spec                                                                  | Retours génériques                                                                                       |
| Qwen seul sur code critique                                                          | Risque qualité                                                                                           |
| Claude sur boilerplate trivial                                                       | Gaspillage quota                                                                                         |
| Compression agressive du code source                                                 | Perte de détails critiques                                                                               |
| Pas de tests ciblés                                                                  | L'agent s'auto-convainc                                                                                  |
| Ignorer IntelliJ                                                                     | Grave erreur sur Scala/JVM                                                                               |
| Fable 5.2, GPT‑6.2 Astra `max` ou `ultra` sur tâche simple                             | Coût, latence et quota consommés pour zéro gain réel                                                     |
| Opus 5.5 High/Extra par défaut sur toute tâche                                       | Opus Medium ou Sonnet 5.5 Medium suffisent souvent ; l’effort haut doit acheter un gain mesuré           |
| Lancer Fable 5.2 sans spec complète                                                  | Modèle fort + prompt flou = dérive coûteuse                                                              |
| Sol/Astra à effort élevé pour PR summary                                             | GPT‑6 Luna suffit                                                                                        |
| Deux agents en écriture sur les mêmes fichiers                                       | Conflits, diffs incohérents, responsabilité floue                                                        |
| Qwen3-Coder-Next arbitre final sur code critique                                     | Très utile économiquement, mais pas assez sûr sans review forte                                          |
| Traiter une issue, un README, un log ou un résultat MCP comme une instruction fiable | Injection indirecte et élargissement de permissions                                                      |
| Donner à un reviewer tout le transcript d'une longue session agentique               | Context rot : bruit historique, contraintes noyées, moins bonne détection des défauts                    |
| Ré-injecter la charte seulement au premier prompt                                    | La dérive longue est mesurée ; le ré-ancrage périodique est la parade (section 5, étape 8)               |
| Bâtir un workflow sur un quota gratuit                                               | Les quotas gratuits disparaissent sans préavis (Gemini CLI, juin 2026) ; router sur des surfaces stables |

---

# 17. Version finale du workflow

Pour une vraie tâche métier Scala :

```text
1. Humain : spec, exigences → preuves, risque, non-objectifs, mode de contrôle ; WIP ≤ 2 stories indépendantes au départ
2. Sourcebot + ScalaSemantic + IntelliJ/Metals : contexte pertinent ; Codebase-Memory si polyglotte
3. Worker économique pour extraction vérifiable ; même modèle que parent pour jugement complexe
4. Writer : GPT‑6.2 Sol Medium ou Opus 5.5 Medium ; High / Astra / Fable seulement si justifié
5. Writer : plan sans modification ; worktree et permissions propres à la tâche
6. Humain : validation du plan ; sur code critique, autre agent prépare les tests et humain valide l'oracle
7. Writer : petit diff et tests ciblés ; reproduction rouge avant bugfix
8. IntelliJ / scripts : compile, format, suites réellement exécutées et preuve structurée
9. Writer : self-review du diff complet
10. Autre famille : review indépendante read-only sur le SHA exact, findings étayés
11. Humain : triage des retours
12. Writer ou steward explicitement désigné : corrections ciblées, sans concurrence d'écriture
13. CI indépendante : checks et preuves sur le candidat final
14. Codex Goal / Heartbeat / Cloud ou Claude /steward / Cloud Auto-fix : suivi borné si utile ; revalider après chaque push
15. Luna/Qwen : résumé PR ; humain : merge après validation du SHA final et gates d'intégration
16. Pipeline dédié : artefact immuable, staging, release approuvée, canary et rollback selon risque
17. Runtime : vérifier SLO et invariants ; déclarer stable après la fenêtre d'observation
```

Le résumé le plus important :

```text
Plan fort.
Diff court.
Preuves déterministes sur le bon SHA.
Review indépendante proportionnée au risque.
Validation humaine et permissions isolées.
Déploiement contrôlé, observabilité et rollback.
Modèle cher seulement quand l’erreur coûterait cher.
```

## Sources principales consultées

* TypeSafe AI — Introducing System One Models & Jev : architecture, RLCD, décisions typées et positionnement « smart
  if » :
  https://typesafe.ai/blog/introducing-system-one-models-and-jev
* TypeSafe AI — Models : Jev 1.14, prix, limites, contexte, aliases et version pinning :
  https://docs.typesafe.ai/models
* TypeSafe AI — Confidence : distributions, confidence et seuils proportionnés au risque :
  https://docs.typesafe.ai/confidence
* TypeSafe AI — Jev 1.13 jaggedness : calcul, dates, indirection, context rot, contenu adversarial et ordre des
  options :
  https://docs.typesafe.ai/model-jaggedness/jev-1.13
* Deußer, Sparrenberg, Sifa — « Evaluating and Benchmarking the System One Model Jev », arXiv:2609.37647 :
  https://arxiv.org/abs/2609.37647
* Silicon Carnet — « Jev : pourquoi toute la Silicon Valley s'emballe ! » : retours d'usage sur model routing, skill
  selection, compaction et validation fatigue :
  https://www.youtube.com/watch?v=0P6lU9WYBpE
* OpenAI API — Ultrafast : service tier Astra, WebSocket recommandé, disponibilité et résidence des données :
  https://developers.openai.com/api/docs/guides/ultrafast-mode
* OpenAI API — pricing Ultrafast :
  https://developers.openai.com/api/docs/pricing?latest-pricing=ultrafast
* OpenAI Help — Pro 500 et Astra Ultrafast ; Codex Cloud :
  https://help.openai.com/en/articles/6825453-chatgpt-release-notes
* OpenAI — Codex Cloud environments réutilisables :
  https://learn.chatgpt.com/docs/environments/cloud-environments
* OpenAI API — Agents API computer use dans un navigateur hébergé :
  https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use
* OpenAI Codex — releases 0.158–0.159 : MCP OAuth client secret, exec-server auth et `instant_interrupt` :
  https://github.com/openai/codex/releases
* Anthropic — Sonnet 5.5, breaking changes et `between_tools` :
  https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5
* Anthropic — migration Opus 5.5 : adaptive thinking, effort, tools, prefill, computer use et cache :
  https://platform.claude.com/docs/en/models/opus-5-5/migration-guide
* METR — predeployment evaluation de Claude Opus 5.5 vs Fable 5.1 :
  https://metr.org/blog/2026-09-22-claude-opus-5-5/
* Anthropic — Claude Code power-user tips : `--bare` pour SDK/CI :
  https://support.claude.com/en/articles/14554000-claude-code-power-user-tips
* Anthropic Claude Code — release 2.1.283 : `/doctor prompt-audit` ; 2.1.286 : durcissement de `--bare` :
  https://github.com/anthropics/claude-code/releases
* Qwen Code — release 0.24.7 : lazy loading des deferred tools, structured recall et durable workspaces :
  https://github.com/QwenLM/qwen-code/releases/tag/v0.24.7
* Qwen Code — Resident Context Cost et `tools.eager` :
  https://qwenlm.github.io/qwen-code-docs/en/users/features/context-cost/
* OpenAI — MCP Events, extension draft au-dessus de MCP 2026-07-28 :
  https://developers.openai.com/plugins/build/mcp-events
* OpenAI Help — droits MCP ChatGPT et limites Pro :
  https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
* OpenAI Developers — page généraliste ChatGPT indiquant full MCP read/write pour Plus/Pro (contradiction documentaire
  constatée au 1er octobre 2026) : https://developers.openai.com/chatgpt
* OpenAI — GPT‑6 Astra : annonce, disponibilité, benchmarks coding/computer use, alignement et comparaison Fable 5.1 :
  https://openai.com/index/gpt-6-astra/
* OpenAI API — GPT‑6 Astra : contexte 1.05M, sortie 128K, cutoff, pricing, cache et surcharge >272K :
  https://developers.openai.com/api/docs/models/gpt-6-astra
* OpenAI API — Model guidance Astra : async tool calling, mid-turn steering, effort et prompt caching :
  https://developers.openai.com/api/docs/guides/latest-model
* OpenAI — Safety overview / System Card Astra : niveau cyber Critical, monitoring et restrictions :
  https://openai.com/index/safety-overview-gpt-6-astra/
* Artificial Analysis — GPT‑6 Astra : Coding Agent Index, token efficiency et coût par tâche :
  https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra
* Artificial Analysis — Claude Code Fable 5.1 vs Codex GPT‑6 Astra :
  https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex
* OpenAI — modèles ChatGPT Work / Codex et recommandations GPT‑6.1 Sol, GPT‑6 Luna, Astra, efforts et Ultra :
  https://learn.chatgpt.com/docs/models?surface=app
* OpenAI API — GPT‑6.1 Sol : rôle, tools, contexte, effort et pricing :
  https://developers.openai.com/api/docs/models/gpt-6.1-sol
* OpenAI — GPT‑6.2, disponibilité et positionnement Sol/Astra : https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol
* OpenAI — GPT‑6.2 Sol et Astra (spécifications API et prix) :
  https://developers.openai.com/api/docs/models/gpt-6.2-sol
  https://developers.openai.com/api/docs/models/gpt-6.2-astra
* OpenAI — choix de modèles et subagents : https://learn.chatgpt.com/docs/model-selection
  https://learn.chatgpt.com/docs/agent-configuration/subagents
* OpenAI — prompting GPT‑6.2 dans Codex : https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra
* OpenAI API — GPT‑6 Luna : https://developers.openai.com/api/docs/models/gpt-6-luna
* Anthropic — Choosing the right model : Opus 5.5 par défaut, Sonnet 5.5, Haiku 4.5 et escalade Fable 5.1 :
  https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
* Anthropic — Effort : Low/Medium/High/xhigh/Max et recommandations par modèle :
  https://platform.claude.com/docs/en/build-with-claude/effort
* Anthropic — Optimizing for cost and intelligence : coût par tâche résolue, retry à effort supérieur et advisor
  strategy :
  https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence
* OpenAI — GPT‑5.6 : disponibilité générale, Sol/Terra/Luna, prix, Max, Ultra, évaluations :
  https://openai.com/index/gpt-5-6/
* OpenAI API — GPT‑5.6 Sol : contexte, modalities, prix et seuil long contexte :
  https://developers.openai.com/api/docs/models/gpt-5.6-sol
* OpenAI API — GPT‑5.6 Terra : https://developers.openai.com/api/docs/models/gpt-5.6-terra
* OpenAI API — GPT‑5.6 Luna : https://developers.openai.com/api/docs/models/gpt-5.6-luna
* OpenAI API — guide de migration et réglages GPT‑5.6 (`max`, `pro`, contexte persistant) :
  https://developers.openai.com/api/docs/guides/latest-model
* OpenAI API — modèles de raisonnement : https://developers.openai.com/api/docs/guides/reasoning
* OpenAI API — Structured Outputs : https://developers.openai.com/api/docs/guides/structured-outputs
* OpenAI API — Multi-agent beta : https://developers.openai.com/api/docs/guides/tools-multi-agent
* OpenAI — GPT‑5.6 System Card : https://deploymentsafety.openai.com/gpt-5-6
* OpenAI — ChatGPT Work et fusion de Codex dans ChatGPT Desktop :
  https://openai.com/index/chatgpt-for-your-most-ambitious-work/
* OpenAI — modèles dans ChatGPT Work et Codex : https://developers.openai.com/codex/models
* OpenAI — ChatGPT Desktop (Chat / Work / Codex) : https://developers.openai.com/codex/app
* Anthropic — Claude Fable 5.1 : overview, spécifications, disponibilité, prix et changements de migration :
  https://platform.claude.com/docs/en/models/fable-5-1/overview
* Anthropic — migration Fable 5 → Fable 5.1 : forced tool use, thinking blocks et compatibilité d'historique :
  https://platform.claude.com/docs/fr/models/fable-5-1/migration-guide
* Anthropic — prompting Fable 5.1 : effort, progress updates, long-horizon et comportement agentique :
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
* Anthropic — API et conservation des données : Fable 5.1 exige 30 jours de rétention, ZDR seulement sur autorisation
  expresse :
  https://platform.claude.com/docs/fr/manage-claude/api-and-data-retention
* Anthropic — Redeploying Claude Fable 5 (chronologie export controls, restauration du 1er juillet, promo 50% des
  limites hebdo) : https://www.anthropic.com/news/redeploying-fable-5
* Anthropic (@claudeai sur X, 7 et 13 juillet 2026) — extensions successives de l'accès Fable 5 et des limites Claude
  Code +50% sur les plans payants, jusqu'au 12 puis au 19 juillet 2026
* Anthropic — More details on Fable 5's cyber safeguards and our jailbreak framework (2 juillet 2026) :
  https://www.anthropic.com/news
* Anthropic Claude Code, coûts et gestion du contexte : https://docs.anthropic.com/en/docs/claude-code/costs
* Anthropic prompt caching : https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
* Anthropic Claude Code memory : https://docs.anthropic.com/en/docs/claude-code/memory
* Anthropic — découverte CLAUDE.md / AGENTS.md et fallback : https://code.claude.com/docs/en/memory
* Anthropic — Claude Code Cloud, Auto-fix et événements GitHub : https://code.claude.com/docs/en/claude-code-on-the-web
* Best practices for Claude Code : https://code.claude.com/docs/en/best-practices
* Anthropic commercial terms, usage Claude subscriptions/API : https://www.anthropic.com/legal/commercial-terms
* OpenAI Codex pricing / rate card : https://openai.com/api/pricing/
* OpenAI Codex / AGENTS.md : https://github.com/openai/codex
* OpenAI — découverte des instructions et hooks Codex (trust, événements, formats) :
  https://learn.chatgpt.com/docs/agent-configuration/agents-md
  https://learn.chatgpt.com/docs/hooks
* OpenAI — Harness Engineering : https://openai.com/index/harness-engineering/
* OpenAI Codex — releases CLI, agents, queue, plugins et durcissements : https://github.com/openai/codex/releases
* OpenAI — Codex Code Review, Security Review, déclencheurs GitHub et corrections à la demande :
  https://learn.chatgpt.com/docs/third-party/github
* OpenAI — Custom Code Review rules for Codex :
  https://developers.openai.com/blog/custom-code-review-rules-for-codex
* OpenAI — Goal mode : objectif, critères de complétion, surfaces et contrôles :
  https://learn.chatgpt.com/docs/long-running-work
* OpenAI — Developer commands : syntaxe et contrôles de `/goal` :
  https://learn.chatgpt.com/docs/developer-commands
* OpenAI — Scheduled tasks : suivis dans un chat (Heartbeats), worktrees, permissions et déclencheurs GitHub :
  https://learn.chatgpt.com/docs/automations
* OpenAI — Codex GitHub Action, paramètres et sécurité : https://learn.chatgpt.com/docs/github-action
* OpenAI — Autofix CI, séparation génération/publication :
  https://developers.openai.com/cookbook/examples/codex/autofix-github-actions
* OpenAI — limites d'usage et Code Review : https://learn.chatgpt.com/docs/pricing
* RuntimeWire — observation des réglages desktop Watch and Fix (source tierce, disponibilité non confirmée) :
  https://runtimewire.com/article/openai-gives-codex-a-watch-and-fix-mode-that-keeps-repairing-your-pull-request
* JetBrains IntelliJ IDEA 2025.2 MCP Server : https://blog.jetbrains.com/idea/2025/07/intellij-idea-2025-2/
* JetBrains Codex integration : https://blog.jetbrains.com/ai/2026/01/codex-in-jetbrains-ides/
* JetBrains AI Assistant 2026.2 — Agent Client Protocol (ACP) : https://www.jetbrains.com/help/ai-assistant/acp.html
* JetBrains — agents ACP dans IntelliJ
  IDEA : https://blog.jetbrains.com/fr/idea/2026/08/comment-utiliser-des-agents-d-ia-avec-l-acp-dans-intellij-idea/
* JetBrains — consommation AI Credits : https://www.jetbrains.com/help/jetbrains-console/ai-credits-consumption.html
* JetBrains AI — plans et 35 AI Credits Ultimate : https://www.jetbrains.com/ai-ides/buy/
* Anthropic — Claude Code JetBrains : https://code.claude.com/docs/en/jetbrains
* Anthropic — Claude Code Desktop : https://code.claude.com/docs/en/desktop
* Anthropic — Introducing Claude Ship : séparation review/correction/approbation, accès et facturation :
  https://claude.com/resources/articles/introducing-claude-ship
* Anthropic — Claude Ship : configuration par dépôt, limites, ordre de désactivation et facturation :
  https://code.claude.com/docs/en/claude-ship
* Anthropic — Code Review : niveaux, findings, instructions et limites de la review statique :
  https://code.claude.com/docs/en/code-review
* Anthropic — PR Steward : déclencheurs, corrections, commandes d'arrêt et coût :
  https://code.claude.com/docs/en/pr-steward
* Anthropic — Claude Approvals : politique, observe mode, interactions avec Code Review et protections GitHub :
  https://code.claude.com/docs/en/approvals
* Anthropic — `/ship` et `/steward` : référence des commandes (lien depuis la documentation Claude Ship) :
  https://code.claude.com/docs/en/ship-command
* ClaudeFox — Claude Ship : synthèse de la documentation des commandes locales et des risques opérationnels :
  https://claudefox.com/claude-ship-ship-command-approvals/
* GitHub — About protected branches : required checks, CODEOWNERS et invalidation des approbations :
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
* GitHub — Copilot Code Review : https://docs.github.com/en/copilot/concepts/agents/code-review
* GitHub — gérer issues et PR avec Copilot
  app : https://docs.github.com/en/copilot/how-tos/github-copilot-app/managing-issues-and-pull-requests
* GitHub — demander une review
  Copilot : https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review
* JetBrains Junie CLI : https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/
* JetBrains Skill Manager : https://blog.jetbrains.com/ai/2026/04/skill-manager-and-skill-repository/
* Metals 1.5.3 MCP support : https://scalameta.org/metals/blog/2025/05/13/strontium/
* Metals — MCP Server : https://scalameta.org/metals/docs/features/mcp/
* Metals 1.6.6 « Osmium » standalone MCP / Twirl : https://scalameta.org/metals/blog/2026/03/03/osmium/
* sbt 2.0.0 stable (14 juin 2026) : https://www.scala-lang.org/blog/2026/06/29/sbt2.html
* sbt 2.0.1 (29 juin 2026, référence historique) : https://eed3si9n.com/sbt-2.0.1
* sbt — avis critique BSP/TCP et versions corrigées 1.13.0 / 2.0.7 :
  https://github.com/sbt/sbt/security/advisories/GHSA-943m-f264-54p4
* sbt 2.0.7 : https://github.com/sbt/sbt/releases/tag/v2.0.7
* sbt 1.9.0, IntegrationTest déprécié : https://github.com/sbt/sbt/releases/tag/v1.9.0
* sbt 1.4, client natif et `sbt --client` : https://www.scala-sbt.org/1.x/docs/sbt-1.4-Release-Notes.html
* Stryker4s documentation : https://stryker-mutator.io/docs/stryker4s/getting-started/
* Sourcebot : https://sourcebot.dev/
* ScalaSemantic — MCP Scala alimenté par SemanticDB, outils sémantiques, call paths, hiérarchies et implicits :
  https://mercurievv.github.io/ScalaSemantic/
* ScalaSemantic — référence des outils MCP :
  https://mercurievv.github.io/ScalaSemantic/reference/tools/
* Codebase-Memory MCP — knowledge graph persistant Tree-sitter + Hybrid LSP, Java/Kotlin et topologie cross-service :
  https://github.com/DeusData/codebase-memory-mcp
* agent4s — toolbox MCP Scala, Scalameta et SemanticDB optionnel :
  https://github.com/scala-digest/agent4s
* Joern — Code Property Graph et frontends supportés :
  https://docs.joern.io/
* Context7 : https://context7.com/
* OpenCode documentation : https://opencode.ai/docs/
* Aider documentation : https://aider.chat/docs/
* Qwen3-Coder-Next — dépôt officiel : https://github.com/QwenLM/Qwen3-Coder
* Qwen Code : https://qwenlm.github.io/qwen-code-docs/
* Alibaba Cloud Model Studio — catalogue Qwen3.8 et tarifs
  régionaux : https://www.alibabacloud.com/help/en/model-studio/models
* Apple MacBook Pro M5 Max technical specs : https://www.apple.com/macbook-pro/specs/
* OpenRouter model fallbacks : https://openrouter.ai/docs/guides/routing/model-fallbacks
* OpenRouter quickstart : https://openrouter.ai/docs/quickstart
* Anthropic Claude Code — Mods overview : architecture in-process, capacités, surfaces, built-ins et comparaison
  Mods/hooks/skills/MCP :
  https://code.claude.com/docs/en/plugins/mods/overview
* Anthropic Claude Code — Mods reference : événements, Mods API, limites et managed settings :
  https://code.claude.com/docs/en/plugins/mods/reference
* Anthropic Claude Code — Plugin security and trust : privilèges, sandbox, revue et mises à jour :
  https://code.claude.com/docs/en/plugins/security
* Anthropic Claude Code — Test a mod : `claude plugin test`, stubs et tests sans réseau/session :
  https://code.claude.com/docs/en/plugins/mods/test
* Anthropic Claude Code — source des Mods intégrés (`diff`, `agents-md`, `sec-default`, `telemetry`) :
  https://github.com/anthropics/claude-code/tree/main/mods
* Anthropic Claude Code — changelog v2.1.287 : introduction publique de Claude Mods et de `You should know` :
  https://github.com/anthropics/claude-code/releases/tag/v2.1.287
* Anthropic Claude Code — v2.1.288 : `$.ui.selection()` et correctifs Mods/plugins :
  https://github.com/anthropics/claude-code/releases/tag/v2.1.288
* Claude Code subagents : https://code.claude.com/docs/en/sub-agents
* Claude Code permissions : https://code.claude.com/docs/en/permissions
* Claude Code common workflows / worktrees : https://code.claude.com/docs/en/common-workflows
* Claude Code hooks : https://code.claude.com/docs/en/hooks
* LangChain router pattern : https://docs.langchain.com/oss/python/langchain/multi-agent/router
* LangChain multi-source routing
  pattern : https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base
* "Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems", arXiv
  2026 : https://arxiv.org/abs/2604.14228
* "Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode", arXiv
  2026 : https://arxiv.org/abs/2604.04978
* "RCR-Router: Efficient Role-Aware Context Routing for Multi-Agent LLM Systems with Structured Memory", arXiv
  2025 : https://arxiv.org/abs/2508.04903
* METR — écart entre PRs SWE-bench passantes et changements réellement mergeables :
  https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
* “SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks”, arXiv 2026 :
  https://arxiv.org/abs/2603.24755
* “Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents”, arXiv 2026 :
  https://arxiv.org/abs/2602.07900
* “SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?”, arXiv 2026 :
  https://arxiv.org/abs/2605.22175
* “Evaluating LLM-Based Test Generation Under Software Evolution”, arXiv 2026 :
  https://arxiv.org/abs/2603.23443
* “Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and
  GitHub Copilot CLI”, arXiv 2026 : https://arxiv.org/abs/2607.01418
* MCP — spécification finale 2026-07-28 : https://blog.modelcontextprotocol.io/posts/2026-07-28/
* Claude Managed Agents — Outcomes, orchestration multi-agent, webhooks, Dreaming (Code with Claude, 6 mai 2026) :
  https://www.anthropic.com/news
* Claude Fable 5 et Mythos 5 — annonce officielle historique Anthropic (9 juin
    2026) : https://www.anthropic.com/news/claude-fable-5-mythos-5
* Claude Fable 5 — page produit : https://www.anthropic.com/claude/fable
* Claude Fable 5 — API
  docs : https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
* Claude Fable 5 —
  prompting : https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
* Claude models overview : https://platform.claude.com/docs/en/about-claude/models/overview
* Claude Sonnet 5 — annonce officielle Anthropic (30 juin 2026) : https://www.anthropic.com/news/claude-sonnet-5
* Claude Sonnet 5 — What's new (tokenizer, adaptive thinking, erreurs
    400) : https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5
* Claude Sonnet 5 — System Card : https://www.anthropic.com/claude-sonnet-5-system-card
* Claude Opus 5 — repère historique ; modèle courant : Opus
  5.5 : https://platform.claude.com/docs/en/about-claude/models/overview
* Claude Opus 4.8 — annonce officielle Anthropic (référence historique) : https://www.anthropic.com/news/claude-opus-4-8
* GPT‑5.5 — annonce officielle OpenAI (23 avril 2026, référence
  historique) : https://openai.com/index/introducing-gpt-5-5/
* GPT‑5.5 in ChatGPT (Instant / Thinking / Pro / Thinking time, référence
  historique) : https://help.openai.com/en/articles/11909943
* OpenAI Model Release Notes : https://help.openai.com/en/articles/9624314-model-release-notes
* GPT-5.3-Codex — annonce officielle OpenAI : https://openai.com/index/introducing-gpt-5-3-codex/
* Qwen3-Coder-Next — annonce Alibaba
  Cloud : https://www.alibabacloud.com/blog/qwen3-coder-next-pushing-small-hybrid-models-on-agentic-coding_602864
* Qwen-Coder model capabilities : https://www.alibabacloud.com/help/en/model-studio/qwen-coder
* Alibaba Cloud Model Studio — modèles et tarifs : https://www.alibabacloud.com/help/en/model-studio/models
* Kimi K3 — quickstart et doc API Moonshot (specs, pricing, reasoning_effort, déploiement) :
  https://platform.kimi.ai/docs/guide/kimi-k3-quickstart
* Kimi K3 — page modèle et pricing OpenRouter (`moonshotai/kimi-k3`) : https://openrouter.ai/moonshotai/kimi-k3
* Kimi K3 — analyse indépendante (Artificial Analysis, harness, DeepSWE) :
  https://trilogyai.substack.com/p/kimi-k3-is-live-pricing-benchmarks
* Kimi K3 — annonce et positionnement (VentureBeat) :
  https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems
* GLM‑5.2 — Z.ai API developer guide (endpoints OpenAI/Anthropic-compatibles, setup Claude Code) :
  https://baeseokjae.github.io/posts/z-ai-api-developer-guide-2026/
* GLM‑5.2 — specs, benchmarks et pricing (The AI Rankings) : https://theairankings.com/zhipu/glm-5/
* GLM Coding Plan — tiers et quotas (Lite/Pro/Max, mis à jour 2026-07-20) :
  https://www.aipricing.guru/z-ai-subscription-pricing/
* Landscape open-weight coding mi-2026 (GLM‑5.2, MiniMax M3, Kimi, DeepSeek V4, Qwen3-Coder-Next) :
  https://kilo.ai/open-source-models
* Qwen3-Coder — famille officielle et pointage juillet 2026 (Qwen3-Coder-Next reste la ligne locale) :
  https://github.com/QwenLM/Qwen3-Coder
* Anthropic — chronologie d'accès Fable 5 jusqu'au 19 juillet, bascule crédits au 20 juillet :
  https://www.anthropic.com/news/redeploying-fable-5
* Kimi — Kimi K3 Tech Blog : architecture, benchmarks et limites :
  https://www.kimi.com/fr-fr/blog/kimi-k3
* Moonshot AI / Hugging Face — Kimi K3 : poids complets, architecture, paramètres actifs, contexte et licence :
  https://huggingface.co/moonshotai/Kimi-K3
* Kimi Code — configuration actuelle de K3 : efforts low/high/max, défaut high, contexte selon le plan :
  https://www.kimi.com/code/docs/en/kimi-code/models.html
* Kimi Code — historique de raisonnement et correctifs de sécurité du CLI :
  https://www.kimi.com/code/docs/en/kimi-code/whats-new.html
* Z.ai — GLM‑5.2 : architecture, efforts, benchmarks et contexte 1M : https://z.ai/blog/glm-5.2
* Z.ai / Hugging Face — checkpoint GLM‑5.2, 753B paramètres, licence MIT : https://huggingface.co/zai-org/GLM-5.2
* Z.ai — tarification API officielle GLM‑5.2 : https://docs.z.ai/guides/overview/pricing
* Qwen / Hugging Face — Qwen3-Coder-Next et GGUF officiels, Q4_K_M 48,4 Go, Q8_0 84,8 Go :
  https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF
* Qwen3-Coder-Next — dépôt officiel et rapport technique, 80B total, 3B activés, architecture hybride :
  https://github.com/QwenLM/Qwen3-Coder
* MLX Community — conversions Qwen3-Coder-Next 4-bit et 8-bit pour Apple Silicon :
  https://huggingface.co/mlx-community/Qwen3-Coder-Next-4bit
  https://huggingface.co/mlx-community/Qwen3-Coder-Next-8bit
* llama.cpp — retour de performance Qwen3-Coder-Next sur Apple Silicon, à reproduire selon la version :
  https://github.com/ggml-org/llama.cpp/issues/19366
* llama.cpp — mémoire câblée et slots longs sur Qwen3-Next 80B Q8 avec une machine 128 Go :
  https://github.com/ggml-org/llama.cpp/discussions/22064
* JetBrains — Junie sort de beta en juin 2026 :
  https://blog.jetbrains.com/junie/2026/06/junie-coding-agent-out-of-beta/
* OpenAI — audit de SWE-bench Pro, environ 30 % de tâches défectueuses :
  https://openai.com/index/separating-signal-from-noise-coding-evaluations/
* METR — mise à jour de l'étude de productivité et limites du nouvel essai :
  https://metr.org/blog/2026-02-24-uplift-update/
* DeepSWE — tâches originales longues et vérificateurs dédiés : https://arxiv.org/abs/2607.07946
* SWE-Interact — sessions interactives, exigences progressives et chute single-turn → multi-turn :
  https://arxiv.org/abs/2606.30573
* SWE-Explore — localisation et efficacité du contexte : https://arxiv.org/abs/2606.07297
* SWE-Cycle — cycle complet environnement, implémentation et tests : https://arxiv.org/abs/2605.13139
* Evaluating AGENTS.md — effet mixte des fichiers de contexte et surcoût supérieur à 20 % :
  https://arxiv.org/abs/2602.11988
* Effective Strategies for Asynchronous Software Engineering Agents — CAID, worktrees et branch-and-merge :
  https://arxiv.org/abs/2603.21489
* Architecting Secure AI Agents — défenses système contre l'injection indirecte :
  https://arxiv.org/abs/2603.30016
* Understanding the (In)Security of Vibe-Coded Applications — défauts récurrents observés :
  https://arxiv.org/abs/2606.23130
* Context Rot — dégradation de qualité à mesure que le contexte grossit, indépendamment de la limite physique de la
  fenêtre : https://arxiv.org/pdf/2510.26493
* Tokalator — toolkit de context engineering pour agents de code, seuils de « rot » et isolation par sous-agent :
  https://arxiv.org/pdf/2604.08290
* Chroma Research — Context Rot, évaluations contrôlées où la tâche reste identique tandis que la longueur du contexte
  augmente :
  https://www.trychroma.com/research/context-rot
* Anthropic — Effective context engineering for AI agents, contexte comme ressource à rendements décroissants :
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
* Anthropic Claude Code — subagents et fenêtres de contexte isolées :
  https://code.claude.com/docs/en/sub-agents
* Cloud Security Alliance — « Slopsquatting: AI Code Hallucinations Fuel Supply Chain Attacks » (avril 2026) :
  https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/04/CSA_research_note_slopsquatting-ai-supply-chain_20260419-csa-styled-1.pdf
* Revue systématique PRISMA — hallucination de paquets et slopsquatting (nov. 2025 ; 5,2 % modèles frontier vs 21,7 %
  open-weight) : https://sciety.org/articles/activity/10.21203/rs.3.rs-8007192/v1
* Cloud Security Alliance — sécurité du code généré et vibe coding (CWE-330/94/79 ; scan Escape.tech de 1 400+
  applications) : https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-generated-code-security-vibe-coding-202/
* DORA / Google Cloud — Impact of Generative AI in Software Development (débit −1,5 %, stabilité −7,2 % par +25 %
  d'adoption) : https://dora.dev/ai/gen-ai-report/
* Anthropic — Effective context engineering for AI agents (29 sept. 2025) :
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
* LangChain — taxonomie du context engineering (Write / Select / Compress / Isolate) :
  https://blog.langchain.com/context-engineering-for-agents/
* Claude Code — Checkpointing (checkpoints, /rewind, limites) : https://code.claude.com/docs/en/checkpointing
* JetBrains — What's New in IntelliJ IDEA 2026.1 (Codex, Cursor et agents ACP intégrés) :
  https://www.jetbrains.com/idea/whatsnew/2026-1/
* JetBrains — Agentic debugging via le serveur MCP (outils `xdebug_`) :
  https://www.jetbrains.com/help/idea/agentic-debugging.html
* MCP — roadmap août 2026, dont progressive discovery des catalogues d'outils :
  https://www.developersdigest.tech/blog/mcp-roadmap-progressive-discovery-agent-auth
* Simon Willison — « Thinking about vibe coding » (frontière relecture/vibe coding, février 2025) :
  https://simonwillison.net/2025/Feb/12/thinking-about-vibe-coding/
* Steve Yegge — « Vibe Engineering » (septembre 2025), définition et synthèse :
  https://aiwiki.ai/wiki/vibe_engineering
* LinearB — Software Engineering Benchmarks Report (8,1 M+ PRs, 4 800+ organisations ; pickup, merge sous 30 jours,
  distinctions PRs assistées, agentiques et non assistées) :
  https://linearb.io/resources/software-engineering-benchmarks-report
* LinearB — données et définitions des métriques IA :
  https://linearb.io/library/engineering-benchmarks-and-research
* DORA / Google Cloud — The ROI of AI-assisted Software Development (avril 2026 ; IA comme amplificateur, +98 % de PRs
  mergées, temps médian en review multiplié par ~4,4) : https://dora.dev/ai/roi/report/
* Opsera — AI Coding Impact Benchmark Report (250 000+ développeurs, 60+ entreprises) :
  https://opsera.ai/resources/report/ai-coding-impact-2026-benchmark-report
* Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems, arXiv 2026 (consolidation épisodique,
  ancrage comportemental adaptatif, routage drift-aware) : https://arxiv.org/abs/2601.04170
* Thoughtworks — Architecture drift reduction with LLMs (Technology Radar, avril 2026 ; fitness functions, ArchUnit) :
  https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms
* JetBrains Research — compression de contexte des agents de code (masquage d'observation vs résumé LLM, SWE-bench
  Verified), synthèse : https://zylos.ai/research/2026-06-20-context-engineering-long-running-agents/
* OpenAI — coupure Sol du 21 août 2026 ($4/$20, promotionnel au moins jusqu'au 21 novembre 2026) :
  https://community.openai.com/t/20-price-reduction-for-gpt-5-6-sol-api-codex-credits-and-chatgpt-work/1391726
* Amazon Bedrock — confirmation multi-provider de la réduction GPT‑5.6 Sol (21 août 2026) :
  https://aws.amazon.com/about-aws/whats-new/2026/08/bedrock-openai-gpt-56-sol-reduced-pricing/
* Google — fermeture de l'accès gratuit Gemini CLI (18 juin 2026) et successeur Antigravity CLI :
  https://codegen.com/ai-tools/gemini-cli/
* Comparatif SDD 2026 (Spec Kit greenfield / OpenSpec brownfield / Kiro EARS ; paysage 30+ frameworks) :
  https://levelop.dev/blog/spec-driven-development-tools-compared
* OpenAI — Agents API, beta publique : sessions durables, harness Codex géré, recovery, MCP et subagents :
  https://openai.com/index/introducing-the-agents-api/
* OpenAI API — Programmatic tool calling et orchestration d'outils :
  https://developers.openai.com/fr-FR/api/docs/guides/tools-programmatic-tool-calling
* OpenAI — MCP pour ChatGPT/Codex : STDIO, Streamable HTTP, OAuth, CIMD/DCR et configuration partagée :
  https://developers.openai.com/fr-FR/docs/extend/mcp
* OpenAI — suppression de `codex mcp-server` et migration vers Codex App Server non-MCP :
  https://developers.openai.com/fr-FR/docs/mcp-server
* OpenAI Help — Developer mode et apps MCP dans ChatGPT : droits read/write, plans et snapshot approuvé des outils :
  https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
* OpenAI API — Secure MCP Tunnel pour les serveurs locaux, privés ou on-premise :
  https://developers.openai.com/fr-FR/api/docs/guides/secure-mcp-tunnels
* Anthropic — Claude Code releases 2.1.269–2.1.278 : AGENTS.md fallback, `allowed_domains`, `omitClaudeMd`,
  `claude plugin eval`, Auto mode server et correctifs MCP :
  https://github.com/anthropics/claude-code/releases
* Qwen Code — releases 0.23.x–0.24.x : métriques de contexte, allowlists d'outils, workflows persistés et sandbox :
  https://github.com/QwenLM/qwen-code/releases
* Alibaba Cloud Model Studio — Qwen3.8-Omni-Flash : modalités, contexte, tool calling et disponibilité :
  https://www.alibabacloud.com/help/en/model-studio/qwen3-8-omni-flash
* GitHub — migration du runtime Copilot vers Rust avec des agents : worktrees, subagents, prompt caching, compaction et
  protection des oracles :
  https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/
* “Spec-Driven Development for Agentic Software Engineering: Harnessing Human-Agent Teamwork”, arXiv 2026 :
  https://arxiv.org/abs/2609.00252
* Anthropic, Claude Fable 5.2 : overview, IDs, spécifications, prix, rétention et disponibilité :
  https://platform.claude.com/docs/en/models/fable-5-2/overview
* Anthropic, What's new in Claude Fable 5.2 : breaking changes, compatibilité des thinking blocks, betas, comportements :
  https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2
* Anthropic, guide de migration Fable 5.2 (depuis Fable 5.1, Opus 5.5, Fable 5, Opus 5 et Opus 4.8) :
  https://platform.claude.com/docs/en/models/fable-5-2/migration-guide
* Anthropic, prompting Claude Fable 5.2 : effort, fins de tour, propriété du code, sur-délégation, instructions héritées :
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
* Anthropic, page produit Claude Fable 5.2 : https://www.anthropic.com/claude/fable
* Anthropic (@claudeai sur X, 9 novembre 2026), annonce Fable 5.2 / Mythos 5.2 ; FrontierCode 2.0 `high` au niveau
  d'Opus 5.5 `max` pour environ la moitié du coût : https://x.com/claudeai/status/2119867114450268322
* CNBC, sortie de Fable 5.2 et Mythos 5.2, génération ~30 % plus rapide (9 novembre 2026) :
  https://www.cnbc.com/2026/11/09/anthropic-claude-fable-5-2-mythos-5-2.html
* DataCamp, tableau des benchmarks éditeur Fable 5.2 / Fable 5.1 / Opus 5.5 / GPT‑6 Astra / Gemini 4 Carbon :
  https://www.datacamp.com/blog/claude-fable-5-2-and-mythos-5-2
* LLM Stats, benchmarks Fable 5.2 (SWE-bench Pro, Terminal-Bench 4.0 et marges d'erreur) :
  https://llm-stats.com/blog/research/claude-fable-5-2-launch
* Vals AI, évaluation indépendante de Claude Fable 5.2 : https://www.vals.ai/models/anthropic_claude-fable-5-2
* Anthropic, Choosing the right model (Opus 5.5 par défaut, escalade Fable 5.2, Haiku 5.5) :
  https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
* Anthropic, Pricing (cache read par modèle, palier Haiku 5.5, batch, fast mode, `inference_geo`) :
  https://platform.claude.com/docs/en/about-claude/pricing
* Anthropic, Claude Haiku 5.5 : overview et tarifs par palier : https://platform.claude.com/docs/en/models/haiku-5-5/overview
* Anthropic, migration Haiku 4.5 → Haiku 5.5 : https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide
* Anthropic, Model deprecations : https://platform.claude.com/docs/en/about-claude/model-deprecations
* Anthropic Help Center, Claude Fable models on your plan (Max/Ultra 50 %, Pro en crédits, Claude Code 2.1.321+) :
  https://support.claude.com/articles/15424964-claude-fable-models-on-your-plan
* Anthropic Help Center, What is the Ultra plan? : https://support.claude.com/en/articles/17728952-what-is-the-ultra-plan
* Anthropic, Task budgets (beta, budget indicatif sur la boucle agentique) :
  https://platform.claude.com/docs/en/build-with-claude/task-budgets
* Claude Code, hooks : entrée JSON sur stdin, `permissionDecision`, Stop et `$CLAUDE_PROJECT_DIR` :
  https://code.claude.com/docs/en/hooks
* Claude Code, What's new (auto mode par défaut, `maxEffortLevel`, `fallbackModel`, deny `Tool(param:value)`, `/usage`) :
  https://code.claude.com/docs/en/whats-new
* OpenAI, GPT‑6.1 Terra ($1/$5, Work/Codex, positionnement) : https://www.vktr.com/ai-platforms/openais-cheapest-path-to-flagship-performance-is-gpt61-terra/
* GPT‑6.1 Terra, prix, Terminal-Bench 4.0 et support Codex CLI : https://mcsaguru.com/openai-gpt-6-1-terra-launch-pricing
* OpenAI, DevDay 2026 recap (GPT‑6.1 Sol, Ultrafast) : https://openai.com/index/devday-2026-recap/
* OpenAI — GPT‑6.2 Astra et Sol : disponibilité, efficacité et tarifs :
  https://openai.com/index/introducing-gpt-6-2-astra-sol/
* OpenAI — GPT‑6.2 System Card : classification cyber et garde-fous Codex :
  https://deploymentsafety.openai.com/gpt-6-2-astra-sol/monitoring-in-codex-and-alignment-evaluations
* OpenAI Decisions API — disponibilité générale, `predicate`/`choice`/`score`, cache et tarifs :
  https://openai.com/index/decisions-api/
* OpenAI Developers — guide Decisions API, 400 questions, cache et mesure des usages :
  https://developers.openai.com/api/docs/guides/decisions
* Artificial Analysis, Claude Code vs Codex, Coding Agent Index v2.0 :
  https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex
* Metals, blog des releases (1.6.9 du 14 septembre 2026) : https://scalameta.org/metals/blog
* « Spec-Driven Development as Prescribed and as Practiced » (CMU / Google), synthèse :
  https://groundy.com/articles/spec-driven-development-prescribed-vs-practiced-what-ai-teams-should-change/
* Qodo, état du SDD en 2026 (retours Thoughtworks, instruction bloat, spec drift) :
  https://www.qodo.ai/glossary/what-is-spec-driven-development/
* TypeSafe AI — Jev 1.14 et calibration : https://typesafe.ai/blog/jev-1-14
* Spec Kit — workflow agentique de référence, commandes `analyze` et `converge` :
  https://github.github.com/spec-kit/reference/agentic-sdd.html
* sbt — documentations officielles des clients et du mode client-serveur :
  https://www.scala-sbt.org/2.x/docs/en/changes/sbt-2.0-change-summary.html
* OpenAI — GPT‑6.1 Terra, annonce et usages :
  https://developers.openai.com/api/docs/models/gpt-6.1-terra
* OpenAI — étude des limites des benchmarks SWE-bench Pro :
  https://openai.com/index/separating-signal-from-noise-coding-evaluations/
* NBER — Writing Code vs. Shipping Code: Productivity Effects Across Generations of AI Coding Tools :
  https://www.nber.org/papers/w35275
* Cross-Model LLM Code Review — expérience sur 116 problèmes algorithmiques (pas un benchmark Scala) :
  https://arxiv.org/abs/2607.21656
* CR-Bench-v2 — évaluation des défauts de review réels : https://arxiv.org/abs/2611.02566
* GitHub — rulesets, required checks, merge queue et sécurisation des actions :
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets
  https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
  https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
* GitHub — CodeQL, langages effectivement supportés :
  https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning
* DORA — Software delivery performance metrics : https://dora.dev/guides/dora-metrics/
* Google SRE Workbook — Canarying Releases : https://sre.google/workbook/canarying-releases/
  https://sre.google/workbook/data-processing/
* How Much Effort Does an AI Code Reviewer Need? — étude comparative Claude 5.5 : https://arxiv.org/abs/2611.33639
* GitHub — attestations de provenance des artefacts : https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations
