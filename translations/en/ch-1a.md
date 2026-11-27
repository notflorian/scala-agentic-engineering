<!-- section: chapter -->
# 1A. Vibe coding, AI-assisted coding, and agentic coding

The term **vibe coding**, popularized by Andrej Karpathy in February 2025, originally described a practice in which programmers delegate almost all code writing, accept the model’s suggestions, and judge the work mainly by what they can see it do. This approach works for a disposable prototype, an exploration, or a low-stakes interface. It falls short as a production method for business-critical, financial, security-sensitive, or long-lived systems.

Two points about the term’s origin clarify the debate in 2026. Karpathy said the tweet was half a joke, aimed at throwaway weekend projects. He never proposed vibe coding as a production method. As early as February 2025, Simon Willison drew a useful distinction. Accepting diffs without reading them is vibe coding. Reviewing every line and understanding what it does is AI-assisted programming. The problem arises when review is skipped. By late 2025, **vibe engineering** had entered the vocabulary for experienced professionals who work substantially faster with LLM agents while retaining full responsibility for the software. What distinguishes these two practices is how the developer reviews, tests, and takes responsibility for the result. That is the focus of this guide.

There are three different ways of working:

| Mode                        | Human control                                                     | Adapted use                                     | Principal risk                                           |
|-----------------------------|---------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------|
| **Vibe coding**             | Low, sensation validation and execution                       | Prototype, Spike, Personal Disposable Tool        | Invisible debt, security, lost understanding            |
| **AI-assisted engineering** | The developer designs and re-reads, the model accelerates                 | Daily work on code maintained              | Automate decisions that should remain human    |
| **Agentic coding**          | The agent explores, plans, modifies and tests within a bounded perimeter | Tasks well specified with tests and permissions | Drive, loop, action outside perimeter, indirect injection |

For a senior Scala, the target is therefore not "more vibe coding", but a controlled ** agent engineering **:

```text
verifiable specification
→ minimal but sufficient context
→ plan
→ proportionate permissions
→ instrumented execution
→ compilation and deterministic tests
→ independent review
→ human validation
```

**Evidence-driven agentic engineering**: the SDD sets the contract, the harness engineering makes its constraints executable, and the evidence determines whether the change can progress. For each requirement, combines independent evidence (behaviour test, inspection, benchmark or runtime measurement), the SHA actually validated and the risks not covered. An agent's statement, a review without proof or a simple green status do not constitute an oracle. The cycle ends after validation of the deployed artifact, not simply at the merge (section 15B).

<!-- section: s-1 -->
## What the state of art shows in 2026

1. **The model alone does not determine success.** Harness, tools available, debugger, context quality and testing can change results almost as much as the choice of the model. Comparisons between scores published by suppliers are valid only if the harness, effort, tools and protocol are comparable.
2. ** Short benchmarks overestimate long-term autonomy.** Agents perform well on isolated outcomes, but fall sharply on long, historical multi-file developments. SWE-EVO, for example, aims at tasks much longer than SWE-bench and highlights this gap.
3. **SWE-bench Verified is no longer a good single standard.** OpenAI has documented problems of contamination and defective tests. For the code, prefer a portfolio including audited SWE-bench tasks, Terminal-Bench, review tasks and above all an internal benchmark Scala not public.
4. **Human productivity is not guaranteed by a good artificial score.** A randomized METR study of developers experienced in their own repositories observed a slowdown with the starting tools 2025. The data then collected suggest a possible improvement, but METR finds the new trial unreliable because of selection bias and difficult measurements with several competing agents. Therefore, there is not yet any causal replication specific to the tools of the test. 2026. The local measurement of time to the merge remains essential. 2026 : point estimate of about 18 % acceleration on the historical sub-cohort (confidence interval −38 % à +9 % and about 4 % on new participants (IC
   −15 % à +9 % In the initial test, participants felt that on average they had been able to obtain a signal that was too noisy to conclude, which METR preferred to deal with by recasting the protocol rather than by publishing a single figure. ~20 % faster due to AI when they were ~19 % slower — the difference between perception and measurement is the reason why this guide requires local metrics (cost per change accepted, time to the merge) rather than the feeling of sessions.
5. **Repository instructions are useful only if they are operational.** Searches on `AGENTS.md` find a benefit when the file contains commands, non-standard conventions, invariants and shutdown rules. A long generic description of the architecture can increase the context without improving the result.
6. **The multi-agent is not an automatic intelligence multiplier.** It helps when sub-tasks are truly independent, the responsibilities and files are separated and a root agent synthesizes. On a shared mutable state, it increases conflict, cost and coordination errors.
7. **A technically correct patch is not enough to evaluate an agent.** Also measures compliance with the scope, stopping rules and conventions, the quality of the plan, the ability to report uncertainty and the cost of human review. Two agents who pass the same tests can have a very different value if one generates twice as much rework or off-site changes.
8. **Memory, skills and persistent rules become an engineering surface.** Agents capable of evolving their own memory, skills or routing must never self-promote these changes. Any persistent evolution must be diffusible, versioned, tested, reviewed and reversible before activation.
9. **A large context window does not remove the *context rot*.** Evaluations 2026 differentiating the physical capacity of the window and the effective quality of use of its content: with the same task, more tokens can degrade recovery, respect for constraints and reasoning well before the maximum limit. The right objective is therefore not "filling in" 1M tokens", but maintain a **minimal working set and decision-making**. Isolated sub-agents are a structural parade: they consume a lot of context locally and refer to the parent only a condensed result.

Conclusion: The border level increases the area of possible tasks, but the quality of engineering around the agent remains the most controllable factor.

<!-- section: s-2 -->
### Methodological supplement

> **SWE-bench Pro does not replace SWE-bench Verified.** OpenAI now estimates that about 30 % of tasks
> SWE-bench Pro are also defective: tests too strict, hidden requirements absent from the prompt, coverage
> The audit of 8 July 2026
> (automated pipeline: 27,4 % of 731 marked public tasks; notation by five senior engineers: 34,1 %)
> has led OpenAI] to ** explicitly withdraw its recommendation** to make it the coding evaluation of
> The good evaluation portfolio therefore combines several axes.
> rather than a new one
> Single classification.

| Axle to be measured                | Useful evaluation                 | What she reveals                                                                               |
|------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------|
| Conventional deposit correction | SWE-bench, with task audit | Repair capacity on isolated exits                                                       |
| Original long task       | **DeepSWE**                      | Reduced Contamination, written auditors to accept several valid solutions           |
| Iterative collaboration      | **SWE-Interact** or SWE-Together | Discovery of intent, memorization of constraints, need for human corrections            |
| Deposit Exploration         | **SWE-Explore**                  | Line location and context efficiency                                     |
| Full cycle                | **SWE-Cycle**                    | Environmental reconstruction, implementation and testing generation in the same path |
| Reality of your work       | **Benchmark Scala Private**        | Cost and quality on Play, Pekko, Tapir, Spark, Implicit, Serialization and Real Build          |

For a code task, measure the **cost per change accepted** ; to control delivery, the **cost per change deployed and stable** (section 15B), not the gross success rate:

```text
cost per accepted change
= tokens + latency + human minutes + CI + rework + escaped defects
```

Use a common unit to aggregate these costs (e.g. euros with an explicit hourly cost), or keep separate components. Tokens and minutes do not add directly. For cost up to production, add deployment, runtime validation, rollback/hotfix and defects observed during a window fixed before measurement. Only counts as stable a change that has finished this window.

Does not seek an overall "IA productivity". Stratifies as a minimum measures by **greenfield, maintenance, legacy, bugfix, migration, refactor and critical code** : studies 2026 achieve contradictory results precisely because they do not always measure the same tasks, developers or review costs.

<!-- section: s-3 -->
### A green benchmark is not yet a fair deal

A METR assessment of 296 PRs generated by agents found that the SWE-bench grader averaged **24,2 points of success** more than the maintainers responsible for assessing whether the change was truly useful and mergeable; about half of the PRs that passed the tests would not have been merpedoed. The sample included only three depositions, pre-generation models, and a single test without iteration on the maintainer feedback: it is not a fundamental limit of capacity, but it invalidates the naive equivalence `tests du benchmark passants = changement acceptable`.

On long tasks, SlopCodeBench also observes an accumulation of duplication, verbosity and structural erosion as checkspoints follow. A prompt demand for quality reduces certain defects at the beginning without removing their growth. The good proof regime therefore combines four independent barriers:

```text
explicit business contract
→ reproduction that fails before the patch
→ deterministic tests, properties, and mutation testing
→ accountable human review of the diff, its scope, and its maintainability
```

Benchmark scores are used for routing and experimentation; they must never become an authorization for autonomy or for merge.

> **Screen between writing and delivering.** The working paper NBER *Writing Code vs. Shipping Code* observes, on more than
> 500 000 developers GitHub, an estimated increase in activity much greater for commits than for
> projects and releases. The study remains observational with pairing: it does not demonstrate a causal effect
> The WIP is therefore limited to the ability to review and deliver, and measures up to production.

<!-- section: s-4 -->
### Production guard for vibe coding

Empirical studies of 2026 on truly "coded vibe" applications find families of recurring defects: temporary logic left in production, unfiltered inputs, exposed secrets, forgotten constraints over the turns and local optimisation that degrades the global system. A stronger model or a better prompt reduces these defects, but does not eliminate them.

> **Orders of magnitude measured in 2026.** The audit of 200 truly "encoded" and deployed vibe applications
> (1 471 validated vulnerabilities) finds at least one vulnerability in **90 % of deposits**, of which more than three
> high or critical severity quarters; broken access control appears in 75,5 % of deposits, i.e. approximately 20×
> the OWASP baseline 2025. An independent scan of 1 400+ applications results in the same order of magnitude (65 %
> have at least one security problem, 58 % at least one critical vulnerability, 400+ secrets exposed).
> The root cause analysis classifies these defects into three families — **memory** (forgotten constraints between the two families)
> turns), **objective** (local optimization that degrades the global system) and **knowledge** (dangerous patterns)
> the three mechanisms that deterministic gates and the human review of this guide must have
> Discontinue, since no prompt correction is lasting.

```text
Vibe coding prototype
→ no production data or keys
→ functional tests + security + performance + maintainability
→ human review of the diff and dependencies
→ migration to the controlled agentic workflow
→ deployment only then
```

A vibe coding session should never push directly into production, even when the demonstration appears functional. The production boundary is a **change of proof regime**, not a simple next step of the cat.

