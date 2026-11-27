<!-- section: chapter -->
# 7A. Integrating LLMs in functional Scala

When an LLM becomes a dependency of your *product* rather than just your development workflow, treat it like any other external service. Give it an abstract interface and typed errors, isolate effects at the boundary, and make it testable.

<!-- section: s-1 -->
## Overview of approaches (June 2026)

| Approach                         | Libraries                        | Forces                                              | Limits                                                 |
|----------------------------------|-----------------------------------|-----------------------------------------------------|---------------------------------------------------------|
| Low level HTTP Client           | `sttp` + `circe` (or `zio-http`)  | Total control, zero heavy dependence, fine caching | Everything you need to write: directory, streaming, tool_use          |
| Wrapper API dedicated                | `sttp-openai`                     | Typed Endpoints, maintained by softwaremill          | Covers OpenAI/compatible; Anthropic via separate client |
| Ecosystem JVM                   | `langchain4j` (Java, callable)   | Agents, RAG, memory, multiple integrations       | API very Java oriented; ergonomics Scala medium        |
| Customer generation by contract | `smithy4s` (if spec Smithy available) | Client/server typed, generated doc                   | Suppose a Smithy spec maintained — rare for LLM   |

Recommendation: for a backend Scala, **client low level sttp + home abstraction** Almost always beats a framework of general agents. APIs LLM are simple HTTP APIs JSON ; the value is in *tone* typing the domain, not in generic abstraction.

<!-- section: s-2 -->
## Structure a generic `LlmClient[F[_]]`

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

In the tests, a deterministic implementation (`LlmClient` that replays recorded answers) is substituted — the business logic around LLM is then tested without network, cost and flakiness.

<!-- NEW SECTION -->

