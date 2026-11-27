<!-- section: chapter -->
# 15B. Release Engineering vom mergefähigen PR zur auslieferbaren Software

Der Merge ist nicht das Ende des Nachweises. Für einen Gewerbecode in der Produktion, verwendet eine risikogerechte Validierungskette; wandelt die Agenten nicht in Produktionsunternehmen.

```text
Spezifikation + REQ-/Akzeptanzbelege
→ Implementierungsprüfung (Umfang, Kompilierung, Tests)
→ Review-Prüfung (unabhängige Befunde, endgültiger PR-Head)
→ Integrationsprüfung (CI auf dem tatsächlichen Merge-Kandidaten)
→ Release-Prüfung (unveränderliches Artefakt, Staging, Sicherheit)
→ Produktionsprüfung (autorisiertes Deployment, schrittweiser Rollout)
→ Prüfung im Betrieb (SLO, Regressionen, Rollback)
```

**Release gate.** Nachdem das Artefakt des gelieferten Commits erbaut ist, testet dieses Artefakt, identifiziert es durch unveränderliche Verdauung (OCI-Bild, JAR-Bild, Verteilung) und promeus-es, ohne es zwischen Staging und Produktion wieder aufzubauen. Bewahrt SHA Quelle, Verdauung, Build-Versionen/Abhängigkeiten, Ergebnisse CI und, je nach Projekt, SBOM, Scans und Herkunftsnachweis. Die Einsatzidentität ist vom Writer und dem Writer getrennt. CI die unzuverlässigen Code ausführt. Kein Produktionsgeheimnis in den Agenten; temporäre Erlaubnisse und durch menschliche Gate-geschützte Umgebung oder Release-Politik.

**Canary / rollout progressive.** Auf einem kritischen Dienst, setzt auf einem reduzierten Umfang (Instanzen, Verkehr, Treiber oder Jobs) und vergleicht mit der Control-Gruppe. Vor dem Starten von metrischen, Fehler- und Latenzschwellen, Beobachtungsfenster und minimalem Volumen gesetzt; ohne ausreichendes Signal, sperrt die Förderung. Erhöht nur nach und nach, wenn die SLO und Invariants zufrieden bleiben. Für ein kleines Projekt oder einen nicht kritischen Job können Staging + smoke Tests und Rollback ausreichend sein. Kanarienvogel ist nur dann nützlich, wenn beide Versionen tatsächlich vergleichbar sind und wenn die Messung eine Regression erkennen lässt.

| Anwendung | Zu überwachende Regressionssignale |
|-------------|------------------------------------|
| Play / Tapir | 5xx, s[95/p99, Berufsfehler, Erfolgsquote |
| Pekko / Auswirkungen | mailboxes, timeouts, dead letters, ressources und sättigung |
| Spark | Volumen, Diagramme, Nullen, Partitionen, Doppelungen, Fehler, Kosten/Dauer der Jobs |
| JVM | heap, GC, Threads, CPU |
| Datenbank | Fehler, Locks, Latenz, Integrität, Migration |

Strukturierte Log-Instrumente, metrische und Spuren (OpenTelemetry wenn angepasst). Correle Service/Version/digest und Einsatzveranstaltung. Senden Sie weder PII noch Geheimnisse in logs/LLM. Legen Sie die Abschaltungskriterien und den Zwangsvollstrecker fest; wenn eine Schwelle überschritten wird, stoppen Sie die Beförderung, Rollback über die genehmigte Pipeline oder deaktivieren Sie die Funktion, und öffnen Sie dann einen Vorfall und ein Korrektur-Ticket. Lassen Sie einen Agenten die Produktion nicht direkt korrigieren.

**Rollback.[** Bewahrt das neueste gesunde Artefakt, ein geprüftes Verfahren, Deaktivierungs-Flags und Wiederherstellungsnachweise. Eine zerstörerische DB-Migration oder eine irreversible Schrift wird nicht durch die Umschreibung eines JAR aufgehoben: nutzt expand/contract, Bottom-up-Kompatibilität/absteigende Kompatibilität während des Rollouts, erprobte Backup/Wiederherstellung und Daten-Versöhnungsplan. Für Spark bevorzugt man vor der Beförderung idempotent, wiederspielbar und isolierte Ausgänge. Der Mensch validiert unumkehrbare Vorgänge.

<!-- section: s-1 -->
### Definition von Done auf der Produktionsseite

```text
- PR und Integrationskandidat sind validiert.
- Unveränderliches Artefakt ist identifiziert, getestet und von der autorisierten Pipeline weitergereicht.
- Staging und Smoke-Tests erfolgreich; Rollback und Wiederherstellung wurden entsprechend dem Risiko getestet.
- Canary oder Rollout ist freigegeben; keine Warnmeldungen oder Regressionen oberhalb der Grenzwerte.
- Beobachtungsfenster beendet; Metriken und Ausnahmen sind dokumentiert.
```

Der erste Zustand ist ✓ merge-ready ✓, der zweite in Betrieb genommene Zustand  ✓, der letzte stabile Zustand ✓. Maßt diese Zustände getrennt, anstatt den Erfolg einem Commit oder einer grünen Review zuzuordnen.

---

