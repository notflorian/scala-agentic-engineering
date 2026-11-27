<!-- section: chapter -->
# 10B. OpenRouter come alternativa occasionale

Per l'attuale flusso di lavoro, precisione ** nessun gateway locale è richiesto**:OpenRouter crea una chiave dedicata, imposta un limite di spesa sul lato account e seleziona esplicitamente il modello da testare.

```text
Claude Code / Codex bloqués
→ préparer un reproducer minimal
→ OpenRouter
→ choisir volontairement GLM / Kimi / Gemini / Grok
→ conserver le nom du modèle et du provider dans le journal de tâche
```

Il principio è volutamente semplice: **OpenRouter non diventa il normale percorso di sviluppo**. Claude Code, Codex, Qwen locali, locali, GitHub Copilot e non è così JetBrains AI continuare a utilizzare le loro superfici native.

> Stato della strada Gemini.** Google accesso chiuso
> free/Pro/Ultra a Gemini CLI su 18 giugno 2026; il suo successore Antigravity CLI è open source con una quota aggiuntiva
> molto piccolo libero (dimensione ordine: ~ arrivare ~20] query/day). Non si affida più a "un terzo agente libero" side alternativa
> Google: per una recensione Gemini nella risoluzione dei problemi, il percorso razionale rimane il [[API]] o OpenRouter, che questa sezione vuole
> lezione generale per tutta la pila: non costruire mai un flusso di lavoro su una quota libera — si può pretendere
> scomparire nel corso del trimestre.

<!-- section: s-1 -->
## Configurazione minima

Solo una variabile di ambiente è sufficiente per script o strumenti che utilizzano OpenRouter:

```bash
export OPENROUTER_API_KEY="..."
```

Per favore. Scala punto di integrazione, mantenere la stessa astrazione `LlmClient[F[_]]` come in un'altra 7A e iniettare una configurazione dedicata:

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

Il client mantiene quindi un endpoint OpenAI compatibile senza introdurre un server locale aggiuntivo.

<!-- section: s-2 -->
## Regole di caduta

Per questa guida:

```text
Provider fallback pour le même modèle
→ autorisé

Fallback automatique vers un autre modèle
→ désactivé par défaut
```

Il cambiamento di disposizione migliora la disponibilità senza cambiare la natura dell'analisi. Un cambio automatico di modello al contrario sfocia l'obiettivo ricercato: ottenere consapevolmente un'opinione da un'altra famiglia di modelli.

<!-- section: s-3 -->
## Confidentiality Regole relative

OpenRouter aggrega diversi fornitori le cui politiche possono differire. Per codice professionale:

```text
- envoyer le minimum de contexte nécessaire ;
- préférer un reproducer, une stack trace et les fichiers strictement concernés ;
- ne jamais envoyer le repository entier par défaut ;
- anonymiser les données métier et secrets ;
- choisir explicitement les providers compatibles avec les exigences du projet ;
- garder les parties les plus sensibles en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-4 -->
## Che cosa OpenRouter non dovrebbe sostituire

```text
Claude Code        → agent principal raisonnement/debug + reviewer croisé via abonnement Claude
Codex              → agent principal d'exécution + reviewer croisé via abonnement ChatGPT
Qwen local         → modèle local direct
GitHub Copilot     → workflow GitHub
JetBrains AI       → assistance IDE
OpenRouter         → escalade exceptionnelle vers d'autres modèles
```

Questa separazione evita di trasformare una semplice porta d'emergenza in un nuovo strato di infrastrutture per mantenere.

---

