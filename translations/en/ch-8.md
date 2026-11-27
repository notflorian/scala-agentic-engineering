<!-- section: chapter -->
# 8. Recommended repository structure

Add these files or folders to the root, keeping ** one place of truth**:

```text
AGENTS.md                       # Shared, short, version-controlled source
CLAUDE.md                       # Optional: imports @AGENTS.md + Claude-specific rules
GEMINI.md                       # Pointer to AGENTS.md or a symlink, depending on your tool
.github/copilot-instructions.md # GitHub Copilot review / coding agent rules, if used
.github/instructions/           # Path-specific Copilot rules where needed
.aiignore                       # AI exclusions: secrets, large artifacts, generated files
.claude/rules/scala.md          # Claude rules for specific paths/scopes where useful
.claude/rules/testing.md
.claude/rules/security.md
stryker4s.conf                  # Mutation testing
docs/architecture.md
docs/testing.md
docs/review-checklist.md
docs/scala-style.md
scripts/ai-test-changed
scripts/ai-lint-changed
scripts/ai-diff-context
scripts/ai-rules-drift
```

The purpose is not to accumulate documentation, but to avoid the agent rediscovering the same rules at each session. The file must remain short, stable and operational.

> **Synchronization of context files:** Codex loads global instructions for `CODEX_HOME`, then
> the files of the project path from the root to the current directory. At each level,
> `AGENTS.override.md` takes precedence over `AGENTS.md`; instructions closest to the work directory
> The fallback names and the maximum size depend on the configuration.
>
> Claude Code, with the built-in Mod `cc-plugin-agents-md`, uses by default `claude-md-or-agents-md` :
> `AGENTS.md` is loaded if no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the
> current directory or its parents. User/administered instructions and `.claude/rules/` continue
> `AGENTS.override.md` is not read by Claude via this fallback.
> `claude-md-and-agents-md` load both without duplicated a file already imported. The fallback can be
> not available on certain surfaces; it does not replace an explicit import when necessary.
>
> For this mixed workflow, prefer a common `AGENTS.md`, and if a `CLAUDE.md` exists, start it by
> `@AGENTS.md`. Then only keep the rules really specific to Claude. Check the instructions
> loaded in a new session ([`/context all`] side Claude, and ask Codex to list the files
> For submodules, also check the discovery from the actual directory.
> No override should be able to weaken an external security rule.

Side Claude Code : the **rules** under `.claude/rules/` allow to complete the project instructions with more targeted instructions, e.g. by sub-tree or type of task. This is often preferable to a huge `CLAUDE.md` global when this file exists.

Also: the **auto-memory**Claude Code requires a recent version, documented from v2.1.59+. The first lines of `MEMORY.md` can be loaded automatically, and sub-agents can have their own memory. Use this memory for reminders of recurring patterns, not for secrets, not for unreviewed architecture decisions, and not as a substitute for versioned documentation.

<!-- section: s-1 -->
## Minimum content of `AGENTS.md`

```text
Build, test and formatting commands (exact commands)
Non-obvious architecture boundaries and business invariants
Public API / JSON / migration constraints
Protected files and permitted write scope
Scala conventions absent from existing documentation
Stop conditions and definition of done
Pointers to relevant docs and spec
```

Write these rules ** for the agent, not as human documentation**: prefer paths, commands, numbers and verifiable conditions. Keep a few hundred words as a starting point. README, tutorials, the exhaustive list of modules and model comparisons remain in `docs/`, loaded on demand.

<!-- section: s-2 -->
### Routing in user configuration

Keeps the matrix of section 3 in a routing document or user profiles Codex/Claude rather than in each `AGENTS.md`: the repository must remain independent of the model. If an orchestrator should consult this matrix, only adds a pointer to it. Business and security constraints do not change according to the model.

<!-- section: s-3 -->
## Minimum content of `CLAUDE.md`

```text
@AGENTS.md

## Claude Code
Use plan mode for risky multi-file changes.
```

Moves the common rules from the old `CLAUDE.md` to `AGENTS.md` (no duplication). Claude plan mode is a harness preference; actual permissions remain in the configuration and sandbox.

<!-- section: s-4 -->
## Why keep `AGENTS.md`

With Codex and the Integrated Mod `cc-plugin-agents-md` of the Claude Code (fallback) `AGENTS.md` default), `AGENTS.md` Recent work on coding agents indicates that a file of instructions of this type can reduce execution time and output tokens while maintaining a comparable completion rate. The expected practical effect is simple: less repeated context, less forgotten instructions, less drift between tools.

> **Statement of evidence: mixed result, not automatic benefit.** Another assessment of 2026 observes that files
> de contexte réduisent souvent légèrement le taux de réussite et augmentent le coût de plus de 20 %, especially when they
> The files written by the maintainers do better than those written by the maintainers.
> These are automatically generated, but must also be measured.
>
> Rule corrected: `AGENTS.md` must contain only what actually changes an action — exact commands,
> non-obvious invariants, prohibited files, conventions absent from README and stop rules. No guided tour
> narrative of the repository, no catalogue of technologies, no generic tips. Regularly compares a sample
> with and without the file. Quantitative additional benchmark from the
> the same literature: remain under **~500 words**, focusing on test standards, style conventions, and
> Hazard warnings — no guided tour of the repository — and read the file as code at each review.

<!-- section: s-5 -->
#### Validation protocol: measuring the effectiveness of AGENTS.md

An AGENTS.md that does not change the result is the dead context that costs tokens at each session.

**Test A/B on 10 representative tasks:**

1. Selects 10 actual backlog tasks (mix greenfield/bugfix/refactor)
2. For each task, perform 2 times:
    - Run A: with AGENTS.md in context
    - Run B: without AGENTS.md (or with an empty version)
3. Measurement for each run:
    - Number of laps before completion
    - Number of files offscope affected
    - Number of compilation errors
    - Compliance with test conventions
    - Total cost in tokens
4. Compare:
    - If AGENTS.md does not reduce any metric → it is useless, delete it
    - If it reduces some metrics → only keeps useful sections
    - If it increases the cost without improving the quality → it is harmful

**Indicators of an effective AGENTS.md:**

- Agent quotes exact test commands without rediscovering them
- The agent doesn't touch the forbidden files without being reminded.
- The agent complies with the naming conventions from the first diff
- The number of human "recalls" during the session decreases

**Indicators of harmful AGENTS:**

- The agent produces more verbose diffs (it "applies" too many rules)
- Cost in tokens increases > 20% without measurable improvement
- The agent hallucinates commands that are not in the file
- Generic rules undermine specific rules

Maintenance rule: Whenever an AGENTS.md rule is breached by an agent AND the violation is caught in review, the rule is either poorly formulated or in the wrong place. Correct it or materialize it in a section control 5] or 15A rather than adding one more sentence.

<!-- section: s-6 -->
#### Audit of *rule drift*: check that instructions still describe the actual repo

The rules for agents are deliberately specific — paths, commands, modules, forbidden files — and that is precisely why they age quickly. A false instruction is worse than an absent instruction: it forces the agent to reconcile `AGENTS.md` with a codebase that has already changed.

Add `scripts/ai-rules-drift` and execute it after any architecture/build changes, then at least once a week if the repository moves a lot:

```text
Verify that:
- every path mentioned in AGENTS.md / CLAUDE.md still exists
- each referenced sbt module still exists
- every compile/test/format command is still valid
- deleted DBs, services, directories, and scripts are no longer referenced
- files marked off-limits still correspond to actual critical surfaces
- CLAUDE.md, if present, still imports or supplements the expected shared source.
```

The script can remain deterministic for simple checks (`test -e`, grep modules, controls `--help`/dry-run) and do only **report** Ambiguous cases. Never allow the agent who detects drift to rewrite and then self-approve its own persistent rules: the rule diff reviews itself as code.

<!-- section: s-7 -->
### Instructions GitHub Copilot without duplicate `AGENTS.md`

If the repository uses GitHub Copilot, preserved `AGENTS.md` as a common contract and reservation `.github/copilot-instructions.md` the specific expectations of **Review GitHub** : severity of the findings, PR conventions, files to be monitored and criteria to be reported. `.github/instructions/**/*.instructions.md` allow to specialize these rules by path. Avoid copying all the architecture or rules Scala : a common instruction must remain in `AGENTS.md`.

Copilot Code Review reads the instructions and skills of the ** lead branch of the PR.** An amendment to these rules is therefore part of the code surface to be reviewed: an agent must not be able to relax its own constraints in the same PR without this change being explicitly visible and validated.

