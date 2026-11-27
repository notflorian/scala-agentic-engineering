<!-- section: chapter -->
# 3. Model selection and routing

<!-- section: s-1 -->
## Simple rule

```text
Qwen / Haiku préparent et filtrent.
Micro-dev sous fort contrôle humain → GPT‑6 Luna High ou Sonnet 5.5 Medium.
Agentic coding end-to-end → GPT‑6.2 Sol Medium ou Opus 5.5 Medium.
Debugging / architecture difficiles → Opus 5.5 High ou GPT‑6.2 Sol High.
Frontier ponctuel → GPT‑6.2 Astra Light ou Fable 5.2 Low avant de pousser aveuglément l'effort du modèle inférieur au maximum.
Un seul writer par worktree.
L'autre famille de modèles reviewe ou challenge, elle ne duplique pas automatiquement toute la trajectoire.
Ultra / multi-agent uniquement lorsque les sous-problèmes sont réellement indépendants.
IntelliJ valide.
Toi, tu décides.
```

Routing must minimize the ** cost of the completed task**, not the cost of the first call:

```text
charge totale attendue
= découverte + implémentation + vérification
+ probabilité de reprise × coût de reprise
+ coût de coordination
```

A more expensive model can therefore be the best purchase if it avoids a bad exploration, several unnecessary diffs and loops of CI. Conversely, a micro-loop controlled by a senior makes Luna, Sonnet or Haiku dominant as soon as the error is detected in a few minutes.

*Never delegate the update of versions in `build.sbt` without requiring the agent to first interview a MCP, Context7, Maven Central or official documentation. Library names and versions are exactly the type of information that models hallucinate when working out of context.*

<!-- section: s-2 -->
## Routing matrix

| Task                                                    | Mode         | Recommended Senior Officer                   | Second useful passage                           | Why?                                                                           |
|----------------------------------------------------------|--------------|----------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------|
| Summarize a module, grep, uses, simple logs            | Micro-dev    | **Haiku 5.5** or Qwen local                  | None except ambiguity                           | High frequency reading, low risk                                             |
| Accurate mechanical modification, boilerplate, rename   | Micro-dev    | **GPT‑6 Luna High**                          | Sonnet 5.5 Medium so subtle types             | Very good cost when the human keeps the direction                                    |
| Write a simple test from a known behavior   | Micro-dev    | **GPT‑6 Luna High**                          | Sonnet 5.5 Medium if rich trade rule        | Easily verifiable output                                                       |
| Stack trace or precise failure                           | Micro-dev    | **Sonnet 5.5 Medium**                        | Luna High to apply a bounded patch        | Sonnet brings more understanding without paying Opus                               |
| Small reproducible bug, known perimeter                     | Micro-dev    | **Sonnet 5.5 Medium**                        | Luna High for testing/mechanical editing         | Short loops, immediate feedback                                                 |
| Local patch, non-trivial types or invariants            | Micro-dev    | **GPT‑6.1 Terra Medium**                     | GPT‑6.2 Sol Medium if exploration necessary  | Intermediate third party to be measured on bounded patches |
| Small local refactor                                     | Micro-dev    | **Sonnet 5.5 Medium**                        | Luna High for mechanical verification          | Senior retains architecture                                                  |
| Targeted review of a small diff                            | Verification | **GPT‑6.2 Sol Light**                        | Sonnet 5.5 Medium if second helpful notice         | More judgment than a worker, without paying a full agent review            |
| Complete standard output, clear spec                     | Agentic      | **GPT‑6.2 Sol Medium**                       | **Opus 5.5 Medium** in review                  | Best flaw Codex for exploration → patch → tests → PR                        |
| Normal multi-file feature                           | Agentic      | **GPT‑6.2 Sol Medium**                       | Opus 5.5 Medium in Review                      | Ownership end-to-end with cost content                                             |
| Complex feature, several layers                      | Agentic      | **GPT‑6.2 Sol High**                         | Opus 5.5 Medium/High                           | More planning and verification                                         |
| Architecture or migration choice                       | Agentic      | **Opus 5.5 High**                            | Sol Medium to challenge the plan             | Judgment dominates the production of code                                           |
| Root cause unknown / bug Scala subtle                   | Agentic      | **Opus 5.5 High**                            | Sol Medium/High for independent hypothesis    | Understanding the problem costs more than the patch                                     |
| Competition, async, flaky difficult test                 | Agentic      | **Opus 5.5 High**                            | Sol High if the first track fails           | Reduces the risk of anchoring on a false cause                                    |
| Migration/public compatibility                       | Agentic      | **GPT‑6.2 Sol High**                         | Opus 5.5 High in Conceptual Review           | Disciplined execution + second independent judgment                                |
| Large cross-sectional refactor                                | Agentic      | **Opus 5.5 High**                            | Sol Medium/High in Review                      | Opus for global consistency; Ground to break blind angles                     |
| Normal review of a PR written by Codex                 | Verification | **Opus 5.5 Medium**                          | None except critical finding                    | Fresh context and other family of models                                         |
| Normal review of a PR written by Claude                | Verification | **GPT‑6.2 Sol Medium**                       | None except critical finding                    | Symmetry author/reviewer                                                           |
| Review architecture, invariants, limit cases             | Verification | **Opus 5.5 High**                            | Astra Light so high stake    | Search for conceptual errors rather than only reread the diff             |
| Security, Auth, Critical Contract                         | Criticism     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High as Reviewer                   | Buy the superior capacity without going directly into extreme effort           |
| Very ambiguous problem, end-to-end judgment                | Frontier     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High to criticize the plan           | The ability to judge counts more than the length of the diff                   |
| Very difficult decision in the middle of a normal task    | Advisor      | **Fable 5.2 Low**                            | Sol/Opus remains the executor                     | Buy ad hoc border judgment without transferring all the task         |
| Sol High fails by capacity limit                   | Climbing     | **GPT‑6.2 Astra Light**                        | Medium/High only if necessary            | Changing thetier can cost less than an extended Extra High Sol                    |
| Opus High fails by capacity limit                  | Climbing     | **Fable 5.2 Low**                            | Sol/Astra to challenge                      | Same logic: low-effort border before lower maximum effort               |
| Simple CI failed after correct implementation            | Resumed      | **GPT‑6 Luna High** or **Sonnet 5.5 Medium** | Climbing only if conceptual problem      | Do not pay Sol/Opus for local and verifiable correction                     |
| Independent post-PR follow-up (CI, review, mergeability)         | Resumed      | **GPT‑6.2 Sol Medium**                      | High if root cause difficult; Sol 6.1 in fallback | Goal mode, Heartbeats or Cloud; bounded sequential loop, not Ultra           |
| Second failure revealing a bad conception          | Resumed      | **GPT‑6.2 Sol High** or **Opus 5.5 High**    | Use the other family to break anchor | The problem is no longer mechanical: the hypothesis has to be requalified                 |
| Repeated failures despite Sol High / Opus High               | Climbing     | **GPT‑6.2 Astra Light** or **Fable 5.2 Low**   | The other front line challenge                 | Capacity becomes the limiting factor; leaving with a context of its own         |
| Autonomous session > 30 min, sequential dependencies     | Long horizon | **Opus 5.5 Extra (`xhigh`)**                 | Sol High at the end                              | Extra is justified by length, not symbolic importance                |
| Extremely difficult work for several hours    | Frontier     | **Fable 5.2 High**                           | Astra Light/Medium in Independent Review      | Reserve high border cost to trajectories where it avoids major overlaps |
| Exploration codebase-scale decomposable                  | Multi-agent  | **GPT‑6.2 Sol Ultra**                        | Opus Medium for synthesis/review               | Ultra applies especially to independent read-heavy axes                           |
| Tests, exploration and triage massively parallelizable | Multi-agent  | **GPT‑6.2 Sol Ultra**                        | Claude only on major anomalies | Parallelism pays when subtasks are independent and verifiable       |
| Several writers on the same files                 | —            | **To be avoided**                                 | Sequencing                                 | Coordination costs generally exceed the gain                               |

> **Note Qwen3-Coder-Next Local** : the official model is a MoE of **80B total parameters, 3B activated**, avec 48
> hybrid layers, a native context **262 144 Tokens** and operation exclusively **non-thinking**. The
> number
> reduced active parameters improve the cost of calculation, but the **80B weight should still reside in
> memory
> ** : « 3B active" therefore does not mean that it behaves in RAM as a dense 3B.
>
> The official GGUF sizes are: **Q4_K_M 48,4 Go**, **Q5_K_M 56,7 Go**, **Q6_K 65,5 Go** and **Q8_0 84,8 Go**. The
> file size is not the total consumption: add context cache, backend buffers, the
> macOS, IntelliJ, sbt and JVM of the project. On **128 Go**, the four variants can theoretically be
> They do not offer the same operational margin.
>
> ```text
> Q4_K_M  → défaut « marge maximale » : IDE, sbt et plusieurs JVM restent confortables.
> Q5_K_M  → défaut recommandé : meilleur compromis qualité / mémoire sur cette machine.
> Q6_K    → option haute qualité : viable si les autres applications restent raisonnables.
> Q8_0    → option d'évaluation : possible, mais marge réduite et bénéfice à prouver face à Q5/Q6.
> ```
>
> Official documentation Qwen uses precisely **Q5_K_M** in his example `llama.cpp`, avec `-c 40960`, and not the
> maximum context 256K. For daily work, go on **32K à 64K**, then only increases if a
> The context declared by the model is a maximum capacity, not a configuration.
> Economic
> default.
>
> **Recommendation for your M5 Max 128 Go** : preserved **Q4_K_M and Q5_K_M** on the SSD.5_K_M as profile
> daily pre-analysis, module summary and generation of simple tests; switch to Q4_K_M when IntelliJ,
> plusieurs modules sbt, Spark ou des JVM lourdes consomment déjà beaucoup de mémoire. Ne conserve Q6_K ou Q8_0 que si
> one
> bake-off Scala shows a measurable gain in quality. With 8 To from SSD, storage is not the constraint; the
> pressure
> memory, latency and quality per task are.
>
> **Backend Apple Silicon** : test **MLX-LM and llama.cpp** Instead of immediately freezing a single engine.
> MLX 4-bit and 8-bit conversions exist, and a reproducible ratio of Qwen3-Coder-Next observed decoding
> much faster under MLX than under a given version of llama.cpp on Apple Silicon. This result depends on
> versions and does not constitute a guarantee for the M5 Max; it justifies a local benchmark with fixed versions.
> `llama.cpp` However, it is still the best documented way forward. Qwen and easily exposes a server OpenAI- compatible.
>
> **Metal and wired memory** : does not show " 75 %" as an absolute hardware limit. `llama.cpp` displayed on
> start `recommendedMaxWorkingSetSize`, which is the value to be observed on the version of macOS and the relevant Mac.
> Undocumented setting `iogpu.wired_limit_mb` exists and is used by the community, but it must not become a
> standard prerequisites: first test the model without system modification. Q8_0 can work on a machine 128 Go,
> but a long context or multiple slots can bring the process closer to this limit before physical RAM
> either
> Fully occupied.
>
> **Minimum measurement protocol**: compares Q4_K_M, Q5_K_M and possibly Q6_K on the same ten tasks Scala, with
> the same context and the same harness. Measure the rapid processing, the generation rate, the time to the
> first token, maximum memory, memory pressure macOS, and accepted task rate. Do not deduct speed
> of the number of active parameters: hybrid architecture and the implementation of kernels can produce
> variance
> important between backends.
>
> **Qwen3.8-27B.** The dense **Qwen3.8-27B** becomes the local quality-first challenger to add to the
> bake-off Scala. Qwen publishes a context of up to 1M according to deployment and scores editor of 73 on
> Terminal-Bench 2.1 and 61,7 on SWE-bench Pro. These numbers do not justify replacing Coder-Next by default:
> test
> both with the same harness, the same context, the same tools and the same time budget. **Coder-Next remains the
> specialised and economical local baseline; Qwen3.8-27B is the challenge to be given priority when quality counts more
> ** Rates API Qwen3.8 depend on the region and should not be presented as a world price.

>
> **Qwen3.8-Omni-Flash.** Since 17 September 2026Alibaba also offers this model API multimodal: text, image,
> input audio and video, output text, function calling, configurable thinking, web search, context cache,
> **1M tokens of context** and up to **131 072 tokens of output** via Cat Completions or ResponsesAPI. It completes
> routing for scanning screencasts, talks, interfaces or multimodal documentation; it ** does not replace**
> Qwen3-Coder-Next as a local code baseline or Qwen3.8-27B as challenger Scala quality-first. Rates vary
> depending on the region of deployment: keep this data out of sustainable routing rules and check Model Studio at
> Time of choice.

<!-- section: s-3 -->
### Side Anthropic

| Model         | API ID              | Tariff (input/output / M tokens) | Background          | Default effort | Active role in this guide                                                           |
|----------------|---------------------|---------------------------------|-------------------|-------------------|------------------------------------------------------------------------------------|
| **Fable 5.2**  | `claude-fable-5-2`  | $8 / $40                        | 1M (exit 128K)  | `high`            | Frontier: long-term and demanding reasoning when Opus 5.5 is not enough      |
| **Opus 5.5**   | `claude-opus-5-5`   | $4 / $20                        | 1M (exit 128K)  | **`medium`**      | Agentic defect: autonomous coding, architecture, debugging and large refactors      |
| **Sonnet 5.5** | `claude-sonnet-5-5` | $2 / $10                        | 1M (exit 128K)  | `high` API        | Micro-dev / well-specified tasks; `medium` recommended for agentic coding bounded |
| **Haiku 5.5**  | `claude-haiku-5-5`  | $0.10 / $0.50 (prompt ≤ 100K)   | 1M (exit 128K)  | `medium`          | Workers, sorting, extraction, logs, low-risk sub-agents                     |

> **Current Routing:**Anthropic recommends that most workflows start with **Opus 5.5**,
> whose default effort is `medium`, then adjust the effort before changing the model. **Sonnet 5.5**, the
> well-specified agentic coding starts usefully at `medium` and goes up to `high` for longer tasks or
> difficult.
> `xhigh` (noted) **Extra** in this guide) and `max` are reserved for cases where the evals show a gain. **Haiku 4.5 do not
> Haiku 5.5, which replaces it, supports it with `medium` by default.** The paragraphs below on Sonnet 5 / Opus 5 remain reference points of the
> migration
> They do not replace this active matrix.

> **Migration API to Opus 5.5 / Sonnet 5.5.** The two models impose more discipline on the client than the
> previous generations: adaptive thinking is the normal diet, the *forced tool use* (`tool_choice: any/tool`)
> returns an error 400, and the *thinking blocks* must remain attached to their model and to the conversation that has them
> **Opus 5.5** also rejects non-standard sampling parameters and the prefill wizard; its effort by
> default is `medium`. **Sonnet 5.5** uses `thinking: {"type": "between_tools"}` to remove the initial thinking
> (`low`] to `high` only), and now returns the intermediate text between tool calls in blocks `thinking`.
> On Claude API and Google Cloud, both models use the current computer-user toolset
> `computer_toolset_20260801` rather than `computer_20251124`. A model migration must therefore test **payloads,
> streaming, tools and conversation resume**, not just replace the model ID.

> **Sonnet 5** replace Sonnet 4.6 (`claude-sonnet-4-6`, always available at the same price
> $3/$15) as a daily driver. It is a [*drop-in replacement[* side API, with three behavioral changes to
> know before migrating:
> - **Adaptive thinking enabled by default** ; the extended thinking manual (`thinking: {type: "enabled"}` with
>   `budget_tokens`) now returns an ** error 400** — migrates to adaptive thinking.
> - ** Locked sampling parameters**: any non-default value of `temperature`, `top_p` or `top_k` returns
>   an error 400.
> - **New tokenizer** (same line asOpus 4.7+) : ~30% more tokens for the same text (up to 1.35x
>   The tokenizer can always increase the number of tokens charged, so count the
>   quick with the token meeting endpoint and see the `max_tokens` tight ones.
>
> Other operational specificities: **Effort Control** generalised (low level) → **xhigh**, defect *high* on
> l'API and Claude Code), first **cybersecurity safeguards real time** on a Sonnet (a refusal returns in HTTP)
> 200 with `stop_reason: "refusal"`, not in error — to be managed in the customer), no Priority Tier, output 128K
> ([300K in batch via the header beta `output-300k-2026-03-24`). It is also the new default model of the planes
> Free and Pro on claude.ai.

> **Common updates**: quick caching and batching (–50% input and output) apply to *all* models
> Claude. The price of reading the cache depends on the model: **Fable 5.2 costs $0.20/M tokens in cache read**
> (compared to $0.25/M for Fable 5.1). Batch remains useful for non-emergency work: PR summaries grouped,
> planned audits and installation generation. Fable 5.2, Opus 5.5 and Sonnet 5.5 include context 1M at tariff
> standard, without long context overload.
>
> **Tariff accuracy.** The read cache is worth **0,025× input** on Fable 5.2/5.1 ($0.20 and $0.25/M),
> **0,05×** on Opus 5.5 and Sonnet 5.5 ($0.20 and $0.10/M) and 0,1× on Haiku 4.5. Haiku 5.5 is the only current model
> with a **palier of quick length**: beyond 100 000 tokens of entry (cache included), all its rates are
> Number five times. Fable 5.2 $4/$20, Opus 5.5 $2/$10, Sonnet 5.5 $1/$5. Fast mode: Fable 5.2 $16/$80,
> Opus 5.5 $8/$40. `inference_geo: "us"` applies a multiplier of 1,1× on the categories concerned.

> **Claude Fable 5.2 replaces Fable 5.1 in the active routing of this guide.** Sheet
> Technical : ID `claude-fable-5-2` (`anthropic.claude-fable-5-2` on Bedrock), context **1M**, exit **128K**,
> **$8/$40**, write cache 5 Min $10 and 1 h $16, cache read **$0.20/M**, batch $4/$20, fast mode `speed: "fast"` à
> $16/$80, adaptive thinking always active, default effort `high`, cutoff June 2026, withdrawal not before the
> 9 November 2027. Same constraints as 5.1: **30 mandatory retention days (no RDA without authorization)
> express**, `tool_choice: any/tool` and prefill in 400, sampling to omit, no Priority Tier, no structured
> outputs for CMEK organisations. The model generates about 30 % faster than 5.1. **Mythos 5.2** is the same
> model with fewer safeguards, reserved for verified organisations.
>
> **Positioning.** The official matrix remains "most workloads start with Opus 5.5 "; we move on to
> Fable 5.2 if the `xhigh` or [`max` valleys remain insufficient on demanding or long-term reasoning.
> New to be incorporated into routing: on FrontierCode 2.0 (which measures whether maintainers would interfere with change),
> Anthropic reports **Fable 5.2 `high` à 45,3 %, at the level ofOpus 5.5 the best effort (45,5 %), pour environ la
> Half the cost per task**. Scores editor at best effort: FrontierCode 2.0 **49,1 %** (Opus 5.5 45,5; Astra
> 42,8 ; Fable 5.1 32,4FrontierSWE v2 **69,9 %** (Opus 62,3 ; Astra 65,5), Remote Labor Index 41,3 % against 21,3 %
> for Opus. On the short coding the gap is small: Terminal-Bench 4.0 67,6 % against 66,4 % (Opus `xhigh`), in the
> The independent measures Vals confirm the grade: equality with Opus 5.5 on Terminal-Bench 4.0
> ([65,15 %] %), Opus ahead of SWE-bench Multimodal (70,2 % against 62,3 %).
> **Mini-SWE-agent** of Vals, this equality corresponds to about **$14,56/Task for Fable against
> $12,04 for Opus**, with Fable faster (55 min against 64 min): the cost advantage per task announced
> by Anthropic on FrontierCode **does not spread** The practical consequence:
>
> ```text
> Opus 5.5 High insuffisant (capacité)        → Fable 5.2 avant Opus 5.5 Max, à mesurer sur le benchmark Scala privé
> Décision difficile ponctuelle (advisor)     → Fable 5.2 low/medium
> Mission longue autonome                     → Fable 5.2 high (low/medium finissent plus souvent le tour trop tôt)
> Tâche bornée, bug UI/front, review courante → Opus 5.5 ou Sonnet 5.5 restent les meilleurs achats
> ```
>
> **Breaking changes since Fable 5.1** (checked in the official migration guide):
> - the **prefix check** now applies to all accounts: a thinking block returned with a `system`,
>   `tools` or a history different from those that produced it gives a 400 (`The block is bound to a different
>   conversation`). **A change in the tool list MCP between two queries counts as an edition** : pin
>   the tool list during the session, or uses changes in tools during conversation (beta
>   `inline-tools-2026-09-15`, via messages `role: "system"`. Beware of the harnesses that load the tools to the
>   request by amending `tools`;
> - **Fable 5.1 and Opus 5.5 do not read the thinking blocks of Fable 5.2** (they are deleted without error, so the
>   reasoning is lost in silence); Fable 5.2 read those of 5.1 andOpus 5.5. Server fallbacks
>   ([`fallbacks: "default"`], beta `server-side-fallback-2026-07-01`) target only `claude-opus-4-8` and
>   `claude-opus-5`: logs the executed model;
> - `computer_20251124` returns 400 (except Bedrock): use `computer_toolset_20260801` ;
> - the advisor of an executor Fable 5.2 must be `claude-fable-5-2` or `claude-mythos-5-2` ;
> - thinking counts in `max_tokens` (risk of `stop_reason: "max_tokens"` before any text) and Fable 5.2 to its
>   **own rate limit**, distinct from Fable's 5/5.1New useful betas: compaction on demand
>   (`compact-2026-09-04`), minding blocks (`thinking-binding-controls-2026-08-01`, with
>   `prefix_mismatch_behavior: "drop_block"` only as a palliative).
>
> **Behaviours that directly affect the quality of the differences and the cost** (prompting guide Fable 5.2) :
> - **Property of the code.** Without explicit instructions, the model adds to the existing structure, duplicates and reports the
>   similar problems instead of correcting them. The sentence proposed by Anthropic ("This codebase is yours...") does
>   merge duplicate code in about half of the tests, but cost about 1,5× output tokens, add
>   tests and docs not requested and changes an existing behavior in one trial in six to ten. **For tickets
>   to the minimum difference of this guide, do not add it**; reserve it to an explicit task of deduplication or refactor,
>   and reread the diff rather than the summary, which often omits small changes.
> - **Over-delegation.** At `xhigh` and `max`, Fable 5.2 can launch subagents to reread his own work, and the
>   subagents can represent a large part of the session cost. Audits the lines of `AGENTS.md`, skills and
>   files of agents that invite to delegate, and checks the default model of subagents.
> - **Premature ends** (list of remaining tasks, offer to continue) more frequent to `low` and `medium`:
>   for a long mission, adds the instruction "do not stop as long as there is still work required", while
>   distinguishing ordinary obstacle (to be dealt with) and deliberate blocking (forbidden file, guard: to be left and
>   Keep your own confirmations for risky actions.
> - **Server budget 的 circuit break.** The `task_budget` API is indicative: fixed a **external ceiling** cost,
>   number of calls, duration and number of attempts in the harness. Too tight `max_tokens` can interrupt
>   Fable before the first visible text, because thinking tokens count in the output. If the session seems
>   silent, uses tool-to-tool updates when available instead of multiplying the re-launches.
> - **Inherited instructions to be purged** : "answer without deliberation" does not stop the reflection from `medium`
>   (less effort rather); lines "treats this response as finished" from the prompting Opus 5.5 make
>   the model much less able to catch up with its own mistakes; the budgets of tokens written in the prompt
>   may be removed to `high`/`xhigh` without loss; outdated storage precautions reduce memory
>   This is exactly the role of `/doctor prompt-audit` (section 3, subagents).
>
> **Access and quota.** Claude Code **2.1.321+** (`claude --model claude-fable-5-2` ; the alias `fable` depends
> The eligible Max/Ultra plans can use Fable up to a fraction capped at **50 % of the
> weekly limits**, depending on actual conditions; use on Pro may depend on additional credits
> or temporary promotion. Do not confuse
> Never **visible model**, **quota included** and **billing API/credits** : controls the consumption screen and the
> the plan conditions at the time of the session. Recalibrate the effort `medium`, `high` and `xhigh` and the cost per task.

> **Note tokenizer**: the new tokenizer was introduced by **Opus 4.7** (not 4.8) and generates up to ~35% of
> tokens in addition toOpus 4.6 for the same text. **Sonnet 5 adopt the same line** (~30% more tokens than
> Sonnet 4.6], up to 1.35x depending on the content). The counting penalty remains relevant for Opus to
> identical price; on Sonnet 5, the permanent tariff **$2/$10** offsets a large part of the increase in the number
> of tokens in relation to Sonnet 4.6. The passage Opus 4.7 → 4.8 does not bear any additional penalty for tokenizer.

> **Opus 5 and transition since 4.8** Opus 5 is now the **model Anthropic difficult by default** Rate
> identical to Opus 4.8 ($5/$25) Guard 4.8 only as a compatibility fallback or historical reference.
> - **Fast Mode** ($10/$50, ~2.5x standard speed): for a hard task but *interactive* (debugging in pairs),
>   Opus 5 Fast is often a better purchase than Fable.
> - **Effort Control**: driving by effort remains the explicit step before Fable 5.2. On Opus 5, `xhigh` and `max`
>   require that the thinking remain active; `thinking: disabled` with these levels returns an error 400.
> - **Dynamic Workflows** remains relevant for codebase-scale parallelism; in Claude Code, complete it now
>   with Agent View. **Agent Teams** remains experimental and **Ultrareview** in research preview: don't transform them
>   and still in compulsory dependencies of workflow.

> **Note Claude Managed Agents** (hosted platform, public beta since April) 2026, header
> `managed-agents-2026-04-01`) : since Code with Claude (6 May 2026), the platform adds **Outcomes** (grading)
> independent on entry, revision loop if output does not pass), **multi-agent orchestration** (up to
> 20 a parallel specialist sub-agent on a shared filesystem), **webhooks** (beta)
> **Dreaming** (research preview: memory curation between sessions).
> rate API + $0.08 per hour of active session. For this guide, this is the third option on long missions,
> next to Fable mono-agent and Opus + Dynamic Workflows — relevant especially if you want a harness hosted with
> Executable success criteria (Outcomes is the platform version of the "gate of review" in section 15A).

> **OpenAI Agents API** is the side-hosted pendant OpenAI: it uses the
> harness managed by Codex with **sustainable sessions**, compaction and recovery managed, MCP and sub-agents with isolated context.
> Two primitives directly materialize the engineering context of the section 10 : **tool search** does not charge the
> tool definitions that when they become relevant, and the **programmatic tool calling** allows stringing,
> parallelize and filter calls before reinjecting only useful results. That's not a new reason
> to prefer OpenAI à Anthropic : comparison **Agents API**, Claude Managed Agents and local harnesses at cost by
> change accepted, keeping the same specs, tests and stop rules.
>
> **Computer use** can also run in a browser hosted by OpenAI.
> creates the session, explicitly approves each new origin and manages sensitive authentication itself.
> An original approval is not a confirmation by action: for purchase, deletion or other transaction
> keep a controlled runtime or a separate applicative gate.


Complementary operational characteristics:

| Model         | Relative latency | Prompt hiding     | Batch (–50%) | Operational specifications                                                                        |
|----------------|------------------|--------------------|--------------|---------------------------------------------------------------------------------------------------|
| **Fable 5.2**  | Moderate          | Yes; read $0.20/M | Yes          | Adaptive thinking always on ; defect `high` ; effort per message ; fast mode $16/$80            |
| **Opus 5.5**   | Moderate          | Yes                | Yes          | Adaptive thinking always on ; defect **`medium`** ; Low→Max                                     |
| **Sonnet 5.5** | Quick           | Yes                | Yes          | Adaptive thinking; default API `high`, but `medium` recommended for agentic coding well specified |
| **Haiku 5.5**  | Fastest   | Yes; read $0.01/M | Yes          | Default adaptive thinking; default effort `medium`; price level beyond 100K tokens |

<!-- section: s-4 -->
### Side OpenAI / Codex

**GPT‑6.2 Sol** is the recommended defect for the **complex coding and repeated agent workflows** in Codex when available. OpenAI position it as more effective by task than Sol 6.1, at the same rate API. **GPT‑6 Luna** targets focused, repeatable and high volume tasks; **GPT‑6.1 Terra** is the intermediate tier. **GPT‑6.2 Astra** remains the escalation of capacity for the most demanding tasks.

| Model          | ID API        | Standard price / 1 M tokens (input / output) | Recommended role in this guide |
|-----------------|---------------|---------------------------------------------|-------------------------------|
| **GPT‑6 Luna**  | `gpt-6-luna`  | **$0.10 / $0.50** | Micro-dev, mechanical modifications, simple testing, sorting and low-risk workers |
| **GPT‑6.1 Terra** | `gpt-6.1-terra` | **$1 / $5** | Local patch and targeted review when Luna lacks judgment |
| **GPT‑6.2 Sol** | `gpt-6.2-sol` | **$2 / $10** | **Default Codex Agent Medium** : End-to-end issue, multi-file feature, tests, PR, review and stewardship |
| **GPT‑6.2 Astra** | `gpt-6.2-astra` | **$8 / $40** | Frontier: very ambiguous problem, critical contract, escalation of capacity |
| GPT‑6.1 Sol / GPT‑6 Astra | `gpt-6.1-sol` / `gpt-6-astra` | $2 / $10 ; $10 / $50 | Fallbacks if versions 6.2 are not available; historical baselines |

> **GPT‑6.1 Terra fill the hole between Luna and Sol.** Released 26 October 2026 (`gpt-6.1-terra`),
> it costs **$1/$5** (cached input $)$0.05/M), i.e. half of the Sol 6.1, with the same window of about 1,05M tokens.
> is available in ChatGPT Work and Codex (Plus, Pro, Enterprise, Edu; not in the Chat tab) and requests a Codex
> Recent CLI (0.159+ depending on the sources). OpenAI positions it on common bug fixes, computer use,
> vision and writing; for demanding coding, now prefers **Sol 6.2 or Astra 6.2**. Published score:
> 50,3 % on Terminal-Bench 4.0 at max effort (21,5 % for GPT‑5.6 Terra) For this guide, Terra becomes the **candidate
> natural for bounded patches and review of small diffs** when Luna is too fair and Sol too expensive: to be separated
> by bake-off before changing the matrix.

> **GPT‑6.2 Sol and Astra** : 1,05M tokens of windows, of which 922Maximum input K and 128Maximum output K.
> Cache read: $0.10/M for Sol, $0.40/M for Astra; cache write 30 min to 1,25× input, 12 h à 2,5×.
> Beyond 272K tokens of entry, input/cache rates double and the output rate is multiplied by 1,5
> the entire request. Batch is 50 % of the Standard rate; Flex is not offered on new models 6.2.
> Do not transpose these prices to the subscription quota. Sol 6.1 Medium and Astra 6 Light remain fallbacks if
> 6.2 versions are unavailable. Stewardship is a harness capacity, not model. Benchmarks
> This is not the case for models 6.2.

> **Ultrafast is a service tier, not a new model or level of effort.** Historical benchmark: for GPT-6 Astra, l'API Ultrafast
> Targets up to ~8× the speed of Standard and invoice in short context **$60/M input $6/M cached input, $75/M cache
> Write and $300/M output**. Use it only when latency actually dominates the total cost; for loops
> Agentics with many tool calls, OpenAI recommends a persistent WebSocket Responses connection.
> does not support the residence of EU data: it works in global processing or with US residence.
> product, Astra Ultrafast is included in particular in **Pro 500** and some Enterprise offers. It therefore does not change
> quality routing of this section: `Astra Standard` and `Astra Ultrafast` have the same model capacity.
> On GPT‑6.2, check the rates and rights of the plan before activation; reserves fast third parties only to loops
> interactives really limited by latency, not waiting for CI.

In **Codex / Work**, reason with visible levels **Light → Medium → High → Extra High → Ultra**. The default of this guide is **Soil Medium**, **Luna High** for micro-loops and **Astra Light** for an escalation of capacity. `Ultra` is more than a single mono-agent run and is profitable only if the work can actually break down into independent axes. API, the level names remain `low/medium/high/xhigh/max` according to the model: do not confuse the wording produced with the portable value of `reasoning.effort`.

The GPT‑5.6 models may remain available during the rollout, but they are no longer the default active route for this guide.

<!-- section: s-5 -->
#### Five dimensions not to be confused

| Lever                            | What it changes                                                                                     | Practical rule                                                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Model**                        | Capacity, speed and price: Luna, Terra, Sol 6.2 or Astra 6.2.                                 | Luna for the bounded; Sol 6.2 for repeated agentic; Astra only when the upper capacity reduces the covers. |
| **Effort**                        | Reasoning budget: wording Codex Light→Ultra; API `low/medium/high/xhigh/max` According to model. | Soil: Default Medium; Luna: High; Astra: Light; increase only if planning/verification warrants.   |
| **`reasoning.mode: "pro"`** (API) | More model work for a more reliable final response.                                    | Independent of effort; compare standard/pro on representative tasks.                                          |
| **`ultra` as an effort Codex**    | Some SDK/harness Codex now expose `ultra` as a reasoning level above `max`. | Treat it as a harness capacity, not as a portable value of Responses API.                             |
| **Ultra / Multi-Agent**           | Orchestration of several agents or sessions depending on the surface produced/API.                         | Use it only if the work actually separates into independent parts.                                          |

In **Responses API**, the maximum documented value of `reasoning.effort` remains `max` and **Multi-agent** remains a distinct beta functionality. In some harnessCodex, `ultra` may instead designate an effort of reasoning. Therefore, never deduct the semantics from the word "ultra" alone: log the surface, model, effort and actual number of agents. OpenAI does not publish a fixed cost multiplier; total cost measurement, latency and success rate on your repository before standardization.

<!-- section: s-6 -->
#### Astra: Long Mission Controls

Astra adds three capabilities that are particularly useful to agents:

```text
async tool calling
→ continuer à raisonner ou appeler d'autres outils pendant qu'un outil lent s'exécute

mid-turn steering
→ ajouter une contrainte ou changer de direction sans redémarrer toute la mission

configuration updates
→ changer l'effort en cours de trajectoire sans casser inutilement le préfixe de cache
```

For an agentic backend, prefers the **Responses API** : the tool calling Astra is the reference surface. Astra does not accept `reasoning.effort = none`neither the custom settings of `temperature` / `top_p` Documented as incompatible. **Fast mode** API can go up to ~2× faster for **2× standard price** ; it has no SLA of latency and must not become the default of a long mission.

<!-- section: s-7 -->
#### Availability and surfaces ChatGPT / Codex

| Surface                  | Model access and mode                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **ChatGPT Work / Codex** | GPT‑6.2 Sol and Astra, GPT‑6.1 Terra, Luna and fallbacks according to plan, client, workspace and rollout.                                              |
| **GPT‑6.2 Sol / Astra**  | Plus, Pro, Business, Enterprise and Edu in Codex/Work according to rights; Light→Ultra effort controls according to available parameters. |
| **GPT‑6 Luna**           | Economic model for focused and repeatable tasks in Work/Codex.                                                            |
| **Ultra / multi-agent**  | To be reserved for independent axes; do not assimilate it to "more reflection" on a sequential chain.                    |
| **API**                  | `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6-luna` via supported surfaces; check tools and effort per model.                |

The actual rights always depend on the plan, the region, the workspace and the rollout. Never code a durable product rule from the name of a subscription.

<!-- section: s-8 -->
#### Caching, security and safeguards

GPT‑6.2 Sol invoice the cached input **$0.10/M** against $2/M in standard input; cache writes remain to 1,25× input. GPT‑6 Luna down to **$0.01/M** in cached input. Stabilizes the top of the prompt (`AGENTS.md`conventions Scala, contracts, test rules) and leaves diffs, logs and errors below.

> **Two cost levers by volume.** On GPT‑6.1 Sol and GPT‑6 Luna, Batch and Flex cost 50 % less than
> Standard; on GPT‑6.2 Sol/Astra, Batch retains this reduction, but Flex is not offered.
> Use them for latency tolerance: planned audits, grouped PR summaries, set-up generation and sorting
> mass. Do not automatically transpose these tariffs API quota ChatGPT/Codex : the right indicator remains the cost per
> task completed in the actually used surface.

GPT‑5.6 remains classified "High" but not "Critical" in cyber. **GPT‑6 Astra (original generation) is the first model OpenAI classified Critical in cybersecurity** This level of capacity is accompanied by a more stringent trajectory monitoring: in the case of a new system, the ability to monitor the performance of a new system is not limited to a new system. ChatGPT/Codex, a legitimate task can be slowed down, paused or asked for validation; via API, the work can be stopped.

This increase in capacity does not justify any additional autonomy. With Astra, make even more explicit: filescope, network, external operations, destructive writing, budget, duration, shutdown conditions and human validation. Favourable point for sensitive code: **Astra supports Zero Data Retention for customers API eligible**, while Fable 5.2 imposes 30 days by default unless expressly authorized byAnthropic.

<!-- section: s-9 -->
#### Benchmarks and prudence

The Astra launch figures are particularly strong in **coding agent and computer use**, but must remain attached to their harness. OpenAI reports in particular: Terminal-Bench 4.0 **57,9 % Astra vs. 55,8 % Fable 5.1**DeepSWE 1.1 **74,1 % vs. 67,4 %**, FrontierCode Extended **64,5 % vs. 63,6 %** and its internal migration tasks DB **63,9 % vs. 57,8 %**. On AutomationBench, Astra reached **41,4 % vs. 31,4 %** for Fable 5.1These are assessments published by OpenAI : useful as a signal, never as a verdict on Scala.

The independent evaluation Artificial Analysis strongly nuances the picture. **Coding Agent Index v1.4**, Claude Code + Fable 5.1 (`max`, with fallback) gets **70** against **67** for Codex + Astra (`max`), but Astra consumes about **4,0M tokens/task against 7,1M** and costs about **$4,72/Task against $9,18**. On the **Intelligence Index**, Fable 5.1 `max` is also in front of (**66 vs 61**) The right teaching is therefore not "Astra > Fable" : **Fable keeps a small aggregate quality advantage in these protocols, Astra a major advantage of task efficiency in Codex**.

Astra also publishes a very good long context reminder on MRCR v2 : **100 % à 256–512K** and **96,3 % à 512K–1M**. Does not turn these scores into permission to send the entire monorepo: beyond 272K, its tariff increases and the *context rot* is still a problem of reasoning, not only of physical ability.

For this guide, the robust conclusion becomes:

```text
GPT‑6 Luna High = micro-dev et workers Codex sous contrôle humain fort.
GPT‑6.2 Sol Medium = défaut Codex pour l'agentic coding end-to-end.
GPT‑6.2 Sol High = feature complexe, migration et reprise difficile.
GPT‑6.2 Astra Light = escalade de capacité avant de pousser mécaniquement Sol à l'effort extrême.
Sonnet 5.5 Medium = micro-dev Claude et tâches agentiques bien spécifiées.
Opus 5.5 Medium = défaut Claude pour l'agentic coding autonome.
Opus 5.5 High = architecture, debugging et refactor difficiles.
Fable 5.2 Low = escalade frontier quand Opus High reste insuffisant.
Astra vs Fable = décider au coût par changement accepté, pas au prix par token.
```

<!-- section: s-10 -->
### GPT‑6 Astra vs Claude Fable 5.2: historical landmark of two borders

This comparison keeps the figures of the GPT‑6 Astra original: for current routing, uses GPT‑6.2 Astra If the customer proposes it. Its standard short rate is $8/$40 (cache read $)$0.40/M) ; does not attribute to him the results of the old Astra. Compare the current models on the same harness and deposit.

Compares the **model in its real harness**, not an isolated editor number. Fable 5.2 is less expensive by standard token than GPT‑6 Astra, but the cost difference per task depends on the hiding, effort, tools and repeats.

| Axis | GPT‑6 Astra | Claude Fable 5.2 | Practical consequence |
|-----|-------------|------------------|---------------------|
| Natural Harness | Codex / ChatGPT Work / Responses API | Claude Code / Messages API | Measuring the complete system |
| Standard price input / output (M tokens) | **$10 / $50** | **$8 / $40** | Fable cheaper nominally |
| Cache read (M tokens) | **$1** | **$0.20** | Advantage Fable on prefixes actually reused |
| Long context | 1,05M; overload beyond 272K | 1M; standard rate | Prefer targeted context in both cases |
| Effort | Light→Ultra on surface; API low→max | low→max ; adaptive thinking | Fable `high` for long autonomy, `low` for ad hoc advice |
| Computer use | Capable, with orchestration and tools | Strong Editing Results | Check on reproducible scenarios |
| Quality of diff mergeable | Harness assessments Codex | FrontierCode 2.0 : 49,1 % at the best effort according to Anthropic | Editing protocols do not prove general superiority |
| Independence of measures | Third-party evaluations available | Vals: equality with Opus on Terminal-Bench 4.0, reverse in multimodal | Waiting for a comparison Fable 5.2 / Astra with comparable harness |
| ZDR | Eligible customers API | 30 default days, contractual exception required | Filter tasks by confidentiality requirements |
| Long missions | Async tools, mid-turn steeling | Effort per tower, thoughting related to history | Protect status, tools and stopping rules |

**Benchmark reading.** Anthropic Announcement Fable 5.2 in front of Astra on FrontierCode 2.0FrontierSWE v2 and OSWorld 2.1, but they're **results editor**. The Coding Agent Index of Artificial Analysis Claude Code + Opus 5.5 à Codex + Astra indicates a different compromise between success rates, cost and duration; it **does not measure Fable 5.2**. Historical comparison Fable 5.1/Astra should no longer be used as a current routing rule. The independent Vals results also show that Fable 5.2 is not systematically better thanOpus 5.5.

Practical routing rule:

```text
Micro-dev interactif, humain dans la boucle
→ GPT‑6 Luna High ou Sonnet 5.5 Medium

Issue standard end-to-end
→ GPT‑6.2 Sol Medium
→ Opus 5.5 Medium en review indépendante

Architecture / root cause / refactor difficile
→ Opus 5.5 High
→ GPT‑6.2 Sol Medium/High pour challenger

Sol High insuffisant par limite de capacité
→ GPT‑6.2 Astra Light puis Medium si nécessaire

Opus High insuffisant par limite de capacité
→ Fable 5.2 Low puis Medium si nécessaire

Même tâche vraiment frontier, choix Astra vs Fable
→ deux worktrees / même spec / mêmes tests
→ comparer coût total + minutes humaines + qualité du diff
→ humain arbitre
```

Do not set a permanent couple "Claude writer / Codex reviewer". **The writer chooses by nature of task**: Sol 6.2 generally has the standard outcome; Opus 5.5 more readily possesses the architecture, debugging and refactors dominated by judgment. The other family then serves as an independent reviewer or challenger. Duplicating the two complete trajectories is only justified for a bake-off or a truly front-line decision.

<!-- section: s-11 -->
### Chinese open-weight models ([Kimi K3], GLM‑5.2, and the rest of the cluster)

Since mid-2026a third family was established next toAnthropic andOpenAI : the models **Chinese front level openers**, which achieves an agentic coding close to Sonnet/Opus at a much lower cost per token. For a senior Scala who is already piloting Claude Code and Codex, they're not replacements for the daily driver, but **a cost lever on a specific class of subtasks** and one **sovereignty option** (self-host) for sensitive code.

**Category trap to be set out from the outset** : these models are not **not** in the same category as Qwen3-Coder-Next. Qwen Local (80B/3B actives) is really exploitable on your laptop 128 Go: Q4_K_M leaves a very wide margin, Q5_K_M is the best defect and Q6_K remains viable. Q8_0 can be loaded, but must be validated with context, IntelliJ and sbt really open. GLM‑5.2 (753B) and above all Kimi K3 (2.8T) do not hold **not** local on 128 Go: These are models **API** (Zai, Moonshot, OpenRouter) or **self-host on multi-GPU server**. Moonshot recommends a deployment Kimi K3 on config 64+ accelerators. So never put them in the box " Qwen local": they live in the box " API third party" or "team server".

| Model      | Editor / access                                                                                                    | Architecture                                                                                             | Background                 | Price API (in / out /M)                | Perf benchmark (independent measures / editor)                                                                                             |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Kimi K3** | Moonshot — API, OpenRouter (`moonshotai/kimi-k3`), Kimi Code CLI; **published full weights** licensed Kimi K3 | MoE 2.8Total T, **104B activated** ; 896 experts, 16 KDA + Warning Residuals, native vision    | Up to 1M according to the plan | **$3 / $15** (cache-hit input $0.30)  | Scanners editor with max effort and several harnesses; excellent frontend and long-horizon signals, to be confirmed on Scala                   |
| **GLM‑5.2** | Zipu/Z.ai — API OpenAI- **and Anthropic-compatible**, GLM Coding Plan; MIT checkpoint published                      | MoE **753B** Total BF16 ; active number not officially documented; sparse attention « IndexShare » | 1M                       | **$1.40 / $4.40** (cache input $)$0.26) | Scores editor : SWE-bench Pro **62.1**, TerminalBench 2.1 81.0 with Terminus-2 and 82.7 better harness; compare to identical protocol |

**Effort of reasoning.** GLM‑5.2 Exhibit **High** and **Max**. Kimi K3 Exhibit `reasoning_effort: low | high | max`. The template page/API indicates **`max` default**, while Kimi Code can define a different defect according to its version and plan: therefore always sets the effort explicitly in a benchmark or automation. 1M depends on the plan: 256K on Moderato, up to 1M on Allegretto and above. For a short interactive task, start at `low` or `high` ; reservation `max` long missions where the cost of exit is justified.

<!-- section: s-12 -->
#### Where they enter *ton* routing

```text
✅ Review de volume et triage à faible enjeu   → GLM‑5.2 (High) : tarif token très inférieur à Opus, mais coût par tâche à mesurer
✅ Extraction, classification, PR summaries bulk → GLM‑5.2 ou Kimi K3, en batch, quand le volume rend Sonnet/Terra cher
✅ Génération frontend / maquette web           → Kimi K3 (#1 Frontend Code Arena) si tu sors du périmètre Scala pur
✅ Second avis open-weight indépendant          → un modèle d'une 3e « école » d'entraînement casse les angles morts communs Claude/GPT
✅ Code sensible / air-gapped / souveraineté     → GLM‑5.2 en self-host (poids MIT) : rien ne sort de ton infra
```

```text
❌ Driver quotidien Scala à la place de Sonnet 5.5 : capable, mais tu perds l'écosystème (Claude Code, subagents, Metals MCP mûrs)
❌ Tâche interactive courte sur Kimi K3 en effort max : latence et verbosité, mauvais achat ; utiliser low/high
❌ Décision d'architecture critique en solo : garde Opus/Fable ou un vrai second avis Sol ; l'open-weight y reste un challenger, pas l'arbitre
❌ « Remplacer » Qwen local : mauvaise catégorie (voir piège ci-dessus)
```

<!-- section: s-13 -->
#### Occasional access to GLM via OpenRouter

For this workflow, do not add a dedicated GLM subscription by default. **GLM remains a backup model**, to call via OpenRouter when Claude Code, Codex and Qwen local did not resolve the problem. This preserves the diversity of models without adding a new account, key and plan to follow.

If GLM becomes a tool used every week or brings a measurable gain on a task class, then re-evaluates the value of direct access Z.ai. As long as this threshold is not reached, simplicity prevails.

<!-- section: s-14 -->
#### The rest of the cluster (to locate, not to adopt everything)

`MiniMax M3` (June 2026) is the first open-weight to combine border coding, context 1M *and* native multimodality (openweight head on SWE-bench Pro to 59.0 before GLM‑5.2). `DeepSeek V4` declines a V4 Pro and V4 Flash ($)$0.14/$0.28 /M) unbeatable on the long cost/context ratio for massive sorting. None is "best everywhere": the mid-size open-weight scene.2026 is a tight cluster where the right choice depends on the task and price, not a global ranking.

<!-- section: s-15 -->
#### Two reserves to keep in mind

1. **Provenance and distillation.**Kimi K3 identified itself as "Claude" in at least one reported exchange. This anecdotal self-identification **is not proof of distillation** and does not allow any scientific or contractual conclusions on training data. If provenance counts for a customer, requires documentation from the publisher and treats information as unknown until it is published.
2. **Benchmark methodology.** The editor tables mix different harnesses (KimiCode, Claude Code, Codex, mini-SWE agent) and K3 is sensitive to preserving the history of *thinking*. The deviations displayed are often less than one point: they do not always survive a change of harness. Rule unchanged: **bake-off controlled on your real tasks** (fixed versions, fixed permissions, deterministic acceptance tests, cost per change accepted), not adopted on the basis of a ranking.

<!-- section: s-16 -->
#### Bake-off protocol Scala: Kimi K3 against GLM‑5.2

Not only compares the final responses. Uses as a minimum **15 private tasks**, never published, divided between:

```text
3 bugs Scala 3 subtils : givens, implicits, variance, types opaques
3 évolutions Play / Tapir / Pekko sur 3 à 8 fichiers
3 tâches Spark / concurrence / performance
3 reviews de PR avec défauts injectés connus
3 tâches de tests : ScalaTest, ScalaCheck, mutation testing
```

Protocol: same commit, same initial worktree, same tools, same time limit, same network, same context package, same shutdown criteria and **three repetitions per task**. Kimi should be tested separately in `high` and `max`; GLM in `High` and `Max`. If the harnesses cannot be identical, publish two matrices and do not assign the deviation to the model alone.

Mandatory measures:

```text
- tâche acceptée par les tests et la review humaine ;
- compilation, tests ciblés, mutation score ;
- défauts de sécurité ou de contrat détectés ;
- lignes ajoutées / supprimées et fichiers touchés ;
- nombre de reprises, tool calls et boucles identiques ;
- tokens input, cache, reasoning et output ;
- coût API total, latence et minutes humaines jusqu'au merge ;
- taux de réussite pass@1 et stabilité sur trois runs.
```

Adopts GLM or Kimi on a stream only if it reduces the cost per accepted change**without** degrade the safeguards. A higher editor score but more human corrections is a regression, not a gain.

<!-- section: s-17 -->
## Decision-making rule by task

<!-- section: s-18 -->
### When to use **Fable 5.2** (Mythos-class)

Fable 5.2 costs twice Opus 5.5 per token ($8/$40 against $4/$20). Anthropic recommends starting with **Opus 5.5 `medium`**, to climb to `high`, then reserve Fable 5.2 to the still insufficient valleys or on the real long- horizon. For an escalation of capacity, test **Fable `low`** before systematically pushing Opus to `Extra`/`Max` :

```text
✅ Migration complète d'un framework (Play 2 → 3, Pekko, Spark upgrade)
✅ Session autonome multi-heures / multi-jours sans supervision
✅ Refactor cross-modules sur > 10 fichiers interdépendants
✅ Débogage d'un bug métier dont la cause est très loin du symptôme
✅ Décision architecturale sans "bonne réponse évidente" après essai Opus 5.5 High
✅ Tâche où tu paierais sinon un senior engineer une demi-journée
```

```text
❌ Tâche bien scoped et bornée : Sonnet 5.5 ou Opus 5.5 sont de meilleurs achats
❌ Revue de diff ou PR summary : overkill, coût inutile
❌ Génération de boilerplate ou de fixtures : Qwen ou Haiku suffisent
❌ One-liner ou patch ciblé : Luna High, Sonnet 5.5 Medium ou Aider
❌ Tâche dure mais interactive avec toi dans la boucle : Opus 5.5 Medium/High suffit généralement
```

> **Positioning 5.2.** Anthropic recommends that you keep **Opus 5.5 as a starting point** for most of the
> workloads. Fable 5.2 `low` is a ** advisor on a point**, to be evaluated on a limited and verifiable task; for a mission
> really autonomous, starts to `high` in order to reduce premature tour ends. **cost per change
> accepted** on the private benchmark Scala, rather than generalizing the results of the supplier.
> $0.20/M improves the economy of long stable prefixes. When the verifier is reliable, also test the schema
> **Low → retry High overfail** including recaptures, latency, review and human validation.

<!-- section: s-19 -->
### Prompting Fable 5.2: Structure a long mission

Fable 5.2 (window 1M, exit until 128K) is not just a stronger Opus. It aims at demanding reasoning and the long-horizon when Opus evaluations remain insufficient. The continuity of thinking blocks and the stability of tool definitions become constraints of harness, in addition to the effort configurable by message. Reference: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2`. The levers below remain valid for 5.2 ; points specific to 5.2 (ownership of the code, over-delegation, premature turn ends, historical append-only, inherited instructions to be purged) are detailed in the note Fable 5.2 of the section on "Coast Anthropic ».

Five specific levers:

1. **Charter of mission at the head of context, hidden.** The initial block (objective, non-objective, invariant, stopping rules) must never change between the towers: it benefits from the prompt caching and serves as an anti-driving anchor on long sessions. Everything that evolves (state, errors, diffs) goes after.
2. ** Explicit persistent state.** On a multi-hour mission, requires a state file (`MIGRATION_STATE.md` in the worktree) that the model updates at each milestone: processed modules, remaining modules, decisions made, blockages. It is this file — not the conversation — that is the basis for context compaction or recovery.
3. **Checkpoints with exit criteria.** Cuts the mission into verifiable milestones by deterministic commands (`compile`, targeted tests, scalafmtCheckAll). No transition to the next milestone without current green milestone.
4. **Routes the effort by turn without changing the model.** Use`medium/high` for exploration, `xhigh/max` for a really difficult decision, then `low/medium` for a mechanical edition. The per-message effort preserves the cache and avoids paying the maximum level throughout the trajectory.
5. **If a compaction is necessary, impose its summary contract.** Request to explicitly preserve problems and resolutions, tried or discarded tracks, decisions and constraints, current state, open points and details difficult to rebuild. The server compaction already manages this need; for a client-side compaction, never sum up in free prose without these fields.

Mission Template Fable 5.2:

```text
# MISSION (statique — ne pas modifier en cours de session)
Objectif : [migration / refactor précis]
Non-objectifs : [ce qui est explicitement hors scope]
Invariants : API publiques, contrats JSON, comportements listés dans AGENTS.md
Durée max : [N heures] — Coût max : [N USD] — Diff max par jalon : [N lignes]

# RÈGLES D'ARRÊT (statique)
Stop et rapport immédiat si :
- un invariant doit être violé pour avancer ;
- le même jalon échoue 2 fois pour des causes différentes ;
- build.sbt, migration DB ou contrat public doit changer ;
- l'estimation de durée restante dépasse 2x l'estimation initiale.

# PROTOCOLE (statique)
1. Lire AGENTS.md et MIGRATION_STATE.md.
2. Traiter UN jalon : plan court → diff → compile → tests ciblés.
3. Mettre à jour MIGRATION_STATE.md et committer le jalon.
4. Rapport de progression : jalon terminé, jalons restants, risques nouveaux, écart au plan.
5. Reprendre en 2.

# ÉTAT (dynamique — joindre la version courante de MIGRATION_STATE.md)
[état]
```

> **Contingency Fable 5.2.** Don't silently downgrade a session: Fable 5.1 and Opus 5.5 do not reread the
> Fable 5.2 Thinking blocks also does not edit old messages, system prefix or tool list
> by reusing these blocks: consistency control can produce an error 400. If a change in tools or tools
> model is indispensable, saves the useful state in `MIGRATION_STATE.md`, then repars with a proper context.
> `tool_choice: any/tool` is prohibited on Fable 5.2; uses `auto` and validates the result with a strict schema.

> **Operational Note**: A security switch can change the actually executed model.
> low-level crypto code or security, log this model, check that it retains the expected and anticipated capacity level
> this case in the stop rule rather than discover it during session.

<!-- section: s-20 -->
### When to use **Opus 5.5**

That's it. **default Claude Code for autonomous agentic coding**. Its default effort is `medium`, which changes the routing compared to Opus 5 : starts at `medium`, up to `high` when the task is difficult, then use `Extra` (`xhigh`) or `Max` that if the duration or the events justify it.

```text
✅ Issue complète quand Claude possède la trajectoire exploration → patch → tests
✅ Architecture, migration et plan multi-modules
✅ Root cause éloignée du symptôme, implicits/givens/effets difficiles
✅ Gros refactor où la cohérence globale domine la simple édition
✅ Review indépendante d'une PR écrite par Codex
✅ Orchestration de sous-agents read-heavy avec contexte isolé
```

```text
medium → défaut agentique
high   → debugging / architecture / long-horizon difficile
Extra  → >30 min et chaîne réellement longue ; pas pour une simple tâche "importante"
Max    → exceptionnel, qualité absolue prioritaire et gain mesuré
```

<!-- section: s-21 -->
### When to use **Sonnet 5.5**

The best choice Claude when ** the senior keeps his hand strongly** or when the agentic task is well specified. Anthropic explicitly recommends `medium` for agentic coding and multistep use of well-structured tools, then `high` for longer or difficult tasks.

```text
✅ Petit bug reproductible
✅ Refactor local bien scoped
✅ Tests métier et property-based tests ciblés
✅ Stack trace → diagnostic → correctif
✅ Feature claire dont l'architecture est déjà décidée
✅ Worker d'implémentation derrière un plan humain ou Opus
```

```text
low    → transformation simple / latence prioritaire
medium → défaut micro-dev et agentic coding bien spécifié
high   → tâche plus longue ou plus difficile
Extra / Max → seulement si tes evals montrent un gain ; sinon passer à Opus 5.5
```

The economic rule is no longer "Maximum effort Sonnet before Opus." If Sonnet High fails for a capacity limit, ** Opus Medium** is often a better purchase than an extended Sonnet Extra/Max.

<!-- section: s-22 -->
### When to use **Haiku 5.5**

Systematically for tasks *high frequency and low risk*:

```text
✅ Sous-agents de lecture ou extraction à faible risque (sortie vérifiable)
✅ Résumés de logs, PR summaries rapides
✅ Classification et routage
✅ Éditions ciblées < 20 lignes
✅ Génération de messages de commit
✅ Appels répétitifs à faible risque, si le benchmark confirme le gain
```

> **Haiku 5.5 replace Haiku 4.5 like worker Claude.** It costs **$0.10/$0.50** as long as the prompt
> remains under 100 000 tokens (cache read $0.01/M), i.e. ** ten times less than Haiku 4.5** and the same price order as
> GPT‑6 Luna ; beyond 100K tokens of entry, cache included, rate increases to $0.50/$2.50Background 1M, exit 128K,
> Adaptive thinking active by default and ** parameter `effort` supported (`medium` by default)**. Migration traps:
> the prefill now returns 400, `temperature`/`top_p`/`top_k` are to be omitted, `budget_tokens` returns 400, the
> thinking counts in `max_tokens`, and a forced `tool_choice` remains accepted but removes reflection before the call.
> The tokenizer has about 30 % more tokens than Haiku 4.5. Practical rule: keep subagent contracts
> **under 100K tokens** to stay in the lower landing, which joins the isolation discipline of the section 3.
> Haiku 4.5 remains active, but withdrawal is now possible at any time with the usual 60 days' notice.

<!-- section: s-23 -->
### When to use **GPT‑6 Luna**

```text
✅ Micro-dev : modification locale dont tu contrôles la direction
✅ Tests simples, fixtures, boilerplate, renommages et transformations mécaniques
✅ Recherche d'occurrences, résumés, logs et PR summaries
✅ Worker/subagent dont la sortie est vérifiée immédiatement
```

OpenAI recommends to start Luna at **High**. Don't try to turn Luna into a border agent with Extra High: if the task becomes ambiguous or conceptual, go to Sol 6.2 rather than paying for long times on a too small model.

<!-- section: s-24 -->
### When to use **GPT‑6.2 Sol**

```text
✅ Issue standard complète : découverte → implémentation → tests → PR
✅ Feature multi-fichiers et bug non trivial
✅ Review indépendante d'une PR écrite par Claude
✅ Migration bornée, compatibilité et refactor transversal
✅ Second avis sérieux sur une architecture proposée par Opus
```

```text
Light       → issue très bien spécifiée, patch local, reproduction claire
Medium      → défaut agentique quotidien
High        → feature complexe, root cause difficile, migration, beaucoup de cas limites
Extra High  → capacité suffisante mais besoin réel de davantage d'analyse/vérification
Ultra       → uniquement si le travail se décompose en investigations indépendantes
```

<!-- section: s-25 -->
### When to use **GPT‑6.2 Astra**

```text
✅ Sol High échoue parce que la capacité/jugement manque, pas parce que le contexte est pollué
✅ Sécurité, auth, contrat critique ou décision où une mauvaise direction coûte plusieurs reprises
✅ Workflow end-to-end très ambigu avec nombreux outils / computer use
✅ Reviewer frontier ponctuel sur une décision à fort impact
```

Starts with ** Astra Light**. For a task that is really front-end, Astra Light can cost less in total than a Sol Extra High followed by a recovery, because it avoids a bad trajectory. Go up to Medium/High only if necessary; Extra High/Ultra remains exceptional.

<!-- section: s-26 -->
### When to use **mode `ultra` in ChatGPT Work / Codex**

```text
✅ Cartographie codebase-scale d'une application legacy
✅ Migration multi-modules en worktree dédié
✅ Audit architecture + tests + sécurité + performance en parallèle
✅ Décomposition d'un refactor en micro-PRs
✅ Mission où plusieurs sous-analyses indépendantes apportent une vraie valeur
```

```text
❌ One-shot “réécris proprement”
❌ Tâche interactive courte
❌ Repo mal testé sans limite de diff
❌ Modification directe de fichiers critiques sans plan validé
```

In this subsection, `ultra` refers to the ** multi-agent orchestration mode of the product**, and not to the level of effort `ultra` that some SDKs Codex now expose. It is suitable for independent shutters; avoid it when agents write in the same mutable state or when a single slow operation dominates the task. On a legacy application, start by mapping, producing a debt register, proposing characterization tests, and then cutting into micro-PRs. Do not start by writing code.

Minimum Mission Template `ultra`:

```text
Tu interviens comme équipe de reviewers/agents sur une application legacy Scala.

Rôles à simuler :
- architecte legacy ;
- tech lead Scala ;
- reviewer sécurité défensive ;
- QA / test engineer ;
- maintainer sceptique.

Objectif :
[objectif précis]

Contraintes :
- aucun changement de comportement observable sans validation ;
- pas de modification build.sbt / migrations DB / contrats JSON publics sans stop ;
- micro-PRs de moins de 300 lignes modifiées ;
- tests de caractérisation avant refactoring ;
- chaque conclusion doit citer les fichiers observés ;
- distinguer faits, hypothèses et recommandations.

Sortie attendue :
1. carte du périmètre ;
2. risques ;
3. registre de dette ;
4. tests de caractérisation prioritaires ;
5. plan en micro-PRs ;
6. première PR proposée, sans l'appliquer tant que le plan n'est pas validé.
```

<!-- section: s-27 -->
## Fast model selection matrix

```text
Micro-dev, humain garde le contrôle      → GPT‑6 Luna High / Sonnet 5.5 Medium
Worker lecture / triage à faible risque  → Haiku 5.5 / Qwen local / GPT‑6 Luna
Patch local au jugement intermédiaire    → GPT‑6.1 Terra Medium
Issue standard end-to-end                → GPT‑6.2 Sol Medium
Agent Claude end-to-end                  → Opus 5.5 Medium
Feature / bug difficile                  → GPT‑6.2 Sol High ou Opus 5.5 High selon nature
Architecture / root cause dominante      → Opus 5.5 High
Review croisée                           → famille opposée à l'auteur, Medium par défaut
Suivi post-PR Codex                       → GPT‑6.2 Sol Medium (Goal / Heartbeat / Cloud)
Sol High insuffisant                     → GPT‑6.2 Astra Light
Opus High insuffisant                    → Fable 5.2 Low
Long-horizon séquentiel > 30 min         → Opus 5.5 Extra (`xhigh`)
Codebase-scale parallélisable            → GPT‑6.2 Sol Ultra, surtout read-heavy
Frontier absolu                          → Astra Medium+ / Fable Medium+ après preuve du besoin
```

Practical rule:

```text
Le senior garde la direction → modèle rapide et économique.
L'agent possède la trajectoire → Sol 6.2 ou Opus 5.5.
La compréhension domine le patch → privilégier Opus.
L'exécution end-to-end domine → privilégier Sol 6.2.
Une limite de capacité apparaît → Astra Light ou Fable Low avant l'effort extrême du tier inférieur.
Ultra uniquement si le problème contient plusieurs axes réellement indépendants.
```

<!-- section: s-28 -->
## Automatic routing of development tasks

The selection matrix should not be left only manual. To avoid burning credits on simple tasks or, conversely, sending a critical task to a too weak model, adds an explicit routing step before each agent task.

The principle is not to choose the smartest model, but the smallest model capable of producing a mergeable result with an acceptable risk.

```text
Demande / ticket / stack trace
→ classification de tâche
→ estimation difficulté + risque
→ sélection du modèle minimal acceptable
→ exécution avec permissions limitées
→ tests déterministes
→ escalade si échec
→ log coût / qualité
```

<!-- section: s-29 -->
### Recommended architecture

```text
CLI / IDE / ticket
→ task-classifier
→ context-builder
→ model-router
→ agent-runner
→ test-runner
→ reviewer
→ cost-quality log
```

| Component          | Role                                                         | Recommended template/tool                                                                             |
|--------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `task-classifier`  | Sorting the task, risk and difficulty                 | **Jev** if exit is closed; Qwen local / Haiku if open reasoning is required         |
| `context-builder`  | Find useful files, relationships, tests, docs and commands | Sourcebot, ScalaSemantic MCP, Codebase-Memory MCP if polyglot, rg, IntelliJ, Metals MCP, Context7   |
| `model-router`     | Choose the smallest acceptable model                      | Deterministic rules + Jev as a probabilistic signal; OpenRouter only for point climbing  |
| `agent-runner`     | Run with the right permissions                         | Codex, Claude Code subagents, Aider, OpenCode, Qwen Code                                              |
| `test-runner`      | Validate in a deterministic manner                              | sbt, IntelliJ, Metals MCP, CI                                                                         |
| `reviewer`         | Reread without writing                                           | Family opposed to the writer: Opus 5.5 Medium or GPT‑6.2 Sol Medium; Astra/Fable only if critical |
| `cost-quality log` | Measuring cost, quality, feedback and feedback            | Local Scripts, follow-up table                                                                      |

<!-- section: s-30 -->
### Jev: decision layer, not coding model

**Jev 1.14 (`jev-1.14.0`)** is the current System One model of TypeSafe AI. It does not generate text or code: it receives a `state` and typified questions, then directly refer probabilistic decisions. The right mental model is a **Semantic smart if** : open entry, branches defined by the developer.

| Primitive | Use                                                           |
|-----------|-----------------------------------------------------------------|
| `Choice`  | choose from closed options: model, agent, skill, route |
| `Score`   | rate on an orderly scale: risk, relevance, priority   |
| `Noul`    | estimate the likelihood of a proposal being true            |

Jev 1.14 Cost **$0.042/M tokens input** and does not charge the output. The standard regime accepts **64K tokens per request** and **32K for `state` + the longest question** The flow limits depend on the organization and are read in the console. A longer experimental context and the image inputs exist under conditions, without becoming the default of the router. `jev-latest` point towards `jev-1.14.0` : **pin the version** as soon as you calibrate the thresholds, because the change in distribution can invalidate the risk thresholds.

> **OpenAI Decisions API.** Endpoint `POST /v1/decisions`, now generally available `gpt-6-luna`, avec
> typed answers `predicate`, `choice` and `score`. Up to **400 questions** can share the same entry; text,
> Images and structured data are supported according to the field. Standard price: **$0.10/M input tokens**, **$0.01/M
> cache entry tokens read**, no output billing; cache entries, long entries and processing
> The Commission will continue to monitor the implementation of the regional `task-classifier` and `model-router`, compares Decisions and Jev on the same
> questions with calibration by task and risk, never on the price of the token alone.

In this workflow, the best candidates are:

```text
✅ task / risk / difficulty classification
✅ model routing : Luna / Sol / Astra / Sonnet / Opus / Fable
✅ sélection progressive de quelques skills parmi un gros catalogue
✅ triage des résultats de subagents et pertinence d’un contexte
✅ signal topic-shift / « faut-il envisager une compaction ? »
✅ filtrage de notifications et décisions qui méritent l’attention humaine

❌ écrire ou expliquer du Scala
❌ architecture ou root-cause ouverts
❌ calcul, comptage ou comparaison de dates
❌ décider seul d’un push, déploiement, suppression, secret ou migration DB
```

Recommended architecture:

```text
règles déterministes
→ Jev pour un jugement fermé et fréquent
→ code combine probabilités + seuils
→ LLM génératif si raisonnement ouvert ou confiance insuffisante
→ humain si action critique ou irréversible
```

**Safety type** The argument "zero hallucinations" means above all that Jev does not come out of a declared structure or set of options; it can always select the wrong option. **346 009 requests / 37 dataset** find probabilities `Choice` This is the case for the European Union, which is the European Union's largest trading partner. `0.5` is bad for some binary tasks: thresholds must be **calibrated by task and risk**.

Three rules of integration:

1. **The code retains authority.** Deterministic signals (`touches_security`, critical file, destructive action) always take precedence over Jev.
2. **Minimum state.** Jev also undergoes the *context rot*; filter before the call and only sends what really changes the decision.
3. **Tests stability.** On `Choice`, periodically reorders options; assessments of `jev-1.13` indicate a possible sensitivity to order, to be revalidated on `jev-1.14.0`. The `state` adversarial can also influence the response: Jev is a signal, not a sandbox.

<!-- section: s-31 -->
### Minimum classification

The router must produce a structured decision, not a free answer. Example of expected exit:

```json
{
  "task_type": "implementation | debug | test | review | migration | architecture | boilerplate | research",
  "risk": "low | medium | high | critical",
  "difficulty": "trivial | simple | normal | hard | frontier",
  "expected_files": "1 | 2-5 | 6-10 | 10+",
  "requires_code_write": true,
  "requires_external_docs": false,
  "touches_public_api": false,
  "touches_json_contract": false,
  "touches_database": false,
  "touches_build": false,
  "touches_security": false,
  "touches_concurrency": false,
  "model": "qwen | haiku55 | sonnet55 | opus55 | fable52 | gpt6_luna | gpt61_terra | gpt62_sol | gpt62_astra | gpt61_sol | gpt6_astra",
  "reasoning_effort": "light | low | medium | high | extra | xhigh | max | ultra | null",
  "reasoning_mode": "standard | pro | null",
  "multi_agent": false,
  "max_parallel_agents": 3,
  "max_cost_usd": 0.0,
  "max_duration_minutes": 0,
  "confidence": 0.0,
  "escalation_rule": "string",
  "stop_conditions": [
    "string"
  ]
}
```

**Hierarchy of signals** : deterministic criteria (`touches_*`, `expected_files`, expected diff size) are the triggers *Primary* and climbing. If classification comes from **Haiku/Qwen**, `confidence` is a secondary and poorly calibrated self-assessment. **Jev**, uses distribution and `confidence` turned, but with a **threshold calibrated by question and level of risk**, never a `0.75` In both cases, high confidence must never be achieved. *de-escalating* A critical deterministic signal.

`reasoning_effort` must be standardized by surface: Claude uses `low | medium | high | xhigh | max` on compatible models, with **Opus 5.5 and Haiku 5.5 `medium`** default; Codex display **Light | Medium | High | Extra High | Ultra**, whileAPI OpenAI expounds values `low | medium | high | xhigh | max` According to model. `multi_agent` The effort is a lever of quality and cost, but a higher tier with low effort can be cheaper in total than a lower tier pushed to the extreme.

<!-- section: s-32 -->
### Automatic routing matrix

| Signal detected                                               | Initial model                | Climbing                                                                      |
|--------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------|
| Summary, sorting, grep, simple logs                           | Haiku 5.5 / Qwen              | Sonnet 5.5 Medium if ambiguous                                                   |
| Boilerplate, DTO, fixtures, mechanical edition                | GPT‑6 Luna High               | Sonnet 5.5 Medium if subtle types/domains                                    |
| Simple or non-regression localized test                      | GPT‑6 Luna High               | Sonnet 5.5 Medium if important business rule                                  |
| Patch targeted, human keeps the direction                       | Luna High / Sonnet 5.5 Medium | Sol 6.2 Light/Medium if exploration required                                |
| Patch bounded with intermediate judgment                      | GPT‑6.1 Terra Medium           | GPT‑6.2 Sol Medium if exploration necessary |
| Business feature bounded, 1 to 5 files                        | GPT‑6.2 Sol Medium            | Sol High if difficulty; Opus Medium in review                                |
| Feature 5 to 10 files with invariants                      | GPT‑6.2 Sol Medium/High       | Opus 5.5 High if architecture/root cause dominates                               |
| Bug Scala subtle, implicable, givens, effects                  | Opus 5.5 High                 | Sol High for independent hypothesis; Fable Low if insufficient capacity     |
| Multi-module bounded migration                               | GPT‑6.2 Sol High              | Opus High in review; Astra Light if Sol cap                             |
| Refactor codebase-scale                                      | Opus 5.5 High                 | Extra so long-horizon ; Fable Low if Opus cap                            |
| Review of a PR Codex                                        | Opus 5.5 Medium               | High if critical risk                                                       |
| Review of a PR Claude                                       | GPT‑6.2 Sol Medium            | High then Astra Light if risk border                                      |
| Independent monitoring of a PR Codex                               | GPT‑6.2 Sol Medium            | High if difficult diagnosis; Sol 6.1 Medium if 6.2 unavailable             |
| Security / Auth / Critical Contract                           | GPT‑6.2 Astra Light + human    | Astra Medium/High + review Opus High                                          |
| Independent read-heavy axes                                 | GPT‑6.2 Sol Ultra             | Astra Ultra only if additional capacity is actually needed |
| Change `build.sbt`, dependencies, DB, public contract JSON | No self-writing           | Plan + Human validation                                                     |

<!-- section: s-33 -->
### Climbing policy

The automatic routing must function as a controlled cascade:

```text
Micro-boucle vérifiable : Qwen / Haiku / GPT‑6 Luna High / Sonnet 5.5 Medium
→ ownership agentique : GPT‑6.2 Sol Medium / Opus 5.5 Medium
→ difficulté : Sol High / Opus High
→ limite de capacité : Astra Light / Fable Low
→ effort supérieur seulement si la capacité est suffisante mais le raisonnement manque
→ Ultra seulement si parallélisable
→ humain
```

**Don't just change a pattern in the middle of a derailed conversation.** If failure comes from a polluted trajectory — repeated false hypothesis, accumulating hallucinations, corrections that recreate other errors — the context is itself part of the problem. Sonnet 5.5 → Opus 5.5, Sol 6.2 → Astra or Opus 5.5 → Fable 5.2 :

```text
1. Stop write mode.
2. Produire HANDOFF.md : objectif, état du diff, faits vérifiés, essais échoués, erreur actuelle, inconnues.
3. Ouvrir une session fraîche avec seulement spec + AGENTS.md + HANDOFF.md + fichiers/diff pertinents.
4. Escalader le modèle dans cette nouvelle session si la difficulté le justifie toujours.
```

The escalation of **capacity** is useful on a problem properly posed; it must not carry the conversational debt of an already biased session.

Climb automatically if:

```text
- un signal déterministe critique est présent (touches_* sensible, diff hors gabarit) ;
- auto-confidence LLM < 0.75, ou confidence Jev sous le seuil calibré pour cette décision ;
- erreur de compilation identique 2 fois ;
- test ciblé toujours rouge après 2 corrections ;
- diff hors scope ;
- plus de fichiers modifiés que prévu ;
- plus de 300 lignes de diff inattendues ;
- build.sbt, plugins.sbt, migration DB ou contrat JSON public est touché ;
- API publique modifiée ;
- le routeur détecte sécurité, concurrence, performance ou argent ;
- le modèle déclare explicitement une incertitude forte ;
- le coût estimé d'une erreur dépasse le coût du modèle supérieur.
```

Interromps (without automatically climbing) if:

```text
- max_cost_usd est atteint (budget local) ;
- max_duration_minutes est atteint (timeout wall-clock) :
  une session agentique qui boucle est un mode de défaillance distinct d'une session qui échoue,
  et l'escalade vers un modèle plus cher ne corrige pas une boucle.
```

De-escalation automatically if:

```text
- tâche purement textuelle ;
- aucun write mode nécessaire ;
- pas de risque métier ;
- moins de 20 lignes attendues ;
- fichier unique ;
- objectif déterministe ;
- test existant très ciblé ;
- contexte stable et déjà connu du projet.
```

<!-- section: s-34 -->
### Non-automatic rules

Never let a router decide alone to write on:

```text
- build.sbt ;
- plugins.sbt ;
- resolvers ;
- versions de dépendances ;
- migrations DB ;
- contrats JSON publics ;
- sécurité ;
- authentification ;
- autorisation ;
- concurrence ;
- gestion d'argent ;
- suppression de données ;
- scripts de déploiement ou d'infrastructure.
```

In these cases, the router can only propose:

```text
- modèle recommandé ;
- plan ;
- fichiers probables ;
- tests à exécuter ;
- risques ;
- règle d'arrêt.
```

<!-- section: s-35 -->
### Recommended subagents Claude Code

**Calibration Codex 6.2.** For a parent GPT‑6.2 Sol or Astra, go with the same model and effort for subagents (official recommendation) OpenAI) Then reduce the trier of the really mechanical tasks, with controllable output: Luna/Haiku for grep, extraction, logs and abstracts; Sol/Opus for invariants, architecture and root cause. The same principle of measurement applies to Claude. A reviewer of the other family remains an independent session, not a less expensive worker of the author.

Claude Code is the best place to apply this routing on a daily basis, as subagents can have their own context, tools and permissions.

```text
researcher
- Modèle : Haiku / Qwen si externe
- Mode : read-only
- Rôle : trouver fichiers, usages, tests, documentation

scala-implementer
- Modèle : Sonnet 5.5 `medium`
- Mode : write limité au repo
- Rôle : implémenter les tâches bornées sous contrôle d’un plan clair

hard-debugger
- Modèle : Opus 5.5 `high`
- Mode : write limité, plan obligatoire
- Rôle : bugs Scala subtils, implicits, effets, causes éloignées

migration-planner
- Modèle : Opus 5.5 `high` ; Fable 5.2 `low` (décision ponctuelle) ou `high` (mission longue) si Opus plafonne
- Mode : plan-first, worktree dédié
- Rôle : migrations multi-modules, refactors longs, stratégie de découpage
- Note : évaluer Dynamic Workflows (Opus 5.5 + subagents parallèles massifs)
  comme alternative à un Fable mono-agent sur les migrations codebase-scale

reviewer
- Modèle : Codex / GPT‑6.2 Sol `medium` ; Astra `light` si critique
- Mode : no-write
- Rôle : review indépendante, classement bloquant / important / optionnel

pr-summarizer
- Modèle : Qwen / GPT‑6 Luna
- Mode : no-write
- Rôle : résumé PR, release notes, checklist finale
```

<!-- section: s-36 -->
#### Context isolation: main role of subagents on long tasks

The gain of subagents is not just parallelism. Each subagent works in a ** fresh and isolated context window**; therefore the parent does not need to accumulate the searches, logs, files and dead ends of each subaspect. This isolation protects the main context against the *rotation context*.

The recommended sharing is:

```text
PARENT
- objectif
- contraintes et non-objectifs
- plan validé
- décisions prises
- diff courant
- preuves essentielles
- risques ouverts

SUBAGENTS
- exploration de nombreux fichiers
- recherche Sourcebot / rg
- call paths, hiérarchies, usages et chaînes de givens via ScalaSemantic
- graphe structurel cross-language via Codebase-Memory si Java/Kotlin/Scala cohabitent
- investigation live des types / givens / diagnostics via Metals
- documentation externe
- logs et suites de tests volumineuses
- cartographie d'un module legacy
```

Rule of Decision:

```text
Les détails de cette sous-tâche seront-ils encore utiles au parent après sa fin ?

NON → subagent isolé
OUI → garder dans le contexte parent
```

The delegation message must be a ** contract**, as the subagent must not depend on the entire conversational history of the parent:

```text
Mission :
[périmètre précis]

Mode :
read-only / write borné

Cherche :
[questions précises]

Ne fais pas :
[hors scope]

Retourne uniquement :
1. conclusion ;
2. preuves file:line ;
3. tests ou commandes pertinents ;
4. incertitudes restantes.

Réponse cible : < 1–2K tokens.
```

Return is an interface, not a transcript. 80K tokens and send them back 1,5K, insulation is useful; if it is in bed 10K and send it back 8K, he mainly moved the noise. A simple metric to follow on long tasks is:

```text
isolation_ratio
= tokens consommés par le subagent
/ tokens retournés au parent
```

So the right pattern is **map → reduce** Several specialized workers spend local context, then the parent synthesizes some short results. Avoids the reverse anti-pattern — seven agents who each read the repo and return ten-page reports — which recreates the *context rot* in the root context.

For ** your solo workflow Scala**, also treats the fan-out as a budget of tokens/quota:

```text
défaut                              → 1 agent actif
2 investigations indépendantes     → 2 subagents read-only
2 User Stories indépendantes        → 2 writers maximum pour commencer (WIP inclut les PR en review)
3+ sessions parallèles              → uniquement si le gain et la capacité de review sont mesurés
writer                              → toujours 1 par branche / PR / worktree
```

Logge at least `parallel_sessions_peak`, `subagent_count` and `subagent_tokens`. A subagent protects the context of the parent, but it recharges its own context: it is therefore never "free". If it does not bring useful insulation or really parallel work, does not launch it.

For coordination, prefers a ** startopology**: the parent delegates independent contracts and synthesizes returns. Avoids teams where agents speak freely, share a mailbox or distribute themselves a mutable state. In this guide, the "coordinator" must remain a simple **delegator**, not a social system of agents.

> **Orchestration Claude Code**: **Agent View** is used to supervise several sessions and tasks;
> **Agent Teams** allows collaboration between bodies but remains experimental; **Ultrareview** is a cloud review
> multi-agent in research preview. **Remote Control** allows to supervise a local session from another device
> While keeping the execution and MCP on the local machine. These surfaces complement the subagents; they do not
> change
> not the "one writer per worktree" rule.

> **Mod `You should know` (2.1.287+)**: `cc-plugin-you-should-know` launches a side agent during long tasks
> and displays above the prompt the items that you or Claude might miss. It is ** deactivated by default** and
> active via `/plugin enable cc-plugin-you-should-know@builtin`. Treat it as a signal of opportunistic vigilance,
> never like an independent reviewer, an oracle or a gate: his remarks must still be connected to evidence,
> a verifiable test or diff.

> **Claude Code 2.1.27x: finer insulation.** Since 2.1.277, a subagent customized or provided by a plugin can
> declare `omitClaudeMd` not to load `CLAUDE.md` user, project and local; administered policies
> reserves this mode to highly specialized exploration workers whose delegation contract contains
> The same version allows to attach `allowed_domains` to a command
> Bash/PowerShell/Monitor: Network opening is valid for this command, not for the entire session. ** Confirm**
> on
> "Minimum context per subagent" and "Minimum permission per subagent" rules, without justifying deletion of the
> project context for an implementer who needs it.
>
> Since 2.1.278, Auto mode uses by default a **Classify server-side** on compatible surfaces and
> Anthropic
> indicates that this classifier does not add a classification cost; `/status` indicates whether `Auto mode server` is active.
> This reduces a routing overhead, not the authorisation or review requirements. Finally, plugins and skills
> become testable artifacts themselves: `claude plugin eval` (2.1.269) performs a series of scorted evaluations
> and reproducible with output JSON/HTML, while `/skill-doctor` helps to locate loaded but useless skills.
> A persistent change of plugin or skill must therefore go through eval + review before promotion.
>
> The following versions add two complementary tools to avoid the drift of the harness. **2.1.283**,
> `/doctor prompt-audit` (alias `/checkup prompt-audit`) audit `CLAUDE.md`, skills, agents and controls to locate
> on
> instructions become obsolete or contradictory after a change in model generation. And in mode
> non-interactive, **`--bare`** is now documented as the way to launch a minimum harness: not
> self-discovery of hooks/plugins/MCP/memory/instructions, and since 2.1.286 only servers MCP explicitly
> named are connected, without system reminders or background tasks. Use `--bare` for **evals and scripts
> Reproducible**, not as the default daily mode.

<!-- section: s-37 -->
### OpenRouter for occasional routing API

In **this precise solo workflow**, the main routing does not need a gateway APIThe five daily paths already have their own surface and budget:

```text
Claude Code        → abonnement Claude Max
Codex              → abonnement ChatGPT
Qwen local         → MLX / llama.cpp / endpoint local
GitHub Copilot     → abonnement GitHub Copilot
JetBrains AI       → abonnement JetBrains AI
```

The need API remaining is **exceptional** When: Claude Code then Codex stay stuck and want an opinion from another family of models, for example **GLM, Kimi, Gemini, Grok or a new model to be evaluated**In this case, **OpenRouter is the best defect** : one key, no server to maintain, quick access to many models and providers, centralized billing and fallback availability.

```text
Blocage persistant
→ extraire le contexte minimal utile
→ OpenRouter
   ├── GLM
   ├── Kimi
   ├── Gemini
   ├── Grok
   └── nouveau modèle à tester
→ comparer l'analyse avec Claude / Codex
→ humain arbitre
```

**Do not automatically route daily work to OpenRouter.** The choice of the emergency model must remain explicit: the objective is precisely to get another perspective, not to leave a router silently choosing a different family.

<!-- section: s-38 -->
#### Fallbacks: provide yes, default no model

OpenRouter can switch automatically between providers. For this guide, distinguishes two levels:

```text
Même modèle, provider A indisponible
→ même modèle, provider B
→ OUI : résilience sans changer la nature du reviewer

GLM indisponible
→ Gemini
→ Kimi
→ Grok
→ NON par défaut : le changement de modèle doit rester visible et intentionnel
```

For a technical investigation, therefore, always log ** the model actually used.** An inter-model fallback may mask the reason why a conclusion differs from Claude or Codex.

<!-- section: s-39 -->
#### Qwen local: stay direct

Do not add OpenRouter only to standardize Qwen. `llama.cpp`, MLX or the local harness can already exhibit a OpenAI-compatible endpoint. As long as there are only one or two local models, the additional layer does not add enough value:

```text
Qwen local
→ llama-server / MLX
→ Qwen Code / OpenCode / script local
```

<!-- section: s-40 -->
#### Confidentiality with an aggregator

Providers accessible via OpenRouter may have different retention policies. For sensitive professional code:

```text
- ne jamais envoyer le repository entier par défaut ;
- préférer un reproducer minimal, quelques types/méthodes, la stack trace et le test ciblé ;
- anonymiser le contexte métier si possible ;
- choisir explicitement les providers compatibles avec les exigences de rétention du projet ;
- garder le code le plus sensible en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-41 -->
### Loggers

The router must be adjusted to actual data, not intuition. For each agent task, log:

```text
task_type
risk
difficulty
decision_layer
decision_confidence
decision_threshold
decision_overridden
model_used
effort_level
fallbacks
parallel_sessions_peak
subagent_count
subagent_tokens
input_tokens
output_tokens
cost_usd
duration
files_changed
diff_lines
tests_run
tests_passed
review_findings
human_rework
merged_or_reverted
time_to_deploy
human_active_minutes
review_queue_minutes
review_true_positives
review_false_positives
review_missed_defects
quota_consumed_by_role
production_regressions
rollback_or_hotfix
```

After two weeks, adjust the thresholds:

```text
- si Qwen échoue souvent sur un type de tâche, route directement vers Sonnet ;
- si Sonnet réussit sans retours review sur un type de tâche, évite Opus ;
- si Opus réduit fortement les boucles de correction, garde-le pour cette classe ;
- si Opus `xhigh/max` suffit là où tu envoyais Fable, redescends ;
- si Fable ne produit pas moins de reprises humaines, réserve-le aux vraies sessions longues ;
- si `max` ne trouve que des remarques optionnelles, redescends vers `high` ou `medium`.
```

<!-- section: s-42 -->
### Prompt minimum router (generative fallback)

If Jev is available and as exits are closed, prefers `Choice` / `Score` / `Noul` The prompt below is useful when open reasoning is needed or as a basis for comparison.

```text
Tu es un routeur de tâches de développement logiciel pour un projet Scala/Java/Play/Spark.

Analyse la demande ci-dessous et retourne uniquement du JSON valide.

Objectif : choisir le plus petit modèle capable de produire un résultat mergeable avec un risque acceptable.

Prends en compte :
- type de tâche ;
- difficulté ;
- risque métier ;
- taille probable du diff ;
- nombre probable de fichiers ;
- besoin d'écriture ;
- besoin de docs externes ;
- risque Scala spécifique : implicits, givens, effets, sérialisation JSON ;
- fichiers critiques : build.sbt, migrations DB, auth, sécurité, concurrence, argent ;
- modèle, effort et, si nécessaire, mode `pro` ou multi-agent (`ultra` côté produit) ;
- plafond de coût et de durée ;
- règle d'escalade ;
- conditions d'arrêt.

Les signaux déterministes (fichiers critiques, taille de diff) priment sur ta propre confidence.

Demande :
[COLLER LA DEMANDE]

Contexte disponible :
[COLLER FICHIERS, STACK TRACE, DIFF STAT OU RÉSUMÉ]
```

<!-- section: s-43 -->
### Guiding principle of routing

```text
Le routeur ne choisit pas le modèle le plus intelligent.
Il choisit le modèle le moins cher capable de produire un diff mergeable,
avec une règle d'escalade explicite dès que le risque ou l'incertitude augmente.
```

<!-- section: s-44 -->
## Impact on the monthly budget

*(indicative relative order from tariffs) API standard; subscription and quota do not mechanically convert into dollars API)*

| Model              |           Price API input/output / M | Volume recommendation                                                                          |
|---------------------|------------------------------------:|---------------------------------------------------------------------------------------------------|
| Qwen local          |                                   0 | Pre-analysis and safe volume tasks                                                             |
| **Jev 1.14**        | **$0.042/M input; free output** | Decision layer: classification, routing, scoring and selection of high frequency skills        |
| **GPT‑6 Luna**      |                   **$0.10 / $0.50** | Micro-dev Codex, workers, sorting, simple tests                                                   |
| **Haiku 5.5**       |                   **$0.10 / $0.50** | Sub-agents, triage; bearing ×5 if input > 100K ; effort `medium` configurable                        |
| **GPT‑6.2 Sol**     |                        **$2 / $10** | Fault Codex agentic; excellent performance point before Astra                                 |
| **Sonnet 5.5**      |                        **$2 / $10** | Micro-dev Claude defect; `medium` for agentic coding well specified                              |
| **Opus 5.5**        |                        **$4 / $20** | Deficit Claude agentique at `medium`; `high` for difficult tasks                             |
| **GPT‑6.2 Astra**   |                        **$8 / $40** | Capacity climb; start at Light                                                          |
| **Fable 5.2**       |                        **$8 / $40** | Frontier Claude ; start at Low during a capacity escalation                                 |
| Extra / Max / Ultra |                            variable | Use only after measurement: more effort is not synonymous with better cost per task completed |

> **The price per token is not the TCO.** Also evaluates Fable 5.2`low` on limited and verifiable tasks: it can cost less per task solved
> that a lower model that seeks, rereads and backtracks more; conversely, Opus 5.5 `medium` can reach the
> the same quality as Fable on some workflows for a fraction of the cost. The local benchmark must therefore measure
> ** cost per change accepted**, human resumes and minutes.

<!-- section: s-45 -->
## Anti-credit rule burned

Do not launch Fable 5.2, GPT‑6.2 Astra, Opus 5.5 `Extra/Max` or expensive `Ultra` mode unless you can provide:

```text
- objectif précis ;
- contraintes ;
- fichiers ou modules probables ;
- critères d'acceptation ;
- tests à exécuter ;
- non-objectifs ;
- limite explicite de diff ;
- plafond de coût et de durée ;
- règle d'arrêt.
```

A very strong model on a quick blur does not produce a good result: it produces a more expensive drift.

> **Binding limits rather than discipline alone.** Several settings Claude Code transform this rule into
> safeguards: `maxEffortLevel` cap the effort on all providers; a deny rule targeting a tool parameter
> (e.g. `Agent(model:opus)`] prohibits launching a subagent on a expensive model; `CLAUDE_CODE_SUBAGENT_MODEL`
> fix the model of subagents; `fallbackModel` list up to three fold models tested in order (to
> log, see above); `/usage` breaks down consumption by skill, subagent, plugin and server MCP; and
> hooks see the current effort via `$CLAUDE_EFFORT`. Side API, les **task budgets** (beta)
> `task-budgets-2026-03-13`, `output_config.task_budget`) give the model a budget of tokens for the entire loop
> Agentic: it is a budget **indicative**, not a ceiling, which must be doubled by a `max_tokens` and a ceiling
> customer side; its value is part of the prompt rendered, so changing it breaks the cache. Check the doc list
> models supported before using it on Fable 5.2 or Opus 5.5.

<!-- section: s-46 -->
#### Checklist pre-flight before any task > $2 estimated cost

Before running Fable 5.2, GPT‑6.2 Astra, Opus 5.5 with high effort or a multi-agent session, validates this checklist. Each unchecked box is a reason not to run and go down as a model or a scope.

□ Objective formulated 1 phrase with action verb □ Non-explained objectives (at least 2) □ Relevant files/modules identified (accurate paths) □ Testable acceptance criterion defined □ Targeted test command ready to run □ Maximum acceptable diff set (e.g. < 300 lines) □ Fixed cost limit (e.g. $5) and maximum duration (e.g.: 30 min) □ Stop rule (if [condition]) □ The plan was validated by the human BEFORE the write mode □ Dedicated Worktree created if the task touches > 5 files □ Minimal context prepared (no "here is the whole repo")

Rapid cost estimate (order of magnitude):

| Task               | Model      | Tokens estimated      | Estimated cost |
|---------------------|-------------|---------------------|-------------|
| Feature 3 files  | Sonnet 5.5  | ~20K in / ~5K out   | ~$0.09      |
| Multi-module Bug   | Opus 5.5    | ~50K in / ~10K out  | ~$0.40      |
| Migration framework | Fable 5.2   | ~200K in / ~50K out | ~$3.60      |
| Audit Astra max     | GPT‑6.2 Astra | ~100K in / ~20K out | ~$1.60      |

If the estimated cost exceeds 3x the cost of the lower model for the same task, the difference in quality must be justified by the risk. "More intelligent" is not a justification.
---

