<!-- section: chapter -->
# 1A. Vibe coding, programación asistida por IA y programación agéntica

El término **vibe coding**, popularizado por Andrej Karpathy en febrero de 2025, describía originalmente una práctica en la que el programador delega casi toda la escritura del código, acepta las propuestas del modelo y juzga el trabajo sobre todo por el resultado observable. Este enfoque funciona para prototipos desechables, proyectos exploratorios o interfaces de bajo riesgo. Como método de producción, resulta insuficiente para sistemas de negocio, financieros, sensibles a la seguridad o concebidos para perdurar.

Dos precisiones sobre el origen del término ayudan a entender el debate en 2026. Karpathy aclaró que el tuit era medio en broma y estaba pensado para proyectos desechables de fin de semana. Nunca propuso el vibe coding como método de producción. Ya en febrero de 2025, Simon Willison trazó una distinción de referencia. Aceptar los diffs sin leerlos es vibe coding. Revisar cada línea y entender qué hace es programación asistida por IA. El problema aparece cuando se omite la revisión. A finales de 2025 se incorporó el término **vibe engineering** para describir a quienes, con experiencia profesional, aceleran mucho su trabajo con agentes LLM y conservan plena responsabilidad por el software. La revisión, las pruebas y la responsabilidad distinguen las dos prácticas y son el objetivo de esta guía.

Hay que distinguir tres modos de trabajo:

| Modo                        | Control humano                                                     | Uso adaptado                                     | Riesgo principal                                           |
|-----------------------------|---------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------|
| **Vibe coding**             | Baja, validación por sensación y ejecución                       | Prototype, spike, herramienta personal desechable        | Deuda invisible, seguridad, comprensión perdida            |
| **AI-assisted engineering** | El desarrollador diseña y lee, el modelo acelera                 | Trabajo diario en código mantenido              | Automatizar las decisiones que deben seguir siendo humanas    |
| **Agentic coding**          | El agente explora, planea, modifica y prueba en un perímetro limitado | Tareas específicas con pruebas y permisos | Drive, hebilla, acción fuera de perímetro, inyección indirecta |

Para un senior Scala, el objetivo no es, por lo tanto, más vibe coding, sino un **Ingeniería de agentes controlada ** :

```text
especificación verificable
→ contexto mínimo pero suficiente
→ plan
→ permisos proporcionales
→ ejecución instrumentada
→ compilación y pruebas deterministas
→ revisión independiente
→ validación humana
```

**Evidence-driven agentic engineering**: SDD fija el contrato, el arness engineering hace que sus limitaciones sean ejecutables, y las pruebas determinan si el cambio puede avanzar. Para cada requisito, combina una prueba independiente (prueba de comportamiento, inspección, benchmark o medida runtime), el SHA realmente validado y los riesgos no cubiertos. Una afirmación del agente, una revisión sin prueba o un mero estatus verde no constituyen un oráculo. El ciclo termina después de la validación del artefacto desplegado, no simplemente en la merge (sección 15B).

<!-- section: s-1 -->
## Lo que muestra el estado del arte en 2026

1. **El modelo por sí solo no determina el éxito.** El arness, las herramientas disponibles, el debugger, la calidad del contexto y las pruebas pueden modificar los resultados casi tanto como la elección del modelo. Las comparaciones entre puntuaciones publicadas por los proveedores sólo son válidas si el arness, el esfuerzo, las herramientas y el protocolo son comparables.
2. **Los benchmarks cortos sobreestiman la autonomía larga.** Los agentes obtienen buenos resultados en salidas aisladas, pero están cayendo fuertemente en la evolución multi-archivo, larga e histórica. SWE-EVO, por ejemplo, se ocupa de tareas mucho más largas que SWE-bench y pone de relieve esta diferencia.
3. **SWE-bench Verified ya no es un buen semental único.** OpenAI ha documentado problemas de contaminación y pruebas defectuosas. Para el código, prefiere una cartera que incluye tareas de SWE-bench auditadas, Terminal-Bench, tareas de revisión y sobre todo un benchmark interno Scala No público.
4. **La productividad humana no está garantizada por una buena puntuación de agente.** Un estudio aleatorio de METR en desarrolladores experimentados en sus propios depósitos observó una desaceleración con las herramientas iniciales 2025. Los datos recogidos a continuación sugieren una posible mejora, pero METR considera que el nuevo ensayo no es fiable debido a los sesgos de selección y medidas difíciles con varios agentes competidores. Por lo tanto, todavía no existe una replicación causal propia con las herramientas de 2026. La medida local del tiempo hasta la mermelada sigue siendo indispensable. Orden de magnitud de la actualización de febrero 2026 : estimación puntual de aproximadamente 18 % de aceleración en la subhorta histórica (planteamiento de confianza −38 % à +9 % y alrededor de 4 % de nuevos participantes (IC)
   −15 % à +9 % de una señal demasiado ruidosa para concluir, que METR prefirió tratar refundiendo el protocolo en lugar de publicar un número único. Detalle decisivo para el pilotaje: en el ensayo inicial, los participantes estimaron que en promedio habían sido ~20 % más rápido gracias a la IA mientras que eran ~19 % más lentos la diferencia entre percepción y medición es la razón por la que esta guía requiere métricas locales (costo por cambio aceptado, tiempo hasta la merge) en lugar de la sensación de las sesiones.
5. **Las instrucciones de depósito sólo son útiles si están en funcionamiento.** Investigación sobre `AGENTS.md` encuentra un beneficio cuando el archivo contiene comandos, convenciones no estándar, invariantes y reglas de parada. Una larga descripción genérica de la arquitectura puede aumentar el contexto sin mejorar el resultado.
6. **El multiagente no es un multiplicador automático de inteligencia.** Ayuda cuando las subtareas son realmente independientes, las responsabilidades y los archivos están separados y un agente raíz sintetiza. En un estado mutable compartido aumenta conflictos, costes y errores de coordinación.
7. **Un parche técnicamente correcto no es suficiente para evaluar a un agente.** También mide el cumplimiento del scope, de las normas de parada y de los convenios, la calidad del plan, la capacidad de señalar la incertidumbre y el coste de revisión humana. Dos agentes que pasan las mismas pruebas pueden tener un valor muy diferente si uno genera el doble de rework o de cambios fuera del perímetro.
8. **La memoria, los esquís y las reglas persistentes se convierten en una superficie de ingeniería.** Los agentes capaces de hacer evolucionar su propia memoria, sus esquís o su enrutamiento nunca deben auto-promover estos cambios. Cualquier evolución persistente debe ser difamable, versátil, comprobable, reevaluada y reversible antes de activar.
9. **Una gran ventana de contexto no elimina el *context rot*.** Evaluación 2026 distinguir la capacidad física de la ventana y la calidad efectiva de uso de su contenido: con la misma tarea, más tokens pueden degradar recuperación, respeto de las tensiones y razonamiento mucho antes del límite máximo. Por lo tanto, el objetivo correcto no es cumplir 1M tokens  ¡Pero mantener un **working set minimum and decisions**. Los subagentes aislados son un desfile estructural: consumen localmente muchos contextos y sólo remiten al padre un resultado condensado.

Conclusión: el nivel fronterizo aumenta la superficie de posibles tareas, pero la calidad de la ingeniería alrededor del agente sigue siendo el factor de control más importante.

<!-- section: s-2 -->
### Complemento metodológico

> **SWE-bench Pro no sustituye solo a SWE-bench Verified.** OpenAI ahora considera que alrededor de 30 % de las tareas de
> SWE-bench Pro también son defectuosas: pruebas demasiado estrictas, requisitos ocultos ausentes del prompt, cobertura
> La auditoría del 8 Julio 2026
> (pipelina automatizada: 27,4 % de 731 tareas públicas marcadas; anotaciones por cinco ingenieros mayores: 34,1 %)
> por otra parte, ha conducido OpenAI à **retirar explícitamente su recomendación** hacer de ello una evaluación de codificación de
> Referencia:  la señal más fuerte que la única estimación. La buena cartera de evaluación combina varios ejes
> En lugar de un nuevo
> Clasificación única.

| Eje de medición                | Evaluación útil                 | Lo que revela                                                                               |
|------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------|
| Correctivo de depósito clásico | SWE-bench, con auditoría de tareas | Capacidad de reparación en salidas aisladas                                                       |
| Tarea original larga       | **DeepSWE**                      | Contaminación reducida, auditores escritos para aceptar varias soluciones válidas           |
| Colaboración iterativa      | **SWE-Interact** o SWE-Together | Descubrimiento de intenciones, memorización de las limitaciones, necesidad de correcciones humanas            |
| Explorando el depósito         | **SWE-Explore**                  | Ubicación a nivel de líneas y eficacia del contexto                                     |
| Ciclo completo                | **SWE-Cycle**                    | Reconstrucción ambiental, implementación y generación de pruebas en una misma trayectoria |
| Realidad de tu trabajo       | **Benchmark Scala privada**        | Costo y calidad en Play, Pekko, Tapir, Spark, implicaciones, serialización y construcción reales          |

Para una tarea de código, mida el **costo por cambio aceptado** ; para pilotar la entrega, el **costo por cambio desplegado y estable** (sección 15B), no la tasa bruta de éxito:

```text
coste por cambio aceptado
= tokens + latencia + minutos de trabajo humano + CI + retrabajo + defectos no detectados
```

Usa una unidad común para agregar estos costes (por ejemplo, euros con un coste por hora explícito), o mantiene los componentes separados. Los tokens y los minutos no suben directamente. Para el coste hasta la producción, añade despliegue, validación runtime, rollback/hotfix y defectos observados durante una ventana fijada antes de la medición. Sólo cuenta como estable un cambio que haya terminado esta ventana.

No busques una productividad global IA **greenfield, mantenimiento, legacy, bugfix, migración, refactor y código crítico** : los estudios 2026 consiguen resultados contradictorios precisamente porque no miden siempre las mismas tareas, desarrolladores o costes de revisión.

<!-- section: s-3 -->
### Un benchmark verde no es todavía un diff mergeable

Evaluación de la METR 296 PRs generados por agentes constató que el grado SWE-bench concedía por término medio **24,2 puntos de éxito más** que los mantenedores encargados de evaluar si el cambio era realmente útil y mergeable; aproximadamente la mitad de los PRs que pasaban las pruebas no habrían sido arruinados. La muestra sólo se refiere a tres depósitos, modelos anteriores a la generación más reciente y un solo ensayo sin iteración en el feedback manoteniente: no es un límite fundamental de capacidad, pero esto invalida la equivalencia ingenua `tests du benchmark passants = changement acceptable`.

En las tareas largas, SlopCodeBench observa además una acumulación de duplicación, verbosidad y erosión estructural a medida que los checkpoints se encadenan. Un rápido demandando calidad reduce algunos defectos al principio sin eliminar su crecimiento. El buen régimen de prueba acumula, por lo tanto, cuatro barreras independientes:

```text
contrato de negocio explícito
→ reproducción que falla antes del parche
→ pruebas deterministas, propiedades y pruebas de mutación
→ revisión del diff, de su alcance y de su mantenibilidad por una persona responsable
```

Las puntuaciones de benchmark sirven para el enrutamiento y los experimentos; nunca deben convertirse en un permiso de autonomía o de merge.

> **Diferencia entre escribir y entregar.** El papeleo de la NBER *Writing Code vs. Shipping Code* observa, en más de
> 500 000 desarrolladores GitHub, un aumento estimado de la actividad de los commits mucho mayor que en los
> proyectos y las liberaciones. El estudio sigue siendo observacional con emparejamiento: no demuestra un efecto causal
> Así que limita el WIP a la capacidad de repaso y entrega, y mide hasta la producción.

<!-- section: s-4 -->
### Guardería de producción para el vibe coding

Los estudios empíricos de 2026 sobre aplicaciones realmente ?vb codificadas ? • recuperan familias de defectos recurrentes: lógica provisional dejada en producción, entradas no filtradas, secretos expuestos, olvido de tensiones a lo largo de las torres y optimización local que degrada el sistema global. Un modelo más fuerte o mejor prompt reduce estos defectos, pero no los elimina.

> **Órdenes de magnitud medidos en 2026.** La auditoría de 200 aplicaciones realmente  ¡vb codificadas y desplegadas  ¡a muy bien
> (1 471 vulnerabilidades validadas) encuentra al menos una vulnerabilidad en **90 % de depósitos**, de los cuales más de tres
> cuartos de gravedad alta o crítica; el control de acceso roto aparece en 75,5 % de los depósitos, es decir, alrededor de 20 ¡
> la línea de base OWASP 2025. Un escaneo independiente de 1 400+ aplicaciones da lugar al mismo orden de magnitud (65 %
> presentan al menos un problema de seguridad, 58 % como mínimo una vulnerabilidad crítica, 400+ secretos expuestos).
> El análisis de las causas profundas clasifica estos defectos en tres familias **memoria** (Olvidadas entre las
> torres), **Objetivo** (optimación local que degrada el sistema global) y **conocimiento** (patternos peligrosos)
> reproducidos): exactamente los tres mecanismos que los gatas deterministas y la revista humana de esta guía deben
> interrumpir, ya que ningún prompt los corrige de forma duradera.

```text
Prototipo con vibe coding
→ sin datos ni claves de producción
→ pruebas funcionales + seguridad + rendimiento + mantenibilidad
→ revisión humana del diff y las dependencias
→ migración al flujo agéntico controlado
→ solo entonces: despliegue
```

Una sesión de vibe coding nunca debe crecer directamente en producción, incluso cuando la demostración parece funcional. La frontera de producción es un **cambio de régimen de prueba**, no un paso más del gato.

