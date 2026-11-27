<!-- section: chapter -->
# 1. Guiding principle

For a senior Scala developer, the aim is to maximize the following ratio. Writing code faster is secondary.

```text
Useful changes deployed and stable
÷
(unnecessary diffs + review feedback + bugs + credits spent + human time)
```

The right mental model:

```text
You = tech lead and final decision-maker
IntelliJ = source of truth for Scala/JVM structure and control center
JetBrains AI = inline assistance and low-friction IDE actions
Codex = primary implementation agent for standard issues + independent reviewer when Claude writes
Claude Code = primary reasoning, debugging, and architecture agent + independent reviewer when Codex writes
Local Qwen = low-cost assistant
GitHub Copilot = GitHub-native layer for issues, PRs, and automated review
Aider = small, clean Git-focused diff
MCP + Sourcebot + Context7 = targeted context
RTK + Headroom = noise reduction
Jev = probabilistic decision layer for classification, scoring, and routing — never the coding model or the only critical gate
GPT‑6 Luna / GPT‑6.2 Sol / GPT‑6.2 Astra = Codex routing for micro-loops, agentic work, and frontier tasks
Haiku 5.5 / Sonnet 5.5 / Opus 5.5 / Fable 5.2 = Claude routing by volume, human oversight, and autonomy
Tests + Stryker4s + CI = final arbiters (deterministic)
```

---

