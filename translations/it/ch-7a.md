<!-- section: chapter -->
# 7A. Integrazione degli LLMs in Scala funzionale

Quando un LLM diventa una dipendenza del tuo *prodotto* e non riguarda più solo il flusso di sviluppo, trattalo come qualsiasi servizio esterno. Prevedi un’interfaccia astratta ed errori tipizzati, isola gli effetti ai confini del sistema e rendilo testabile.

<!-- section: s-1 -->
## Panoramica degli approcci (Giugno 2026)

| Approccio alla ricerca                         | Bilanciamenti                        | Forze di sicurezza                                              | Limiti di risposta                                                 |
|----------------------------------|-----------------------------------|-----------------------------------------------------|---------------------------------------------------------|
| Client HTTP di basso livello           | `sttp` + `circe` (o) `zio-http`)  | Controllo totale, zero dependance pesante, fine caching conseguente | Tutto quello che ti serve scrivere: directory, streaming, tool_use          |
| Wrapper API dedicato casual                | `sttp-openai`                     | Endpoints digitati, mantenuti da softwaremill casual          | Copre OpenAI/compatibile; Anthropic tramite client separato |
| Ecosystem JVM                   | `langchain4j` (Java, callable)   | Agenti, RAG, memoria, integrazioni multiple       | API molto orientato a Java; ergonomiche Scala medio termine        |
| Generazione del cliente per contratto | `smithy4s` (se spec Smithy disponibile) | Client/server digitato, generato doc assegnato                   | Supponiamo che una Smithy spec mantenuto — raro per casualità LLM   |

Raccomandazione: per un backend casuale Scala, **cliente basso livello sttp + home abstraction** Quasi sempre batte un quadro di agenti generali. APIs probabili LLM sono semplici API HTTP JSON ; il valore è in aumento *tonnellata di neve* digitando il dominio, non in astrazione generica.

<!-- section: s-2 -->
## Struttura un generico `LlmClient[F[_]]`

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

Nei test, un'implementazione deterministica (obiettivo`LlmClient` che riscuote le risposte registrate) è sostituito — la logica aziendale attorno a casualità LLM viene poi testato senza rete, costo e flakiness.

<!-- NUOVO SEZIONE --> intervenire

