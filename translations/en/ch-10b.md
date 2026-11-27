<!-- section: chapter -->
# 10B. OpenRouter as an occasional fallback

For the current workflow, ** no local gateway is required**:OpenRouter serves only as an exit door to backup models. Creates a dedicated key, sets an expense limit on the account side and explicitly selects the model to be tested.

```text
Claude Code / Codex blocked
→ prepare a minimal reproducer
→ OpenRouter
→ deliberately choose GLM / Kimi / Gemini / Grok
→ record the model and provider names in the task log
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
Provider fallback for the same model
→ allowed

Automatic fallback to a different model
→ disabled by default
```

The change of provision improves availability without changing the nature of the analysis. An automatic change of model on the contrary blurs the objective sought: consciously obtain an opinion from another family of models.

<!-- section: s-3 -->
## Confidentiality rules

OpenRouter aggregates several providers whose policies may differ. For professional code:

```text
- send the minimum context needed
- prefer a reproducer, a stack trace, and only the files directly involved
- never send the entire repository by default
- anonymize business data and secrets
- explicitly choose providers compatible with project requirements
- keep the most sensitive parts local or with already-approved direct providers.
```

<!-- section: s-4 -->
## What OpenRouter should not replace

```text
Claude Code        → primary reasoning/debugging agent + cross-reviewer via Claude subscription
Codex              → primary implementation agent + cross-reviewer via ChatGPT subscription
Local Qwen         → local model directly
GitHub Copilot     → GitHub workflow
JetBrains AI       → IDE assistance
OpenRouter         → exceptional escalation to other models
```

This separation avoids turning a simple emergency door into a new layer of infrastructure to maintain.

---

