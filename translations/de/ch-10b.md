<!-- section: chapter -->
# 10B. OpenRouter als gelegentliche Ausweichlösung

Für den aktuellen Workflow: **Kein Gateway vor Ort erforderlich** : OpenRouter dient nur als Ausgangstor zu den Notfallmodellen. Erstellt einen dedizierten Schlüssel, setzt eine Kostengrenze auf der Seite des Kontos und wählt ausdrücklich das zu testende Modell aus.

```text
Claude Code / Codex bloqués
→ préparer un reproducer minimal
→ OpenRouter
→ choisir volontairement GLM / Kimi / Gemini / Grok
→ conserver le nom du modèle et du provider dans le journal de tâche
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
Provider fallback pour le même modèle
→ autorisé

Fallback automatique vers un autre modèle
→ désactivé par défaut
```

Die Änderung der Vorsehung verbessert die Verfügbarkeit, ohne die Natur der Analyse zu ändern. Eine automatische Änderung des Modells im Gegenteil verwirrt das Ziel: bewusst eine Meinung aus einer anderen Familie von Modellen zu erhalten.

<!-- section: s-3 -->
## Vertraulichkeitsregeln

OpenRouter fängt mehrere Vorgesetzte an , deren Politik unterschiedlich sein kann . Für Berufscode:

```text
- envoyer le minimum de contexte nécessaire ;
- préférer un reproducer, une stack trace et les fichiers strictement concernés ;
- ne jamais envoyer le repository entier par défaut ;
- anonymiser les données métier et secrets ;
- choisir explicitement les providers compatibles avec les exigences du projet ;
- garder les parties les plus sensibles en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-4 -->
## WasOpenRouter nicht ersetzen sollte

```text
Claude Code        → agent principal raisonnement/debug + reviewer croisé via abonnement Claude
Codex              → agent principal d'exécution + reviewer croisé via abonnement ChatGPT
Qwen local         → modèle local direct
GitHub Copilot     → workflow GitHub
JetBrains AI       → assistance IDE
OpenRouter         → escalade exceptionnelle vers d'autres modèles
```

Diese Trennung vermeidet es, eine einfache Nottür in eine neue Infrastrukturschicht zu verwandeln, die beibehalten werden soll.

---

