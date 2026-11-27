<!-- section: chapter -->
# 7B. Tipizzazione forte degli input e degli output degli LLMs

L'output di un LLM è un inaffidabile `String`. Il confine tra "testo modello" e "valore dominante" deve essere un decodificatore digitato che fallisce esplicitamente - mai un'analisi ottimistica.

<!-- section: s-1 -->
## Il modello di addestramento ADT + Circe

Prendere la classificazione della gravità della recensione Codex (sezione 5, passo 6) :

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

Tre regole non negoziabili, echoing sezione carrello 7:

* Mai. `Map[String, Any]` a "andare più veloce": se lo schema cambia, si desidera un errore di decodifica, non un determinato `NullPointerException` tre strati più avanti;
* il [`enum` + `emap` piuttosto che un `String`: il compilatore costringe la completezza `match` a valle;
* il decoder non ha valore sconosciuto — un LLM] che invents `"CRITICAL"` deve causare il fallimento della pipeline, non essere silenziosamente classificato opzionale.

<!-- section: s-2 -->
## Schema del modello della forza: tool_use e output strutturati

La decodifica tipod cattura le uscite malformate; ancora meglio è renderle rare forzando il diagramma lato interferenza API:

* **Anthropic** : dichiarare uno strumento con frequenza `input_schema` (JSON Schema). Per i modelli che accettano la scelta dello strumento forzato, conseguente `tool_choice: {"type": "tool", "name": "report_review"}` Intenderò l'appello. **Eccezione Fable 5.2 / Opus 5.5** : `tool_choice: "any"` e non è così `tool_choice: {"type": "tool", ...}` ritorna un errore 400 ; usi `tool_choice: "auto"`un'istruzione esplicita ("chiariamo `report_review` In tutti i casi, decodificare gli argomenti per arrivare `ReviewResult`.
* **OpenAI** : nel vuoto **Risposta API**, il formato strutturato è dichiarato via casuale `text.format` con la forza `type: "json_schema"` e non è così `strict: true` ; `response_format` Lo schema forza una risposta completa normalmente, ma il cliente deve ancora trattare esplicitamente con rifiuto, risposta incompleta, errore verifica API e invarianti nelle compravendite non espressi in JSON Schema.
* **Jev** Per una decisione chiusa, le opzioni fanno parte dell'interfaccia del modello e la risposta fornisce una risposta diretta al problema. **distribuzione delle probabilità** Per produrre testo, una spiegazione o una struttura aperta, tenere un vuoto LLM generative + decodifica digitata.

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

> **Validazione aggiuntiva** : per i contratti più ricchi, `zio-schema` (o) `io.circe.schema`) permette di intervenire
> derivare dal JSON Schema della situazione Scala tipo — un'unica fonte di verità, l'unico `case class`, invece di uno schema elettrico
> Mano tenuto dal codice.

