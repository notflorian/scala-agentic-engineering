<!-- section: chapter -->
# 15B. Release Engineering vom mergefähigen PR zur auslieferbaren Software

Der Merge ist nicht das Ende des Nachweises. Für einen Gewerbecode in der Produktion, verwendet eine risikogerechte Validierungskette; wandelt die Agenten nicht in Produktionsunternehmen.

```text
spec + REQ/acceptance evidence
→ implementation gate (scope, compilation, tests)
→ review gate (independent findings, final PR head)
→ integration gate (CI on the actual merge candidate)
→ release gate (immutable artifact, staging, security)
→ production gate (authorized deployment, progressive rollout)
→ runtime verification (SLO, regressions, rollback)
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
- PR et candidat d'intégration validés.
- Artefact immuable identifié, testé et promu par le pipeline autorisé.
- Staging et smoke tests passants ; rollback / récupération testés selon risque.
- Canary ou rollout approuvé ; aucune alerte ou régression au-delà des seuils.
- Fenêtre d'observation terminée ; métriques et exceptions documentées.
```

Der erste Zustand ist ✓ merge-ready ✓, der zweite in Betrieb genommene Zustand  ✓, der letzte stabile Zustand ✓. Maßt diese Zustände getrennt, anstatt den Erfolg einem Commit oder einer grünen Review zuzuordnen.

---

