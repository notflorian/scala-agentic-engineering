<!-- section: chapter -->
# 7A. LLM-Integration in funktionalem Scala

Wenn ein LLM zur Abhängigkeit deines *Produkts* wird und über den Entwicklungsablauf hinausgeht, behandle es wie jeden anderen externen Dienst. Lege eine abstrakte Schnittstelle und typisierte Fehler fest, isoliere Effekte an den Systemgrenzen und stelle die Testbarkeit sicher.

<!-- section: s-1 -->
## Panorama der Ansätze (Juni) 2026)

| Ansatz                         | Bibliotheken                        | Kräfte                                              | Grenzwerte                                                 |
|----------------------------------|-----------------------------------|-----------------------------------------------------|---------------------------------------------------------|
| Niedriger HTTP-Client           | `sttp` + `circe` (oder `zio-http`)  | Volle Kontrolle, keine schwere Abhängigkeit, feines Caching | Alles ist zu schreiben: retry, streaming, tool_use          |
| Wrapper API gewidmet                | `sttp-openai`                     | Typische Endpoints, beibehalten von softwaremill          | Deckung OpenAI/kompatibel; Anthropic über separate Client |
| Ökosystem JVM                   | `langchain4j` (Java, anrufbar)   | Agenten, RAG, Gedächtnis, viele Integrationen       | API sehr zielgerichtet Java ; Ergonomie Scala Mittel        |
| Kundenerstellung durch Vertrag | `smithy4s` (wenn spec Smithy verfügbar) | Typische Client/Server, generierter Doc                   | Angenommen, Smithy-Spect bleibt selten bei LLM   |

Empfehlung: für einen Backend Scala, **niedriger Kunde sttp + Hausabstrakt** Meistens schlägt ein Framework von Generalisten. LLM sind einfache HTTP-APIs JSON ; der Wert ist in *Ton* Typisierung der Domain, nicht in der allgemeinen Abstraktion.

<!-- section: s-2 -->
## Eine allgemeine `LlmClient[F[_]]` Struktur

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

In den Tests wird eine deterministische Implementation (`LlmClient` ersetzt, die aufgezeichnete Antworten wiedergibt.) Die professionelle Logik um die [LLM testet sich dann ohne Netzwerk, ohne Kosten und ohne Flakine.

<!-- NEUER ABSCHNITT -->

