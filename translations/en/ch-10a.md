<!-- section: chapter -->
# 10A. Observability for LLM calls

An untelemetry-free workflow is driven by intuition — and intuition systematically underestimates the costs of failure loops. Three metrics are enough to drive: **cost per mergeable task**, **P latency50/P99 by model**, **cache rate hit**.

<!-- section: s-1 -->
## Tracing with otel4s

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

The cost is calculated on the customer side (tokens × model price, section table 3) — does not depend on the supplier for this metric, the fields vary. `tool_use`, log each tool call in JSON structured (name, duration, success): this is what shows that an agent has passed 40 turns on `bash` for 3 on `compile-file`.

<!-- section: s-2 -->
## Choose its observability layer

| Option                        | Integration effort         | Forces                                                 | Limits                                                   |
|-------------------------------|------------------------------|--------------------------------------------------------|-----------------------------------------------------------|
| **otel4s** (OpenTelemetry)    | Medium (code instrumentation) | Standard, fits with existing application tracing | No view "LLM" prefabricated — dashboards to be built   |
| **Logs JSON Structured**      | Low (logback + appender)  | Zero dependency new, enough for solo follow-up | No trace distributed, manual aggregation            |
| **Langfuse** (specialised) LLM) | Low (SDK or proxy)        | Cost/Latency/Prompt Views Ready, Session Replay   | Additional service to host or SaaS — to audit     |
| **Dashboard OpenRouter**      | None                          | Sufficient to follow the rare emergency calls      | Does not see Claude Max, Codex subscription, or Qwen local |

For the current use: the dashboard OpenRouter is sufficient for the ** exceptional external calls**, while the quotas Claude, Codex, Copilot and JetBrains remain followed in their respective surfaces. Do not introduce Grafana only to unify a few monthly calls. otel4s becomes relevant when the LLM enters the product (section 7A) or when calls API are sufficiently automated to justify centralized observability.

Observability of code agents has become a product category in itself (e.g. Amazon CloudWatch "Coding Agent Insights", July 2026, which aggregates the telemetry of Claude Code, Codex and GitHub Copilot). For solo use, your three metrics suffice; but this is the sign that the measurement of agent behaviour is now treated as a full cost item, not as refinement.

