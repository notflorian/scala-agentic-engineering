<!-- section: chapter -->
# 2. Empfohlener Technologie-Stack

Mit **MacBook Pro 16" M5 Max... 18 CPU-Herzen, 40 GPU-Herzen, Neural Engine 16 Herzen, 128 Geschlossener Speicher GB, SSD 8 To**, **IntelliJ Ultimat**, **Scala/Java/Play/Spark**, würde ich diesen Stack wählen:

| Schlaf                 | Werkzeug                                                 | Rolle                                                                                                                                   |
|------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Direktinvestitionen          | **[IntelliJ Ultimate**                                 | Navigation, Typisierung, Refactor, Debug, Tests und Kontrollstation der Agenten                                                             |
| Unterstützung für ausländische Direktinvestitionen         | **JetBrains AI**                                      | Code Completion, Next Edit Vorschläge, AI Aktionen und kleine Transformationen, ohne den Hauptvermittler zu ersetzen                         |
| Hauptagent Claude | **Claude Code Max**                                   | Opus 5.5 `medium` für agentic coding, architektur und debugging; Sonnet 5.5 `medium` für micro-dev; Fable 5.2 Grenzsteiger |
| Lokales Modell           | **Qwen3-Coder-Next / Qwen3.8-27B**                    | Coder-Next als Schnellbasisline; Qwen3.8-27B als quality-first-Challenger                                                |
| Lokale Harness          | **Qwen Code oder OpenCode**                             | Qwen Code ist nun ein komplettes agentielles Harness ; OpenCode bleibt eine Alternative, die zu messen ist                                        |
| Agent Codex /review | **Codex in IntelliJ / ChatGPT Desktop / Codex CLI** | GPT‑6.2 Sol `Medium` für das lownership end-to-end , GPT‑6 Luna `High` in Mikro-Dev; GPT‑6.2 Astra `Light`+ für Grenzaufgaben      |
| GitHub workflow        | **GitHub Copilot**                                    | Gelesen → Agent, PR, automatische review und Korrekturen CI für Resetorien GitHub                                                  |
| Optionale PR-Überwachung   | **Codex Goal mode / Heartbeats / Cloud; Claude Code `/ship` / `/steward` / Auto-fix Cloud; Claude Ship** | GPT‑6.2 Sol `Medium` Überwachung Codex Begrenzt; Agenten GitHub centralisés en équipe, sans remplacer la review croisée ni la CI |
| Kleiner Diff             | **Aider**                                             | Gezielte Änderungen, Git-first, Lint-/Testschleife                                                                                     |
| IDE optional    | **JetBrains Junie / JetBrains AI**                    | Einheimischer Agent in IntelliJ, wenn Sie in der I.E. bleiben möchten                                                                                  |
| Suche codebase     | **Sourcebot**                                         | Multi-Repo-Suche, Symbole, Nutzungen, relevante Dateien                                                                           |
| KnowledgeGraph         | **ScalaSemantic MCP / Codebase-Memory MCP**           | ScalaSemantic für den semantischen Graphen Scala ; Codebase-Memory für den polyglotten Strukturgraphen Java/Kotlin                       |
| Layer-Decision         | **Jev 1.14**                                          | Hochfrequenzgeschlossene Entscheidungen: Klassifizierung, Routing, Skill-Auswahl, Scoring und Klettersignal                           |
| Aktualisierte Dokumente            | **Context7**                                          | Überprüfung API, frameworks, libs (Anti-halluzination)                                                                                |
| IDE-Integration  | **JetBrains ACP + MCP**                               | ACP verbindet die IDE mit den Agenten ; MCP stellt Instrumente, Kontext und Aktionen IntelliJ                                                           |
| Optimierung tokens    | **RTK + Headroom**                                    | Reduziert logs, diffs, terminals                                                                                                |
| Routing API            | **OpenRouter**                                        | Punktueller Zugang zu alternativen Modellen                                                                                                 |

Status und Reife der Instrumente:

| Werkzeug                   | Status                                           | Beobachtungsstelle vor der Annahme                                                                                                                                  |
|-------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code             | Stabil, offizielles Werkzeug                           | Opus 5.5 ist das aktuelle Opus-Modell für die lang anhaltende "Agentic coding ." Sonnet 5.5 ist das schnelletier; Agent Teams bleibt experimentell, Ultrareview en research preview   |
| Claude Ship             | Code Review GA; Steward / Approvals en beta     | Service Team/Enterprise separat berechnet; `/ship` und `/steward` Räumlichkeiten sind von der Verwendung Claude CodeSiehe Abschnitt 12.                                             |
| Codex post-PR           | Goal mode, Scheduled tasks, Cloud und offizielle Review Code | Heartbeats nach Fläche; Berechtigungen und Zertifikate zu überprüfen; Watch and Fix nicht bestätigt; kein automatisches Merge. Siehe Abschnitt 12. |
| Claude Mods             | Verfügbar seit Claude Code 2.1.287            | JS/TS-Erweiterung in-process; sehr leistungsfähig, aber nicht sandboxiert: Nur geprüften Code installieren und seine Verwendung auf die Bedürfnisse beschränken, die hooks/skills/MCP nicht gut abdecken |
| Jev 1.14                | Early access ; API System One                    | Sehr guter Kandidat für geschlossene Entscheidungen ; Schwellenwerte zu kalibrieren pro Aufgabe, minimaler Zustand, nie endgültige Behörde über eine kritische Aktion                           |
| Qwen3-Coder-Next lokal  | Stabile Modellseite                               | Über 128 Go: Q4_K_M ≈ 48,4 Komfortables Go; Q5_K_M ≈ 56,7 Go empfohlen; Q6_K ≈ 65,5 Go lebensfähig; Q8_0 ≈ 84,8 GB pünktlich testen                           |
| OpenCode                | Aktiv, LSP teilweise exp.                    | LSP Metals auf deinem repo vor Standardisierung bestätigen                                                                                                           |
| Qwen Code               | Aktiv, seriöse Alternative                      | Auto-Memory/Skills, Subagenten, Worktrees, MCP/LSP; Agent Teams und Arena bleiben experimentell                                                                     |
| ChatGPT Desktop / Codex | Desktop-App ChatGPT, CLI, IDE und Cloud-Erweiterung | Codex kann nun mehrere Sitzungen/Agenten steuern; Plugins und Berechtigungen müssen noch geprüft werden                                                                  |
| JetBrains Junie / CLI   | **Stable**, BYOK                                 | Glaubwürdige Option, die durch Bake-off auf dem Projektarchiv Scala                                                                                                      |
| Aider                   | Stabil, beibehalten                                 | Disziplin "wenige Dateien" unerlässlich                                                                                                                         |
| Sourcebot               | Stabil                                           | Unterbringungs- und Indexierungskosten für mehrere Repos                                                                                                                     |
| Context7                | Stabil                                           | Variable Abdeckung nach Nischen Libs Scala                                                                                                                  |
| RTK                     | Stabil                                           | PreToolUse Hooks auf Ihre tatsächlichen Ausgänge zu testen sbt                                                                                                              |
| Headroom                | **Experimental**                                 | Nur an nicht kritischen Logs/Diffs testen                                                                                                                     |
| OpenRouter              | Stabil                                           | Null in der Nähe; ideal als Punktausgang nach GLM/Kimi/Gemini/Grok und neue Modelle                                                                  |

JetBrains a zwei Ebenen MCP zu unterscheiden: der Träger MCP AI-Assistent-Seite existiert seit IntelliJ IDEA 2025.1 als Kunde, und DI JetBrains auch einen Server MCP integriert seit 2025.2 Dies ist besonders wichtig für den Zugang externer Kunden zu IDE-Tools. Scala, wo der Agent Symbole, Typen, Module, Inspektionen und Run-Konfigurationen braucht, nicht nur Rohtext.

Seit IntelliJ IDEA 2026.1 Der integrierte CodexClaude Agent und Junie, dann Cursor und GitHub Copilot über das Register ACP Öffentlichkeit (Ende Januar geöffnet) 2026), mit einem Management MCP durch einen konsolidierten Vertreter in 2026.2 Eine Unterscheidung des Protokolls wird hinzugefügt: **ACP (Agent Client Protocol) verbindet die IDE mit dem Coding Agent**, tandis que **MCP verbindet den Agenten mit Werkzeugen und Kontext**. IntelliJ kann so als IU und strukturelle Wahrheit dienen, während Claude bleibt, Codex, Junie, GitHub Copilot oder einem anderen Bediensteten ACP Wechselbar. Jeder Agent behält seine eigenen Harness, Modelle, Authentifizierung und Berechtigungen; die austauschbare Einheit ist daher nicht mehr nur die LLM, aber der komplette Agent. Die Werkzeuge des Servers MCP IntelliJ können durch Agenten eingeschränkt werden; für Debugging Scala/JVM, die Werkzeuge debugger
vom Server MCP IntelliJ (vorfixierte Werkzeuge `xdebug_`, die von der Konfiguration des MCP Servers aktiviert werden können) können Stack, Variablen, Threads und Runtime-Beweise ohne Injektion von `println` in den Code sammeln.

<!-- section: s-1 -->
### Architektur IntelliJ 2026.2 empfohlen

```text
IntelliJ IDEA
├── JetBrains AI
│   ├── Code Completion
│   ├── Next Edit Suggestions
│   └── AI Actions / petites transformations
├── Claude Code officiel
│   ├── plugin JetBrains / CLI
│   └── Claude Code Desktop
│       → abonnement Claude Max, agent principal sur raisonnement/debug/architecture
├── Codex
│   ├── agent ACP dans AI Chat
│   ├── ChatGPT Desktop / CLI
│   └── compte ChatGPT/OpenAI
│       → agent principal sur issues standard / reviewer croisé quand Claude écrit
└── GitHub Copilot
    └── couche GitHub-native : issues, PR, review automatique, CI
```

**ACP ersetzt keine offiziellen Integrationen.** Für Claude, Wache **Claude Code Amtlich** als Hauptweg, wenn Sie das Claude Max-Abonnement nutzen möchten: das Plugin JetBrains, CLI und die Registerkarte Code von Claude Desktop teilen die gleichen Harness Claude Code und seine Regeln (`AGENTS.md` als Fallback oder `CLAUDE.md`, Erlaubnisse, hooks, MCP, skills). Claude Code Desktop fügt mehrere einzelne Worktrees-Sitzungen hinzu, visuelle Diffs-Checks, integrierte Terminal/Editor und PR-Tracking. ACP Die Interoperabilitätsschicht, die IntelliJ mehrere Agenten in einer gemeinsamen I.E. aufzunehmen.

Für Codex, den integrierten Agenten in IntelliJ kann sich mit dem **Konto ChatGPT** oder einen Schlüssel OpenAI. Mit einer eigenen Authentifizierung des Anbieters, die Verwendung des Agenten nicht verbrauchen die AI Credits JetBrainsGleiche Logik für die anderen Bediensteten ACP die ihr eigenes Lieferantenkonto verwenden. In-editor-Funktionen **Code Voll** und **Next Edit Vorschläge** Auch die Quote von AI Credits wird nicht verbraucht. **JetBrains AI Ultimate (35 AI Credits / 30 (Tage)** Daher wird vor allem ein Budget für Junie, AI Chat und Cloud-Funktionen JetBrains ; es muss nicht den größten Teil der agentiellen Entwicklung finanzieren, wenn Claude Code und Codex ihre jeweiligen Abonnements verwenden.

Seite notieren JetBrains n 2026 : **Codex ist nun als Agent in den Dl integriert** neben Junie und Claude das Register ACP können weitere Agenten und ein System von **Skills** vollständige Wiederverwendbarkeit MCP. Die IDE wird somit zu einem **Lokale control plane** : Navigation, Diagnose und Debugger bleiben JetBrains, während der Writer oder revier kann durch Sitzung geändert werden, ohne die Umgebung aufzugeben Scala/JVM.

---

