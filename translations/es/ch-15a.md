<!-- section: chapter -->
# 15A. CI/CD para flujos de trabajo agénticos

La CI es el juez final determinista del principio rector  la condición de adaptarlo a los PRs agentes, que tienen modos de fallo específicos: pruebas que no pueden fallar, diffs fuera de plantilla, rizos costosos.

<!-- section: s-1 -->
## Las cuatro gatas específicas de los PRs agenticos

```text
1. Control de límites y alcance: diff base → candidato, archivos protegidos, tamaño y número de archivos
2. Control de calidad de pruebas: conjuntos realmente ejecutados + puntuación de mutación y mutantes importantes según el riesgo
3. Control de revisión: hallazgos BLOCKING / REGRESSION_RISK verificados y corregidos, o resueltos por una persona
4. Control de presupuesto: todo job que invoque un LLM tiene un límite de tiempo Y un tope de coste
```

Dos ejes complementarios a considerar una vez que se haya establecido la base de las cuatro gatas:

- **Control de deriva de arquitectura** :: La tecnología Radar de Thoughtworks (abril) 2026) señala que el uso intensivo de agentes acelera la deriva entre el código real y la arquitectura de referencia, y recomienda que se combinen controles deterministas (fitness functions, ArchUnit, que analiza el bytecode JVM y por lo tanto funciona también en Scala compilado) con una evaluación LLM periódica. Una regla ArchUnit el módulo `api` no depende de la implementación de la misma. CI cuesta menos que una vuelta de agente y detiene una deriva estructural que ni escalafmt ni Stryker4s No lo veas.
- **Control de duplicación** : SlopCodeBench (sección 1A) mida una acumulación de duplicación a través de los checkpoints agentes; un scan type jscpd (detector de copiado pegado que token las fuentes Scala) en los archivos afectados transforma esta señal en métrica seguida o incluso en gate. La duplicación es el defecto menos visible en revisión humana y uno de los más costosos en mantenimiento aplazado.

Sobre GitHub, **Copilot Code Review o Codex Código Review puede añadirse como señal automática**, pero no sustituye a ninguno de estos gates. Una revisión del bot no es una aprobación humana; comprueba las reglas GitHub Reales. Comienza por una revisión previa solicitud o en la apertura, y luego reserva la revisión después de la corrección a los cambios que la justifiquen y a los nuevos SHA que requieran una validación independiente.

**Claude Approvals no es una prueba de calidad.** Una regla `claude: approves` no activa por sí sola Código de revisión; `seats: 1` podrá contar al autor y `seats: 0` puede permitir una mierda sin lectura humana. GitHub puede también contar la aprobación del bot en su cuota de reviews. Para el flujo de trabajo de esta guía, guarda `claude: comments` Al principio, los aprobadores humanos independientes en equipo, y una mierda humana en solitario. Nunca utiliza un clasificador probabilista como el único árbitro de un cambio crítico.

La presencia de `.claude/approvals.yml` puede desactivar las revisiones automáticas en los caminos cubiertos, incluso en modo observa: para conservarlas, referencia `claude/code_review` en las reglas (por ejemplo, bajo `advisory`Una condición Approvals no lee los resultados de CI : conserva compila, pruebas, escalafmt, seguridad y mutación testing como required checks GitHub Separados. En equipo, protege la rama objetivo y la política con CODEOWNERS, prohíbe los bypass a los agentes e invalida las anteriores autorizaciones cuando el diff cambia. Sólo hace obligatorio el check Approvals después de haber evaluado las decisiones en observa; no active ni automerge ni merge cola sin una gate humana efectiva para los cambios que lo requieran. Un check verde, una discusión resuelta o un comentario
« aucun défaut » ne valent jamais une validation métier.

<!-- section: s-2 -->
### GitHub Rulesets e independencia de la gate

Impose de los required checks procedentes de la integración esperada, sin bypass para las identidades de los agentes; protege las ramas objetivo, prohibición de fuerza-push y supresión, aprobación de las modificaciones recientes y invalidación de las antiguas autorizaciones cuando el diff cambia. En equipo, requiere la aprobación de un humano independiente, y `CODEOWNERS` para los archivos de control; en solitario, no configura una regla imposible de satisfacer por el autor, conserva el mergado humano y un control de política separado. No cuenta una revisión bot como un humano. Una merge cola es opcional, a condición de verificar `merge_group`, y exigir las gatas del commit de integración. En caso de conflicto, cambio de SHA o avanzado de la base, reevalua el estado; una CI verde sobre una antigua revisión no valida al nuevo candidato.

<!-- section: s-3 -->
## Ejemplo: `.github/workflows/ai-review.yml`

Ejemplo para el depósito de dos módulos de la sección 11 (sbt 1.x). Fige las acciones a un SHA completo auditado y comprueba sus dependencias transitivas; actualicelas por PR dedicada. El SHA básico proviene del evento GitHub, no de un campo de PR controlado por su autor. `github.sha` es el candidato de integración para `pull_request` y `merge_group` ; la revisión humana se refiere al diff base/PR head, distinto de este commit de prueba. Para una merge cola, los controles deben realizarse también en el grupo de merge.

```yaml
name: ai-review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  merge_group:
    types: [checks_requested]

permissions:
  contents: read

concurrency:
  group: ai-review-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  deterministic-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          fetch-depth: 0
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1

      # Validate the integration candidate; fail on a missing base or wrong checkout.
      - name: Validate candidate
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}
          CANDIDATE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail
          test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
          test -n "$BASE_SHA"
          git merge-base --is-ancestor "$BASE_SHA" "$CANDIDATE_SHA"
          python3 scripts/ai-validate.py --base "$BASE_SHA" --mode validate \
            --receipt "$RUNNER_TEMP/validation.json"

  mutation-gate:
    needs: deterministic-checks
    runs-on: ubuntu-latest
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1
      # Configure Stryker's break threshold and inspect surviving mutants in the actual project.
      - name: Mutation testing
        run: sbt "project api" stryker
```

**Frontera de confianza de CI :** na YAML El PR puede modificar los scripts y el flujo de trabajo que contiene, o incluso los comandos de build o los informes. Protege los flujos de trabajo, los scripts, las reglas de prueba, las políticas y `CODEOWNERS` ; si está disponible, impone un required workflow de confianza procedente de un depósito/commit protegido (ruleset de organisation) y carga al validador desde esta fuente y no desde el candidato. Una modificación legítima de la política pasa por un PR y una validación humanas separadas. En solitario sin required workflow externo, compara estos archivos a la base y no autoriza ninguna merge hasta que se haya revisado una modificación de gate. No se base en un simple convenio `AGENTS.md`.

El checkout de la PR puede ejecutar código arbitrario a través de sbt : ningún secreto privilegiado, ningún token de la escritura, ni `pull_request_target` Los informes de prueba son pruebas operativas, no certificados inviolables si el código de prueba en sí es hostil. Archivo los informes y la procedencia en la CI según la política del proyecto; la validación debe ser reelaborada en el candidato final (y en el commit entregado si es diferente).

Puntos de doctrina:

* **los jueces deterministas pasan primero** : compilar, formato y pruebas selectivas son baratos en comparación con una llamada LLM Un trabajo LLM que gira en código que no compila es presupuesto quemado;
* si una revisión LLM de CI es realmente automatizado, dale una **clave API dedicada**, un plazo y un límite de gasto propio del trabajo; para un uso principalmente interactivo a través de las suscripciones Claude y ChatGPT, esta automatización sigue siendo opcional;
* **El trabajo LLM es read-only** : comenta la PR, nunca comete. Un agente que corrige en la CI recrea el problema 16, peor (sin humanos en el bucle);
* **`sbt --client` en locales, JVM fresca en CI** : el demonio sbt es la palanca de los rizos locales; en CI, una caché de dependencias controlada puede acelerar la resolución, pero no sustituye a las pruebas ni al aislamiento. **sbt 2.0.0 es estable desde el 14 Junio 2026** ; utiliza como mínimo **2.0.7** (o **1.13.0** sobre la rama 1.x) debido a la corrección de la OSP/TCP del 21 Agosto: definiciones de edificio en Scala 3, JDK 17 mínimo, cliente nativo `sbtn` (iniciar mucho más rápido, directamente útil para los rizos agenticos), caché local/distante compatible Bazel y `test` incremental. Esta guía sigue el convenio sbt 1.x: la migración hacia sbt 2.x es un cambio de edificio crítico que nunca se delega en un agente60+ ports, incluyendo Play y Scala.js en curso), y posteriormente
  adaptación de estos trabajos.

**Autofix Codex en CI : excepción explícita al trabajo de revisión read-only.** Si es realmente necesario un flujo de corrección alojado, separa el trabajo de generación del parche (sin derecho de push) del trabajo de publicación controlada; limita los disparadores a los eventos y actores aprobados. Nunca lanza código no fiable procedente de una PR con secretos o un token de escritura privilegiado (en particular vía `pull_request_target`) Fige las acciones por SHA, aplica permisos mínimos, un timeout, un presupuesto externo y un cerrojo de competencia por PR; comprueba el head SHA antes de la publicación, y luego vuelve a activar los checks requeridos. No fuerza-push, auto-aprobación ni merge por el trabajo LLM. Los comentarios, logs y parches siguen siendo datos no fiables; el fracaso nunca debe provocar cambios en los gates.

El mismo corte se incorpora a GitLab CI :: tres cursos de capacitación (`deterministic`, `mutation`, `llm-review`), incluso gates, `rules: changes` para lanzar Stryker sólo en los módulos afectados.

---

