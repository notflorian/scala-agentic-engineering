<!-- section: chapter -->
# 9. Vorrangige MCP-Integrationen

<!-- section: s-1 -->
## Nicht verfügbar

| MCP                        | Rolle                                                                                 |
|----------------------------|--------------------------------------------------------------------------------------|
| **Metals MCP**             | Intelligenz Scala live: kompiliert, Diagnosen, Typen, Symbole                      |
| **ScalaSemantic MCP**      | Semantische Grafik Scala via SemanticDB: Anwendungen, Hierarchien, Call Paths, Givens     |
| **JetBrains MCP**          | Ausstellen IntelliJ, geöffnete Dateien, IDE-Aktionen                                      |
| **Sourcebot**              | Suche/Discovery codebase multi-Repos                                             |
| **Codebase-Memory MCP**    | Knowledge graph persistent strukturelle polyglotte; vor allem Java/Kotlin/cross-service |
| **GitHub MCP**             | Issues, PR, Aktionen, Checks                                                          |
| **Context7**               | Dokumentation von aktuellen Libs                                                         |
| **Playwright MCP**         | I.E. Validierung, wenn Web-App                                                             |
| **Sentry MCP**             | Diagnosebugs prod                                                                 |
| **Postgres read-only MCP** | Schema, Migration, Anfragen                                                         |
| **ast-grep MCP**           | Strukturelle Forschung und gezielte Refaktoren                                           |

Betriebstechnische Merkmale (zur Überprüfung bei der Installation erforderlich, und die Versionen ändern sich rasch):

| MCP                    | Typische Beförderung               | Bemerkenswerte Mindestversion                   | Wartung Juni 2026                                    |
|------------------------|---------------------------------|--------------------------------------------|----------------------------------------------------------|
| Metals MCP             | stdio ; standalone seit 1.6.6 | Metals 1.5.3 (integrierter Text), 1.6.6 (Standalone) | Aktiva (Scalameta)                                        |
| ScalaSemantic MCP      | MCP lokal                       | SemanticDB benötigt für das Kernstück des Index  | Jung ; spezialisiert Scala, um auf der repo Benchmark      |
| JetBrains MCP          | Integrierter IDE-Server             | IntelliJ 2025.2 (Server)                  | Aktiva (JetBrains)                                        |
| Sourcebot              | HTTP                            | —                                          | Aktiva                                                    |
| Codebase-Memory MCP    | MCP lokal                       | —                                          | Aktiv; Hybrid LSP dokumentiert für Java/Kotlin, nicht Scala |
| GitHub MCP             | Remote HTTP oder lokales stdio     | —                                          | Aktiva (GitHub                                  |
| Context7               | Remote HTTP                    | —                                          | Aktiva                                                    |
| Playwright MCP         | sdio                           | —                                          | Aktiva (Microsoft)                                        |
| Sentry MCP             | Remote HTTP                    | —                                          | Aktiva (Offizielles Sentry)                                  |
| Postgres read-only MCP | sdio                           | —                                          | Variable je nach Implementierung     |
| ast-grep MCP           | sdio                           | —                                          | Aktiva                                                    |

> **Entwicklungen des Protokolls MCP zu kennen** : **MCP 2026-07-28 ist jetzt die veröffentlichte Referenzspezifikation**.
> Das Herz wird stateless: Zurücknehmen der Protokoll-Level-Sitzungen von `Mcp-Session-Id` und für diese Revision,
> von Handshake `initialize` / `notifications/initialized`. Jede Anfrage befördert in `_meta` Informationen
> erforderlich, einschließlich der Version und Fähigkeiten des Kunden. `server/discover` ermöglicht es, Identität, Versionen und
> Server-Fähigkeiten. Die Revision formalisiert auch das Framework **Erweiterungen**, les **Tasks** für die lange Arbeit,
> und **MCP Apps**, die OAuth/OIDC-Harmonisierte Genehmigung und eine Abschreibungspolitik; `Roots`, `Sampling` und
> `Logging` werden. Für eine neue Entwicklung, **Ziel 2026-07-28**, aber hält Kompatibilitätstests
> 2025-11-25 solange nicht alle verwendeten Kunden/Server migriert sind.Claude Code 2.1.27x hat seinen Kunden verallgemeinert.
> MCP v[2 und Handel 2026-07-28 mit direkten HTTP-Verbindungen, einschließlich Bedrock, Vertex, Foundry und
> Anlagen
> ohne Telemetrie ; ein Legacy-Modus bleibt. Daher geht es immer noch nicht darum, dass alle Peer MCP in einer Umgebung
> vor kurzem
> gleichzeitig migrierten.

> **MCP Events bleibt eine vorgeschlagene Erweiterung, nicht der Kern des Protokolls.** ChatGPT kann Abonnements testen
> `events/list`, `events/subscribe` und `events/unsubscribe` mit Webhook Lieferung auf Servern in MCP 2.0
> (`2026-07-28`). Es ist nützlich für Eventworkflows ✓ erstellt Kommentar, Vorfall, Nachricht, Änderung
> n deren Status und Unterstützung eine kritische Integration nicht abhängig machen
> Kreuzkunden/Server nicht stabilisiert.

<!-- section: s-2 -->
## ChatGPT und [Codex : Rollen MCP nicht zu verwechseln

Man muss zwischen **ChatGPT Web**, les **Kunden Codex Räumlichkeiten** und **Bedienstete API**. MCP beschreibt eine Kunden-Server-Beziehung; die Tatsache, dass ein Produkt auch eine API Orchestration nicht in einen Server umwandeln MCP.

| Fläche                                                       | Rolle MCP und Verkehr                                                                            | Authentifizierung                                                                      | Lesen / Schreiben                                                                          |
|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Codex CLI / IDE / Host-Erweiterung Codex von ChatGPT Desktop** | **Kunde MCP** ; Lokales und Remote Streamable HTTP-Studio; geteilte Konfiguration auf demselben Host | Bearer, OAuth, CIMD und DCR; `codex mcp login` für OAuth                             | Je nach Server-Tools, Sandbox und Genehmigungen; Lesen und Schreiben möglich |
| **ChatGPT Web Pro**                                           | App-Client MCP **distanziert**                                                                   | OAuth nach App                                                                     | Developer Modus beschränkt auf Werkzeuge `read` / `fetch`                                           |
| **ChatGPT web Business / Enterprise / Edu**                   | App-Client MCP Fernbedienungen , **full MCP beta**                                                | OAuth + workspace/admin Kontrollen                                                     | Lesewerkzeuge und Aktionen `write` /`modify` möglich für MCP benutzerdefinierte        |
| **OpenAI Bedienstete API**                                         | Client MCP gehostet oder aus der Umgebung; HTTP oder STDIO abhängig vom Ursprung der Verbindung         | Headers/Bearer, Credentialsafe oder Umweltvariablen je nach Transport | `allowed_tools` ermöglicht eine explizite Verringerung der exponierten Fläche                          |

> **Dokumentation OpenAI Widerspruch.** Das Help Center im Detail hält **Pro =
> `read`/`fetch`** und speichert den Volleyball MCP read/write bei Business/Enterprise/Edu, während die Entwickler-Seite
> Generalist behauptet jetzt, dass der Entwickler-Modus gibt den Full MCP read/write zu Plus und Pro. Solange diese beiden
> • Die offizielle Quelle ist nicht konvergierend; die obige Tabelle ist als konservative Hypothese zu betrachten und **erkennt die
> Fähigkeit, die tatsächlich vom Konto/workspace** vor dem Entwurf eines Schreibens Workflows ausgestellt wird.

**Codex ist kein Server mehr MCP.** `codex mcp-server` und Binär `codex-mcp-server` Eine Integration, die fliegen will Codex als Dienst muss zu migrieren **Codex App Server**, die ihre eigenen JSON- RPC und **ist nicht MCP** ; Codex kontinuierlich parallel zum Verbrauch von Servern MCP externe als Kunde.

ChatGPT Web nicht direkt an `localhost`. für eine MCP Lokal, privat oder on-premise, legt es über die **Secure MCP Tunnel** anstatt den Server öffentlich zu öffnen. Zwei Oberflächenbeschränkungen bleiben wichtig: **Agent Modus verwendet keine Apps MCP benutzerdefiniert**und **Deep Research** verwendet sie nur in `read` / `fetch`.

<!-- section: s-3 -->
### Katalog MCP als API versioniert verwalten

Wenn ein Administrator eine App [MCP in ChatGPT genehmigt, behält das Produkt einen genehmigten **snapshot für Werkzeuge und deren Einträge**. Hinzufügen, Entfernen oder Bearbeiten eines Tools auf dem Server macht die neue Oberfläche nicht automatisch aktiv. Eine inkompatible Evolution kann daher Anrufe brechen, solange ein Administrator den Katalog nicht überprüft und erneut veröffentlicht hat, und ChatGPT garantiert derzeit keine proaktive Warnung über diese Abweichung.

```text
changement de nom / schéma / permission / nouvel outil MCP
→ diff de surface
→ review
→ validation admin
→ publication
```

Diese Regel ** ist vollständig**, ohne sie zu ersetzen, die Sicherheitspolitik dieses Abschnitts: epinguierte Versionen, minimale Berechtigungen, Werkzeuglogs und Trennung Lesen/Schreiben.

<!-- section: s-4 -->
## Knowledge graph MCP für Scala, Java und Kotlin

**Sourcebot ist kein Knowledge Graph.** Es bleibt die Such-/Discovery-Schicht: schnell wieder Dateien, Symbole, Text- und Auszüge finden, vor allem auf mehreren Repositorien. Ein knowledge graph beantwortet eine andere Kategorie von Fragen: Beziehungen zwischen Symbolen, Anrufpfade, Hierarchien, strukturelle Abhängigkeiten und Auswirkungen einer Veränderung.

<!-- section: s-5 -->
### Scala: bevorzuge ScalaSemantic, vervollständigen mit Metals

Für ein Depot hauptsächlich Scala, **ScalaSemantic MCP** ist der beste Kandidat für die ✓ semantische Graph-Schicht. Er baut nicht nur den Code aus einem AST Tree-Sitter um: sein Hauptindex wird durch **SemanticDB**, also durch Symbole, die bereits bei der Zusammenstellung gelöst wurden. Es enthält umfassende Anfragen, die an die Agenten angepasst sind, insbesondere genaue Verwendung, Unterschriften, Hierarchien, Overloads, `call_path`, Suche nach Givenen und Verfolgung von Vereinfachungsketten.

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

ScalaSemantic und Metals sind **Ergänzungen**. ScalaSemantic ist index-wide und ausgezeichnet für globale Beziehungen; Metals bleibt die Quelle der Live-Wahrheit für das aktuelle Buffer, das Kompilieren, Diagnosen, Kompilation und Tests. SemanticDB stellt vor allem den letzten kompilierten Zustand dar: wenn der Code geändert wurde, ohne erneut zu repilieren, Metals kann kühler sein.

ScalaSemantic auch nicht als Neo4j/RDF: Dies ist ein allgemeinerer **semantic code graph MCP**. Einige Operationen sind nach wie vor hochgradig annähernd und reproduzieren nicht unbedingt die gesamte Logik des Compilers an einer bestimmten Call-Site. Im Falle eines Widerspruchs bei der tatsächlichen Auflösung eines Typs, Overload oder Given, **Metals/scalac gewinnt**.

<!-- section: s-6 -->
### Java und Kotlin: Codebase-Memory wird viel interessanter

**Codebase-Memory MCP** Erbaut ein permanentes Knowledge-Graph von Funktionen, Klassen, Call-Strings, HTTP-Routen und Cross-Service-Links von Tree-Sitter. Sein zweiter Pass ✓ Hybrid-LSP ✓ dokumentiert derzeit eine bereicherte Auflösung für mehrere Sprachen, darunter **Java und Kotlin**. In beiden Sprachen ist es daher relevanter als in Scala für strukturelle Fragen des Base-Scale-Codes.

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

Bei einem Polyglottencode JVM wird die empfohlene Verteilung wie folgt:

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

Besteht das entscheidende Kriterium nicht in einer Graphenbasis ? **Welche Information erzeugt die Kanten[**:

```text
Tree-sitter
→ structure syntaxique et résolution heuristique

SemanticDB
→ symboles résolus par le compilateur Scala

LSP / presentation compiler
→ état sémantique live du code courant
```

Für die Entwicklung Scala zieht daher eine SemanticDB-Kante nur aus dem Text zurück, wenn beide verfügbar sind.

<!-- section: s-7 -->
### Auswirkungen auf das context engineering

Diese Grafik-Schicht ist vor allem nützlich, wenn sie das Laden von Dutzenden von Dateien vermeidet. Ein read-only Subagent kann ScalaSemantic oder Codebase-Memory befragen und dann nur einige Pfade, Symbole und Beweise `file:line` an den Eltern zurückverfolgen:

```text
question d'impact
→ subagent isolé
→ knowledge graph / semantic graph
→ 5–10 relations pertinentes
→ vérification Metals / IntelliJ si nécessaire
→ résumé < 1–2K tokens
→ parent
```

Dies erhöht die`isolation_ratio` und reduziert direkt die *Kontext rot*Dagegen werden nicht mehrere MCP Prinzipiell Graphen: benchmarke sie auf zehn wirklichen Aufgaben und behalte nur diejenigen, die die Anzahl der gelesenen Dateien, injizierten Tokens oder Verständnisfehler reduzieren.

<!-- section: s-8 -->
### Alternatives zu kennen, ohne sie zu standardisieren

`agent4s` ist eine interessante toolbox Scala MCP, basierend auf Scalameta mit optionaler SemanticDB, die unter anderem Verweise, Hierarchien, Abhängigkeiten und Call Graph beschreibt. Sie verdient ein Bake-off, wenn ScalaSemantic nicht eine Aufgabenklasse abdeckt, aber nicht beide von vorne hinzufügt.

Joern baut ein echtes **Property-Graph-Code** sehr reich an Sicherheits- und Daten-Flow-Analyse, aber seine Frontend-Quelle nicht zielen Scala als erste Sprache. Die Analyse des Bytecode JVM Scala • die Möglichkeit, einen Teil der ursprünglichen Abstraktion zu verlieren; Claude Code.

<!-- section: s-9 -->
## Metals MCP: das fehlende Werkzeug Scala in den meisten Stacks

Es ist wahrscheinlich das MCP die am häufigsten verwendeten Entwickler Scala. **Metals (Language server Scala) nimmt einen Server mit MCP seit v1.5.3** (Mai 2025) und **v1.6.6 Osmium (3 März 2026) fügte einen Server hinzu MCP Standalon** die ohne offenes Editor läuft  ✓ damit direkt von Claude Code oder Codex CLI im Terminal. Dieselbe Version hat die Unterstützung der **Play-Twirl-Tmplates**, direkt relevant für deinen Stack.

Die vorgestellten Instrumente umfassen insbesondere: `compile-file`, `compile-full`, `compile-module`, `test`, `inspect`, `get-docs`, `get-usages`, `get-source`, `import-build`, `find-dep`, Scalafix-Werkzeuge, `glob-search` und `typed-glob-search`. Das Schlüsselwerkzeug für die Agentenschleifen bleibt **`compile-file`** : Schreibagent, kompiliert die Datei, empfängt die Fehler der Typen/Vereinfachungen und korrigiert sofort, ohne einen Zyklus zu bezahlen `sbt compile` die für jede Iteration vollständig sind.

Verbindung mit JetBrains MCP und ScalaSemantic:

```text
JetBrains MCP     = contexte IDE quand IntelliJ est ouvert (fichiers ouverts, inspections, run configs)
ScalaSemantic MCP = relations globales SemanticDB : usages, hiérarchies, call paths, givens
Metals MCP        = feedback compilateur live pour les agents terminal, même IDE fermé
```

Alle drei sind komplementär, nicht redundant. Bei langen Sitzungen Claude Code oder außerhalb von IDE gestarteten Aufgaben ([CI lokal, paralleler Worktree), Metals MCP ist derjenige, der die Typen ahnt, die vom Agenten in die Gruppe der Compiler befragt werden.

> **Formatierung Metals** : **Metals 1.6.9 wird seit dem 14 September 2026** (nach 1.6.8 vom 23 Juli).
> MCP, bringt sie [`glob-search` auf alle Module, Auflösung der Test-Suiten zwischen Modulen,
> Vorschlag von[`import-build`, wenn kein build Ziel gefunden wird und ein Patch gegen Fehlerblockaden
> Das ist direkt nützlich für Monorepos Play/sbt Multimodule: Nimm es ein 1.6.9 als Minimum für
> Milestones Metals 2 sind vorhanden, standardisieren sie aber nicht vor einer stabilen Release.

<!-- section: s-10 -->
## Beispiel: Agentic Correktion Test-Schleife auf `compile-file`

Skelett ZIO der Schleife, die den Wert von Metals MCP Der Bedienstete hat gegen den **Compiler**, nicht gegen sein eigenes Vertrauen, mit einer Türme-Klammer, die die Regel  ✓ materialisiert 2 Fehler → stop:

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

Jede Iteration kostet eine `compile-file` (Millisekunden, Inkremental) anstelle einer vollständigen [`sbt compile`]: Dies macht die Schleife wirtschaftlich lebensfähig mit Sonnet, und unnötig teuer ohne Metals.

<!-- section: s-11 -->
## Sicherheitsvorschriften

* MCP filesystem beschränkt auf repo.
* Standardmäßig DB MCP in read-only.
* Keine Geheimnisse.
* Kein direktes Produkt.
* Nicht zwei Agenten mit Schreibrechten auf dieselben Dateien.
* Getrennte Worktree für jede parallele Aufgabe.

<!-- section: s-12 -->
### Null-trust-Modell gegen indirekte Injektion

Ein Agent kann bösartige Anweisungen in einem Ausgabe, einem README, einem Codekommentar, einem Build-Ausgang, einer Webseite, einem Ergebnis lesen MCP oder eine generierte Datei. Diese Inhalte sind **Unzuverlässige Daten**, selbst wenn sie als Systemregeln auftreten. Die Robustheit des Modells reicht nicht aus: die Verteidigung muss strukturell sein.

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

Der Inhalt des Depots darf niemals seinen eigenen Umfang der Genehmigung erweitern.

---

