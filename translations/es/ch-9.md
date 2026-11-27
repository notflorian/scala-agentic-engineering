<!-- section: chapter -->
# 9. Integraciones MCP prioritarias

<!-- section: s-1 -->
## Indispensables

| MCP                        | Función                                                                                 |
|----------------------------|--------------------------------------------------------------------------------------|
| **Metals MCP**             | Inteligencia Scala en vivo: compilación, diagnósticos, tipos, símbolos                      |
| **ScalaSemantic MCP**      | Grafio semántico Scala vía SemanticDB: usos, jerarquías, call paths, givens     |
| **JetBrains MCP**          | Explique IntelliJ, archivos abiertos, acciones IDE                                      |
| **Sourcebot**              | Búsqueda/discovery codebase multi-repos                                             |
| **Codebase-Memory MCP**    | Knowledge graph estructural persistente polyglotte , sobre todo Java/Kotlin/cross-service |
| **GitHub MCP**             | Issues, PR, Actions, checks                                                          |
| **Context7**               | Documentación de libs actualizada                                                         |
| **Playwright MCP**         | Validación UI si app web                                                             |
| **Sentry MCP**             | Diagnostic bugs prod                                                                 |
| **Postgres read-only MCP** | Plano, migración, peticiones                                                         |
| **ast-grep MCP**           | Investigación estructural y refactores específicos                                           |

Características operativas (que se revisará en el momento de la instalación  la evolución del transporte y las versiones):

| MCP                    | Transporte típico               | Versión mínima notable                   | Mantenimiento de junio 2026                                    |
|------------------------|---------------------------------|--------------------------------------------|----------------------------------------------------------|
| Metals MCP             | stdio; standalone desde 1.6.6 | Metals 1.5.3 (integrado), 1.6.6 (standalona) | Activo (Scalameta)                                        |
| ScalaSemantic MCP      | MCP local                       | SemanticDB necesario para el corazón del índice  | Joven; especializado Scala, para benchmarker en el repo      |
| JetBrains MCP          | servidor integrado IDE             | IntelliJ 2025.2 (servidor)                  | Activo (JetBrains)                                        |
| Sourcebot              | HTTP                            | —                                          | Activo                                                    |
| Códigobase-Memory MCP    | MCP local                       | —                                          | Activo; Hybrid LSP documentado para Java/Kotlin, no Scala |
| GitHub MCP             | HTTP remoto o stdio local     | —                                          | Activo (GitHub oficial)                                  |
| Context7               | HTTP distant                    | —                                          | Activo                                                    |
| Playwright MCP         | stdio                           | —                                          | Activo (Microsoft)                                        |
| Sentry MCP             | HTTP distant                    | —                                          | Activo (Sentry oficial)                                  |
| Postgres read-only MCP | stdio                           | —                                          | Variable según la implementación de la auditoría de antes de prod     |
| ast-grep MCP           | stdio                           | —                                          | Activo                                                    |

> **Evolución del protocolo MCP para conocer** : **MCP 2026-07-28 es ahora la especificación publicada de referencia**.
> El corazón se convierte en stateless: retirada de las sesiones de nivel protocolario, de `Mcp-Session-Id` y, para esa revisión,
> `initialize` / `notifications/initialized` Cada solicitud transporta en `_meta` la información
> `server/discover` permite descubrir la identidad, las versiones y las capacidades del cliente.
> capacidad del servidor. La revisión también formaliza el marco de **Extensiones**, **Tasks[** para el trabajo largo,
> **MCP Apps**, la autorización alineada OAuth/OIDC y una política de depreciación; `Roots`, `Sampling` y
> `Logging` para un nuevo desarrollo, **Objetivo 2026-07-28**, pero mantiene pruebas de compatibilidad
> 2025-11-25 hasta que todos los clientes/servidores utilizados sean migrados. Claude Code 2.1.27x generalizó su cliente
> MCP v2 y Negociación 2026-07-28 las conexiones HTTP directas, incluyendo Bedrock, Vertex, Foundry y
> instalaciones
> Sin telemetría; subsiste un modo legacy. Por lo tanto, no supone que todos los pares MCP de un entorno
> reciente
> Migraron al mismo tiempo.

> **MCP Events sigue siendo una extensión propuesta, no el núcleo del protocolo.** ChatGPT sabe experimentar suscripciones
> `events/list`, `events/subscribe` y `events/unsubscribe` con entrega webhook en servidores en MCP 2.0
> (`2026-07-28`). Esto es útil para los flujos de trabajo de eventos • Comentario creado, incidente, mensaje, cambio
> de estado ? pero no haga que una integración crítica dependa de esta extensión mientras su estado y soporte
> no se estabilizan los clientes/servidores.

<!-- section: s-2 -->
## ChatGPT y Codex : funciones MCP No confundir

Hay que distinguir **ChatGPT web**, las **clientes Codex locales** y el **Agentes API**. MCP describe una relación cliente/servidor; el hecho de que un producto también puede exponer una API de orquesta no lo convierte en servidor MCP.

| Superficie                                                       | Función MCP y transporte                                                                            | Autenticación                                                                      | Lectura / escritura                                                                          |
|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Codex CLI / extensión IDE / host Codex de ChatGPT Desktop** | **Client MCP** ; STIDO local y Streatable HTTP remoto; configuración compartida en el mismo host | Bearer, OAuth, CIMD y DCR; `codex mcp login` para OAuth                             | Dependiendo de las herramientas del servidor, el sandbox y las autorizaciones; la lectura y escritura posibles |
| **ChatGPT web Pro**                                           | Cliente de apps MCP **distantes**                                                                   | OAuth según la app                                                                     | Developer modo limitado a las herramientas `read` / `fetch`                                           |
| **ChatGPT Web Business / Enterprise / Edu**                   | Cliente de aplicaciones MCP remotos; **full MCP en beta**                                                | OAuth + control workspace/admin                                                     | Herramientas de lectura y acciones `write` / `modify` posibles para los MCP personalizados        |
| **OpenAI Agentes API**                                         | Cliente MCP alojado o desde el entorno; HTTP o STDIO según el origen de la conexión         | Headers/Bearer, caja fuerte de credentials o variables ambientales según el transporte | `allowed_tools` permite reducir explícitamente la superficie expuesta                          |

> **Documentación OpenAI En contraposición.** El Help Center detallado mantiene **Pro =
> `read`/`fetch`** y reserva el full MCP read/write a Business/Enterprise/Edu, mientras que la página de desarrollador
> Generalista ahora afirma que el developer mode da el full MCP read/write a Plus y Pro. Mientras ambos
> fuentes oficiales no convergen, mantenga el cuadro anterior como hipótesis conservadora y **detecta los
> capacidad real expuesta por la cuenta/workspace** antes de diseñar un flujo de trabajo de escritura.

**Codex ya no es un servidor MCP.** `codex mcp-server` y el binario `codex-mcp-server` se han eliminado. Una integración que quiere pilotar Codex como servicio debe migrar hacia **Codex App Server**, que utiliza su propio JSON- RCP y **no es MCP** ; Codex continua al mismo tiempo que consume servidores MCP externos como cliente.

ChatGPT web no se conecta directamente a `localhost`. Para uno MCP local, privado o on-premise, explícalo a través del **Secure MCP Tunnel** en lugar de abrir el servidor públicamente. Dos limitaciones de superficie siguen siendo importantes: **Agente de moda no utiliza las apps MCP personalizadas**, et **Deep Research** sólo los utiliza en `read` / `fetch`.

<!-- section: s-3 -->
### Gobernar catálogo MCP como una API versión

Cuando un administrador aprueba una aplicación MCP en ChatGPT, el producto conserva un **snapshot aprobado herramientas y sus entradas**. Agregar, retirar o modificar una herramienta en el servidor no hace automáticamente la nueva superficie activa. Por lo tanto, una evolución incompatible puede romper llamadas hasta que un administrador haya revisado y publicado el catálogo, y ChatGPT no garantiza actualmente una alerta proactiva sobre esta deriva.

```text
changement de nom / schéma / permission / nouvel outil MCP
→ diff de surface
→ review
→ validation admin
→ publication
```

Esta regla ** completa**, sin sustituirla, la política de seguridad de esta sección: versiones enclavadas, permisos mínimos, logs de herramientas y separación lectura/escritura.

<!-- section: s-4 -->
## Knowledge graph MCP para Scala, Java y Kotlin

**Sourcebot no es un knowledge graph.** Queda la capa de búsqueda/discovery: encontrar rápidamente archivos, símbolos, usos de texto y extractos relevantes, especialmente en varios respirerios. Un knowledge graph responde a otra clase de preguntas: relaciones entre símbolos, rutas de llamada, jerarquías, dependencias estructurales y impacto de un cambio.

<!-- section: s-5 -->
### Scala : Priorizar ScalaSemantic, completar con Metals

Para un depósito principalmente Scala, **ScalaSemantic MCP** es el mejor candidato identificado para la capa de la capa de la semántica de la semántica de la semántica. No sólo reconstruye el código desde un AST Tree-sitter: su índice principal es alimentado por **SemanticDB**, por lo tanto, mediante símbolos ya resueltos en el momento de la compilación. Presenta peticiones globales adaptadas a los agentes, en particular usos exactos, firmas, jerarquías, overloads, `call_path`, búsqueda de givens y rastreo de cadenas de implicits.

```text
Sourcebot
→ « où est X ? »
→ « quels fichiers parlent de Y ? »

ScalaSemantic MCP
→ « quels sont les usages exacts de ce symbole ? »
→ « quel chemin d'appel relie A à B ? »
→ « qui étend ce trait ? »
→ « quels givens peuvent produire T ? »
→ « de quels implicits dépend ce given ? »

Metals MCP
→ « quel est le type réel ici, maintenant ? »
→ « ce fichier compile-t-il ? »
→ « quels diagnostics le compilateur retourne-t-il ? »
→ « quels tests échouent ? »
```

ScalaSemantic y Metals son **adicionales**. ScalaSemantic es index-wide y excelente para las relaciones globales; Metals Sigue siendo la fuente de la verdad en vivo para el buffer actual, la presentación compilar, los diagnósticos, la compilación y las pruebas. SemanticDB representa principalmente el último estado compilado: si el código acaba de ser modificado sin recompilación, Metals puede ser más fresco.

Tampoco presenta ScalaSemantic como un Neo4j/RDF genérico: es más precisamente un **semantic code graph MCP**. Algunas operaciones siguen siendo aproximaciones de alto nivel y no reproducen necesariamente toda la lógica del compilador a un call lugar preciso. En caso de contradicción sobre la resolución efectiva de un tipo, de un overload o de un given, **Metals/scalac gana**.

<!-- section: s-6 -->
### Java y Kotlin: Codebase-Memory se vuelve mucho más interesante

**Codebase-Memory MCP** Construye un knowledge graph persistente de funciones, clases, call chains, carreteras HTTP y enlaces cross-service desde Tree-sitter. Su segunda pasada **Java y Kotlin**. En estos dos lenguajes, por lo tanto, es más pertinente que en Scala para las cuestiones estructurales de código base-escalera.

```text
Java / Kotlin

Sourcebot
= recherche et discovery

Codebase-Memory MCP
= knowledge graph persistant
= call graph
= impact analysis
= architecture
= routes et relations cross-service

IntelliJ / LSP
= sémantique live et arbitrage local
```

En un código base JVM poliglotis, la distribución recomendada pasa a ser:

```text
Scala pur
→ Sourcebot + ScalaSemantic + Metals

Java/Kotlin
→ Sourcebot + Codebase-Memory + IntelliJ/LSP

Scala + Java + Kotlin / microservices
→ Sourcebot
→ ScalaSemantic pour la sémantique Scala
→ Codebase-Memory pour la topologie polyglotte et cross-service
→ Metals / IntelliJ pour arbitrer la sémantique live
```

¿El criterio determinante no es el de si tiene una base gráfica? **qué información crea los bordes** :

```text
Tree-sitter
→ structure syntaxique et résolution heuristique

SemanticDB
→ symboles résolus par le compilateur Scala

LSP / presentation compiler
→ état sémantique live du code courant
```

Por lo tanto, para el desarrollo Scala, prefiere una arista SemanticDB a una arista reconstruida únicamente desde el texto cuando ambos están disponibles.

<!-- section: s-7 -->
### Efecto sobre el context engineering

Esta capa de gráfico es sobre todo útil si evita cargar decenas de archivos. Un subagent read-only puede interrogar a ScalaSemantic o Codebase-Memory y luego rastrear sólo algunos caminos, símbolos y pruebas `file:line` al padre:

```text
question d'impact
→ subagent isolé
→ knowledge graph / semantic graph
→ 5–10 relations pertinentes
→ vérification Metals / IntelliJ si nécessaire
→ résumé < 1–2K tokens
→ parent
```

Esto aumenta el`isolation_ratio` y reduce directamente el *context rot*. En cambio, no activa más de un MCP de gráfico por principio: benchmarkelas en diez tareas reales y guarde solamente aquellos que reduzcan el número de archivos leídos, los tokens inyectados o los errores de comprensión.

<!-- section: s-8 -->
### Alternativas a conocer sin estandarizarlas

`agent4s` es un toolbox Scala MCP Interesante, basado en Scalameta con SemanticDB opcional, que expone, entre otras cosas, referencias, jerarquías, dependencias y call graph. Merece un bake-off si ScalaSemantic no cubre una clase de tareas, pero no añade las dos primeras.

Joern construye un verdadero **Código Property Graph** muy rica para el análisis de seguridad y datos de flujo, pero su fuente frontal no apunta Scala El análisis del bytecode JVM Scala es posible , a costa de la pérdida de una parte de las abstracciones fuente; por lo tanto , reserva Joern a auditorías especializadas en lugar de en el contexto cotidiano de Claude Code.

<!-- section: s-9 -->
## Metals MCP : la herramienta Scala desaparecidos en la mayoría de los stacks

Es probablemente el MCP el más infrautilizada por los desarrolladores Scala. **Metals (language server Scala) atraca un servidor MCP desde la v1.5.3** (mayo 2025), y **v1.6.6 Osmium (3 Marzo 2026) añadió un servidor MCP standalone** que gira sin un editor abierto, por lo tanto, disponible directamente por Claude Code o Codex CLI en terminal. Esta misma versión ha añadido el soporte de **templates Twirl de Play**, directamente relevante para tu estack.

Las herramientas expuestas incluyen, entre otras cosas: `compile-file`, `compile-full`, `compile-module`, `test`, `inspect`, `get-docs`, `get-usages`, `get-source`, `import-build`, `find-dep`, las herramientas Scalafix, `glob-search` y `typed-glob-search`. La herramienta clave para los rizos agenticos permanece **`compile-file`** : el agente escribe, recopila el archivo, recibe los errores de tipo/implicits y corrige inmediatamente, sin pagar un ciclo `sbt compile` completa en cada iteración.

Articulación con JetBrains MCP y ScalaSemantic:

```text
JetBrains MCP     = contexte IDE quand IntelliJ est ouvert (fichiers ouverts, inspections, run configs)
ScalaSemantic MCP = relations globales SemanticDB : usages, hiérarchies, call paths, givens
Metals MCP        = feedback compilateur live pour les agents terminal, même IDE fermé
```

Los tres son complementarios, no redundantes. Claude Code larga o las tareas lanzadas fuera de IED (CI local, worktree paralelo), Metals MCP es el que transforma el agente adivina los tipos

> **Versión Metals** : **Metals 1.6.9 se publica desde el 14 septiembre 2026** (después de 1.6.8 del 23 Julio).
> MCP aporta el `glob-search` a todos los módulos, la resolución de los resultados de las pruebas entre módulos, la
> sugerencia de`import-build` cuando no se encuentra ningún objetivo de edificio y un parche contra bloqueos sobre errores
> Esto es directamente útil para los monorepos de Play/sbt Multi-▁moyenses: toma 1.6.9 como mínimo para
> pendientes agenticos. Existen milestonas Metals 2, pero no las estandarizan hasta que se produzca una liberación estable.

<!-- section: s-10 -->
## Ejemplo: hebilla de prueba-correción agentica en `compile-file`

Esqueleto ZIO del bucle que hace el valor de Metals MCP El agente corrige contra el **compilador**, no contra su propia confianza, con un borne de torres que materializa la regla 2 ajedrez → stop  ¡Oh!

```scala
import zio.*

final case class Diagnostic(file: String, line: Int, message: String)
final case class CompileResult(success: Boolean, diagnostics: List[Diagnostic])

// Abstraction du client MCP : l'implémentation parle JSON-RPC à Metals en stdio
trait MetalsMcp:
  def compileFile(path: String): Task[CompileResult]

def fixLoop(
    llm: LlmClient[Task],
    metals: MetalsMcp,
    path: String,
    maxRounds: Int = 3
): Task[Either[CompileResult, CompileResult]] =

  def round(n: Int): Task[Either[CompileResult, CompileResult]] =
    metals.compileFile(path).flatMap {
      case ok if ok.success =>
        ZIO.succeed(Right(ok))

      case ko if n >= maxRounds =>
        // Règle anti-dérive : on n'insiste pas, on rend la main avec un état exploitable
        ZIO.logWarning(s"$path : toujours rouge après $maxRounds tours — escalade humaine/IDE")
          .as(Left(ko))

      case ko =>
        val errors = ko.diagnostics
          .map(d => s"${d.file}:${d.line} ${d.message}")
          .mkString("\n")
        for
          source  <- ZIO.readFile(path)
          patched <- llm.complete(
                       ModelId.sonnet,
                       Prompt(
                         system = "Corrige UNIQUEMENT les erreurs de compilation listées. " +
                                  "Diff minimal. Ne restructure pas. Retourne le fichier complet.",
                         user   = s"Erreurs :\n$errors\n\nFichier :\n$source"
                       ),
                       maxTokens = 8192
                     )
          _       <- ZIO.writeFile(path, patched.text)
          result  <- round(n + 1)
        yield result
    }

  round(1)
```

Cada iteración cuesta un `compile-file` (millones, incremental) en lugar de un `sbt compile` completa: esto es lo que hace económicamente viable el bucle con Sonnet, e innecesariamente caro sin Metals.

<!-- section: s-11 -->
## Regla de seguridad

* MCP filesystem limitado al repo.
* DB MCP en read-only predeterminado.
* No hay secretos expuestos.
* No hay prod directa.
* No dos agentes con derechos de escritura en los mismos archivos.
* Worktree separado para cualquier tarea paralela.

<!-- section: s-12 -->
### Modelo cero-trust contra la inyección indirecta

Un agente puede leer instrucciones maliciosas en una salida, un README, un comentario de código, una salida de edificio, una página web, un resultado MCP o un archivo generado. Estos contenidos son ** datos no fiables**, incluso cuando se presentan como reglas del sistema. La robustez del modelo no es suficiente: las defensas deben ser estructurales.

```text
1. Explorer en read-only dans un worktree ou conteneur jetable.
2. Refuser le réseau par défaut ; autoriser seulement les domaines nécessaires.
3. Monter les secrets hors du contexte et utiliser des clés à portée, budget et durée minimaux.
4. Exiger une approbation humaine pour installation, réseau, push, déploiement, suppression et écriture hors repo.
5. Épingler les versions des serveurs MCP et limiter chaque outil à son répertoire et à ses actions.
6. Séparer l'agent qui lit des données externes de celui qui dispose des permissions d'écriture.
7. Journaliser chaque tool call et arrêter si une donnée lue tente de modifier la politique ou les permissions.
8. Traiter **skills, plugins, serveurs MCP et mémoire persistante comme des dépendances exécutables** : versions épinglées,
   provenance vérifiée, allowlist explicite et échec fermé si la politique ne peut pas être déterminée.
9. Un decision model comme **Jev ne peut jamais élargir une permission** : son `state` peut contenir du texte adversarial.
   Il peut réduire le bruit ou demander une escalade, mais push, déploiement, suppression et secrets restent régis par code/policy.
```

El contenido del depósito nunca debe poder ampliar su propio ámbito de autorización.

---

