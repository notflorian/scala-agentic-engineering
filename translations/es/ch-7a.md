<!-- section: chapter -->
# 7A. Integración de LLMs en Scala funcional

Cuando un LLM se convierte en una dependencia de tu *producto* y ya no solo de tu flujo de desarrollo, trátalo como cualquier servicio externo. Define una interfaz abstracta y errores tipados, aísla los efectos en el límite y facilita las pruebas.

<!-- section: s-1 -->
## Panorama de enfoques (junio 2026)

| Enfoque                         | Librerías                        | Fuerzas                                              | Límites                                                 |
|----------------------------------|-----------------------------------|-----------------------------------------------------|---------------------------------------------------------|
| Cliente HTTP de bajo nivel           | `sttp` + `circe` (o `zio-http`)  | Control total, cero dependencia pesada, caching fin | Todo es para escribir: retry, streaming, tool_use          |
| Wrapper API dedicado                | `sttp-openai`                     | Endpoints tipo, mantenido por softwarewaremill          | Cubre OpenAI/compatibles; Anthropic a través de un cliente separado |
| Ecosistema JVM                   | `langchain4j` (Java, llamable)   | Agentes, RAG, memorias, integraciones múltiples       | API muy orientado Java; ergonomía Scala media        |
| Generación de clientes por contrato | `smithy4s` (si spec Smithy dispone) | Cliente/servidor tipo, doc generado                   | Supone una spec Smithy que se mantiene rara para LLM   |

Recomendación: para un backend Scala, **cliente de bajo nivel sttp + abstraccion casera** casi siempre un framework de los agentes generalistas. LLM son simples APIs HTTP JSON ; el valor está en *ton* Tipo de dominio, no en la abstracción genérica.

<!-- section: s-2 -->
## Estructurar un `LlmClient[F[_]]` genérico

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

En las pruebas se sustituye una implementación determinista (`LlmClient` que reinterpreta las respuestas registradas) - la lógica del oficio alrededor del LLM se prueba entonces sin red, sin costo y sin flakiness.

<!-- NUEVA SECCIÓN -->

