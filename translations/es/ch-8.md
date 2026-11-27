<!-- section: chapter -->
# 8. Estructura recomendada del repositorio

Añade estos archivos o carpetas a la raíz, manteniendo **un solo lugar de la verdad** :

```text
AGENTS.md                       # Source commune, courte, versionnée
CLAUDE.md                       # Optionnel :Importe @AGENTS.md + règles Claude spécifiques
GEMINI.md                       # Pointeur vers AGENTS.md ou symlink selon ton outil
.github/copilot-instructions.md # Règles de review / coding agent GitHub Copilot, si utilisé
.github/instructions/           # Règles Copilot path-specific si nécessaire
.aiignore                       # Exclusions IA : secrets, gros artefacts, generated
.claude/rules/scala.md          # Règles Claude path/scopes si utiles
.claude/rules/testing.md
.claude/rules/security.md
stryker4s.conf                  # Mutation testing
docs/architecture.md
docs/testing.md
docs/review-checklist.md
docs/scala-style.md
scripts/ai-test-changed
scripts/ai-lint-changed
scripts/ai-diff-context
scripts/ai-rules-drift
```

El objetivo no es acumular documentación, sino evitar que el agente redescubra las mismas reglas en cada sesión. El archivo debe permanecer corto, estable y operativo.

> **Sincronización de archivos de contexto:** Codex carga las instrucciones globales de `CODEX_HOME`, luego
> los archivos de la ruta proyecto desde la raíz al directorio actual. En cada nivel,
> `AGENTS.override.md` prima sobre `AGENTS.md` ; las instrucciones más cercanas al directorio de trabajo
> Los nombres de fallback y el tamaño máximo dependen de la configuración.
>
> Claude Code, con el Mod integrado `cc-plugin-agents-md`, utiliza por defecto `claude-md-or-agents-md` :
> `AGENTS.md` está cargado si ninguno `CLAUDE.md`, `.claude/CLAUDE.md` o `CLAUDE.local.md` no existe en el
> Directorio actual o sus padres. Las instrucciones de usuario/administradas y `.claude/rules/` continúan
> `AGENTS.override.md` no es leído por Claude a través de este fallback. El modo
> `claude-md-and-agents-md` carga ambas sin duplicar un archivo ya importado. El fallo puede ser
> no disponible en algunas superficies; no sustituye a un importador explícito cuando es necesario.
>
> Para este workflow mixto, se prefiere un `AGENTS.md` común, y si `CLAUDE.md` Existe, comienza con
> `@AGENTS.md`. A continuación, mantén sólo las reglas realmente específicas de Claude. Verifica las instrucciones
> cargadas en un nuevo período de sesiones (`/context all` Claude, y preguntar a Codex listar archivos
> para sub-componentes, comprueba también el descubrimiento desde el directorio real
> ningún override puede debilitar una regla de seguridad externa.

A saber lado Claude Code : los **rules** en `.claude/rules/` permite completar las instrucciones de proyecto con instrucciones más específicas, por ejemplo por subarborescencia o tipo de tarea. A menudo es mejor que un enorme `CLAUDE.md` global cuando este archivo existe.

Es decir , también : el **auto-memory** Claude Code requiere una versión reciente, documentada desde v2.1.59+. Las primeras líneas de `MEMORY.md` se pueden cargar automáticamente, y los subagentes pueden tener su propia memoria. Usa esta memoria para recordatorios de patterns recurrentes, no para secretos, no para decisiones de arquitectura no revisadas, y no como sustituto de la documentación versionada.

<!-- section: s-1 -->
## Contenido mínimo de `AGENTS.md`

```text
Build, test and formatting commands (exact commands)
Non-obvious architecture boundaries and business invariants
Public API / JSON / migration constraints
Protected files and permitted write scope
Scala conventions absent from existing documentation
Stop conditions and definition of done
Pointers to relevant docs and spec
```

Escribe estas reglas **para el agente, no como documentación humana** : prefiere rutas, comandos, números y condiciones verificables. Guarda unos cientos de palabras como punto de partida. README, tutoriales, lista exhaustiva de los módulos y las comparaciones de modelos permanecen en `docs/`, cargados a petición.

<!-- section: s-2 -->
### Ruta en la configuración de usuario

Conserva la matriz de la sección 3 en un documento de enrutamiento o perfiles de usuario Codex/Claude en lugar de en cada `AGENTS.md` : el depósito debe seguir siendo independiente del modelo. Si un orquesta debe consultar esta matriz, añade sólo un puntero a ella. Las limitaciones de trabajo y seguridad no cambian según el modelo.

<!-- section: s-3 -->
## Contenido mínimo de `CLAUDE.md`

```markdown
@AGENTS.md

## Claude Code
Use plan mode for risky multi-file changes.
```

Mueve las reglas comunes del antiguo `CLAUDE.md` a `AGENTS.md` (sin duplicación). El modo plan Claude es una preferencia de arness; las autorizaciones efectivas permanecen en la configuración y el sandbox.

<!-- section: s-4 -->
## Por qué conservar `AGENTS.md`

Con Codex y el Mod integrado `cc-plugin-agents-md` de Claude Code (fallback) `AGENTS.md` por defecto), `AGENTS.md` Los trabajos recientes sobre los agentes de codificación indican que un fichero de instrucciones de este tipo puede reducir el tiempo de ejecución y los tokens de salida manteniendo al mismo tiempo una tasa de completación comparable. El efecto práctico esperado es simple: menos contexto repetido, menos instrucciones olvidadas, menos deriva entre herramientas.

> ** Estado de las pruebas: resultado mixto, no beneficio automático.** Otra evaluación de 2026 observa que los archivos
> contexto suelen reducir ligeramente la tasa de éxito y aumentan el coste en más de 20 %, especialmente cuando
> repiten el README o añaden requisitos innecesarios. Los archivos escritos por los sostenedores hacen mejor que los
> Generados automáticamente, pero también deben ser medidos.
>
> Regla corregida: `AGENTS.md` debe contener únicamente lo que cambia efectivamente una acción
> invariantes no evidentes, archivos prohibidos, convenciones ausentes de README y reglas de parada. No hay visitas guiadas
> narrativa del depósito, sin catálogo de tecnologías, sin consejos genéricos. Compare regularmente una muestra
> de tareas con y sin el archivo.
> la misma literatura: permanecer bajo **~500 palabras**, centrado en las normas de prueba, las convenciones de estilo y las
> avisos de peligro de no visita guiada del repositorio  ¡y releer el archivo como código a cada revisión.

<!-- section: s-5 -->
#### Protocolo de validación: medir la eficacia de AGENTS.md

Un crack.md que no cambia nada en el resultado es el contexto muerto que cuesta tokens en cada sesión. Protocolo de validación trimestral:

**Test A/B sobre 10 tareas representativas:**

1. Selecciona 10 tareas reales del backlog (mix greenfield/bugfix/refactor)
2. Para cada tarea, ejecuta 2 veces:
    - Run A: con ramilletes.md en el contexto
    - Run B: sin lips.md (o con una versión vacía)
3. Medición para cada run:
    - Número de vueltas antes de completar
    - Número de archivos fuera del scope afectados
    - Número de errores de compilación
    - Cumplimiento de los convenios de prueba
    - Costo total en tokens
4. Compare:
    - Si no reduce NINGUNA métrica → es inútil, quítalo.
    - Si reduce algunas métricas → sólo mantiene las secciones útiles
    - Si aumenta el coste sin mejorar la calidad → es perjudicial

** Indicadores de un ramificador eficaz.md:**

- El agente cita los pedidos de prueba exactos sin redescubrirlos
- El agente no toca los archivos prohibidos sin que se lo recuerden.
- El agente respeta los convenios de nominación desde el primer diff
- El número de "llamadas" humanas durante el período de sesiones disminuye

** Indicadores de un ramificador.md dañino:**

- El agente produce diffs más verboso (es "aplica" demasiadas reglas)
- El coste en tokens aumenta > 20% sin mejora mensurable
- El agente alucina comandos que no están en el archivo
- Las normas genéricas anotan las normas específicas

Regla de mantenimiento: cada vez que una regla de AGENTS.md es violada por un agente Y que la violación es capturada en repaso, la regla es mal formulada o en el lugar equivocado. Corrígela o materializa-la en un control de la sección 5 o 15A en lugar de añadir una frase más.

<!-- section: s-6 -->
#### Auditoría de *rule drift*: comprobar que las instrucciones siguen describiendo la repo real

Las reglas destinadas a los agentes son voluntariamente específicas  la ruta, el comando, los módulos, los archivos prohibidos y precisamente por eso envejecen rápidamente. Una instrucción falsa es peor que una instrucción ausente: obliga al agente a reconciliar `AGENTS.md` con un códigobase que ya ha cambiado.

Añade `scripts/ai-rules-drift` y ejecutalo después de cualquier cambio de arquitectura/build, y luego al menos una vez a la semana si el depósito se mueve mucho:

```text
Vérifier :
- chaque chemin cité dans AGENTS.md / CLAUDE.md existe encore ;
- chaque module sbt cité existe encore ;
- chaque commande de compile/test/format est encore valide ;
- aucun nom de DB, service, dossier ou script supprimé n'est encore référencé ;
- les fichiers « interdits » correspondent encore aux vraies surfaces critiques ;
- si CLAUDE.md existe, il importe ou complète toujours la source commune attendue.
```

El script puede permanecer determinista para los checks simples (`test -e`, tamaño de los módulos, comandos `--help`/dry-run) y sólo hacer **informar** los casos ambiguos. Nunca permita al agente que detecta la deriva a reescribir y luego auto-aprobar sus propias reglas persistentes: el diff de reglas se revisa como código.

<!-- section: s-7 -->
### Instrucciones GitHub Copilot sin duplicar `AGENTS.md`

Si el repositorio utiliza GitHub Copilot, conserva `AGENTS.md` como contrato común y reserva `.github/copilot-instructions.md` las expectativas específicas de **review GitHub** : gravedad de los findings, convenciones de PR, archivos de monitoreo y criterios que deben ser notificados. `.github/instructions/**/*.instructions.md` permite especializar estas reglas por carretera. Evita copiar toda la arquitectura o las reglas. Scala : una instrucción común debe permanecer en `AGENTS.md`.

Copilot Code Review lee las instrucciones y esquís de la **rama de cabeza de la PR**Por lo tanto , una modificación de estas normas forma parte de la superficie de código que debe revisarse: un agente no debe poder suavizar sus propias limitaciones en el mismo PR sin que este cambio sea explícitamente visible y validado .

