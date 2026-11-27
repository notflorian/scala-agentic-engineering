<!-- section: chapter -->
# 3. Modellauswahl und Routing

<!-- section: s-1 -->
## Einfache Regel

```text
Qwen / Haiku bereiten vor und filtern.
Kleine Entwicklungsaufgaben unter enger menschlicher Kontrolle → GPT‑6 Luna High oder Sonnet 5.5 Medium.
Durchgängige agentenbasierte Entwicklung → GPT‑6.2 Sol Medium oder Opus 5.5 Medium.
Schwieriges Debugging / anspruchsvolle Architektur → Opus 5.5 High oder GPT‑6.2 Sol High.
Punktueller Frontier-Einsatz → GPT‑6.2 Astra Light oder Fable 5.2 Low, bevor du den Aufwand beim schwächeren Modell blind maximierst.
Nur ein implementierender Agent pro Worktree.
Die andere Modellfamilie prüft oder hinterfragt das Ergebnis, ohne automatisch den gesamten Ablauf zu wiederholen.
Ultra / mehrere Agenten nur bei wirklich unabhängigen Teilproblemen.
IntelliJ validiert.
Du entscheidest.
```

Das Routing sollte die [**Kosten der abgeschlossenen Aufgabe[** minimieren, nicht den Preis des ersten Aufrufs:

```text
Erwarteter Gesamtaufwand
= Erkundung + Implementierung + Überprüfung
+ Wahrscheinlichkeit der Nacharbeit × Kosten der Nacharbeit
+ Koordinationsaufwand
```

Ein teureres Modell kann daher der beste Kauf sein, wenn es eine schlechte Erforschung, mehrere unnötige Diffs und Schleifen von CI verhindert. Im Gegensatz dazu macht eine Mikro-Schleife, die von einem Senior gesteuert wird, Luna, Sonnet oder Haiku dominierend, sobald der Fehler innerhalb weniger Minuten erkannt wird.

*Die Aktualisierung der Versionen niemals in `build.sbt` ohne zu verlangen, dass der Agent zuerst eine MCP, Context7, Maven Central oder die offizielle Dokumentation. Namen und Versionen von Bibliotheken sind genau die Art von Informationen, die Vorlagen halluzinieren, wenn sie außerhalb des Kontextes arbeiten.*

<!-- section: s-2 -->
## Routing-Matrix

| Aufgabe                                                    | Modus         | Empfohlener Hauptakteur                   | Zweite nützliche Passage                           | Warum                                                                           |
|----------------------------------------------------------|--------------|----------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------|
| Ein Modul, grep, use, einfache logs zusammenstellen            | Micro-dev    | **Haiku 5.5** oder Qwen lokal                  | Keine, sofern nicht eindeutig                           | Hochfrequenz-Lesen, geringes Risiko                                             |
| Genaue mechanische Änderung, Boilerplate, Umbenennung   | Micro-dev    | **GPT‑6 Luna High**                          | Sonnet 5.5 Medium so subtilen Typen             | Sehr gute Kosten, wenn der Mensch die Führung behält                                    |
| Schreiben Sie einen einfachen Test aus bekannten Verhalten   | Micro-dev    | **GPT‑6 Luna High**                          | Sonnet 5.5 Medium so reicher Beruf Regel        | leicht nachprüfbare Ausgabe                                                       |
| Stack-Sortierung oder präziser Feilzug                           | Micro-dev    | **[Sonnet 5.5 Medium**                        | Luna High zum Auftragen eines kleinen Patches        | Sonnet bringt mehr Verständnis, ohne Opus bezahlen                               |
| Kleiner reproduzierter Fehler, bekannter Bereich                     | Micro-dev    | **[Sonnet 5.5 Medium**                        | Luna High für mechanische Tests/Verlag         | Kurzschleifen, sofortige Rückmeldung                                                 |
| Lokale Patch, nicht-triviale Typen oder Invarianten            | Micro-dev    | **[GPT‑6.1 Terra Medium**                     | GPT‑6.2 Sol Medium, falls erforderlich  | Drittes Mittel, das an schrägen Pflastern zu messen ist |
| Kleiner lokaler Refactor                                     | Micro-dev    | **[Sonnet 5.5 Medium**                        | Luna High für mechanische Überprüfung          | Senior behält Architektur                                                  |
| Gezielte Überprüfung eines kleinen Diffs                            | Überprüfung | **GPT‑6.2 Sol Light**                        | Sonnet 5.5 Medium wenn zweite nützliche Stellungnahme         | Mehr Urteil als ein Worker, ohne eine vollständige agentic review zahlen            |
| Komplette Standard-Issue, klares Spektakel                     | Agentic      | **[GPT‑6.2 Sol Medium**                       | **[Opus 5.5 Medium** als Review                  | Bester Fehler Codex zur Exploration → Pflaster → Tests → PR                        |
| Normale Multi-Datei-Feature                           | Agentic      | **[GPT‑6.2 Sol Medium**                       | Opus 5.5 Medium in Review                      | Ownership end-to-end mit Kosten Inhalt                                             |
| Komplizierte Feature, mehrere Schichten                      | Agentic      | **GPT‑6.2 Sol High**                         | Opus 5.5 Medium/High                           | Mehr Planung und Überprüfung                                         |
| Architektur oder Migrationswahl                       | Agentic      | **Opus 5.5 High**                            | Sol Medium für die Herausforderung des Plans             | Das Urteil beherrscht die Herstellung von Code                                           |
| Root Ursache unbekannt / bug Scala subtil                   | Agentic      | **Opus 5.5 High**                            | Sol Medium/High für unabhängige Hypothese    | Das Problem zu verstehen kostet mehr als das Patch                                     |
| Wettbewerb, async, flaky Test schwierig                 | Agentic      | **Opus 5.5 High**                            | Sol High, wenn die erste Spur fehlschlägt           | Verringert das Risiko einer Verankerung an einer falschen Ursache                                    |
| Migration/Öffentliche Kompatibilität                       | Agentic      | **GPT‑6.2 Sol High**                         | Opus 5.5 Hoch in einer konzeptionellen Bewertung           | Disziplinierte Vollstreckung + zweite unabhängiges Urteil                                |
| Großer Querrefactor                                | Agentic      | **Opus 5.5 High**                            | Sol Medium/High in Review                      | Opus für globale Konsistenz; Boden zum Brechen toter Winkel                     |
| Normale Review einer PR, geschrieben von Codex                 | Überprüfung | **[Opus 5.5 Medium**                          | Keine außer finding critical                    | Frischer Hintergrund und andere Modellfamilie                                         |
| Normale Review einer PR von Claude geschrieben                | Überprüfung | **[GPT‑6.2 Sol Medium**                       | Keine außer finding critical                    | Autor/Reviewer-Symmetrie                                                           |
| Review Architektur, Invarianten, Grenzfälle             | Überprüfung | **Opus 5.5 High**                            | Astra Light so besonders hoch    | Suchen Sie nach konzeptionellen Fehlern anstatt nur das Diff zu lesen             |
| Sicherheit, Auth, kritischer Vertrag                         | Kritik     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High als review                   | Kaufen Sie die überlegene Kapazität, ohne direkt in extremer Anstrengung zu gehen           |
| Sehr zweideutiges Problem, End-to-End-Urteil                | Frontier     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High, um den Plan zu kritisieren           | Die Beurteilungsfähigkeit zählt mehr als die Länge des Diffs                   |
| Sehr schwierige Entscheidung in der Mitte einer normalen Aufgabe    | Advisor      | **Fable 5.2 Low**                            | Sol/Opus bleibt der Executor                     | Pünktlich ein Grenzurteil kaufen, ohne die ganze Aufgabe zu übertragen         |
| Boden High fehlschlägt durch Kapazitätsgrenze                   | Klettern     | **GPT‑6.2 Astra Light**                        | Medium/High nur bei Bedarf            | Das Ändern von Tier kann weniger kosten als ein verlängerter Extra High Sol                    |
| Opus High fehlgeschlagen durch Kapazitätsgrenze                  | Klettern     | **Fable 5.2 Low**                            | Boden/Astra für Herausforderungen                      | Gleiche Logik: Geringe Belastung vor niedrigerer Höchstkraft               |
| Einfaches fehlgeschlagen CI nach korrekter Implementierung            | Wiederaufnahme      | **GPT‑6 Luna Hoch** oder **Sonnet 5.5 Medium** | Klettern nur so konzeptuelles Problem      | Nicht zahlen Sol/Opus für lokale und nachprüfbare Korrektur                     |
| Überwachung nach der autonomen PR (CI, review, mergegibility)         | Wiederaufnahme      | **[GPT‑6.2 Sol Medium**                      | High wenn root Ursache schwierig; Sol 6.1 im Fallback | Goal Modus, Heartbeats oder Cloud; sequenzielle Sperre, nicht Ultra           |
| Zweites Versagen, das eine falsche Auffassung offenbart          | Wiederaufnahme      | **GPT‑6.2 Sol Hoch** oder **Opus 5.5 Hoch**    | Die andere Familie verwenden, um die Verankerung zu brechen | Das Problem ist nicht mehr mechanisch: die Hypothese muss neu bezeichnet werden                 |
| Wiederholte Schach trotz Sol High / Opus High               | Klettern     | **GPT‑6.2 Astra Light** oder **Fable 5.2 Low**   | Die andere Grenze in der Herausforderung                 | Die Fähigkeit wird zum einschränkenden Faktor; mit einem eigenen Kontext wieder losgehen         |
| Autonome Sitzung > 30 min, Sequenzabhängigkeiten     | Weitblick | **Opus 5.5 Extra (`xhigh`)**                 | Hochboden am Ende                              | Extra ist durch die Länge gerechtfertigt, nicht durch die symbolische Bedeutung                |
| Sehr schwierige Arbeit über mehrere Stunden    | Frontier     | **Fable 5.2 High**                           | Astra Light/Medium als unabhängige Bewertung      | Die hohen Grenzkosten für die Flugbahnen, in denen größere Wiederholungen vermieden werden, buchen |
| Erkundung des entschärfenden Basis-Skala-Code                  | Multiagent  | **GPT‑6.2 Sol Ultra**                        | Opus Medium für Synthese/Review               | Ultra gilt vor allem für unabhängige read-heavy Achsen                           |
| Tests, Exploration und Sortierung, die massiv parallel sind | Multiagent  | **GPT‑6.2 Sol Ultra**                        | Claude nur über wichtige Anomalien | Parallelität zahlt, wenn die Teilaufgaben unabhängig und überprüfbar sind       |
| Mehrere Writers auf denselben Dateien                 | —            | ** zu vermeiden**                                 | Sequentisierung                                 | Die Koordinierungskosten liegen im Allgemeinen über dem Gewinn                               |

> **Anmerkung Qwen3-Coder-Next lokal** : das offizielle Modell ist ein MoE von **80B Parameter insgesamt, 3B aktiviert**, avec 48
> Hybridschichten, ein nativer Kontext von **262 144 Tokens** und nur für den Betrieb **Nicht-Thinking**. Le
> Zahl
> reduzierten aktiven Parametern verbessert die Berechnungskosten, aber die [**80B des Gewichts müssen dennoch in
> Speicher
> ** : « 3B actives bedeutet also nicht, dass es sich wie ein dichtes RAM verhält. 3B.
>
> Die offiziellen GGUF-Größen sind: **Q4_K_M 48,4 Go**, **Q5_K_M 56,7 Go**, **Q6_K 65,5 Go** und **Q8_0 84,8 Go**. La
> Dateigröße ist jedoch nicht der Gesamtverbrauch: fügt Kontext-Cache, Backend-Buffer,
> Server, macOS, IntelliJ, sbt und JVM Projekt **128 Go**Die vier Varianten können theoretisch
> chargées, mais elles n'offrent pas la même marge opérationnelle.
>
> ```text
> Q4_K_M  → Standardeinstellung mit maximaler Reserve: IDE, sbt und mehrere JVMs laufen weiterhin problemlos.
> Q5_K_M  → empfohlene Standardeinstellung: bester Kompromiss zwischen Qualität und Speicherbedarf auf diesem Rechner.
> Q6_K    → Option für höhere Qualität: praktikabel, wenn die anderen Anwendungen wenig Ressourcen beanspruchen.
> Q8_0    → Evaluierungsoption: möglich, aber mit weniger Reserve. Der Vorteil gegenüber Q5/Q6 muss sich erst zeigen.
> ```
>
> Die offizielle Dokumentation Qwen verwendet gerade **Q5_K_M** in seinem Beispiel `llama.cpp`, mit `-c 40960`, und nicht die
> Maximaler Kontext 256K. Für die tägliche Arbeitsvermittlung, geh auf **32K à 64K**, und dann erhöht sich nur, wenn eine
> Die tatsächliche Aufgabe rechtfertigt dies. Der Kontext, der vom Modell angezeigt wird, ist eine maximale Kapazität, keine Konfiguration
> Wirtschaft
> Standard.
>
> **Empfehlung für dein M5 Max 128 Go** : haltbar gemacht **Q4_K_M und Q5_K_M** auf der SSD. Verwende Q5_K_M als Profil
> Voranalyse täglich, Zusammenfassung von Modulen und einfache Tests; Wechseln auf Q4_K_M, wenn IntelliJ,
> mehrere Module sbt, Spark oder JVM Schwer verbrauchen bereits viel Speicher.6_K oder Q8_0 wenn
> un
> bake-off Scala zeigt einen messbaren Qualitätsgewinn. Mit [8 To SSD ist der Speicher nicht die Belastung ; la
> Druck
> Gedächtnis, Latenz und Qualität pro Aufgabe sind es.
>
> **Backend Apple Silicon** Teste **MLX-LM und llama.cpp** Anstatt sofort einen einzigen Motor zu frieren.
> MLX-Konversionen 4-bit und 8-bit existieren, und ein reproduzierbares Verhältnis zu Qwen3-Coder-Next zeigte eine Dekodierung.
> Mit MLX ist es wesentlich schneller als mit einer bestimmten Version von llama.cpp auf Apple Silicon. Dieses Ergebnis hängt von
> Versionen und keine Garantie für M5 Max; es rechtfertigt eine lokale Benchmark mit eingefrorenen Versionen.
> `llama.cpp` bleibt jedoch der am besten dokumentierte Weg von [Qwen und stellt einen OpenAI-kompatiblen Server leicht aus.
>
> **Metal und Kabelspeicher[**: nicht vorhanden  ✓ 75 % .] % ✓ als absolute materielle Grenze. `llama.cpp` zeigt an
> Starten `recommendedMaxWorkingSetSize`, das ist der Wert, der auf der betreffenden Version von macOS und dem Mac zu beobachten ist.
> nicht dokumentierte Einstellung `iogpu.wired_limit_mb` existiert und wird von der Community verwendet, aber es darf nicht zu einem
> Standardanforderungen: Testet zuerst das Modell ohne Systemänderungen. Q8_0 kann auf einer Maschine betrieben werden 128 Go,
> aber ein langer Kontext oder mehrere Slots können den Prozess dieser Grenze näher bringen, bevor die physische RAM
> entweder
> Vollständig beschäftigt.
>
> **Mindestmessprotokoll** : Vergleich Q4_K_M, Q5_K_M und ggf. Q6_K auf den gleichen zehn Aufgaben Scala, avec
> Der gleiche Kontext und der gleiche Harness. Maßt den schnellen Prozess, den Generationsdurchfluss, die Zeit bis zum
> Erste Token, maximale Speicher, Speicherdruck macOS und Anzahl der angenommenen Aufgaben.
> nur die Anzahl der aktiven Parameter: Hybrid-Architektur und Kernel-Implementierung können
> Abweichungen
> , die zwischen den Backends bestehen.
>
> **Qwen3.8-27B.** Die Dichte **Qwen3.8-27B** wird der lokale Herausforderungenger quality-first, der dem
> bake-off Scala. Qwen veröffentlicht einen Kontext, der bis zu 1M je nach Einsatz und Editor-Scores 73 über
> Terminal[Bench 2.1 und 61,7 auf SWE-bench Pro. Diese Zahlen rechtfertigen nicht den Ersatz von Standardcoder-Next:
> testen
> beide mit dem gleichen Harness, dem gleichen Kontext, den gleichen Werkzeugen und dem gleichen Zeitbudget. **Coder-Next bleibt die
> baseline vor Ort spezialisiert und wirtschaftlich; Qwen3.8-27B ist der Herausforderer zu bevorzugen, wenn Qualität mehr zählt
> die Durchflussmenge.** Tarife API Qwen3.8 dépendent de la région et ne doivent pas être présentés comme un prix mondial.

>
> **Qwen3.8-Omni-Flash.** Seit dem 17 September 2026, Alibaba bietet auch dieses Modell API multimodaler Text, Bild,
> Audio- und Videoeingaben, Textausgang, function calling, thinking konfigurierbar, Websuche, Kontext-Cache,
> **1M tokens Kontext** und bis **131 072 Ausgabetoken** via Chat Completions oder Responses API. Er ergänzt
> Routing für die Analyse von Screencasts, Talks, Schnittstellen oder multimodalen Dokumentationen; es ** ersetzt nicht[**
> Qwen3-Coder-Next als lokale Code-Baseline noch Qwen3.8-27B als Herausforderung Scala quality-first. Die Tarife variieren
> je nach Einsatzgebiet: Bewahre diese Daten außerhalb der nachhaltigen Routing-Regeln und prüfe Model Studio auf
> Zeit der Wahl.

<!-- section: s-3 -->
### Seite Anthropic

| Muster         | API ID              | Tarif (Output/Output / M tokens) | Hintergrund          | Standardanreiz | Aktive Rolle in diesem Leitfaden                                                           |
|----------------|---------------------|---------------------------------|-------------------|-------------------|------------------------------------------------------------------------------------|
| **Fable 5.2**  | `claude-fable-5-2`  | $8 / $40                        | 1M (Ausgang 128K)  | `high`            | Frontier: anspruchsvolles Denken und langer Horizont, wenn Opus 5.5 nicht ausreicht      |
| **Opus 5.5**   | `claude-opus-5-5`   | $4 / $20                        | 1M (Ausgang 128K)  | **`medium`**      | Agentic Default: autonomes Coding, Architektur, Debugging und große Refactors      |
| **Sonnet 5.5** | `claude-sonnet-5-5` | $2 / $10                        | 1M (Ausgang 128K)  | `high` API        | Micro-dev / Aufgaben genau spezifiziert; `medium` empfohlen für agentic coding borné |
| **Haiku 5.5**  | `claude-haiku-5-5`  | $0.10 / $0.50 (prompt ≤ 100K)   | 1M (Ausgang 128K)  | `medium`          | Workers, Sortieren, Extrahieren, Logs, Subagenten mit geringem Risiko                     |

> **Laufendes Routing:** Anthropic empfiehlt, die meisten Workloads mit **Opus 5.5**,
> mit Standardkraft `medium`, und dann die Anstrengung, bevor Sie das Modell ändern anpassen. **Sonnet 5.5**, am
> gut spezifiziertes agentisches coding beginnt sinnvoll bei `medium` und steigt auf [`high` für längere Aufgaben oder
> Sehr schwierig.
> `xhigh` (bemerkenswert **Extra** in diesem Leitfaden) und `max` sind für Fälle reserviert, in denen die Evals einen Gewinn zeigen. **Haiku 4.5 n
> unterstützt nicht den Belastungsparameter; Haiku 5.5, die es ersetzt, unterstützt es mit `medium` Standard.** Die folgenden Absätze auf Sonnet 5 Opus 5 restent des repères de
> Migration
> Historisch; sie ersetzen diese aktive Matrix nicht.

> **Migration API zu Opus 5.5 / Sonnet 5.5.** Die beiden Modelle schreiben dem Kunden mehr Disziplin als den Kunden vor.
> frühere Generationen: Thinking adaptive ist die normale Diät, *forced tool use[* (`tool_choice: any/tool`)
> gibt einen Fehler zurück 400, und die [*thinking blocks* müssen an ihrem Modell und dem Gespräch, das sie
> Produkte. **[Opus 5.5** weist auch die nicht-Standard-Sampling-Parameter und Prefill-Assistent; seine Anstrengung durch
> Fehler `medium`. **Sonnet 5.5** verwendet `thinking: {"type": "between_tools"}` zum Entfernen des ursprünglichen Thinking
> [`low` nur auf `high`, und gibt jetzt den Zwischentext zwischen tool calls in Blöcken `thinking` zurück.
> Auf Claude API und Google Cloud verwenden beide Modelle das aktuelle Computer-Toolset
> `computer_toolset_20260801` anstatt `computer_20251124`]. Daher muss eine Modellmigration **payloads,
> Streaming, Tools und Konversation**, nicht nur die Modell-ID ersetzen.

> **Sonnet 5** ersetzt Sonnet 4.6 (`claude-sonnet-4-6`, immer zum gleichen Tarif verfügbar
> $3/$15) als täglicher Treiber. *drop-in replacement* Seite API, mit drei Verhaltensänderungen bei
> wissen, bevor Sie migrieren:
> - **Adaptive thinking standardmäßig aktiviert[** ; Extended thinking manuell (`thinking: {type: "enabled"}` mit
>   `budget_tokens`) gibt nun eine **Fehler 400** ✓ wandert in den adaptive thinking.
> - **Gesperrte Sampling-Einstellungen** : Wert nicht fehlgeschlagen `temperature`, `top_p` oder `top_k` ergibt
>   ein Fehler 400.
> - **Neuer Tokenizer** (gleiche Blutlinie wieOpus 4.7+) : ~30% mehr Token für denselben Text (bis 1.35x
>   Der Tokenizer kann die Anzahl der in Rechnung gestellten Tokens jederzeit erhöhen .
>   schnell mit dem Token Counting Endpoint und schau dir die `max_tokens` Enge.
>
> Sonstige operative Besonderheiten: **Aufgabe Control** Allgemein (Ebenen low → **xhigh**, Fehler *high* über
> die [API und [Claude Code), erste ** Echtzeit-Cyber Security-Schutz[** auf einem Sonnet (eine Ablehnung kehrt in HTTP zurück
> 200 mit [`stop_reason: "refusal"`], kein Fehler, nicht im Client zu verwalten), kein Priority Tier, Ausgabe 128K
> (300K en batch über den Beta-Header `output-300k-2026-03-24`). Es ist auch das neue Standardmodell der Pläne
> Free und Pro auf claude.ai.

> **Gemeinschaftsrabatte** : das schnelle Caching und das Batch-Verfahren ( ✓–50% Input und Output) gelten für *alle* Modelle
> Claude. Der Preis für das Abspielen des Caches hängt jedoch vom Modell ab: **Fable 5.2 kostet $0.20/M tokens im Zwischenspeicher gelesen**
> (gegenüber $0.25/M für Fable 5.1). Das Batch bleibt nützlich für nicht-dringende Arbeit: PR summaries gruppiert,
> Planung von Prüfungen und Erzeugung von Fixierungen. Fable 5.2, Opus 5.5 und Sonnet 5.5 einschließlich Kontext 1M zum Tarif
> Standard, ohne lange Kontextüberlastung.
>
> **Preisgenauigkeit.** Cache read ist wert **0,025× Input** über Fable 5.2/5.1 ($0.20 und $0.25/M),
> **0,05×** über Opus 5.5 und Sonnet 5.5 ($0.20 und $0.10/M) und 0,1× über Haiku 4.5. Haiku 5.5 ist das einzige aktuelle Modell
> mit einem **Pince-Längenbereich** : über 100 000 tokens hinaus (inklusive Versteck), alle seine Tarife sind
> multipliés par cinq. Batch : Fable 5.2 $4/$20, Opus 5.5 $2/$10, Sonnet 5.5 $1/$5. Fast Modus: Fable 5.2 $16/$80,
> Opus 5.5 $8/$40. `inference_geo: "us"` verwendet einen Multiplikator von 1,1× für die betreffenden Kategorien.

> **Claude Fable 5.2 ersetzt Fable 5.1 im aktiven Routing dieses Leitfadens.** Formblatt
> Technik: ID `claude-fable-5-2` (`anthropic.claude-fable-5-2` über Bedrock), Kontext **1M**, Ausgabe **128K**,
> **$8/$40**, write-Cache 5 min $10 und 1 h $16, cache read **$0.20/M**, Batch $4/$20, fast mode `speed: "fast"` à
> $16/$80, adaptive thinking immer aktiv, Standard-Bemühungen `high`, cutoff Juni 2026, nicht vor dem
> 9 November 2027. Gleiche Einschränkungen wie 5.1 : **30 obligatorische Hafttage (keine ZDR ohne Genehmigung)
> ausdrücklich)**, `tool_choice: any/tool` und Prefill in 400, Sampling zu verpassen, keine Priority Tier, keine Strukturd
> Outputs für CMEK-Organisationen. Das Modell erzeugt etwa 30 % schneller als 5.1. **Mythos 5.2** ist das gleiche
> Modell mit weniger Schutz, nur für geprüfte Organisationen.
>
> **Positionierung.[** Die offizielle Matrix bleibt die meisten Workloads beginnen mit Opus 5.5; man geht auf
> Fable 5.2 wenn die Werte `xhigh` oder `max` restent insuffisantes sur du raisonnement exigeant ou du long-horizon.
> Neu in das Routing einzubinden: auf FrontierCode 2.0 (was misst, wenn die Hüter die Änderung verwässern würden),
> Anthropic Bericht **Fable 5.2 `high` à 45,3 %, aufOpus 5.5 die beste Anstrengung (45,5 % (%), für etwa
> Hälfte der Kosten je Aufgabe**. Editor-Scores mit bestem Aufwand: FrontierCode 2.0 **49,1 %** (Opus 5.5 45,5 ; Astra
> 42,8 ; Fable 5.1 32,4), FrontiersWE v2 **69,9 %** (Opus 62,3 ; Astra 65,5), Remote Labor Index 41,3 % dagegen 21,3 %
> für Opus. Auf dem kurzen coding ist die Abweichung gering: Terminal-[Bench 4.0 67,6 % gegen 66,4 % (Opus `xhigh`), in der
> Fehlermarge. Unabhängige Messungen Vals bestätigen die Nuance: Gleich gleich mit Opus 5.5 am Terminal-[Bench 4.0
> (65,15 %), Opus vor SWE-bench Multimodal ([70,2 %] % gegen 62,3 %).
> **Mini-SWE-Agent** • die Gleichbehandlung von Frauen und Männern, **$14,56/Aufgabe für Fable gegen
> $12,04 für Opus**, mit Fable schneller (55 min gegen min 64 min) : Kostenvorteil pro angekündigter Aufgabe
> durch Anthropic über FrontierCode ** verallgemeinert sich nicht** auf andere Harnesen. Praktische Folge:
>
> ```text
> Opus 5.5 High reicht von der Leistungsfähigkeit her nicht aus → Fable 5.2 vor Opus 5.5 Max, im privaten Scala-Benchmark messen
> Punktuelle schwierige Entscheidung (Beratung) → Fable 5.2 low/medium
> Langer autonomer Auftrag → Fable 5.2 high (low/medium beenden den Turn häufiger zu früh)
> Klar abgegrenzte Aufgabe, UI-/Frontend-Bug oder routinemäßiges Review → Opus 5.5 oder Sonnet 5.5 bleiben wirtschaftlicher
> ```
>
> **Breaking changes da Fable 5.1** (im offiziellen Migrationsleitfaden überprüft):
> - **Die Präfixprüfung** gilt jetzt für alle Konten: Ein Thinking-Block mit anderem `system`,
>   anderen `tools` oder einem anderen Verlauf als bei seiner Erzeugung führt zu einem 400-Fehler (`The block is bound to a different
>   conversation`). **Eine Änderung der MCP-Werkzeugliste zwischen zwei Anfragen zählt als Bearbeitung**: Fixiere
>   die Werkzeugliste für die Sitzung oder ändere die Werkzeuge im Gespräch (Beta
>   `inline-tools-2026-09-15` über Nachrichten mit `role: "system"`). Achte auf Harnesses, die Werkzeuge
>   bei Bedarf laden und `tools` ändern;
> - **Fable 5.1 und Opus 5.5 Lesen Sie nicht die Thinking Blocks Fable 5.2** (sie werden fehlerfrei gelöscht, so dass die
>   Denken ist in Stille verloren) ; Fable 5.2 liest die von 5.1 undOpus 5.5. Serverfallbacks
>   (`fallbacks: "default"`, beta `server-side-fallback-2026-07-01`) sind nur `claude-opus-4-8` und
>   `claude-opus-5`: protokolliert das ausgeführte Modell;
> - `computer_20251124` ergibt 400 (außer Bedrock) : verwenden `computer_toolset_20260801` ;
> - Der Advisor eines Vollstreckers Fable 5.2 muss `claude-fable-5-2` oder `claude-mythos-5-2` sein;
> - Der Thinking zählt in `max_tokens` (Risiko von `stop_reason: "max_tokens"` vor allem Text) und Fable 5.2 hat seine
>   **Eigene begrenzte Milz**, getrennt von Fable 5/5.1. Neue nützliche Betas: Komplett auf Anfrage
>   (`compact-2026-09-04`), binding des thinking blocks (`thinking-binding-controls-2026-08-01`, mit
>   `prefix_mismatch_behavior: "drop_block"` nur als Palliativ).
>
> **Verhalten, die direkt die Qualität der Diffs und die Kosten betreffen[** (Priming-Leitfaden Fable 5.2):
> - **Eigenschaft des Codes.** Ohne ausdrückliche Angabe fügt das Modell der bestehenden Struktur hinzu, dupliziert und meldet die
>   Nachbar- und nicht Korrekturprobleme. Der Satz von Anthropic (✓ This codebase is yours...) macht
>   Der duplizierte Code wird in etwa der Hälfte der Tests zusammengeführt, kostet aber etwa 1,5× aus der Ausgabe, fügt hinzu
>   nicht angeforderte Tests und Docs und ändert das Verhalten in einem von sechs bis zehn Versuchen. **Für Tickets
>   diff minimal in diesem Leitfaden, nicht hinzufügen** ; behält es einer ausdrücklichen Aufgabe der Deduplizierung oder Refactor vor;
>   und repliziere den Diff anstatt die Zusammenfassung, die oft kleine Änderungen verpasst.
> - **Über-Delegation.** An `xhigh` und `max`, Fable 5.2 kann Subagenten starten, um seine eigene Arbeit zu wiederholen, und die
>   Subagents können einen großen Teil der Sitzungskosten ausmachen. `AGENTS.md`, Skills und
>   Agenten-Dateien, die zu delegieren, und überprüft die Standard-Vorlage der Subagenten.
> - **Frühe Touren sind vorbei** (Liste der verbleibenden Aufgaben, bietet weiter) häufiger auf `low` und `medium` :
>   für eine lange Mission, fügt die Lieferung hinzu, nicht, solange es von der geforderten Arbeit bleibt, alles in
>   Unterschiedliche (zu behandelnde) gewöhnliche Hindernisse und vorsätzliche Sperrung (Verbotsdatei, Verwechslungsschutz: zu lassen und
>   signalisieren). Bewahre deine eigenen Bestätigungen für riskante Aktien.
> - **Server-Budget-Budget, OK?** Das `task_budget` API ist indikativ , **Externe Obergrenze** Kosten,
>   Anzahl der Anrufe, Dauer und Anzahl der Versuche im Harness. Ein `max_tokens` zu eng kann unterbrechen
>   Fable vor dem ersten sichtbaren Text, da die thinking tokens in der Ausgabe zählen. Wenn die Sitzung scheint
>   Stille, verwendet Updates zwischen Werkzeugen, wenn verfügbar, anstatt die Recovery-Multiplikation.
> - **Zu reinigende geerbte Anweisungen**:  ✓ antwortet ohne Beratung    ✓ stoppt die Reflexion nicht ab `medium`
>   (Normalerweise senkt die Belastung) ; die Zeilen ✓ behandeln diese Antwort als abgeschlossen ✓ aus dem preventing Opus 5.5 machen
>   das Modell viel weniger geeignet, seine eigenen Fehler aufzufangen; die Token-Budgets geschrieben in der schnellen
>   können ohne Verlust bei `high`/`xhigh` entfernt werden; die im Gedächtnis gesammelten veralteten Vorsichtsmaßnahmen verringern die
>   Nützliches Verhalten. Das ist genau die Rolle von `/doctor prompt-audit` (Abschnitt 3, Subagenten).
>
> **Zugang und Quoten.** Claude Code **2.1.321+** (`claude --model claude-fable-5-2` ; Alias `fable` hängt von
> Die zulässigen Max/Ultra-Pläne können Fable bis zu einer maximalen Fraktion von **50 % der
> Wochenbeschränkungen**, je nach den tatsächlichen Bedingungen; die Nutzung auf Pro kann von zusätzlichen Gutschriften abhängen
> oder vorübergehender Beförderung.
> Nie **Sichtbare Vorlage**, **Einschließlich Quoten** und **Abrechnung API/Mittel** : Kontrolle des Verbrauchsbildschirms und
> Bedingungen des Plans zum Zeitpunkt der Sitzung. Rekalibriert die Anstrengungen `medium`, `high` und `xhigh` und die Kosten pro Aufgabe.

> **Tokenizer-Note** : Der neue Tokenizer wurde eingeführt durch **Opus 4.7** (nicht 4.8) und erzeugt bis zu ~35% de
> Tokens zusätzlich alsOpus 4.6 für denselben Text. **Sonnet 5 nimmt die gleiche Linie an** (~30% Tokens mehr als
> Sonnet 4.6, bis [1.35]x je nach Inhalt. Die Zählungsstrafe bleibt für die Migration Opus bis
> identischer Tarif; auf Sonnet 5, den endgültigen Tarif **$2/$10** ausgleicht einen großen Teil der Zunahme der Zahl
> von Tokens im Vergleich zu Sonnet 4.6. Die Passage Opus 4.7 → 4.8 keine zusätzlichen Sanktionen gegen Tokenizer verhängt.

> **Opus 5 und Übergang von 4.8** Opus 5 ist jetzt das **Modell Anthropic standardmäßig schwierig** Tarif
> identisch mit Opus 4.8 ($5/$25). Garde 4.8 nur als Kompatibilitätsfall oder historischer Verweis.
> - **Fast Mode** ($10/$50, ~2.5x die Standardgeschwindigkeit: für eine harte Aufgabe, aber *interactive[* (debugging en pair),
>   Opus 5 Fast ist oft ein besserer Kauf als Fable.
> - **Aufgabe Control** : Durch Anstrengung zu fahren bleibt der explizite Schritt vor Fable 5.2. Über Opus 5, `xhigh` und `max`
>   erfordern, dass der Thinking aktiviert bleibt; `thinking: disabled` mit diesen Ebenen gibt einen Fehler zurück400.
> - **Dynamic Workflows** ist weiterhin relevant für die Parallelität von Base-Scale-Code; in Claude Code, komplettiert jetzt
>   Agent View. **Agent Teams** bleibt experimentell und **Ultrareview** in research preview: Verwandele sie nicht
>   noch in obligatorischen Workflow-Abhängigkeiten.

> **Note Claude Managed Agents** (gehostete Plattform, Beta public seit April 2026, header
> `managed-agents-2026-04-01` : Seit Code with Claude (6 Mai 2026 fügt die Plattform **Outcomes** (grader
> **Multiagent-Orchestrierung[** (bis
> 20 parallele Spezialisten auf einem geteilten filesystem, **webhooks** am Ende der Sitzung (beta)
> (research preview: memory curation zwischen den Sitzungen) und [**Dreaming[** (research preview).
> Tarif API + $0.08 pro Stunde der aktiven Sitzung. Für diesen Leitfaden ist dies die dritte Option bei langen Missionen,
> neben Fable mono-agent und Opus + Dynamic Workflows ist es vor allem relevant, wenn Sie einen mit
> Vollstreckbare Erfolgskriterien (Outcomes ist die Plattformversion des ✓ gate de review    ✓ des Abschnitts 15A).

> **OpenAI Bedienstete API** ist die Seite gehostet OpenAI : Sie verwendet das
> Codex mit [**]Sessions langlebig**, verwalteter Compaction und Erholung, [MCP und Subagenten mit isoliertem Kontext.
> Zwei primitive materialisieren direkt das context engineering des Abschnitts 10: [**tool search** lädt die
> Werkzeugdefinitionen, wenn sie relevant werden, und **programmatic tool calling[**] ermöglicht es, zu ketten,
> Parallelieren und Filtern von Anrufen, bevor Sie nur die nützlichen Ergebnisse wieder injizieren. Das ist kein neuer Grund
> Bevorzugt OpenAI à Anthropic Vergleich **Bedienstete API**, Claude Managed Agents und lokale Harnesen zu Kosten von
> Änderung akzeptiert, unter Beibehaltung der gleichen Spektakel, Tests und Regeln für die Einstellung.
>
> **Computer use[** kann auch in einem Browser ausgeführt werden, der von OpenAI gehostet wird.
> erstellt die Sitzung, genehmigt ausdrücklich jeden neuen Ursprung und verwaltet sensible Authentifizierungen selbst.
> Eine ursprüngliche Genehmigung ist keine Bestätigung pro Aktie: für Kauf, Löschung oder andere Transaktion
> Halten Sie ein kontrolliertes Runtime oder ein separates Anwendungsgate.


Zusätzliche operative Merkmale:

| Muster         | Relative Latenz | Prompt caching     | Batch (Batch)–50%) | Operative Besonderheit                                                                        |
|----------------|------------------|--------------------|--------------|---------------------------------------------------------------------------------------------------|
| **Fable 5.2**  | Mäßig          | Ja ; read $0.20/M | Ja.          | Adaptive thinking immer on ; default `high` ; message pro message ; fast Modus $[$16/$80            |
| **Opus 5.5**   | Mäßig          | Ja.                | Ja.          | Adaptive thinking immer on ; defekt **`medium`** ; Low→Max                                     |
| **Sonnet 5.5** | Schnell           | Ja.                | Ja.          | Adaptive thinking ; default API`high`, aber `medium` empfohlen für agentic coding |
| **Haiku 5.5**  | Die schnellste   | Ja ; read $0.01/M | Ja.          | Standard-Anpassung thinking ; Standard-Angriff `medium` ; Preisstufen über [100]K tokens |

<!-- section: s-4 -->
### Seite OpenAI / Codex

**GPT‑6.2 Sol** ist der empfohlene Fehler für das **coding komplex und wiederholte agentielle Workflows** in Codex wenn verfügbar. OpenAI positioniert es als effizienter pro Aufgabe als Sol 6.1, zum gleichen Tarif API. **GPT‑6 Luna** fokussierte, wiederholbare und hochvolumige Aufgaben; **GPT‑6.1 Terra** ist das mittlere Tier. **GPT‑6.2 Astra** Es bleibt die Eskalation der Kapazität für die anspruchsvollsten Aufgaben.

| Muster          | ID API        | Standardpreis / 1 M tokens (Output/Output) | Empfohlene Rolle in diesem Leitfaden |
|-----------------|---------------|---------------------------------------------|-------------------------------|
| **GPT‑6 Luna**  | `gpt-6-luna`  | **$0.10 / $0.50** | Micro-dev, mechanische Veränderungen, einfache Tests, Sortieren und Workers mit geringem Risiko |
| **GPT‑6.1 Terra** | `gpt-6.1-terra` | **$1 / $5** | Lokale Patch und gezielte Bewertung, wenn Luna nicht urteilt |
| **GPT‑6.2 Sol** | `gpt-6.2-sol` | **$2 / $10** | **Standard [Codex Medium**: Ausgabe end-to-end, Multi-Datei-Feature, Tests, PR, review und stewardship |
| **GPT‑6.2 Astra** | `gpt-6.2-astra` | **$8 / $40** | Frontier: sehr zweideutiges Problem, kritischer Vertrag, Kapazitätssteigung |
| GPT‑6.1 Sol / GPT‑6 Astra | `gpt-6.1-sol` / `gpt-6-astra` | $2 / $10 ; $10 / $50 | Falls keine Versionen verfügbar sind 6.2; Historische Baselines |

> **GPT‑6.1 Terra schließt das Loch zwischen Luna und Sol.** Aus dem 26 Oktober 2026 (`gpt-6.1-terra`),
> es kostet **$1/$5** (cached input $0.05/M), d. h. die Hälfte des Bodens 6.1, mit demselben Fenster von ca. 1,05M tokens.
> ist verfügbar in ChatGPT Work und Codex (Plus, Pro, Enterprise, Edu; nicht auf der Registerkarte Chat) und beantragt eine Codex
> [0.159+ je nach Quelle.OpenAI positioniert es auf den aktuellen Fehlerkorrekturen, dem Computer use,
> Vision und Schreiben; für anspruchsvolles Coding bevorzugt nun **Sol 6.2 oder Astra 6.2**. Score veröffentlicht:
> 50,3 % am Terminal[Bench 4.0 bei max. Anstrengung [21,5 % für GPT‑5.6 Terra. Für diesen Leitfaden wird Terra zum **Candidat
> natürlich für bornierte Pflaster und kleine diffs review** wenn Luna ist zu fair und Boden zu teuer: zu starten
> durch Bake-off vor dem Ändern der Matrix.

> **GPT‑6.2 Sol und Astra** : 1,05M Fenstertoken, darunter 922K maximaler Eingang und 128Maximale K-Ausgang.
> Cache read: $0.10/M für Sol, $0.40/M für Astra; write-Cache 30 min bis 1,25× Input, 12 h à 2,5×.
> Über 272K tokens hinaus verdoppeln sich die Input-/Cache-Preise und der Output-Tarif wird mit 1,5 multipliziert.
> die gesamte Abfrage. Batch liegt bei 50 % des Standardtarifs; Flex wird nicht für neue Modelle 6.2 angeboten.
> Diese Preise werden nicht auf die Abonnementquote übertragen. Sol 6.1 Medium und Astra 6 Light sind weiterhin Fallbacks, wenn die
> Versionen 6.2 sind nicht verfügbar. stewardship ist eine Kapazität des Harness, nicht des Modells. benchmarks
> Die Veröffentlichungen der EU-Mitgliedstaaten werden in den letzten Jahren noch immer als historische Basis dienen, die nicht den Modellen zugeschrieben werden darf. 6.2.

> **Ultrafast ist ein Diensttier, kein neues Modell und kein Aufwandsniveau.** Historischer Vergleich: für GPT-6 Astra, das [API Ultrafast
> Ziel bis ~8× Geschwindigkeit von Standard und Rechnung im kurzen Kontext **$60/M input, $6/M cached input, $75/M versteckt
> write und $300/M output**. Benutze es nur, wenn die Latenz tatsächlich die Gesamtkosten überwiegt; für Schleifen
> Agentics mit vielen tool calls, OpenAI empfiehlt eine dauerhafte WebSocket-Antworten Verbindung. Ultrafast nicht
> übernimmt nicht den Wohnsitz der EU-Daten: es arbeitet in der globalen Verarbeitung oder mit US-Wohnsitz.
> Produkt, Astra Ultrafast ist insbesondere in **Pro 500** und einige Enterprise-Angebote enthalten. Es ändert sich daher nicht
> die Qualität dieses Abschnitts: `Astra Standard` und [`Astra Ultrafast` haben die gleiche Modellkapazität.
> Auf GPT‑6.2 überprüft die Tarife und Rechte des Plans vor Aktivierung; behält schnelle Dritte nur an Schleifen
> , die durch Latenz tatsächlich begrenzt sind, nicht auf die Erwartung von CI.

In **[Codex / Work**, wird mit den sichtbaren Ebenen **Light → Medium → High → Extra High → Ultra**. Der Fehler dieses Leitfadens ist **Sol Medium**, **Luna High** für Mikro-Schleife und **Astra Light** für eine Kapazitätsskalierung.`Ultra`] überschreitet einen einfachen Single-Run und ist nur rentabel, wenn die Arbeit tatsächlich in unabhängige Achsen zerlegt werden kann. Setzt API, bleiben die Namen der Ebenen `low/medium/high/xhigh/max` entsprechend dem Modell: nicht mit dem portablen Wert von `reasoning.effort`.

Die Vorlagen GPT‑5.6 können während des Rollouts verfügbar bleiben, stellen aber nicht mehr die aktuelle Standardroute dieses Leitfadens dar.

<!-- section: s-5 -->
#### Cinq dimensions à ne pas confondre

| Heber                            | Was er ändert                                                                                     | Praktische Regel                                                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Modell[**                        | Kapazität, Geschwindigkeit und Preis: Luna, Terra, Sol 6.2 oder Astra 6.2.                                 | Luna für die borné ; Sol 6.2 für die wiederholte Agentic; Astra nur, wenn die höhere Kapazität reduziert die Wiederholungen. |
| **Effort**                        | Begründungsbudget: Bezeichnung Codex Light→Ultra; API `low/medium/high/xhigh/max` je nach Modell. | Boden: Standardmedium ; Luna: High ; Astra: Light ; Erhöhung nur, wenn Planung/Überprüfung es rechtfertigt.   |
| **`reasoning.mode: "pro"`** (API) | Mehr Modellarbeit für eine zuverlässigere endgültige Antwort.                                    | Unabhängig von der Belastung; Standard/Pro-Vergleich auf repräsentativen Aufgaben.                                          |
| **`ultra` als Aufwand Codex**    | Einige SDK/Harness Codex stellen nun `ultra` als Reasoning-Ebene über `max` aus. | Es als eine Fähigkeit der Harness behandeln, nicht als tragbaren Wert der Responses API.                             |
| **Ultra / Multiagent**           | Orchestrierung von mehreren Agenten oder Sitzungen je nach Produktfläche/API.                         | Nur dann, wenn sich die Arbeit wirklich in unabhängige Bereiche spaltet.                                          |

In der **Responses API**, den dokumentierten Höchstwert von `reasoning.effort` Rest `max` und **Multiagent** bleibt eine separate Beta-Funktionalität. In einigen Harness Codex, `ultra` kann im Gegenteil eine Denkanstrengung bezeichnen. Ziehe daher niemals die Semantik des einzigen Wortes  ✓ Ultra  denn logge die Oberfläche, das Modell, die Anstrengung und die tatsächliche Zahl der Agenten ein. OpenAI veröffentlicht keine festen Kostenmultiplikatoren; Messung Gesamtkosten, Latenz und Erfolgsrate auf deinem Depot vor Standardisierung.

<!-- section: s-6 -->
#### Astra: Kontrollen für lange Dienstreisen

Astra fügt den Bediensteten drei besonders nützliche Fähigkeiten hinzu:

```text
async tool calling
→ während eines langsamen Toolaufrufs weiter analysieren oder andere Tools aufrufen

mid-turn steering
→ eine Vorgabe ergänzen oder den Kurs ändern, ohne den ganzen Auftrag neu zu starten

configuration updates
→ den Reasoning-Aufwand während der Ausführung ändern, ohne den Cache-Präfix unnötig zu verwerfen
```

Für ein agentielles Backend, bevorzugt die **Responses API** : Tool calling Astra ist die Referenzfläche. Astra akzeptiert nicht `reasoning.effort = none`, noch die benutzerdefinierten Einstellungen `temperature` / `top_p` Die als unvereinbar dokumentierten Dokumente. **Fast-Modus** API kann bis zu ~ gehen ~2× schneller für **2× Standardpreis** ; es hat keine Latenz SLA und darf nicht zum Mangel einer langen Mission werden.

<!-- section: s-7 -->
#### Verfügbarkeit und Flächen ChatGPT /Codex

| Fläche                  | Muster- und Moduszugriff                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **ChatGPT Work / Codex** | GPT‑6.2 Sol und Astra, GPT‑6.1 Terra, Luna und Fallbacks nach Plan, Kunde, Workspace und Rollout.                                              |
| **[GPT‑6.2 Sol /Astra**  | Plus, Pro, Business, Enterprise und Edu in Codex/Work nach Rechten; Light→Ultra Aufwandssteuerung nach verfügbaren Parametern. |
| **GPT‑6 Luna**           | Wirtschaftsmodell für fokussierte und wiederholbare Aufgaben in Work/Codex.                                                            |
| **Ultra/Multiagent**  | Für unabhängige Achsen zu verwenden; sie nicht als ✓ mehr Reflexion über eine Sequenzkette zu betrachten.                    |
| **API**                  | `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6-luna` über die unterstützten Oberflächen; die Werkzeuge und die Anstrengungen pro Modell überprüfen.                |

Die tatsächlichen Rechte hängen immer vom Plan, der Region, dem Workspace und dem Rollout ab. Verschlüsseln Sie niemals eine dauerhafte Produktregel aus dem Namen eines Abonnements.

<!-- section: s-8 -->
#### Caching, Sicherheit und Sicherung

GPT‑6.2 Sol berechnet den cached input **$0.10/M** gegen $2/M als Standardinput; Writes Cache bleibt bei 1,25× Input. GPT‑6 Luna , um **$0.01/M** en cached input. Also stabilisiert sich die Spitze des Temporen (`AGENTS.md`, Übereinkommen Scala, Verträge, Testregeln) und hinterlässt diffs, logs und Fehler unten.

> **Zwei Kostenträger im Volumen.** Über GPT‑6.1 Sol und GPT‑6 Luna, Batch und Flex kosten 50 % weniger als
> Standard ; auf GPT‑6.2 Sol/Astra behält Batch diesen Rabatt, aber Flex wird nicht angeboten.
> Verwende sie für das, was Latenz toleriert: geplante Prüfungen, PR-Summarien zusammen, Erzeugung von Fixierungen und Sortierung
> massive. Nicht automatisch umsetzen diese Tarife API zu der Quote ChatGPT/Codex : Der richtige Indikator bleibt die Kosten
> Aufgabe abgeschlossen in der tatsächlich verwendeten Oberfläche.

GPT‑5.6 bleibt in Cyber als "High-      ✓" eingestuft, aber nicht als "Critical " ✓. **GPT‑6 Astra (Originalgeneration) ist das erste Modell OpenAI Critical in Cybersicherheit eingestuft** : mit den richtigen Werkzeugen kann es unbekannte Schwachstellen finden und neue Betriebsketten entwickeln. Dieses Niveau der Kapazität begleitet von einer strengeren Flugbahnüberwachung: in ChatGPT/Codex, eine legitime Aufgabe kann verlangsamt, unterbrochen oder eine Validierung beantragt werden; API, die Arbeit kann gestoppt werden.

Diese Kapazitätserhöhung rechtfertigt keine zusätzliche Autonomie. Mit Astra, noch deutlicher machen: Datei-Scope, Netzwerk, externe Operationen, zerstörerische Schriften, Budget, Dauer, Abschaltungsbedingungen und menschliche Validierung. Positiver Punkt für den sensiblen Code: **Astra unterstützt die Zero Data Retention für Kunden API Förderfähige**, während Fable 5.2 fordert 30 Standard-Tage, es sei denn, ausdrückliche GenehmigungAnthropic.

<!-- section: s-9 -->
#### Benchmarks und Vorsichtsmaßnahmen

Die Astra-Startzahlen sind besonders stark in **coding agentique und computer use**, aber müssen an ihren Hebegurten festhalten. OpenAI Bericht insbesondere: Terminal-Bench 4.0 **57,9 % Astra vs. 55,8 % Fable 5.1**, DeepSWE 1.1 **74,1 % gegenüber 67,4 %**, FrontierCode Extended **64,5 % gegenüber 63,6 %** und seine internen Migrationsaufgaben DB **63,9 % gegenüber 57,8 %**. Auf AutomationBench erreicht Astra **41,4 % gegenüber 31,4 %** für Fable 5.1. Dies sind Bewertungen, die von OpenAI : nützlich als Signal, nie als Urteil über Scala.

Die unabhängige Bewertung Artificial Analysis nährt die Tabelle stark. **Coding Agent Index v1.4**, Claude Code + Fable 5.1 (`max`, mit Fallback) erhält **70** gegen **67** für Codex + Astra (`max`), aber Astra verbraucht etwa **4,0M tokens/Aufgabe gegen 7,1M** und kostet ungefähr **$4,72/Aufgabe gegen $9,18**. über die **Intelligence Index**, Fable 5.1 `max` ist auch vor (**66 vs. 61**) Die gute Lehre ist daher nicht ✓ Astra > Fable ✓: **Fable behält einen kleinen Qualitätsvorteil in diesen Protokollen zusammen, Astra einen großen Vorteil der Effizienz pro Aufgabe in Codex**.

Astra veröffentlicht auch eine sehr gute lange Erinnerung auf MRCR v2 : **100 % à 256–512K** und **96,3 % à 512K–1M**. Verwandele diese Punkte nicht in die Erlaubnis, das ganze Monorepo zu senden: über 272K, sein Tarif steigt und die *Kontext rot* bleibt ein Problem der Argumentation, nicht nur der physischen Kapazität.

Für diesen Leitfaden wird die robuste Schlussfolgerung wie folgt:

```text
GPT‑6 Luna High = kleine Entwicklungsaufgaben und Codex-Worker unter enger menschlicher Kontrolle.
GPT‑6.2 Sol Medium = Codex-Standard für durchgängige agentenbasierte Entwicklung.
GPT‑6.2 Sol High = komplexe Features, Migrationen und schwierige Korrekturen.
GPT‑6.2 Astra Light = bei mangelnder Leistungsfähigkeit eskalieren, bevor du den Aufwand bei Sol pauschal maximierst.
Sonnet 5.5 Medium = kleine Entwicklungsaufgaben für Claude und klar spezifizierte agentenbasierte Aufgaben.
Opus 5.5 Medium = Claude-Standard für autonome agentenbasierte Entwicklung.
Opus 5.5 High = anspruchsvolle Architektur, schwieriges Debugging und Refactoring.
Fable 5.2 Low = Eskalation auf ein Frontier-Modell, wenn Opus High weiterhin nicht ausreicht.
Astra oder Fable = nach Kosten pro akzeptierter Änderung entscheiden, nicht nach Preis pro Token.
```

<!-- section: s-10 -->
### GPT‑6 Astra vs Claude Fable 5.2 : historischer Hinweis auf zwei Fronten

Dieses Vergleichsverfahren behält die Zahlen des GPT‑6 Astra original: für das aktuelle Routing, verwendet GPT‑6.2 Astra wenn der Kunde es anbietet. Sein kurzer Standardtarif ist $8/$40 (read cache $0.40/M) ; nicht die Ergebnisse der alten Astra zuweisen. Vergleichen Sie die aktuellen Modelle auf der gleichen Harness und dem gleichen Projektarchiv.

Vergleicht das **Modell in seinem tatsächlichen Harness**, nicht eine einzelne Editorzahl. Fable 5.2 ist durch Standardtoken billiger als GPT‑6 Astra, aber die Kostendifferenz pro Aufgabe hängt vom Caching, Aufwand, Werkzeugen und Wiederholungen ab.

| Achse | GPT‑6 Astra | Claude Fable 5.2 | Praktische Folgen |
|-----|-------------|------------------|---------------------|
| Natürliche Harness | Codex / ChatGPT Work / Responses API | Claude Code /Nachrichten API | Das gesamte System messen |
| Standardpreis Input/Output (M tokens) | **$10 / $50** | **$8 / $40** | Billiger nominal |
| Cache read (M tokens) | **$1** | **$0.20** | Tatsächlich wiederverwendeter Vorteil Fabelhaft auf Präfixen |
| Langfristiger Kontext | 1,05M ; Überlastung über 272K | 1M ; Standardtarif | Zielorientierter Kontext in beiden Fällen |
| Aufwand | Light→Ultra je nach Oberfläche ; API low→max | low→max; adaptive thinking | Fable `high` für eine lange Autonomie, `low` für eine punktuelle Stellungnahme |
| Computer use | Mit Orchester und Werkzeugen widerstandsfähig | Starke Editorergebnisse | Reproduzierbare Szenarien überprüfen |
| Qualität des Differentials | Bewertungen mit Hebegurten Codex | FrontierCode 2.0 : 49,1 % bei bestem Aufwand, je nach Anthropic | Editorprotokolle beweisen keine allgemeine Überlegenheit |
| Unabhängigkeit der Maßnahmen | Verfügbare Bewertungen Dritter | Vals: Gleichheit mit Opus auf Terminal[Bench 4.0, Rückgang auf multimodaler Ebene | Warten Sie auf einen Vergleich Fable 5.2 /Astra mit vergleichbarem Gurt |
| ZDR | Zugelassene Kunden API | 30 Standardtage, Vertragsausnahme erforderlich | Aufgaben filtern nach Vertraulichkeitsanforderungen |
| Lange Dienstreisen | Async tools, mid-turn steering | Trick-Ermüdung, thinking in Verbindung mit der Geschichte | Schutz des Zustands, der Werkzeuge und der Abschaltungsregeln |

**Lesen Sie die Benchmarks.** Anthropic Ankündigung Fable 5.2 vor Astra auf FrontierCode 2.0, FrontierSWE v2 und OSWorld 2.1, aber es sind **Editorergebnisse**. Der Coding Agent Index von Artificial Analysis Vergleich Claude Code + Opus 5.5 à Codex + Astra zeigt einen anderen Kompromiss zwischen Erfolgsquote, Kosten und Dauer an; **nicht messen Fable 5.2**. Historischer Vergleich Fable 5.1/Astra darf nicht mehr als aktuelle Routing-Regel dienen. Die unabhängigen Ergebnisse von Vals zeigen auch, dass Fable 5.2 ist nicht systematisch besser alsOpus 5.5.

Praktische Routing-Regel:

```text
Interaktive kleine Entwicklungsaufgaben mit menschlicher Kontrolle
→ GPT‑6 Luna High oder Sonnet 5.5 Medium

Standard-Issue von Anfang bis Ende
→ GPT‑6.2 Sol Medium
→ Opus 5.5 Medium für das unabhängige Review

Schwierige Architektur, Ursachenanalyse oder Refactoring
→ Opus 5.5 High
→ GPT‑6.2 Sol Medium/High als Gegenprüfung

Sol High ist von der Leistungsfähigkeit her unzureichend
→ GPT‑6.2 Astra Light, bei Bedarf Medium

Opus High ist von der Leistungsfähigkeit her unzureichend
→ Fable 5.2 Low, bei Bedarf Medium

Dieselbe echte Frontier-Aufgabe, Wahl zwischen Astra und Fable
→ zwei Worktrees / gleiche Spezifikation / gleiche Tests
→ Gesamtkosten + menschliche Arbeitsminuten + Qualität des Diffs vergleichen
→ menschliche Entscheidung
```

Legt kein permanentes Paar mehr fest  Claude writer / Codex review      .]**Der Writer wählt sich nach Aufgabenart**: Sol 6.2 besitzt in der Regel den Standardausgang ; Opus 5.5 besitzt die Architektur, das Debugging und die vom Urteil dominierten Refactors. Die andere Familie dient als unabhängiges Rezensions- oder Herausfordereren. Die Duplizierung der beiden kompletten Bahnen ist nur für ein Bake-off oder eine wirklich grenzende Entscheidung gerechtfertigt.

<!-- section: s-11 -->
### Seite Chinesische Open-Weight-Modelle (Kimi K3, GLM‑5.2, und der Rest des Clusters)

Seit Mitte2026, hat sich eine dritte Familie nebenAnthropic undOpenAI : Modelle **chinesische Grenzebene**, die eine Agentenkodierung in der Nähe von Sonnet/Opus zu sehr niedrigen Kosten pro Token erreichen. Scala der bereits fliegt Claude Code und CodexSie sind keine Ersatzleute des täglichen Treibers, aber **einen Kostenhebel für eine bestimmte Klasse von Unteraufträgen** und einer **Souveränitätsoption** (self-host) für den sensiblen Code.

**Von Anfang an anzugebender Kategorie-Fall** : Diese Modelle sind **nicht** in derselben Kategorie wie Qwen3-Coder-Next. Qwen lokal (80B/3B Aktiv) ist wirklich auf deinem Laptop nutzbar 128 Go: Q4_K_M hinterlässt einen sehr großen Spielraum, Q5_K_M ist der beste Fehler und Q6_K bleibt lebensfähig. Q8_0 kann geladen werden, muss aber mit dem Kontext validiert werden; IntelliJ und sbt Die Kommission hat sich mit dem Vorschlag der Kommission befaßt, den die Kommission dem Rat vorgelegt hat. GLM‑5.2 (753B) und vor allem Kimi K3 (2.8T) nicht **nicht** lokal auf 128 Go: Dies sind Modelle **API** (Z.ai, Moonshot, OpenRouter) oder **Self-host auf Multi-GPU-Server**. Moonshot empfiehlt im Übrigen eine Einführung Kimi K3 auf konfigs von 64+ Beschleuniger. Lege sie daher nie in das Feld       ^ Qwen local: Sie leben im Feld ✓ API Drittanbieter oder Teamserver.

| Muster      | Editor / Zugriff                                                                                                    | Architektur                                                                                             | Hintergrund                 | Preis API (in / out /M)                | Perf-Reperte (unabhängige Maßnahmen / Editor)                                                                                             |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Kimi K3** | Moonshot ✓ API, OpenRouter (`moonshotai/kimi-k3`), Kimi Code CLI; **vollständiges Gewicht veröffentlicht** unter Lizenz Kimi K3 | MoE 2.8T insgesamt **104B aktiviert** ; 896 Sachverständige, 16 aktiviert; KDA + Achtung Residuals, natives Sehen    | Bis 1M nach Plan | **$3 / $15** (cache-hit input $0.30)  | Editor-Scores mit max. Anstrengung und mit mehreren Harness; ausgezeichnete frontend und langhorizontale Signale, zu bestätigen auf Scala                   |
| **GLM‑5.2** | Zhipu/Z.ai API OpenAI- **und Anthropic-kompatibel**, GLM Coding Plan ; Checkpoint MIT veröffentlicht                      | MoE **753B** BF insgesamt16 ; Aktive Zahl nicht offiziell dokumentiert; Sparse passt  ✓ IndexShare | 1M                       | **$1.40 / $4.40** (input cache $0.26) | Editor-Scores: SWE-bench Pro **62.1**, Terminal-Bench 2.1 81.0 mit Endstation-2 und 82.7 beste Harness; Vergleich mit identischem Protokoll |

**Denkanstoß.** GLM‑5.2 stellt fest **Hoch** und **Max**. Kimi K3 stellt fest `reasoning_effort: low | high | max`. Die Vorlagenseite/API zeigt **`max` Standard**, während Kimi Code je nach Version und Plan einen anderen Fehler definieren kann: setzt daher immer explizit den Aufwand in einem Benchmark oder einer Automatisierung fest. 1M hängt vom Plan ab: 256K auf Moderno, bis 1M über Allegretto und darüber. Für eine kurze interaktive Aufgabe, beginnt bei `low` oder `high` ; Reserve `max` lange Dienstreisen, bei denen die Kosten für die Ausreise gerechtfertigt sind.

<!-- section: s-12 -->
#### Wo sie in die *Ton* Routing

```text
✅ Reviews in großer Zahl und Triage mit geringem Risiko → GLM‑5.2 (High): deutlich günstiger pro Token als Opus, Kosten pro Aufgabe aber messen
✅ Extraktion, Klassifizierung und viele PR-Zusammenfassungen → GLM‑5.2 oder Kimi K3, im Batchbetrieb, wenn Sonnet/Terra bei hohem Volumen zu teuer werden
✅ Frontend-Erstellung / Web-Mock-up → Kimi K3 (#1 Frontend Code Arena), wenn du über reines Scala hinausgehst
✅ Unabhängige Zweitmeinung eines Open-Weight-Modells → ein Modell aus einer 3. Trainingsfamilie hilft gegen gemeinsame blinde Flecken von Claude/GPT
✅ Sensibler Code / isolierter Betrieb / Datensouveränität → GLM‑5.2 selbst hosten (MIT-lizenzierte Gewichte): Nichts verlässt deine Infrastruktur
```

```text
❌ Scala-Alltagsmodell als Ersatz für Sonnet 5.5: leistungsfähig, aber du verlierst das Ökosystem (Claude Code, Subagenten, ausgereiftes Metals MCP)
❌ Kurze interaktive Aufgabe mit maximalem Aufwand auf Kimi K3: Latenz und Ausführlichkeit machen das unrentabel. low/high verwenden
❌ Kritische Architekturentscheidung mit nur einem Modell: Bei Opus/Fable bleiben oder eine echte Zweitmeinung von Sol einholen. Das Open-Weight-Modell bleibt eine Gegenstimme und entscheidet nicht allein
❌ Qwen lokal „ersetzen“: falsche Kategorie (siehe Stolperfalle oben)
```

<!-- section: s-13 -->
#### Gelegentlicher Zugang zu GLM über OpenRouter

Fügt für diesen Workflow kein spezielles GLM-Abonnement hinzu. **GLM bleibt ein Rettungsmodell**, anrufen OpenRouter wenn Claude Code, Codex und Qwen Lokale Probleme konnten nicht gelöst werden. Dadurch wird die Vielfalt der Modelle erhalten, ohne ein neues Konto, einen neuen Schlüssel und einen neuen Plan hinzuzufügen.

Wenn GLM ein Werkzeug wird, das jede Woche verwendet wird oder einen messbaren Gewinn für eine Task-Klasse bringt, dann neu bewertet das Interesse an einem direkten Zugriff Z.ai. Solange diese Schwelle nicht erreicht ist, ist Einfachheit prime.

<!-- section: s-14 -->
#### Der Rest des Clusters (zu ermitteln, nicht für alles zu übernehmen)

`MiniMax M3` (Juni 2026) ist das erste Open-Weight, das Grenzkodierung kombiniert, Kontext 1M *und* native Multimodalität (open-weight Header auf SWE-bench Pro bis 59.0 vorne GLM‑5.2). `DeepSeek V4` ein V absetzt4 Pro und V4 Flash (= $)$0.14/$0.28 /M) unschlagbar auf das lange Verhältnis Kosten/Kontext für Massensortierung. Keiner ist überall am besten   ✓: die Open-Weight-Szene von Mitte-2026 ist ein enger Cluster, wo die richtige Wahl von der Aufgabe und vom Preis abhängt, nicht von einer globalen Rangliste.

<!-- section: s-15 -->
#### Zwei Reserven, die im Auge behalten werden müssen

1. **Herkunft und Destillation.** Kimi K3 hat sich in mindestens einem berichteten Austausch als "Claude ✓" identifiziert. Diese anekdotische Selbstkennzeichnung **ist kein Nachweis für Destillation** und lässt keine wissenschaftlichen oder vertraglichen Schlussfolgerungen über Trainingsdaten zu. Wenn die Herkunft für einen Kunden zählt, erfordert eine Dokumentation des Herausgebers und verarbeitet die Informationen als unbekannt, bis sie veröffentlicht wird.
2. **Benchmark-Methode.** Die Editortabellen vermischen verschiedene Harness (KimiCode, Claude Code, Codex, Mini-SWE-Agent) und K3 ist anfällig für die Erhaltung der Geschichte der *thinking*. Die angezeigten Abweichungen sind oft niedriger als ein Punkt: sie überleben nicht immer eine Änderung der Harnesen. unveränderte Regel: **Bake-off kontrolliert auf deine wirklichen Aufgaben** (festgestellte Versionen, feste Erlaubnisse, deterministische Akzeptanztests, Kosten durch akzeptierte Änderung), keine Annahme auf den Glauben einer Rangliste.

<!-- section: s-16 -->
#### Bake-off-Protokoll Scala: Kimi K3 gegen GLM‑5.2

Vergleicht nicht nur die endgültigen Antworten. Benutzt mindestens **15 private Aufgaben[**, die nie veröffentlicht wurden, aufgeteilt auf:

```text
3 schwer erkennbare Scala-3-Bugs: Givens, Implicits, Varianz, opake Typen
3 Weiterentwicklungen in Play / Tapir / Pekko über 3 bis 8 Dateien
3 Aufgaben zu Spark / Nebenläufigkeit / Performance
3 PR-Reviews mit bekannten, gezielt eingebauten Fehlern
3 Testaufgaben: ScalaTest, ScalaCheck, Mutation Testing
```

Protokoll: Auch commit, auch worktree initial, gleiche Werkzeuge, gleiche Zeitlimit, gleiches Netzwerk, gleiches Kontextpaket, gleiche Stoppkriterien und **drei Wiederholungen pro Auftrag**. Kimi muss separat getestet werden `high` und `max`; GLM in `High` und `Max`. Wenn die Gurte nicht identisch sein können, veröffentlicht zwei Matrizen und weist die Abweichung nicht allein auf das Modell zurück.

Verbindliche Maßnahmen:

```text
- Aufgabe durch Tests und menschliches Review akzeptiert
- Kompilierung, gezielte Tests, Mutation Score
- erkannte Sicherheitsmängel oder Vertragsverletzungen
- hinzugefügte / entfernte Zeilen und betroffene Dateien
- Anzahl der Anläufe, Toolaufrufe und wiederkehrenden Schleifen
- Tokens für Eingabe, Cache, Reasoning und Ausgabe
- API-Gesamtkosten, Latenz und menschliche Arbeitsminuten bis zum Merge
- Erfolgsquote pass@1 und Stabilität über drei Durchläufe.
```

Adopte GLM oder Kimi auf einem Stream nur, wenn es die Kosten pro akzeptierter Änderung reduziert ** ohne** Verschleierung der Watches. Ein höherer Editor-Score, aber mehr menschliche Korrekturen ist eine Regression, kein Gewinn.

<!-- section: s-17 -->
## Regel der Entscheidung nach Aufgaben

<!-- section: s-18 -->
### Wenn **Fable 5.2** (Mythos-class) angewendet wird

Fable 5.2 Zweimal Opus 5.5 von token ($8/$40 gegen $4/$20). Anthropic empfiehlt, mit **Opus 5.5 `medium`**, nach `high`, dann buchen Fable 5.2 , die noch nicht ausreichend sind oder den richtigen langen Horizont erreichen. Für eine Eskalation der Kapazität, testet **Fable `low`** bevor Sie systematisch Opus zu drücken `Extra`/`Max` :

```text
✅ Vollständige Migration eines Frameworks (Play 2 → 3, Pekko, Spark-Upgrade)
✅ Autonome Sitzung über mehrere Stunden oder Tage ohne Aufsicht
✅ Modulübergreifendes Refactoring in > 10 voneinander abhängigen Dateien
✅ Debugging eines fachlichen Fehlers, dessen Ursache weit vom sichtbaren Symptom entfernt ist
✅ Architekturentscheidung ohne „offensichtlich richtige Antwort“ nach einem Versuch mit Opus 5.5 High
✅ Aufgabe, für die du sonst einen halben Tag Arbeitszeit eines Senior Engineers bezahlen würdest
```

```text
❌ Klar abgegrenzte Aufgabe: Sonnet 5.5 oder Opus 5.5 sind wirtschaftlicher
❌ Diff-Review oder PR-Zusammenfassung: unverhältnismäßig und unnötig teuer
❌ Boilerplate oder Fixtures erzeugen: Qwen oder Haiku reichen aus
❌ Einzeiler oder gezielter Patch: Luna High, Sonnet 5.5 Medium oder Aider
❌ Schwierige, aber interaktive Aufgabe mit menschlicher Kontrolle: Opus 5.5 Medium/High reicht meist aus
```

> **Positionierung 5.2.** Anthropic empfiehlt die Aufbewahrung **Opus 5.5 als Ausgangspunkt** für die meisten
> workloads. Fable 5.2 `low` ist ein pünktlicher **Advisor**, der auf einer begrenzten und nachprüfbaren Aufgabe zu bewerten ist; für eine Mission
> tatsächlich selbstständig, beginnt mit `high`, um vorzeitige Dreharbeiten zu reduzieren. Messen Sie die [**]Kosten durch Änderung
> akzeptiert** auf dem privaten Benchmark Scala, anstatt die Ergebnisse des Anbieters zu verallgemeinern.
> $0.20/M verbessert die Sparbarkeit der stabilen langen Präfixe. Wenn der Prüfer zuverlässig ist, testet auch das Schema
> **Low → Retry High auf Versagen** einschließlich Wiederholungen, Latenz, Reviews und humaner Validierung.

<!-- section: s-19 -->
### Prompting Fable 5.2: Strukturieren Sie eine lange Mission

Fable 5.2 (fenster) 1M, Ausfahrt bis 128K) ist nicht nur ein stärkerer Opus. Er zielt auf die anspruchsvolle Argumentation und den langen Horizont ab, wenn die Opus-Bewertungen unzureichend sind. Die Kontinuität der Thinking-Blocks und die Stabilität der Werkzeugdefinitionen werden zusätzlich zu den konfigurierbaren Bemühungen durch eine Nachricht zu Lasten des Harnesses. Referenz: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2`Die folgenden Hebel gelten weiterhin für 5.2 ; die Punkte, die 5.2 (Code-Eigentum, Über-Delegierung, vorzeitige Touren, historische append-only, geerbten Anweisungen zu reinigen) sind in der Notiz Fable 5.2 der Fachgruppengruppe Ü Seite Anthropic ».

Fünf spezifische Hebel:

1. **Missionscharte an der Spitze des Kontextes, versteckt.** Der anfängliche Block (objektiv, nicht objektiv, invariant, Stoppregeln) darf sich nie zwischen den Türmen ändern: er profitiert vom schnellen Caching und dient als Anti-Drive-Anker auf langen Sessions. Alles, was sich entwickelt (Status, Fehler, Diffs) geht danach.
2. ** Expliziter Dauerzustand.** Bei einer Mehrstundenmission erfordert das Modell eine Statusdatei (`MIGRATION_STATE.md` im Worktree), die an jedem Meilenstein aktualisiert wird: bearbeitete Module, verbleibende Module, getroffene Entscheidungen, Blockaden. Diese Datei ist nicht die Konversation, die im Falle von Kontextkompakte oder Wiederaufnahme verbindlich ist.
3. **Checkpoints mit Ausgabekriterium.** Die Mission wird durch deterministische Befehle in nachprüfbare Meilensteine unterteilt (`compile`, gezielte Tests, scalafmtCheckAll). Kein Übergang zum nächsten Meilenstein ohne grün fließenden Meilenstein.
4. **Straße die Anstrengung durch Drehung ohne Änderung des Modells.** Verwende `medium/high` für die Exploration, `xhigh/max` für eine wirklich schwierige Entscheidung, dann `low/medium` für eine mechanische Bearbeitung. Permessage macht den Cache aufrecht und vermeidet die Zahlung des maximalen Niveaus während der gesamten Flugbahn.
5. **Falls eine Kompaktheit erforderlich ist, schreibt deren Zusammenfassungsvertrag vor.** Bittet darum, ausdrücklich Probleme und Auflösungen, versuchte oder ausgegrenzte Spuren, Entscheidungen und Einschränkungen, aktueller Zustand, offene Punkte und schwer zu rekonstruierende Details zu bewahren. Die Serverkompakte verwaltet bereits diese Notwendigkeit; für eine Client-Seitenkompakte fasst ohne diese Felder niemals einen freien Prosa zusammen.

Missionsraum Fable 5.2:

```text
# AUFTRAG (statisch — während der Sitzung nicht ändern)
Ziel: [konkrete Migration / konkretes Refactoring]
Nicht-Ziele: [was ausdrücklich außerhalb des Umfangs liegt]
Invarianten: öffentliche APIs, JSON-Verträge, in AGENTS.md aufgeführtes Verhalten
Maximale Laufzeit: [N Stunden] — Maximale Kosten: [N USD] — Maximaler Diff je Meilenstein: [N Zeilen]

# ABBRUCHREGELN (statisch)
Sofort stoppen und Bericht erstatten, wenn:
- du nur vorankommst, indem du eine Invariante verletzt;
- derselbe Meilenstein 2 Mal aus unterschiedlichen Gründen scheitert;
- build.sbt, eine DB-Migration oder ein öffentlicher Vertrag geändert werden muss;
- die geschätzte Restdauer mehr als 2x so hoch ist wie die ursprüngliche Schätzung.

# ABLAUF (statisch)
1. AGENTS.md und MIGRATION_STATE.md lesen.
2. EINEN Meilenstein bearbeiten: kurzer Plan → Diff → Kompilierung → gezielte Tests.
3. MIGRATION_STATE.md aktualisieren und den Meilenstein committen.
4. Fortschrittsbericht: abgeschlossener Meilenstein, verbleibende Meilensteine, neue Risiken, Abweichung vom Plan.
5. Bei 2. fortsetzen.

# STATUS (dynamisch — aktuelle Fassung von MIGRATION_STATE.md beifügen)
[Status]
```

> **Kontinuität Fable 5.2.** Nicht still eine Sitzung zurücksetzen: Fable 5.1 und Opus 5.5 nicht wiedergeben
> thinking blocks von Fable 5.2. Schreibe auch keine alten Nachrichten, das Systempräfix oder die Werkzeugliste
> durch Wiederverwenden dieser Blöcke: Die Konsistenzprüfung kann einen Fehler verursachen 400. Wenn eine Änderung von Werkzeugen oder
> Vorlage ist unerlässlich, sichern Sie den nützlichen Zustand in `MIGRATION_STATE.md`, und gehen Sie dann mit einem eigenen Kontext.
> `tool_choice: any/tool` ist auf Fable 5.2 verboten; verwendet `auto` und bestätigt das Ergebnis mit einem strengen Schema.

> **Betriebsnote[**: Ein Sicherheitswippe kann das tatsächlich ausgeführte Modell ändern.
> Krypto-Code oder niedrige Sicherheit, logge dieses Modell, überprüft, ob es die erwartete und geplante Kapazität zu halten
> Dieses Verfahren wird in der Regel nicht in der Sitzung entdeckt, sondern in der Regel beendet.

<!-- section: s-20 -->
### Wenn **Opus 5.5**

Es ist das **Fehler Claude Code für den autonomen agentic coding**. Seine Standardanstrengung ist `medium`, was das Routing im Vergleich zu Opus ändert 5 : beginnt mit `medium`, steigen Sie zu `high` wenn die Aufgabe schwierig ist, dann verwendet `Extra` (`xhigh`) oder `Max` wenn die Dauer oder die Werte dies rechtfertigen.

```text
✅ Vollständige Bearbeitung eines Issues, wenn Claude den gesamten Ablauf steuert: Erkundung → Patch → Tests
✅ Architektur, Migration und Planung über mehrere Module
✅ Vom Symptom weit entfernte Ursache, schwierige Implicits/Givens/Effekte
✅ Umfangreiches Refactoring, bei dem die Stimmigkeit des Gesamtsystems wichtiger ist als einzelne Änderungen
✅ Unabhängiges Review eines von Codex erstellten PRs
✅ Koordination lesender Subagenten mit isoliertem Kontext
```

```text
medium → Standardeinstellung für agentenbasierte Arbeit
high   → schwieriges Debugging, anspruchsvolle Architektur oder langwierige Aufgaben
Extra  → >30 min und wirklich aufwendige Abfolge; nicht für eine lediglich „wichtige“ Aufgabe
Max    → Ausnahmefall mit höchster Priorität für Qualität und nachgewiesenem Nutzen
```

<!-- section: s-21 -->
### Wenn **Sonnet 5.5**

Die beste Wahl Claude, wenn **der Senior hält die Hand stark** oder wenn die agentische Aufgabe genau angegeben ist. Anthropic empfiehlt ausdrücklich `medium` für den agentischen Coding und den Multistep-Einsatz gut eingerahmter Werkzeuge, dann `high` für längere oder schwierige Aufgaben.

```text
✅ Kleiner reproduzierbarer Fehler
✅ Klar abgegrenztes lokales Refactoring
✅ Gezielte fachliche Tests und Eigenschaftstests
✅ Stacktrace → Diagnose → Korrektur
✅ Klar umrissenes Feature, dessen Architektur bereits feststeht
✅ Implementierungs-Worker nach einem Plan eines Menschen oder von Opus
```

```text
low    → einfache Transformation / geringe Latenz hat Vorrang
medium → Standard für kleine Entwicklungsaufgaben und klar spezifizierte agentenbasierte Entwicklung
high   → längere oder anspruchsvollere Aufgabe
Extra / Max → nur bei nachgewiesenem Vorteil in deinen Evaluierungen; sonst auf Opus 5.5 wechseln
```

Die wirtschaftliche Regel ist daher nicht mehr ✓ Sonnet mit maximaler Anstrengung vor Opus     ✓. Wenn Sonnet High für eine Kapazitätsgrenze fehlschlägt, **Opus Medium[** ist oft ein besserer Kauf als ein verlängerter Sonnet Extra/Max.

<!-- section: s-22 -->
### Wenn **Haiku 5.5**

Systemisch für Aufgaben *hohe Häufigkeit und geringes Risiko[*:

```text
✅ Lesende Subagenten oder Extraktion mit geringem Risiko (überprüfbare Ausgabe)
✅ Log-Zusammenfassungen und schnelle PR-Zusammenfassungen
✅ Klassifizierung und Routing
✅ Gezielte Änderungen < 20 Zeilen
✅ Commit-Nachrichten verfassen
✅ Wiederholte Aufrufe mit geringem Risiko, wenn der Benchmark den Vorteil bestätigt
```

> **Haiku 5.5 ersetzt Haiku 4.5 Wie Worker Claude.** Es kostet **$0.10/$0.50** wie der Schnelle
> bleibt unter 100 000 tokens (cache read $0.01/M) oder **dix fois moins que Haiku 4.5** und die gleiche Preisfolge wie
> GPT‑6 Luna ; über [100K tokens hinaus, einschließlich Cache, geht der Tarif auf $0.50/$2.50. Hintergrund 1M, Ausgabe 128K,
> adaptive thinking standardmäßig und **Parameter `effort` unterstützt ([`medium` standardmäßig)**. Migrationsfalle:
> prefill gibt jetzt zurück 400, `temperature`/`top_p`/`top_k` sind zu unterlassen, `budget_tokens` ergibt 400, am
> thinking zählt in `max_tokens`, und eine [`tool_choice`] gezwungen bleibt akzeptiert, aber entfernt die Reflexion vor dem Aufruf.
> Der Tokenizer zählt ca. 30 % Tokens mehr als Haiku 4.5. Praktische Regel: Bewahrt die Subagentenverträge
> **unter 100K tokens** um in der unteren Etage zu bleiben, was die Isolationsdisziplin des Abschnitts erreicht 3.
> Haiku 4.5 bleibt aktiv, aber der Widerruf ist jetzt jederzeit möglich, wenn die übliche Ankündigung von [60 Tagen erfolgt.

<!-- section: s-23 -->
### Wenn **GPT‑6 Luna**

```text
✅ Kleine Entwicklungsaufgabe: lokale Änderung, deren Ausrichtung du steuerst
✅ Einfache Tests, Fixtures, Boilerplate, Umbenennungen und mechanische Transformationen
✅ Fundstellen, Zusammenfassungen, Logs und PR-Zusammenfassungen
✅ Worker/Subagent, dessen Ausgabe direkt überprüft wird
```

OpenAI empfiehlt, Luna bei [**]High** zu beginnen. Versuche nicht, Luna in einen Agenten zu verwandeln, der mit Extra High grenzt: Wenn die Aufgabe zweideutig oder konzeptuell wird, geht man auf Sol 6.2 um, anstatt lange Wiederholungen auf einem zu kleinen Modell zu bezahlen.

<!-- section: s-24 -->
### Wenn **GPT‑6.2 Sol**

```text
✅ Vollständiges Standard-Issue: Erkundung → Implementierung → Tests → PR
✅ Feature über mehrere Dateien oder nicht trivialer Fehler
✅ Unabhängiges Review eines von Claude erstellten PRs
✅ Abgegrenzte Migration, Kompatibilität und übergreifendes Refactoring
✅ Fundierte Zweitmeinung zu einer von Opus vorgeschlagenen Architektur
```

```text
Light       → klar spezifiziertes Issue, lokaler Patch, eindeutige Reproduktion
Medium      → täglicher Standard für agentenbasierte Aufgaben
High        → komplexes Feature, schwer auffindbare Ursache, Migration, viele Grenzfälle
Extra High  → Modell ist leistungsfähig genug, aber weitere Analyse oder Überprüfung ist wirklich nötig
Ultra       → nur wenn sich die Arbeit in unabhängige Untersuchungen aufteilen lässt
```

<!-- section: s-25 -->
### Wenn **GPT‑6.2 Astra**

```text
✅ Sol High scheitert an Leistungsfähigkeit oder Urteilsvermögen und nicht an überladenem Kontext
✅ Sicherheit, Authentifizierung, kritischer Vertrag oder Entscheidung, bei der ein falscher Ansatz mehrere Korrekturrunden kostet
✅ Durchgängiger, sehr uneindeutiger Workflow mit vielen Tools / Computer Use
✅ Punktuelle Prüfung einer weitreichenden Entscheidung mit einem Frontier-Modell
```

Beginnt mit **Astra Light**. Für eine Aufgabe, die wirklich grenzt, kann Astra Light insgesamt weniger kosten als ein extra High Sol, gefolgt von einer Erholung, weil es einen schlechten Kurs verhindert. Monte to Medium/High nur, wenn nötig; Extra High/Ultra bleiben außergewöhnlich.

<!-- section: s-26 -->
### Wann wird es angewendet? **Modus `ultra` in ChatGPT Work / Codex**

```text
✅ Untersuchung einer Legacy-Anwendung über die gesamte Codebasis hinweg
✅ Migration über mehrere Module in einem eigenen Worktree
✅ Architektur, Tests, Sicherheit und Performance parallel prüfen
✅ Refactoring in kleine PRs unterteilen
✅ Auftrag, bei dem unabhängige Teilanalysen einen echten Mehrwert bringen
```

```text
❌ Einmalanweisung wie „Schreib das sauber um“
❌ Kurze interaktive Aufgabe
❌ Schwach getestetes Repository ohne Diff-Grenze
❌ Direkte Änderung kritischer Dateien ohne validierten Plan
```

In diesem Unterabschnitt bezeichnet `ultra` den [**Multiagent-Orchestrierungsmodus des Produkts** und nicht den Aufwand [`ultra`, den einige SDK [Codex jetzt darstellen. Es ist geeignet für unabhängige Komponenten ; vermeide ihn, wenn die Agenten im selben mutbaren Zustand schreiben oder wenn nur eine langsame Operation die Aufgabe beherrscht. Bei einer legacy-Anwendung beginnt die Kartierung, die Erstellung eines Schuldregisters, die Erstellung von Charakterisierungstests und die Aufteilung in Mikro-PRs. Beginnt nicht mit dem Schreiben von Code.

Mindest-Gabelit für eine Mission `ultra`:

```text
Du arbeitest als Team aus Reviewern und Agenten an einer Scala-Legacy-Anwendung.

Zu simulierende Rollen:
- Architekt für Altsysteme;
- Scala Tech Lead;
- Reviewer für defensive Sicherheit;
- QA / Test Engineer;
- skeptischer Maintainer.

Ziel:
[konkretes Ziel]

Vorgaben:
- keine Änderung des beobachtbaren Verhaltens ohne Validierung;
- für Änderungen an build.sbt, DB-Migrationen oder öffentlichen JSON-Verträgen zunächst stoppen;
- kleine PRs mit weniger als 300 geänderten Zeilen;
- Charakterisierungstests vor dem Refactoring;
- jede Schlussfolgerung muss die geprüften Dateien nennen;
- Fakten, Hypothesen und Empfehlungen unterscheiden.

Erwartete Ausgabe:
1. Übersicht über den betroffenen Bereich;
2. Risiken;
3. Liste technischer Schulden;
4. vorrangige Charakterisierungstests;
5. Plan für kleine PRs;
6. Vorschlag für den ersten PR, ohne ihn vor Freigabe des Plans umzusetzen.
```

<!-- section: s-27 -->
## Schnelle Modellauswahl-Matrix

```text
Kleine Entwicklungsaufgabe unter menschlicher Kontrolle → GPT‑6 Luna High / Sonnet 5.5 Medium
Lesender Worker oder Triage mit geringem Risiko → Haiku 5.5 / Qwen lokal / GPT‑6 Luna
Lokaler Patch mit mittlerem Beurteilungsaufwand → GPT‑6.1 Terra Medium
Standard-Issue von Anfang bis Ende → GPT‑6.2 Sol Medium
Durchgängige Bearbeitung durch Claude → Opus 5.5 Medium
Schwieriges Feature / schwieriger Bug → GPT‑6.2 Sol High oder Opus 5.5 High je nach Aufgabe
Schwerpunkt Architektur oder Ursachenanalyse → Opus 5.5 High
Unabhängiges Review → andere Modellfamilie als der Autor, standardmäßig Medium
Nachverfolgung eines PRs durch Codex → GPT‑6.2 Sol Medium (Goal / Heartbeat / Cloud)
Sol High unzureichend → GPT‑6.2 Astra Light
Opus High unzureichend → Fable 5.2 Low
Lange sequenzielle Aufgabe > 30 min → Opus 5.5 Extra (`xhigh`)
Parallelisierbare Arbeit über die ganze Codebasis → GPT‑6.2 Sol Ultra, besonders bei leseintensiven Aufgaben
Höchste Frontier-Anforderungen → Astra Medium+ / Fable Medium+ bei nachgewiesenem Bedarf
```

Praktische Regel:

```text
Der Senior steuert die Arbeit → schnelles und kostengünstiges Modell.
Der Agent steuert den gesamten Ablauf → Sol 6.2 oder Opus 5.5.
Das Verständnis ist wichtiger als der eigentliche Patch → Opus bevorzugen.
Die durchgängige Ausführung ist entscheidend → Sol 6.2 bevorzugen.
Das Modell stößt an seine Leistungsgrenze → Astra Light oder Fable Low, bevor du den Aufwand beim schwächeren Modell maximierst.
Ultra nur bei mehreren wirklich unabhängigen Teilproblemen.
```

<!-- section: s-28 -->
## Automatisches Routing von Entwicklungsaufgaben

Die Auswahlmatrix darf nicht nur manuell bleiben. Um zu vermeiden, dass Credits auf einfachen Aufgaben verbrannt werden oder umgekehrt, eine kritische Aufgabe an ein zu schwaches Modell zu senden, fügt einen expliziten Routing-Schritt vor jeder agentiellen Aufgabe hinzu.

Das Prinzip ist nicht, das intelligenteste Modell zu wählen, sondern das kleinste Modell, das mit einem akzeptablen Risiko ein messbares Ergebnis erzielen kann.

```text
Anfrage / Ticket / Stacktrace
→ Aufgabe klassifizieren
→ Schwierigkeit + Risiko einschätzen
→ kleinstes geeignetes Modell auswählen
→ mit begrenzten Berechtigungen ausführen
→ deterministische Tests ausführen
→ bei Fehlschlag eskalieren
→ Kosten / Qualität protokollieren
```

<!-- section: s-29 -->
### Empfohlene Architektur

```text
CLI / IDE / Ticket
→ task-classifier
→ context-builder
→ model-router
→ agent-runner
→ test-runner
→ reviewer
→ Kosten- und Qualitätsprotokoll
```

| Komponente          | Rolle                                                         | Empfohlenes Modell / Werkzeug                                                                             |
|--------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `task-classifier`  | Aufgabe, Risiko und Schwierigkeit ordnen                 | **Jev** wenn der Ausgang geschlossen ist; Qwen lokal / Haiku, wenn eine offene Argumentation erforderlich ist         |
| `context-builder`  | Finden Sie nützliche Dateien, Beziehungen, Tests, Dokumente und Befehle | SourcebotScalaSemantic MCPCodebase-Memory MCP wenn polyglotte, rg, IntelliJ, Metals MCP, Context7   |
| `model-router`     | Wählen Sie das kleinste akzeptable Modell                      | Deterministische Regeln + Jev als probabilistisches Signal; OpenRouter nur für pünktliche Eskalation  |
| `agent-runner`     | Mit den richtigen Berechtigungen ausführen                         | Codex, Claude Code Subagenten, Aider, OpenCode, Qwen Code                                              |
| `test-runner`      | Deterministische Validierung                              | sbt, IntelliJ, Metals MCP, CI                                                                         |
| `reviewer`         | Lesen ohne zu schreiben                                           | Gegen den Writer: Opus 5.5 Medium oder GPT‑6.2 Sol Medium ; Astra/Fable nur so kritisch |
| `cost-quality log` | Messen Sie Kosten, Qualität, Rücksendungen Bewertung und Wiederholungen            | Lokale Skripte, Follow-up-Tabelle                                                                      |

<!-- section: s-30 -->
### Jev: decision layer, non coding model

**[Jev 1.14 [`jev-1.14.0`** ist das aktuelle System One-Modell von TypeSafe AI. Es erzeugt weder Text noch Code: es erhält eine `state` und typisierte Fragen und gibt dann direkt probabilistische Entscheidungen zurück. Das richtige mentale Modell ist ein ** smart if Ÿberzeugt** : Offener Eintrag, vom Entwickler definierte Zweige.

| Primär | Verwendung                                                           |
|-----------|-----------------------------------------------------------------|
| `Choice`  | wählen Sie aus geschlossenen Optionen: Modell, Agent, Skill, Straße |
| `Score`   | auf einer geordneten Skala zu beachten: Risiko, Relevanz, Priorität   |
| `Noul`    | Einschätzung der Wahrscheinlichkeit, dass ein Vorschlag wahr ist            |

Jev 1.14 Kosten **$0.042/M tokens input** Die Standardregelung akzeptiert **64K tokens pro Anfrage** und **32K für `state` + die längste Frage** ; die Durchflussgrenzen hängen von der Organisation ab und werden in der Konsole gelesen. Ein längerer experimentellen Kontext und Bildeingänge existieren unter Bedingungen, ohne dass der Router zum Fehler wird. `jev-latest` Richtung `jev-1.14.0` : **Stecken Sie Version** Sobald Sie Schwellenwerte stufen, da die Änderung der Verteilung die Risikoschwellen ungültig machen kann.

> **OpenAI Entscheidungen API.** Endpoint `POST /v1/decisions`, jetzt in der Regel verfügbar auf `gpt-6-luna`, avec
> Typische Antworten `predicate`, `choice` und `score`. Bis **400 Fragen** können einen gleichen Eintrag teilen; Text,
> Strukturierte Bilder und Daten werden nach dem Feld unterstützt. Standardpreis: **$0.10/M tokens**, **$0.01/M
> Tokens aus gelesenem Cache**, keine Ausgaberechnung; Cache-Buchungen, lange Eingaben und Verarbeitungen
> Die Preise für Regionalbeihilfen sind in den einzelnen Regionen unterschiedlich. `task-classifier` und `model-router`, verglichen mit Decisions und Jev über die gleichen
> Fragen mit einer Kalibrierung pro Aufgabe und Risiko, nie auf dem einzigen Preis des Token.

In diesem Workflow sind die besten Kandidaten:

```text
✅ Aufgaben, Risiken und Schwierigkeitsgrade klassifizieren
✅ Modelle zuweisen: Luna / Sol / Astra / Sonnet / Opus / Fable
✅ Schrittweise passende Skills aus einem großen Katalog auswählen
✅ Ergebnisse von Subagenten sichten und die Relevanz von Kontext bewerten
✅ Themenwechsel erkennen und signalisieren, ob eine Kontextkomprimierung sinnvoll wäre
✅ Benachrichtigungen filtern und Entscheidungen markieren, die menschliche Aufmerksamkeit erfordern

❌ Scala-Code schreiben oder erklären
❌ Offene Architekturfragen und Ursachenanalysen
❌ Berechnungen, Zählungen oder Vergleiche von Datumsangaben
❌ Allein über Push, Deployment, Löschung, Secrets oder DB-Migration entscheiden
```

Empfohlene Architektur:

```text
Deterministische Regeln
→ Jev für häufige Entscheidungen mit klar abgegrenzten Optionen
→ Code kombiniert Wahrscheinlichkeiten + Schwellenwerte
→ generatives LLM bei offener Analyse oder zu niedriger Konfidenz
→ Mensch bei kritischen oder irreversiblen Aktionen
```

**Typ-Safe  ✓ okay.** Das Argument "zero Halluzinationen" bedeutet vor allem, dass Jev nicht aus einer Struktur oder einer Reihe von deklarierten Optionen heraus; es kann immer die falsche Option auswählen. **346 009 Abfragen / 37 Datasets** die Wahrscheinlichkeit `Choice` • die Berücksichtigung der wirtschaftlichen, sozialen und wirtschaftlichen Auswirkungen der Umstrukturierung der Wirtschaft; `0.5` ist schlecht für einige Binäraufgaben: Schwellen müssen **nach Aufgaben und Risiken maßgeschneidert**.

Drei Regeln für die Integration:

1. **Der Code behält die Autorität.** Deterministische Signale (`touches_security`, kritische Datei, zerstörerische Aktion) immer Vorrang vor Jev.
2. **Minimaler Zustand.** Jev wird auch er *Kontext rot* ; Filter vor dem Aufruf und nur die Entscheidung, die tatsächlich ändert.
3. **Teste die Stabilität.** Über `Choice`, die Optionen pünktlich neu ordnen; `jev-1.13` signalisieren eine mögliche Empfindlichkeit gegenüber der Bestellung, die auf `jev-1.14.0`. Le `state` adversarial kann auch die Antwort beeinflussen: Jev ist ein Signal, keine Sandbox.

<!-- section: s-31 -->
### Mindesteinstufung

Der Router muss eine strukturierte Entscheidung produzieren, keine freie Antwort. Beispiel für den erwarteten Ausgang:

```json
{
  "task_type": "implementation | debug | test | review | migration | architecture | boilerplate | research",
  "risk": "low | medium | high | critical",
  "difficulty": "trivial | simple | normal | hard | frontier",
  "expected_files": "1 | 2-5 | 6-10 | 10+",
  "requires_code_write": true,
  "requires_external_docs": false,
  "touches_public_api": false,
  "touches_json_contract": false,
  "touches_database": false,
  "touches_build": false,
  "touches_security": false,
  "touches_concurrency": false,
  "model": "qwen | haiku55 | sonnet55 | opus55 | fable52 | gpt6_luna | gpt61_terra | gpt62_sol | gpt62_astra | gpt61_sol | gpt6_astra",
  "reasoning_effort": "light | low | medium | high | extra | xhigh | max | ultra | null",
  "reasoning_mode": "standard | pro | null",
  "multi_agent": false,
  "max_parallel_agents": 3,
  "max_cost_usd": 0.0,
  "max_duration_minutes": 0,
  "confidence": 0.0,
  "escalation_rule": "string",
  "stop_conditions": [
    "string"
  ]
}
```

**Signalhierarchie** : Deterministische Kriterien (`touches_*`, `expected_files`, diff Größe erwartet) sind die Auslöser *Primär* Routing und Klettern. Wenn Klassifizierung kommt von **Haiku/Qwen**, `confidence` reste une auto-estimation secondaire et mal calibrée. Si elle vient de **Jev**, verwendet Verteilung und `confidence` zurück, aber mit einem **nach Frage und Risikoniveau maßgeschneiderte Schwelle**nie ein `0.75` In beiden Fällen darf ein hohes Vertrauen niemals *Deklination* ein kritisches deterministisches Signal.

`reasoning_effort` muss nach Oberfläche standardisiert werden: Claude verwendet `low | medium | high | xhigh | max` über kompatible Modelle, mit **Opus 5.5 und Haiku 5.5 `medium`** Standard , Codex Poster **Light | Medium | Hoch | Extra High | Ultra**, während dieAPI OpenAI legt Werte `low | medium | high | xhigh | max` je nach Modell. `multi_agent` Der Aufwand ist ein Hebel von Qualität und Kosten, aber ein höheres Tier mit geringer Anstrengung kann insgesamt billiger sein als ein niedrigerer, nach oben getriebener Tier.

<!-- section: s-32 -->
### Automatische Routing-Matrix

| Signal erkannt                                               | Ursprüngliches Modell                | Klettern                                                                      |
|--------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------|
| Zusammenfassung, Sortieren, Grep, einfache Logs                           | Haiku 5.5 / Qwen              | Sonnet 5.5 Medium si ambigu                                                   |
| Boilerplate, DTO, Fixierungen, mechanische Bearbeitung                | GPT‑6 Luna Hoch               | Sonnet 5.5 Medium wenn subtile Arten/Domain                                    |
| Einfacher oder nicht-reagierender Test lokalisiert                      | GPT‑6 Luna Hoch               | Sonnet 5.5 Medium wenn wichtige Gewerberegel                                  |
| Ziel-Patch, menschliche Führung                       | Luna High / Sonnet 5.5 Medium | Sol 6.2 Light/Medium, falls erforderlich                                |
| Begrenzte Patch mit Zwischenurteil                      | GPT‑6.1 Terra Medium           | GPT‑6.2 Sol Medium, falls erforderlich |
| Begrenzte Gewerbefeature, 1 bis 5 Dateien                        | GPT‑6.2 Sol Medium            | Sol High wenn schwierig; Opus Medium review                                |
| Feature 5 bis 10 Dateien mit Invarianten                      | GPT‑6.2 Sol Medium/High       | Opus 5.5 High wenn Architektur/Root Ursache dominiert                               |
| Bug Scala subtil, Implizit, Givens, Effekte                  | Opus 5.5 Hoch                 | Hochboden für unabhängige Hypothese; Fable Low wenn Kapazität unzureichend     |
| Migration von bornierten Multimodulen                               | GPT‑6.2 Sol Hoch              | Opus High en review ; Astra Light, wenn Oberboden                             |
| Refactor Base-scale-Code                                      | Opus 5.5 Hoch                 | Extra so lang-horizontal; Fable Low wenn Opus-Obergrenze                            |
| Review einer PR Codex                                        | Opus 5.5 Medium               | Hoch bei kritischem Risiko                                                       |
| Review einer PR Claude                                       | GPT‑6.2 Sol Medium            | High dann Astra Light wenn Risiko grenzen                                      |
| Unabhängige Überwachung einer PR Codex                               | GPT‑6.2 Sol Medium            | High so schwierig Diagnose; Sol 6.1 Medium wenn 6.2 nicht verfügbar             |
| Sicherheit / auth / kritischer Vertrag                           | GPT‑6.2 Astra Light + human    | Astra Medium/High + Review Opus High                                          |
| Unabhängige read-heavy Achsen                                 | GPT‑6.2 Sol Ultra             | Astra Ultra nur, wenn zusätzliche Kapazität wirklich benötigt wird |
| Änderung `build.sbt`, Abhängigkeiten, DB, Vertrag JSON öffentlich | Kein Selbstschreiben           | Plan + Humanvalidierung                                                     |

<!-- section: s-33 -->
### Eskalationspolitik

Das automatische Routing muss wie ein kontrollierter Wasserfall funktionieren:

```text
Überprüfbare Mikroschleife: Qwen / Haiku / GPT‑6 Luna High / Sonnet 5.5 Medium
→ durchgängige Verantwortung beim Agenten: GPT‑6.2 Sol Medium / Opus 5.5 Medium
→ anspruchsvolle Aufgabe: Sol High / Opus High
→ Grenze der Leistungsfähigkeit: Astra Light / Fable Low
→ höherer Aufwand nur, wenn das Modell leistungsfähig genug ist, aber die Analyse nicht ausreicht
→ Ultra nur bei parallelisierbarer Arbeit
→ Mensch
```

**Ändere nicht einfach das Modell inmitten einer verwirrenden Unterhaltung.** Wenn das Scheitern von einer verschmutzten Bahn kommt Ÿ wiederholte falsche Annahme, Halluzinationen, die sich sammeln, Korrekturen, die andere Fehler erstellen › der Kontext ist selbst ein Teil des Problems. Sonnet 5.5 → Opus 5.5, Sol 6.2 → Astra oder Opus 5.5 → Fable 5.2 :

```text
1. Schreibmodus stoppen.
2. HANDOFF.md erstellen: Ziel, Stand des Diffs, überprüfte Fakten, fehlgeschlagene Versuche, aktueller Fehler und offene Fragen.
3. Neue Sitzung nur mit Spezifikation + AGENTS.md + HANDOFF.md + relevanten Dateien/Diffs starten.
4. Wenn die Schwierigkeit es weiter rechtfertigt, in der neuen Sitzung auf ein stärkeres Modell wechseln.
```

Die Eskalation von **Kapazität** ist nützlich für ein eigentliches Problem; sie darf die Gesprächsschuld nicht von einer bereits verzerrten Sitzung tragen.

Steigen Sie automatisch, wenn:

```text
- ein kritisches deterministisches Signal liegt vor (sensible touches_*-Felder, Diff außerhalb der Vorgaben);
- vom LLM selbst angegebene Konfidenz < 0.75 oder Jevs Konfidenz unter dem kalibrierten Grenzwert für diese Entscheidung;
- derselbe Kompilierungsfehler tritt 2 Mal auf;
- gezielter Test schlägt nach 2 Korrekturen weiterhin fehl;
- Diff liegt außerhalb des Arbeitsumfangs;
- mehr Dateien geändert als vorgesehen;
- mehr als 300 unerwartete Diff-Zeilen;
- build.sbt, plugins.sbt, eine DB-Migration oder ein öffentlicher JSON-Vertrag ist betroffen;
- öffentliche API wurde geändert;
- der Router erkennt Risiken bei Sicherheit, Nebenläufigkeit, Performance oder Geld;
- das Modell meldet ausdrücklich hohe Unsicherheit;
- die geschätzten Fehlerkosten übersteigen die Kosten eines stärkeren Modells.
```

Unterbrechungen (ohne automatisch klettern) wenn:

```text
- max_cost_usd ist erreicht (lokales Budget);
- max_duration_minutes ist erreicht (Zeitlimit nach verstrichener Echtzeit):
  Eine agentenbasierte Sitzung, die in einer Schleife steckt, ist eine andere Fehlerart als eine gescheiterte Sitzung.
  Der Wechsel zu einem teureren Modell löst die Schleife nicht auf.
```

Automatisch deklicken, wenn:

```text
- rein textliche Aufgabe;
- kein Schreibmodus erforderlich;
- kein fachliches Risiko;
- weniger als 20 Zeilen erwartet;
- nur eine Datei;
- deterministisches Ziel;
- vorhandener, sehr gezielter Test;
- stabiler und im Projekt bereits bekannter Kontext.
```

<!-- section: s-34 -->
### Regeln für die Nichtautomatisierung

Lassen Sie nie einen Router entscheiden, eine Schrift auf:

```text
- build.sbt;
- plugins.sbt;
- resolvers;
- Abhängigkeitsversionen;
- DB-Migrationen;
- öffentliche JSON-Verträge;
- Sicherheit;
- Authentifizierung;
- Autorisierung;
- Nebenläufigkeit;
- Geldverwaltung;
- Datenlöschung;
- Deployment- oder Infrastrukturskripte.
```

In diesen Fällen kann der Router nur Folgendes vorschlagen:

```text
- empfohlenes Modell;
- Plan;
- voraussichtlich betroffene Dateien;
- auszuführende Tests;
- Risiken;
- Abbruchregel.
```

<!-- section: s-35 -->
### Empfohlene Subagenten Claude Code

**Kalibrierung Codex 6.2.** Für einen Elternteil GPT‑6.2 Sol oder Astra, geh mit dem gleichen Modell und der gleichen Anstrengung für Subagenten (offizielle Empfehlung OpenAI) Dann kümmere dich um die tatsächlich mechanischen Aufgaben mit kontrollierter Ausgabe: Luna/Haiku für Grap, Extraktion, Logs und Zusammenfassungen; Sol/Opus für Invarianten, Architektur und Root Ursache. Das gleiche Messprinzip gilt für Claude. Ein Reviewer der anderen Familie bleibt eine unabhängige Sitzung, kein billiger Worker des Autors.

Claude Code ist der beste Ort, um dieses Routing auf den Alltag anzuwenden, da Subagenten ihren eigenen Kontext, ihre Werkzeuge und ihre Berechtigungen haben können.

```text
researcher
- Modell: Haiku / Qwen, wenn extern
- Modus: nur lesend
- Rolle: Dateien, Verwendungen, Tests und Dokumentation finden

scala-implementer
- Modell: Sonnet 5.5 `medium`
- Modus: Schreibzugriff auf das Repository begrenzt
- Rolle: abgegrenzte Aufgaben nach einem klaren Plan umsetzen

hard-debugger
- Modell: Opus 5.5 `high`
- Modus: begrenzter Schreibzugriff, Plan erforderlich
- Rolle: subtile Scala-Fehler, Implicits, Effekte und schwer auffindbare Ursachen

migration-planner
- Modell: Opus 5.5 `high`; Fable 5.2 `low` (einzelne Entscheidung) oder `high` (langer Auftrag), wenn Opus an seine Grenzen stößt
- Modus: erst planen, eigener Worktree
- Rolle: modulübergreifende Migrationen, längere Refactorings und Strategie zur Aufteilung
- Hinweis: Dynamic Workflows (Opus 5.5 + viele parallele Subagenten) prüfen
  als Alternative zum Einsatz eines einzelnen Fable-Agenten bei Migrationen über die gesamte Codebasis

reviewer
- Modell: Codex / GPT‑6.2 Sol `medium`; Astra `light` bei kritischen Aufgaben
- Modus: kein Schreibzugriff
- Rolle: unabhängiges Review, Einstufung als blockierend / wichtig / optional

pr-summarizer
- Modell: Qwen / GPT‑6 Luna
- Modus: kein Schreibzugriff
- Rolle: PR-Zusammenfassungen, Release Notes, abschließende Checkliste
```

<!-- section: s-36 -->
#### Kontextisolation: Hauptrolle von Subagenten bei langen Aufgaben

Der Gewinn der Subagenten ist nicht nur Parallelität. **Fenster mit frischer und isolierter Umgebung** ; der Elternteil braucht daher keine Suchanfragen, Logs, entfernte Dateien und Sackgassen aus jeder Unteraufgabe zu sammeln. Diese Isolierung schützt den Hauptkontext vor dem *Kontext rot*.

Die empfohlene Aufteilung ist:

```text
HAUPTAGENT
- Ziel
- Vorgaben und Nicht-Ziele
- validierter Plan
- getroffene Entscheidungen
- aktueller Diff
- wesentliche Belege
- offene Risiken

SUBAGENTEN
- zahlreiche Dateien erkunden
- Suche mit Sourcebot / rg
- Aufrufpfade, Hierarchien, Verwendungen und Given-Ketten über ScalaSemantic
- sprachübergreifendes Strukturdiagramm über Codebase-Memory, wenn Java/Kotlin/Scala gemeinsam vorkommen
- Typen / Givens / Diagnosen live über Metals untersuchen
- externe Dokumentation
- umfangreiche Logs und Testsuiten
- Übersicht über ein Legacy-Modul
```

Entscheidungsregel:

```text
Sind die Details dieser Teilaufgabe nach ihrem Abschluss noch für den Hauptagenten relevant?

NEIN → isolierter Subagent
JA → im Kontext des Hauptagenten behalten
```

Die Übertragungsnachricht muss ein **Vertrag** sein, da der Subagent nicht von der gesamten Geschichte des Elterngesprächs abhängig sein darf:

```text
Auftrag:
[genauer Umfang]

Modus:
nur lesend / begrenzter Schreibzugriff

Untersuche:
[genaue Fragen]

Nicht bearbeiten:
[außerhalb des Umfangs]

Gib nur Folgendes zurück:
1. Schlussfolgerung;
2. Belege im Format file:line;
3. relevante Tests oder Befehle;
4. verbleibende Unsicherheiten.

Zielumfang: < 1–2K Tokens.
```

Die Rücksendung ist eine Schnittstelle, keine Transkription. Wenn ein Subagent 80K tokens liest und zurückgibt [1,5]K, ist die Isolierung nützlich; wenn er 10K liest und 8K zurückgibt, hat er vor allem das Geräusch verschoben. Eine einfache Metrik für lange Aufgaben ist:

```text
isolation_ratio
= vom Subagenten verbrauchte Tokens
/ an den Hauptagenten zurückgegebene Tokens
```

Der richtige Pattern ist also **map → reduce** : plusieurs workers spécialisés dépensent du contexte localement, puis le parent synthétise quelques résultats courts. Évite l'anti-pattern inverse — sept agents qui lisent chacun le repo et renvoient des rapports de dix pages — qui recrée le *Kontext rot* im Wurzelkontext.

Für **ton workflow solo Scala** behandelt das Fan-out auch als Budget für Tokens/Quoten:

```text
Standard                          → 1 aktiver Agent
2 unabhängige Untersuchungen      → 2 rein lesende Subagenten
2 unabhängige User Stories        → anfangs höchstens 2 implementierende Agenten (WIP zählt PRs im Review mit)
3+ parallele Sitzungen            → nur bei gemessenem Vorteil und nachgewiesener Review-Kapazität
Implementierung                   → stets nur 1 Agent pro Branch / PR / Worktree
```

Logge mindestens `parallel_sessions_peak`, `subagent_count` und `subagent_tokens`. Ein Subagent schützt den Kontext des Elternteils, lädt aber seinen eigenen Kontext auf: Er ist also niemals kostenlos        ✓. Wenn er keine nützliche Isolierung oder wirklich parallele Arbeit bringt, startet er ihn nicht.

Für die Koordination bevorzugt ** Sterntopologie[**: Der Elternteil überträgt unabhängige Verträge und fasst die Rückkehrer zusammen. Vermeidet Teams, in denen die Agenten frei miteinander reden, eine E-Mailbox teilen oder sich selbst einen mutbaren Status zuteilen. In diesem Leitfaden muss der Koordinator ein einfacher ** Delegator bleiben**, kein soziales System von Agenten.

> **Orchestrierung Claude Code** : **Agent View** dient der Überwachung mehrerer Sitzungen und Aufgaben;
> **Agent Teams** ermöglicht die Zusammenarbeit zwischen den Gremien , bleibt jedoch experimentell . **Ultrareview** ist eine Cloud-Review
> Multiagent en research preview. **Remote Control** ermöglicht die Überwachung einer lokalen Sitzung von einem anderen Gerät aus
> während die Ausführung und die MCP auf der lokalen Maschine. Diese Oberflächen ergänzen die Subagenten; sie nicht
> ändern
> nicht die Regel ✓ nur ein Writer von worktree ✓.

> **Mod `You should know` (2.1.287+)** : `cc-plugin-you-should-know` startet eine Side Agent während langer Aufgaben
> und zeigt die Elemente, die du oder Claude vermissen könntest, über dem Schnellen an. Es ist ** standardmäßig deaktiviert[** und
> sťactive via `/plugin enable cc-plugin-you-should-know@builtin`. Behandle es als opportunistisches Wachsignal,
> nie wie ein unabhängiger Reviewer, ein Orakel oder ein Gate: seine Bemerkungen müssen noch mit einem Beweis verbunden werden,
> einen nachprüfbaren Test oder Diff.

> **Claude Code 2.1.27x: Feinere Isolierung.** Seit 2.1.277, ein Subagent benutzerdefiniert oder von einem Plugin zur Verfügung gestellt kann
> Erklärung `omitClaudeMd` nicht laden `CLAUDE.md` Benutzer, Projekt und Lokal; die Politik verwaltet
> • die Veröffentlichung der Ergebnisse der Studie über die Entwicklung der Forschung und Entwicklung in der Europäischen Gemeinschaft;
> bereits den gesamten Kontext erforderlich. Die gleiche Version ermöglicht es, `allowed_domains` an einen Befehl zu binden
> Bash/PowerShell/Monitor: Die Netzwerköffnung gilt für diesen Befehl, nicht für die gesamte Sitzung. Dies ** bestätigt[**
> und
> Mindestanforderungen an Subagent ✓ und Mindestberechtigungen pro Teilaufgabe
> Projektkontext für einen Implementer, der es braucht.
>
> Seit 2.1.278, verwendet der Auto-Modus standardmäßig ein **Serverseite klassifizieren** auf kompatiblen Flächen und
> Anthropic
> gibt an, dass diese Klassifizierung keine Klassifizierungskosten hinzufügt; `/status` gibt an, ob `Auto mode server` aktiv ist.
> Dies reduziert ein overhead Routing, nicht die Anforderungen an die Genehmigung oder review. Schließlich, Plugins und Skills
> werden selbst zu testbaren Artefakten: `claude plugin eval` (2.1.269) führt eine Reihe von scored-Evaluierungen aus
> und reproduzierbar mit Ausgang JSON/HTML, während `/skill-doctor` hilft, beladene, aber unnötige Skills zu erkennen.
> Eine dauerhafte Änderung von Plugin oder skill muss daher durch eval + review vor der Promotion gehen.
>
> Die folgenden Versionen fügen zwei zusätzliche Werkzeuge hinzu, um das Driften der Harnesen zu vermeiden. Seit **2.1.283**,
> `/doctor prompt-audit` (alias `/checkup prompt-audit`) oudite `CLAUDE.md`, skills, Agenten und Befehle zur Identifizierung
> und
> Anweisungen, die veraltet oder widersprüchlich geworden sind, nachdem die Modellgeneration geändert wurde.
> nicht-interaktiv, **`--bare`** wird jetzt als Mittel zum Starten eines Mindestgurtes dokumentiert: nicht
> Selbst-Discovery von Hooks/Plugins/MCP/Speicher/Anweisungen und seit [2.1.286 nur Server MCP
> Namen sind verbunden, ohne Systemrückrufe oder Hintergrundaufgaben. Benutze `--bare` für **Evals und Skripte
> reproduzierbar**, nicht als Standard-Tagesmodus.

<!-- section: s-37 -->
### OpenRouter für das gelegentliche Routing API

In **dieses Solo-Workflow** braucht das Haupt-Routing keinen Gateway API. Die fünf täglichen Pfade haben bereits ihre eigene Oberfläche und ihr eigenes Budget:

```text
Claude Code        → Claude-Max-Abonnement
Codex              → ChatGPT-Abonnement
Qwen lokal         → MLX / llama.cpp / lokaler Endpunkt
GitHub Copilot     → GitHub-Copilot-Abonnement
JetBrains AI       → JetBrains-AI-Abonnement
```

Notwendigkeit API Rest ist **Ausnahme** : wenn Claude Code und Codex bleiben blockiert und wollen eine Meinung aus einer anderen Familie von Modellen, zum Beispiel **GLM, Kimi, Gemini, Grok oder ein neues Modell zu bewerten**. In diesem Fall **OpenRouter ist der beste Fehler** : nur ein Schlüssel, kein Server zu halten, schneller Zugriff auf viele Modelle und Vorseher, zentrale Rechnungsstellung und Verfügbarkeit Fallback.

```text
Anhaltende Blockade
→ den mindestens nötigen Kontext extrahieren
→ OpenRouter
   ├── GLM
   ├── Kimi
   ├── Gemini
   ├── Grok
   └── neues Modell für einen Test
→ die Analyse mit Claude / Codex vergleichen
→ der Mensch entscheidet
```

**Fahren Sie nicht automatisch die tägliche Arbeit in Richtung OpenRouter.** Die Wahl des Rettungsmodells muss explizit bleiben: Ziel ist es, eine andere Perspektive zu erhalten, nicht, einen Router still wählen zu lassen, eine andere Familie zu wählen.

<!-- section: s-38 -->
#### Fallbacks: Vorschau ja, Vorlage nicht standardmäßig

OpenRouter kann automatisch zwischen den Vorgesetzten wechseln. Für diesen Leitfaden, unterscheidet zwei Ebenen:

```text
Gleiches Modell, Anbieter A nicht verfügbar
→ gleiches Modell, Anbieter B
→ JA: ausfallsicher, ohne die Art des Reviews zu ändern

GLM nicht verfügbar
→ Gemini
→ Kimi
→ Grok
→ standardmäßig NEIN: Ein Modellwechsel muss sichtbar und beabsichtigt bleiben
```

Für eine technische Untersuchung, also logge immer **das tatsächlich verwendete Modell**. Ein Fallback zwischen Modellen kann den Grund für die Abweichung einer Schlussfolgerung von Claude oder Codex.

<!-- section: s-39 -->
#### Qwen local : Bleib direkt

Nicht hinzufügen OpenRouter nur zur Vereinheitlichung Qwen. `llama.cpp`, MLX oder das lokale Harness können bereits ein Endpoint OpenAISolange es nur ein oder zwei lokale Modelle gibt, bringt die zusätzliche Schicht nicht genügend Wert:

```text
Qwen lokal
→ llama-server / MLX
→ Qwen Code / OpenCode / lokales Skript
```

<!-- section: s-40 -->
#### Vertraulichkeit mit einem Aggregator

Über OpenRouter zugängliche Vorseher können unterschiedliche Haltungsrichtlinien haben. Für sensiblen Berufscode:

```text
- standardmäßig nie das gesamte Repository senden;
- einen minimalen reproduzierbaren Fall, einige Typen oder Methoden, den Stacktrace und den gezielten Test bevorzugen;
- den fachlichen Kontext nach Möglichkeit anonymisieren;
- gezielt Anbieter wählen, die die Vorgaben des Projekts zur Datenaufbewahrung erfüllen;
- besonders sensiblen Code lokal oder bei bereits genehmigten Direktanbietern behalten.
```

<!-- section: s-41 -->
### Zu loggende Metriken

Der Router muss auf reale Daten eingestellt werden, nicht auf Intuition. Für jede agentielle Aufgabe, Blog:

```plaintext
task_type
risk
difficulty
decision_layer
decision_confidence
decision_threshold
decision_overridden
model_used
effort_level
fallbacks
parallel_sessions_peak
subagent_count
subagent_tokens
input_tokens
output_tokens
cost_usd
duration
files_changed
diff_lines
tests_run
tests_passed
review_findings
human_rework
merged_or_reverted
time_to_deploy
human_active_minutes
review_queue_minutes
review_true_positives
review_false_positives
review_missed_defects
quota_consumed_by_role
production_regressions
rollback_or_hotfix
```

Nach zwei Wochen werden die Schwellenwerte angepasst:

```text
- wenn Qwen bei einer Aufgabenart oft scheitert, weise sie direkt Sonnet zu;
- wenn Sonnet eine Aufgabenart ohne Review-Rückmeldungen bewältigt, vermeide Opus;
- wenn Opus die Korrekturschleifen stark verkürzt, behalte es für diese Aufgabenart bei;
- wenn Opus `xhigh/max` dort ausreicht, wo du bisher Fable eingesetzt hast, gehe auf Opus zurück;
- wenn Fable die menschliche Nacharbeit nicht verringert, setze es nur für wirklich lange Sitzungen ein;
- wenn `max` nur optionale Anmerkungen findet, gehe auf `high` oder `medium` zurück.
```

<!-- section: s-42 -->
### Minimale Router-Prompt (Generativer Fallback)

Doch. Jev ist verfügbar und dass die Ausgänge geschlossen sind, bevorzugt `Choice` / `Score` / `Noul` Die folgenden Quittungen sind nützlich, wenn eine offene Argumentation erforderlich ist oder als Vergleichsbasis verwendet wird.

```text
Du weist Softwareentwicklungsaufgaben für ein Scala/Java/Play/Spark-Projekt geeigneten Modellen zu.

Analysiere die folgende Anfrage und gib ausschließlich gültiges JSON aus.

Ziel: Wähle das kleinste Modell, das bei vertretbarem Risiko ein merge-fähiges Ergebnis liefert.

Berücksichtige:
- Aufgabenart;
- Schwierigkeit;
- fachliches Risiko;
- wahrscheinliche Größe des Diffs;
- wahrscheinliche Anzahl betroffener Dateien;
- Bedarf an Schreibzugriff;
- Bedarf an externer Dokumentation;
- Scala-spezifische Risiken: Implicits, Givens, Effekte, JSON-Serialisierung;
- kritische Dateien und Themen: build.sbt, DB-Migrationen, Authentifizierung, Sicherheit, Nebenläufigkeit und Geld;
- Modell, Reasoning-Aufwand und bei Bedarf Modus `pro` oder mehrere Agenten (`ultra` in der Produktoberfläche);
- Kosten- und Laufzeitgrenze;
- Eskalationsregel;
- Abbruchbedingungen.

Deterministische Signale (kritische Dateien, Diff-Größe) haben Vorrang vor deiner eigenen Konfidenz.

Anfrage:
[ANFRAGE EINFÜGEN]

Verfügbarer Kontext:
[DATEIEN, STACKTRACE, DIFF-STATISTIK ODER ZUSAMMENFASSUNG EINFÜGEN]
```

<!-- section: s-43 -->
### Leitprinzip des Routing

```text
Der Router sucht nicht nach dem intelligentesten Modell.
Er wählt das kostengünstigste Modell, das einen merge-fähigen Diff liefern kann.
Bei steigendem Risiko oder wachsender Unsicherheit greift eine explizite Eskalationsregel.
```

<!-- section: s-44 -->
## Auswirkungen auf den monatlichen Haushalt

*(Richtwert ab Tarifen) API Standard; Abonnement und Quote konvertieren nicht mechanisch in Dollar API)*

| Muster              |           Preis API input/output / M | Volumenempfehlung                                                                          |
|---------------------|------------------------------------:|---------------------------------------------------------------------------------------------------|
| Qwen lokal          |                                   0 | Voranalyse und sichere Aufgaben nach Volumen                                                             |
| **Jev 1.14**        | **$[$0.042/M input ; kostenloses Output** | Decision layer: Klassifizierung, Routing, Scoring und Auswahl von Hochfrequenz-Skills        |
| **GPT‑6 Luna**      |                   **$0.10 / $0.50** | Micro-dev Codex, Workers, Sortieren, einfache Tests                                                   |
| **Haiku 5.5**       |                   **$0.10 / $0.50** | Subagent, Sortieren; Schritt ×5 wenn input > 100K ; mass `medium` konfigurierbar                        |
| **GPT‑6.2 Sol**     |                        **$2 / $10** | Fehler Codex agentisch; ausgezeichnete Leistung vor Astra                                 |
| **Sonnet 5.5**      |                        **$2 / $10** | Mikro-Dev-Fehler Claude `medium` für agentic coding genau spezifiziert                              |
| **Opus 5.5**        |                        **$4 / $20** | Mangel an Claude agentique bei `medium`; `high` bei schwierigen Aufgaben                             |
| **GPT‑6.2 Astra**   |                        **$8 / $40** | Kapazität Klettern; Starten Sie bei Light                                                          |
| **Fable 5.2**       |                        **$8 / $40** | Frontier Claude ; Starten Sie bei Low bei einer Kletterkapazität                                 |
| Extra / Max / Ultra |                            Variable | Nur nach Maß verwenden: Mehr Aufwand bedeutet nicht mehr Kosten pro abgeschlossene Aufgabe |

> **Der Preis pro Token ist nicht TCO.** Bewertung auch Fable 5.2 `low` auf begrenzte und nachprüfbare Aufgaben: es kann weniger pro gelöste Aufgabe kosten
> dass ein niedrigeres Modell, das mehr sucht, relitiere und backtracke; umgekehrt, Opus 5.5 `medium` kann die
> • die gleiche Qualität wie Fable auf bestimmten Workloads für einen Bruchteil der Kosten.
> **Kosten durch akzeptierte Änderung**, Wiederholungen und menschliche Minuten.

<!-- section: s-45 -->
## Regel gegen Kreditverbrennungen

Werfen Sie nicht. Fable 5.2, GPT‑6.2 Astra, Opus 5.5 `Extra/Max` oder einen Modus `Ultra` teuer nur, wenn Sie liefern können:

```text
- konkretes Ziel;
- Vorgaben;
- voraussichtlich betroffene Dateien oder Module;
- Akzeptanzkriterien;
- auszuführende Tests;
- Nicht-Ziele;
- ausdrückliche Grenze für den Diff;
- Kosten- und Laufzeitgrenze;
- Abbruchregel.
```

Ein sehr starkes Modell auf einer schnellen Unschärfe produziert kein gutes Ergebnis: es erzeugt eine teurere Drift.

> **Vollstreckbare Mittel statt Disziplin allein.** Mehrere Einstellungen Claude Code verwandeln diese Regel in
> Sicherung: `maxEffortLevel` begrenzt den Aufwand auf alle Vorgesetzten; eine Deny-Regel, die auf einen Werkzeugparameter zielt
> (z. B. `Agent(model:opus)` untersagt, einen Subagenten auf ein teures Modell zu werfen; `CLAUDE_CODE_SUBAGENT_MODEL`
> legt das Modell der Subagenten fest; `fallbackModel` listet bis zu drei geprüfte Faltmodelle in der Reihenfolge (bis
> Protokollieren, siehe oben) ; `/usage` unterteilt den Verbrauch nach skill, subagent, plugin und server MCP ; und
> hooks sehen die aktuelle Anstrengung über `$CLAUDE_EFFORT`. Seite API, die **task Budget[** (beta
> `task-budgets-2026-03-13`, `output_config.task_budget`) geben dem Modell einen Token-Budget für die gesamte Schleife
> agentic: es ist ein **vorwahl**, nicht eine Obergrenze, die mit `max_tokens` und einer Obergrenze verdoppelt werden muss
> Client-Seite ; sein Wert ist Teil des Quick-Rendering, so ändern Sie es bricht den Cache. Überprüfen Sie die Liste in der Doc
> der unterstützten Modelle, bevor sie auf Fable 5.2 oder Opus 5.5 verwendet werden.

<!-- section: s-46 -->
#### Vor-Flight-Checklist vor jeder Aufgabe > $2 geschätzter Kosten

Vor dem Starten Fable 5.2, GPT‑6.2 Astra, Opus 5.5 mit hohem Aufwand oder einer Multiagent-Sitzung, bestätigt diese Checkliste. Jedes nicht markierte Feld ist ein Grund, NICHT zu starten und in ein Modell oder ein Scope zurückzukehren.

□ Zielsetzung 1 Satz mit Aktionsverb □ Nicht-erläuterte Ziele (mindestens 2) □ Betroffene Dateien/Module (genaue Pfade) □ Prüfbares Akzeptanzkriterium □ Gezielter Testbefehl bereit ausgeführt werden □ Diff maximal zulässig festgelegt (z.B.: < 300 Zeilen) □ Feste Kostenobergrenze (z.B. $5) und die Dauerobergrenze (z.B.: 30 min) □ Urteil des Gerichts erster Instanz (Stopp, wenn [Bedingung]]) □ Der Plan wurde von Menschen vor dem Write-Modus validiert □ Dedizierte Worktree erstellt, wenn die Aufgabe > berührt 5 Dateien □ Mindestsituation vorbereitet (keine "alle Wiederholung")

Schnelle Kostenschätzung (in der Größenordnung):

| Aufgabe               | Muster      | Geschätzte Tokens      | Geschätzte Kosten |
|---------------------|-------------|---------------------|-------------|
| Feature 3 Dateien  | Sonnet 5.5  | ~20K in / ~5K out   | ~$0.09      |
| Multimodul-Bug   | Opus 5.5    | ~50K in / ~10K out  | ~$0.40      |
| Migration framework | Fable 5.2   | ~200K in / ~50K out | ~$3.60      |
| Astra-Audit max     | GPT‑6.2 Astra | ~100K in / ~20K out | ~$1.60      |

Wenn die geschätzten Kosten 3x die Kosten des niedrigeren Modells für dieselbe Aufgabe übersteigen, muss die Qualitätsdifferenz durch das Risiko gerechtfertigt werden. "Intelligenter" ist keine Rechtfertigung.
---

