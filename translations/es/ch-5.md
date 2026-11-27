<!-- section: chapter -->
# 5. Flujo de trabajo estándar para una tarea de negocio en Scala

<!-- section: s-1 -->
## Paso 0 : encuadre humano

Antes de la IA, escribes o aclaras:

```text
Objectif :
Comportement actuel :
Comportement attendu :
Contraintes métier :
API publique à préserver :
Fichiers probablement concernés :
Tests ciblés :
Validation harness :
Risque :
Critère d'acceptation :
```

Note los requisitos profesionales e invariantes importantes (`REQ-01`, `REQ-02`, etc. Para cada requisito, declara la prueba o la prueba esperada antes de la implementación; un requisito sin oráculo debe estar explícitamente marcado sin cobertura y arbitrado. En el PR, asocia requisito, comando/prueba, resultado, SHA validado y límites de la prueba. La matriz de trazabilidad puede permanecer muy corta para un ticket trivial.

`Validation harness` deberá nombrar ** antes del modo de write** las pruebas que el propio agente pueda ejecutar: compilación selectiva, pruebas unitarias/integración, ScalaCheck, escalafmt, eventualmente Stryker4s y control del diff. Si aún no sabes cómo demostrar que el cambio es correcto, la tarea no está lista para ser delegada.

Sin eso, pagas los modelos para descubrir el problema en lugar de resolverlo.

> **Posicionamiento contra el estado del arte 2026 (Spec-Driven Development  land)** : este encuadre es exactamente lo que
> la industria se ha formalizado bajo el nombre de SDD, convertido en el contrapeso dominante en el coding vibe
> artefacto más rentable producido por el ser humano cuando el agente escribe el código. La herramienta (GitHub Spec Kit, OpenSpec,
> AWS Kiro, notación EARS para requisitos de prueba) puede estructurar este flujo de trabajo, pero no es obligatorio: este
> Guía práctica ya la variante ** spec-anchored** (la spec marco y sobrevive a la tarea, el código + las pruebas permanecen
> la fuente de la verdad), que es la postura recomendada para el código de oficios existente, por oposición al
> ** spec-as-source** (el humano sólo edita la spec), todavía experimental.
> campo: el nivel de detalle de la spec debe seguir la *crítica* del código de  ¡definir un script desechable es
> del desperdicio, la subestabilidad de un contrato público es una deriva garantizada.
>
> **Seleccionar herramientas SDD sin framework-sprawl.** El paisaje SDD
> Ahora supera los treinta frameworks (Spec Kit, OpenSpec, Kiro, BMAD-METHOD, GSD, Tessl...).
> práctica que se desprende de ello: **GitHub Spec Kit** para el greenfield (constitución → specify → clarify → plan →
> checklist → tasks → analyze → implement → converge, con pasos de control opcionales) ;
> **OpenSpec[** para brownfield iterativo de las specs versionadas en la repo con *delta markers[* por cambio, la
> posición más cercana a la variante spec-anchored de esta guía; **AWS Kiro** si quieres la notación EARS integrada
> y el ecosistema AWS. Ninguno es un requisito previo: si `AGENTS.md` + el paquete de análisis anterior + las gatas CI
> (sección 15A) ya están haciendo el trabajo, añadir un framework SDD añade contexto, no calidad.
> negociable: la spec vive en el repo y se repasa como código  la spec mantenido fuera de versión se convierte en un segundo
> Fuente de la verdad divergente.

> **Dos arneses que no deben confundirse.** Un papel SDD publicado el 31 agosto 2026 propone una distinción útil entre
> **technical harness** (modelo, herramientas, contexto, permisos, pruebas) y **methodological harness** (spec, roles,
> responsabilidades, revisión y autoridad de puesta en libertad). **confirma** la estructura de esta guía: mejorar
> Claude Code, Codex o MCP no sustituye a la disciplina de especificación y validación humana.
> Sin embargo, principalmente conceptual y se apoya ampliamente en la literatura gris; utiliza esta distinción
> como marco de diseño, no como prueba empírica de que un marco SDD dado mejora la productividad.

> **Primera información sobre la práctica real.** El estudio CMU/Google
> and as Practicad  ¡Despertad! (declarative, no replicada) observa que los profesionales experimentados ya aplican SDD de
> manera **selectiva, especialmente para nuevas funciones o cambios riesgosos**, con speces redactados por los agentes a partir de una intención
> humaine puis relues, et une vérification surtout par tests écrits par les agents. Le défaut principal est la
> **deriva silenciosa spec ↔ código[** cuando no existe ningún plan de mantenimiento; las devoluciones Thoughtworks añaden
> la * instrucción bloat* (espejos y contextos que crecen hasta que el agente pierde el hilo). Esto confirma dos
> reglas de esta guía: dosificación por criticidad, y spec versión y repasada. Añade solamente una tercera regla:
> **una prueba escrita por el agente no valida su propia spec** ; mantenga la prueba de reproducción que falla antes del parche
> y la mutación de testing (sección 5, etapa 4) En el lado de herramientas, **`/speckit.converge`** relee el código frente a
> `spec.md`, `plan.md` y `tasks.md` y **añade solamente las tareas que faltan a `tasks.md`**Es un control de
> coherencia útil después de la implementación, **no un oráculo** : ni las pruebas independientes ni la revisión humana deben
> ser suprimidos con el pretexto de que Spec Kit anuncia  ¡Converged!

<!-- section: s-2 -->
#### Templato de spec operativo (copiar y pegar)

Este template materializa la variante spec-anchored de la guía. Vive en el repo (por ejemplo `specs/TICKET-123.md`) y se revisa como código.

<!-- section: s-3 -->
# SPEC: [TICKET-[123]] [Tiro corto]

<!-- section: s-4 -->
## 1Objetivo (1 oración, verbo de acción)

[Ex: "Añadir una tasa de descuento por etapas de cantidad al servicio de DiscountService"]

<!-- section: s-5 -->
## 2 No objetivos (explicito, anti-derivado)

- [Ex: "No modificar el cálculo de descuento existente por código de descuento"]
- [Ex: "No tocar el API público del módulo pricing"]

<!-- section: s-6 -->
## 3 Comportamiento esperado (reglas de trabajo, numeradas)

1. [Regla 1: si la cantidad >= 10 se entrega 5%]
2. [Regla 2: si la cantidad >= 50 se entrega 12%]
3. [Regla 3 : Los escalones no se acumulan, se aplica el más alto]

<!-- section: s-7 -->
## 4 Limitaciones técnicas

- API público que debe conservarse: [firmas exactas]
- Serialización JSON : [sin cambios / añadir campo X con backward compat]
- Rendimiento: [no hay consulta DB adicional en el hot path]
- Competencia: [estado inmutable / atomicidad requerida]

<!-- section: s-8 -->
## 5. Archivos probablemente afectados

- `src/main/scala/.../DiscountService.scala`
- `src/test/scala/.../DiscountServiceSpec.scala`

<!-- section: s-9 -->
## 6. Pruebas de aceptación (criterios de "dona")

| No se aplica a los vehículos de las categorías A y B. | Prueba esperada |
|----------------------|-----------------|
| REQ-01: umbral 10 | Prueba unitaria: 9 → 0 %, 10 → 5 % |
| REQ-02: umbral 50 | Prueba unitaria: 49 → 5 %, 50 → 12 % ; propiedad entregada ≤ 12 % |
| REQ-03 : no acumulación | Prueba de no retroceso en la acumulación; entrega por código de descuento sin cambios |
| REQ-04: contrato JSON | Prueba de compatibilidad |
| REQ-05: rendimiento | Medición del número de solicitudes DB sobre la hipótesis de integración |

- [ ] Mutación testing: puntuación / mutantes importantes para justificar en los archivos afectados
- [ ] Resultados relacionados con el SHA y los requisitos; excepciones y riesgos residuales explícitos

<!-- section: s-10 -->
## 7 Riesgos y mitigaciones

| Riesgo               | Probabilidad | Impacto | Mitigation                      |
|----------------------|-------------|--------|---------------------------------|
| [Arrondi BigDecimal] | Media       | Arriba   | [Usar RoundingMode.HALF_UP] |

<!-- section: s-11 -->
## 8. Definición de done (checklist final)

- [ ] Compile sans warning
- [ ] Pruebas de objetivos verdes
- [ ] scalafmtCheckAll passage
- [ ] Revisión del segundo modelo realizada
- [ ] Diff < [N] líneas
- [ ] No hay archivos fuera del scope modificado

Nivel de detalle adaptado a la criticidad:

- Script desechable → secciones 1, 2, 6 Suficiente
- Contrato público / dinero / seguridad → todas las secciones obligatorias

---

<!-- section: s-12 -->
## Paso 1 : investigación específica

Usa en este orden:

1. **Sourcebot** para localizar archivos, usos, pruebas.
2. **IntelliJ** para verificar símbolos, tipos, jerarquías.
3. **Context7** si una API externa o una versión reciente está implicada.
4. **Qwen local[** para producir una exposición informativa.

Prompt Qwen:

```text
Analyse ces fichiers et produis :
- résumé du flux métier
- classes et méthodes impliquées
- invariants à préserver
- tests existants
- risques
- ambiguïtés
- prompt propre à donner à Claude Code

Ne propose pas encore de patch.
```

---

<!-- section: s-13 -->
## Paso 2: plano por la lengüeta writer, sin cambios

Prompt writer (Codex o Claude Code):

```text
Tu es l'agent writer de cette tâche.

Objectif :
[objectif]

Contraintes :
- diff minimal
- pas de changement d'API publique sans validation explicite
- préserver les comportements existants
- ajouter ou adapter les tests
- procéder par petites étapes
- expliquer les risques
- ne rien modifier avant validation

Commence par explorer le code et proposer un plan.
```

Regla de los documentos: **sin planos, sin write modo**. El plan debe enumerar los archivos a modificar, los archivos a no tocar, la estrategia de prueba, los riesgos y el tamaño esperado del diff.

---

<!-- section: s-14 -->
## Paso 3 : implementación por pequeños diffs

Prompt:

```text
Exécute uniquement l'étape 1.
Ne touche pas aux autres étapes.
Garde le diff minimal.
Après modification, donne :
- fichiers modifiés
- raison de chaque changement
- commande de test ciblée
```

Para Scala, evita los grandes refactors automáticos. 30 à 300 líneas de diff cuando es posible. Las vueltas de campo y los estudios recientes sobre los PRs agentes convergen hacia pequeños y bornados PRs, más fáciles de leer y menos propensos al ajedrez CI. A nivel organizativo, el estudio del despliegue Claude Code / Copilot CLI en Microsoft (arXiv, julio) 2026, decenas de miles de ingenieros) medida ~24% de PRs se estrellan más en los adoptadores de la misma forma que el efecto es real, pero se materializa en los PRs *Revisables*No en diffs gigantes.

---

<!-- section: s-15 -->
## Paso 4 : validación IntelliJ + pruebas

Agentes LLM son conocidos por escribir pruebas "happy path" (pruebas que pasan pero no comprueban los casos de error o los límites). Scala/SBT :

```text
scalafmtCheckAll
compile
Test / compile
testOnly <TestCiblé>
IntegrationTest / testOnly <TestCiblé>
```

Entonces sólo si el riesgo lo justifica:

```text
test
IntegrationTest / test
```

> **Nota sbt :** configuración `IntegrationTest` es **Despreciada desde sbt 1.9.0** en beneficio de un subproyecto
> dedicado (por ejemplo, un módulo `it` que `dependsOn(core % "test->test")`) o pruebas taggés. Si tu proyecto lo utiliza
> Todavía, los comandos anteriores siguen siendo válidos, pero nunca permite que un agente migra esta configuración por sí solo
> Ese es exactamente el tipo de cambio. `build.sbt` que debe pasar por una validación explícita.
> módulo,
> Vas directamente a un subproyecto `it`. Piensa también en dar al agente la orden más rápida disponible:
> `sbt --client` (o Bloop) evita pagar el inicio de la JVM por cada iteración del bucle de prueba-corrección, este
> que
> En **sbt 2.x**, `sbt` ya utiliza el modo cliente-servidor nativo `sbtn`
> por defecto; `sbt --client` sigue siendo una forma explícita. Medir el inicio en el proyecto real: migración 1.x → 2.x
> y cambio de `build.sbt` requieren validación humana (véase la sección 15A).
>
> Sí. `serverConnectionType` está configurado para `Tcp`, sbt 1.4.0 à 2.0.6 es
> vulnerable a una ejecución de código no autenticada a través de BSP. Elimina esta configuración o pasa al mínimo a **sbt 1.13.0
> o 2.0.7**. El transporte local predeterminado (socket Unix o named pipe) no se verá afectado.
> prioridad antes de exponer el servidor sbt a un IDE, agente o contenedor remoto.

<!-- section: s-16 -->
#### Optimización sbt para los rizos agentivos

La velocidad del bucle compilado-test es la primera palanca de productividad de agentes. Configuración recomendada en `.sbtopts` (repo):

<!-- section: s-17 -->
# .sbtopts  lazo optimizado para los rizos agenticos

```text
-J-Xms2g
-J-Xmx8g
-J-XX:+UseZGC
-J-XX:+UseStringDeduplication
-Dsbt.supershell=false
-Dsbt.color=false
-Dsbt.log.noformat=true
```

Explicación de las opciones:

- `UseZGC` : opción de medición contra el G1 por defecto en el depósito real; no prometes una ganancia sistemática ni pausas siempre inferiores a 1 ms
- `supershell=false` y `color=false`: reducirá el ruido en las salidas que el agente separe (menos tokens, menos context rot)
- `noformat=true`: Ídem, salidas brutas más fáciles de parser

Bajo sbt 2.x, `sbt` ya lanza el cliente nativo por defecto; `sbtn` sigue siendo una entrada explícita útil:

<!-- section: s-18 -->
# Primer lanzamiento (inicie el servidor)

`sbt`

<!-- section: s-19 -->
# Apelaciones posteriores desde el agente (inicio casi instantáneo)

`sbtn "compile"` `sbtn "testOnly *DiscountServiceSpec"`

Configuración del servidor en `project/server.sbt`:

```scala
// Keep the build server on a local transport.
Global / serverConnectionType := ConnectionType.Local
```

El transporte local es normalmente el defecto: **no muestra el servidor sbt en TCP** para acelerar a los agentes. `build.sbt` Sólo para enmascarar recompilaciones o verificaciones: `onChangedBuildSource := IgnoreSourceChanges`, `Test / fork := false` y la desactivación de Scaladoc pueden hacer que el resultado no sea representativo de la CI o modificar los comportamientos de las pruebas. Preferir el módulo y las suites (`project`, `testOnly`) sin alterar su semántica. **sbt 2.x, `test` es incremental y puede volver a utilizar sus resultados en caché** : utiliza `testFull` para una validación completa antes de una PR o en CI.

**Benchmark antes/después en tu depósito.** Comparado con JVM y las mismas opciones, en al menos diez ciclos de compilación incrementales + pruebas selectivas: latencia media, p95, reinicios sbt, presión de memoria y estabilidad de pruebas. No presente un ahorro cifrado en otro proyecto como una garantía.

Para Play Framework o proyectos de varios módulos:

```text
sbt "project api" compile
sbt "project api" "testOnly *DiscountServiceSpec"
sbt "project integration" "testOnly *OrderFlowSpec"
```

El punto esencial sigue siendo: no sólo pide a la IA  la prudencia de la prueba, da vueltas a las pruebas. Los protectores deterministas golpean las instrucciones textuales.

Elige las validaciones según el riesgo real, sin apilar herramientas innecesarias:

| Riesgo Scala/JVM | Prueba pertinente |
|------------------|-------------------|
| Cálculo del trabajo | ScalaCheck, límites, mutaciones de testing |
| Compatibilidad binario / TASTy | MiMa / TASTy-MiMa cuando sea pertinente |
| REST / JSON | Pruebas de contratos, esquemas y compatibilidad |
| Competencia y efectos | Ordenación controlada, cancellation, timeout, liberation des ressources |
| Spark | Datasets deterministas, nulls, esquema, particiones, idempotence |
| Rendimiento JVM | JMH o benchmark objetivo reproducible |
| Arquitectura | Escalafix / fitness functions en bytecode o fuentes |
| Seguridad | SAST que cubren realmente Scala, SCA, secreto escaneado y pruebas de autorización |

**CodeQL Java/Kotlin no demuestra una manta Scala** : comprueba la lista de lenguajes compatibles y experimenta el analizador elegido sobre defectos conocidos. No asimila un escáner de dependencias a un análisis de las fuentes.


<!-- section: s-20 -->
### Valor probatorio de las pruebas generadas

Una prueba escrita por el mismo agente que la implementación no es un oráculo independiente. Los trabajos recientes señalan que los agentes producen frecuentemente pruebas de observación o de impresión sin aserciones discriminatorias; aumentar el número de pruebas por el prompt no basta para mejorar la tasa de resolución. Otras evaluaciones por mutación muestran que las suites verdes detectan mal defectos realistas generados por agentes, y que su eficacia se deteriora cuando el código evoluciona incluso sin cambios semánticos esperados.

Por lo tanto , para un bugfix conserva la prueba más rentable:

```text
1. ajouter un test de reproduction minimal ;
2. vérifier qu'il échoue sur le commit de base pour la bonne raison ;
3. appliquer le patch ;
4. vérifier que ce test puis la suite pertinente passent ;
5. faire varier l'oracle : propriétés, cas limites, tests métamorphiques ou mutants ciblés ;
6. faire relire le test avant l'implémentation lorsque le domaine est critique.
```

No establezca un umbral de mutación universal que incite a jugar la métrica de la velocidad de la velocidad. Comparar la puntuación en el perímetro afectado, requiere una justificación para cada mutante que sobrevive importante y soy sobre todo el **delta de mutación puntuación**, retrocesos escapadas y retornos de repaso. Una prueba que no podía fallar antes del parche no demuestra el parche.

**La etapa de endurecimiento (Mutación Testing):** Una vez que la IA escribió las pruebas y son verdes, valida su robustez con Stryker4s :

```text
sbt "project api" stryker
```

Una puntuación baja **puede** revelar pruebas insuficientes, pero también mutantes equivalentes, no pertinentes o mal dirigidos. Examina primero los mutantes supervivientes, su impacto profesional y las exclusiones; no añade afirmaciones artificiales para aumentar la puntuación. Si un mutante importante permanece vivo, devuelve el informe al agente pidiendo un **prueba de comportamiento observable independiente del parche**, y luego reiniciar las pruebas selectivas.

---

<!-- section: s-21 -->
#### Paso 5: Obligar la verificación antes de la declaración de terminación

Agentes LLM Añade esta instrucción sistemática al final de cada aplicación rápida:

Antes de declarar que esta tarea ha terminado, usted DICE:

1. Ejecutar el comando de compilación y mostrar el resultado
2. Ejecutar la prueba objetivo y mostrar el resultado
3. Comprobar el diff desde la base aprobada, los cambios committados y no committados, y los archivos no seguidos
4. Listar los archivos modificados con la razón de cada cambio
5. Si un paso falla, corregir y empezar de nuevo 1 No digas "dona" a menos que los 5 puntos anteriores están satisfechos.

Para automatizar estas comprobaciones, utiliza los scripts comunes de la sección 5 (hooks) CI de la sección 15A. El hook `PostToolUse` compila solamente: `Test/compile` Los resultados de las suites y el diff completo deben estar asociados con el SHA candidato, y el CI un Stop hook no es una prueba de completar; no debe impedir una parada de bloqueo.

Variante para tareas críticas (seguridad, dinero, contrato público):

Antes de declarar que esta tarea ha terminado, ejecuta y muestra:

1. sbt compila (cero error, cero warning nuevo)
2. sbt "testOnly *SpecCible" (todos verdes)
3. sbt scalafmtCheckAll (formateo conforme)
4. Diff base → candidato y estado Git completa (sólo los archivos del plano)
5. Compruebe que el diff NO contiene: TODO, FIXME, println de debug, importación no utilizada, cambio de firma pública no solicitada Muestra el resultado de cada paso. Si un paso falla, corrige y reanuda. No declare "dona" antes de que los 5 pasos sean verdes.

---

<!-- section: s-22 -->
## Paso 6 : self-review por el writer

Prompt:

```text
Fais une review de ton propre diff avant de le transmettre au reviewer indépendant.
Liste :
- risques métier
- cas limites
- tests manquants
- changements inutiles
- fichiers à relire manuellement
- hypothèses que tu as faites
```

Este paso a menudo elimina errores evidentes antes de revisión externa. **Nunca vale la pena aprobarla.** : el agente que escribió el diff comparte las mismas hipótesis que su implementación y no puede constituir la gate final. El writer puede limpiar; un contexto fresco de **Otras familias de modelos** debe presentar sus conclusiones independientes.

---

<!-- section: s-23 -->
## Paso 7: revisión independiente por otra familia de modelos

Prompt reviewer: **Opus 5.5 Medium** si Codex escribió , **GPT‑6.2 Sol Medium** Si Claude escribió. Sube a High para un PR arriesgado y hacia Astra Light/Fable Low sólo si la capacidad adicional está justificada:

```text
Act as an independent senior Scala/JVM code reviewer.

Review the exact PR head SHA against its merge base, approved specification, acceptance criteria and AGENTS.md.
Work in a fresh read-only session; do not modify the implementation. Do not rely on the writer's reasoning
until you have formed your own assessment.

Prioritize functional correctness, preserved invariants, regressions, compatibility, test oracle quality,
error handling, resource safety, concurrency, performance, security and scope violations.

For every actionable finding, provide severity, file/line, reviewed SHA, violated requirement or invariant,
a concrete failure scenario or reproduction, the smallest plausible correction, and remaining uncertainty.
Distinguish verified defects from hypotheses. Ignore stylistic preferences and unrelated refactoring.
Do not invent findings. Return a concise verdict and evidence-backed findings only.
Never approve or merge the PR yourself.
```

Variante con clasificación de gravedad máquina-explotable ? mejor para la clasificación y un gato alimentado únicamente por findings validados independientemente (ver ejemplo de decodificación tipo en sección 12) :

```text
Classe chaque retour avec exactement un de ces labels :
- BLOCKING        : bug métier, perte de données, faille, contrat public cassé
- REGRESSION_RISK : comportement existant potentiellement altéré, cas limite non couvert
- STYLE           : lisibilité, convention, nommage — jamais bloquant
- OUT_OF_SCOPE    : amélioration valable mais hors ticket — à ignorer dans cette PR

Retourne uniquement du JSON valide :
{
  "findings": [ { "severity": "...", "file": "...", "message": "..." } ],
  "summary": "..."
}
```

La regla de gate asociada: `BLOCKING` y `REGRESSION_RISK` deberán ser tratados o impugnados explícitamente antes de la mermelada; `STYLE` es opcional; `OUT_OF_SCOPE` Parte en el backlog, nunca en el diff corriente.

Estas etiquetas siguen siendo ** hipótesis de repaso**, no hechos. Cada retorno bloqueado debe llevar una prueba verificable: archivo y línea, contrato violado, reproducción, prueba que falla o regla estática precisa. Sin prueba, pasa a la clasificación humana; la autoetiqueta de un modelo nunca debe bloquear por sí sola una mierda. Esta validación evita los falsos positivos costosos y los rizos del autor IA ↔ repasar IA  ¡que queman créditos sin nueva información.

El pattern recomendado sigue siendo: **un writer, un reviewer de la otra familia**. La revisión cruzada es una hipótesis de trabajo, no una garantía: un estudio *Cross-Model LLM Code Review* sobre 116 problemas algoritmicos con Opus 4.7 / GPT-5.5 observa una ganancia Codex → Claude (71,6 → 89,7 % de éxito) y una disminución Claude → Codex (91,4 → 82,8 % cuando el repaso reescribe el programa sin realizar las pruebas. No deduzco ninguna clasificación de los modelos actuales en Scala. El revisor detecta y justifica; el writer corrige después de la clasificación. Medirá los verdaderos/falso positivo, defectos faltados y retrocesos introducidos por las correcciones. Después de una corrección menor, re-revisión dirigida de los cambios e invariantes; revisión completa sólo si el riesgo o el alcance ha cambiado.

> **Esfuerzo y límites de la revisión.** Sobre 90 parches Django, un estudio *How Much Effort Does an AI Code Reviewer
> ¿Need?* Encontrar Opus 5.5 Medium no inferior a High en un margen predeterminado de 15 puntos, a un coste medio
> inferior en aproximadamente 20 %. Incluso High acepta 45 % de los parches considerados incorrectos por el oráculo reforzado; algunos
> Las etiquetas siguen siendo cuestionables.Bench-v2 (584 defectos reutilizables asociados a PRs) confirma que la cobertura
> los defectos por los agentes son limitados. Estos resultados consienten Medium para el día a día, pero no demuestran ni
> la equivalencia universal Medium/High ni la eficacia de los modelos actuales en Scala. Sin gate autonome LLM.

 Por defecto: **Suelo 6.2 Medium escribe → Opus 5.5 Medium review**, o **Opus 5.5 Medium/High escrito → Suelo 6.2 Medium review**- Luna/Haiku se utilizan para tareas mecánicas; Astra/Fable sólo se movilizan en escalada. `Ultra` se reserva a las misiones desvinculadas en ejes independientes.

---

<!-- section: s-24 -->
## Paso 8 : corrección selectiva

Nunca le pides al revisor que aplique automáticamente todas sus sugerencias. Selecciona las devoluciones útiles y vuelve a **writer original**:

```text
Voici les retours de review que je valide :
[liste]

Corrige uniquement ces points.
Ignore les suggestions optionnelles.
Garde un diff minimal.
Relance les tests ciblés.
```

**Deja de revisar cuando los criterios son verdes.** Un paso correctivo después de repasar es el defecto; un segundo sólo está justificado por un finding `BLOCKING` / `REGRESSION_RISK` nuevo y fundamentado, una prueba roja o una prueba determinista. No utilice un prompt del tipo  lago itero todavía hasta que sea perfecto  la  la: más allá del mejor checkpoint, el agente termina a menudo inventando cambios para satisfacer la demanda y puede degradar el diff.

Si es necesario un nuevo pase, compara sistemáticamente el nuevo diff con el checkpoint anterior y mantiene la versión que mejor satisface **spec + pruebas + scope**, no la versión más reciente.

Si delegas la corrección post-PR a Codex (Goal mode, Heartbeat o Cloud), `/steward` o PR Steward (sección 12), transfiere explícitamente el ownership de la rama, con el SHA de salida, la spec y las únicas devoluciones autorizadas. Deja de controlar antes de que el writer original se recupere. Cualquier nuevo commit recupera las validaciones pertinentes; la revisión independiente debe referirse al diff final, no al SHA antes de la corrección automática.

<!-- section: s-25 -->
## Paso 9: Guardafuegos anti-deriva agentes

Añade reglas de parada explícitas, que reducen los diffs innecesarios, los rizos de corrección y los créditos quemados:

```text
Stop immédiat si :
- l'agent touche un fichier hors plan sans explication ;
- l'agent modifie build.sbt, plugins.sbt, resolvers ou versions sans validation explicite ;
- la même erreur de compilation revient 2 fois ;
- les tests ciblés échouent 2 fois avec des causes différentes ;
- le diff dépasse la taille annoncée ;
- le correctif commence à changer l'architecture au lieu de résoudre le ticket.
- l'agent tente une écriture destructrice, un push, un déploiement, un partage externe ou une action sur des secrets
  qui n'étaient pas explicitement autorisés.
```

En este caso, no vuelvas a subir el fix de it. Más bien pide:

```text
Stop. Résume l'état exact :
- fichiers modifiés
- hypothèses faites
- erreur actuelle
- commandes exécutées
- prochaine action minimale proposée
Ne modifie rien.
```

> **Reanudar la mano sin pagar el doble de la misma exploración.** Tres mecanismos Claude Code a conocer:
>
> - **Checkpoints** : cada prompt crea un checkpoint (snapshot de archivos antes de cada edición por las herramientas de
>   Claude). `Échap Échap` o `/rewind` restaura la conversación, el código o ambos en un punto anterior, incluyendo
>   Después de cerrar la terminal. Límite conocido: sólo los cambios hechos a través de las herramientas de edición de Claude
>   se siguen, no los lanzados en Bash  ¡un checkpoint no sustituye ni un commit ni el worktree.
> - **`/compact` no lave una mala hipótesis** : la compacción resume la conversación y *conserva* Así que
>   Cuando el agente regresa dos veces a la misma pista falsa, el desfile es
>   `/clear` y luego un rápido estrechado con el nuevo estado  ¡no una compacción adicional.
> - **Permisos en deny-by-default** : `settings.json` acepta reglas allow / ask / deny; combina un allowlist
>   estrecha con deny explícito (red, archivos críticos, push) en lugar de aprobar a mano en bucle.
>   Esta es la versión produce las reglas de no automatización de la sección 3.
> - **Auto modo predeterminado** : desde 14 agosto 2026, el modo de auto es el modo de permiso predeterminado de las noticias
>   Sesiones en los planos Pro, Max y Team. Su clasificador reduce las interrupciones, pero no es una gate
>   trabajo: comprueba que tus reglas `deny` sobre `build.sbt`, migraciones, flujos de trabajo CI y push permanecen activas (los
>   *hard deny rules* del auto modo bloquean sin tener en cuenta las excepciones `allow`, y mantiene los hooks abajo.

<!-- section: s-26 -->
#### Claude Mods: Cuando superar los hooks clásicos

Desde **Claude Code 2.1.287**, un **Mod** es un plugin cuyos handlers JavaScript/TypeScript sloven en el proceso Claude CodeUn handler puede **Observar, reescribir o aceptar** un evento: tool call, prompt, torre, control o renderizado de la interfaz de la interfaz. Es una capa diferente de MCP : uno MCP proporciona herramientas desde un proceso/servicio externo; un Mod puede cambiar el comportamiento del propio arness. **3 octubre 2026**, la versión 2.1.288 ya añade `$.ui.selection()` y varios parches Mods/plugins: API como **joven y evolutivo**, y pincha la versión Claude Code para todo Mod que se vuelve crítico en tu flujo de trabajo.

| Necesidad                                                                                                 | Primitiva a preferir |
|--------------------------------------------------------------------------------------------------------|----------------------|
| Repetir instrucciones / un método                                                                 | **Skill**            |
| Acceso a un sistema o herramienta externa                                                        | **MCP**              |
| Bloquear, autorizar o registrar un evento con una regla simple                                        | **Settings hook**    |
| UI interactiva, estado compartido entre eventos, control local, intercepción/reescritura de un evento | **Mod**              |

La Mods API puede guardar comandos, tools y subagentes, llamar a un modelo, leer el estado y el uso de la sesión, mantener un store compartido, leer/escribir archivos, iniciar un proceso, llamar a HTTP o a MCP, y comunicarse con otras sesiones. Los Mods funcionan con sus hooks en el terminal JetBrains Los elementos de la unidad de control de la calidad no se devuelven a todas las superficies headless/cloud, ni al código tab de Claude Desktop.

**No sustituyas los tres hooks shell que aparecen a continuación por un Mod únicamente porque sea posible.** Para las gatas simples y deterministas (`build.sbt`, migraciones, diff max, pruebas obligatorias), un settings hook sigue siendo más pequeño, más legible y más fácil de auditar. Usa un Mod sólo si necesitas un estado cross-event, un flujo de trabajo interactivo, un flujo de trabajo interactivo o una interceptación que el hook clásico expresa mal.

> **Frontera de confianza mucho más amplia.** Un Mod s
> Prompts, tool calls, variables de entorno y settings, iniciar procesos o hacer red, reescribir una
> solicitud y gastar cuota a través de llamadas modelo. Los procesos que inicia son ** fuera del sandbox Bash** de
> Claude.
> Un Mod instalado también puede aprobar algunos tool calls que una regla `ask` ou un `PreToolUse` usuario tendría
> Detenlo.
> Por lo tanto, los permisos Claude no son un sandbox alrededor del código del plugin.

Antes de instalar o promover un Mod de terceros:

```text
1. Vérifier la source du marketplace et figer la version/commit quand c’est possible.
2. Lire .claude-plugin/plugin.json, hooks/hooks.json, le module register.*, bin/ et .mcp.json éventuel.
3. claude plugin validate ./mon-mod
   → inspecter en particulier les lignes hooks: et calls: sans exécuter le Mod.
4. claude --plugin-dir ./mon-mod plugin details <nom>
   → vérifier l’inventaire réel des composants.
5. claude plugin test ./mon-mod
   → tests de hooks déterministes, sans session, login ni réseau.
6. Si le plugin a des evals : claude plugin eval ... avant promotion.
7. Premier essai avec --plugin-dir dans un worktree jetable ; --safe-mode comme voie de récupération.
```

Para una organización, un verdadero control debe vivir en **managed settings** (`allowManagedModsOnly`, orden de los plugins gestionados, `disableAllHooks` y en el Mod integrado `cc-plugin-sec-default`, no en la buena voluntad de un Mod usuario. Para tu uso solo, la regla equivalente es simple: **Built-ins / código personal auditado > plugin comunitario opaco**, y ninguna actualización automática de un Mod sensible sin relectura del diff de la versión.

<!-- section: s-27 -->
#### Configuración común de los hooks Claude Code / Codex

Separada **feedback local** y **gate de validación**. Un hook en un pedido `Edit` no ve necesariamente las escrituras Bash, MCP o IDE; no puede garantizar el confinamiento. Suprímase `ai-guard.sh` basado en la búsqueda de cadenas en un comando: los caminos dinámicos, symlinks y ejecuciones indirectas escapan a este filtro. Aplica los permisos/sandbox de la sección 12 ; controla los caminos realmente modificados en el diff final. Los hooks no son un sustituto de la CI independiente.

Ejemplos para un proyecto de confianza, `.claude/settings.json` :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Y `.codex/hooks.json` :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "apply_patch",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Los dos arneses llaman a los mismos scripts (los eventos y payloads propios de las herramientas permanecen separados). Codex requiere releer y aprobar las definiciones de hooks no gestionados (`/hooks`); no desactivar este control. Un worktree puede cargar los hooks del checkout principal; comprueba las fuentes realmente ejecutadas. Los hooks y scripts de confianza deben estar protegidos de la escritura por el agente; en entorno gestionado, colocarlos fuera del worktree. No ejecuta hooks de proyecto no auditados.

Script `scripts/ai-compile-check.sh` (feedback de compilación solamente; puede ser deshabilitado si demasiado frecuente):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
logFile=$(mktemp)
trap 'rm -f "$logFile"' EXIT
# Capture the process exit code, not a pattern in the logs.
if sbt --client "Test/compile" >"$logFile" 2>&1; then
  exit 0
else
  exitCode=$?
  printf 'sbt Test/compile failed (exit %s)\n' "$exitCode" >&2
  tail -n 40 "$logFile" >&2
  exit 2
fi
```

El resultado se basa en el código de retorno de sbt, incluso sin línea `[error]`. `Test/compile` Compile las pruebas pero no las ejecute. `grep` o un pedido RTK como árbitro del éxito; conserva el código de retorno del comando original. En presencia de varias sesiones, no lanza compilaciones concurrentes al mismo servidor sbt.

Script `scripts/ai-stop-audit.sh` (llamada no bloqueada, común a los dos arneses):

```bash
#!/usr/bin/env bash
set -euo pipefail
# No transcript heuristics and no forced retry on legitimate blockers.
cat >/dev/null
printf '%s\n' '{"systemMessage":"Completion requires a fresh validation receipt for the exact candidate SHA and independent CI; report blockers without claiming done."}'
```

El Stop hook nunca busca un comando en la transcripción: una mención de `testOnly` No obligues al agente a continuar cuando un invariante o un presupuesto imponga una parada. Para completar, requiere el informe estructurado de `scripts/ai-validate.py` (sección 11) y los checks CI Las pruebas locales producidas bajo la identidad del agente son útiles para el diagnóstico, pero falsificables: la política de CI, sus scripts y sus resultados deben vivir en una frontera independiente del agente.

Un Mod Claude privilegiado o un hook no confiable puede modificar el oleoducto; conserva las restricciones externas y los controles administrados. La gate final no puede ser modificado y luego auto-aprobado por el writer. Los hooks pueden ser ignorados o no se activan según la superficie; comprueba los acontecimientos, caminos y permisos efectivos antes de la adopción.

<!-- section: s-28 -->
#### Protocolo de recuperación cuando el agente bucle

Un bucle agente (el mismo error, la misma corrección, el mismo fallo) es un modo de fallo distinto del fracaso simple. La escalada del modelo no la corrige. Aquí está el protocolo en 4 pasos:

**Paso R1 - Parada y extracción de estado (0 token adicional)**

Detén al agente de inmediato.

No cambies nada. 5 Puntos:

1. Archivos modificados hasta ahora (diff desde la base aprobada + git status)
2. Hipótesis actual sobre la causa
3. Lo que fue tentado y por qué falló.
4. La próxima acción mínima que propondrás
5. Lo que no estás seguro.

**Paso R2 Diagnóstico humano con IED (5-10 min)**

Usa IntelliJ para comprobar lo que el agente no puede ver:

- El tipo real de expresión (Ctrl+Shift+P / Tipo info)
- La resolución efectiva de un implícito/given (Ctrl+B sobre implicit)
- La jerarquía de tipos esperada vs producida
- El breakpoint debugger sobre el comportamiento inesperado

El objetivo es encontrar la información estructural que le falta al agente.

**Paso R3  la sesión fresca con contexto restringido**

/clear Nuevo prompt con el AMO:

- Objetivo (1 frase)
- El fichero o método exacto de que se trate
- El error exacto (copiado desde IDE, no desde transcripción)
- La información estructural hallada en R2
- "Sólo propone un cambio mínimo. Compile y pruebe."

**Paso R4 Si falla después de R3, escalada de modelo**

Sólo ahora se justifica la escalada de Sonnet → Opus → Fable, ya que el contexto es limpio y el problema está bien planteado.

Anti-pattern absoluto: Reanudar el mismo modelo en el mismo contexto con la esperanza de un resultado diferente. Es la definición del bucle.

> **Reanclaje periódico, el desfile medido contra la deriva larga.**
> La investigación 2026 sobre el agente drift ? (degradación del comportamiento medida en trayectorias largas y largas
> sistemas multi-agentes) converge en tres familias de mitigaciones: consolidación episódica de la historia en
> resúmenes estructurados, anclaje conductual adaptativo (reinyectación periódica de la carta y el objetivo
> corriente) y enrutado teniendo en cuenta la deriva. Traducción inmediata para tus sesiones:
> - ** re-inyecta la carta** (objetivo, no objetivos, invariantes, definición de donación) en cada hito y la vuelta de
>   Subagento no sólo al primer prompt: una restricción que ya no está en la ventana reciente ya no existe;
> - **generaliza el archivo de estado** (`MIGRATION_STATE.md`) en todo período de sesiones largo, no sólo a las misiones
>   Fable: es el ancla que sobrevive a las compacciones y a las reposiciones;
> - ** circuito breakers de doble umbral**: una advertencia sobre la repetición de un mismo tool call o de una misma
>   error y luego parada dura en la segunda repetición idéntica , en lugar de un único umbral brutal;
> - **sesión fresca en caso de bucle** : la escalada del modelo no corrige un bucle (sección 3) ; `/clear` +
>   estado + carta relegada, sí.

---

