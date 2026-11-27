<!-- section: chapter -->
# 15A. CI/CD für agentenbasierte Arbeitsabläufe

Die CI ist der endgültige Richter, der das Leitprinzip bestimmt, sofern es an die Prs adaptiert wird, die spezifische Ausfallmodi haben: Tests, die nicht scheitern können, diffs außerhalb der Schablone, teure Schleifen.

<!-- section: s-1 -->
## Die vier gate spezifisch für die Prs-Agenten

```text
1. Prüfung von Größe und Arbeitsumfang: Diff Basis → Kandidat, geschützte Dateien, Größe und Anzahl der Dateien
2. Prüfung der Testqualität: tatsächlich ausgeführte Suites + Mutation Score und nach Risiko relevante Mutanten
3. Review-Prüfung: verifizierte Befunde BLOCKING / REGRESSION_RISK bearbeitet oder menschlich entschieden
4. Budgetprüfung: Jeder Job mit LLM-Aufruf hat ein Zeitlimit UND eine Kostenobergrenze
```

Zwei zusätzliche Achsen, die nach der Basis der vier Gates zu betrachten sind:

- **Architektur-Driftsteuerung** : Thoughtworks Technology Radar (April) 2026) nimmt zur Kenntnis, dass der intensive Einsatz von Agenten die Abweichung zwischen dem tatsächlichen Code und der angestrebten Architektur beschleunigt, und empfiehlt, deterministische Kontrollen zu koppeln (Fitness functions, ✓ ArchUnit, die den Bytecode analysiert JVM und arbeitet daher auch auf Scala kompiliert) mit einer Bewertung LLM Periodisch. ArchUnit-Regel, das Modul `api` hängt nicht von der implementation ab, die in CI kostet weniger als eine Agentenrunde und stoppt eine strukturelle Drift, die weder scalafmt noch Stryker4s sehen.
- **Duplizierungskontrolle[**: SlopCodeBench (Abschnitt 1A) misst eine Duplizierung über die Agentencheckpoints; ein jscpd-Typ-Scan (Kopier-geklebter Kopierer, der die Quellen Scala tötet) auf den betroffenen Dateien verwandelt dieses Signal in metrisches gefolgtes oder gar Gate. Die Duplizierung ist der am wenigsten sichtbare Fehler in der menschlichen Überprüfung und einer der teuersten in der verzögerten Wartung.

Über GitHub, **Copilot Code Review oder Codex Code Review kann als automatisches Signal hinzugefügt werden**, aber ersetzt keines dieser Gates. Eine Bewertung des Bots ist keine menschliche Zustimmung ; überprüft die Regeln GitHub Werden die Ergebnisse der Überprüfung auf Anfrage oder bei der Eröffnung überprüft, so behält die Überprüfung nach der Korrektur die Änderungen vor, die sie rechtfertigen, und die neuen SHA, die eine unabhängige Validierung erfordern.

**Claude Approvals ist kein Qualitätsnachweis.** Eine Regel `claude: approves` nicht allein den Code Review auslösen; `seats: 1` kann der Autor zählen und `seats: 0` kann ein Merge ohne menschliches Lesen ermöglichen. GitHub kann auch die Genehmigung des Bots in seiner Review-Quote zählen. Für den Workflow dieses Leitfadens, halten `claude: comments` zunächst unabhängige menschliche Angreifer im Team und ein Solo-Merge. Benutze niemals einen probabilistischen Einstufungsrichter als einzigen Schiedsrichter einer kritischen Veränderung.

Das Vorhandensein von `.claude/approvals.yml` kann automatische Reviews auf den erfassten Pfaden deaktivieren, auch im Beobachtungsmodus: um sie zu halten, Referenz `claude/code_review` in den Regeln (z.B. unter `advisory`). Eine Bedingung Aprovals liest nicht die Ergebnisse von CI: kompiliert, getestet, scalafmt, Sicherheit und Mutation testing als required checks GitHub getrennt. Im Team schützt das Ziel und die Politik mit CODEOWNERS, verhindert die bypass-Besuche an die Agenten und schaltet alte Genehmigungen ab, wenn sich der Diff ändert. Macht den Check Aprovals erst nach der Bewertung der Entscheidungen obligatorisch; aktiviert weder Auto-Meerge noch Schwanz ohne effektives menschliches Gate für die notwendigen Änderungen. Ein grüner Check, eine gelöste Diskussion oder ein Kommentar
Keine Fehler sind eine Berufsvalidierung.

<!-- section: s-2 -->
### GitHub Rulesets und Gate-Unabhängigkeit

Benötigt required checks aus der erwarteten Integration, ohne bypass für Agenten-Identitäten ; schützt die Zielzweige, Verbot der Kraft-Push und Löschung, Genehmigung der letzten Änderungen und Ungültigkeit der alten Genehmigungen, wenn sich der Diff ändert. Im Team, fordern die Zustimmung eines unabhängigen Menschen, und `CODEOWNERS` für Kontrolldateien ; Solo, nicht konfigurieren eine Regel, die vom Autor nicht zu erfüllen ist, behält das menschliche merge und eine separate politische Kontrolle. Zählt nicht eine Bot-Review als Mensch. Ein Schlange ist optional, unter der Bedingung der Überprüfung `merge_group`], und verlangen die Gates des Integrationscommit. Im Falle von Konflikten, Wechsel von SHA oder fortgeschrittenen Basis, neu bewertet den Zustand ; eine CI grüne auf einer alten Revision nicht gültig neuen Kandidaten.

<!-- section: s-3 -->
## Beispiel: `.github/workflows/ai-review.yml`

Beispiel für das Zwei-Module-Projektarchiv im Abschnitt 11 (sbt 1.x). Verfeinert die Aktionen zu einem vollständigen geprüften SHA und überprüft ihre transitiven Abhängigkeiten ; aktualisiert sie durch dedizierte PR. Die Basis SHA kommt von der Veranstaltung GitHub, kein PR-Feld, das vom Autor kontrolliert wird. `github.sha` ist der Kandidat für Integration für `pull_request` und `merge_group` ; die menschliche Review bezieht sich auf den Diff base/PR head, getrennt von diesem Test-Commit. Bei einem Schwanz Merge müssen die Kontrollen auch auf der merge Gruppe durchgeführt werden.

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

**Vertrauensgrenze der CI :** se YAML illustriert die Checks, nicht nur einen unverletzlichen Mechanismus. Die PR kann die darin enthaltenen Skripte und Workflows ändern, oder sogar die Build-Befehle oder Berichte. Schützt Workflows, Skripte, Testregeln, Richtlinien und `CODEOWNERS` ; wenn verfügbar, erfordert ein vertrauenswürdiges required workflow aus einem geschützten Projektarchiv/Commit (Organisations-Rule) und lädt den Validator von dieser Quelle aus und nicht vom Kandidaten aus. Eine legitime Änderung der Politik erfolgt durch eine separate menschliche PR und Validierung. Allein ohne required workflow externe, vergleicht diese Dateien an der Basis und erlaubt keine Merge, bis eine Gate-Änderung überprüft wurde. `AGENTS.md`.

Das PR-Checkout kann willkürlichen Code über sbt ausführen: keine privilegierten Geheimnisse, keine Schreibtoken, keine [`pull_request_target`], die den PR-Code ausführen, keine versteckten bevorzugten Jobs ohne Herkunftskontrolle. Die Testberichte sind operative Beweise, keine unverletzlichen Bescheinigungen, wenn der Testcode selbst feindlich ist. Archiviert Berichte und Herkunft in der CI entsprechend der Projektpolitik; die Validierung muss auf den Endanwärter (und auf den Commit, wenn anders geliefert).

Punkte der Lehre:

* **Deterministische Richter gehen zuerst** : Kompilierung, Format und gezielte Tests sind im Vergleich zu einem Anruf kostengünstig LLM Einen Job LLM der auf Code läuft, der nicht kompiliert ist aus dem Budget verbrannt;
* wenn eine Review LLM von CI ist wirklich automatisiert, gib ihm eine **Schlüssel API gewidmet**, ein Timeout und eine eigene Ausgabenobergrenze für den Job; für den hauptsächlich interaktiven Einsatz über die Abonnements Claude und ChatGPT, diese Automatisierung bleibt optional;
* **Arbeit LLM ist read-only** : Er kommentiert die PR, er tötet nie. Ein Agent, der in der CI stellt das Problem ^ zwei Schreibkräfte der Fachgruppe neu 16, schlimmer (ohne Menschen in der Schleife) ;
* **`sbt --client` auf lokaler Ebene, JVM frisch in CI** Der Dämon sbt ist der Hebel für die Teilnehmerschleifen; CI, ein kontrollierter Abhängigkeits-Cache kann die Auflösung beschleunigen, ersetzt aber weder die Tests noch die Isolierung. **sbt 2.0.0 ist stabil seit dem 14 Juni 2026** ; verwendet mindestens **2.0.7** (oder **1.13.0** auf dem Zweig 1.x) aufgrund des BSP/TCP-Patch vom 21 August: Definitionen von Build in Scala 3JDK 17 Minimum, nativer Kunde `sbtn` (ein viel schnellerer Start, direkt nützlich für die Agentenschleifen), lokales/externes Cache kompatibel Bazel und `test` Inkremental. Dieser Leitfaden folgt dem Übereinkommen sbt 1.x: Migration nach sbt 2.x ist ein kritischer Build-Änderung, die nie auf einen menschlichen ✓-Plan Agenten delegiert, dedizierte Branche, Überprüfung der Kompatibilität von Plugins (60+ Tragen, darunter Play und Scala.js läuft), dann
  Anpassung dieser Jobs.

**Autofix Codex n CI : ausdrückliche Ausnahme vom read-only review Job.** Wenn ein gehosteter Patch-Feed wirklich benötigt wird, trennt der Erzeugungsjob vom Patch (ohne Push-Recht) vom kontrollierten Push-Job; begrenzt die Auslöser auf genehmigte Ereignisse und Akteure. Ermöglicht niemals einen unzuverlässigen Code aus einer PR mit bevorzugten Schreibgeheimnissen oder Token (insbesondere über `pull_request_target`) Die Aktien werden von SHA fixiert, minimale Berechtigungen, ein Timeout, ein externes Budget und ein Wettbewerbssperre von PR angewendet; überprüft den SHA head vor der Veröffentlichung, und schaltet dann die erforderlichen Checks wieder ein. Keine Kraft-Push, Selbst-Genehmigung oder merge durch den Job LLMKommentare, Logs und Patches bleiben unzuverlässige Daten; ein Versagen darf niemals zu einer Veränderung der Gates führen.

Die gleiche Aufteilung wird in GitLab CI umgesetzt: drei Praktika ([`deterministic`, `mutation`, `llm-review`), dieselben Gates, [`rules: changes`, um Stryker nur auf den betroffenen Modulen zu starten.

---

