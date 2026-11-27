<!-- section: chapter -->
# 7. Scala-specific rules

<!-- section: s-1 -->
## Never let the agent do it automatically

* changing a public signature;
* modify implics, Givens, typeclasses or conversions without explanation;
* replace a specific type with `Any`, `Object`, `String` or `Map[String, Any]`;
* swallow an error with `recover { case _ => ... }`;
* make a synchronous effect blocking in a loop;
* modify `build.sbt`, plugins, versions or resolvers without prior validation and network verification;
* touch DB migrations without rollback plan;
* Simplify a domain model without a trade test;
* change the public serialization JSON.

<!-- section: s-2 -->
## To be explicitly requested

```text
Before changing Scala code:
- explain the types involved
- identify the implicits/givens in use
- identify side effects
- check existing tests
- preserve public signatures
- avoid changes to JSON serialization without a test
```

<!-- section: s-3 -->
## Post-diff Scala checklist

```text
- Does the code really compile?
- Are the imports correct?
- Do implicits/givens still resolve?
- Are error types preserved?
- Are Futures/IO/Effects non-blocking?
- Is JSON serialization unchanged?
- Do tests cover the business behavior?
- Is the diff minimal?
```

<!-- section: s-4 -->
## Mechanical refactors: scalafix before LLM

For repetitive syntax rewrites (syntax migration) Scala 2 → 3, systematic replacement of API depreciated, reorganisation of imports), **scalafix is deterministic where a LLM is probabilistic** : a rule applies identically on 500 files, without hallucination or forgetfulness. Good role sharing:

```text
LLM (Claude): write or adapt the scalafix rule
scalafix: apply the transformation across the codebase
LLM: handle cases the rule could not cover
```

It is the same logic that "deterministic safeguards beat textual instructions," applied to refactors.

A concrete example of role sharing — a syntactic rule that the LLM writes once and that scalafix applies on the whole base without drift:

```scala
package fix

import scalafix.v1.*
import scala.meta.*

// Règle générée par Claude, relue par un humain, appliquée par scalafix.
// Migration : `logger.warn(msg, exception)` (API dépréciée)
//          →  `logger.warn(exception)(msg)` (nouvelle API curryfiée)
class MigrateLoggerWarn extends SyntacticRule("MigrateLoggerWarn"):

  override def fix(implicit doc: SyntacticDocument): Patch =
    doc.tree.collect {
      case t @ Term.Apply(Term.Select(qual, Term.Name("warn")), List(msg, ex))
          if qual.syntax.toLowerCase.contains("logger") =>
        Patch.replaceTree(t, s"${qual.syntax}.warn(${ex.syntax})(${msg.syntax})")
    }.asPatch
```

```bash
# Application déterministe sur 500 fichiers, en secondes :
sbt "scalafixAll MigrateLoggerWarn"
# Puis : le LLM ne traite QUE les cas que scalafix a laissés (rapport de la règle)
```

The promptness to give LLM is not "migrating logger calls" but: *"write a rule scalafix `SyntacticRule` for this transformation, with its tests, and list the patterns that the rule will not cover"*. The cost is paid once; the application is free and reproducible.

<!-- section: s-5 -->
## Specificities Scala 3 vs Scala 2

Models LLM very often mix the two syntaxes or reinvent complex macros.

```text
- Use strict Scala 3 syntax (optional indentation, enums, extensions).
- Never create macros (inline, quoted) without prior human approval. Always prefer standard functions.
```

<!-- section: s-6 -->
## Dependency hallucination: the risk of slopsquatting

Models do not only invent version numbers: they invent **names of entire artifacts**, and attackers record these plausible names in public registers to deposit payloads. This supply-chain attack, documented as *slopsquatting*, is measured in 2026 about **19,7 %** generated code samples containing at least one hallucinated package name, with more than 200 000 unique fictitious names identified; open-weight models produce about four times as much as proprietary borders (~21,7 % against ~5,2 % — keep in mind before leaving Qwen local propose a dependency.

Derivative rules to be applied at the repo level:

```text
- every new artifact in build.sbt must exist on Maven Central BEFORE writing the change
  (verify over the network rather than relying on model memory)
- for every unknown dependency, require a first publication date and a publisher
  with an established track record
- commit lockfiles (coursier / dependencyLock) and check hashes in CI
- any agent-initiated installation outside the allowlist → human review before execution
- never let an agent resolve dependencies (sbt update) with a modified build
  until the diff has been reviewed.
```

This is the supply-chain version of the rule "check versions via Context7 / Maven Central" of section 3: the name itself is a unreliable data.

---

