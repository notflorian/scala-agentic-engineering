<!-- section: chapter -->
# 10A. Observabilidade das chamadas a LLMs

Um fluxo de trabalho operacional sem telemetria foi pilotado com a intuição e a intuição subestima sistematicamente os custos dos riços de xadrez. Três métricas bastam para pilotar: **coste por tarefa mergeável**, **latencia P50/P99 por modelo**, **tase de cache hit**.

<!-- section: s-1 -->
## Tracing com otel4s

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

O custo é calculado no lado do cliente (tokens × tarifa do modelo, tabela da secção 3) Não depende do fornecedor para esta métrica, os campos variam. `tool_use`, logge cada chamada de ferramenta em JSON estruturado (nome, duração, sucesso): isto é o que permite ver que um agente passou 40 voltas sobre `bash` em vez de 3 sobre `compile-file`.

<!-- section: s-2 -->
## Escolher a sua camada de observação

| Opção                        | Esforço de integração         | Forças                                                 | Limites                                                   |
|-------------------------------|------------------------------|--------------------------------------------------------|-----------------------------------------------------------|
| **otel4s** (OpenTelemetry)    | Meio (instrumentation code) | Padrão, se agrégase com o tracing de aplicação existente | Sem vista "LLM" pré-fabricado tijolos para construir   |
| **Logs JSON estruturados**      | Baixa (logback + appender)  | Cero dependência nova, suficiente para o seguimento sozinho | Sem traços distribuídos, agregação manual            |
| **Langfuse** (especializado LLM) | Baixo (SDK ou proxy)        | Opiniões de custo/latencia/pronta preparação, revisão das sessões   | Serviço adicional para hospedagem ou SaaS para auditório     |
| **Dashboard OpenRouter**      | Não.                          | O suficiente para rastrear as poucas chamadas de emergência      | Não vê Claude Max, nem Codex assinatura, nem Qwen local |

Para o uso atual: o dashboard OpenRouter basta para os **Llamadas externas excepcionais**, enquanto as quotas Claude, Codex, Copilot e JetBrains permanecem seguidas nas respectivas superfícies. Não introduza Grafana apenas para unificar algumas chamadas mensais. otel4s se torna pertinente quando o LLM entra no produto (secção 7A) ou quando as apelações API são suficientemente automatizadas para justificar uma observabilidade centralizada.

A observabilidade dos agentes de código tornou-se uma categoria produzida em si mesma (por exemplo, Amazon CloudWatch Coding Agent Insights 2026, que amplia a telemetria de Claude Code, Codex e GitHub CopilotPara um uso só, suas três métricas bastam; mas é o sinal de que a medição do comportamento dos agentes é agora como uma partida de custo por direito próprio, não como um refinamento.

