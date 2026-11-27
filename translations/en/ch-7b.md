<!-- section: chapter -->
# 7B. Strongly typed LLM inputs and outputs

The output of a LLM is an unreliable `String`. The boundary between "model text" and "domain value" must be a typed decoding that explicitly fails — never an optimistic parsing.

<!-- section: s-1 -->
## The pattern ADT + Circe

Take the severity classification of the review Codex (section 5, step 6) :

```scala
import io.circe.*
import io.circe.generic.semiauto.*

enum Severity:
  case Blocking, RegressionRisk, Style, OutOfScope

object Severity:
  given Decoder[Severity] = Decoder.decodeString.emap {
    case "BLOCKING"        => Right(Severity.Blocking)
    case "REGRESSION_RISK" => Right(Severity.RegressionRisk)
    case "STYLE"           => Right(Severity.Style)
    case "OUT_OF_SCOPE"    => Right(Severity.OutOfScope)
    case other             => Left(s"Sévérité inconnue : $other") // échec explicite, pas de fallback silencieux
  }

final case class Finding(severity: Severity, file: String, message: String)
final case class ReviewResult(findings: List[Finding], summary: String)

object ReviewResult:
  given Decoder[Finding]      = deriveDecoder
  given Decoder[ReviewResult] = deriveDecoder
```

Three non-negotiable rules, echoing section 7:

* never `Map[String, Any]` to "go faster": if the schema changes, you want a decoding error, not a `NullPointerException` three layers further;
* the [`enum` + `emap` rather than a `String`: the compiler forces the `match` completeness downstream;
* the decoder fails on unknown value — a LLM which invents `"CRITICAL"` must cause the pipeline to fail, not be silently classified optional.

<!-- section: s-2 -->
## Force model-side schema: tool_use and Structured Outputs

Typed decoding captures malformed outputs; even better is to make them rare by forcing the diagram side API:

* **Anthropic** : declare a tool with `input_schema` (JSON Schema). For models that accept the tool choice forced, `tool_choice: {"type": "tool", "name": "report_review"}` I'm going to impose the appeal. **Exception Fable 5.2 / Opus 5.5** : `tool_choice: "any"` and `tool_choice: {"type": "tool", ...}` return an error 400 ; uses `tool_choice: "auto"`an explicit instruction ("calls `report_review` In all cases, decode the arguments to `ReviewResult`.
* **OpenAI** : in the **Responses API**, the structured format is declared via `text.format` with `type: "json_schema"` and `strict: true` ; `response_format` belongs to the Chat Completions surface. The scheme forces a completed response normally, but the client still has to deal explicitly with refusal, incomplete response, error API and invariants in trades not expressed in JSON Schema.
* **Jev** For a closed decision, the options are part of the model interface and the response provides a direct response to the problem. **distribution of probabilities** To produce text, an explanation or an open structure, keep a LLM generative + typed decoding.

```scala
import io.circe.Json
import io.circe.syntax.*

// Le schéma est dérivable automatiquement (zio-schema, ou tapir SchemaType → JSON Schema),
// mais le maintenir à la main reste lisible pour un petit contrat :
val reviewToolSchema: Json = Json.obj(
  "type" -> "object".asJson,
  "properties" -> Json.obj(
    "findings" -> Json.obj(
      "type"  -> "array".asJson,
      "items" -> Json.obj(
        "type" -> "object".asJson,
        "properties" -> Json.obj(
          "severity" -> Json.obj(
            "type" -> "string".asJson,
            "enum" -> List("BLOCKING", "REGRESSION_RISK", "STYLE", "OUT_OF_SCOPE").asJson
          ),
          "file"    -> Json.obj("type" -> "string".asJson),
          "message" -> Json.obj("type" -> "string".asJson)
        ),
        "required" -> List("severity", "file", "message").asJson
      )
    ),
    "summary" -> Json.obj("type" -> "string".asJson)
  ),
  "required" -> List("findings", "summary").asJson
)
```

> **Additional validation** : for the richer contracts, `zio-schema` (or `io.circe.schema`) allows for
> derive the JSON Schema from the Scala type — a single source of truth, the `case class`, instead of a schematic
> Hand held by the code.

