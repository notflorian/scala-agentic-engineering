<!-- section: chapter -->
# 10A. Osservabilità delle chiamate agli LLMs

Un flusso di lavoro privo di telemetria è guidato dall'intuizione — e l'intuizione sottovaluta sistematicamente i costi dei loop di guasto. **costo per attività di fusione**, **P latenza50/P99 da modellare**, **tasso di cache colpito**.

<!-- section: s-1 -->
## Tracciamento con otel4s

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

Il costo è calcolato sul lato del cliente (tokens × prezzo del modello, sezione tabella indicativa 3) — non dipende dal fornitore per questa metrica, i campi variano. `tool_use`, logga ogni chiamata di strumento in sequenza JSON strutturato (nome, durata, successo): ecco cosa mostra che un agente ha superato 40 si accende `bash` per il futuro 3 su di noi `compile-file`.

<!-- section: s-2 -->
## Scegli il suo livello di osservabilità

| Opzione                        | Integrazione dello sforzo         | Forze di sicurezza                                                 | Limiti di risposta                                                   |
|-------------------------------|------------------------------|--------------------------------------------------------|-----------------------------------------------------------|
| **otel4s** (OpenTelemetry)    | Media (codice strumentazione) | Standard, si adatta con l'applicazione esistente tracing casual | Nessuna vista "LLM" prefabbricato — cruscotti per essere costruito appositamente   |
| **Registri di registrazione JSON Struttura in legno**      | Basso (logback + appendir)  | Dipendenza zero nuova, sufficiente per il follow-up solitario | Nessuna traccia distribuita, aggregazione manuale            |
| **Langfuse** (specializzato) LLM]]]] | Basso (SDK o proxy)        | Cost/Latency/Prompt Views Ready, Session Replay casual   | Servizio aggiuntivo per host o SaaS — per audit suppletivo     |
| **Dashboard per il tempo libero OpenRouter**      | Non e' vero.                          | Basti seguire le rare chiamate di emergenza      | Non vede l'abbonamento a Claude Max, Codex, o Qwen locale |

Per l'uso corrente: il cruscotto accelera OpenRouter è sufficiente per l'eliminazione ** chiamate esterne eccezionali**, mentre le quote Claude, contingenti Codex, Copilota e speranza JetBrains non introdurre Grafana solo per unificare alcune chiamate mensili. otel4s diventa pertinente quando l'argomento LLM entra nel prodotto (sezione casuale 7A) o quando si chiama API sono sufficientemente automatizzati per giustificare l'osservanza centralizzata.

L'osservazione degli agenti di codice è diventata una categoria di prodotto in sé (ad esempio Amazon CloudWatch "Coding Agent Insights", luglio 2026, che aggrega la telemetria di Claude Code, Codex e GitHub Copilot). Per uso personale, bastano tre metriche; ma questo è il segno che la misurazione del comportamento dell'agente è ora trattata come un elemento di costo completo, non come perfezionamento.

