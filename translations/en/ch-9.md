<!-- section: chapter -->
# 9. Priority MCP integrations

<!-- section: s-1 -->
## Essentials

| MCP                        | Role                                                                                 |
|----------------------------|--------------------------------------------------------------------------------------|
| **Metals MCP**             | Intelligence Scala live : compile, diagnostics, types, symbols                      |
| **ScalaSemantic MCP**      | Semantic graph Scala via SemanticDB: usages, hierarchies, call pathes, Givens     |
| **JetBrains MCP**          | Exhibit IntelliJ, open files, IDE actions                                      |
| **Sourcebot**              | Multi-rest search/discovery codebase                                             |
| **Codebase-Memory MCP**    | Knowledge structural graph persistent polyglot; especially Java/Kotlin/cross-service |
| **GitHub MCP**             | Issues, PR, Actions, checks                                                          |
| **Context7**               | Updated libs documentation                                                         |
| **Playwright MCP**         | IU validation if web app                                                             |
| **Sentry MCP**             | Diagnostic bugs prod                                                                 |
| **Postgres read-only MCP** | Schematic, migration, requests                                                         |
| **ast-grep MCP**           | Structural research and targeted refactors                                           |

Operational characteristics (to be checked at the time of installation — transports and versions are changing rapidly):

| MCP                    | Typical transport               | Notable minimum version                   | June maintenance 2026                                    |
|------------------------|---------------------------------|--------------------------------------------|----------------------------------------------------------|
| Metals MCP             | stdio; standalone since 1.6.6 | Metals 1.5.3 (integrated), 1.6.6 (standalone) | Active (Scalameta)                                        |
| ScalaSemantic MCP      | MCP local                       | SemanticDB required for the heart of the index  | Young; specialised Scala, to be benchmarked on the repo      |
| JetBrains MCP          | IDE built-in server             | IntelliJ 2025.2 (server)                  | Assets (JetBrains)                                        |
| Sourcebot              | HTTP                            | —                                          | Assets                                                    |
| Codebase-Memory MCP    | MCP local                       | —                                          | Active; Hybrid LSP documented for Java/Kotlin, not Scala |
| GitHub MCP             | Remote HTTP or local stdio     | —                                          | Official assets (GitHub)                                  |
| Context7               | Remote HTTP                    | —                                          | Assets                                                    |
| Playwright MCP         | stdio                           | —                                          | Active (Microsoft)                                        |
| Sentry MCP             | Remote HTTP                    | —                                          | Active (Official Entry)                                  |
| Postgres read-only MCP | stdio                           | —                                          | Variable depending on implementation — auditer before prod     |
| ast-grep MCP           | stdio                           | —                                          | Assets                                                    |

> **Developments in the Protocol MCP to know** : **MCP 2026-07-28 is now the published reference specification**.
> The heart becomes stateleess: withdrawal of protocol level sessions, of `Mcp-Session-Id` and, for this revision,
> of the handshake `initialize` / `notifications/initialized`. Each request carries in `_meta` the information
> of which the client's version and capabilities. `server/discover` allows to discover identity, versions and
> server capabilities. The revision also formalizes the server framework **Extensions**, les **Tasks** for long work,
> the **MCP Apps**, the OAuth/OIDC aligned authorization and a depreciation policy; `Roots`, `Sampling` and
> `Logging` are depreciated. For a new development, **target 2026-07-28**, but keep compatibility tests
> 2025-11-25 until all customers/servers used are migrated. Claude Code 2.1.27x has generalized its client
> MCP v2 and negotiation 2026-07-28 to direct HTTP connections, including Bedrock, Vertex, Foundry and
> facilities
> without telemetry; a legacy mode remains. Therefore still does not assume that all peers MCP of an environment
> recent
> have migrated at the same time.

> **MCP Events remains a proposed extension, not the core of the protocol.** ChatGPT know how to experiment with subscriptions
> `events/list`, `events/subscribe` and `events/unsubscribe` with webhook delivery on servers in MCP 2.0
> [`2026-07-28`). It's useful for event workflows — created comment, incident, message, change
> the state — but does not make a critical integration dependent on this extension as long as its status and support
> Cross-border customers/servers are not stabilized.

<!-- section: s-2 -->
## ChatGPT and Codex: roles MCP not to be confused

We have to distinguish **ChatGPT web**, les **clients Codex Local** and the **Agents API**. MCP describes a customer/server relationship; the fact that a product can also expose a client/server API orchestration does not transform it into a server MCP.

| Surface                                                       | Role MCP and transport                                                                            | Authentication                                                                      | Reading / Writing                                                                          |
|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Codex CLI / IDE extension / host Codex of the ChatGPT Desktop** | **Client MCP**; Local STDIO and Remote HTTP Streamable; shared configuration on the same host | Bearer, OAuth, CIMD and DCR; `codex mcp login` for OAuth                             | Depending on server tools, sandbox and approvals; possible reading and writing |
| **ChatGPT web Pro**                                           | App Client MCP **Remote**                                                                   | OAuth according to the app                                                                     | Developer mode limited to tools `read` / `fetch`                                           |
| **ChatGPT web Business / Enterprise / Edu**                   | App Client MCP remote; **full MCP In beta**                                                | OAuth + workspace/admin controls                                                     | Reading tools and actions `write` / `modify` possible for MCP personalized        |
| **OpenAI Agents API**                                         | Client MCP hosted or from the environment; HTTP or STDIO depending on the connection origin         | Headers/Bearer, credential box or environmental variables depending on transport | `allowed_tools` allows explicitly reducing the exposed surface                          |

> **Documentation OpenAI contradictory.** The detailed Help Center maintains **Pro =
> `read`/`fetch`** and reserve the full MCP read/write to Business/Enterprise/Edu, while the developer page
> Generalist now asserts that the developer mode gives the full MCP read/write to Plus and Pro. As long as these two
> official sources do not converge, keep the above table as conservative hypothesis and ** detects the
> capabilities actually exposed by the account/workspace** before designing a writing workflow.

**Codex is no longer a server MCP.** `codex mcp-server` and binary `codex-mcp-server` The integration that wants to drive the Codex as a service must migrate to **Codex App Server**, which uses its own JSON-RPC and **is not MCP** ; Codex continues to consume servers in parallel MCP external as a customer.

ChatGPT web does not connect directly to `localhost`. For a MCP local, private or on-premise, expose it via the **Secure MCP Tunnel** Instead of open the server publicly. Two surface limitations remain important: **Agent mode does not use apps MCP personalized**, et **Deep Research** uses them only in `read` / `fetch`.

<!-- section: s-3 -->
### Manage a MCP catalog as a API versioned

When an administrator approves an app MCP] in ChatGPT, the product keeps an approved **snapshot of the tools and their inputs**. Adding, removing or modifying a tool on the server does not automatically render the new active surface. Thus, an incompatible evolution can break calls until an administrator has reviewed and republished the catalog, and ChatGPT currently does not guarantee a proactive alert about this drift.

```text
name, schema, or permission change / new MCP tool
→ surface diff
→ review
→ admin approval
→ publication
```

This **rule completes**, without replacing it, the security policy of this section: pinned versions, minimum permissions, tool logs and read/write separation.

<!-- section: s-4 -->
## Knowledge graph MCP for Scala, Java and Kotlin

**Sourcebot is not a knowledge graph.** The search/discovery layer remains: quickly find files, symbols, textual usages and relevant extracts, especially on several restitories. A knowledge graph answers another class of questions: relationships between symbols, calling paths, hierarchies, structural dependencies and the impact of a change.

<!-- section: s-5 -->
### Scala: prefer ScalaSemantic, complete with Metals

For a deposit mainly Scala, **ScalaSemantic MCP** is the best candidate identified for the "semantic graph" layer. It does not only rebuild the code from an AST Tree-sitter: its main index is powered by **SemanticDB**, by symbols already solved during the compilation. It exposes global requests adapted to agents, including exact usages, signatures, hierarchies, overloads, `call_path`, searching for Givens and tracing of illicit chains.

```text
Sourcebot
→ “Where is X?”
→ “Which files discuss Y?”

ScalaSemantic MCP
→ “What are the exact usages of this symbol?”
→ “What call path connects A to B?”
→ “What extends this trait?”
→ “Which givens can produce T?”
→ “Which implicits does this given depend on?”

Metals MCP
→ “What is the actual type here, right now?”
→ “Does this file compile?”
→ “What diagnostics does the compiler return?”
→ “Which tests fail?”
```

ScalaSemantic and Metals are **Additional**. ScalaSemantic is index-wide and excellent for global relationships; Metals remains the source of live truth for the current buffer, compiler presentation, diagnostics, compilation and tests. SemanticDB is mainly the last compiled state: if the code has just been modified without recompilation, Metals Maybe it's cooler.

Also does not present ScalaSemantic as a Neo4j/ERF: it is more precisely a **semantic code graph MCP**. Some operations remain high-level approximations and do not necessarily reproduce all the compiler logic to a specific call site. In case of contradiction on the actual resolution of a type, overload or Given, **Metals/scalac wins**.

<!-- section: s-6 -->
### Java and Kotlin: Codebase-Memory becomes much more interesting

**Codebase-Memory MCP** build a persistent knowledge graph of functions, classes, call chains, HTTP routes and cross-service links from Tree-sitter. Its second pass "Hybrid LSP" currently documents a rich resolution for several languages including **Java and Kotlin**. On these two languages, it is therefore more relevant than on Scala for structural issues of base-scale code.

```text
Java / Kotlin

Sourcebot
= search and discovery

Codebase-Memory MCP
= persistent knowledge graph
= call graph
= impact analysis
= architecture
= cross-service routes and relationships

IntelliJ / LSP
= live semantics and local verification
```

On a polyglot JVM base code, the recommended distribution becomes:

```text
Pure Scala
→ Sourcebot + ScalaSemantic + Metals

Java/Kotlin
→ Sourcebot + Codebase-Memory + IntelliJ/LSP

Scala + Java + Kotlin / microservices
→ Sourcebot
→ ScalaSemantic for Scala semantics
→ Codebase-Memory for polyglot and cross-service topology
→ Metals / IntelliJ to verify live semantics
```

The determining criterion is not "does it have a graphic basis?", but **what information creates edges** :

```text
Tree-sitter
→ syntactic structure and heuristic resolution

SemanticDB
→ symbols resolved by the Scala compiler

LSP / presentation compiler
→ live semantic state of the current code
```

For development Scala, therefore, prefers a SemanticDB edge to a reconstructed edge only from the text when both are available.

<!-- section: s-7 -->
### Effect on context engineering

This graph layer is especially useful if it avoids loading dozens of files. A read-only subagent can query ScalaSemantic or Codebase-Memory, then only trace a few paths, symbols and proofs `file:line` to the parent:

```text
impact question
→ isolated subagent
→ knowledge graph / semantic graph
→ 5–10 relevant relationships
→ verify in Metals / IntelliJ if needed
→ summary < 1–2K tokens
→ parent
```

This increases the`isolation_ratio` and directly reduces the *context rot*. On the other hand, do not activate several MCP graph by principle: benchmark them on ten real tasks and keep only those that reduce the number of files read, injected tokens or misunderstood.

<!-- section: s-8 -->
### Alternatives to know without standardizing them

`agent4s` is a toolbox Scala MCP An interesting one, based on Scalameta with SemanticDB optional, which includes references, hierarchies, dependencies and call graph. It deserves a bake-off if ScalaSemantic does not cover a class of tasks, but does not add both at once.

Joern builds a real ** Code Property Graph** very rich for security and data flow analysis, but its source frontend does not target Scala as a first-order language. Bytecode analysis JVM Scala is possible, at the cost of losing part of the source abstractions; therefore Joern reserves to specialized audits rather than the daily context of Claude Code.

<!-- section: s-9 -->
## Metals MCP : the tool Scala missing in most stacks

It's probably the MCP most underused by developers Scala. **Metals (language server) Scala) ships a server MCP since V1.5.3** (May 2025), and the **v1.6.6 "Osmium" (3 March 2026) added a server MCP standalone** which runs without an open editor — so usable directly by Claude Code or Codex CLI in terminal. This same version added the support of the **Play Twirl templates**, directly relevant to your stack.

The tools presented include: `compile-file`, `compile-full`, `compile-module`, `test`, `inspect`, `get-docs`, `get-usages`, `get-source`, `import-build`, `find-dep`, Scalafix tools, `glob-search` and `typed-glob-search`. The key tool for the loops remains **`compile-file`** : the agent writes, compiles the file, receives type/implicit errors and corrects immediately, without paying a cycle `sbt compile` complete with each iteration.

Articulation with JetBrains] MCP and ScalaSemantic:

```text
JetBrains MCP     = IDE context when IntelliJ is open (open files, inspections, run configs)
ScalaSemantic MCP = global SemanticDB relationships: usages, hierarchies, call paths, givens
Metals MCP        = live compiler feedback for terminal agents, even with the IDE closed
```

The three are complementary, not redundant. For long sessions Claude Code or tasks launched outside of IDE (CI local, parallel worktree), MetalsMCP] is the one that transforms "the agent guesses the types" into "the agent questions the compiler".

> **Versioning Metals** : **Metals 1.6.9 has been published since 14 September 2026** (after 1.6.8 of the 23 July).
> MCP, it brings the `glob-search` on all modules, the resolution of test suites between modules, the
> suggestion of`import-build` when no build target is found and a fix against error blockages
> Linking. This is directly useful for multi-module monorepos Play/sbt: take 1.6.9 as a minimum for
> Agentic loops. Miletones Metals 2 exist, but do not standardize them until a stable release.

<!-- section: s-10 -->
## Example: test-correction loop on `compile-file`

Skeleton ZIO of the loop that makes the value of Metals MCP — the agent corrects against the **compiler**, not against his own confidence, with a terminal of towers that materializes the rule "2 chess→ stop":

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

Each iteration costs one `compile-file` (milliseconds, incremental) instead of a complete `sbt compile`: this makes the loop economically viable with Sonnet, and unnecessarily expensive without Metals.

<!-- section: s-11 -->
## Safety rule

* MCP filesystem limited to repo.
* DB MCP read-only by default.
* No secrets exposed.
* No direct prod.
* Not two agents with writing rights on the same files.
* Separate worktree for any parallel task.

<!-- section: s-12 -->
### Zero-trust model against indirect injection

An agent can read malicious instructions in an issue, README, code comment, build output, web page, result MCP or a generated file. These contents are **Unreliable data**, even when they appear as system rules. Robustness of the model is not enough: defences must be structural.

```text
1. Explore read-only in a disposable worktree or container.
2. Deny network access by default and allow only the necessary domains.
3. Mount secrets outside the context and use keys with minimal scope, budget, and lifetime.
4. Require human approval for installation, network access, push, deployment, deletion, and writes outside the repo.
5. Pin MCP server versions and restrict each tool to its directory and permitted actions.
6. Separate the agent that reads external data from the one with write permissions.
7. Log each tool call and stop if any data read attempts to change policy or permissions.
8. Treat **skills, plugins, MCP servers, and persistent memory as executable dependencies**: pin versions,
   verify provenance, use an explicit allowlist, and fail closed if the policy cannot be determined.
9. A decision model such as **Jev must never expand a permission**. Its `state` can contain adversarial text.
   It may reduce noise or request escalation, but pushes, deployments, deletions, and secrets remain governed by code and policy.
```

The contents of the repository must never be able to expand its own scope of authorization.

---

