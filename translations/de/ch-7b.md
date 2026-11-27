<!-- section: chapter -->
# 7B. Stark typisierte Ein- und Ausgaben für LLMs

Die Ausgabe eines [LLM ist eine unzuverlässige `String`. Die Grenze zwischen ✓ Text des Modells ✓ und  ✓ Domainwert muss eine typisierte Dekodierung sein, die ausdrücklich fehlschlägt, nie eine optimistische parsing.

<!-- section: s-1 -->
## Pattern ADT + Circe

Nehmen wir die Einstufung des Schweregrades der Review Codex (Abschnitt 5, Schritt 6:

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

Drei nicht handelbare Regeln, entsprechend dem Abschnitt 7:

* nie `Map[String, Any]` für    ✓ schneller gehen: Wenn sich das Schema ändert, willst du einen Dekodierungsfehler, nicht eine `NullPointerException` drei Schichten weiter;
* l'`enum` + `emap` anstatt eine `String` : Der Compiler treibt die Vollständigkeit des `match` nachgeschaltet ,
* der Decoder fehlschlägt auf unbekannten Wert  ✓ ein LLM, das [`"CRITICAL"` erfindet, muss die Pipeline scheitern lassen, nicht still optional eingestuft werden.

<!-- section: s-2 -->
## Musterseite erzwingen: tool_use und Strukturd Outputs

Typische Dekodierung fängt die schlecht geformten Ausgänge; noch besser ist es, sie selten zu machen, indem man das Schema Seite API zwang:

* **Anthropic** : ein Werkzeug mit `input_schema` (JSON Für Modelle, die erzwungenes Tool Choice akzeptieren, `tool_choice: {"type": "tool", "name": "report_review"}` Sie müssen den Anruf machen. **Ausnahme Fable 5.2 / Opus 5.5** : `tool_choice: "any"` und `tool_choice: {"type": "tool", ...}` geben einen Fehler zurück 400 ; verwendet `tool_choice: "auto"`, eine ausdrückliche Anweisung (siehe auch `report_review` Vor dem Abschluss ✓) und einem strengen Schema. In jedem Fall dekodieren Sie die Argumente auf `ReviewResult`.
* **OpenAI** : dans la **Responses API**, wird das strukturierte Format durch `text.format` mit `type: "json_schema"` und `strict: true` ; `response_format` gehört zur Chat Completions-Oberfläche. Das Schema zwingt zu einer normalerweise beendeten Antwort, aber der Client muss immer noch ausdrücklich ablehnen, unvollständige Antwort, Fehler API und invariants nicht expressiblen Beruf in JSON Schema.
* **Jev** : reduziert es nicht auf weniger kostspielige Struktur und Outputs       . Bei einer geschlossenen Entscheidung sind die Optionen Teil der Schnittstelle des Modells und die Antwort liefert direkt eine **Wahrscheinlichkeitsverteilung** Durch den Code verwertbar. Um Text, eine Erklärung oder eine offene Struktur zu erzeugen, hält ein LLM Generativ + Typisch-Dekodierung.

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

> **Zusätzliche Validierung** : bei reicheren Verträgen, `zio-schema` (oder `io.circe.schema`) erlaubt
> die JSON Schema vom Typ Scala Die Wahrheit ist eine einzige Quelle, die `case class`, statt eines Schemas
> gehalten mit der Hand, die vom Code abgeleitet wird.

