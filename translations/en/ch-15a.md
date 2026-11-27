<!-- section: chapter -->
# 15A. CI/CD for agentic workflows

CI is the final deterministic judge of the guiding principle — provided that it adapts to the agentic PRs, which have specific modes of failure: tests that cannot fail, diffs out of template, expensive loops.

<!-- section: s-1 -->
## The four PRs specific gates

```text
1. Gate de gabarit et scope : diff base → candidat, fichiers protégés, taille et nombre de fichiers
2. Gate de qualité de test : suites réellement exécutées + mutation score et mutants importants selon risque
3. Gate de review : findings BLOCKING / REGRESSION_RISK vérifiés traités ou arbitrés humainement
4. Gate de budget : tout job appelant un LLM a un timeout ET un plafond de coût
```

Two complementary axes to consider once the four gates are in place:

- **Architectural drift control** : Thoughtworks Technology Radar (April) 2026) notes that the intensive use of agents accelerates the drift between the real code and the architecture targeted, and recommends linking deterministic controls (fitness functions — ArchUnit, which analyses the bytecode) JVM and therefore also works on Scala compiled) with an evaluation LLM a rule ArchUnit "the module `api` does not depend on the implementation » executed in CI Cost less than an agent tower and stop a structural drift than neither scalafmt nor Stryker4s Don't see.
- ** Duplication Control**: SlopCodeBench (section 1A) measures a duplication accumulation over agent checkspoints; a jscpd-like scan (copy-paste detector that tokenizes the sources Scala) on the affected files turns this signal into a followed metric or even a gate. Duplication is the least visible defect in human review and one of the most expensive in delayed maintenance.

On GitHub, **Copilot Code Review or Codex Code Review can be added as an automatic signal**, but does not replace any of these gates. A review of the bot is not a human approval; checks the rules GitHub begin with a review on request or at the opening, then reserve the review after correction to the changes that justify it and to the new SHAs that require independent validation.

**Claude Approvals is not proof of quality.** A rule `claude: approves` does not trigger Code Review alone; `seats: 1` can count the author and `seats: 0` can allow a merge without human reading. GitHub can also count the approval of the bot in its review quota. For the workflow of this guide, keep`claude: comments` initially, independent human approbators in teams, and a human merge in solo. Never use a probabilistic classification as the sole arbiter of a critical change.

The presence of `.claude/approvals.yml` can disable automatic reviews on covered paths, even in observation mode: to keep them, reference `claude/code_review` in the rules (e.g. under `advisory`). An Approvals condition does not read the results of CI: keeps compile, tests, scalafmt, security and mutation testing as required checks GitHub separated. As a team, protects the target branch and policy with CODEOWNERS, forbids bypasses to agents and invalidates old approvals when the diff changes. Makes the check Approvals mandatory only after having evaluated the decisions observed; does not activate auto-merge or merge tail without an effective human gate for the changes that require it. A green check, a resolute discussion or a comment
"no defects" are never worth a job validation.

<!-- section: s-2 -->
### GitHub Rulesets and gate independence

Impose required checks from the expected integration, without bypass for agent identities; protects target branches, prohibition of force-push and removal, approval of recent changes and invalidation of old approvals when diff changes. In team, require approval of an independent human, and `CODEOWNERS` for control files; solo, does not configure an impossible rule to satisfy by the author, retains the human merge and separate policy control. Does not count a review bot as a human. A tail merge is optional, provided to check `merge_group`, and to require the gates of the integration commit. In case of conflict, change of SHA or advance of the base, re-evaluate the state ; a CI Green on an old revision does not validate the new candidate.

<!-- section: s-3 -->
## Example: `.github/workflows/ai-review.yml`

Example for the two-module repository in section 11 (sbt 1.x). Fig the actions to a complete audited SHA and check their transitive dependencies; update them by dedicated PR. The basic SHA comes from the event GitHub, not from a PR field controlled by its author. `github.sha` is the integration candidate for `pull_request` and `merge_group`; the human review is about the diff base/PR head, distinct from this test commit. For a tail merge, the controls must also be executed on the merge group.

```yaml
name: ai-review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  merge_group:
    types: [checks_requested]

permissions:
  contents: read

concurrency:
  group: ai-review-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  deterministic-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          fetch-depth: 0
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1

      # Validate the integration candidate; fail on a missing base or wrong checkout.
      - name: Validate candidate
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}
          CANDIDATE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail
          test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
          test -n "$BASE_SHA"
          git merge-base --is-ancestor "$BASE_SHA" "$CANDIDATE_SHA"
          python3 scripts/ai-validate.py --base "$BASE_SHA" --mode validate \
            --receipt "$RUNNER_TEMP/validation.json"

  mutation-gate:
    needs: deterministic-checks
    runs-on: ubuntu-latest
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1
      # Configure Stryker's break threshold and inspect surviving mutants in the actual project.
      - name: Mutation testing
        run: sbt "project api" stryker
```

**Confidence border of CI :** the YAML illustrates checks, not a mechanism inviolable by itself. PR can modify the scripts and workflow it contains, or even build commands or reports. Protects workflows, scripts, test rules, policies and reports. `CODEOWNERS` ; if available, impose a trusting workflow requirement from a protected repository/commit (rules and organization) and load the validator from this source rather than from the candidate. A legitimate policy change is via a separate PR and human validation. Solo without requiring external workflow, compares these files to the base and does not allow a merge until a change in the gate has been reviewed. Do not rely on a simple convention `AGENTS.md`.

The PR checkout can execute arbitrary code via sbt: no privileged secret, no token of writing, no `pull_request_target` executing the PR code, no cache shared with privileged jobs without source control. Test reports are operational proofs, not inviolable certificates if the test code itself is hostile. Archive reports and provenance in the CI according to the project policy; validation must be redone on the final candidate (and on the commit delivered so different).

Doctrinal issues:

* **deterministic judges pass first** : Compile, format and targeted tests are inexpensive compared to a call LLM — a job LLM which runs on code that does not compile is budget burned;
* if a review LLM of the CI is really automated, give it a **Key API dedicated**, a timeout and a job-specific spending cap; for mainly interactive use via Claude and ChatGPT, this automation remains optional ;
* **the job LLM is read-only** He comments on the PR, he never commits. An agent who corrects in the CI recreates the "two writing agents" problem of the section 16, worse (without human in the loop);
* **`sbt --client` in local, JVM fresh in CI** : the demon sbt is the lever of local loops; in CI, a controlled dependency cache can speed up resolution, but does not replace testing or insulation. **sbt 2.0.0 is stable since the 14 June 2026** ; uses at least **2.0.7** (or **1.13.0** on the branch 1.x) because of the BSP/TCP correction of the 21 August: building definitions in Scala 3JDK 17 minimum, native customer `sbtn` (starting much faster — directly useful for agent loops), local/distance cache compatible Bazel and `test` This guide follows the convention sbt 1.x: migration to sbt 2.x is a critical build change that never delegates to an agent — human plan, dedicated branch, plugin compatibility check (60+ supported, including Play and Scala.js in progress), then
  adaptation of these jobs.

**Autofix Codex in CI : explicit exception to review job read-only.** If a hosted patch stream is really needed, separates the generation job from the patch (without push right) from the controlled publication job; limits the triggers to approved events and actors. Never launches unreliable PR code with secrets or privileged writing token (notably via `pull_request_target`) Fig the actions by SHA, apply minimum permissions, timeout, external budget and a competitive lock by PR; check the head SHA before publication, then restart the required checks. No force-push, self-approval or merge by the job LLM. Comments, logs and patches remain unreliable data; failure must never lead to a change in the gates.

The same cutting is translated into GitLab CI: three stages (`deterministic`, `mutation`, `llm-review`), same gates, `rules: changes` to run Stryker only on the affected modules.

---

