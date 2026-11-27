<!-- section: chapter -->
# 10B. OpenRouter como alternativa puntual

Para el flujo de trabajo actual, **no es necesario ninguna gateway local** : OpenRouter sólo sirve como puerta de salida a los modelos de emergencia. Crea una llave dedicada, fija un límite de gasto lado cuenta y selecciona explícitamente el modelo a probar.

```text
Claude Code / Codex bloqueados
→ preparar una reproducción mínima
→ OpenRouter
→ elegir deliberadamente GLM / Kimi / Gemini / Grok
→ registrar el nombre del modelo y del proveedor en el historial de la tarea
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
Proveedor alternativo para el mismo modelo
→ autorizado

Cambio automático a otro modelo
→ desactivado por defecto
```

El cambio de provider mejora la disponibilidad sin cambiar la naturaleza del análisis. Un cambio automático del modelo rompe por el contrario el objetivo buscado: obtener conscientemente una opinión de otra familia de modelos.

<!-- section: s-3 -->
## Normas de confidencialidad

OpenRouter agregue a varios proveedores cuyas políticas pueden diferir. Para código profesional:

```text
- enviar el mínimo contexto necesario;
- preferir una reproducción, una traza de ejecución y solo los archivos pertinentes;
- nunca enviar todo el repositorio por defecto;
- anonimizar datos de negocio y secretos;
- elegir explícitamente proveedores compatibles con los requisitos del proyecto;
- mantener las partes más sensibles en local o con proveedores directos ya aprobados.
```

<!-- section: s-4 -->
## QuéOpenRouter no debe sustituir

```text
Claude Code        → agente principal de razonamiento y depuración + revisor cruzado con la suscripción de Claude
Codex              → agente principal de ejecución + revisor cruzado con la suscripción de ChatGPT
Qwen local         → modelo local directo
GitHub Copilot     → flujo de trabajo de GitHub
JetBrains AI       → asistencia en el IDE
OpenRouter         → escalado excepcional a otros modelos
```

Esta separación evita transformar una simple puerta de emergencia en una nueva capa de infraestructura que se debe mantener.

---

