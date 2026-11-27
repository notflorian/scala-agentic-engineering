<!-- section: chapter -->
# 10A. Observabilidad de las llamadas a LLMs

Un flujo de trabajo operativo sin telemetría se pilota con la intuición y la intuición subestima sistemáticamente los costes de los rizos de ajedrez. Tres métricas bastan para pilotar: **coste por tarea mergeable**, **latencia P50/P99 por modelo**, **tasa de caché hit**.

<!-- section: s-1 -->
## Tracing con otel4s

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

El coste se calcula en el lado del cliente (tokens × tarifa del modelo, tabla de la sección 3) No depende del proveedor para esta métrica, los campos varían. `tool_use`, logge cada llamada de herramienta en JSON estructurado (nombre, duración, éxito): esto es lo que permite ver que un agente ha pasado 40 vueltas sobre `bash` en lugar de 3 sobre `compile-file`.

<!-- section: s-2 -->
## Elegir su capa de observabilidad

| Opción                        | Esfuerzo de integración         | Fuerzas                                                 | Límites                                                   |
|-------------------------------|------------------------------|--------------------------------------------------------|-----------------------------------------------------------|
| **otel4s** (OpenTelemetry)    | Medio (instrumentation code) | Estándar, se agrégase con el tracing de aplicación existente | Sin vista "LLM" prefabricada  ladrillos para construir   |
| **Logs JSON estructurados**      | Baja (logback + appender)  | Cero dependencia nueva, suficiente para el seguimiento solo | Sin trazas distribuidas, agregación manual            |
| **Langfuse** (especializado LLM) | Bajo (SDK o proxy)        | Opiniones de costo/latencia/pronta preparación, repaso de las sesiones   | Servicio adicional para hospedaje o SaaS para auditorio     |
| **Dashboard OpenRouter**      | No.                          | Suficiente para rastrear las pocas llamadas de emergencia      | No ves a Claude Max, ni Codex suscripción, ni Qwen local |

Para el uso actual: el dashboard OpenRouter basta para los **Llamadas externas excepcionales**, mientras que las cuotas Claude, Codex, Copilot y JetBrains permanecen seguidos en sus respectivas superficies. No introduzcas Grafana sólo para unificar algunas llamadas mensuales. otel4s se convierte en pertinente cuando el LLM entra en el producto (sección 7A) o cuando las apelaciones API son suficientemente automatizados para justificar una observabilidad centralizada.

La observabilidad de los agentes de código se ha convertido en una categoría producida en sí misma (por ejemplo, Amazon CloudWatch Coding Agent Insights 2026, que agranda la telemetría de Claude Code, Codex y GitHub CopilotPara un uso solo, tus tres métricas bastan; pero es el signo de que la medición del comportamiento de los agentes se trata ahora como una partida de coste por derecho propio, no como un refinamiento.

