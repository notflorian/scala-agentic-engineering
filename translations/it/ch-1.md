<!-- section: chapter -->
# 1. Principio guida

Per uno sviluppatore Scala senior, l’obiettivo principale è massimizzare il rapporto seguente. Scrivere codice più in fretta è secondario.

```text
Changements utiles déployés et stables
÷
(diffs inutiles + retours review + bugs + crédits brûlés + temps humain)
```

Il buon modello mentale:

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

