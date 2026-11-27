<!-- section: chapter -->
# 1A. Vibe Coding, KI-gestütztes Programmieren und agentenbasiertes Programmieren

Der Begriff **Vibe Coding**, den Andrej Karpathy im Februar 2025 bekannt machte, bezeichnete ursprünglich eine Praxis, bei der Entwickler fast die gesamte Codeerstellung delegieren, die Vorschläge des Modells übernehmen und ihre Arbeit vor allem am beobachtbaren Ergebnis messen. Der Ansatz eignet sich für kurzlebige Prototypen, Experimente oder unkritische Benutzeroberflächen. Als Produktionsmethode reicht er für Fachanwendungen, Finanzsysteme, sicherheitskritische oder langlebige Systeme nicht aus.

Zwei Hinweise zur Herkunft des Begriffs klären die Debatte im Jahr 2026. Karpathy erklärte, der Tweet sei halb als Scherz gemeint gewesen und habe sich auf kurzlebige Wochenendprojekte bezogen. Er hat Vibe Coding nie als Produktionsmethode vorgeschlagen. Schon im Februar 2025 zog Simon Willison eine klare Grenze. Diffs ungelesen zu übernehmen ist Vibe Coding. Jede Zeile zu prüfen und zu verstehen ist KI-gestütztes Programmieren. Das Problem entsteht, wenn die Prüfung ausbleibt. Ende 2025 kam **Vibe Engineering** hinzu. Der Begriff bezeichnet erfahrene Fachleute, die mit LLM-Agenten erheblich schneller arbeiten und die volle Verantwortung für die Software behalten. Prüfung, Tests und Verantwortung unterscheiden die beiden Praktiken und stehen in diesem Leitfaden im Mittelpunkt.

Es sind drei Arbeitsformen zu unterscheiden:

| Modus                        | Kontrolle durch den Menschen                                                     | Geeignete Anwendung                                     | Primärrisiko                                           |
|-----------------------------|---------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------|
| **Vibe coding**             | Gering, Validierung durch Empfindung und Ausführung                       | Prototyp, Spike, persönliches Einwegwerkzeug        | Unsichtbare Schulden, Sicherheit, verlorenes Verständnis            |
| **AI-assisted engineering** | Der Entwickler entwirft und relinkt, das Modell beschleunigt                 | Tägliche Arbeit am Code beibehalten              | Automatisierung menschlicher Entscheidungen    |
| **Agentic coding**          | Der Agent erforscht, plant, ändert und testet in einem begrenzten Bereich | Aufgaben, die mit Tests und Erlaubnissen genau festgelegt sind | Drücke, Schleife, Aktion außerhalb des Umkreises, indirekte Injektion |

Für einen Senioren Scala, ist das Ziel also nicht mehr als vibe coding, sondern eine **kontrolliertes agentielles Engineering ** :

```text
Überprüfbare Spezifikation
→ möglichst kleiner, aber ausreichender Kontext
→ Plan
→ angemessene Berechtigungen
→ instrumentierte Ausführung
→ Kompilierung und deterministische Tests
→ unabhängiges Review
→ menschliche Validierung
```

**Evidence-driven agentic engineering** : le SDD der Vertrag fest, das Harness engineering macht seine Einschränkungen ausführbar, und die Beweise bestimmen, ob die Änderung vorankommen kann. Für jede Anforderung, verbindet einen unabhängigen Nachweis (Verhaltenstest, Inspektion, Benchmark oder Runtime-Messung), den tatsächlich validierten SHA und die nicht gedeckten Risiken. Eine Aussage des Agenten, eine Bewertung ohne Beweise oder einen einfachen grünen Status bilden kein Orakel. Der Zyklus endet nach Validierung des eingesetzten Artefakts, nicht nur auf dem merge (Abschnitt 15B).

<!-- section: s-1 -->
## Was der Stand der Kunst in 2026 zeigt

1. **Das Modell allein bestimmt den Erfolg nicht.** Das Harness, die verfügbaren Werkzeuge, das Debugger, die Kontextqualität und die Tests können die Ergebnisse fast so stark verändern wie die Wahl des Modells. Vergleichen zwischen den von Lieferanten veröffentlichten Scores sind nur gültig, wenn die Harnes, die Anstrengung, die Werkzeuge und das Protokoll vergleichbar sind.
2. **Kurze Benchmarks überschätzen die lange Autonomie.** Agenten erzielen gute Ergebnisse bei isolierten Ausgaben, aber sie fallen stark auf die multi-Datei-Entwicklungen, lange und historische. SWE-EVO zum Beispiel zielt auf viel längere Aufgaben als SWE-bench ab und hebt diese Lücke hervor.
3. **SWE-bench Verified ist nicht mehr ein guter einzelner Standard.** OpenAI dokumentierte Probleme mit Verunreinigungen und fehlerhaften Tests. Für den Code bevorzugt ein Portfolio, das geprüfte SWE-bench-Aufgaben, Terminal[Bench, Review-Aufgaben und vor allem ein nichtöffentliches internes Benchmark Scala enthält.
4. **Die Produktivität des Menschen wird nicht durch eine gute Agenten-Score garantiert.** Eine randomisierte Studie von METR an Entwicklern, die in ihren eigenen Ablagerungen erfahren waren, beobachtete eine Verlangsamung mit den Start-Tools 2025. Die Daten, die dann gesammelt wurden, deuten auf eine mögliche Verbesserung hin, doch MER hält den neuen Test aufgrund von Auswahlfehlern und schwierigen Messungen mit mehreren konkurrierenden Agenten für unzuverlässig. 2026Die lokale Messung der Zeit bis zum Meer ist nach wie vor unverzichtbar. 2026 : Punktuelle Schätzung von etwa 18 % Beschleunigung auf der historischen Subkohorte (Konfidenzintervall −38 % à +9 % und etwa 4 % der neuen Teilnehmer (CI
   −15 % à +9 % • ein Signal, das zu laut ist, um zu schlussfolgern, das MER bevorzugte, indem es das Protokoll umformulierte, anstatt eine einzelne Zahl zu veröffentlichen. ~20 % schneller dank der KI, während sie ~19 % langsamer als die Differenz zwischen Wahrnehmung und Messung ist der Grund, warum dieser Leitfaden lokale metrische Werte (Kosten pro akzeptierter Änderung, Zeit bis zum Merge) anstatt das Gefühl der Sitzungen erfordert.
5. **Einreichungsanweisungen sind nur dann nützlich, wenn sie einsatzfähig sind.** Suchen auf `AGENTS.md` finden einen Nutzen, wenn die Datei Befehle, nicht-standardmäßige Konventionen, Invarianten und Abschaltungsregeln enthält. Eine lange generische Beschreibung der Architektur kann den Kontext erhöhen, ohne das Ergebnis zu verbessern.
6. **Der Multiagent ist kein automatischer Intelligenz-Multiplikator.** Es hilft, wenn die Teilaufgaben wirklich unabhängig sind, die Verantwortlichkeiten und Dateien getrennt sind und ein Wurzel-Adjektor synthetisiert. Auf einem geteilten mutierbaren Zustand erhöht es Konflikte, Kosten und Koordinationsfehler.
7. **Ein technisch korrekter Patch reicht nicht aus, um einen Agenten zu bewerten.** Messen Sie auch die Einhaltung des Scopes, der Abschaltregeln und der Konventionen, die Qualität des Plans, die Fähigkeit, Unsicherheit und die Kosten der menschlichen Überprüfung zu melden. Zwei Agenten, die die gleichen Tests durchführen, können einen sehr unterschiedlichen Wert haben, wenn einer doppelt so viele rework oder Änderungen außerhalb des Umkreises erzeugt.
8. **Speicher, Skills und anhaltende Regeln werden zu einer Ingenieuroberfläche.** Agenten, die in der Lage sind, ihre eigenen Speicher, Skills oder Routing zu entwickeln, dürfen diese Änderungen niemals selbst fördern. Jede anhaltende Entwicklung muss vor Aktivierung entfernbar, versioniert, getestet, überprüft und reversibel sein.
9. **Ein großes Kontextfenster entfernt nicht das *Kontext rot*.** Evaluierungen 2026 unterscheiden die physische Kapazität des Fensters und die tatsächliche Qualität der Nutzung seines Inhalts: bei identischer Aufgabe können mehr Tokens Wiederherstellung, Einhaltung der Einschränkungen und Überlegungen lange vor der maximalen Grenze verschlechtern. Das richtige Ziel ist daher nicht zu erfüllen. 1M tokens, aber halten Sie eine **Mindest-Working-Set und Entscheidungsfindung**. Die isolierten Subagenten sind eine strukturelle Parade: sie verbrauchen lokal viele Kontexte und verweisen nur auf ein kondensiertes Ergebnis.

Fazit: Die Grenzebene erhöht die Oberfläche der möglichen Aufgaben, aber die Qualität des Engineerings um den Agenten bleibt der wichtigste kontrollierbare Faktor.

<!-- section: s-2 -->
### Methodologische Ergänzung

> **SWE-bench Pro ersetzt nicht allein SWE-bench Verified.** OpenAI Die Kommission hat in ihrer Mitteilung "Die Zukunft Europas - Eine Strategie für Wachstum und Beschäftigung" (Dok. 30 % der Aufgaben
> Auch SWE-bench Pro ist defekt: zu strenge Tests, versteckte Anforderungen fehlen aus dem Tempo, Abdeckung
> Unzureichende oder irreführende Anordnung. Prüfung vom 8 Juli 2026
> 27,4 % der [731 markierten öffentlichen Aufgaben; Anmerkung von fünf älteren Ingenieuren: 34,1 %
> hat OpenAI im Übrigen zu [**] ihre Empfehlung** ausdrücklich zurückziehen, sie zur Kodierungsbewertung von
> • ein stärkeres Signal als nur die Schätzung. Das richtige Bewertungsportfolio kombiniert daher mehrere Achsen
> anstatt ein neues
> Einzigartige Einstufung.

| Messachse                | Nützliche Bewertung                 | Was sie offenbart                                                                               |
|------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------|
| Standard-Einzahlungskorrigiert | SWE-bench, mit Prüfung der Aufgaben | Reparaturkapazität an isolierten Ausgängen                                                       |
| Original-Langaufgabe       | **DeepSWE**                      | Reduzierte Kontamination, geschriebene Prüfer, um mehrere gültige Lösungen zu akzeptieren           |
| Iterative Zusammenarbeit      | **SWE-Interact** oder SWE-Together | Absichtserklärungen entdecken, Einschränkungen speichern, menschliche Korrekturen benötigen            |
| Exploration des Depots         | **SWE-Explore**                  | Lokalisierung der Linien und Effizienz des Kontexts                                     |
| Vollständiger Zyklus                | **SWE-Cycle**                    | Wiederaufbau der Umwelt, Implementierung und Generierung von Tests in einem einzigen Pfad |
| Realität deiner Arbeit       | **Benchmark Scala privat**        | Kosten und Qualität auf Play, Pekko, Tapir, Spark, Implizite, Serialisation und Build          |

Für eine Code-Aufgabe wird der [**Kosten pro akzeptierter Änderung** , um die Lieferung zu steuern, der [**Kosten pro durchgeführter und stabiler Änderung[** (Abschnitt 15B) und nicht die Brutto-Erfolgsquote berechnet:

```text
Kosten pro akzeptierter Änderung
= Tokens + Latenz + menschliche Arbeitsminuten + CI + Nacharbeit + unentdeckte Fehler
```

Benutzt eine gemeinsame Einheit, um diese Kosten (z. B. Euro mit expliziten Stundenkosten) zu aggregieren, oder hält die einzelnen Komponenten getrennt. Tokens und Minuten werden nicht direkt addiert. Für Kosten bis zur Produktion, fügt Einführung, Validierung runtime, Rollback/hotfix und Fehler, die während eines vor der Messung festgelegten Fensters beobachtet werden. Zählt nur eine Änderung, die dieses Fenster beendet hat, als stabil.

Suche nicht nach einer globalen KI-Produktivität. Stratiert die Messungen mindestens durch **greenfield, Wartung, Legacy, Bugfix, Migration, Refactor und kritischer Code[**: Studien 2026 erzielen widersprüchliche Ergebnisse, gerade weil sie nicht immer die gleichen Aufgaben, Entwickler oder Bewertungskosten messen.

<!-- section: s-3 -->
### Ein grünes Benchmark ist noch kein messageables Diff

Eine Metr-Bewertung 296 PRs pro Agenten festgestellt, dass der Grader SWE-bench im Durchschnitt **24,2 Weitere Erfolgspunkte** Die Stichprobe bezieht sich nur auf drei Ablagerungen, Modelle vor der letzten Generation und einen einzigen Test ohne Iteration auf den Betreuer-Feedback: es ist keine grundlegende Grenze der Kapazität, aber es beeinträchtigt die naive Gleichwertigkeit `tests du benchmark passants = changement acceptable`.

Bei langen Aufgaben stellt SlopCodeBench außerdem eine Anhäufung von Vervielfachung, Verbigkeit und struktureller Erosion fest, wenn die Checkpoints sich verstricken. Ein schneller Qualitätsanspruch reduziert einige Mängel anfangs, ohne ihr Wachstum zu beseitigen. Das gute Beweissystem vereint daher vier unabhängige Barrieren:

```text
Expliziter Fachvertrag
→ Reproduktion, die vor dem Patch fehlschlägt
→ deterministische Tests, Eigenschaftstests und Mutation Testing
→ Review des Diffs, seines Umfangs und seiner Wartbarkeit durch einen verantwortlichen Menschen
```

Die Benchmark-Scores werden zum Routing und Experimentieren verwendet; sie dürfen nie zu einer Autorisierung der Autonomie oder des Merges werden.

> **Abstand zwischen Schreiben und Liefern.** Der Working Paper NBER *Writing Code vs. Shipping Code* observe, sur plus de
> 500 000 Entwickler GitHub, ein geschätzter Anstieg der Aktivität viel stärker für Commits als für
> Projekte und Releases. Die Studie bleibt Beobachtung mit Paarung: sie zeigt keinen Kausaleffekt
> Die WIP beschränkt sich also auf die Überprüfungs- und Lieferkapazität und misst bis zur Produktion.

<!-- section: s-4 -->
### Produktions-Wartung für Vibe coding

Die empirischen Studien von 2026 über tatsächlich verschlüsselte Anwendungen ✓ vibe finden wieder Familien von wiederkehrenden Mängeln: vorläufige Logik in der Produktion, ungefilterte Eingänge, ausgesetzte Geheimnisse, Vergessenheit der Belastungen durch die Türme und lokale Optimierung, die das Gesamtsystem verschlechtert. Ein stärkeres Modell oder eine bessere Geschwindigkeit reduziert diese Fehler, aber nicht beseitigt sie nicht.

> **Größenreihen gemessen in 2026.** Die Prüfung 200 Anwendungen tatsächlich kodiert und umgesetzt Ÿ b
> (1 471 Geprüfte Schwachstellen) findet mindestens eine Anfälligkeit in **90 % der Einlagen**, davon mehr als drei
> Viertel hoher oder kritischer Schweregrad; die gebrochene Zugriffskontrolle erscheint in 75,5 % der Einlagen, also etwa [20×
> die Basislinie OWASP 2025. Ein unabhängiger Scan von [1 400+ Anwendungen führt in der gleichen Größenordnung 65 %
> mindestens ein Sicherheitsproblem aufweisen, 58 % mindestens eine kritische Anfälligkeit, [400 + Geheimnisse ausgestellt).
> Die Analyse der Ursachen dieser Mängel rangiert in drei Familien ^ **Speicher** (vergessen zwischen den
> Umdrehungen), **Ziel** (lokale Optimierung, die das Gesamtsystem verschlechtert) und **Wissen** (Gefährliche Pattern)
> ) : genau die drei Mechanismen, die deterministische Gates und die menschliche Zeitschrift dieses Leitfadens
> Unterbrechung, da sie nicht dauerhaft korrigiert werden.

```text
Vibe-Coding-Prototyp
→ keine Produktionsdaten oder -schlüssel
→ funktionale Tests + Sicherheit + Performance + Wartbarkeit
→ menschliches Review des Diffs und der Abhängigkeiten
→ Übergang zu einem kontrollierten agentenbasierten Workflow
→ erst dann ausliefern
```

Eine vibe coding-Sitzung darf niemals direkt in die Produktion schieben, auch nicht wenn die Demonstration funktional erscheint. Die Produktionsgrenze ist ein **Ändern der Beweisregelung**, kein einfacher nächster Schritt der Katze.

