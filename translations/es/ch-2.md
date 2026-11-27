<!-- section: chapter -->
# 2. Stack recomendado

Con **MacBook Pro 16" M5 Max, 18 corazones CPU, 40 corazones GPU, Neural Engine 16 corazones, 128 Go de memoria unificada, SSD 8 To**, **IntelliJ Ultimate**, **Scala/Java/Play/Spark**, elegiría esta stack:

| Capa                 | Herramienta                                                 | Función                                                                                                                                   |
|------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| IDE principal          | **IntelliJ Ultimate[**                                 | Navegación, tipografía, refactor, error, pruebas y puesto de control de agentes                                                             |
| Asistencia IDE         | **JetBrains AI**                                      | Código Completion, Next Edit Sugerencias, AI Acciones y pequeñas transformaciones sin sustituir al agente principal                         |
| Agente Claude principal | **Claude Code Max**                                   | Opus 5.5 `medium` para agentic coding, arquitectura y debugging; Sonnet 5.5 `medium` para micro-dev; Fable 5.2 en escalada fronteriza |
| Modelo local           | **Qwen3-Coder-Next / Qwen3.8-27B**                    | Coder-Next como baselina rápida; Qwen3.8-27B como challenger quality-first para medir                                                |
| Harness local          | **Qwen Code o OpenCode**                             | Qwen Code es ahora un arness agente completo; OpenCode sigue siendo una alternativa a medir                                        |
| Agente Codex / reviewer | **Codex en IntelliJ / ChatGPT Desktop / Codex CLI** | GPT‑6.2 Sol `Medium` para el end-to-end-end; GPT‑6 Luna `High` en micro-dev; GPT‑6.2 Astra `Light`+ para las tareas fronterizas      |
| GitHub workflow        | **GitHub Copilot**                                    | Issues → agent, PR, review automatice and corrections CI for rescatitries GitHub                                                  |
| Seguimiento de PR opcional   | **Codex Goal mode / Heartbeats / Cloud; Claude Code `/ship` / `/steward` / Cloud Auto-fix ; Claude Ship** | GPT‑6.2 Sol `Medium` para el seguimiento Codex borné; agentes GitHub centralizadas en equipo, sin sustituir la revisión cruzada ni la CI |
| Pequeño diff             | **Aider**                                             | Modificaciones específicas, git-first, hebilla lint/test                                                                                     |
| IDE agente opcional    | **JetBrains Junie / JetBrains AI**                    | Agente nativo en IntelliJ si quieres quedarte en la UI                                                                                  |
| Búsqueda de códigobase     | **Sourcebot**                                         | Búsqueda multi-repos, símbolos, usos, archivos relevantes                                                                           |
| KnowledgeGraph         | **ScalaSemantic MCP / Codebase-Memory MCP**           | ScalaSemantic para el gráfico semántico Scala ; Codebase-Memory para el gráfico estructural poliglota Java/Kotlin                       |
| Decision layer         | **Jev 1.14**                                          | Decisiones cerradas de alta frecuencia: clasificación, routing, skill selection, escoring y señal de escalada                           |
| Docs actualizados            | **Context7**                                          | Verificación API, frameworks, libs (anti- alucinación)                                                                                |
| Integración agente IDE  | **JetBrains ACP + MCP**                               | ACP vincula la IED con los agentes; MCP expone herramientas, contexto y acciones IntelliJ                                                           |
| Optimisation tokens    | **RTK + Headroom**                                    | Descuento de logs, diffs, outputs terminal                                                                                                |
| Ruta API            | **OpenRouter**                                        | Acceso puntual a modelos alternativos                                                                                                 |

Situación y madurez de las herramientas:

| Herramienta                   | Situación                                           | Punto de vigilancia antes de la adopción                                                                                                                                  |
|-------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code             | Estable, herramienta oficial                           | Opus 5.5 es el modelo Opus actual para la larga coding larga; Sonnet 5.5 es el tier rápido; Agente Teams sigue siendo experimental, Ultrareview en research preview   |
| Claude Ship             | Código de revisión GA ; Steward / Approvals beta     | Servicio de Team/Enterprise facturado por separado; `/ship` y `/steward` locales son de uso local Claude CodeVéase sección 12.                                             |
| Codex post-PR           | Goal mode, Scheduled tasks, Cloud y Code Review oficiales | Heartbeats por superficie; permisos y cuotas para comprobar; Watch and Fix no confirmado; sin mermelada automática. Véase sección 12. |
| Claude Mods             | Disponible desde Claude Code 2.1.287            | Extension JS/TS in-process; muy potente pero no sandboxea: nsimplantar sólo código auditado y limitar su uso a las necesidades que hooks/skills/MCP no cubren bien |
| Jev 1.14                | Early access; API System One                    | Muy buen candidato para las decisiones cerradas; umbrales para el calibre por tarea, estado mínimo, nunca autoridad final sobre una acción crítica                           |
| Qwen3-Coder-Next local  | Estable lado modelo                               | Sobre 128 GB: Q4_K_M ≈ 48,4 Go cómodo; Q5_K_M ≈ 56,7 GB recomendado; Q6_K ≈ 65,5 Go viable; Q8_0 ≈ 84,8 GB a probar puntualmente                           |
| OpenCode                | Activo, LSP parcialmente exp.                    | Validar el LSP Metals en tu repo de antes estandarización                                                                                                           |
| Qwen Code               | Activo, alternativa seria                      | Auto-Memory/Skills, subagentes, worktrees, MCP/LSP; Agente Teams y Arena siguen siendo experimentales                                                                     |
| ChatGPT Desktop / Codex | App desktop ChatGPT, CLI, extensión IDE y Cloud | Codex ahora es capaz de pilotar varias sesiones/agentes; plugins y permisos aún no han sido auditados                                                                  |
| JetBrains Junie / CLI   | **Stable**, BYOK                                 | Opción creíble, a partir de bake-off en el depósito Scala                                                                                                      |
| Aider                   | Estable, mantenido                                 | Disciplina "poco archivos" indispensable                                                                                                                         |
| Sourcebot               | Estable                                           | Costo de alojamiento e indicación multi-repos                                                                                                                     |
| Context7                | Estable                                           | Cobertura variable según libs Scala De nicho                                                                                                                  |
| RTK                     | Estable                                           | Hooks PreToolUse para probar en tus salidas sbt reales                                                                                                              |
| Headroom                | **Experimental**                                 | Prueba en logs/diferentes no críticos únicamente                                                                                                                     |
| OpenRouter              | Estable                                           | Cero infra; ideal como puerta de salida puntual a GLM/Kimi/Gemini/Grok y nuevos modelos                                                                  |

JetBrains a dos niveles MCP por distinguir: el soporte MCP lado AI Assistant existe desde IntelliJ IDEA 2025.1 como cliente, y IDE JetBrains también exponen un servidor MCP integrado desde 2025.2 para que los clientes externos accedan a las herramientas de IED. Esto es especialmente importante para Scala, donde el agente necesita símbolos, tipos, módulos, inspecciones y run configuraciones, no sólo texto en bruto.

Desde IntelliJ IDEA 2026.1 - que se ha integrado Codex, Claude Agent y Junie, luego Cursor y GitHub Copilot a través del registro ACP público (abierto a finales de enero) 2026), con una gestión MCP por agente consolidado en 2026.2 Añade una distinción de protocolo: **ACP (Agente Cliente Protocol) conecta IDE con el coding agent**, mientras que **MCP conectar el agente con las herramientas y el contexto**. IntelliJ puede así servir de UI y de verdad estructural mientras deja a Claude, Codex, Junie GitHub Copilot u otro agente ACP intercambiable. Cada agente conserva su propio arness, sus modelos, su autenticación y sus permisos; por lo tanto, la unidad remolcada ya no es solamente el LLMLas herramientas del servidor MCP IntelliJ pueden ser restringidos por agente; para el debugging Scala/JVM, herramientas de debugger
expuestos por el servidor MCP IntelliJ (Herramientas prefijadas) `xdebug_`, activables desde la configuración del MCP Server) permiten recopilar stack, variables, treads y evidencias runtime sin inyectar `println` en el código.

<!-- section: s-1 -->
### Arquitectura IntelliJ 2026.2 recomendado

```text
IntelliJ IDEA
├── JetBrains AI
│   ├── Code Completion
│   ├── Next Edit Suggestions
│   └── AI Actions / petites transformations
├── Claude Code officiel
│   ├── plugin JetBrains / CLI
│   └── Claude Code Desktop
│       → abonnement Claude Max, agent principal sur raisonnement/debug/architecture
├── Codex
│   ├── agent ACP dans AI Chat
│   ├── ChatGPT Desktop / CLI
│   └── compte ChatGPT/OpenAI
│       → agent principal sur issues standard / reviewer croisé quand Claude écrit
└── GitHub Copilot
    └── couche GitHub-native : issues, PR, review automatique, CI
```

**ACP no sustituye a las integraciones oficiales.** Para Claude, guardia **Claude Code Oficial** como vía principal cuando quieres explotar la suscripción Claude Max: el plugin JetBrains, el CLI y la ficha Código de Claude Desktop comparten el mismo arness Claude Code y sus normas (`AGENTS.md` en fallback o `CLAUDE.md`, permisos, hooks, MCP, skills). Claude Code Desktop añade varias sesiones aisladas por worktrees, revisión visual de los diffs, terminal/editor integrados y seguimiento de los PR. ACP es sobre todo la capa de interoperabilidad que permite IntelliJ recibir varios agentes en una UI común.

Para Codex, el agente integrado en IntelliJ puede autenticarse con el **cuenta ChatGPT** o una llave OpenAI. Con una autenticación propia del proveedor, el uso del agente no consume los AI Credits JetBrains. La misma lógica para los otros agentes ACP que utilizan su propia cuenta proveedora. Las funciones in-editor **Código de complemento** y **Next Edit Sugerencias** Tampoco consumen la cuota de AI Credits. Una suscripción **JetBrains AI Ultimate (35 AI Credits / 30 días)** Por lo tanto, se convierte sobre todo en un presupuesto para Junie, AI Chat y las funciones de la nube JetBrains ; no tiene que financiar la mayor parte del desarrollo operativo si Claude Code y Codex usar sus respectivas suscripciones.

Nota al lado JetBrains en 2026 : **Codex ahora se integra como agente en IDE** junto con Junie y Claude, el registro ACP permite añadir otros agentes, y un sistema de **Skills** Reutilizaciones completas MCP. La IED se convierte así en un **control plano local** : navegación, diagnósticos y debugger permanecen JetBrains, mientras que el writer o el reviewer puede ser cambiado por sesión sin abandonar el medio ambiente Scala/JVM.

---

