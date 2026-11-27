<!-- section: chapter -->
# 10B. OpenRouter as an occasional fallback

For the current workflow, ** no local gateway is required**:OpenRouter serves only as an exit door to backup models. Creates a dedicated key, sets an expense limit on the account side and explicitly selects the model to be tested.

```text
Claude Code / Codex bloqués
→ préparer un reproducer minimal
→ OpenRouter
→ choisir volontairement GLM / Kimi / Gemini / Grok
→ conserver le nom du modèle et du provider dans le journal de tâche
```

The principle is deliberately simple: **OpenRouter does not become the normal path of development**. Claude Code, Codex, Qwen local, GitHub Copilot and JetBrains AI continue to use their native surfaces.

> State of the Gemini road.** Google closed access
> free/Pro/Ultra at Gemini CLI on 18 June 2026; its successor Antigravity CLI is closed-source with a quota
> very small free (size order: ~20] queries/day). No longer rely on "a third free agent" side
> Google: for a Gemini review in troubleshooting, the rational path remains the [API] or OpenRouter, which this section
> already provides. General lesson for all the stack: never build a workflow on a free quota — it can
> disappear in the course of the quarter.

<!-- section: s-1 -->
## Minimum configuration

Only one environment variable is sufficient for scripts or tools that use OpenRouter:

```bash
export OPENROUTER_API_KEY="..."
```

For Scala point integration, keep the same abstraction `LlmClient[F[_]]` as in 7A and inject a dedicated configuration:

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

The client then keeps an OpenAI-compatible endpoint without introducing an additional local server.

<!-- section: s-2 -->
## Fallback rules

For this guide:

```text
Provider fallback pour le même modèle
→ autorisé

Fallback automatique vers un autre modèle
→ désactivé par défaut
```

The change of provision improves availability without changing the nature of the analysis. An automatic change of model on the contrary blurs the objective sought: consciously obtain an opinion from another family of models.

<!-- section: s-3 -->
## Confidentiality rules

OpenRouter aggregates several providers whose policies may differ. For professional code:

```text
- envoyer le minimum de contexte nécessaire ;
- préférer un reproducer, une stack trace et les fichiers strictement concernés ;
- ne jamais envoyer le repository entier par défaut ;
- anonymiser les données métier et secrets ;
- choisir explicitement les providers compatibles avec les exigences du projet ;
- garder les parties les plus sensibles en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-4 -->
## What OpenRouter should not replace

```text
Claude Code        → agent principal raisonnement/debug + reviewer croisé via abonnement Claude
Codex              → agent principal d'exécution + reviewer croisé via abonnement ChatGPT
Qwen local         → modèle local direct
GitHub Copilot     → workflow GitHub
JetBrains AI       → assistance IDE
OpenRouter         → escalade exceptionnelle vers d'autres modèles
```

This separation avoids turning a simple emergency door into a new layer of infrastructure to maintain.

---

