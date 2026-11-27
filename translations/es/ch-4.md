<!-- section: chapter -->
# 4. Presupuesto mensual razonable y estrategia de caché

El presupuesto debe ser manejado como un presupuesto de ingeniería, no como un gasto abstracta de la IIA. La buena métrica no es el coste por mensaje, sino:

```text
coût total d'une tâche mergeable
= coût modèle + temps humain + temps CI + retours review + reprises de bugs
```

<!-- section: s-1 -->
## Presupuesto inicial realista

| Puesto                                                 |                 Presupuesto indicativo | Nota                                                                                                                                                                                    |
|-------------------------------------------------------|---------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code vía Claude Pro/Max                        |                      20 à 200+ $ | Max se justifica si Opus/Sonnet giran todos los días; el cupo se comparte entre las superficies Claude compatibles.                                                                        |
| ChatGPT con Codex                                    |                     20 $ y más | Más adecuado para el uso limitado; Pro se justifica si Sol 6.2 se convierte en un writer diario y no sólo un reviewer.                                                                        |
| JetBrains AI Ultimate                                 | ~300 $/año; 35 AI Credits / 30 j | Util para funciones de nube JetBrains y Junie; Código Completion / Next Edit Sugerencias y agentes autenticados en sus proveedores no consumen estos créditos.                     |
| GitHub Copilot                                        |                         variable | Opcional: relevante sobre todo si GitHub es el centro del flujo de trabajo issues/PR/review; ampliamente redundante como tercer gato de código.                                                      |
| OpenRouter / API puntual GLM/Kimi/Gemini/Grok      |                         0 à 50 $ | Puerta de salida excepcional cuando Claude/Codex/Qwen no son suficientes; el presupuesto voluntario es débil y límite máximo.                                                                         |
| GLM Coding Plan (Z.ai)  la segunda suscripción opcional  |                 ~18 a 160 $/mes | Forfait open-weight *conformidad* : endpoint Anthropic-compatible, se enchufe en Claude Code para absorber review/triage sin poner tus límites Claude. Lite ~18 $, Pro ~72 $, Max ~160 $. |
| Qwen local                                            |             0 $ sin electricidad | Muy bueno para pre-análisis, síntesis y boilerplate, pero no para decidir solo en código crítico.                                                                                           |
| Sourcebot, Aider, OpenCode/Qwen Code, RTK             |                     0 a variable | Muchas herramientas son de código abierto, pero el alojamiento, índices y claves API posibles cuestan.                                                                                      |
| Headroom y herramientas de compresión de contexto recientes |                     experimental | Para probar en logs/diffs no críticos antes de integrarlo en el flujo de trabajo estándar.                                                                                                         |

Total objetivo realista para uso intensivo solo: **250 à 450 $/mes**, que se ajustará después de dos semanas de medición real. 300 à 350 $ sigue siendo plausible, pero no hay que congelarlo: un solo mal bucle agente en un contexto grande puede costar más que una semana de micro-patas bien arrugadas.

<!-- section: s-2 -->
## Puntos de precios y cuotas que no deben mantenerse en la guía

Claude Code se incluye en los planes Claude de pago compatibles, pero el uso exacto depende del plan, del modelo y de los límites de sesión. Las páginas oficiales indican especialmente Claude Pro a 20 $/mes, Max desde 100 $/mes, y usos Max 5x/20x según la oferta. Por lo tanto, mantén la guía en forma de rangos, no como una verdad contable permanente.

Lado Codex, evita transformar los nombres de modelos y ajustes ChatGPT en verdad contable permanente. El enrutamiento activo de esta guía es **GPT‑6 Luna / GPT‑6.1 Terra / GPT‑6.2 Sol / GPT‑6.2 Astra**, con Sol 6.2 Medium como defecto agente. Los límites de uso, el acceso a Max/Ultra y la facturación dependen del plano, la superficie, la región y el rollout. Escribe las reglas alrededor de la **Clase de trabajo y costo por cambio aceptado**, luego comprueba la página oficial antes de industrializar un perfil o un presupuesto.

Antecedentes importantes: **Anthropic Reserva el uso por suscripción Claude Free/Pro/Max/Team/Enterprise a las aplicaciones nativas Anthropic y a los usos previstos en sus condiciones.** Desde el principio 2026, Anthropic ha prohibido explícitamente el uso de tokens OAuth de estas suscripciones en arneses de terceros o herramientas no oficiales: estos flujos deben pasar por una clave API dedicada (Claude Console o nube provider) y respetar los términos comerciales. Concretamente: Claude Code y Claude.ai para las suscripciones Claude; OpenCode/Qwen Code/Aider para Qwen locales, modelos API o llaves BYOK, sin utilizar nunca un token de sesión Claude Pro/Max en una herramienta externa.

No confundir con lo que *es* permiso: conectar Claude Code sobre el **endpoint Anthropic- Compatible con Z.ai.** con una **llave Z.ai** (GLM Coding Plan, §3) es lícito  ¡Usas la llave de un proveedor contra el endoso de ese mismo proveedor, no desvías ningún token OAuth Claude. La línea roja es el **un token de suscripción Claude** fuera de las aplicaciones Anthropic, no apuntar Claude Code a otro proveedor con su propia llave.

**Presupuesto post-PR Claude Ship.** En solitario, `/ship`, `/steward` y Cloud Auto-fix consumen el uso aplicable de Claude Code (No hay coste de VM separado para la nube Anthropic Según la documentación) ; no es gratuita la vigilancia en segundo plano. GitHub de Claude Ship (Team/Enterprise) consumen créditos de uso de la organización no incluidos en la asignación. `PR/mois × coût moyen de review × nombre de reviews par PR + corrections Steward + classifiers Approvals + CI supplémentaire`. Empieza con una revisión a petición o en la apertura, no en cada push, y fija un límite máximo mensual para Code Review y PR Steward (este último no tiene por defecto). `observe` de Approvals también puede activar reviews y clasificadores
facturado. Desactivar el uso de créditos no es suficiente para detener los agentes activos: Desactivar Approvals, luego Steward, luego Código de revisión si quieres cortar estos gastos.

**Presupuesto post-PR Codex.** `@codex review` y revisiones automáticas GitHub están sujetos a las condiciones del Código de revisión; `/review` local, Goal mode, Heartbeats y tareas Codex Cloud autenticados con tu cuenta ChatGPT utilizan las asignaciones aplicables al plano y a la superficie. No hay script de vigilancia archivado ni clave API OpenAI Para el flujo de trabajo nativo no se requiere más. Sin embargo, comprueba las cuotas, créditos adicionales y permisos efectivos: cada recuperación y corrección pueden consumir cuota, incluso sin nueva diff. Preferir un objetivo bordado o un Heartbeat corto con deducción por SHA y parada explícita; nunca los dos simultáneamente en una misma rama. `openai/codex-action` Con llave API sigue siendo una opción de CI por separado,
a reservar a las necesidades de automatización que las superficies nativas no cubren.

<!-- section: s-3 -->
## Prompt caching: palanca principal, pero para formular con precisión

Para no explotar el presupuesto, estructura las peticiones de los agentes de manera determinista:

1. Ponga el contexto estático en la parte superior: `AGENTS.md`, reglas Scala, arquitectura, convenciones de pruebas.
2. A continuación, coloca el contexto semiestático: esquemas, contratos JSON, convenios de trabajo.
3. Coloque el contexto dinámico en la parte inferior: archivos modificados, errores de compilación, logs de pruebas.
4. Evita cambiar el encabezado de prompt a cada iteración si quieres beneficiarse de la caché.

Una caché exitosa puede reducir el costo de **lectura** de tokens de entrada a alrededor de 10 % del coste input normal según los proveedores (en los modelos Anthropic corrientes: 5 % para Opus 5.5 y Sonnet 5.5, 2,5 % para Fable 5.2, 10 % para Haiku 5.5 ; 5 % para GPT‑6.2 Sol/Astra GPT‑6.1 Sol/Terra).90 % de ahorro en toda la tarea de la red: los tokens de salida, la escritura de caché, los tool calls y los errores de bucle permanecen facturados.

<!-- section: s-4 -->
## Normas contra el crédito quemado

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

**Ahorras en la doble suscripción.** Estabiliza el writer y su esfuerzo durante una trayectoria; los cambios de modelo pueden perturbar la caché y añadir rework. Un contexto fresco sigue siendo voluntario para el revisor independiente o una hipótesis contaminada. No lanza ni repaso exhaustivo sistemático sobre cada micro-patch, ni segundo steward sobre un mismo PR. Deduca el seguimiento por repo/PR/SHA/check/finding, privilegia una reanudación de eventos o un Heartbeat borné cuando la CI , y arréglalo en el checkpoint. Medición de los cupos consumidos por función y por tarea (cuando el proveedor lo expone); diferencia créditos incluidos, sobrecostos de pago y API. Una cuota todavía elevada no es motivo para abrir más tickets.

