<!-- section: chapter -->
# 10A. Beobachtbarkeit von LLM-Aufrufen

Ein magnetischer Workflow ohne Telemetrie führt zur Intuition  denn die Intuition unterschätzt systematisch die Kosten der Schachschleifen. Drei Meter reichen aus, um zu steuern: **Kosten je messbare Aufgabe**, **Latenz P50/P99 nach Modell**, **Hit-Cache-Rate**.

<!-- section: s-1 -->
## Tracing mit otel4s

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

Die Kosten werden auf Kundenseite berechnet (tokens × Modelltarif, Abschnittstabelle 3) Die Felder sind nicht vom Lieferanten für diese Metrik abhängig. `tool_use`, logge jeden Toolaufruf in JSON Strukturiert (Name, Dauer, Erfolg): Dies ist, was zeigt, dass ein Agent Vergangenheit 40 Drehungen auf `bash` anstatt 3 über `compile-file`.

<!-- section: s-2 -->
## Wahl der Beobachtungsschicht

| Option                        | Integrationsbemühungen         | Kräfte                                                 | Grenzwerte                                                   |
|-------------------------------|------------------------------|--------------------------------------------------------|-----------------------------------------------------------|
| **[otel4s** (OpenTelemetry)    | Mittel (Instrumentation Code) | Standard, wird mit bestehendem Anwendungstracing gestrafft | Kein Vorgefertigtes "LLM" Dashboards   |
| **Logs JSON strukturiert**      | Niedrig (logback + appender)  | Neue Abhängigkeit, ausreichend für Solo-Tracking | Keine verteilten Spuren, manuelle Aggregation            |
| **Langfuse[** (spezialisiert LLM) | Schwach (SDK oder Proxy)        | Kosten/Latenz/Prompt-Ansichten bereit, Wiederholung der Sitzungen   | Zu beherbergende Zusatz- oder SaaS-Service ✓ zu prüfen     |
| **Dashboard OpenRouter**      | Keine                          | Genug, um den wenigen Notrufen zu folgen      | Siehe weder Claude Max noch Codex Abo noch [Qwen vor Ort. |

Für den aktuellen Einsatz: Dashboard OpenRouter Für die **Außergewöhnliche externe Anrufe**, während die Quoten Claude, Codex, Copilot und JetBrains bleiben in ihren jeweiligen Flächen. Geben Sie Grafana nicht nur ein, um einige monatliche Anrufe zu vereinen. otel4s wird relevant, wenn die LLM in das Erzeugnis eindringen (Abschnitt 7A) oder wenn die Anrufe API sie sind ausreichend automatisiert, um eine zentrale Beobachtung zu rechtfertigen.

Die Beobachtungsfähigkeit von Code-Agenten ist zu einer Produktkategorie geworden (z. B. Amazon CloudWatch ✓ Coding Agent Insights, Juli 2026, die die Telemetrie von [Claude Code, Codex und GitHub Copilot bündelt). Für einen Soloeinsatz reichen die drei metrischen Werte aus; aber es ist ein Zeichen dafür, dass die Messung des Verhaltens von Code-Agenten jetzt als eine eigenständige Kostenposition, nicht als Raffinesse, behandelt wird.

