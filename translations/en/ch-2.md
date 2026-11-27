<!-- section: chapter -->
# 2. Recommended stack

With **MacBook Pro 16" M5 Max, 18 CPU hearts, 40 GPU hearts, Neural Engine 16 hearts, 128 Go Unified Memory, SSD 8 To**, **IntelliJ Ultimate**, **Scala/Java/Play/Spark**I'd choose this stack:

| Layer                 | Tool                                                 | Role                                                                                                                                   |
|------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Main FDI          | **IntelliJ Ultimate**                                 | Navigation, typing, refactoring, debug, testing and screening of agents                                                             |
| FDI assistance         | **JetBrains AI**                                      | Completing Code, Next Edit Suggestions, AI Actions and Small Transformations without replacing the Senior Agent                         |
| Senior Agent Claude | **Claude Code Max**                                   | Opus 5.5 `medium` for agentic coding, architecture and debugging; Sonnet 5.5 `medium` for micro-dev; Fable 5.2 Climbing front line |
| Local model           | **Qwen3-Coder-Next / Qwen3.8-27B**                    | Coder-Next as fast baseline; Qwen3.8-27B as challenger quality-first to measure                                                |
| Local Harness          | **Qwen Code or OpenCode**                             | Qwen Code is now a complete agentic harness; OpenCode remains an alternative to be measured                                        |
| Agent Codex / Reviewer | **Codex in IntelliJ / ChatGPT Desktop / Codex CLI** | GPT‑6.2 Sol `Medium` for ownership end-to-end; GPT‑6 Luna `High` in micro-dev; GPT‑6.2 Astra `Light`+ for frontier tasks      |
| GitHub workflow        | **GitHub Copilot**                                    | Issued → agent, PR, automatic review and corrections CI for restitories GitHub                                                  |
| Optional PR tracking   | **Codex Goal mode / Heartbeats / Cloud ; Claude Code `/ship` / `/steward` / Cloud Auto-fix ; Claude Ship** | GPT‑6.2 Sol `Medium` for monitoring Codex bounded; centralized team agents GitHub without replacing cross-review or CI |
| Small diff             | **Aider**                                             | Targeted changes, git-first, loop lint/test                                                                                     |
| IDE optional agent    | **JetBrains Junia / JetBrains AI**                    | Native agent in IntelliJ if you want to stay in the IU                                                                                  |
| Search codebase     | **Sourcebot**                                         | Multi-rest search, symbols, uses, relevant files                                                                           |
| KnowledgeGraph         | **ScalaSemantic MCP / Codebase-Memory MCP**           | ScalaSemantic for the semantic graph Scala; Codebase-Memory for the Java/Kotlin polyglot structural graph                       |
| Decision-layer         | **Jev 1.14**                                          | Decisions closed at high frequency : classification, routing, skill selection, scoring and climbing signal                           |
| Updated Docs            | **Context7**                                          | Verification API, frameworks, libs (anti- hallucination)                                                                                |
| Integration IDE agent  | **JetBrains ACP + MCP**                               | ACP connects FDI to agents; MCP exposes tools, context and actions IntelliJ                                                           |
| Optimization tokens    | **RTK + Headroom**                                    | Reduction logs, diffs, output terminal                                                                                                |
| Routing API            | **OpenRouter**                                        | Timely access to alternative models                                                                                                 |

Status and maturity of tools:

| Tool                   | Status                                           | Point of vigilance before adoption                                                                                                                                  |
|-------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code             | Stable, official tool                           | Opus 5.5 is the current Opus model for the long-term active coding; Sonnet 5.5 is the fast-track; Agent Teams remains experimental, Ultrareview in research preview   |
| Claude Ship             | Code Review GA ; Steward / Approvals en beta     | Service Team/Enterprise billed separately; `/ship`] and `/steward` locals are subject to useClaude Code. See section 12.                                             |
| Codex post-PR           | Goal mode, Scheduled Tasks, Cloud and Code Review official | Heartbeats according to surface; permissions and quotas to check; Watch and Fix not confirmed; no automatic merge. See section 12. |
| Claude Mods             | Available from Claude Code 2.1.287            | Extension JS/TS in-process ; very powerful but unsandboxed : only install audited code and limit its use to the needs only hooks/skills/MCP cover poorly |
| Jev 1.14                | Early access ; API System One                    | Very good candidate for closed decisions; thresholds to calibrate per task, minimum state, never final authority over critical action                           |
| Qwen3-Coder-Next local  | Stable model side                               | On 128 Go: Q4_K_M ≈ 48,4 Comfortable go; Q5_K_M ≈ 56,7 Recommended Go; Q6_K ≈ 65,5 Sustainable Go; Q8_0 ≈ 84,8 Go to test on time                           |
| OpenCode                | Active, LSP partially exp.                    | Validate the LSP Metals on your repo before standardization                                                                                                           |
| Qwen Code               | Active, serious alternative                      | Auto-Memory/Skills, subagents, workers, MCP/LSP; Agent Teams and Arena remain experimental                                                                     |
| ChatGPT Desktop / Codex | App desktop ChatGPT, CLI, IDE extension and Cloud | Codex now knows how to manage several sessions/agents; plugins and permissions still have to be audited                                                                  |
| JetBrains Junie / CLI   | **Stable**, BYOK                                 | Credible option, to be split by bake-off on deposit Scala                                                                                                      |
| Aider                   | Stable, maintained                                 | Discipline "few files" indispensable                                                                                                                         |
| Sourcebot               | Stable                                           | Cost of accommodation and multi-rest indexing                                                                                                                     |
| Context7                | Stable                                           | Variable coverage according to niche libs Scala                                                                                                                  |
| RTK                     | Stable                                           | Hooks PreToolUse to test on your actual sbt outputs                                                                                                              |
| Headroom                | **Experimental**                                 | Test on non-critical logs/diffs only                                                                                                                     |
| OpenRouter              | Stable                                           | Zero infra; ideal as a point output to GLM/Kimi/Gemini/Grok and new models                                                                  |

JetBrains has two levels MCP to distinguish: the support MCP side AI Assistant exists since IntelliJ IDEA 2025.1 as a client, and IDEs JetBrains also exhibit a server MCP integrated since 2025.2 for external clients to access IDE tools. This is particularly important for Scala, where the agent needs symbols, types, modules, inspections and run configurations, not just raw text.

Since IntelliJ IDEA 2026.1 — which has integrated Codex, Claude Agent and Junie, then Cursor and GitHub Copilot via the register ACP (opened at the end of January) 2026), with management MCP by consolidated agent in 2026.2 — adds a distinction of protocol: **ACP (Agent Client Protocol) connects the IDE to the coding agent**, while **MCP connects the agent to the tools and context**. IntelliJ can thus serve as IU and structural truth while leaving Claude, Codex, Junie, GitHub Copilot or another agent ACP Each agent retains its own harness, models, authentication and permissions, so the replaceable unit is no longer just the LLMThe tools of the server. MCP IntelliJ may be restricted per agent; for debugging Scala/JVM, debugger tools
exposed by the server MCP IntelliJ (prefixed tools) `xdebug_`, activable from the configuration of MCP Server) allow to collect stack, variables, threads and runtime evidence without injecting `println` in the code.

<!-- section: s-1 -->
### Architecture IntelliJ 2026.2 recommended

```text
IntelliJ IDEA
├── JetBrains AI
│   ├── Code Completion
│   ├── Next Edit Suggestions
│   └── AI Actions / small transformations
├── Official Claude Code
│   ├── JetBrains plugin / CLI
│   └── Claude Code Desktop
│       → Claude Max subscription, primary agent for reasoning/debugging/architecture
├── Codex
│   ├── ACP agent in AI Chat
│   ├── ChatGPT Desktop / CLI
│   └── ChatGPT/OpenAI account
│       → primary agent for standard issues / cross-reviewer when Claude writes
└── GitHub Copilot
    └── GitHub-native layer: issues, PRs, automated review, CI
```

**ACP does not replace official integrations.** For Claude, guard **Claude Code Official** as the main route when you want to exploit the Claude Max subscription: the plugin JetBrains, the CLI and the Code tab of Claude Desktop share the same Harness Claude Code and its rules (`AGENTS.md` in fallback or `CLAUDE.md`, permissions, hooks, MCP, skills). Claude Code Desktop adds several sessions isolated by worktrees, visual review of diffs, built-in terminal/editor and PR tracking. ACP the interoperability layer which allows the IntelliJ to accommodate several agents in a common IU.

For Codex, the agent integrated with IntelliJ can authenticate with the **account ChatGPT** or a key OpenAI. With supplier-specific authentication, agent usage does not consume AI Credits JetBrains. Same logic for other agents ACP which use their own supplier account. In-editor functions **Completing Code** and **Next Edit Suggestions** does not consume the quota of AI Credits either. **JetBrains AI Ultimate (35 AI Credits / 30 days)** becomes a budget for Junie, AI Chat and cloud functions JetBrains ; it does not have to finance the bulk of the agentic development if Claude Code and Codex use their respective subscriptions.

Note side JetBrains in 2026 : **Codex is now integrated as an agent in IDEs** alongside Junie and Claude, the register ACP allows to add other agents, and a system of **Skills** Full reusable MCP. FDI thus becomes a **local plane control** : navigation, diagnostics and debugger remain JetBrains, while the writer or reviewer can be changed per session without abandoning the environment Scala/JVM.

---

