<!-- section: chapter -->
# 8. Empfohlene Repository-Struktur

Fügt diese Dateien oder Ordner zur Wurzel hinzu, wobei ** nur ein Ort der Wahrheit[** zu halten ist:

```text
AGENTS.md                       # Source commune, courte, versionnée
CLAUDE.md                       # Optionnel :Importe @AGENTS.md + règles Claude spécifiques
GEMINI.md                       # Pointeur vers AGENTS.md ou symlink selon ton outil
.github/copilot-instructions.md # Règles de review / coding agent GitHub Copilot, si utilisé
.github/instructions/           # Règles Copilot path-specific si nécessaire
.aiignore                       # Exclusions IA : secrets, gros artefacts, generated
.claude/rules/scala.md          # Règles Claude path/scopes si utiles
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

Das Ziel besteht nicht darin, Dokumentation zu sammeln, sondern zu vermeiden, dass der Agent bei jeder Sitzung die gleichen Regeln entdeckt. Die Datei muss kurz, stabil und funktionell bleiben.

> **Synchronisierung von Kontextdateien:** Codex lädt die globalen Anweisungen von `CODEX_HOME` und
> die Dateien des Projektpfades von der Wurzel zum aktuellen Verzeichnis. Auf jeder Ebene,
> `AGENTS.override.md` Prämie auf `AGENTS.md` ; Anweisungen am nächsten zum Arbeitsverzeichnis
> Als letztes werden die Fallback-Namen und die maximale Größe hinzugefügt.
>
> Claude Code, mit der integrierten Mod `cc-plugin-agents-md`, verwendet die Standardeinstellung `claude-md-or-agents-md`:
> `AGENTS.md` wird geladen, wenn keine `CLAUDE.md`, `.claude/CLAUDE.md` oder `CLAUDE.local.md` in der
> aktuelles Verzeichnis oder seine Eltern. Benutzer-/Benutzer-Anweisungen und `.claude/rules/` fortfahren
> `AGENTS.override.md` wird nicht von Claude über diesen Fallback gelesen.
> `claude-md-and-agents-md` lädt beides, ohne eine bereits importierte Datei zu duplizieren.
> auf bestimmten Flächen nicht verfügbar; es ersetzt nicht einen expliziten Import, wenn erforderlich.
>
> Für diesen gemischten Workflow, bevorzugt eine gemeinsame `AGENTS.md`, und wenn eine `CLAUDE.md` existiert, starte es mit
> `@AGENTS.md`. Bewahre dann nur die wirklich spezifischen Regeln für Claude. Überprüfen Sie die Anweisungen
> laden in eine neue Sitzung (`/context all` Claude-Seite, und bitten Sie Codex, die Dateien zu listen
> . Für Untermodule ist auch die Entdeckung aus dem realen Verzeichnis zu überprüfen.
> Kein Override darf eine externe Sicherheitsregel schwächen.

Neben Claude Code: [**Rule** unter `.claude/rules/` ermöglichen es, die Projektanweisungen mit gezielteren Anweisungen zu ergänzen, z. B. durch Unterbaum oder Aufgabentyp. Oft ist es besser als eine riesige `CLAUDE.md`, wenn diese Datei existiert.

Auch: die **auto-memory** Claude Code erfordert eine neue Version, die von v dokumentiert wird2.1.59+. Die ersten Zeilen von `MEMORY.md` können automatisch geladen werden, und Subagenten können ihren eigenen Speicher haben. Verwende diesen Speicher für wiederkehrende Pattern-Erinnerungen, nicht für Geheimnisse, nicht für unveröffentlichte Architekturentscheidungen und nicht als Ersatz für versionierte Dokumentation.

<!-- section: s-1 -->
## Mindestinhalt von `AGENTS.md`

```text
Build, test and formatting commands (exact commands)
Non-obvious architecture boundaries and business invariants
Public API / JSON / migration constraints
Protected files and permitted write scope
Scala conventions absent from existing documentation
Stop conditions and definition of done
Pointers to relevant docs and spec
```

Schreibe diese Regeln **für den Agenten, nicht als menschliche Dokumentation** : bevorzugt nachprüfbare Pfade, Befehle, Zahlen und Bedingungen. Behalte einige hundert Wörter als Ausgangspunkt. README, Tutorials, die vollständige Liste der Module und Modellevergleiche bleiben in `docs/`, auf Verlangen geladen.

<!-- section: s-2 -->
### Route in der Benutzerkonfiguration

Bewahrt die Matrix des Abschnitts [3 in einem Routing-Dokument oder in einem Benutzerprofil [Codex/Claude anstatt in jedem `AGENTS.md` : Das Projektarchiv muss unabhängig von der Vorlage bleiben. Wenn ein Orchester diese Matrix überprüfen muss, fügt er nur einen Zeiger hinzu. Die Arbeits- und Sicherheitsanforderungen ändern sich nicht je nach Modell.

<!-- section: s-3 -->
## Mindestinhalt von `CLAUDE.md`

```markdown
@AGENTS.md

## Claude Code
Use plan mode for risky multi-file changes.
```

Verschiebt die allgemeinen Regeln von der alten `CLAUDE.md` auf `AGENTS.md` (keine Duplizierung). Der Claude-Planmodus ist eine Vorliebe für Harnesen; die tatsächlichen Berechtigungen bleiben in der Konfiguration und in der Sandbox.

<!-- section: s-4 -->
## Warum `AGENTS.md`

Mit Codex und die integrierte Mod `cc-plugin-agents-md` von Claude Code (fallback) `AGENTS.md` Standard), `AGENTS.md` Noch natürlicher wird der gemeinsame Vertrag. Jüngste Arbeiten an den Kodierungsagenten zeigen, dass eine solche Befehlsdatei die Ausführungszeit und die Ausgabetoken reduzieren kann, während eine vergleichbare Ergänzungsrate beibehalten wird. Die praktische Wirkung ist einfach: weniger wiederholte Kontexte, weniger vergessene Anweisungen, weniger Ablenkung zwischen Werkzeugen.

> **Status der Beweise: gemischtes Ergebnis, kein automatischer Gewinn.** Eine weitere Bewertung von 2026 stellt fest, dass die Dateien
> Besonders wenn sie die Kosten um mehr als 20 % erhöhen, wird die Erfolgsquote häufig leicht gesenkt.
> Das README wiederholen oder fügen unnötige Anforderungen hinzu. Die von den Betreuern geschriebenen Dateien machen es besser als die
> die automatisch erzeugt werden, aber auch gemessen werden müssen.
>
> Korrigierte Regel: `AGENTS.md` muss nur enthalten , was tatsächlich eine genaue Aktie ändert,
> Nicht offensichtliche Invarianten, verbotene Dateien, fehlende README-Übereinkommen und Halteregeln. Keine Führung
> Projektarchiv-Erzählung, kein Technologiekatalog, keine generischen Ratschläge.
> , die mit und ohne die Datei. Quantitative Ergänzung aus der
> Die gleiche Literatur: unter **~500 Wörter[** bleiben, konzentriert sich auf Testnormen, Stilkonventionen und
> Gefahrenwarnungen ✓ keine geführte Führung des Projektarchivs ✓ und wiederholen Sie die Datei als Code zu jeder Zeitschrift.

<!-- section: s-5 -->
#### Validierungsprotokoll: Messung der Wirksamkeit von AGENTS.md

Eine AGENTS.md, die nichts an dem Ergebnis ändert, ist der tote Kontext, der Tokens in jeder Sitzung kostet.

**Test A/B auf 10 repräsentative Aufgaben:**

1. Wählt 10 tatsächliche backlog-Aufgaben (mix greenfield/bugfix/refactor)
2. Für jede Aufgabe führt 2 mal:
    - Run A: mit AGENTS.md im Kontext
    - Run B: ohne AGENTS.md (oder mit leerer Version)
3. Messung für jeden Run:
    - Anzahl der Runden vor der Vervollständigung
    - Anzahl der betroffenen Off-Scope-Dateien
    - Anzahl der Zusammenstellungsfehler
    - Einhaltung von Testvereinbarungen
    - Gesamtkosten in Tokens
4. Vergleich:
    - Wenn AGENTS.md KEINE metrische → es unnötig reduziert, entfernen Sie es
    - Wenn es einige metrische → behält nur die nützlichen Abschnitte
    - Wenn es die Kosten erhöht, ohne die Qualität zu verbessern → es schädlich ist

**Indikatoren für ein wirksames AGENTS.md:**

- Agent zitiert genaue Testbefehle, ohne sie erneut zu entdecken
- Der Agent berührt keine verbotenen Dateien, ohne dass er zurückgerufen wird.
- Der Bedienstete hält die Ernennungsvereinbarungen vom ersten Tag an ein
- Die Zahl der "Rufe" von Menschen in der Sitzung nimmt ab

**Indikatoren eines schädlichen AGENTS.md:**

- Der Agent produziert grünere Diffs (er "gelt" zu viele Regeln)
- Die Kosten für Tokens steigen > 20% ohne messbare Verbesserung
- Der halluzinierende Agent von Befehlen, die nicht in der Datei sind
- Die allgemeinen Vorschriften brechen die spezifischen Vorschriften

Wartungsregeln: Jedes Mal, wenn eine Regel von AGENTS.md von einem Agenten verletzt wird UND wenn die Verletzung in einer Review erfasst wird, ist die Regel entweder falsch formuliert oder falsch. Korrigiert sie oder materialisiert sie in einer Kontrolle des Abschnitts 5 oder 15]A anstatt einen weiteren Satz hinzuzufügen.

<!-- section: s-6 -->
#### Prüfung von *rule drift* : überprüfen, ob die Anweisungen die tatsächliche repo noch beschreiben

Die Regeln für Agenten sind freiwillig spezifisch ✓ Pfade, Befehle, Module, nicht erlaubte Dateien, und genau deshalb altern sie schnell. Eine falsche Anweisung ist schlimmer als eine fehlende Anweisung: sie zwingt den Agenten, `AGENTS.md` mit einem Basiscode zu versöhnen, der sich bereits geändert hat.

Fügt `scripts/ai-rules-drift` hinzu und führt es nach jeder Änderung der Architektur/Build aus, dann mindestens einmal pro Woche, wenn sich das Projektarchiv viel bewegt:

```text
Vérifier :
- chaque chemin cité dans AGENTS.md / CLAUDE.md existe encore ;
- chaque module sbt cité existe encore ;
- chaque commande de compile/test/format est encore valide ;
- aucun nom de DB, service, dossier ou script supprimé n'est encore référencé ;
- les fichiers « interdits » correspondent encore aux vraies surfaces critiques ;
- si CLAUDE.md existe, il importe ou complète toujours la source commune attendue.
```

Das Skript kann deterministisch für einfache Checks bleiben (`test -e`, grep der Module, Befehle `--help`/dry-run) und tun nur **Bericht** zweideutige Fälle. Erlaubt niemals dem Agenten, der die Drift erkennt, seine eigenen Regeln zu schreiben und dann selbst zu genehmigen: das Regeldiff wird als Code überprüft.

<!-- section: s-7 -->
### Anweisungen GitHub Copilot ohne Duplizieren `AGENTS.md`

Wenn das Projektarchiv verwendet GitHub Copilot, aufbewahrt `AGENTS.md` als gemeinsamer Vertrag und als Vorbehalt `.github/copilot-instructions.md` die spezifischen Erwartungen der **Überprüfung GitHub** : Schwere der Findings, PR-Konventionen, zu überwachende Dateien und Kriterien, die angezeigt werden müssen. `.github/instructions/**/*.instructions.md` erlauben, diese Regeln auf dem Weg zu spezialisieren. Vermeide es, die gesamte Architektur oder alle Regeln zu kopieren Scala : eine gemeinsame Anweisung muss in `AGENTS.md`.

Copilot Code Review liest die Anweisungen und Skills der ** Kopfzweig der PR**. Eine Änderung dieser Regeln ist daher Teil der zu überarbeitenden Codeoberfläche: Ein Agent darf seine eigenen Belastungen im selben PR nicht lockern können, ohne dass diese Änderung ausdrücklich sichtbar und validiert ist.

