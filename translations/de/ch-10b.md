<!-- section: chapter -->
# 10B. OpenRouter als gelegentliche Ausweichlösung

Für den aktuellen Workflow: **Kein Gateway vor Ort erforderlich** : OpenRouter dient nur als Ausgangstor zu den Notfallmodellen. Erstellt einen dedizierten Schlüssel, setzt eine Kostengrenze auf der Seite des Kontos und wählt ausdrücklich das zu testende Modell aus.

```text
Claude Code / Codex kommen nicht weiter
→ minimalen reproduzierbaren Fall vorbereiten
→ OpenRouter
→ GLM / Kimi / Gemini / Grok bewusst auswählen
→ Modell und Anbieter im Aufgabenprotokoll festhalten
```

Das Prinzip ist freiwillig einfach: **OpenRouter wird nicht der normale Weg der Entwicklung**. Claude Code, Codex, Qwen lokal, GitHub Copilot und JetBrains AI Sie benutzen ihre nativen Oberflächen weiter.

> Zustand der Straße Gemini.** Google hat den Zugriff geschlossen
> kostenlos/Pro/Ultra in Gemini CLI am 18 Juni 2026 ; sein Nachfolger Antigravity CLI ist mit einer Quote geschlossen
> Kostenlos sehr reduziert (in der Größenordnung: ~20 Abfragen/Tag). Zählt nicht mehr auf ✓ einen dritten kostenlosen Agenten  ✓ seitlich
> Google: für eine Gemini-Rezension in Fehlerbehebung, der rationale Weg bleibt die [API oder OpenRouter, was dieser Abschnitt
> sieht bereits vor. Allgemeine Lektion für den ganzen Stack: nie einen Workflow auf einer kostenlosen Quote bauen ✓ es kann
> Im Laufe des Quartals verschwinden.

<!-- section: s-1 -->
## Mindesteinstellungen

Eine einzige Umgebungsvariable genügt für Skripte oder Werkzeuge, die OpenRouter verwenden:

```bash
export OPENROUTER_API_KEY="..."
```

Für eine pünktliche Integration Scala behält die gleiche Abstraktion `LlmClient[F[_]]` wie im Abschnitt 7A und gibt eine spezielle Konfiguration ein:

```scala
import zio.*

final case class OpenRouterConfig(
    apiKey: String,
    baseUrl: String = "https://openrouter.ai/api/v1"
)

object OpenRouterConfig:
  val layer: ZLayer[Any, SecurityException, OpenRouterConfig] =
    ZLayer.fromZIO {
      for
        key <- System.env("OPENROUTER_API_KEY").someOrFail(
                 SecurityException("OPENROUTER_API_KEY manquante")
               )
      yield OpenRouterConfig(key)
    }
```

Der Client behält dann einen OpenAI-kompatibelen Endpoint ohne zusätzlichen lokalen Server.

<!-- section: s-2 -->
## Fallback-Regeln

Für diesen Leitfaden:

```text
Anbieterwechsel für dasselbe Modell
→ erlaubt

Automatischer Wechsel zu einem anderen Modell
→ standardmäßig deaktiviert
```

Die Änderung der Vorsehung verbessert die Verfügbarkeit, ohne die Natur der Analyse zu ändern. Eine automatische Änderung des Modells im Gegenteil verwirrt das Ziel: bewusst eine Meinung aus einer anderen Familie von Modellen zu erhalten.

<!-- section: s-3 -->
## Vertraulichkeitsregeln

OpenRouter fängt mehrere Vorgesetzte an , deren Politik unterschiedlich sein kann . Für Berufscode:

```text
- nur den mindestens nötigen Kontext senden;
- einen reproduzierbaren Fall, einen Stacktrace und die unmittelbar betroffenen Dateien bevorzugen;
- standardmäßig nie das gesamte Repository senden;
- fachliche Daten und Secrets anonymisieren;
- gezielt Anbieter auswählen, die die Projektanforderungen erfüllen;
- die sensibelsten Teile lokal oder bei bereits genehmigten Direktanbietern behalten.
```

<!-- section: s-4 -->
## WasOpenRouter nicht ersetzen sollte

```text
Claude Code        → Hauptagent für Analyse und Debugging + unabhängiges Gegenreview über ein Claude-Abonnement
Codex              → Hauptagent für die Umsetzung + unabhängiges Gegenreview über ein ChatGPT-Abonnement
Qwen lokal         → direkt genutztes lokales Modell
GitHub Copilot     → GitHub-Workflow
JetBrains AI       → Unterstützung in der IDE
OpenRouter         → Eskalation auf andere Modelle in Ausnahmefällen
```

Diese Trennung vermeidet es, eine einfache Nottür in eine neue Infrastrukturschicht zu verwandeln, die beibehalten werden soll.

---

