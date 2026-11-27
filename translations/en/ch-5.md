<!-- section: chapter -->
# 5. Standard workflow for a Scala business task

<!-- section: s-1 -->
## Step 0: Human scoping

Before AI, you write or clarify:

```text
Objectif :
Comportement actuel :
Comportement attendu :
Contraintes métier :
API publique à préserver :
Fichiers probablement concernés :
Tests ciblés :
Validation harness :
Risque :
Critère d'acceptation :
```

Numbers important business requirements and invariants ([`REQ-01`], `REQ-02`, etc.). For each requirement, declares the test or proof expected before implementation; a requirement without oracle must be explicitly marked uncovered and arbitrated. In the PR, combines requirement, command/test, result, validated SHA and limits of proof. The traceability matrix may remain very short for a trivial ticket.

`Validation harness` must appoint **before the write mode** proof that the agent can perform itself: targeted compilation, unit testing/integration, ScalaCheck, scalafmt, possibly Stryker4s If you still don't know how to prove that the change is correct, the task is not ready to be delegated.

Without that, you pay the models to find out the problem instead of solving it.

> **Positioning vs. state of the art 2026 ("Spec-Driven Development")** : this framing is exactly what
> the industry has formalised under the name of SDD, become the dominant counterweight to "vibe coding" — spec as
> The most profitable artifact produced by humans when the agent writes the code. The tooling (GitHub] Spec Kit, OpenSpec,
> AWS Kiro, EARS notation for testable requirements) can structure this workflow, but is not mandatory: this
> already practical guide the variant **spec-anchored** (the spec frames and survives the task, the code + tests remain
> the source of truth), which is the recommended posture for the existing trade code — as opposed to the
> **spec-as-source** (human only edits spec), which is still experimental.
> field: the level of detail of the spec must follow the * criticality* of the code — over-specifying a disposable script is
> of waste, under-specifying a public contract is a guaranteed drift.
>
> **Choose a tooling SDD without framework-sprawl.** The landscape SDD
> Now more than thirty frameworks ([Spec Kit], OpenSpec, Kiro, BMAD-METHOD, GSD, Tessl...).
> The following practices emerge: **GitHub Spec Kit** for greenfield (constitution → specify → clarify → Plan →
> checklist → tasks → analyze → implementation → converge, with optional control steps);
> **OpenSpec** for iterative brownfield — specs versioned in the repo with *delta marketers* by change, the
> closest posture to the spec-anchored variant of this guide; **AWS Kiro** if you want the integrated EARS notation
> and the AWS ecosystem. None is a prerequisite: if `AGENTS.md` + the above framing package + the gates CI
> (section 15A) already do the work, adding a framework SDD adds context, not quality.
> negotiable: spec lives in the repo and looks like code — a spec held out of version becomes a second
> source of truth diverges.

> **Two Harnesses Not to Be Confound.** A Paper SDD published on 31 August 2026 offers a useful distinction between
> **technical harness** (model, tools, context, permissions, tests) and **Methodological Harness** (spec, roles,
> This vocabulary **confirms** the structure of this guide:
> Claude Code, Codex or MCP does not replace the discipline of specification and human validation.
> However, mainly conceptual and largely based on grey literature; uses this distinction
> as a design framework, not as empirical evidence that a given framework SDD improves productivity.

> **First Real Practice Data.** The CMU/Google Study "Spec-Driven Development as Prescribed
> and as Practiced" noted that experienced practitioners already apply the SDD
> **selective way, especially for new features or risky changes**, with specs written by agents from an intention
> The main flaw is that of the human being, and then read again, and a check mainly by tests written by agents.
> **silent drift spec ↔ code** when no maintenance plan exists; Thoughtworks returns add
> the [*] instruction bloat* (specs and context that grow until the agent loses the thread).
> rules of this guide: criticality dosing, and versioned and reviewed spec. Adds only a third rule:
> **a test written by the agent does not validate its own spec**; keeps the reproductive test that fails before the patch
> and the mutation testing (section 5], step 4). In the tooling, **`/speckit.converge`** rereads the code against
> `spec.md`, `plan.md` and `tasks.md` and **adds only missing tasks to `tasks.md`**. It is a control of
> useful consistency after implementation, **not an oracle**: neither independent tests nor human review should
> be deleted on the pretext that Spec Kit announces "Converged".

<!-- section: s-2 -->
#### Operational spec template (copy-paste)

This template materializes the spec-anchored variant of the guide. It lives in the repo (e.g. `specs/TICKET-123.md`) and looks like code.

<!-- section: s-3 -->
# SPEC: [TICKET-123] — [Short title]

<!-- section: s-4 -->
## 1. Objective (1 sentence, action verb)

[Ex: "Add a quantity-level discount rate to the DiscountService"]

<!-- section: s-5 -->
## 2. Non-objectives (explicit, anti-driving)

- [Ex: "Do not modify the existing discount calculation by promo code"]
- [Ex: "Do not touch the publicAPI of the charging module"]

<!-- section: s-6 -->
## 3. Expected behaviour (business rules, numbered)

1. [Rule 1 : if quantity >= 10, remise 5%]
2. [Rule 2 : if quantity >= 50, remise 12%]
3. [Rule 3: bearings do not cumulate, the highest applies]

<!-- section: s-7 -->
## 4. Technical constraints

- API public to be preserved: [accurate signatures]
- Serialization JSON: [unchanged / add field X with backward compass]
- Performance: [no additional DB request in hot path]
- Competition: [immutable / atomity required]

<!-- section: s-8 -->
## 5. Files probably affected

- `src/main/scala/.../DiscountService.scala`
- `src/test/scala/.../DiscountServiceSpec.scala`

<!-- section: s-9 -->
## 6. Acceptance tests (done criteria)

| Requirement/invariant | Expected evidence |
|----------------------|-----------------|
| REQ-01: threshold 10 | Unit test: 9 → 0 %, 10 → 5 % |
| REQ-02: threshold 50 | Unit test: 49 → 5 %, 50 → 12 %; property reset ≤ 12 % |
| REQ-03: non-cumulative | Non-regression test on cumulation; discount by unchanged promo code |
| REQ-04: contract JSON | Compatibility test |
| REQ-05: performance | Measurement of the number of DB queries on the integration scenario |

- [ ] Testing mutation: score / important mutants to justify on affected files
- [ ] SHA and Requirements Results; Explicit Exceptions and Residual Risk

<!-- section: s-10 -->
## 7. Risks and mitigations

| Risk               | Probability | Impact | Mitiation                      |
|----------------------|-------------|--------|---------------------------------|
| [Arrondi BigDecimal] | Medium       | Top   | [Use RoundingMode.HALF_UP] |

<!-- section: s-11 -->
## 8. Definition of done (final blacklist)

- [ ] Compile without warning
- [ ] Green Targeted Tests
- [ ] scalafmtCheckAll passes
- [ ] Review second model completed
- [ ] Diff < [N] lines
- [ ] No files off-scope modified

Level of detail adapted to criticality:

- Disposable Script → sections 1, 2, 6 suffice
- Public contract / money / security → all mandatory sections

---

<!-- section: s-12 -->
## Step 1: Targeted Search

Use in this order:

1. **Sourcebot** to locate files, uses, tests.
2. **IntelliJ** to check symbols, types, hierarchies.
3. **Context7** if an external API or a recent version is involved.
4. **Qwen local** to produce a briefing.

Prompt Qwen:

```text
Analyse ces fichiers et produis :
- résumé du flux métier
- classes et méthodes impliquées
- invariants à préserver
- tests existants
- risques
- ambiguïtés
- prompt propre à donner à Claude Code

Ne propose pas encore de patch.
```

---

<!-- section: s-13 -->
## Step 2: plan by the writer, without modification

Prompt writer (Codex] or Claude Code):

```text
Tu es l'agent writer de cette tâche.

Objectif :
[objectif]

Contraintes :
- diff minimal
- pas de changement d'API publique sans validation explicite
- préserver les comportements existants
- ajouter ou adapter les tests
- procéder par petites étapes
- expliquer les risques
- ne rien modifier avant validation

Commence par explorer le code et proposer un plan.
```

Document rule: **No plan, no write mode**. The plan must list the files to be modified, the files to be left blank, the test strategy, the risks and the expected size of the diff.

---

<!-- section: s-14 -->
## Step 3: small diff implementation

Prompt:

```text
Exécute uniquement l'étape 1.
Ne touche pas aux autres étapes.
Garde le diff minimal.
Après modification, donne :
- fichiers modifiés
- raison de chaque changement
- commande de test ciblée
```

For Scala, avoid the large automatic refactors. Request lots of 30 à 300 Diff lines when possible. Field returns and recent studies on the PRs converge to small, narrow PRs, easier to read and less prone to failure CI. At the organizational level, the study of deployment Claude Code / Copilot CLI at Microsoft (arXiv, July) 2026, tens of thousands of engineers) measures ~24% of PRs mixed more among adopters — the effect is real, but it materializes in PRs *Reviewable*, not in giant diffs.

---

<!-- section: s-15 -->
## Step 4: validation IntelliJ + tests

Agents LLM are known to write "happy path" tests (tests that pass but do not check error cases or limits). Scala/SBT :

```text
scalafmtCheckAll
compile
Test / compile
testOnly <TestCiblé>
IntegrationTest / testOnly <TestCiblé>
```

Then only if the risk justifies it:

```text
test
IntegrationTest / test
```

> **Note sbt :** configuration `IntegrationTest` is **depreciated since sbt 1.9.0** for a sub-project
> dedicated (e.g. a module `it`] that `dependsOn(core % "test->test")`) or tagged tests. If your project uses it
> again, the above commands remain valid, but never let an agent migrate this configuration on its own —
> It is exactly the kind of change `build.sbt` that must go through explicit validation. On a new
> module,
> go directly to a sub-project `it`. Also think about giving the agent the fastest available order:
> `sbt --client` (or Bloop) avoids paying for the start of JVM at each iteration of the test-correction loop, this
> who
> can speed up the actic loops. **sbt 2.x**, `sbt` already uses the native client-server mode `sbtn`
> default; `sbt --client` is still an explicit form. Measuring the start on the real project: migration 1.x → 2.x
> and change of `build.sbt` require human validation (see section 15A).
>
> If `serverConnectionType` is configured to `Tcp`, sbt 1.4.0 à 2.0.6 is
> vulnerable to unauthenticated code execution via BSP. Removes this setting or moves at least to **sbt 1.13.0
> or 2.0.7**. The default local transport (Unix socket or named pipe) is not affected. This update is
> prior to exposing the sbt server to a remote IDE, agent or container.

<!-- section: s-16 -->
#### Optimizations sbt for the agent loops

The speed of the compile-test loop is the first agent productivity lever. Configuration recommended in `.sbtopts` (repo):

<!-- section: s-17 -->
# .sbtopts — optimised for activating loops

```text
-J-Xms2g
-J-Xmx8g
-J-XX:+UseZGC
-J-XX:+UseStringDeduplication
-Dsbt.supershell=false
-Dsbt.color=false
-Dsbt.log.noformat=true
```

Explanation of choices:

- `UseZGC` : option to be measured against the G1 default on the actual deposit; do not promise a systematic gain or breaks always less than 1 ms
- `supershell=false`] and `color=false`: reduces noise in exits parsed by the agent (less tokens, less context rots)
- `noformat=true`: Idem, rough outputs easier to parse

Under sbt 2.x, `sbt` already launches the default native client; `sbtn` remains a useful explicit entry:

<!-- section: s-18 -->
# First launch (start server)

`sbt`

<!-- section: s-19 -->
# Subsequent calls from the agent (almost instant start)

`sbtn "compile"` `sbtn "testOnly *DiscountServiceSpec"`

Configuration of the server in `project/server.sbt`:

```scala
// Keep the build server on a local transport.
Global / serverConnectionType := ConnectionType.Local
```

Local transport is normally the default: **does not expose the server sbt in TCP** to speed up the agents. `build.sbt` only to hide recompilations or checks: `onChangedBuildSource := IgnoreSourceChanges`, `Test / fork := false` and the deactivation of Scaladoc may render the result unrepresentative of the CI or modify test behaviors. Prefers to target module and suites (`project`, `testOnly`) without altering their semantics. **sbt 2.x, `test` is incremental and can reuse its results in cache** : uses `testFull` for a complete validation before a PR or in CI.

**Benchmark before/after on your deposit.** Compare to JVM and identical options, on at least ten incremental compilation cycles + targeted tests: median latency, p95, restarts sbt, memory pressure and stability of tests. Does not present a cost saving on another project as a guarantee.

For Play Framework or multi-module projects:

```text
sbt "project api" compile
sbt "project api" "testOnly *DiscountServiceSpec"
sbt "project integration" "testOnly *OrderFlowSpec"
```

The main point remains: do not only ask AI to be cautious, run tests. Determinist safeguards beat textual instructions.

Choose validations based on real risk, without stacking unnecessary tools:

| Risk Scala/JVM | Relevant evidence |
|------------------|-------------------|
| Business calculation | ScalaCheck, limits, mutation testing |
| Binary compatibility / TASTy | MiMa / TASTy-MiMa when relevant |
| REST / JSON | Contract testing, schematics and compatibility |
| Competition and effects | Controlled order, cancellation, timeout, resource release |
| Spark | Deterministic datasets, nulls, schematics, partitions, idealism |
| Performance JVM | JMH or reproducible target benchmark |
| Architecture | Scalafix / fitness functions on bytecode or sources |
| Security | SAST actually covering Scala, SCA, secret scanning and authorisation tests |

**CodeQL Java/Kotlin does not prove a cover Scala** : Checks the list of supported languages and tests the selected analyser on known defects. Do not assign a dependency scanner to a source analysis.


<!-- section: s-20 -->
### Provident value of tests generated

A test written by the same agent as the implementation is not an independent oracle. Recent work finds that agents frequently produce observation or printing tests without discriminant assertions; increasing the number of tests by the prompt is not enough to improve the resolution rate. Other mutation evaluations show that green suites do not detect realistic defects generated by agents, and that their effectiveness deteriorates even when the code evolves without expected semantic change.

For a bugfix, keep the most profitable proof:

```text
1. ajouter un test de reproduction minimal ;
2. vérifier qu'il échoue sur le commit de base pour la bonne raison ;
3. appliquer le patch ;
4. vérifier que ce test puis la suite pertinente passent ;
5. faire varier l'oracle : propriétés, cas limites, tests métamorphiques ou mutants ciblés ;
6. faire relire le test avant l'implémentation lorsque le domaine est critique.
```

Do not set a universal mutation threshold that would encourage "play the metric." Compares the score on the affected perimeter, requires a justification for each major surviving mutant and is mainly the **delta of mutation score**, escaped regressions and review returns. A test that could not fail before the patch does not prove the fix.

**The Hardening Stage (Mutation Testing):** Once the AI has written the tests and they are green, validates their robustness with Stryker4s:

```text
sbt "project api" stryker
```

A low score **can** reveal insufficient tests, but also equivalent mutants, irrelevant or poorly targeted. First examine the surviving mutants, their business impact and exclusions; do not add artificial assertions to increase the score. If an important mutant remains alive, return the report to the agent by asking for an **test of observable behavior independent of the patch**, then restart the targeted tests.

---

<!-- section: s-21 -->
#### Step 5: Force verification before declaration of completion

The agents LLM frequently declare "done" without having checked. Add this systematic instruction at the end of each implementation prompt:

Before declaring this task completed, you MUST:

1. Run compilation command and show result
2. Run the targeted test and show the result
3. Check the diff from the approved database, committed and uncommitted changes, and untracked files
4. List modified files with reason for each change
5. If a step fails, correct and repeat from 1 Do not say "done" unless the 5 points above are satisfied.

To automate these checks, use the common scripts in section 5] (hooks) and section CI 15A. The hook `PostToolUse` compiles only: `Test/compile` does not run the tests. The results of the suites and the full diff must be associated with the candidate SHA, and the CI must repeat the validation independently. A stop hook is not proof of completion; it must not prevent a stop for blocking.

Variant for critical tasks (security, money, public contract):

Before declaring this task completed, perform and show:

1. sbt compile (zero error, zero warning new)
2. sbt "testonly *SpecFiblé" (all green)
3. sbt scalafmtCheckAll (conforming formatting)
4. Diff base → candidate and full status Git (only plan files)
5. Check that the diff does NOT contain: TODO, FIXME, debug println, unused import, change of public signature not requested Shows the result of each step. If a step fails, corrects and repeats. Do not declare "done" before the 5 steps are green.

---

<!-- section: s-22 -->
## Step 6: self-review by the writer

Prompt:

```text
Fais une review de ton propre diff avant de le transmettre au reviewer indépendant.
Liste :
- risques métier
- cas limites
- tests manquants
- changements inutiles
- fichiers à relire manuellement
- hypothèses que tu as faites
```

This step often removes obvious errors before external review. **It is never worth approval**: the agent who wrote the diff shares the same assumptions as its implementation and cannot constitute the final gate. The writer can clean up; a fresh context of **the other family of models** must provide his independent findings. Human agrees.

---

<!-- section: s-23 -->
## Step 7: independent review by the other model family

Prompt reviewer: **Opus 5.5 Medium** if Codex has written; **GPT‑6.2 Sol Medium** if Claude has written. Go to High for a risky PR and to Astra Light/Fable Low only if the additional capacity is justified:

```text
Act as an independent senior Scala/JVM code reviewer.

Review the exact PR head SHA against its merge base, approved specification, acceptance criteria and AGENTS.md.
Work in a fresh read-only session; do not modify the implementation. Do not rely on the writer's reasoning
until you have formed your own assessment.

Prioritize functional correctness, preserved invariants, regressions, compatibility, test oracle quality,
error handling, resource safety, concurrency, performance, security and scope violations.

For every actionable finding, provide severity, file/line, reviewed SHA, violated requirement or invariant,
a concrete failure scenario or reproduction, the smallest plausible correction, and remaining uncertainty.
Distinguish verified defects from hypotheses. Ignore stylistic preferences and unrelated refactoring.
Do not invent findings. Return a concise verdict and evidence-backed findings only.
Never approve or merge the PR yourself.
```

Variant with machine-operational severity classification — preferred for sorting and a gate powered only by independently validated findings (see the example of decoding typed in section 12):

```text
Classe chaque retour avec exactement un de ces labels :
- BLOCKING        : bug métier, perte de données, faille, contrat public cassé
- REGRESSION_RISK : comportement existant potentiellement altéré, cas limite non couvert
- STYLE           : lisibilité, convention, nommage — jamais bloquant
- OUT_OF_SCOPE    : amélioration valable mais hors ticket — à ignorer dans cette PR

Retourne uniquement du JSON valide :
{
  "findings": [ { "severity": "...", "file": "...", "message": "..." } ],
  "summary": "..."
}
```

The associated gate rule: `BLOCKING`] and `REGRESSION_RISK` must be treated or explicitly challenged before merge; `STYLE` is optional; `OUT_OF_SCOPE` leaves in the backlog, never in the current diff.

These labels remain **review assumptions**, not facts. Each blocking return must bear verifiable proof: file and line, contract breached, reproduction, test failure or precise static rule. Without proof, it goes into human sorting; the self-label of a model must never block a merge alone. This validation avoids costly false positives and loops "author IA ↔ Review IA" that burn credits without new information.

The recommended pattern remains: **a writer, a reviewer of the other family**. Cross-examination is a working hypothesis, not a guarantee: a study *Cross-Model LLM Code Review* on 116 algorithmic problems with Opus 4.7 / GPT-5.5 observed a gain Codex → Claude (71,6 → 89,7 % success) and a drop Claude → Codex (91,4 → 82,8 % o the program is rewritten by the reviewer without performing the tests; Scala. The reviewer detects and justifies ; the writer corrects after sorting. Measures the true/false positives, missed defects and regressions introduced by the corrections. After a minor correction, targeted re-review of changes and invariants; complete review only if the risk or scope has changed.

> **Effort and limits of the review.** On 90 Django patches, a study *How Much Effort Does an AI Code Reviewer
> Need?* finds Opus 5.5 Medium not lower than High in a predefined margin of 15 points, at an average cost
> less than about 20 % Even High accepts 45 % of patches considered incorrect by the reinforced oracle; some
> labels remain questionable. CR-Bench-v2 (584 reviewable defects associated with PRs) confirms that coverage
> These results reinforce Medium for everyday life, but do not prove that the
> the universal equivalency Medium/High and the effectiveness of current models on Scala. No autonomous gate LLM.

 By default: **Sol 6.2 Medium written → Opus 5.5 Medium review**, ou **Opus 5.5 Medium/High written → Sol 6.2 Medium review**. Luna/Haiku are used for mechanical tasks; Astra/Fable are only mobilized in escalation. `Ultra` remain reserved for missions decoupable in independent axes.

---

<!-- section: s-24 -->
## Step 8: Targeted correction

You never ask the reviewer to automatically apply all his suggestions. You select useful returns, then you go back to the original **writer**:

```text
Voici les retours de review que je valide :
[liste]

Corrige uniquement ces points.
Ignore les suggestions optionnelles.
Garde un diff minimal.
Relance les tests ciblés.
```

**Stops the revision when the criteria are green.** A corrective pass after review is the default; a second is only justified by a finding `BLOCKING` / `REGRESSION_RISK` Do not use a "iterary" type of prompt until it is perfect: beyond the best checkpoint, the agent often ends up inventing changes to satisfy the demand and can degrade the diff.

If a new pass is required, systematically compares the new diff to the previous checkpoint and keeps the version that best satisfies **spec + tests + scope**, not the most recent version.

If you delegate the post-PR correction to Codex (Goal mode, Heartbeat or Cloud), `/steward` or PR Steward (section 12), explicitly transfer ownership of the branch, with the starting SHA, spec and only allowed returns. Stop monitoring it before any resumption by the original writer. Any new commit revives the relevant validations; the independent review should focus on the final diff, not on the SHA before the automatic correction.

<!-- section: s-25 -->
## Step 9: anti-driving safeguards

Add explicit shutdown rules, reduce unnecessary diffs, correction loops and burned credits:

```text
Stop immédiat si :
- l'agent touche un fichier hors plan sans explication ;
- l'agent modifie build.sbt, plugins.sbt, resolvers ou versions sans validation explicite ;
- la même erreur de compilation revient 2 fois ;
- les tests ciblés échouent 2 fois avec des causes différentes ;
- le diff dépasse la taille annoncée ;
- le correctif commence à changer l'architecture au lieu de résoudre le ticket.
- l'agent tente une écriture destructrice, un push, un déploiement, un partage externe ou une action sur des secrets
  qui n'étaient pas explicitement autorisés.
```

In this case, don't restart it. Ask instead:

```text
Stop. Résume l'état exact :
- fichiers modifiés
- hypothèses faites
- erreur actuelle
- commandes exécutées
- prochaine action minimale proposée
Ne modifie rien.
```

> **Resuscitate without paying twice for the same exploration.** Three mechanisms Claude Code to know:
>
> - **Checkpoints**: each prompt creates a checkpoint (snapshot of files before each edition by the tools of
>   Claude). `Échap Échap` or `/rewind` restores the conversation, code or both to an earlier point, including
>   after closing the terminal. Known limit: only changes made via Claude's editing tools
>   are followed, not those launched in Bash — a checkpoint does not replace a commit or worktree.
> - **`/compact` Don't wash a bad hypothesis** : the compaction sums up the conversation and *preserved* so
>   the wrong hypothesis that the model repeats. When the agent returns twice to the same false track, the parade is
>   `/clear` then a quick tightened with the new state — not an additional compaction.
> - **Permissions in Deny-by-default** : `settings.json` accepts rules allow / ask / deny; combines aallowlist
>   narrow with explicit deny (network, critical files, push) rather than hand-in-loop approval.
>   This is the product version of the non-automatic rules of the 3 section.
> - **Auto default mode** : since the 14 August 2026, auto mode is the default permission mode for news
>   sessions on Pro, Max and Team plans. Its classifier reduces interruptions, but it's not a gate
>   trade: make sure your rules `deny` on `build.sbt`, migrations, workflows CI and push remain active (the
>   *hard deny rules* of auto mode block without taking into account exceptions `allow`), and keep the hooks below.

<!-- section: s-26 -->
#### Claude Mods : when to exceed the classic hooks

Since **Claude Code 2.1.287**, one **Mod** is a plugin whose JavaScript/TypeScript handlers run in the process Claude Code. A handler may **observe, rewrite or support** an event: tool call, prompt, turn, command or render interface. It is a different layer of MCP : one MCP provides tools from an external process/service; a Mod can change the behavior of the harness itself. **3 October 2026**, the version 2.1.288 add already `$.ui.selection()` and several Mods/plugins patches: therefore treats this API as **young and evolving**, and pin the version Claude Code for any Mod that becomes critical in your workflow.

| Need                                                                                                 | Preferential |
|--------------------------------------------------------------------------------------------------------|----------------------|
| Repeat instructions/method                                                                 | **Skill**            |
| Provide access to an external system or tool                                                        | **MCP**              |
| Block, authorize or log an event with a simple rule                                        | **Settings hook**    |
| Interactive UI, event-shared status, local command, event interception/rewrite | **Mod**              |

The Mods API can save commands, tools and subagents, call a template, read the status and usage of the session, keep a shared store, read/write files, run a process, call HTTP or a MCP, and communicate with other sessions. Mods work with their hooks in the terminal — including the built-in terminal and plugin JetBrains — as well as in Claude Desktop's Tab Code; the UI elements are not returned on all headless/cloud surfaces.

**Do not replace the three shell hooks below with a Mod only because it is possible.** For simple and deterministic gates (`build.sbt`, migrations, max diff, mandatory tests), a setting hook remains smaller, more readable and easier to audit. Use a Mod only if you need cross-event status, an IU, an interactive workflow or an intercept that the classic hook expresses poorly.

> **A much wider trusted border.** A Mod runs with the rights of your user, can read the
> quick, tool calls, environment variables and settings, start processes or network, rewrite a
> query and spend quota via model calls. The processes that it starts are **outside the sandbox Bash** of
> Claude.
> An installed Mod can also approve some tool calls that a `ask` rule or `PreToolUse` user would have
> Stopped.
> Claude permissions therefore do not constitute a sandbox around the plugin code.

Before installing or promoting a Third Party Mod:

```text
1. Vérifier la source du marketplace et figer la version/commit quand c’est possible.
2. Lire .claude-plugin/plugin.json, hooks/hooks.json, le module register.*, bin/ et .mcp.json éventuel.
3. claude plugin validate ./mon-mod
   → inspecter en particulier les lignes hooks: et calls: sans exécuter le Mod.
4. claude --plugin-dir ./mon-mod plugin details <nom>
   → vérifier l’inventaire réel des composants.
5. claude plugin test ./mon-mod
   → tests de hooks déterministes, sans session, login ni réseau.
6. Si le plugin a des evals : claude plugin eval ... avant promotion.
7. Premier essai avec --plugin-dir dans un worktree jetable ; --safe-mode comme voie de récupération.
```

For an organization, real control must live in the **managed settings** (`allowManagedModsOnly`, order of managed plugins, `disableAllHooks` in accordance with policy) and in the Integrated Mod `cc-plugin-sec-default`, not in the good will of a User Mod. For your solo use, the equivalent rule is simple: **built-ins / personal code audited > opaque community plugin**, and no automatic update of a Sensitive Mod without rereading the version diff.

<!-- section: s-27 -->
#### Common hook configuration Claude Code / Codex

Separates **]local feedback** and ** validation gate**. A hook on a command `Edit` does not necessarily see the Bash, MCP or IDE scripts; it cannot guarantee containment. Deletes `ai-guard.sh` based on the search for strings in a command: dynamic paths, symlinks and indirect executions escape this filter. Apply the permissions/sandbox of section 12; controls the actually modified paths in the final diff. Hooks are not a substitute for the CI independent.

Examples for a trust project, `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

And `.codex/hooks.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "apply_patch",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Both harnesses call the same scripts (the events and payloads specific to the tools remain distinct). Codex requires rereading and approving unmanaged hook definitions (`/hooks`); does not disable this control. A worktree can load the hooks of the main checkout; checks the actually executed sources. Trusted hooks and scripts must be protected from writing by the agent; in the managed environment, place them out of the worktree. Do not run unaudited project hooks.

Script `scripts/ai-compile-check.sh` (compilation feedback only; can be disabled if too common):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
logFile=$(mktemp)
trap 'rm -f "$logFile"' EXIT
# Capture the process exit code, not a pattern in the logs.
if sbt --client "Test/compile" >"$logFile" 2>&1; then
  exit 0
else
  exitCode=$?
  printf 'sbt Test/compile failed (exit %s)\n' "$exitCode" >&2
  tail -n 40 "$logFile" >&2
  exit 2
fi
```

The result is based on the return code of sbt, even without a line `[error]`. `Test/compile` compiles the tests but does not run them. Do not use `grep` or a command RTK as an arbitrator of success; retains the return code of the original command. In the presence of several sessions, does not launch competing compilations on the same server sbt.

Script `scripts/ai-stop-audit.sh` (non-blocking, common to both harness):

```bash
#!/usr/bin/env bash
set -euo pipefail
# No transcript heuristics and no forced retry on legitimate blockers.
cat >/dev/null
printf '%s\n' '{"systemMessage":"Completion requires a fresh validation receipt for the exact candidate SHA and independent CI; report blockers without claiming done."}'
```

The Stop Hook never looks for an order in the transcript: a reference to `testOnly` does not prove its execution or success. Do not force the agent to continue when an invariant or budget imposes a stop. For completion, requires the structured report of `scripts/ai-validate.py` (section 11) and checks CI on the candidate. Local evidence produced under the agent's identity is useful for diagnosis, but falsifiable: the policy of CI, its scripts and results must live within a boundary independent of the agent.

A privileged Claude Mod or a unreliable hook can modify the pipeline; keep external restrictions and administered controls. The final gate cannot be modified and then self-approved by the writer. Hooks can be ignored or not triggered depending on the surface; checks events, paths and actual permissions before adoption.

<!-- section: s-28 -->
#### Recovery protocol when the loop agent

An agentic loop (same error, same correction, same failure) is a mode of failure distinct from simple failure. The model climbing does not correct it. Here is the protocol in 4 steps:

**Step R1 — Stop and state extraction (0 additional token)**

Stop the agent immediately. Do NOT restart "fix it". Run:

Stop. Don't change anything. Summarizes 5 points:

1. Files modified so far ( diff from approved database + git status)
2. Current Assumption on Cause
3. What was tempted and why it failed
4. The next minimal action you'd propose
5. What you're not sure about

**Step R2 — Human diagnosis with IDE (5-10 min)**

Use IntelliJ to check what the agent cannot see:

- The real type of an expression (Ctrl+Shift+P / info type)
- The actual resolution of an implicit/given (Ctrl+B on the Implicit)
- The expected type hierarchy vs. produced
- Breakpoint debugger on unexpected behavior

The aim is to find the structural information that the agent lacks.

**Step R3 — Fresh session with tight context**

/clear Quick new with ONLY:

- The objective (1 sentence)
- The exact file or method concerned
- Accurate error (copyed from the IDE, not from the transcript)
- Structural information found in R2
- "Proposes only one minimal change. Compile and test."

**Step R4 — If failure after R3, model escalation**

It is only now that the Sonnet climb → Opus → Fable is justified, because the context is clean and the problem is well posed.

Absolute anti-pattern: restart the same model in the same context hoping for a different result. This is the definition of the loop.

> **Periodical re-anchoring, the parade measured against long drift.**
> The research 2026 on the "drift agent" (behavioral degradation measured on long trajectories and the
> multi-agent systems) converges on three mitigation families: episodic consolidation of history in
> structured summaries, adaptive behavioral anchoring (re-injection of the charter and objective periodically)
> and routing taking account of drift. Immediate translation for your sessions:
> - **re-injects the charter** (objective, non-objective, invariant, definition of done) at each milestone and at the return of
>   subagent — not only at the first prompt: a constraint that is no longer in the recent window no longer exists;
> - **Generalizes the status file** (`MIGRATION_STATE.md`) at any long session, not only at missions
>   Fable: it is the anchor that survives compactions and repeats;
> - **double-threshold breaker circuit**: a warning about the repetition of the same tool call or the same tool call
>   error, then a hard stop on the same second repetition — rather than a single brutal threshold;
> - **fresh session in case of loop**: model climbing does not correct a loop (section 3); `/clear` +
>   status + charter rereads, yes.

---

