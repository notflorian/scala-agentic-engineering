<!-- section: chapter -->
# 1. Leitprinzip

Für erfahrene Scala-Entwicklerinnen und -Entwickler steht das folgende Verhältnis im Mittelpunkt. Schneller zu programmieren ist zweitrangig.

```text
Nützliche, ausgelieferte und stabile Änderungen
÷
(unnötige Diffs + Review-Anmerkungen + Bugs + verbrauchte Credits + menschlicher Zeitaufwand)
```

Das richtige Mentalmodell:

```text
Du = Tech Lead und letzte Entscheidungsinstanz
IntelliJ = verlässliche Quelle für die Struktur von Scala/JVM und Kontrollzentrale
JetBrains AI = Inline-Unterstützung und unkomplizierte IDE-Aktionen
Codex = Hauptagent für Standard-Issues und unabhängiger Reviewer, wenn Claude implementiert
Claude Code = Hauptagent für Analyse, Debugging und Architektur sowie unabhängiger Reviewer, wenn Codex implementiert
Qwen lokal = kostengünstiger Assistent
GitHub Copilot = GitHub-native Integration für Issues, PRs und automatische Reviews
Aider = kleiner, sauberer Git-orientierter Diff
MCP + Sourcebot + Context7 = gezielt ausgewählter Kontext
RTK + Headroom = weniger Rauschen
Jev = probabilistische Entscheidungsschicht für Klassifizierung, Bewertung und Routing — weder Coding-Modell noch alleinige Instanz für kritische Freigaben
GPT‑6 Luna / GPT‑6.2 Sol / GPT‑6.2 Astra = Codex-Routing für Mikroschleifen, agentenbasierte und Frontier-Aufgaben
Haiku 5.5 / Sonnet 5.5 / Opus 5.5 / Fable 5.2 = Claude-Routing nach Arbeitsumfang, menschlicher Kontrolle und Autonomie
Tests + Stryker4s + CI = letzte, deterministische Prüfinstanzen
```

---

