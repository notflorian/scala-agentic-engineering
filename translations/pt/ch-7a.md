<!-- section: chapter -->
# 7A. Integração de LLMs em Scala funcional

Quando um LLM passa a ser uma dependência do seu *produto* e deixa de estar restrito ao fluxo de desenvolvimento, trate-o como qualquer serviço externo. Defina uma interface abstrata e erros tipados, isole os efeitos nas fronteiras e facilite os testes.

<!-- section: s-1 -->
## Panorama de enfoques (junio 2026)

| Abordagem                         | Bibliotecas                        | Forças                                              | Limites                                                 |
|----------------------------------|-----------------------------------|-----------------------------------------------------|---------------------------------------------------------|
| Cliente HTTP de baixo nível           | `sttp` + `circe` (o `zio-http`)  | Controle total, zero dependência pesada, caching fin | Tudo é para escrever: retry, streaming, tool_use          |
| Wrapper API dedicado                | `sttp-openai`                     | Endpoints tipo, mantido por softwarewaremill          | Cubre OpenAI/compatibles; Anthropic através de um cliente separado |
| Ecosistema JVM                   | `langchain4j` (Java, chamable)   | Agentes, RAG, memórias, integrações múltiplas       | API muito orientado Java; ergonomia Scala média        |
| Geração de clientes por contrato | `smithy4s` (se spec Smithy dispõe) | Cliente/servidor tipo, doc gerado                   | Supõe uma spec Smithy que se mantém rara para LLM   |

Recomendação: para um backend Scala, **cliente de baixo nível sttp + abstração caseira** quase sempre um framework dos agentes generalistas. LLM são simples APIs HTTP JSON ; o valor está em *ton* Tipo de domínio, não na abstração genérica.

<!-- section: s-2 -->
## Estruturar um `LlmClient[F[_]]` genérico

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

Nos testes, substitui-se uma implementação determinista (`LlmClient` que reinterpreta as respostas registadas) - a lógica do ofício em torno do LLM foi então testada sem rede, sem custo e sem flakiness.

<!-- NOVA SECÇÃO -->

