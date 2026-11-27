<!-- section: chapter -->
# 7B. Tipagem forte das entradas e saídas de LLMs

A saída de uma LLM é uma `String` A fronteira entre o texto do modelo da linha de crédito e o valor do domínio da linha de crédito deve ser um descodificador típico que fraca explicitamente a versão otimista do parsing.

<!-- section: s-1 -->
## O pattern ADT + Circe

Voltamos à classificação de gravidade da revisão Codex (secção 5, etapa 6:

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

Três regras não transaccionáveis, eco da secção 7:

* nunca de `Map[String, Any]` para ir mais rápido: se o esquema mudar, você quer um erro de descodificação, não uma `NullPointerException` três camadas mais adiante;
* l'`enum` + `emap` Em vez de uma `String` : o compilador força a exaustividade do `match` a seguir;
* O descodificador falha no valor desconhecido LLM que inventa `"CRITICAL"` deve falhar o tubo, não estar em silêncio classificado opcionalmente.

<!-- section: s-2 -->
## Forçar o esquema lado modelo: tool_use e Structured Outputs

O descodificador tipo captura as saídas malformadas; ainda melhor é torná-las raras forçando o esquema lado API:

* **Anthropic** : declarar uma ferramenta com `input_schema` (JSON schema). Para os modelos que aceitam o tool choice forçado, `tool_choice: {"type": "tool", "name": "report_review"}` Obriga a chamada. **Excepções Fable 5.2 / Opus 5.5 ** : `tool_choice: "any"` e `tool_choice: {"type": "tool", ...}` devolvem um erro 400 ; utiliza `tool_choice: "auto"`, uma instrução explícita (o `report_review` antes de concluir ?) e um esquema estrito. Em todos os casos, descodificar os argumentos para `ReviewResult`.
* **OpenAI** : na **Responses API**, o formato estruturado se manifesta através de `text.format` com `type: "json_schema"` e `strict: true` ; `response_format` pertence à superfície Chat Completions. O esquema obriga uma resposta terminada normalmente, mas o cliente ainda tem que tratar explicitamente rejeição, resposta incompleta, erro API não expressáveis em JSON Schema.
* **Jev** : não se reduz a Futured Outputs mais baratos! Para uma decisão fechada, as opções fazem parte da interface do modelo e a resposta fornece diretamente uma ** Distribuição de probabilidades** Para produzir texto, uma explicação ou uma estrutura aberta, mantenha um LLM Generativo + descodificador tipo.

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

> **Validação adicional** : para os contratos mais ricos, `zio-schema` (ou `io.circe.schema`) permite
> derivar o JSON Schema do tipo Scala - uma única fonte de verdade, o `case class`, em vez de um esquema
> Mantendo à mão que deriva do código.

