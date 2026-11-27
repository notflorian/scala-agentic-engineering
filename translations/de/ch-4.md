<!-- section: chapter -->
# 4. Realistisches Monatsbudget und Caching-Strategie

Das Budget sollte als ein Ingenieurbudget, nicht als abstrakte  ✓IA-Ausgaben gesteuert werden. Die richtige Metrik ist nicht die Kosten pro Nachricht, aber:

```text
coût total d'une tâche mergeable
= coût modèle + temps humain + temps CI + retours review + reprises de bugs
```

<!-- section: s-1 -->
## Realer Ausgangshaushalt

| Posten                                                 |                 Vorläufiger Haushaltsplan | Anmerkung                                                                                                                                                                                    |
|-------------------------------------------------------|---------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code via Claude Pro/Max                        |                      20 à 200+ $ | Max ist gerechtfertigt, wenn Opus/Sonnet jeden Tag umdrehen; die Quote wird auf die kompatiblen Claude-Oberflächen aufgeteilt.                                                                        |
| ChatGPT mit Codex                                    |                     20 $ und mehr | Mehr geeignet für den bornierten Einsatz; Pro ist gerechtfertigt, wenn Sol 6.2 ein tägliches Writer und nicht nur ein Reviewer wird.                                                                        |
| JetBrains AI Ultimate                                 | ~300 $/Jahr; 35 AI Credits / 30 j | Nützlich für Cloud-Funktionen JetBrains und Junie ; Completion / Next Edit Code Vorschläge und authentifizierte Agenten bei ihrem Lieferanten verbrauchen diese Credits nicht.                     |
| GitHub Copilot                                        |                         Variable | Optional: relevant vor allem wenn GitHub das Zentrum des Workflows issues/PR/review ist; weitgehend redundant als dritte Codechat.                                                      |
| OpenRouter / [API pünktlich GLM/Kimi/Gemini/Grok      |                         0 à 50 $ | Außergewöhnliches Ausgangstor, wenn Claude/Codex/[Qwen nicht ausreicht; freiwillig niedriges Budget und maximales Budget.                                                                         |
| GLM Coding Plan (Z.ai) — second abonnement optionnel  |                 ~18 à 160 $/Monat | Open-weight-Paket *Übereinstimmung* : Endpunkt Anthropic-kompatibel, passt in Claude Code um Review/Sortierung zu absorbieren, ohne deine Grenzen zu beginnen Claude. Lite ~18 $, Pro ~72 $, Max. ~160 $. |
| Qwen lokal                                            |             0 $ ohne Strom | Sehr gut für Voranalyse, Synthese und Boilerplate, aber nicht für die Entscheidung allein auf kritischen Code.                                                                                           |
| Sourcebot, Aider, OpenCode/Qwen Code, RTK             |                     0 mit Variable | Viele Werkzeuge sind Open Source, aber eventuell kosten Hosting, Indexe und Schlüssel API.                                                                                      |
| Headroom und neue Kontextkomprimierungswerkzeuge |                     Versuch | Vor der Integration in den Standardworkflow an nicht kritischen Logs/Diffs zu testen.                                                                                                         |

Realistisches Ziel für einen intensiven Soloeinsatz: **250 bis 450 $/Monat**, das nach zwei Wochen tatsächlicher Messung angepasst werden muss. Das ursprüngliche Budget von 300 bis 350 $ bleibt plausibel, aber es darf nicht eingefroren werden: Eine einzige schlechte Agentenschleife auf einem großen Kontext kann teurer als eine Woche gut gerostete Mikropatches kosten.

<!-- section: s-2 -->
## Preispunkte und Quoten, die im Leitfaden nicht festgelegt werden sollten

Claude Code ist in den kompatiblen kostenpflichtigen Claude-Plänen enthalten, aber die genaue Verwendung hängt vom Plan, dem Modell und den Sitzungsgrenzen ab. 20 $/Monat, Max ab 100 $/Monat, und Verwendung Max 5x/20x nach dem Angebot. Behalte also den Leitfaden in Form von Gabeln, nicht als permanente buchhalterische Wahrheit.

Seite Codex, vermeidet die Umwandlung von Vorlagennamen und Einstellungen ChatGPT in der Tat permanente Buchführung. **GPT‑6 Luna / GPT‑6.1 Terra / GPT‑6.2 Sol / GPT‑6.2 Astra**, mit Sol 6.2 Medium als Agentic-Fehler. Nutzungsgrenzen, Zugriff auf Max/Ultra und Rechnungsstellung hängen von der Ebene, der Oberfläche, der Region und dem Rollout ab. Schreibe die Regeln um die **Aufgabenklasse und Kosten durch akzeptierte Änderung**, und überprüft dann die offizielle Seite, bevor Sie ein Profil oder Budget industrialisieren.

Wichtiger Hinweis: **Anthropic Claude Free/Pro/Max/Team/Enterprise behält die Nutzung im Abonnement für native Anwendungen vor Anthropic und zu den in seinen Bedingungen vorgesehenen Zwecken.** Von Anfang an 2026, Anthropic hat ausdrücklich verboten die Verwendung von OAuth-Token in diesen Abonnements in Harnes von Drittanbietern oder inoffiziellen Werkzeugen: diese Ströme müssen über einen Schlüssel API gewidmet (Claude Console oder Cloud provider) und halten Sie sich an die Geschäftsbedingungen. Konkret: Claude Code und Claude.ai für die Abonnements Claude; OpenCode/Qwen Code/Aider für Qwen Lokal, Modelle API oder BYOK-Schlüssel, ohne jemals einen Claude Pro/Max-Session-Token in einem externen Tool zu verwenden.

Nicht mit dem zu verwechseln, was *ist* erlaubt: anschließen Claude Code über die **Endpunkt Anthropic-Z.ai-kompatibel** mit einer **Z.ai-Schlüssel** (GLM Coding Plan, §)3) ist erlaubt ✓ Du benutzt den Schlüssel eines Lieferanten gegen den Endpoint des gleichen Anbieters, Du wendest keinen Token OAuth Claude ab. Die rote Linie ist die **Wiederverwendung eines Claude-Abonnements token** aus Apps Anthropic, nicht die Tatsache zu zeigen Claude Code zu einem anderen Lieferanten mit seinem eigenen Schlüssel.

**Nach-PR-Haushalt Claude Ship.** Allein, `/ship`, `/steward` und Auto-fix Cloud verbrauchen die entsprechende Verwendung von Claude Code (keine separaten VM-Kosten für die Cloud Anthropic Nach der Dokumentation) ; eine Überwachung im Hintergrund ist nicht kostenlos. GitHub von Claude Ship (Team/Enterprise) verbraucht Gutschriften für den Betrieb ohne Zuweisung. `PR/mois × coût moyen de review × nombre de reviews par PR + corrections Steward + classifiers Approvals + CI supplémentaire`. Beginnt mit einer Review auf Anfrage oder bei der Eröffnung, nicht auf jedem Push, und setzt eine monatliche Obergrenze für Code Review und PR Steward (letzter hat keine Voreinstellung). `observe` • die Fähigkeit von Approvals, Reviews und Klassifizierungen
Kosten. Deaktivieren Sie die Verwendung von credits nicht genug, um die aktiven Agenten zu stoppen: Approvals deaktivieren, dann Steward, dann Code Review, wenn Sie diese Ausgaben schneiden wollen.

**Nach-PR-Haushalt Codex.** `@codex review` und automatische Reviews GitHub die Bedingungen des Code Review erfüllen; `/review` Lokal, Goal Mode, Heartbeats und Aufgaben Codex Mit deinem Konto authentifizierte Cloud ChatGPT verwenden die Zuteilungen für Plan und Oberfläche. Kein archiviertes Überwachungsskript oder Schlüssel API OpenAI Zusätzliches ist für den nativen Workflow nicht erforderlich. Überprüfen Sie jedoch Quoten, zusätzliche Gutschriften und effektive Berechtigungen: jede Wiederaufnahme und jede Korrektur kann die Quote verbrauchen, auch ohne neue Diff. Bevorzugt ein begrenztes Ziel oder ein kurzes Heartbeat mit Abzweigung durch SHA und expliziter Einstellung; nie beide gleichzeitig auf einem einzigen Zweig. `openai/codex-action` mit Schlüssel API bleibt eine Option von CI getrennt in Rechnung gestellt,
für den Automatisierungsbedarf, den die nativen Oberflächen nicht decken, zu sorgen.

<!-- section: s-3 -->
## Prompt caching: Haupthebel, aber genau zu formulieren

Um den Haushalt nicht zu explodieren, Struktur der Anfragen der Agenten deterministisch:

1. Legt den statischen Kontext oben auf: `AGENTS.md`, Regeln Scala, Architektur, Testkonventionen.
2. Setzen Sie dann den halbstatischen Kontext: Muster, Verträge JSON, Geschäftsverträge.
3. Legt den dynamischen Kontext unten: Geänderte Dateien, Kompilierungsfehler, Testlogs.
4. Vermeide es, den Schnellkopf bei jeder Iteration zu ändern, wenn du von dem Cache profitieren möchtest.

Ein erfolgreicher Hit-Cache kann die Kosten für **Lesen** von Eintrittstoken bei ca. 10 % der normalen Inputkosten je nach Lieferanten (auf den Modellen) Anthropic Strommengen: 5 % für Opus 5.5 und Sonnet 5.5, 2,5 % für Fable 5.2, 10 % für Haiku 5.5 ; 5 % für GPT‑6.2 Sol/Astra und GPT‑6.1 Sol- Das ist nicht " ^.90 % Einsparungen auf der gesamten Aufgabe n: Ausgabetoken, Cache-Schreiben, Tool calls und Schleiffehler bleiben in Rechnung.

<!-- section: s-4 -->
## Regeln für die Kreditverringerung

```text
- Ne donne jamais toute la repo par défaut.
- Donne des chemins de fichiers et une hypothèse de zone concernée.
- Coupe les logs à la première erreur utile.
- Après 2 échecs identiques, stop : repasse en diagnostic humain/IDE.
- Après 3 fichiers modifiés hors plan, stop : demande un nouveau plan.
- Après 300 lignes de diff inattendues, stop : review manuelle avant suite.
- Quand le contexte n'aide plus : `HANDOFF.md` explicite + session fraîche ; `/compact` n'est qu'un dernier recours.
- Préfère rg, Sourcebot, IntelliJ, Metals ou scripts locaux aux longs dumps MCP.
```

**Einsparen auf dem Doppel-Abonnement.[** Stabilisiert das Writer und seine Bemühungen während einer Flugbahn; Modelländerungen können den Cache stören und rework hinzufügen. Ein frischer Kontext bleibt freiwillig, um es unabhängig oder eine kontaminierte Hypothese zu überprüfen. Legt weder eine systematische umfassende Überprüfung auf jedem Mikro-Patch noch zweiteward auf ein und demselben PR vor. Entzieht die Überwachung durch repo/PR/SHA/check/finding, bevorzugt eine ereignisbezogene Erholung oder ein beschränktes Heartbeat, wenn die CI wartet, und stoppt es am Checkpoint. Messen Sie die verbrauchten Zertifikate nach Rollen und Aufgaben (wenn vom Anbieter ausgestellt) ; unterscheidet zwischen enthaltenen Krediten, gebührenpflichtigen Überschreitungen und API. Eine verbleibende hohe Quote ist kein Grund, mehr Ticketickets zu öffnen.

