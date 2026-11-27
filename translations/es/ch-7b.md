<!-- section: chapter -->
# 7B. Tipado fuerte de las entradas y salidas de los LLMs

La salida de un LLM es una `String` La frontera entre el texto del modelo de la línea de crédito y el valor del dominio de la línea de crédito debe ser un decodificador típico que fracase explícitamente  la versión optimista del parsing.

<!-- section: s-1 -->
## El pattern ADT + Circe

Volvamos a la clasificación de gravedad de la revisión Codex (sección 5, etapa 6:

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

Tres reglas no negociables, en eco de la sección 7:

* nunca de `Map[String, Any]` para ir más rápido  ¡: si el esquema cambia, quieres un error de decodificación, no una `NullPointerException` tres capas más adelante;
* l'`enum` + `emap` En lugar de una `String` : el compilador fuerza la exhaustividad del `match` a continuación;
* el descodificador falla sobre el valor desconocido LLM que inventa `"CRITICAL"` debe fallar la tubería, no estar en silencio clasificado opcionalmente.

<!-- section: s-2 -->
## Forzar el esquema lado modelo: tool_use y Structured Outputs

El decodificación tipo captura las salidas malformadas; aún mejor es hacerlas raras forzando el esquema lado API:

* **Anthropic** : declarar una herramienta con `input_schema` (JSON schema). Para los modelos que aceptan el tool choice forzado, `tool_choice: {"type": "tool", "name": "report_review"}` Obliga la llamada. **Excepciones Fable 5.2 / Opus 5.5** : `tool_choice: "any"` y `tool_choice: {"type": "tool", ...}` devuelven un error 400 ; utiliza `tool_choice: "auto"`, una instrucción explícita (el `report_review` antes de concluir ?) y un esquema estricto. En todos los casos, decodifica los argumentos hacia `ReviewResult`.
* **OpenAI** : en la **Responses API**, el formato estructurado se manifiesta a través de `text.format` con `type: "json_schema"` y `strict: true` ; `response_format` pertenece a la superficie Chat Completions. El esquema obliga una respuesta terminada normalmente, pero el cliente todavía tiene que tratar explícitamente rechazo, respuesta incompleta, error API no expresables en JSON Schema.
* **Jev** : no se reduce a  ¡Futured Outputs más baratos! Para una decisión cerrada, las opciones forman parte de la interfaz del modelo y la respuesta proporciona directamente una **Distribución de probabilidades** Para producir texto, una explicación o una estructura abierta, mantén un LLM Generativo + decodificador tipo.

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

> **Validación adicional** : para los contratos más ricos, `zio-schema` (o `io.circe.schema`) permite
> derivar el JSON Schema desde el tipo Scala - una sola fuente de verdad, el `case class`, en lugar de un esquema
> Mantenido a mano que deriva del código.

