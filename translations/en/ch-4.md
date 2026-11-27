<!-- section: chapter -->
# 4. A realistic monthly budget and a caching strategy

The budget must be managed as an engineering budget, not as an abstract expenditure. The correct metric is not the cost per message, but:

```text
total cost of a mergeable task
= model cost + human time + CI time + review feedback + bug rework
```

<!-- section: s-1 -->
## Realistic start budget

| Post                                                 |                 Indicative budget | Note                                                                                                                                                                                    |
|-------------------------------------------------------|---------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code via Claude Pro/Max                        |                      20 à 200+ $ | Max is justified if Opus/Sonnet turns every day; the quota is shared between compatible Claude surfaces.                                                                        |
| ChatGPT with Codex                                    |                     20 $ and more | More suitable for limited use; Pro is justified if Sol 6.2 becomes a daily writer and not only a reviewer.                                                                        |
| JetBrains AI Ultimate                                 | ~300 $/year; 35 AI Credits / 30 j | Helpful for cloud functions JetBrains and Junie; Code Completion / Next Edit Suggestions and authenticated agents at their supplier do not consume these credits.                     |
| GitHub Copilot                                        |                         variable | Optional: relevant especially if GitHub is the center of workflow issues/PR/review; widely redundant as third code chat.                                                      |
| OpenRouter / API point GLM/Kimi/Gemini/Grok      |                         0 à 50 $ | Exceptional exit door when Claude/Codex/Qwen is not enough; voluntarily low and capped budget.                                                                         |
| GLM Coding Plan (Z.ai) — second optional subscription  |                 ~18 to 160 $/month | Open-weight package *conformance* : endpoint Anthropic-compatible, plugging in Claude Code to absorb review/triage without breaking your limits Claude. Lite ~18 $, Pro ~72 $, Max ~160 $. |
| Qwen local                                            |             0 $ excluding electricity | Very good for pre-analysis, synthesis and boilerplate, but not to decide alone on critical code.                                                                                           |
| Sourcebot, Aider, OpenCode/Qwen Code, RTK             |                     0 to variable | Many tools are open source, but possible hosting, indexes and keys API cost.                                                                                      |
| Headroom and recent context compression tools |                     experimental | To be tested on non-critical logs/diffs before integrating it into the standard workflow.                                                                                                         |

Total realistic target for intensive solo use: **250 à 450 $/month**, to be adjusted after two weeks of actual measurement. 300 à 350 $ remains plausible, but it should not be frozen: a single bad agentic loop on a large context can cost more than a week of well-routing micro-patches.

<!-- section: s-2 -->
## Price points and quotas not to be fixed in the guide

Claude Code is included in the compatible Claude pay plans, but the exact use depends on the plan, the model and the session limits. The official pages indicate in particular Claude Pro to 20 $/month, Max from 100 $/month, and uses Max 5x/20x depending on the offer. So keep the guide in the form of forks, not as a permanent accounting truth.

Side Codex, avoid changing model names and settings ChatGPT The active routing of this guide is **GPT‑6 Luna / GPT‑6.1 Terra / GPT‑6.2 Sol / GPT‑6.2 Astra**, with Sol 6.2 Medium as an agentic defect. The limits of use, access to Max/Ultra and billing depend on the plan, surface, region and rollout. So write the rules around the **task class and cost per change accepted**, then check the official page before industrializing a profile or budget.

Important reminder: **Anthropic reserves Claude Free/Pro/Max/Team/Enterprise subscription usage for native applications Anthropic and the uses provided for in its conditions.** From the beginning 2026, Anthropic explicitly prohibits the use of OAuth tokens of these subscriptions in third party harnesses or unofficial tools: these flows must pass through a key API This is a dedicated (Claude Console or cloud provider) and respect commercial terms. Claude Code and Claude.ai for Claude subscriptions; OpenCode/Qwen Code/Aider for Qwen local, models API or BYOK keys, without ever reusing a Claude Pro/Max session token in an external tool.

Not to be confused with *is* permit: plug-in Claude Code on the **endpoint Anthropic- Z.ai's compatible** with a **Z.ai key** (GLM Coding Plan, §3) is lawful — you use the key of a supplier against the endpoint of that same supplier, you do not divert any token OAuth Claude. The red line is the **re-use of a Claude subscription token** out of apps Anthropic, not pointing Claude Code to another supplier with his own key.

** Post-PR Budget Claude Ship.** In solo, `/ship`, `/steward` and Cloud Auto-fix consume the applicable use of Claude Code (no separate VM cost for the cloud Anthropic] according to the documentation); background monitoring is not free. Claude Ship's agents GitHub (Team/Enterprise) consume non-allocation organizational usage credits included. Estimate `PR/mois × coût moyen de review × nombre de reviews par PR + corrections Steward + classifiers Approvals + CI supplémentaire`. Starts with a review on request or at the opening, not on each push, and sets a monthly ceiling for Code Review and PR Steward (the latter does not have any by default). Approvals' mode `observe` can also trigger reviews and classifys
Disable credit usage is not enough to stop active agents: Disable Approvals, then Steward, and then Code Review if you want to cut those expenses.

**Post-PR budget Codex.** `@codex review` and automatic reviews GitHub are subject to Code Review conditions; `/review` local, Goal mode, Heartbeats and tasks Codex Cloud authenticated with your account ChatGPT use the applicable plan and surface allocations. No archived monitoring scripts or key API OpenAI However, check for quotas, additional credits and actual permissions: each take-over and each correction can consume quota, even without any new differences. Prefers a limited objective or a Heartbeat with deduced by SHA and explicit shutdown; never both simultaneously on the same branch. `openai/codex-action` with key API remains an option of CI separately invoiced,
to be reserved for the automation needs that native surfaces do not cover.

<!-- section: s-3 -->
## Prompt caching: major lever, but to formulate precisely

In order not to explode the budget, structure the requests of agents in deterministic manner:

1. Place the static context at the top: `AGENTS.md`, rules Scala, architecture, test conventions.
2. Place the semi-static context next: schematics, contracts JSON, trade agreements.
3. Place the dynamic context at the bottom: modified files, compilation errors, test logs.
4. Avoid changing the prompt header at each iteration if you want to benefit from the cache.

A successful hit cache can reduce the cost of **reading** of tokens of entry to about 10 % of normal input cost by supplier (on models) Anthropic Currents: 5 % for Opus 5.5 and Sonnet 5.5, 2,5 % for Fable 5.2, 10 % for Haiku 5.5 ; 5 % for GPT‑6.2 Sol/Astra and GPT‑6.1 SolIt's not a "Terra".90 % saving on the entire task: output tokens, cache writing, tool calls and loop errors remain billed.

<!-- section: s-4 -->
## Anti-credit rules burned

```text
- Never provide the entire repo by default.
- Provide file paths and a hypothesis about the affected area.
- Trim logs at the first useful error.
- After 2 identical failures, stop and switch back to human or IDE diagnosis.
- After 3 files are changed outside the plan, stop and ask for a new plan.
- After 300 unexpected lines of diff, stop for manual review before continuing.
- When context stops helping, write an explicit `HANDOFF.md` and start a fresh session. Use `/compact` only as a last resort.
- Prefer rg, Sourcebot, IntelliJ, Metals, or local scripts to long MCP dumps.
```

** Savings on double subscription.** Stabilizes the writer and his effort during a trajectory; model changes can disrupt the cache and add rework. A fresh context remains voluntary for the independent reviewer or a contaminated hypothesis. Do not launch a systematic comprehensive review on each micro-patch or second stepward on the same PR. Deduces the follow-up by repo/PR/SHA/check/finding, prefers an event recovery or a limited Heartbeat when the CI waits, and stops it at the checkpoint. Measures the quotas consumed by role and task (when exposed by the supplier); distinguishes included credits, overruns and API. A still high quota is not a reason to open more tickets.

