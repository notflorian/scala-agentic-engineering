<!-- section: chapter -->
# 10B. OpenRouter como alternativa puntual

Para el flujo de trabajo actual, **no es necesario ninguna gateway local** : OpenRouter sólo sirve como puerta de salida a los modelos de emergencia. Crea una llave dedicada, fija un límite de gasto lado cuenta y selecciona explícitamente el modelo a probar.

```text
Claude Code / Codex bloqués
→ préparer un reproducer minimal
→ OpenRouter
→ choisir volontairement GLM / Kimi / Gemini / Grok
→ conserver le nom du modèle et du provider dans le journal de tâche
```

El principio es voluntario simple: **OpenRouter no se convierte en el camino normal de desarrollo**. Claude Code, Codex, Qwen local, GitHub Copilot y JetBrains AI continúan utilizando sus superficies nativas.

> Estado de la carretera Gemini.** Google cerró el acceso
> gratuit/Pro/Ultra en Gemini CLI el 18 Junio 2026 ; su sucesor Antigravity CLI es closed-source con una cuota
> gratis muy reducido (orden de magnitud: ~20 Las solicitudes/día) ya no cuentan con un tercer agente gratuito.
> Google: para un aviso Gemini en solución de problemas, la vía racional sigue siendo elAPI o OpenRouter, lo que esta sección
> Lección general para todo el stack: nunca construyas un flujo de trabajo en una cuota gratuita
> Desaparecer en el trimestre.

<!-- section: s-1 -->
## Configuración mínima

Una sola variable de entorno es suficiente para los scripts o herramientas que utilizan OpenRouter :

```bash
export OPENROUTER_API_KEY="..."
```

Por una integración Scala puntual, mantén la misma exclusión `LlmClient[F[_]]` que en la sección 7A e inyecta una configuración dedicada:

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

El cliente conserva entonces un endpoint OpenAI-compatible sin introducir un servidor local adicional.

<!-- section: s-2 -->
## Reglas de fallback

Para esta guía:

```text
Provider fallback pour le même modèle
→ autorisé

Fallback automatique vers un autre modèle
→ désactivé par défaut
```

El cambio de provider mejora la disponibilidad sin cambiar la naturaleza del análisis. Un cambio automático del modelo rompe por el contrario el objetivo buscado: obtener conscientemente una opinión de otra familia de modelos.

<!-- section: s-3 -->
## Normas de confidencialidad

OpenRouter agregue a varios proveedores cuyas políticas pueden diferir. Para código profesional:

```text
- envoyer le minimum de contexte nécessaire ;
- préférer un reproducer, une stack trace et les fichiers strictement concernés ;
- ne jamais envoyer le repository entier par défaut ;
- anonymiser les données métier et secrets ;
- choisir explicitement les providers compatibles avec les exigences du projet ;
- garder les parties les plus sensibles en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-4 -->
## QuéOpenRouter no debe sustituir

```text
Claude Code        → agent principal raisonnement/debug + reviewer croisé via abonnement Claude
Codex              → agent principal d'exécution + reviewer croisé via abonnement ChatGPT
Qwen local         → modèle local direct
GitHub Copilot     → workflow GitHub
JetBrains AI       → assistance IDE
OpenRouter         → escalade exceptionnelle vers d'autres modèles
```

Esta separación evita transformar una simple puerta de emergencia en una nueva capa de infraestructura que se debe mantener.

---

