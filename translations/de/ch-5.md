<!-- section: chapter -->
# 5. Standardablauf für fachliche Aufgaben in Scala

<!-- section: s-1 -->
## Schritt 0: menschliches Bild

Vor der KI schreibst du oder erklärst:

```text
Ziel:
Aktuelles Verhalten:
Erwartetes Verhalten:
Fachliche Vorgaben:
Zu erhaltende öffentliche API:
Voraussichtlich betroffene Dateien:
Gezielte Tests:
Validierungsumgebung:
Risiko:
Akzeptanzkriterium:
```

nummeriert die wichtigen beruflichen und invarianten Anforderungen ([`REQ-01`,`REQ-02` usw.). Für jede Anforderung, erklärt der Test oder der Nachweis, der vor der Implementation erwartet wird; eine Anforderung ohne Oracle muss ausdrücklich nicht abgedeckt und abgeschottet sein. In der PR kombiniert Anforderung, Befehl/Test, Ergebnis, validierter SHA und Grenzen des Nachweises. Die Matrix der Rückverfolgbarkeit kann für ein Trivial-Ticket sehr kurz bleiben.

`Validation harness` muss benennen **vor dem Write-Modus** die Nachweise, dass der Bedienstete selbst ausführen kann: gezielte Zusammenstellung, Einheitstests/Integration; ScalaCheck, scalafmt, ggf. Stryker4s Wenn du noch nicht weißt, wie du beweisen kannst, dass die Änderung korrekt ist, ist die Aufgabe nicht delegiert.

Ohne das bezahlst du die Modelle, um das Problem herauszufinden, anstatt es zu lösen.

> **Positionierung vs. den Stand der Kunst 2026 (✓ Spec-Driven Development ✓)**: Dieses Bild ist genau das, was
> die Industrie hat unter dem Namen SDD formalisiert, wurde das dominierende Gegengewicht zum   ✓ vibe coding ✓ die spec als
> Das profitabelste Artefakt des Menschen, wenn der Agent den Code schreibt. Das Werkzeug (GitHub Spec Kit, OpenSpec,
> AWS Kiro, EARS-Rating für testbare Anforderungen) kann diesen Workflow strukturieren, ist aber nicht obligatorisch:
> praktische Anleitung bereits die Variante **spec-anchored** (der Rahmen und überlebt die Aufgabe, Code + die Tests bleiben
> die Quelle der Wahrheit), das ist die empfohlene Haltung für den bestehenden Berufscode  ✓ im Gegensatz zu
> **spec-as-source** (der Mensch bearbeitet nur die Spekta, noch experimentell. Dosierungsregel aus der Rückkehr)
> Feld: Die Detailebene der Spect muss der *Criticity* des Codes .] folgen, um ein Einweg-Skript zu erstellen ist
> Vergeudung, Unterspezizierung eines öffentlichen Vertrages ist eine Garantie Drift.
>
> **Werkzeug auswählen SDD ohne Framework-Sprawl.** Die Landschaft SDD
> dépasse désormais la trentaine de frameworks (Spec Kit, OpenSpec, Kiro, BMAD-METHOD, GSD, Tessl....
> Praxis, die sich daraus ergibt: **GitHub Spec Kit** für Greenfield (Konstituierung) → specify → Clarify → plan →
> checklist → tasks → analyze → implement → converge, mit fakultativen Kontrollschritten;
> **OpenSpec** für iteratives brownfield ✓ specs, die in der Repo mit *delta markers[* durch Änderung, die
> Position, die der spec-anchored-Variante dieses Leitfadens am nächsten steht; **AWS Kiro**, wenn Sie die integrierte EARS-Rating wollen
> und das AWS-Ökosystem. Keines ist eine Voraussetzung: wenn `AGENTS.md` + das oben dargestellte Bild-Paket + die Gates CI
> (Abschnitt 15A) tun bereits die Arbeit, fügen Sie ein Framework SDD fügt Kontext, nicht Qualität. Regel nein
> verhandelbar: Die spec lebt in der repo und überprüft sich als Code-    ✓ ein versionsfrei gehaltenes spec wird zu einer Sekunde
> Quelle der Wahrheit divergiert.

> **Zwei Gurte, die nicht verwechselt werden dürfen.** Ein Papier SDD veröffentlicht am 31 August 2026 schlägt eine nützliche Unterscheidung zwischen
> **technical harness** (Modell, Werkzeuge, Kontext, Erlaubnisse, Tests) und [**methodological harness[** (Spek, Rollen,
> Verantwortlichkeiten, Überprüfung und Release-Behörde). **bestätigt** Struktur dieses Leitfadens: Verbesserung
> Claude Code, Codex oder MCP ersetzt nicht die Disziplin Humane Spezifikation und Validierung.
> , jedoch hauptsächlich konzeptuell und weitgehend auf der grauen Literatur basiert; verwendet diese Unterscheidung
> als Designrahmen, nicht als empirischer Beweis dafür, dass ein gegebenes Framework SDD die Produktivität verbessert.

> **Erste tatsächliche Praxisdaten.** Die CMU/Google-Studie ✓ Spec-Driven Development as Prescribed
> und as Practiced     ✓ (deklarativ, nicht repliziert) stellt fest, dass erfahrene Praktiker bereits SDD von
> **selektive Art und Weise, besonders für neue Funktionen oder riskante Änderungen**, mit Spektakeln, die von Agenten aus einer Absicht geschrieben wurden
> Der Hauptfehler ist, dass die
> **stiller Ablauf spec ↔ code**, wenn kein Instandhaltungsplan existiert; die Thoughtworks-Rückgaben fügen hinzu
> [*instruction bloat* (Spektrume und Kontexte, die wachsen, bis der Agent den Faden verliert). Dies bestätigt zwei
> Regeln dieses Leitfadens: Dosierung durch Criticity, und spec Version und überarbeitet. Fügt nur eine dritte Regel hinzu:
> ** ein Test, der vom Agenten geschrieben wurde, bestätigt nicht seine eigene spec[** ; hält den Reproduktionstest, der vor dem Patch fehlschlägt
> und die Mutation testing (Abschnitt 5, Schritt 4) Werkzeug, **`/speckit.converge`** relinkt den Code vor dem
> `spec.md`, `plan.md` und `tasks.md` und **fügt nur die fehlenden Aufgaben hinzu zu `tasks.md`**Es ist eine Kontrolle von
> Nützliche Konsistenz nach der Implementierung, **kein Orakel**: Weder unabhängige Tests noch die Beurteilung durch den Menschen sollten
> unter dem Vorwand gelöscht werden, dass Spec Kit kündigt ✓ Converged  ✓.

<!-- section: s-2 -->
#### Operatives speclat (Kopier-Einfügen)

Dieses Template materialisiert die spec-anchored-Variante des Führers. Es lebt in der repo (z.B. `specs/TICKET-123.md`) und reviewt sich als Code.

<!-- section: s-3 -->
# SPEC: [TICKET-123]  ✓ [Short Titre]

<!-- section: s-4 -->
## 1 Ziel (1 Satz, Aktionsverb)

[ex: "Fügen Sie eine Mengenrabattrate pro Schritt bei DiscountService"]

<!-- section: s-5 -->
## 2 Nicht-Ziele (Erläuterung, Anti-Drive)

- [z. B.: "Änderung der bestehenden Rabattberechnung durch Gutscheincode"]
- [z. B.: "Rühren Sie nicht die [API öffentlich zugängliche Plug-in-Module an"]

<!-- section: s-6 -->
## 3 Erwartetes Verhalten (Berufsregeln, nummeriert)

1. [Regel] 1 : wenn Menge >= 10, Rabatt 5%]
2. [Regel] 2 : wenn Menge >= 50, Rabatt 12%]
3. [Regel 3 : Die Lager nicht kumulieren, die höchste gilt]

<!-- section: s-7 -->
## 4. Technische Einschränkungen

- API zu bewahrende öffentliche Sicherheit: [genaue Unterschriften]
- Serialisierung JSON: [unverändert / X-Feld mit backward compat hinzufügen]
- Leistung: [keine zusätzliche DB-Anfrage im Hot path]
- Wettbewerb: [unveränderlicher Zustand / atomischer Zustand erforderlich]

<!-- section: s-8 -->
## 5. Wahrscheinlich betroffene Dateien

- `src/main/scala/.../DiscountService.scala`
- `src/test/scala/.../DiscountServiceSpec.scala`

<!-- section: s-9 -->
## 6.

| Anforderung/invariant | Erwarteter Nachweis |
|----------------------|-----------------|
| REQ-01: Schwellenwert 10 | Einheitstest: 9 → 0 %, 10 → 5 % |
| REQ-02: Schwellenwert 50 | Einheitstest: 49 → 5 %, 50 → 12 %; übergebene Eigenschaft ≤ 12 % |
| REQ-03: Nicht-Kumulierung | Nicht-Regressionstest auf die Kumulierung; Rückgabe durch unveränderten Gutscheincode |
| REQ04: Vertrag JSON | Kompatibilitätstest |
| REQ-05: Leistung | Messung der Anzahl der DB-Anfragen zum Integrationsszenario |

- [ ] Mutation testing: wichtige Punkte / Mutanten auf die betroffenen Dateien zu rechtfertigen
- [ ] Ergebnisse im Zusammenhang mit SHA und Anforderungen; ausdrückliche Ausnahmen und Restrisiken

<!-- section: s-10 -->
## 7 Risiken und Migrationen

| Risiko               | Wahrscheinlichkeit | Auswirkungen | Migrieren                      |
|----------------------|-------------|--------|---------------------------------|
| [Arrondi BigDecimal] | Mittel       | Hoch   | [RoundingMode.HALF_UP] |

<!-- section: s-11 -->
## 8. Definition von Done (endgültige Checkliste)

- Kompiliert ohne Warning
- [ ] Grüne gezielte Tests
- [ ] scalafmtCheckAll Pass
- [ ] Review zweites Modell durchgeführt
- [ ] Diff < [N] Zeilen
- [ ] Keine Dateien aus dem Scope geändert

Gliederungsebene geeignet für die Kritik:

- Einweg-Skript → Abschnitte 1, 2, 6 ausreichend
- Öffentlicher Vertrag / Geld / Sicherheit → alle obligatorischen Abschnitte

---

<!-- section: s-12 -->
## Schritt 1: gezielte Suche

Verwende in dieser Reihenfolge:

1. **Sourcebot** zum Finden von Dateien, Anwendungen, Tests.
2. **IntelliJ** zur Überprüfung von Symbolen, Typen, Hierarchien.
3. **Context7** wenn API externe oder eine neue Version ist beteiligt.
4. **[Qwen local** zur Herstellung eines Briefings.

Prognose Qwen:

```text
Analysiere diese Dateien und liefere:
- Zusammenfassung des fachlichen Ablaufs
- beteiligte Klassen und Methoden
- zu erhaltende Invarianten
- vorhandene Tests
- Risiken
- Unklarheiten
- einen klaren Prompt für Claude Code

Schlage noch keinen Patch vor.
```

---

<!-- section: s-13 -->
## Schritt 2: Plan durch den Agenten writer, ohne Änderungen

Prompt writer (Codex oder Claude Code) :

```text
Du implementierst diese Aufgabe.

Ziel:
[Ziel]

Vorgaben:
- minimaler Diff
- keine Änderung der öffentlichen API ohne ausdrückliche Freigabe
- vorhandenes Verhalten bewahren
- Tests hinzufügen oder anpassen
- in kleinen Schritten vorgehen
- Risiken erläutern
- vor der Freigabe nichts ändern

Sieh dir zuerst den Code an und schlage einen Plan vor.
```

Regel aus Dokumenten: **Kein Plan, kein Write mode**.Der Plan muss die zu bearbeitenden Dateien, die nicht berührenden Dateien, die Teststrategie, die Risiken und die erwartete Größe des Diffs auflisten.

---

<!-- section: s-14 -->
## Schritt 3: Implementation durch kleine diffs

Prognose:

```text
Führe ausschließlich Schritt 1 aus.
Lass die übrigen Schritte unangetastet.
Halte den Diff klein.
Gib nach der Änderung Folgendes an:
- geänderte Dateien
- Grund für jede Änderung
- Befehl für den gezielten Test
```

Für Scala, vermeidet große automatische refactors. 30 à 300 Diff-Linien, wenn möglich. Feldrückkehrer und neue Studien über die Prs-Agenten konvergieren zu kleinen und bornierten PRs, leichter zu wiederholen und weniger anfällig für Schach CI. Auf organisatorischer Ebene die Untersuchung der Einführung Claude Code / Copilot CLI bei Microsoft (arXiv, Juli) 2026, Zehntausende Ingenieure)~24% der PRS, die bei den Adoptern zusätzlich zu verzeichnen sind, sind real, aber in PRs materialisiert *Reviews möglich*Nicht in riesigen Diffs.

---

<!-- section: s-15 -->
## Schritt 4: Validierung IntelliJ + Tests

Agenten LLM sind bekannt für Happy-path-Tests (Tests, die passieren, aber nicht prüfen Fehlerfälle oder Grenzen). Empfohlene Reihenfolge für [[Scala/SBT:

```plaintext
scalafmtCheckAll
compile
Test / compile
testOnly <TestCiblé>
IntegrationTest / testOnly <TestCiblé>
```

Nur dann, wenn das Risiko es rechtfertigt:

```plaintext
test
IntegrationTest / test
```

> **Anmerkung sbt :** Konfiguration `IntegrationTest` ist **dépréciée depuis sbt 1.9.0** zugunsten eines Teilprojekts
> dediziert (z.B. ein Modul `it`, das `dependsOn(core % "test->test")`) oder taggierte Tests. Wenn Ihr Projekt es verwendet
> noch, die oben genannten Befehle bleiben gültig, aber nie lassen Sie einen Agenten diese Konfiguration allein migrieren.    ✓
> Es ist genau die Art der Änderung `build.sbt`, die durch eine explizite Validierung erfolgen muss.
> Modul,
> direkt auf einem Unterprojekt `it`. Denken Sie auch daran, dem Agenten den schnellsten verfügbaren Befehl zu geben:
> `sbt --client` (oder Bloop) vermeidet es, den Start der JVM bei jeder Iteration der Test-Korrektur-Schleife zu bezahlen.
> die
> kann die Agentenschleifen beschleunigen. **sbt 2.x**, `sbt` verwendet bereits den nativen Client-Server-Modus `sbtn`
> Standard , `sbt --client` bleibt eine explizite Form. Messen Sie den Start auf das tatsächliche Projekt: Migration 1.x → 2.x
> und Änderung von `build.sbt` erfordern eine menschliche Validierung (siehe Abschnitt [15]A).
>
> Doch. `serverConnectionType` ist konfiguriert zu `Tcp`, sbt 1.4.0 à 2.0.6 ist
> anfällig für eine nicht authentifizierte Codeausführung über BSP. Löscht diese Einstellung oder geht auf **sbt 1.13.0
> oder 2.0.7**. Der Standard-Lokaltransport (Unix Socket oder Named Pipe) wird nicht beeinflusst. Dieses Update ist
> Priorität, bevor Sie den Server sbt einem entfernten IDE, Agenten oder Container aussetzen.

<!-- section: s-16 -->
#### Optimierungen sbt für Agentenschleifen

Die Geschwindigkeit der kompilierten Testschleife ist der erste Hebel für die Produktivität. Empfohlene Konfiguration in `.sbtopts` (repo) :

<!-- section: s-17 -->
# .sbtopts ✓ optimiert für Agentenschleifen

```plaintext
-J-Xms2g
-J-Xmx8g
-J-XX:+UseZGC
-J-XX:+UseStringDeduplication
-Dsbt.supershell=false
-Dsbt.color=false
-Dsbt.log.noformat=true
```

Erläuterung der Wahl:

- `UseZGC`: Standard-Option gegen G[1 auf der tatsächlichen Ablagerung zu messen; verspricht keine systematischen Gewinne oder Pausen unter 1 ms
- `supershell=false` und [`color=false`: reduziert den Lärm in den Ausgängen des Agenten (weniger Tokens, weniger roter Kontext)
- `noformat=true`: idem, Rohausgänge leichter zu bewegen

Unter sbt 2.x, `sbt` startet bereits den nativen Client standardmäßig; `sbtn` bleibt ein nützlicher expliziter Eintrag :

<!-- section: s-18 -->
# Erstes Starten (Start des Servers)

`sbt`

<!-- section: s-19 -->
# Nächste Anrufe vom Agenten (fast sofort starten)

`sbtn "compile"` `sbtn "testOnly *DiscountServiceSpec"`

Server-Einstellungen in `project/server.sbt`:

```scala
// Keep the build server on a local transport.
Global / serverConnectionType := ConnectionType.Local
```

Der lokale Transport ist in der Regel der Fehler: **stellt den Server nicht aus sbt als TCP** Sie können die Agenten beschleunigen. `build.sbt` nur zur Verschleierung von Wiederholungen oder Überprüfungen: `onChangedBuildSource := IgnoreSourceChanges`, `Test / fork := false` und die Deaktivierung von Scaladoc können das Ergebnis nicht repräsentativ für die CI oder das Verhalten der Tests ändern. Bevorzugt das Modul und die Folgerungen (`project`, `testOnly`) ohne ihre Semantik zu verändern. **sbt 2.x, `test` ist inkremental und kann seine Ergebnisse im Cache wiederverwenden** : verwendet `testFull` für eine vollständige Validierung vor einer PR oder CI.

**Benchmark vor/nach deinem Depot.** Vergleicht mit JVM und identische Optionen, über mindestens zehn Zyklen Inkrementale Zusammenstellungen + gezielte Tests: mediane Latenz, p95, neu starten sbt, Speicherdruck und Stabilität der Tests. Nicht verschlüsselt auf ein anderes Projekt als Garantie.

Für Play Framework oder Multimodul-Projekte:

```plaintext
sbt "project api" compile
sbt "project api" "testOnly *DiscountServiceSpec"
sbt "project integration" "testOnly *OrderFlowSpec"
```

Der wichtigste Punkt bleibt: bittet die KI nicht nur um Vorsicht, sondern drehe die Tests. Die deterministischen Sicherheitsleute schlagen die Textanweisungen.

Wähle die Validierungen nach dem tatsächlichen Risiko, ohne unnötige Werkzeuge zu stapeln:

| Risiko Scala/JVM | Wichtiger Nachweis |
|------------------|-------------------|
| Berufsberechnung | ScalaCheck, Grenzen, Mutation testing |
| Binärkompatibilität / TASTy | MiMa / TASTy-MiMa, wenn relevant |
| REST / JSON | Vertragstests, Muster und Kompatibilität |
| Wettbewerb und Auswirkungen | Beschluß, Besiegelung, Timeout, Freigabe der Ressourcen |
| Spark | Deterministische Daten, Nulls, Schemata, Partitionen, Idempotenz |
| Leistung JVM | JMH oder reproduzierbares Zielbenchmark |
| Architektur | Scalafix / fitness functions auf bytecode oder Quellen |
| Sicherheit | SAST tatsächlich Scala, SCA, Geheimnis Scanning und Zulassungstests |

**CodeQL Java/Kotlin beweist keine Abdeckung Scala** : Prüft die Liste der unterstützten Sprachen und prüft den gewählten Analysator auf bekannten Fehlern.


<!-- section: s-20 -->
### Nachweiswert der durchgeführten Tests

Ein Test, der von demselben Agenten geschrieben wurde wie die Implementierung, ist kein unabhängiges Orakel. Neuere Arbeiten zeigen, dass die Agenten häufig Beobachtungs- oder Drucktests ohne diskriminierende Behauptungen durchführen; eine Erhöhung der Anzahl der Tests durch die Schnelle reicht nicht aus, um die Auflösungsrate zu verbessern. Andere Mutationsbewertungen zeigen, dass die durch die Agenten verursachten realistischen Fehler durch grüne Folgen nicht erkannt werden und dass ihre Wirksamkeit verschlechtert wird, wenn sich der Code auch ohne erwartete semantische Veränderungen entwickelt.

Für einen Bugfix behalten Sie daher den kostengünstigsten Beweis:

```text
1. einen minimalen Reproduktionstest ergänzen;
2. prüfen, dass er auf dem Basis-Commit aus dem richtigen Grund fehlschlägt;
3. den Patch anwenden;
4. prüfen, dass sowohl dieser Test als auch die passende Testsuite bestehen;
5. das Testorakel variieren: Eigenschaften, Grenzfälle, metamorphische Tests oder gezielte Mutanten;
6. in kritischen Fachbereichen den Test vor der Implementierung prüfen lassen.
```

Legt nicht eine universelle Mutationsschwelle fest, die dazu anregt, die metrischen Werte zu spielen. Vergleicht die Punktzahl auf dem betroffenen Perimeter, erfordert eine Rechtfertigung für jeden großen Überlebenden und folgt vor allem dem **delta der Mutation Score[**, den verlorenen Regressionen und den Returns von Reviews. Ein Test, der vor dem Patch nicht fehlschlagen konnte, beweist nicht den Patch.

**Der Härteschritt (Mutation Testing):** Sobald die KI die Tests geschrieben hat und sie grün sind, bestätigt ihre Robustheit mit Stryker4s:

```plaintext
sbt "project api" stryker
```

Niedrige Punktzahl **kann** nicht nur unzureichende Tests, sondern auch gleichwertige Mutanten, die nicht relevant oder nicht zielgerichtet sind, aufdecken. Untersucht zunächst die überlebenden Mutanten, ihre beruflichen Auswirkungen und Ausschlüsse; fügt keine künstlichen Aussagen hinzu, um die Punktzahl zu erhöhen. Wenn ein wichtiger Mutant lebendig bleibt, gibt den Bericht an den Agenten zurück, indem er um einen **beobachtbare Patch-unabhängige Verhaltensprüfung**, dann startet die gezielten Tests.

---

<!-- section: s-21 -->
#### Schritt 5: Erzwingen Sie die Überprüfung vor der Ergänzungserklärung

Agenten LLM melden häufig "Gut" ohne Überprüfung. Fügt diese systematische Anweisung am Ende jedes Implementation-Schrittes hinzu:

Bevor du diese Aufgabe beendest, musst du:

1. Kompilierbefehl ausführen und das Ergebnis anzeigen
2. Zieltest ausführen und das Ergebnis anzeigen
3. Prüfen Sie den Diff aus der genehmigten Datenbank, die kommittierten und unkommittierten Änderungen und die nicht verfolgten Dateien
4. Liste der geänderten Dateien mit dem Grund für jede Änderung
5. Wenn ein Schritt fehlschlägt, korrigieren Sie und wiederholen Sie es seit 1 Sag "Gib" nur, wenn die 5 Punkte oben sind zufrieden.

Um diese Überprüfungen zu automatisieren, verwenden Sie die gemeinsamen Skripte im Abschnitt 5 (hooks) und [CI] im Abschnitt 15A. Der Hook `PostToolUse` kompiliert nur: `Test/compile` führt die Tests nicht aus. Die Ergebnisse der Suiten und der komplette Diff müssen mit dem SHA-Kandidat verknüpft sein, und die CI muss die Validierung unabhängig von der PHP-Funktion wiederholen. Ein Stop-Hook ist kein Komplementierungsnachweis; es darf keine Sperrung verhindern.

Variante für kritische Aufgaben (Sicherheit, Geld, öffentlicher Auftrag):

Vor der Erklärung dieser Aufgabe abgeschlossen, ausgeführt und zeigt:

1. sbt kompiliert (Null-Fehler, Null-Warning-Neu)
2. sbt "TestOnly *SpecCiblé" (alle grün)
3. sbt scalafmtCheckAll (konforme Formatierung)
4. Diff base → Kandidaten und Status Git vollständig (nur die Dateien auf der Karte)
5. Prüft, ob das Diff NICHT enthält: TODO, FIXME, println de debug, nicht verwendeter Import, nicht angeforderter öffentlicher Signaturwechsel Zeigt das Ergebnis jedes Schritts an. Wenn ein Schritt fehlschlägt, korrigiert und erneut gestartet wird. Sag nicht "Geschenk" bevor die 5 Schritte grün sind.

---

<!-- section: s-22 -->
## Schritt 6: Self-review durch den writer

Prognose:

```text
Prüfe deinen eigenen Diff, bevor du ihn an den unabhängigen Reviewer weitergibst.
Liste auf:
- fachliche Risiken
- Grenzfälle
- fehlende Tests
- unnötige Änderungen
- manuell zu prüfende Dateien
- Annahmen, die du getroffen hast
```

Dieser Schritt entfernt häufig offensichtliche Fehler vor externer Review. **Sie ist niemals eine Anerkennung wert.** : Der Agent, der den Diff geschrieben hat, teilt die gleichen Annahmen wie seine Implementierung und kann nicht das endgültige Gate bilden. Der Writer kann reinigen; ein frischer Kontext **andere Modellfamilie** muss seine unabhängigen Feststellungen vorlegen.

---

<!-- section: s-23 -->
## Schritt 7: unabhängige Bewertung durch die andere Modellfamilie

Prompt reviewer: **[Opus 5.5 Medium** wenn Codex geschrieben hat; **GPT‑6.2 Sol Medium[**, wenn Claude schrieb. Steigen Sie nach High für eine riskante PR und zu Astra Light/Fable Low nur , wenn die zusätzliche Kapazität gerechtfertigt ist:

```text
Arbeite als unabhängiger Senior-Reviewer für Scala/JVM-Code.

Prüfe exakt den Head-SHA des PRs anhand seines Merge-Base-Commits, der genehmigten Spezifikation, der Akzeptanzkriterien und AGENTS.md.
Arbeite in einer neuen, rein lesenden Sitzung und ändere die Implementierung nicht. Ziehe die Überlegungen des implementierenden Agenten
erst heran, nachdem du dir ein eigenes Urteil gebildet hast.

Priorisiere funktionale Korrektheit, Erhalt der Invarianten, Regressionen, Kompatibilität, Qualität der Testorakel,
Fehlerbehandlung, Ressourcensicherheit, Nebenläufigkeit, Performance, Sicherheit und Verstöße gegen den vereinbarten Umfang.

Nenne für jeden relevanten Befund Schweregrad, Datei und Zeile, geprüften SHA, verletzte Anforderung oder Invariante,
ein konkretes Fehlerszenario oder einen reproduzierbaren Fall, die kleinste plausible Korrektur und verbleibende Unsicherheiten.
Unterscheide nachgewiesene Fehler von Hypothesen. Ignoriere Stilpräferenzen und sachfremdes Refactoring.
Erfinde keine Befunde. Gib nur ein kurzes Urteil und nachgewiesene Befunde zurück.
Genehmige oder merge den PR niemals selbst.
```

Variante mit maschinen-bedienbarem Schweregrad-Klassifizierung bevorzugt für Sortieren und Gate, das nur durch unabhängige validierte Findings betrieben wird (siehe Beispiel für die typisierte Dekodierung in Abschnitt 12):

```text
Ordne jeder Rückmeldung genau eines dieser Labels zu:
- BLOCKING        : fachlicher Fehler, Datenverlust, Sicherheitslücke oder gebrochener öffentlicher Vertrag
- REGRESSION_RISK : möglicherweise verändertes bestehendes Verhalten oder ungetesteter Grenzfall
- STYLE           : Lesbarkeit, Konvention oder Benennung — niemals blockierend
- OUT_OF_SCOPE    : sinnvolle Verbesserung außerhalb des Tickets — in diesem PR ignorieren

Gib ausschließlich gültiges JSON zurück:
{
  "findings": [ { "severity": "...", "file": "...", "message": "..." } ],
  "summary": "..."
}
```

Die zugehörige Gate-Regel: `BLOCKING` und `REGRESSION_RISK` müssen vor merge behandelt oder ausdrücklich angefochten werden; `STYLE` ist optional; `OUT_OF_SCOPE` Geh in den Backlog, nie in den aktuellen Diff.

Diese Labels bleiben ** reviewhypothesen**, keine Fakten. Jede blockierte Rückkehr muss einen nachprüfbaren Nachweis erbringen: Datei und Zeile, Vertrag verletzt, Reproduktion, Test fehlschlägt oder genaue statische Regel. Ohne Beweise geht es in die menschliche Sortierung; das Auto-Etiketten eines Modells darf niemals allein ein Merge blockieren. Diese Validierung verhindert die teuren falschen Positiven und die Schleifen, die Autor IA ↔, IA Neufassungen, die ohne neue Informationen Credits verbrennen.

Die empfohlene Pattern bleibt: **ein writer, ein revier der anderen Familie**. Die Kreuzbewertung ist eine Arbeitshypothese, keine Garantie: eine Studie *Cross-Model LLM Review-Code* über 116 Algorithmische Probleme mit Opus 4.7 / GPT-5.5 beobachtet einen Gewinn Codex → Claude (71,6 → 89,7 % Erfolg) und ein Rückgang Claude → Codex (91,4 → 82,8 %, wenn der Reviewer das Programm neu schreibt, ohne die Tests durchzuführen. Scala. Der reviewer erkennt und rechtfertigt ; der writer korrigiert nach Sortierung. Messen Sie die realen/falschen positiven Fehler, fehlende Fehler und Regressionen, die durch die Korrekturen eingeführt werden. Nach einer geringfügigen Korrektur, gezielte Neuinterview der Änderungen und Invariants; review vollständig nur, wenn das Risiko oder der Wurf geändert hat.

> **Aufwand und Grenzen der Bewertung.** Über 90 Django-Pflaster, eine Studie *How Much Effort Does an AI Code Reviewer
> Need?* findet Opus 5.5 Medium nicht weniger als High innerhalb einer vorgegebenen Marge von 15 Punkten, für mittlere Kosten
> 20 % unterlegen. Auch High akzeptiert 45 % der Patches, die durch das verstärkte Orakel als falsch eingestuft werden; einige
> Etiketten bleiben fragwürdig. CR-[Bench-v2 (584 revidierbare Fehler im Zusammenhang mit PRs) bestätigt, dass die Abdeckung
> Diese Ergebnisse unterstützen Medium für den Alltag, aber nicht beweisen, dass
> die universelle Gleichwertigkeit Medium/High und die Wirksamkeit der aktuellen Modelle auf Scala. Kein eigenständiges Gate [LLM.

 Standard: **Sol 6.2 Schriftliches Medium → Opus 5.5 Medium review**oder **Opus 5.5 Medium/High schreibt → Sol 6.2 Medium review**. Luna/Haiku dienen mechanischen Aufgaben; Astra/Fable wird nur beim Klettern mobilisiert. `Ultra` bleibt den entkoppelbaren Missionen in unabhängigen Achsen vorbehalten.

---

<!-- section: s-24 -->
## Schritt 8: gezielte Korrektur

Du bittest nie den Reviewer, alle seine Vorschläge automatisch anzuwenden. Du wählst die nützlichen Rückmeldungen aus und stellst dann den ursprünglichen **writer**:

```text
Diese Review-Befunde bestätige ich:
[Liste]

Korrigiere nur diese Punkte.
Ignoriere optionale Vorschläge.
Halte den Diff klein.
Führe die gezielten Tests erneut aus.
```

**Stippt die Revision, wenn die Kriterien grün sind.** Ein Korrekturpass nach der Review ist der Fehler; ein zweiter ist nur durch einen neuen und fundierten Finding `BLOCKING` / `REGRESSION_RISK`, einen roten Test oder einen deterministischen Beweis gerechtfertigt. Verwenden Sie keinen schnellen Iterium-Typ noch, bis es perfekt ist: Über den besten Checkpoint hinaus erfindet der Agent häufig Änderungen, um die Nachfrage zu befriedigen, und kann das Diff verschlechtern.

Wenn ein neuer Pass benötigt wird, vergleicht man den neuen Diff systematisch mit dem vorherigen Checkpoint und behält die am besten zufriedene Version **spec + test + scope**, nicht die neueste Version.

Wenn Sie die Korrektur nach der PR auf Codex (Goal mode, Heartbeat oder Cloud), [`/steward` oder PR Steward (Abschnitt 12) übertragen, übertragen Sie ausdrücklich die ownership des Zweiges, zusammen mit dem Start-SHA, der Spect und den einzigen zulässigen Rückgaben. Stoppen Sie die Überwachung vor der Übernahme durch den ursprünglichen Writer. Jede neue Commit startet die entsprechenden Validierungen; die unabhängige Review muss sich auf den letzten Diff, nicht auf den SHA vor der automatischen Korrektur beziehen.

<!-- section: s-25 -->
## Schritt 9: Anti-Drive-Schutz-Agent

Fügt explizite Abschaltungsregeln hinzu. Sie reduzieren unnötige Unterschiede, Korrekturschleifen und verbrannte Gutschriften:

```text
Sofort stoppen, wenn:
- der Agent ohne Erklärung eine nicht im Plan enthaltene Datei ändert;
- der Agent build.sbt, plugins.sbt, resolvers oder Versionen ohne ausdrückliche Genehmigung ändert;
- derselbe Kompilierungsfehler 2 Mal auftritt;
- die gezielten Tests 2 Mal aus unterschiedlichen Gründen fehlschlagen;
- der Diff größer wird als angekündigt;
- die Korrektur beginnt, die Architektur zu verändern, anstatt das Ticket zu lösen.
- der Agent eine destruktive Änderung, einen Push, ein Deployment, externe Freigaben oder einen Vorgang mit Secrets versucht,
  für den keine ausdrückliche Autorisierung vorliegt.
```

In diesem Fall nicht wieder aufrufen   ✓fix it ✓. Anfrage eher:

```text
Stopp. Fasse den genauen Stand zusammen:
- geänderte Dateien
- getroffene Annahmen
- aktueller Fehler
- ausgeführte Befehle
- kleinster vorgeschlagener nächster Schritt
Ändere nichts.
```

> **Die Hand wieder aufnehmen, ohne zweimal die gleiche Exploration zu bezahlen.** Drei Mechanismen Claude Code zu kennen:
>
> - **Checkpoints**: Jede Schnellmeldung erstellt einen Checkpoint (snapshot der Dateien vor jeder Bearbeitung durch die Tools von
>   Claude). `Échap Échap` oder `/rewind` Wiederherstellt das Gespräch, den Code oder beide an einem früheren Punkt, einschließlich
>   nach dem Schließen des Terminals . Bekannte Grenze: Nur Änderungen über Claudes Bearbeitungswerkzeuge
>   folgen, nicht diejenigen, die in Bash gestartet werden, ein Checkpoint ersetzt weder ein Commit noch das Worktree.
> - **`/compact` wäscht nicht eine falsche Hypothese** : die Kompaktheit fasst das Gespräch zusammen und *Stärke* Daher
>   Wenn der Agent zweimal zur gleichen falschen Spur zurückkehrt, ist die Parade
>   `/clear` und dann ein schnelles gedrückt mit dem neuen Zustand ✓ nicht eine zusätzliche Kompression.
> - **Permissions en deny-by-default**: `settings.json` akzeptiert allow / ask / deny-Regeln; kombiniert eine allowlist
>   eng mit expliziten Denys (Netzwerk, kritische Dateien, Push) anstatt von Hand in Schleife zu genehmigen.
>   Dies ist die Produktversion der Regeln für die Nichtautomatisierung des Abschnitts 3.
> - **Auto-Standardmodus** : seit 14 August 2026, ist der Auto-Modus der Standard-Ausnahmemodus für neue
>   - Das ist nicht nur ein Gate, sondern auch ein Gate.
>   Beruf: Prüfe, dass deine Regeln `deny` über `build.sbt`, Migration, Workflows CI und Push weiterhin aktiv bleiben (die
>   *hard deny rules* des Auto-Modus blockieren, ohne die Ausnahmen `allow` zu berücksichtigen, und behalten die unten stehenden Hooks.

<!-- section: s-26 -->
#### Claude Mods: Wenn die klassischen Hooks überschritten werden

Seit **Claude Code 2.1.287**, un **Mod** ist ein Plugin, dessen JavaScript/TypeScript-Handler im Prozess ausführen Claude Code. Ein Handler kann **Beobachten, neu schreiben oder unterstützen** ein Ereignis: tool call, schnell, Runde, Steuerung oder Wiedergabe der Schnittstelle. Es ist eine andere Schicht von MCP : un MCP liefert Tools aus einem externen Prozess/Dienst; ein Mod kann das Verhalten des Harness selbst ändern. **3 Oktober 2026**, die Version 2.1.288 bereits hinzugefügt `$.ui.selection()` und mehrere Mods/Plugins-Patches: behandelt diese API als **jung und skalierbar**, und stecke die Version Claude Code für jede Mod, die in deinem Workflow kritisch wird.

| Bedarf                                                                                                 | Primitiv zu bevorzugen |
|--------------------------------------------------------------------------------------------------------|----------------------|
| Wiederholen von Anweisungen / Methoden                                                                 | **Skill**            |
| Zugang zu einem externen System oder Werkzeug                                                        | **MCP**              |
| Ein Ereignis mit einer einfachen Regel sperren, zulassen oder beherbergen                                        | **Settings hook**    |
| Interaktives IUI, Ereignisfreigabe, lokale Steuerung, Abfangen/Neuschreiben eines Ereignisses | **Mod**              |

Die Mods API können u. a. Befehle, Tools und Subagents speichern, Vorlagen anrufen, den Status und die Benutzung der Sitzung lesen, einen freigegebenen Store beibehalten, Dateien lesen/schreiben, einen Prozess starten, HTTP oder ein MCP anrufen und mit anderen Sitzungen kommunizieren. Die Mods funktionieren mit ihren Hooks im Terminal ✓ einschließlich des integrierten Terminals und des Plugin JetBrains .] sowie im Tab Code von Claude Desktop; die Elemente von Claude Desktop werden nicht auf allen headless/cloud Oberflächen zurückgegeben.

**Ersetzt die drei folgenden Hooks nicht durch eine Mod nur, weil es möglich ist.[** Für einfache und deterministische Gates (`build.sbt`, Migration, diff max, obligatorische Tests) bleibt ein Hook-Setting kleiner, lesbarer und leichter zu prüfen. Benutze nur eine Mod, wenn du einen Cross-event-Status, eine UI, einen interaktiven Workflow oder eine Überwachung brauchst, die im klassischen Hook falsch ausdrückt.

> **Größeres Vertrauen.** Ein Mod settlement, das mit den Rechten deines Benutzers ausgeführt wird, kann die
> Schnell, Tool calls, Umgebungsvariablen und settings, Prozesse starten oder Netzwerk, eine neue schreiben
> Abfrage und Ausgabe von Quoten über Standardanrufe. Die Prozesse, die er startet, sind **aus der Bash-Sandbox[** von
> Claude.
> Eine installierte Mod kann auch bestimmte tool calls genehmigen, die eine `ask` oder [`PreToolUse` Benutzerregel hätte.
> - Ich bin nicht mehr da.
> Claude-Lizenzen sind also keine Sandbox um den Plugin-Code.

Vor der Installation oder Förderung eines Mods Dritter:

```text
1. Quelle des Marketplaces überprüfen und Version oder Commit möglichst festschreiben.
2. .claude-plugin/plugin.json, hooks/hooks.json, das Modul register.*, bin/ und gegebenenfalls .mcp.json lesen.
3. claude plugin validate ./mon-mod
   → insbesondere die Zeilen hooks: und calls: prüfen, ohne den Mod auszuführen.
4. claude --plugin-dir ./mon-mod plugin details <nom>
   → die tatsächlich vorhandenen Komponenten prüfen.
5. claude plugin test ./mon-mod
   → deterministische Hook-Tests ohne Sitzung, Login oder Netzwerk.
6. Wenn das Plug-in Evaluierungen hat: claude plugin eval ... vor der Freigabe.
7. Erster Versuch mit --plugin-dir in einem temporären Worktree; --safe-mode als Rückfalloption.
```

Für eine Organisation muss eine echte Kontrolle in [**managed settings** (`allowManagedModsOnly`, Reihenfolge der verwalteten Plugins, [`disableAllHooks` nach der Politik) und in der integrierten Mod `cc-plugin-sec-default` leben, nicht im guten Willen eines Benutzers. Für deine Solo-Nutzung ist die entsprechende Regel einfach: **built-ins / persönlicher Code geprüft > Opakes Gemeinschaftsplugin**, und keine automatische Aktualisierung eines sensiblen Mods, ohne das Diff der Version zu lesen.

<!-- section: s-27 -->
#### Gemeinsame Konfiguration von Hooks Claude Code / Codex

Trennen **Lokale Rückmeldungen** und **Validierungsgate**. Ein Hook auf einem Befehl `Edit` sieht nicht unbedingt die Bash-Schriften, MCP oder IDE ; es kann die Einschließung nicht garantieren. Löscht `ai-guard.sh` basierend auf der Suche nach Ketten in einem Befehl: Dynamische Pfade, Symlinks und indirekte Ausführungen werden nicht von diesem Filter erfasst. 12 ; kontrolliert die tatsächlich veränderten Pfade im letzten Diff. Hooks sind kein Ersatz für die CI unabhängig.

Beispiele für ein Vertrauensprojekt `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Und `.codex/hooks.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "apply_patch",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Die beiden Harness nennen die gleichen Skripte (die spezifischen Ereignisse und paylads der Werkzeuge bleiben getrennt). Codex erfordert, die Definitionen von nicht verwalteten Hooks zu lesen und zu genehmigen ([`/hooks`; deaktiviert diese Kontrolle nicht. Ein Worktree kann die Hooks des Hauptcheckouts laden; prüft die tatsächlich ausgeführten Quellen. Die Hooks und Skripte des Vertrauens müssen vom Agenten vor dem Schreiben geschützt werden; in der Umgebung, in der sie verwaltet werden, stellt sie außerhalb des Worktree ein.

Skript `scripts/ai-compile-check.sh` (nur Kompilationsfeedback; kann bei zu häufigem Ausfall deaktiviert werden):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
logFile=$(mktemp)
trap 'rm -f "$logFile"' EXIT
# Capture the process exit code, not a pattern in the logs.
if sbt --client "Test/compile" >"$logFile" 2>&1; then
  exit 0
else
  exitCode=$?
  printf 'sbt Test/compile failed (exit %s)\n' "$exitCode" >&2
  tail -n 40 "$logFile" >&2
  exit 2
fi
```

Das Ergebnis basiert auf dem Rückgabecode von sbt, auch ohne Zeile `[error]`. `Test/compile` kompiliert die Tests, führt sie aber nicht aus. `grep` oder eine Bestellung RTK als Schiedsrichter für Erfolg ; behält den Rückgabecode des ursprünglichen Befehls. In Anwesenheit mehrerer Sitzungen, nicht starten konkurrierende Kompilationen auf dem gleichen Server sbt.

Skript `scripts/ai-stop-audit.sh` (nicht-blockierendes, für die beiden Harnesen gemeinsames Rufzeichen):

```bash
#!/usr/bin/env bash
set -euo pipefail
# No transcript heuristics and no forced retry on legitimate blockers.
cat >/dev/null
printf '%s\n' '{"systemMessage":"Completion requires a fresh validation receipt for the exact candidate SHA and independent CI; report blockers without claiming done."}'
```

Das Stop Hook sucht nie nach einem Befehl in der Transkription: eine Erwähnung von `testOnly` Erweist den Bediensteten nicht, weiterzumachen, wenn ein Invariant oder ein Haushalt ein Urteil erfordert. `scripts/ai-validate.py` (Abschnitt 11) und Check-in CI Die lokalen Beweise, die unter der Identität des Bediensteten vorgelegt werden, sind für die Diagnose nützlich, aber fälschlich: die Politik der CI, ihre Skripte und Ergebnisse müssen innerhalb einer vom Agenten unabhängigen Grenze leben.

Ein bevorzugter Mod Claude oder ein unzuverlässiger Hook kann die Pipeline verändern; hält externe Einschränkungen und verwaltete Kontrollen. Das endgültige Gate kann nicht geändert und vom Writer selbst genehmigt werden. Hooks können ignoriert oder nicht je nach Oberfläche ausgelöst werden; überprüft die tatsächlichen Ereignisse, Pfade und Berechtigungen vor der Annahme.

<!-- section: s-28 -->
#### Wiederherstellungsprotokoll, wenn der Agent Schleife

Eine Agentenschleife (gleicher Fehler, gleiche Korrektur, gleiches Versagen) ist ein von einem einfachen Versagen getrennter Ausfallmodus. Das Modellklettern behebt sie nicht. Hier ist das Protokoll in 4 Schritten:

**Schritt R1 - Stoppen und Auslesen (0 (Zusätzliches Token)**

Stoppt den Agenten sofort. Erhöhe nicht "fix it."

Stop. Ändern Sie nichts mehr. Zusammenfassung zu 5 Punkten:

1. Bisher geänderte Dateien (diff von der genehmigten Datenbank + git status)
2. Aktuelle Hypothese zur Ursache
3. Was versucht wurde und warum es versagte
4. Die nächste Mindestaktion, die du vorschlagen würdest.
5. Was du nicht sicher bist

**Schritt R2 Humane Diagnostic mit IDE (5-10 min)**

Verwende IntelliJ, um zu überprüfen, was der Agent nicht sehen kann:

- Der tatsächliche Typ eines Ausdrucks (Strg+Shift+P / Typ info)
- Tatsächliche Auflösung eines impliziten/given (Strg+B zur Vereinfachung)
- Die erwartete Typhierarchie vs.
- Breakpoint debugger über unerwartetes Verhalten

Das Ziel ist es, die strukturellen Informationen zu finden, die der Agent fehlt.

**Schritt R3 ✓ Frische Sitzung mit engem Kontext**

/clear Neue schnelle mit NUR:

- Ziel (1 Satz)
- Die genaue Datei oder Methode
- Der genaue Fehler (aus der IDE, nicht aus der Transkription kopiert)
- Strukturelle Informationen in R2
- "Bringt nur eine minimale Änderung vor. Compile und testet."

**Schritt R4 Wenn R nicht erfolgreich ist3Modellklettern**

Erst jetzt ist die Eskalation Sonnet → Opus → Fable gerechtfertigt, da der Kontext sauber ist und das Problem gut gestellt ist.

Absolute Anti-Patern: Das gleiche Modell wieder in den gleichen Kontext in der Hoffnung auf ein anderes Ergebnis. Es ist die Definition der Schleife.

> **Periodische Wiederverankerung, die Parade, die gegen die lange Drift gemessen wird.**
> Die Untersuchung 2026 auf dem Agenten drift ✓ (Verhaltensminderung, gemessen auf langen Bahnen und
> Multiagentensysteme) konvergiert über drei Mischfamilien: episodesale Konsolidierung der Geschichte in
> Strukturierte Zusammenfassungen, adaptive Verhaltensverankerung (regelmäßige Wiederholung der Charta und des Ziels
> ) und Routing unter Berücksichtigung der Drift. Sofortige Übersetzung für Ihre Sitzungen:
> - ** verwirft die Charta[** (Ziel, Nichtziel, Invariants, Done-Definition) auf jeden Meilenstein und die Rückkehr von
>   subagent     ✓ nicht nur beim ersten Schritt : eine Belastung , die nicht mehr im letzten Fenster vorhanden ist ;
> - **Verallgemeinert die Statusdatei** (`MIGRATION_STATE.md`) auf jeder langen Tagung, nicht nur auf Missionen
>   Fable: Der Anker überlebt die Kompositionen und die Wiederholungen;
> - **Breaker-Schalter mit doppeltem Schwellenwert**: ein Hinweis auf die Wiederholung eines gleichen Tool-Calls oder eines gleichen
>   Fehler, dann ein harter Halt auf der zweiten identischen Wiederholung  ✓ anstatt einer einzigen brutalen Schwelle;
> - **Frische Sitzung im Falle einer Schleife** : Modell Klettern korrigiert keine Schleife (Abschnitt 3) ; `/clear` +
>   Zustand + Charter glatt, ja.

---

